import random

import pytest

from lakeshard.plan import check_plan, estimate_costs, make_plan, shard_needs
from lakeshard.project import LakeProject
from lakeshard.synth import random_dag, write_project


def _graph(tmp_path, n, **kw):
    write_project(str(tmp_path), random_dag(n, **kw))
    return LakeProject.load(str(tmp_path)).graph()


@pytest.mark.parametrize("n,shards", [(1, 1), (30, 1), (30, 5), (200, 8), (200, 200), (400, 37)])
def test_plan_is_partition_and_acyclic(tmp_path, n, shards):
    g = _graph(tmp_path, n, max_imports=5, locality=15)
    plan = make_plan(g, estimate_costs(g), shards=shards)
    check_plan(g, plan)  # raises on overlap, missing deps or cycles
    assert sum(len(s.modules) for s in plan.shards) == n
    assert plan.stats["shard_critical_path_s"] >= plan.stats["module_critical_path_s"] - 1e-6


def test_random_costs_many_graphs(tmp_path):
    rnd = random.Random(7)
    for k in range(15):
        d = tmp_path / f"g{k}"
        g = _graph(d, rnd.randint(5, 150), max_imports=rnd.randint(1, 8), locality=rnd.randint(2, 60),
                   random_state=k)
        costs = {m: rnd.uniform(0.1, 10) for m in g.modules}
        plan = make_plan(g, costs, target_cost=rnd.uniform(1, 60))
        check_plan(g, plan)


def test_needs_are_outside_closure(tmp_path):
    g = _graph(tmp_path, 120, max_imports=4)
    plan = make_plan(g, estimate_costs(g), shards=6)
    needs = shard_needs(g, plan)
    for s in plan.shards:
        assert not set(needs[s.id]) & set(s.modules)
        assert g.closure(s.modules) - set(s.modules) == set(needs[s.id])


def test_project_reads_globs(tmp_path):
    write_project(str(tmp_path), random_dag(10))
    p = LakeProject.load(str(tmp_path))
    g = p.graph()
    assert p.package == "synth" and len(g.modules) == 10 and len(g.targets) == 10
    assert g.order.index("Synth.M0") < g.order.index("Synth.M9") or "Synth.M0" not in g.modules["Synth.M9"].imports
    cfg = p.worker_lakefile("/x/y")
    assert cfg.startswith('buildDir = "/x/y"\n')


def test_split_prefix_modules():
    from lakeshard.verify import split_prefix_modules
    mods = ["Foo", "Foo.A", "Foo.A.B", "Bar.X", "Bar.Y", "FooBar"]
    assert split_prefix_modules(mods) == (["Foo.A.B", "Bar.X", "Bar.Y", "FooBar"], ["Foo", "Foo.A"])


def test_graph_of_chosen_targets(tmp_path):
    write_project(str(tmp_path), random_dag(60, max_imports=3, locality=5))
    p = LakeProject.load(str(tmp_path))
    full = p.graph()
    top = full.order[-1]
    g = p.graph([top])
    assert set(g.modules) == {top} | full.closure([top]) and g.targets == [top]
    import pytest
    with pytest.raises(Exception, match="no source file"):
        p.graph(["Synth.Nope"])
