"""The direct backend's scheduler as a state machine (no Lean, no processes)."""
import random

from lakeshard.project import LakeProject
from lakeshard.scheduler import ModuleScheduler, lower_bound
from lakeshard.synth import random_dag, write_project


def _graph(tmp_path, n, **kw):
    write_project(str(tmp_path), random_dag(n, **kw))
    return LakeProject.load(str(tmp_path)).graph()


def _simulate(g, s, workers, fail, rnd, now=0.0):
    """Run the scheduler to completion; `fail(module, attempt, worker)` decides failures."""
    dispatched = {}
    running = []
    while not s.done():
        for w in workers:
            for t in s.claim(w, 2, now):
                imps = g.modules[t.module].imports
                assert all(s.state[u] == "done" for u in imps), "dispatched before its imports were done"
                dispatched[t.module] = dispatched.get(t.module, 0) + 1
                running.append((t, w))
        assert running or s.done(), "stuck: nothing running and not done"
        rnd.shuffle(running)
        t, w = running.pop()
        now += 1.0
        s.complete(t.task_id, not fail(t.module, t.attempt, w), now, "boom")
    return dispatched


def test_random_runs_with_failures(tmp_path):
    rnd = random.Random(3)
    for k in range(10):
        g = _graph(tmp_path / f"g{k}", rnd.randint(10, 120), max_imports=rnd.randint(1, 5),
                   locality=rnd.randint(2, 30), random_state=k)
        costs = {m: rnd.uniform(0.1, 5) for m in g.modules}
        bad = set(rnd.sample(sorted(g.modules), 2))  # fail on every attempt
        flaky = set(rnd.sample(sorted(g.modules), 3)) - bad  # fail on the first attempt only
        s = ModuleScheduler(g, costs, retries=2)
        for w in ("a", "b", "c"):
            s.register(w, 2, 0.0)
        disp = _simulate(g, s, ["a", "b", "c"], lambda m, a, w: m in bad or (m in flaky and a == 1), rnd)
        for m in bad:  # failed on two different workers (a source problem), or skipped: an import failed first
            assert ((s.state[m] == "failed" and disp[m] == 2 and s.failure_class[m] == "source")
                    or (s.state[m] == "skipped" and m not in disp))
            for d in g.modules:  # everything importing a failed module is skipped
                if m in g.closure([d]):
                    assert s.state[d] in ("skipped", "failed")
        for m in flaky:
            assert s.state[m] in ("done", "skipped") and disp.get(m, 0) <= 2
        assert all(v in ("done", "failed", "skipped") for v in s.state.values())
        assert not (set(disp) & {m for m, v in s.state.items() if v == "skipped"})  # skipped never ran


def test_longest_remaining_path_first(tmp_path):
    g = _graph(tmp_path, 40, max_imports=2, locality=4)
    costs = {m: 1.0 for m in g.modules}
    s = ModuleScheduler(g, costs)
    s.register("a", 1, 0.0)
    ready = [m for m, v in s.state.items() if v == "ready"]
    (t,) = s.claim("a", 1, 0.0)
    assert s.bl[t.module] == max(s.bl[m] for m in ready)


def test_retry_goes_to_another_worker_when_possible(tmp_path):
    g = _graph(tmp_path, 5, max_imports=1)
    s = ModuleScheduler(g, {m: 1.0 for m in g.modules}, retries=3)
    s.register("a", 1, 0.0)
    s.register("b", 1, 0.0)
    (t,) = s.claim("a", 1, 0.0)
    m = t.module
    s.complete(t.task_id, False, 1.0, "x")
    again = s.claim("a", 5, 1.0)
    assert m not in [x.module for x in again]  # held for b
    (t2,) = [x for x in s.claim("b", 5, 1.0) if x.module == m]
    assert t2.attempt == 2
    ev = s.complete(t2.task_id, False, 2.0, "x")  # failed on two different workers: a source problem
    assert ev["action"] == "failed" and ev["class"] == "source" and s.state[m] == "failed"


def test_single_worker_retries_until_exhausted(tmp_path):
    g = _graph(tmp_path, 3, max_imports=1)
    s = ModuleScheduler(g, {m: 1.0 for m in g.modules}, retries=2)
    s.register("a", 1, 0.0)
    (t,) = s.claim("a", 1, 0.0)
    for k in range(3):
        ev = s.complete(t.task_id, False, k + 1.0, "x")
        if k < 2:
            (t,) = s.claim("a", 1, k + 1.0)  # nobody else: the same worker tries again
            assert t.attempt == k + 2
    assert ev["class"] == "retries exhausted"


def test_cached_modules_and_invalidate(tmp_path):
    g = _graph(tmp_path, 30, max_imports=2, locality=4)
    roots = [m for m in g.order if not g.modules[m].imports]
    first = g.order[: len(g.order) // 2]
    keys = {m: f"k-{m}" for m in g.modules}
    s = ModuleScheduler(g, {m: 1.0 for m in g.modules}, keys=keys, done=set(first), needs_closure=True)
    s.register("a", 100, 0.0)
    assert all(s.state[m] == "done" for m in first) and s.cached == set(first)
    tasks = s.claim("a", 100, 0.0)
    assert tasks and not {t.module for t in tasks} & set(first)
    for t in tasks:
        assert t.key == keys[t.module] and set(t.needs) == {keys[u] for u in g.closure([t.module])}
    # a cached root turns out corrupt: it is rebuilt, and its waiting importers wait for it
    r = roots[0]
    waiting = [c for c in s.children[r] if s.state[c] == "waiting"]
    assert s.invalidate(r, 1.0) and s.state[r] == "ready"
    assert all(s.state[c] == "waiting" for c in waiting)
    assert r in [t.module for t in s.claim("a", 100, 1.0)]


def test_lost_worker_and_cancel(tmp_path):
    g = _graph(tmp_path, 6, max_imports=1)
    s = ModuleScheduler(g, {m: 1.0 for m in g.modules}, retries=1, lease_s=10)
    s.register("a", 3, 0.0)
    s.register("b", 3, 0.0)
    tasks = s.claim("a", 3, 0.0)
    assert tasks
    s.heartbeat("b", [], 15.0)
    evs = s.expire(15.0)  # a has not been heard from for 15 s > lease
    assert {e["module"] for e in evs} == {t.module for t in tasks}
    assert all(e["reason"] == "worker lost" for e in evs)
    assert not s.workers["a"]["alive"]
    # a comes back and still reports its old tasks: it is told to cancel them
    assert sorted(s.heartbeat("a", [t.task_id for t in tasks], 16.0)) == sorted(t.task_id for t in tasks)
    assert s.complete(tasks[0].task_id, True, 16.0) is None  # a late result is ignored
    retried = s.claim("b", 6, 16.0)
    assert {t.module for t in tasks} <= {t.module for t in retried}


def test_overdue_and_heavy_threads(tmp_path):
    g = _graph(tmp_path, 4, max_imports=1)
    mods = sorted(g.modules)
    costs = {m: 1.0 for m in mods}
    costs[mods[0]] = 100.0
    s = ModuleScheduler(g, costs, retries=0, timeout_s=5, overdue_grace_s=1, threads=1, heavy_cost=50,
                        heavy_threads=6)
    s.register("a", 4, 0.0)
    tasks = {t.module: t for t in s.claim("a", 4, 0.0)}
    for m, t in tasks.items():
        assert t.threads == (6 if m == mods[0] else 1)
    s.heartbeat("a", list(t.task_id for t in tasks.values()), 7.0)
    evs = s.expire(7.0)
    assert {e["reason"] for e in evs} == {"overdue"} and len(evs) == len(tasks)
    assert all(s.state[m] == "failed" for m in tasks)


def test_lower_bound(tmp_path):
    g = _graph(tmp_path, 30, max_imports=3)
    secs = {m: 2.0 for m in g.modules}
    lb = lower_bound(g, secs, slots=4)
    depth = max(g.depth().values())
    assert lb["critical_path_s"] == 2.0 * depth and lb["work_s"] == 60.0
    assert lb["bound_s"] == max(2.0 * depth, 15.0)


def test_priority_rules_and_fixed_placement(tmp_path):
    from lakeshard.plan import assign_by_chains, assign_by_namespace, assignment_stats
    g = _graph(tmp_path, 60, max_imports=3, locality=6)
    costs = {m: 1.0 + (hash(m) % 7) for m in g.modules}
    # fifo: modules leave in the order they became ready, whatever their remaining path
    s = ModuleScheduler(g, costs, priority="fifo")
    s.register("a", 1, 0.0)
    order_ready, order_dispatched, now = [], [], 0.0
    while not s.done():
        before = {m for m, v in s.state.items() if v == "ready"}
        (t,) = s.claim("a", 1, now)
        order_dispatched.append(t.module)
        s.complete(t.task_id, True, now)
        order_ready += sorted({m for m, v in s.state.items() if v == "ready"} - before - {t.module},
                              key=lambda m: min(x[0] for x in s.ready if x[1] == m))  # first-ready key
        now += 1.0
    roots = [m for m in g.modules if not g.modules[m].imports]
    assert order_dispatched[: len(roots)] == [m for m in order_dispatched if m in roots]  # roots first
    assert order_dispatched[len(roots):] == order_ready[: len(order_dispatched) - len(roots)]
    # structure: remaining path counted in modules, not seconds
    st = ModuleScheduler(g, costs, priority="structure")
    depth_below = {}
    for m in reversed(g.order):
        depth_below[m] = 1 + max((depth_below[c] for c in st.children[m]), default=0)
    assert all(st.bl[m] == depth_below[m] for m in g.modules)
    # fixed placement: a worker only ever gets its own modules
    for assign in (assign_by_namespace(g, costs, ["a", "b"], depth=2), assign_by_chains(g, costs, ["a", "b"], 4)):
        assert set(assign) == set(g.modules) and set(assign.values()) <= {"a", "b"}
        stats = assignment_stats(g, costs, assign)
        assert sum(stats["load_s"].values()) == sum(costs.values())
        s = ModuleScheduler(g, costs, assign=assign)
        s.register("a", 100, 0.0)
        s.register("b", 100, 0.0)
        done = 0
        while not s.done():
            for w in ("a", "b"):
                for t in s.claim(w, 100, 0.0):
                    assert assign[t.module] == w
                    s.complete(t.task_id, True, 0.0)
                    done += 1
        assert done == len(g.modules)
