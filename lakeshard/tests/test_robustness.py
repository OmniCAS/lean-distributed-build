"""Repository in, cache out, and the robustness rules (docs/plan.zh.md section 3), end to end with
Lean. Each test builds a small synthetic project; skipped without the toolchain."""
import json
import os
import shutil
import signal
import subprocess
import sys
import threading
import time

import pytest

from lakeshard import api
from lakeshard.fingerprint import fingerprint, module_keys
from lakeshard.project import LakeProject
from lakeshard.synth import random_dag, write_project
from lakeshard.verify import compare_builds

SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")


def _proj(tmp_path, n=24, work=3, name="proj"):
    proj = tmp_path / name
    write_project(str(proj), random_dag(n, max_imports=3, locality=6), work=[work] * n, warn_every=5)
    return proj


def _ref(tmp_path, proj):
    ref = api.reference_build(str(proj), str(tmp_path / "ref"))
    assert ref["ok"], ref
    return tmp_path / "ref"


def _assemble(proj, rep, dest):
    asm = api.assemble(str(proj), rep["store_root"], str(dest), manifest=rep["manifest"])
    assert asm["ok"], asm
    return dest


def test_keys_change_exactly_downstream(tmp_path, tc_bin):
    proj = _proj(tmp_path)
    p = LakeProject.load(str(proj))
    g = p.graph()
    fp = fingerprint(p, tc_bin)
    k1 = module_keys(g, p, fp["sha256"])
    assert k1 == module_keys(g, p, fp["sha256"])  # deterministic
    m = next(x for x in g.order if g.children()[x])
    with open(proj / g.modules[m].path, "a") as fh:
        fh.write("\ntheorem extra : 2 = 2 := rfl\n")
    k2 = module_keys(g, p, fp["sha256"])
    changed = {x for x in g.modules if k1[x] != k2[x]}
    assert changed == {m} | {x for x in g.modules if m in g.closure([x])}


@pytest.mark.lean
def test_run_restore_and_incremental(tmp_path, tc_bin):
    """run: build, seal (stock Lake writes its traces), kernel check, pack; restore into a fresh
    checkout at another path: `lake build` compiles nothing. Then one edited file rebuilds only
    its downstream modules (item 1: the store is the truth)."""
    proj = _proj(tmp_path)
    ref = _ref(tmp_path, proj)
    res = api.run(str(proj), str(tmp_path / "work"), workers=2, slots=2, threads=1, leanchecker_jobs=2)
    assert res["ok"], res
    assert res["build"]["built"] == 24 and res["seal"]["from_store"] == 24 and res["seal"]["compiled_by_lean"] == 0
    assert res["seal"]["no_build_check"]["ok"] and res["kernel"]["ok_runs"] == 24
    sealed = tmp_path / "work" / "sealed"
    g = LakeProject.load(str(proj)).graph()
    assert compare_builds(g, str(ref), str(sealed))["ok"]
    # restore into a copy of the sources at another path
    copy = tmp_path / "elsewhere" / "proj"
    shutil.copytree(proj, copy, ignore=shutil.ignore_patterns(".lake"))
    r = api.restore(res["cache"]["cache"], str(copy))
    assert r["ok"] and r["lake_no_build"]["ok"] and not r["same_path"], r
    out = subprocess.run([os.path.join(tc_bin, "lake"), "build"], cwd=copy, capture_output=True, text=True)
    assert out.returncode == 0 and "Built" not in out.stdout, out.stdout[-500:]
    # incremental: edit one module, run again
    m = next(x for x in g.order if g.children()[x] and g.modules[x].imports)
    with open(proj / g.modules[m].path, "a") as fh:
        fh.write("\ntheorem extra : 2 = 2 := rfl\n")
    down = {m} | {x for x in g.modules if m in g.closure([x])}
    res2 = api.run(str(proj), str(tmp_path / "work"), workers=2, slots=2, threads=1)
    assert res2["ok"], res2
    assert res2["build"]["built"] == len(down) and res2["build"]["from_store"] == 24 - len(down)
    assert res2["seal"]["from_store"] == len(down)  # Lake found the other modules up to date
    assert res2["seal"]["no_build_check"]["ok"]


@pytest.mark.lean
def test_restore_refuses_other_environment_and_corrupt_cache(tmp_path, tc_bin, monkeypatch):
    proj = _proj(tmp_path, n=8)
    res = api.run(str(proj), str(tmp_path / "work"), workers=1, slots=2)
    assert res["ok"], res
    cache = res["cache"]["cache"]
    copy = tmp_path / "copy"
    shutil.copytree(proj, copy, ignore=shutil.ignore_patterns(".lake"))
    monkeypatch.setenv("LAKESHARD_TEST_FINGERPRINT_SALT", "another machine")
    r = api.restore(cache, str(copy))
    assert not r["ok"] and "environment" in r["refused"]
    monkeypatch.delenv("LAKESHARD_TEST_FINGERPRINT_SALT")
    man = json.load(open(os.path.join(cache, "manifest.json")))
    f = next(x for x in man["files"] if x["path"].endswith(".olean"))
    obj = os.path.join(cache, "objects", f["sha256"][:2], f["sha256"])
    os.chmod(obj, 0o644)
    with open(obj, "r+b") as fh:
        fh.write(b"\0" * 16)
    with pytest.raises(Exception, match="corrupt"):
        api.restore(cache, str(copy))


@pytest.mark.lean
def test_resume_after_the_coordinator_is_killed(tmp_path):
    """Kill the whole build (coordinator and workers) halfway; the rerun builds only the rest
    (item 1) and the result is identical to `lake build` (item 2)."""
    proj = _proj(tmp_path, n=40, work=25)
    ref = _ref(tmp_path, proj)
    work = tmp_path / "work"
    env = dict(os.environ, PYTHONPATH=SRC, PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.Popen([sys.executable, "-m", "lakeshard", "build", str(proj), "--backend", "lean", "--work",
                          str(work), "--workers", "2", "--slots", "1", "--threads", "1"], env=env,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    t0 = time.time()
    while time.time() - t0 < 120:
        ev = work / "events.jsonl"
        if ev.exists() and sum(1 for x in open(ev) if '"event": "result"' in x and '"ok": true' in x) >= 12:
            break
        time.sleep(0.2)
    os.killpg(p.pid, signal.SIGKILL)
    p.wait()
    rep = api.build_direct(str(proj), str(work), workers=2, slots=2, threads=1)
    assert rep["ok"], rep
    assert rep["from_store"] >= 12 and rep["built"] == 40 - rep["from_store"]
    out = _assemble(proj, rep, tmp_path / "assembled")
    cmp = compare_builds(LakeProject.load(str(proj)).graph(), str(ref), str(out))
    assert cmp["ok"] and cmp["identical_files"] == 120, cmp


@pytest.mark.lean
def test_source_error_is_isolated_and_classified(tmp_path):
    """A module that fails on two different workers is a source problem: only its importers are
    skipped, everything else is built and the report lists it (item 3)."""
    proj = _proj(tmp_path, n=20)
    g = LakeProject.load(str(proj)).graph()
    bad = next(x for x in g.order if g.children()[x] and g.modules[x].imports)
    with open(proj / g.modules[bad].path, "a") as fh:
        fh.write("\ntheorem broken : 1 = 2 := rfl\n")
    down = {x for x in g.modules if bad in g.closure([x])}
    rep = api.build_direct(str(proj), str(tmp_path / "work"), workers=3, slots=1, threads=1)
    assert not rep["ok"]
    assert rep["failed_modules"] == {bad: "source"}
    assert set(rep["skipped_modules"]) == down and rep["skipped_count"] == len(down)
    assert rep["modules_built"] == 20 - 1 - len(down)
    tries = [f for f in rep["failures"] if f["module"] == bad]
    assert len(tries) == 2 and tries[0]["worker"] != tries[1]["worker"] and "lean exited with 1" in tries[0]["error"]


@pytest.mark.lean
def test_worker_with_another_environment_is_refused(tmp_path):
    """Item 4: a worker whose environment fingerprint differs gets no work and exits."""
    proj = _proj(tmp_path, n=10)
    work = tmp_path / "work"
    out = {}
    t = threading.Thread(target=lambda: out.update(api.build_direct(str(proj), str(work), local_workers=0,
                                                                     wait_timeout_s=120)), daemon=True)
    t.start()
    for _ in range(200):
        if (work / "coordinator.json").exists():
            break
        time.sleep(0.05)
    info = json.loads((work / "coordinator.json").read_text())

    def worker(name, extra_env):
        env = dict(os.environ, PYTHONPATH=SRC, PYTHONDONTWRITEBYTECODE="1", **extra_env)
        return subprocess.run([sys.executable, "-m", "lakeshard", "worker", "serve", "--coordinator", info["url"],
                               "--id", name, "--slots", "2", "--token-file", info["token_file"], "--workspace",
                               str(tmp_path / name)], env=env, capture_output=True, text=True, timeout=120)

    odd = worker("odd", {"LAKESHARD_TEST_FINGERPRINT_SALT": "different"})
    assert odd.returncode == 3 and "fingerprint" in odd.stderr
    good = worker("good", {})
    assert good.returncode == 0, good.stderr
    t.join(60)
    assert out["ok"] and "odd" in out["refused_workers"] and "test_salt" in out["refused_workers"]["odd"]["parts"]


@pytest.mark.lean
def test_corrupt_object_in_the_store_is_rebuilt(tmp_path):
    """Item 5: an import whose stored object fails its sha256 is noticed by the worker that fetches
    it; the coordinator drops the record and the bad object, rebuilds that module, then continues."""
    proj = _proj(tmp_path, n=16)
    ref = _ref(tmp_path, proj)
    work = tmp_path / "work"
    rep = api.build_direct(str(proj), str(work), workers=2, slots=2, threads=1)
    assert rep["ok"]
    g = LakeProject.load(str(proj)).graph()
    man = json.load(open(rep["manifest"]))["modules"]
    root = next(x for x in g.order if not g.modules[x].imports and g.children()[x])
    child = g.children()[root][0]
    h = __import__("hashlib").sha1(man[root].encode()).hexdigest()
    rec = json.load(open(work / "store" / "records" / h[:2] / (h + ".json")))
    f = next(x for x in rec["files"] if x["path"].endswith(".olean"))
    obj = work / "store" / "objects" / f["sha256"][:2] / f["sha256"]
    data = bytearray(obj.read_bytes())
    data[100:116] = b"\xff" * 16  # same size: the cheap size check at start does not notice
    obj.write_bytes(bytes(data))
    with open(proj / g.modules[child].path, "a") as fh:  # the child must be rebuilt and fetch the root
        fh.write("\ntheorem extra : 3 = 3 := rfl\n")
    rep2 = api.build_direct(str(proj), str(work), workers=2, slots=2, threads=1)
    assert rep2["ok"], rep2
    events = [json.loads(x) for x in open(work / "events.jsonl")]
    assert any(e.get("event") == "invalidated" and e["module"] == root for e in events)
    assert any(x.get("kind") == "corrupt" for x in rep2["failures"])
    out = _assemble(proj, rep2, tmp_path / "assembled")
    ref2 = api.reference_build(str(proj), str(tmp_path / "ref2"))
    assert ref2["ok"]
    cmp = compare_builds(g, str(tmp_path / "ref2"), str(out))
    assert cmp["ok"], cmp


@pytest.mark.lean
def test_lakefile_lean_project(tmp_path, tc_bin):
    """A project configured with lakefile.lean: translated by `run`, built, sealed, restored into a
    checkout that still has only its lakefile.lean, where stock Lake is up to date."""
    proj = _proj(tmp_path, n=12)
    (proj / "lakefile.toml").unlink()
    (proj / "lakefile.lean").write_text(
        'import Lake\nopen Lake DSL\n\npackage synth where\n  moreLeanArgs := #["--tstack=400000"]\n'
        '  leanOptions := #[⟨`autoImplicit, false⟩]\n\n@[default_target]\nlean_lib Synth where\n'
        '  globs := #[.submodules `Synth]\n')
    res = api.run(str(proj), str(tmp_path / "work"), workers=2, slots=2, threads=1)
    assert res["ok"], res
    assert res["translated_config"].endswith(os.path.join(".lake", "lakeshard", "lakefile.toml"))
    assert res["seal"]["from_store"] == 12 and res["seal"]["no_build_check"]["ok"]
    copy = tmp_path / "copy"
    shutil.copytree(proj, copy, ignore=shutil.ignore_patterns(".lake"))
    r = api.restore(res["cache"]["cache"], str(copy))
    assert r["ok"] and r["lake_no_build"]["ok"], r  # Lake with the original lakefile.lean agrees
    out = subprocess.run([os.path.join(tc_bin, "lake"), "build"], cwd=copy, capture_output=True, text=True)
    assert out.returncode == 0 and "Built" not in out.stdout, out.stdout[-500:]
