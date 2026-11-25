"""Hand-checkable cases for the simulator. Run: uv run --with numpy --with pytest pytest study/tests"""
import math
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from sim.engine import Config, Machine, amdahl, execute_static, simulate, simulate_ps  # noqa: E402
from sim.trace import from_edges, random_dag  # noqa: E402


def fork_join():
    # r(1) -> x(2), y(3), z(4) -> s(1); edges are (importer, imported)
    return from_edges(5, [(1, 0), (2, 0), (3, 0), (4, 1), (4, 2), (4, 3)], [1, 2, 3, 4, 1])


def test_chain():
    t = from_edges(3, [(1, 0), (2, 1)], [1, 2, 3])
    r = simulate(t, Config([Machine(4)]))
    assert r["makespan_s"] == pytest.approx(6)
    assert r["critical_path_s"] == pytest.approx(6)
    assert r["ratio"] == pytest.approx(1)


def test_trace_longest_paths():
    t = fork_join()
    cp, path = t.critical_path(t.cost)
    assert cp == 6 and path == [0, 3, 4]
    assert t.bottom_level(t.cost).tolist() == [6, 3, 4, 5, 1]
    assert t.earliest_finish(t.cost).tolist() == [1, 3, 4, 5, 6]


def test_blevel_vs_fifo_fork_join():
    # 2 cores. blevel: z,y at 1; x at 4; s at 6 -> 7.  fifo: x,y at 1; z at 3 -> 7; s -> 8.
    t = fork_join()
    assert simulate(t, Config([Machine(2)], priority="blevel"))["makespan_s"] == pytest.approx(7)
    assert simulate(t, Config([Machine(2)], priority="fifo"))["makespan_s"] == pytest.approx(8)


def test_lower_bound_and_utilization():
    t = fork_join()
    r = simulate(t, Config([Machine(2)]))
    assert r["lower_bound_s"] == pytest.approx(max(6, 11 / 2))
    assert r["utilization"] == pytest.approx(11 / (2 * 7))


def test_latency_two_machines():
    # a(1) on m0 -> b, c (1 each); one core per machine; latency 0.5.
    # b stays on m0 (1-2), c goes to m1 and waits for a's artifacts until 1.5 -> 2.5.
    t = from_edges(3, [(1, 0), (2, 0)], [1, 1, 1])
    r = simulate(t, Config([Machine(1), Machine(1)], latency=0.5, placement="est", record=True))
    assert r["makespan_s"] == pytest.approx(2.5)
    assert r["core_s"]["transfer_wait"] == pytest.approx(0.5)


def test_placement_est_vs_most_free():
    # z(0.5), a(1), b(1) imports a; machines [1 core, 2 cores]; priority by index; latency 10.
    # t=0: z -> m1, a -> m0. t=1: b released, m0 has 1 free core, m1 has 2.
    # most_free puts b on m1 and waits for a's artifacts until 11 -> 12; est keeps it on m0 -> 2.
    t = from_edges(3, [(2, 1)], [0.5, 1, 1])
    ms = [Machine(1), Machine(2)]
    assert simulate(t, Config(ms, priority="index", latency=10))["makespan_s"] == pytest.approx(12)
    assert simulate(t, Config(ms, priority="index", latency=10, placement="est"))["makespan_s"] == pytest.approx(2)


def test_bandwidth_queue():
    # a(1, 100 bytes) on m0; at t=1, b(1) and w(5) both import a; w has the higher priority and
    # takes m0, b goes to m1 and waits 100 B / (100 B/s) = 1 s for a's artifacts -> runs 2..3.
    t = from_edges(3, [(1, 0), (2, 0)], [1, 1, 5], out_bytes=[100, 0, 0])
    r = simulate(t, Config([Machine(1), Machine(1)], bandwidth=100.0, record=True))
    assert r["machine"][0] != r["machine"][1]
    assert r["start"][1] == pytest.approx(2) and r["finish"][1] == pytest.approx(3)
    assert r["makespan_s"] == pytest.approx(6)


def test_task_overhead_and_batching():
    ind = from_edges(3, [], [1, 1, 1])
    assert simulate(ind, Config([Machine(1)], task_overhead=0.5))["makespan_s"] == pytest.approx(4.5)
    chain = from_edges(3, [(1, 0), (2, 1)], [1, 1, 1])
    r = simulate(chain, Config([Machine(1)], task_overhead=0.5, batch_budget=10))
    assert r["makespan_s"] == pytest.approx(3.5) and r["tasks"] == 1


def test_release_module_vs_batch():
    # a(1); b, d import a. 2 cores, budget 1.5: batch [a, b] on one core.
    # module release: d starts at 1 -> 2. batch release: a is published at 2 -> d 2..3.
    t = from_edges(3, [(1, 0), (2, 0)], [1, 1, 1])
    cfg = dict(machines=[Machine(2)], batch_budget=1.5, priority="index")
    assert simulate(t, Config(**cfg, release="module"))["makespan_s"] == pytest.approx(2)
    assert simulate(t, Config(**cfg, release="batch"))["makespan_s"] == pytest.approx(3)


def test_threads_amdahl():
    t = from_edges(1, [], [8])
    assert simulate(t, Config([Machine(4)], threads=4, speedup=amdahl(1.0)))["makespan_s"] == pytest.approx(2)
    assert simulate(t, Config([Machine(4)], threads=4, speedup=amdahl(0.5)))["makespan_s"] == pytest.approx(5)
    # k larger than the machine: shrinks to the free cores
    assert simulate(t, Config([Machine(2)], threads=4, speedup=amdahl(1.0)))["makespan_s"] == pytest.approx(4)


def test_machine_speed():
    t = from_edges(2, [], [4, 4])
    r = simulate(t, Config([Machine(1, speed=2.0), Machine(1, speed=1.0)], priority="index"))
    assert r["makespan_s"] == pytest.approx(4)  # one on each; the slow one takes 4


def test_static_plan_equals_dynamic_when_exact():
    t = fork_join()
    ms = [Machine(2)]
    plan = simulate(t, Config(ms, record=True))
    st = execute_static(t, plan, t.cost, ms)
    assert st["makespan_s"] == pytest.approx(plan["makespan_s"])


def test_static_plan_head_of_line():
    # Plan made with wrong estimates (x looks longest): order r, x, y, z, s on one 2-core machine.
    # Actual x=2,y=3,z=4: x 1-3, y 1-4, z 3-7, s 7-8.
    t = fork_join()
    ms = [Machine(2)]
    est = np.array([1, 5, 3, 2, 1.0])
    plan = simulate(t, Config(ms, est_cost=est, record=True), cost=est)
    assert execute_static(t, plan, t.cost, ms)["makespan_s"] == pytest.approx(8)
    assert simulate(t, Config(ms, est_cost=est))["makespan_s"] == pytest.approx(8)


def test_processor_sharing():
    t = from_edges(2, [], [2, 2])
    assert simulate_ps(t, t.cost, cores=1)["makespan_s"] == pytest.approx(4)
    assert simulate_ps(t, t.cost, cores=2)["makespan_s"] == pytest.approx(2)
    # fork-join, unlimited processes on 2 cores: r 0-1; x,y,z share 2 cores (rate 2/3):
    # x done at 1+3=4; then y,z at rate 1: y (3-2=1 left) at 5, z (4-2-1=1 left) at 6; s 6-7.
    assert simulate_ps(fork_join(), fork_join().cost, cores=2)["makespan_s"] == pytest.approx(7)


@pytest.mark.parametrize("key", range(6))
def test_graham_bound_random(key):
    gen = np.random.default_rng(key)
    t = random_dag(300, 2.0, gen, window=40)
    w = t.cost.sum()
    cp = t.critical_path(t.cost)[0]
    for cores in (1, 3, 8, 64):
        for pr in ("blevel", "fifo", "random"):
            r = simulate(t, Config([Machine(cores)], priority=pr, rng_key=key))
            assert r["makespan_s"] >= max(cp, w / cores) - 1e-9
            assert r["makespan_s"] <= w / cores + (1 - 1 / cores) * cp + 1e-9


def test_bottom_level_matches_naive():
    gen = np.random.default_rng(7)
    t = random_dag(500, 3.0, gen)
    bl = t.bottom_level(t.cost)
    ch = t.children()
    naive = np.zeros(t.n)
    for m in t.order()[::-1]:
        naive[m] = t.cost[m] + max((naive[c] for c in ch[m]), default=0.0)
    assert np.allclose(bl, naive)


def test_multi_machine_no_network_equals_pooled_cores():
    gen = np.random.default_rng(3)
    t = random_dag(400, 2.0, gen, window=30)
    a = simulate(t, Config([Machine(8)]))["makespan_s"]
    b = simulate(t, Config([Machine(4), Machine(4)]))["makespan_s"]
    assert a == pytest.approx(b)
    assert not math.isnan(a)


def test_contract_chains():
    from sim.policies import contract_chains
    # a -> b -> c, a -> d : b,c merge (c's only import is b, b's only importer is c); a stays.
    t = from_edges(4, [(1, 0), (2, 1), (3, 0)], [1, 2, 3, 4])
    ct, c, groups = contract_chains(t, t.cost)
    assert sorted(map(sorted, groups)) == [[0], [1, 2], [3]]
    assert sorted(c.tolist()) == [1, 4, 5]
    assert ct.critical_path(c)[0] == t.critical_path(t.cost)[0] == 6


def test_online_correction_scales_group():
    from sim.policies import OnlineCorrection
    from sim.trace import Trace
    names = ["A.x.1", "A.x.2", "B.y.1"]
    t = Trace("t", names, [[], [0], []], np.ones(3), np.ones(3), np.array([2.0, 2.0, 1.0]))
    oc = OnlineCorrection(t, np.ones(3), level=2, prior=0.0)

    class S:
        pass
    st = S()
    st.cost = t.cost
    st.est = np.ones(3)
    st.done = np.array([True, False, False])
    oc.on_finish(st, 0)
    oc.on_rerank(st)
    # group A.x observed ratio 2 -> unfinished A.x.2 estimated 2; B.y has no data -> global ratio 2
    assert st.est.tolist() == [2.0, 2.0, 2.0]


def test_fixed_assignment():
    # two independent chains a->b and c->d, all cost 1, two 1-core machines.
    # Assigning each chain to its own machine: 2. Putting everything on m0: 4.
    t = from_edges(4, [(1, 0), (3, 2)], [1, 1, 1, 1])
    ms = [Machine(1), Machine(1)]
    assert simulate(t, Config(ms, assign=np.array([0, 0, 1, 1])))["makespan_s"] == pytest.approx(2)
    assert simulate(t, Config(ms, assign=np.array([0, 0, 0, 0])))["makespan_s"] == pytest.approx(4)
    # cross-machine import pays the latency: b on m1 waits for a (latency 0.5)
    r = simulate(t, Config(ms, assign=np.array([0, 1, 1, 0]), latency=0.5))
    assert r["makespan_s"] == pytest.approx(2.5)


def test_delay_scheduling():
    # a(1) on m0; at t=1, b(1) and w(0.5) both import a; one core per machine; latency 10.
    # b (higher bottom level) stays on m0 (1-2). Without delay w goes to m1 and waits for a's
    # artifacts until 11 -> 11.5; with delay=5 it is held back and runs on m0 at 2 -> 2.5.
    t = from_edges(3, [(1, 0), (2, 0)], [1, 1, 0.5])
    ms = [Machine(1), Machine(1)]
    assert simulate(t, Config(ms, latency=10, placement="est"))["makespan_s"] == pytest.approx(11.5)
    assert simulate(t, Config(ms, latency=10, placement="est", delay=5))["makespan_s"] == pytest.approx(2.5)


def test_processor_sharing_elastic():
    # one module, cost 8, perfectly parallel, 4 cores, Lake-style kmax=4 -> 2; kmax=2 -> 4
    t = from_edges(1, [], [8])
    assert simulate_ps(t, t.cost, cores=4, p=np.array([1.0]), kmax=4)["makespan_s"] == pytest.approx(2)
    assert simulate_ps(t, t.cost, cores=4, p=np.array([1.0]), kmax=2)["makespan_s"] == pytest.approx(4)
    # two modules on 4 cores, kmax=4: each gets 2 cores -> both done at 4/2 = ... cost 4 each, p=1 -> 2
    t2 = from_edges(2, [], [4, 4])
    assert simulate_ps(t2, t2.cost, cores=4, p=np.array([1.0, 1.0]), kmax=4)["makespan_s"] == pytest.approx(2)


def test_fernandez_bussell_fork_join():
    # C=2: simple bound max(6, 5.5) = 6. Window [1,5] must hold x(2)+y(3)+z(4) = 9 -> 9/2 - 4 = 0.5
    # -> FB = 6.5. True optimum is 7 (z,y at 1; x at 4; s at 6).
    from sim.bounds import fb_bound, simple_lb
    t = fork_join()
    assert simple_lb(t, t.cost, 2) == pytest.approx(6)
    assert fb_bound(t, t.cost, 2)["fb_s"] == pytest.approx(6.5)
    assert fb_bound(t, t.cost, 1)["fb_s"] == pytest.approx(11)


def test_fb_is_a_lower_bound_random():
    from sim.bounds import fb_bound
    for key in range(4):
        gen = np.random.default_rng(key)
        t = random_dag(200, 2.0, gen, window=25)
        for C in (2, 5, 12):
            fb = fb_bound(t, t.cost, C)["fb_s"]
            mk = simulate(t, Config([Machine(C)]))["makespan_s"]
            assert fb <= mk + 1e-9
            assert fb >= max(t.critical_path(t.cost)[0], t.cost.sum() / C) - 1e-9


def test_cpsat_fork_join():
    pytest.importorskip("ortools")
    from sim.bounds import cpsat
    r = cpsat(fork_join(), fork_join().cost, 2, time_limit=10, scale=1)
    assert r["optimal"] and r["best_s"] == pytest.approx(7)


def test_etf_picks_earliest_pair():
    # Same as the delay case: a on m0; b(1), w(0.5) import a; latency 10, one core each.
    # ETF considers both ready modules on both machines: b on m0 can start at 1 (earliest);
    # then w: m1 at 11 is the only free option -> 11.5 (ETF has no delay), b ends at 2.
    t = from_edges(3, [(1, 0), (2, 0)], [1, 1, 0.5])
    r = simulate(t, Config([Machine(1), Machine(1)], latency=10, placement="etf", record=True))
    assert r["start"][1] == pytest.approx(1) and r["makespan_s"] == pytest.approx(11.5)


def test_linear_clusters():
    from sim.partition import linear_clusters
    # a -> b -> c heavy chain and a -> d light: first cluster is the chain a,b,c; d alone.
    t = from_edges(4, [(1, 0), (2, 1), (3, 0)], [1, 5, 5, 1])
    cl = linear_clusters(t, t.cost, edge=0.5)
    assert cl[0] == cl[1] == cl[2] and cl[3] != cl[0]


def test_machine_joins_late():
    # two independent modules of 4 s; m1 joins at 3 -> one runs 0-4 on m0, the other 3-7 on m1
    t = from_edges(2, [], [4, 4])
    r = simulate(t, Config([Machine(1), Machine(1, start_at=3)], priority="index"))
    assert r["makespan_s"] == pytest.approx(7)
    # if only the late machine exists, everything shifts by its start
    assert simulate(t, Config([Machine(2, start_at=3)]))["makespan_s"] == pytest.approx(7)


def test_eft_wait_holds_critical_module_for_fast_machine():
    # m0 fast (speed 2), m1 slow (speed 1), one core each. x(1 s of work) occupies m0 for 0.5 s;
    # c (4 s of work, critical) must choose: m1 now -> ends 4; wait for m0 -> 0.5 + 2 = 2.5.
    t = from_edges(2, [], [1, 4])
    ms = [Machine(1, 2.0), Machine(1, 1.0)]
    # priority index: x first (takes the fast machine), then c
    assert simulate(t, Config(ms, priority="index"))["makespan_s"] == pytest.approx(4)
    assert simulate(t, Config(ms, priority="index", placement="eft_wait"))["makespan_s"] == pytest.approx(2.5)
