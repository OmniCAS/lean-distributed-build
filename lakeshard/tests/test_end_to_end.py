"""Stage (a)+(b): a tiny synthetic project, built by several local worker processes, assembled,
and compared with a plain `lake build`. Needs the Lean toolchain; skipped otherwise."""
import pytest

from lakeshard import api
from lakeshard.synth import random_dag, write_project


@pytest.mark.lean
@pytest.mark.parametrize("schedule,fail", [("static", "s00001"), ("dynamic", "b000002")])
def test_distributed_equals_lake_build(tmp_path, tc_bin, schedule, fail):
    proj = tmp_path / "proj"
    write_project(str(proj), random_dag(40, max_imports=3, locality=8), warn_every=5)
    ref = api.reference_build(str(proj), str(tmp_path / "ref"))
    assert ref["ok"], ref
    rep = api.build(str(proj), str(tmp_path / "work"), workers=3, threads=2, schedule=schedule, shards=9,
                    batch_cost=15, fail_once={fail})
    assert rep["ok"], rep
    assert rep["modules_built"] == 40
    assert any(f["shard"] == fail for f in rep["failures"])  # injected failure was retried
    asm = api.assemble(str(proj), rep["store"], str(tmp_path / "assembled"))
    assert asm["ok"], asm
    ver = api.verify(str(proj), str(tmp_path / "assembled"), reference=str(tmp_path / "ref"), leanchecker_jobs=4)
    assert ver["lake_no_build"]["ok"], ver
    assert ver["compare"]["ok"] and ver["compare"]["identical_files"] > 0, ver["compare"]
    assert ver["leanchecker"]["ok"] and ver["leanchecker"]["ok_runs"] == 40, ver["leanchecker"]
