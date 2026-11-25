"""The coordinator's HTTP service with hand-driven workers (no Lean needed)."""
import json
import os
import threading
import time
import urllib.error
import urllib.request

import pytest

from lakeshard.project import LakeProject
from lakeshard.protocol import BuildConfig, FileRef, ModuleResult, to_dict
from lakeshard.scheduler import ModuleScheduler
from lakeshard.service import BuildService
from lakeshard.synth import random_dag, write_project


def _post(url, path, body, token="tok"):
    req = urllib.request.Request(url + path, data=json.dumps(to_dict(body)).encode(), method="POST",
                                 headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


@pytest.fixture
def service(tmp_path):
    proj = tmp_path / "proj"
    write_project(str(proj), random_dag(12, max_imports=2, locality=3))
    g = LakeProject.load(str(proj)).graph()
    build = tmp_path / "build"
    cfg = BuildConfig("r1", str(proj), "/tc", "shared", str(build), visibility_timeout_s=1.5, visibility_poll_s=0.1)
    s = ModuleScheduler(g, {m: 1.0 for m in g.modules}, retries=1, lease_s=4.0)
    svc = BuildService(g, s, cfg, str(tmp_path / "work"), token="tok")
    svc.start()
    yield svc, g, build
    svc.stop()


def _outputs(build, m, write=True, delay=0.0):
    rel = os.path.join("lib", "lean", *m.split(".")) + ".olean"
    p = build / rel

    def go():
        time.sleep(delay)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b"olean")

    if write and delay:
        threading.Thread(target=go).start()
    elif write:
        go()
    return [FileRef(rel, "0" * 64, 5)]


def test_token_required(service):
    svc, _g, _b = service
    with pytest.raises(urllib.error.HTTPError) as e:
        _post(svc.url, "/v1/register", {"worker": "x", "slots": 1}, token="wrong")
    assert e.value.code == 401


def test_full_run_with_confirmation(service):
    svc, g, build = service
    cfg = _post(svc.url, "/v1/register", {"worker": "a", "slots": 3})["config"]
    assert cfg["build_dir"] == str(build) and cfg["storage"] == "shared"
    done, n = set(), 0
    while True:
        resp = _post(svc.url, "/v1/claim", {"worker": "a", "n": 3, "wait_s": 1})
        if resp["shutdown"]:
            break
        for t in resp["tasks"]:
            assert set(g.modules[t["module"]].imports) <= done
            n += 1
            if n == 1:  # first report claims success but writes nothing: must be refused and retried
                outs = _outputs(build, t["module"], write=False)
            elif n == 2:  # outputs appear late (as on an NFS client): accepted within the timeout
                outs = _outputs(build, t["module"], delay=0.5)
            else:
                outs = _outputs(build, t["module"])
            res = ModuleResult(t["task_id"], t["module"], "a", True, attempt=t["attempt"], outputs=outs)
            ans = _post(svc.url, "/v1/report", {"result": res})
            assert ans["accepted"]
            if n > 1:
                done.add(t["module"])
    assert svc.wait(5)
    rep = svc.report_dict()
    assert rep["ok"] and rep["modules_built"] == len(g.modules)
    assert rep["totals"]["failed_attempts"] == 1 and "not visible" in rep["failures"][0]["error"]
    assert rep["totals"]["confirm_s"] >= 0.4  # waited for the late file


def test_lost_worker_is_replaced(service):
    svc, g, build = service
    _post(svc.url, "/v1/register", {"worker": "dead", "slots": 2})
    lost = _post(svc.url, "/v1/claim", {"worker": "dead", "n": 2, "wait_s": 1})["tasks"]
    assert lost
    _post(svc.url, "/v1/register", {"worker": "b", "slots": 2})
    seen = set()
    t_end = time.time() + 30
    while time.time() < t_end:
        _post(svc.url, "/v1/heartbeat", {"worker": "b", "running": []})
        resp = _post(svc.url, "/v1/claim", {"worker": "b", "n": 2, "wait_s": 1})
        if resp["shutdown"]:
            break
        for t in resp["tasks"]:
            seen.add(t["module"])
            res = ModuleResult(t["task_id"], t["module"], "b", True, outputs=_outputs(build, t["module"]))
            _post(svc.url, "/v1/report", {"result": res})
    assert {t["module"] for t in lost} <= seen  # given to b after the lease of `dead` ran out
    rep = svc.report_dict()
    assert rep["ok"]
    assert {f["module"] for f in rep["failures"] if f.get("reason") == "worker lost"} == {t["module"] for t in lost}
    # the dead worker's late report is ignored
    late = ModuleResult(lost[0]["task_id"], lost[0]["module"], "dead", True, outputs=_outputs(build, lost[0]["module"]))
    assert _post(svc.url, "/v1/report", {"result": late})["accepted"] is False
