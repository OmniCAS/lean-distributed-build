"""Event-driven simulator of building a module DAG on a set of machines.

Model
-----
* A machine has `cores` identical cores and a `speed` (module time is divided by it).
* A *task* is one dispatch: a batch of >= 1 modules run one after another on one slot of one
  machine, with `k` threads (occupying k cores). It pays `task_overhead` once (coordinator round
  trip, process/Lake start) and `module_overhead` per module.
* Module m with k threads takes `cost[m] / speedup(m, k) / speed` seconds (`cost` = 1-thread time).
* Network: when module m finishes on machine i, its artifacts are pushed to every other machine;
  they arrive after `latency + out_bytes[m] / bandwidth`, queued FIFO on the receiver's inbound
  link. A module can start on machine j once the artifacts of its whole import closure are there
  (tracked as `avail[m, j]` = arrival of m's closure on j). The slot is held while waiting
  ("transfer wait").
* Release: with `release="module"` each module's artifacts are published when it finishes;
  with `release="batch"` only when the whole batch is done (Lake-style batch).
* Scheduling is decided with *estimated* costs (`est_cost`), timing uses the actual `cost`.

Dispatch (dynamic list scheduling): whenever cores are free, take the released module with the
best priority, pick threads and a machine, optionally grow a batch along its import chain, start.

Priorities: "blevel" (remaining longest path, estimated), "fifo" (release order), "lpt" (own
estimated cost), "random", "index" (module index).
Placement: "most_free" (machine with most free cores; ties -> faster), "est" (earliest data-ready
time, i.e. locality aware).
Threads: int k for every module, or a callable (sim_state, m) -> k.
"""
from __future__ import annotations

import heapq
import math
from dataclasses import dataclass, field
from typing import Callable

import numpy as np

from .trace import Trace


@dataclass
class Machine:
    cores: int
    speed: float = 1.0
    name: str = ""
    start_at: float = 0.0  # the machine (worker) joins at this time; no work before


def amdahl(p: np.ndarray | float):
    """speedup(m, k) for parallel fraction p (array per module or scalar)."""
    if np.isscalar(p):
        def f(m, k):
            return 1.0 / ((1.0 - p) + p / k)
    else:
        arr = np.asarray(p, dtype=np.float64)

        def f(m, k):
            return 1.0 / ((1.0 - arr[m]) + arr[m] / k)
    return f


def no_speedup(m, k):
    return 1.0


@dataclass
class Config:
    machines: list[Machine]
    threads: int | Callable = 1
    priority: str = "blevel"
    placement: str = "most_free"
    est_cost: np.ndarray | None = None  # None = exact (actual cost)
    task_overhead: float = 0.0
    module_overhead: float = 0.0
    latency: float = 0.0
    bandwidth: float = math.inf  # bytes/s per receiving machine
    batch_budget: float = 0.0  # estimated seconds per batch; 0 = one module per task
    batch_max: int = 1_000_000
    release: str = "module"
    speedup: Callable = no_speedup
    blevel_overhead: bool = True  # add module/task overhead to the estimated costs used in bottom levels
    rng_key: int = 0
    record: bool = False  # keep per-module start/finish/machine arrays
    # online correction of estimates: callable(state, m_finished) -> None may update state.est
    on_finish: Callable | None = None
    on_rerank: Callable | None = None  # callable(state) -> None, may update state.est in place
    rerank_every: int = 0  # recompute bottom levels from state.est every N finished modules
    plan_key: np.ndarray | None = None  # for priority="plan": smaller = earlier (e.g. planned start)
    assign: np.ndarray | None = None  # fixed machine per module (static spatial partition); no batching
    etf_window: int = 64  # placement="etf": how many top-priority ready modules are considered
    delay: float = math.inf  # placement="est": defer a module whose best free machine must wait more than
    #                          this for data while a busy machine already has it (delay scheduling)


@dataclass
class State:
    trace: Trace
    cfg: Config
    est: np.ndarray
    bl: np.ndarray
    now: float = 0.0
    finish: np.ndarray = None
    start: np.ndarray = None
    machine: np.ndarray = None
    threads: np.ndarray = None
    done: np.ndarray = None
    n_ready: int = 0
    free: np.ndarray = None
    cost: np.ndarray = None
    stats: dict = field(default_factory=dict)


def simulate(trace: Trace, cfg: Config, cost: np.ndarray | None = None) -> dict:
    n = trace.n
    cost = np.asarray(trace.cost if cost is None else cost, dtype=np.float64)
    if np.isnan(cost).any():
        raise ValueError("cost has unknown entries")
    est = np.array(cost if cfg.est_cost is None else cfg.est_cost, dtype=np.float64)
    M = len(cfg.machines)
    ch = trace.children()
    imps = trace.imports
    over_mod = cfg.module_overhead + (cfg.task_overhead if cfg.batch_budget <= 0 else 0.0)

    def bottom(e):
        return trace.bottom_level(e + (over_mod if cfg.blevel_overhead else 0.0))

    bl = bottom(est)
    st = State(trace, cfg, est, bl)
    st.finish = np.full(n, np.nan)
    st.start = np.full(n, np.nan)
    st.machine = np.full(n, -1, dtype=np.int64)
    st.threads = np.zeros(n, dtype=np.int64)
    st.done = np.zeros(n, dtype=bool)
    gen = np.random.default_rng(cfg.rng_key)
    rnd = gen.random(n) if cfg.priority == "random" else None

    net = cfg.latency > 0 or math.isfinite(cfg.bandwidth)
    if net and M > 1:
        avail = np.full((n, M), np.inf)
        link_free = np.zeros(M)
        ob = trace.out_bytes if trace.out_bytes is not None else np.zeros(n)
        ob = np.nan_to_num(ob, nan=0.0)
    else:
        avail = None

    def key(m, t_rel):
        p = cfg.priority
        if p == "blevel":
            return (-st.bl[m], m)
        if p == "fifo":
            return (t_rel, m)
        if p == "lpt":
            return (-st.est[m], m)
        if p == "random":
            return (rnd[m], m)
        if p == "index":
            return (m, m)
        if p == "plan":
            return (cfg.plan_key[m], m)
        if p == "lookahead":
            # remaining longest path plus half the work this module would release at once
            # (children for which it is the last unfinished import)
            unlock = sum(st.est[c] for c in ch[m] if remaining[c] == 1)
            return (-(st.bl[m] + 0.5 * unlock), m)
        raise ValueError(p)

    remaining = np.array([len(i) for i in imps], dtype=np.int64)
    ready: list = []  # heap of (key, m)
    ready_j = [[] for _ in range(M)] if cfg.assign is not None else None
    if cfg.assign is not None and cfg.batch_budget > 0:
        raise ValueError("fixed assignment does not support batching")
    rel_time = np.zeros(n)

    def push(m, t_rel):
        if ready_j is not None:
            heapq.heappush(ready_j[int(cfg.assign[m])], (key(m, t_rel), m))
        else:
            heapq.heappush(ready, (key(m, t_rel), m))
    for m in range(n):
        if remaining[m] == 0:
            push(m, 0.0)
    in_flight = np.zeros(n, dtype=bool)  # released and taken into a batch
    free = np.array([mc.cores for mc in cfg.machines], dtype=np.int64)
    speed = np.array([mc.speed for mc in cfg.machines], dtype=np.float64)
    st.free = free
    st.cost = cost
    events: list = []  # (time, seq, kind, payload)
    seq = 0

    # accounting (core-seconds)
    acc = {"compute": 0.0, "compute_1thread": 0.0, "overhead": 0.0, "transfer_wait": 0.0}
    n_tasks = 0
    n_done = 0
    rerank_count = 0

    def data_ready(m, j):
        if avail is None or not imps[m]:
            return 0.0
        return float(max(avail[u, j] for u in imps[m]))

    def choose_threads(m):
        t = cfg.threads
        if callable(t):
            st.n_ready = len(ready)
            return max(1, int(t(st, m)))
        return int(t)

    est_end = [[] for _ in range(M)]  # per machine: heap of estimated finish times of running tasks

    def start_task(m, j, k, batch):
        nonlocal seq, n_tasks
        free[j] -= k
        heapq.heappush(est_end[j], st.now + cfg.task_overhead + sum(est[b] for b in batch) / speed[j])
        n_tasks += 1
        t = st.now + cfg.task_overhead
        acc["overhead"] += cfg.task_overhead * k
        fin_times = []
        for b in batch:
            dr = data_ready(b, j)
            if dr > t:
                acc["transfer_wait"] += (dr - t) * k
                t = dr
            t += cfg.module_overhead
            acc["overhead"] += cfg.module_overhead * k
            d = cost[b] / cfg.speedup(b, k) / speed[j]
            st.start[b] = t
            t += d
            acc["compute"] += d * k
            acc["compute_1thread"] += cost[b] / speed[j]
            st.machine[b] = j
            st.threads[b] = k
            fin_times.append(t)
        end = t
        for b, ft in zip(batch, fin_times):
            et = ft if cfg.release == "module" else end
            heapq.heappush(events, (et, seq, 0, (b, j)))
            seq += 1
        heapq.heappush(events, (end, seq, 1, (j, k)))
        seq += 1

    def dispatch_fixed():
        for j in np.argsort(-free, kind="stable"):
            j = int(j)
            h = ready_j[j]
            while h and free[j] > 0:
                _, m = heapq.heappop(h)
                st.n_ready = len(h)
                k = min(choose_threads(m), int(free[j]))
                in_flight[m] = True
                start_task(m, j, k, [m])

    def dispatch():
        nonlocal seq, n_tasks
        if ready_j is not None:
            dispatch_fixed()
            return
        deferred = []
        if cfg.placement == "etf" and avail is not None:
            # ETF (Hwang et al. 1989): among the best `etf_window` ready modules and all machines
            # with a free core, start the pair that can begin earliest; ties -> priority order
            while ready and free.max() > 0:
                cands = heapq.nsmallest(min(len(ready), cfg.etf_window), ready)
                fm = np.nonzero(free > 0)[0]
                best = None
                for rank, item in enumerate(cands):
                    mm = item[1]
                    for j in fm:
                        s0 = max(st.now, data_ready(mm, int(j)))
                        key2 = (s0, rank, -free[j])
                        if best is None or key2 < best[0]:
                            best = (key2, item, int(j))
                _, item, j = best
                ready.remove(item)
                heapq.heapify(ready)
                in_flight[item[1]] = True
                start_task(item[1], j, 1, [item[1]])
            return
        while ready and free.max() > 0:
            item = heapq.heappop(ready)
            m = item[1]
            k = choose_threads(m)
            # machines that can host k threads now; else shrink k to the largest free block
            cand = np.nonzero(free >= k)[0]
            if len(cand) == 0:
                k = int(free.max())
                cand = np.nonzero(free >= k)[0]
            if cfg.placement == "affinity" and len(cand) > 1:
                # machine that built most of m's direct imports (bytes if known); ties -> most free
                score = np.zeros(len(cand))
                pos = {int(c): i for i, c in enumerate(cand)}
                for u in imps[m]:
                    i = pos.get(int(st.machine[u]))
                    if i is not None:
                        score[i] += 1.0
                order = np.lexsort((-speed[cand], -free[cand], -score))
                j = int(cand[order[0]])
            elif cfg.placement in ("eft", "eft_wait"):
                # earliest estimated finish: start (now, or for eft_wait also busy machines at their
                # estimated next free slot) + estimated cost / speed; data arrival counted if modelled
                best = None
                for jj in range(M):
                    if free[jj] >= k:
                        a = st.now
                    elif cfg.placement == "eft_wait" and est_end[jj]:
                        a = max(st.now, est_end[jj][0])
                    else:
                        continue
                    s0 = max(a, data_ready(m, jj))
                    f0 = s0 + est[m] / speed[jj]
                    if best is None or f0 < best[0] - 1e-9:
                        best = (f0, jj, free[jj] >= k)
                if best is None:
                    deferred.append(item)
                    continue
                if not best[2]:
                    deferred.append(item)  # hold it for the faster machine that frees up soon
                    continue
                j = best[1]
            elif cfg.placement == "est" and avail is not None:
                dr = np.array([data_ready(m, j) for j in cand])
                # earliest data-ready; ties -> faster machine, then more free cores
                order = np.lexsort((-free[cand], -speed[cand], dr))
                j = int(cand[order[0]])
                if math.isfinite(cfg.delay) and dr[order[0]] - st.now > cfg.delay:
                    busy = [jj for jj in range(M) if jj not in set(cand.tolist())]
                    if busy and min(data_ready(m, jj) for jj in busy) - st.now <= cfg.delay:
                        deferred.append(item)
                        continue
            else:
                order = np.lexsort((-speed[cand], -free[cand]))  # most free cores, then faster
                j = int(cand[order[0]])
            # grow a batch along the import chain (only modules whose imports are all done or
            # already in this batch), by priority, up to the estimated budget
            batch = [m]
            in_flight[m] = True
            if cfg.batch_budget > 0:
                budget = est[m]
                inb = {m}
                frontier: list = []
                for c in ch[m]:
                    if not in_flight[c] and all(st.done[u] or u in inb for u in imps[c]):
                        heapq.heappush(frontier, (key(c, st.now), c))
                while frontier and budget < cfg.batch_budget and len(batch) < cfg.batch_max:
                    _, c = heapq.heappop(frontier)
                    if in_flight[c]:
                        continue
                    batch.append(c)
                    inb.add(c)
                    in_flight[c] = True
                    budget += est[c]
                    for g in ch[c]:
                        if not in_flight[g] and all(st.done[u] or u in inb for u in imps[g]):
                            heapq.heappush(frontier, (key(g, st.now), g))
            start_task(m, j, k, batch)
        for item in deferred:
            heapq.heappush(ready, item)

    for j, mc in enumerate(cfg.machines):
        if mc.start_at > 0:
            free[j] = 0
            heapq.heappush(events, (mc.start_at, seq, 1, (j, mc.cores)))
            seq += 1
    dispatch()
    while events:
        t = events[0][0]
        st.now = t
        finished = []
        while events and events[0][0] <= t:
            _, _, kind, pay = heapq.heappop(events)
            if kind == 1:
                j, k = pay
                free[j] += k
                if est_end[j] and free[j] > 0 and t > 0:
                    heapq.heappop(est_end[j])
            else:
                finished.append(pay)
        for m, j in finished:
            st.done[m] = True
            st.finish[m] = t
            n_done += 1
            if avail is not None:
                arr = np.empty(M)
                for jj in range(M):
                    if jj == j:
                        arr[jj] = t
                    else:
                        s = max(t, link_free[jj])
                        dur = ob[m] / cfg.bandwidth if math.isfinite(cfg.bandwidth) else 0.0
                        link_free[jj] = s + dur
                        arr[jj] = s + dur + cfg.latency
                if imps[m]:
                    arr = np.maximum(arr, avail[imps[m]].max(axis=0))
                avail[m] = arr
            if cfg.on_finish is not None:
                cfg.on_finish(st, m)
        if cfg.rerank_every and n_done // cfg.rerank_every > rerank_count:
            rerank_count = n_done // cfg.rerank_every
            if cfg.on_rerank is not None:
                cfg.on_rerank(st)
            st.bl = bottom(st.est)
            ready[:] = [(key(m, rel_time[m]), m) for _, m in ready]
            heapq.heapify(ready)
        for m, j in finished:
            for c in ch[m]:
                remaining[c] -= 1
                if remaining[c] == 0 and not in_flight[c]:
                    rel_time[c] = t
                    push(c, t)
        dispatch()

    if n_done != n:
        raise RuntimeError(f"simulation stalled: {n_done}/{n} modules")
    total_cores = int(sum(mc.cores for mc in cfg.machines))
    mk = float(np.nanmax(st.finish)) if n else 0.0
    cap = float(sum(mc.cores * mc.speed for mc in cfg.machines))
    cp = trace.critical_path(cost / speed.max())[0]
    w = float(cost.sum())
    lb = max(cp, w / cap)
    res = {
        "makespan_s": mk,
        "lower_bound_s": lb,
        "ratio": mk / lb if lb else 0.0,
        "work_s": w,
        "critical_path_s": cp,
        "cores": total_cores,
        "tasks": n_tasks,
        "utilization": acc["compute"] / (total_cores * mk) if mk else 0.0,
        "core_s": {k: round(v, 2) for k, v in acc.items()},
        "idle_core_s": total_cores * mk - acc["compute"] - acc["overhead"] - acc["transfer_wait"],
    }
    if cfg.record:
        res["start"], res["finish"], res["machine"], res["threads"] = st.start, st.finish, st.machine, st.threads
    return res


def simulate_ps(trace: Trace, cost: np.ndarray, cores: int, max_jobs: int | None = None,
                order: str = "fifo", est_cost: np.ndarray | None = None,
                p: np.ndarray | None = None, kmax: int = 1) -> dict:
    """Processor sharing (what the OS does when more processes than cores run): up to `max_jobs`
    modules run at once. Each gets a share x = min(kmax, cores / running) of cores and progresses
    at rate 1/((1-p_m) + p_m/x) for x >= 1, or x for x < 1 (time slicing). kmax=1, p=None: plain
    single-threaded sharing. This models vanilla Lake with LEAN_NUM_THREADS=kmax (at most kmax
    concurrent `lean` processes, each with up to kmax threads). Released modules wait in `order`
    ("fifo" or "blevel")."""
    pp = np.zeros(trace.n) if p is None else np.asarray(p, dtype=np.float64)
    n = trace.n
    cost = np.asarray(cost, dtype=np.float64)
    est = cost if est_cost is None else np.asarray(est_cost, dtype=np.float64)
    bl = trace.bottom_level(est)
    ch, imps = trace.children(), trace.imports
    remaining = np.array([len(i) for i in imps])
    cap = max_jobs or n
    ready: list = []
    for m in range(n):
        if remaining[m] == 0:
            heapq.heappush(ready, ((-bl[m] if order == "blevel" else 0.0, m), m))
    left = {}  # running module -> remaining work
    now = 0.0
    finish = np.full(n, np.nan)
    done = 0
    busy = 0.0
    while done < n:
        while ready and len(left) < cap:
            _, m = heapq.heappop(ready)
            left[m] = cost[m]
        r = len(left)
        x = min(float(kmax), cores / r)
        if x <= 1.0:
            rates = {m: x for m in left}
        else:
            rates = {m: 1.0 / ((1.0 - pp[m]) + pp[m] / x) for m in left}
        m_min = min(left, key=lambda m: left[m] / rates[m])
        dt = left[m_min] / rates[m_min]
        now += dt
        busy += dt * min(r * x, cores)
        fin = []
        for m in list(left):
            left[m] -= dt * rates[m]
            if left[m] <= 1e-9:
                fin.append(m)
        for m in fin:
            del left[m]
            finish[m] = now
            done += 1
            for c in ch[m]:
                remaining[c] -= 1
                if remaining[c] == 0:
                    heapq.heappush(ready, ((-bl[c] if order == "blevel" else now, c), c))
    cp = trace.critical_path(cost)[0]
    w = float(cost.sum())
    lb = max(cp, w / cores)
    return {"makespan_s": now, "lower_bound_s": lb, "ratio": now / lb, "utilization": busy / (cores * now),
            "finish": finish}


def execute_static(trace: Trace, plan: dict, cost: np.ndarray, machines: list[Machine],
                   task_overhead: float = 0.0, speedup: Callable = no_speedup,
                   latency: float = 0.0) -> dict:
    """Run a fixed plan (from `simulate(..., record=True)` with estimated costs): every module keeps
    its planned machine and thread count, and each machine starts its modules strictly in the
    planned order (head-of-line blocking) once their imports are done (+latency across machines)
    and enough cores are free. This is what a precomputed static schedule does at run time."""
    from collections import deque
    n = trace.n
    cost = np.asarray(cost, dtype=np.float64)
    ps, pm, pk = plan["start"], plan["machine"], plan["threads"]
    M = len(machines)
    queues = [deque() for _ in range(M)]
    for m in np.argsort(ps, kind="stable"):
        queues[int(pm[m])].append(int(m))
    free = np.array([mc.cores for mc in machines], dtype=np.int64)
    speed = np.array([mc.speed for mc in machines])
    finish = np.full(n, np.inf)
    start = np.full(n, np.nan)
    events: list = []
    seq = 0
    now = 0.0
    done = 0

    def try_start():
        nonlocal seq
        for j in range(M):
            q = queues[j]
            while q:
                h = q[0]
                k = int(pk[h])
                dr = 0.0
                for u in trace.imports[h]:
                    dr = max(dr, finish[u] + (latency if pm[u] != j else 0.0))
                if dr > now or free[j] < k:
                    if math.isfinite(dr) and dr > now:
                        heapq.heappush(events, (dr, seq, -1, -1))
                        seq += 1
                    break
                q.popleft()
                free[j] -= k
                start[h] = now
                f = now + task_overhead + cost[h] / speedup(h, k) / speed[j]
                heapq.heappush(events, (f, seq, h, k))
                seq += 1

    try_start()
    while events:
        now = events[0][0]
        while events and events[0][0] <= now:
            _, _, h, k = heapq.heappop(events)
            if h >= 0:
                finish[h] = now
                free[int(pm[h])] += k
                done += 1
        try_start()
    if done != n:
        raise RuntimeError(f"static plan stalled: {done}/{n}")
    mk = float(finish.max())
    cp = trace.critical_path(cost / speed.max())[0]
    cap = float(sum(mc.cores * mc.speed for mc in machines))
    lb = max(cp, float(cost.sum()) / cap)
    return {"makespan_s": mk, "lower_bound_s": lb, "ratio": mk / lb, "finish": finish, "start": start}
