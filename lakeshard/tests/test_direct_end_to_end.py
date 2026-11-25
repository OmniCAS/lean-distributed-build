"""The direct `lean` backend end to end: pull workers over HTTP, outputs identical to `lake build`.
Needs the Lean toolchain; skipped otherwise."""
import json
import os
import subprocess
import sys
import threading
import time
import urllib.request

import pytest

from lakeshard import api
from lakeshard.synth import random_dag, write_project


@pytest.fixture
def proj_and_ref(tmp_path, tc_bin):
    proj = tmp_path / "proj"
    write_project(str(proj), random_dag(40, max_imports=3, locality=8), warn_every=5)
    ref = api.reference_build(str(proj), str(tmp_path / "ref"))
    assert ref["ok"], ref
    return proj, tmp_path / "ref"


@pytest.mark.lean
@pytest.mark.parametrize("storage", ["store-http", "store-dir", "shared"])
def test_direct_equals_lake_build(tmp_path, proj_and_ref, storage):
    """store-http (default): workers keep their own build directories and reach the store only
    through the coordinator's HTTP endpoints; store-dir: a store directory; shared: one build dir."""
    proj, ref = proj_and_ref
    kw = {"store-http": {}, "store-dir": {"store": str(tmp_path / "dirstore")},
          "shared": {"storage": "shared"}}[storage]
    rep = api.build_direct(str(proj), str(tmp_path / "work"), workers=3, slots=2, threads=1, fail_once={"Synth.M7"},
                           **kw)
    assert rep["ok"], rep
    assert rep["modules_built"] == 40 and rep["slots"] == 6
    assert [f["module"] for f in rep["failures"]] == ["Synth.M7"]  # injected, then retried
    events = [json.loads(x) for x in open(tmp_path / "work" / "events.jsonl")]
    m7 = [e for e in events if e.get("event") == "result" and e["module"] == "Synth.M7"]
    assert [e["ok"] for e in m7] == [False, True] and m7[0]["worker"] != m7[1]["worker"]
    assert rep["lower_bound"]["bound_s"] > 0 and rep["lower_bound"]["ratio"] >= 1.0
    _check_records(tmp_path / "work" / "modules.jsonl", rep)
    if storage == "store-http":
        assert rep["store"].startswith("http://") and rep["store_server"]["objects_get"] > 0
        assert rep["totals"]["fetched_bytes"] > 0
        for w in ("w0", "w1", "w2"):  # no worker has a store of its own
            assert not os.path.exists(tmp_path / "work" / "workers" / w / "store")
    if storage == "shared":
        out_dir = rep["build_dir"]
        assert not os.listdir(os.path.join(out_dir, ".lakeshard-tmp"))  # temporary files cleaned up
    else:
        store = rep["store_root"] or rep["store"]
        asm = api.assemble(str(proj), store, str(tmp_path / "assembled"), manifest=rep["manifest"])
        assert asm["ok"], asm
        out_dir = tmp_path / "assembled"
    ver = api.verify(str(proj), str(out_dir), reference=str(ref), leanchecker_jobs=4, lake_check=False)
    assert ver["compare"]["ok"] and ver["compare"]["identical_files"] == 120, ver["compare"]
    assert ver["leanchecker"]["ok"] and ver["leanchecker"]["ok_runs"] == 40, ver["leanchecker"]


def _check_records(path, rep):
    """One run record per attempt, times ordered on the coordinator's clock (same machine: offset 0)."""
    recs = [json.loads(x) for x in open(path)]
    assert len(recs) == rep["totals"]["attempts"] == 41
    ok = [r for r in recs if r["ok"]]
    assert len(ok) == 40 and len({r["module"] for r in ok}) == 40
    for r in ok:
        assert r["host"] and r["threads"] == 1 and r["slots"] == 2 and r["clock_offset_s"] == 0.0
        assert r["ready_t"] <= r["dispatch_t"] <= r["start_t"] <= r["lean_start_t"] <= r["lean_end_t"]
        assert r["lean_end_t"] <= r["end_t"] <= r["report_t"] + 1e-3 and r["report_t"] <= r["done_t"]
        assert r["lean_s"] > 0 and r["cpu_s"] > 0 and r["max_rss_bytes"] > 0 and r["output_bytes"] > 0


def _post(url, token, path, body):
    req = urllib.request.Request(url + path, data=json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


@pytest.mark.lean
def test_lost_worker_and_remote_style_worker(tmp_path, proj_and_ref):
    """A worker takes tasks and vanishes; a worker started separately (as on another machine) joins
    with the coordinator's URL and token and finishes the build."""
    proj, ref = proj_and_ref
    work = tmp_path / "work"
    out = {}
    t = threading.Thread(target=lambda: out.update(api.build_direct(
        str(proj), str(work), local_workers=0, lease_s=3.0, heartbeat_s=0.5, wait_timeout_s=300)), daemon=True)
    t.start()
    cj = work / "coordinator.json"
    for _ in range(200):
        if cj.exists():
            break
        time.sleep(0.05)
    info = json.loads(cj.read_text())
    token = open(info["token_file"]).read().strip()
    from lakeshard.fingerprint import fingerprint
    from lakeshard.project import LakeProject
    fp = fingerprint(LakeProject.load(str(proj)), info["toolchain_bin"])  # the ghost's environment is right
    _post(info["url"], token, "/v1/register", {"worker": "ghost", "slots": 2, "fingerprint": fp})
    lost = _post(info["url"], token, "/v1/claim", {"worker": "ghost", "n": 2, "wait_s": 5})["tasks"]
    assert lost
    src = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
    env = dict(os.environ, PYTHONPATH=src, PYTHONDONTWRITEBYTECODE="1")
    w = subprocess.run([sys.executable, "-m", "lakeshard", "worker", "serve", "--coordinator", info["url"],
                        "--id", "remote1", "--slots", "3", "--threads", "1", "--token-file", info["token_file"],
                        "--workspace", str(tmp_path / "remote1")], env=env, timeout=300, capture_output=True, text=True)
    t.join(timeout=60)
    assert w.returncode == 0, w.stderr
    assert out["ok"], out
    assert {f["module"] for f in out["failures"]} == {x["module"] for x in lost}
    assert all(f.get("reason") == "worker lost" for f in out["failures"])
    assert out["store"].startswith("http://")  # the separately started worker used the HTTP store with the token
    asm = api.assemble(str(proj), out["store_root"], str(tmp_path / "assembled"), manifest=out["manifest"])
    assert asm["ok"], asm
    ver = api.verify(str(proj), str(tmp_path / "assembled"), reference=str(ref), lake_check=False)
    assert ver["compare"]["ok"] and ver["compare"]["identical_files"] == 120, ver["compare"]
