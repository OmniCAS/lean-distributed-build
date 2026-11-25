"""T1: how far are list schedules from the true optimum?

Sub-DAGs of real traces (import-closure pieces and topological windows, 40-250 modules) at
x = C*CP/W in {0.5, 1, 2}; for each: simple bound max(CP, W/C), Fernandez–Bussell bound, the
list rules, a local search over priorities, and CP-SAT's optimum (or proven bounds within the
time limit). Durations are rounded to 0.1 s for all methods (the CP-SAT instance).
Also the whole 2,613-module synthetic project at 4 cores ("is the 1.3-1.5x gap the bound or the
schedule?").  Usage: python t1_optimality.py [quick]
"""
from __future__ import annotations

import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sim.bounds import cpsat, fb_bound, simple_lb  # noqa: E402
from sim.engine import Config, Machine, simulate  # noqa: E402
from sim.rules import keys, local_search  # noqa: E402
from sim.trace import Trace  # noqa: E402

OUT = os.path.join(HERE, "results", "t1.jsonl")


def induced(t: Trace, nodes: list[int], cost: np.ndarray, name: str) -> tuple[Trace, np.ndarray]:
    idx = {m: i for i, m in enumerate(nodes)}
    imps = [[idx[u] for u in t.imports[m] if u in idx] for m in nodes]
    c = np.maximum(np.round(cost[nodes] * 10) / 10, 0.1)
    return Trace(name, [t.mods[m] for m in nodes], imps, t.lines[nodes], t.src_bytes[nodes], c), c


def closure_piece(t: Trace, N: int, gen) -> list[int]:
    """BFS over imports from a random module whose closure is large enough."""
    depth = t.depth()
    cands = np.nonzero(depth >= 8)[0]
    for _ in range(200):
        m = int(gen.choice(cands))
        seen, q = [m], [m]
        S = {m}
        while q and len(seen) < N:
            v = q.pop(0)
            for u in t.imports[v]:
                if u not in S:
                    S.add(u)
                    seen.append(u)
                    q.append(u)
                    if len(seen) >= N:
                        break
        if len(seen) >= N:
            return seen
    raise RuntimeError("no closure piece")


def window(t: Trace, N: int, gen) -> list[int]:
    order = t.order()
    a = int(gen.integers(0, t.n - N))
    return [int(x) for x in order[a:a + N]]


def evaluate(st: Trace, c: np.ndarray, C: int, time_limit: float, ls_iters: int) -> dict:
    ms = [Machine(C)]
    r = {"n": st.n, "C": C, "W": float(c.sum()), "CP": st.critical_path(c)[0]}
    r["x"] = C * r["CP"] / r["W"]
    r["simple_lb"] = simple_lb(st, c, C)
    r["fb_lb"] = fb_bound(st, c, C)["fb_s"]
    ks = keys(st, c)
    best_rec = None
    for name, k in ks.items():
        res = simulate(st, Config(ms, priority="plan", plan_key=k, record=True), c)
        r[name] = res["makespan_s"]
        if best_rec is None or res["makespan_s"] < best_rec["makespan_s"]:
            best_rec = res
    r["lookahead"] = simulate(st, Config(ms, priority="lookahead"), c)["makespan_s"]
    r["fifo"] = simulate(st, Config(ms, priority="fifo"), c)["makespan_s"]
    r["random"] = float(np.mean([simulate(st, Config(ms, priority="random", rng_key=i), c)["makespan_s"] for i in range(5)]))
    ls, _, _ = local_search(st, {"machines": ms}, c, ks["blevel_time"], iters=ls_iters)
    r["local_search"] = ls
    sol = cpsat(st, c, C, time_limit=time_limit, scale=10, hint_start=best_rec["start"])
    r["opt_status"] = sol["status"]
    r["opt_best"] = sol["best_s"]
    r["opt_bound"] = sol["bound_s"]
    r["opt_wall"] = sol["wall_s"]
    return r


def main(quick: bool):
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    srcs = {"mathlib": "data/mathlib.trace.json.gz", "syn": "data/syn.trace.json.gz", "rh": "data/rh-heavy.trace.json.gz"}
    sizes = (40, 100) if quick else (40, 100, 250)
    reps = 1 if quick else 2
    gen = np.random.default_rng(2026)
    out = open(OUT, "a")
    for src, path in srcs.items():
        t = Trace.load(os.path.join(HERE, path))
        for N in sizes:
            for method in ("closure", "window"):
                for rep in range(reps):
                    nodes = closure_piece(t, N, gen) if method == "closure" else window(t, N, gen)
                    st, c = induced(t, nodes, t.cost, f"{src}-{method}-{N}-{rep}")
                    W, CP = float(c.sum()), st.critical_path(c)[0]
                    done = set()
                    for x in (0.5, 1.0, 2.0):
                        C = max(2, int(round(x * W / CP)))
                        if C in done:
                            continue
                        done.add(C)
                        t0 = time.time()
                        r = evaluate(st, c, C, time_limit=10 if quick else 30, ls_iters=60 if quick else 150)
                        r.update({"src": src, "method": method, "N": N, "rep": rep, "x_target": x,
                                  "eval_s": time.time() - t0})
                        out.write(json.dumps(r) + "\n")
                        out.flush()
                        print(f"{src:8s} {method:7s} N={N:3d} C={C:3d} x={r['x']:.2f} blevel/opt={r['blevel_time']/r['opt_best']:.3f} "
                              f"simple/opt={r['simple_lb']/r['opt_best']:.3f} fb/opt={r['fb_lb']/r['opt_best']:.3f} {r['opt_status']}", flush=True)


def whole_syn(time_limit: float = 300.0):
    t = Trace.load(os.path.join(HERE, "data/syn.trace.json.gz"))
    c = np.maximum(np.round(t.cost * 10) / 10, 0.1)
    res = {}
    for C in (4, 8, 16):
        r = {"C": C, "simple_lb": simple_lb(t, c, C), "fb_lb": fb_bound(t, c, C, grid=400)["fb_s"]}
        rec = simulate(t, Config([Machine(C)], record=True), c)
        r["blevel"] = rec["makespan_s"]
        sol = cpsat(t, c, C, time_limit=time_limit, scale=10, hint_start=rec["start"])
        r.update({"cpsat_status": sol["status"], "cpsat_best": sol["best_s"], "cpsat_bound": sol["bound_s"]})
        res[C] = r
        print(json.dumps(r), flush=True)
    json.dump(res, open(os.path.join(HERE, "results", "t1-whole-syn.json"), "w"), indent=1)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "whole_syn":
        whole_syn(float(sys.argv[2]) if len(sys.argv) > 2 else 300.0)
    else:
        main(len(sys.argv) > 1 and sys.argv[1] == "quick")
