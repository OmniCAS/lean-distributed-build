"""Predictions for experiment E1 (theory note, section 8): one machine with c cores vs three
machines with c cores each, c in {4, 8, 16}, on a narrow graph (the 2,613-module synthetic
project, W/CP ~ 5) and a wide graph (synthetic, structure from an RH sub-closure, W/CP >= 60).

Narrow: its own measured per-module times (macOS run; absolute times scale with the Linux/macOS
speed ratio, the ratios below do not). Wide: the real instance is not available yet, so proxies
are cut from the RH graph (sub-closures with W/CP >= 60) and given module times drawn from the
narrow project's measured distribution without its top 1% (the few heavy files would otherwise
set the critical path); proxies are kept only if W/CP >= 60 with those times.

Prediction intervals: 20 replicas with run-to-run noise (log-normal sigma 0.25 per module,
measured between two runs of the same project) x per-task overhead 4-100 ms; 10 GbE
(0.2 ms, 1.1 GB/s), EST placement. Reported: 5th-95th percentiles.
Usage: python e1_predict.py
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sim.engine import Config, Machine, simulate  # noqa: E402
from sim.partition import by_namespace  # noqa: E402
from sim.trace import Trace  # noqa: E402


def sub_closure(rh: Trace, target_n: int, min_par: float, gen) -> list[int]:
    """Import closure of a random module, truncated by BFS to ~target_n, with n/depth >= min_par."""
    depth = rh.depth()
    for _ in range(400):
        m = int(gen.integers(0, rh.n))
        if depth[m] < 15:
            continue
        S, q = {m}, [m]
        while q and len(S) < target_n:
            v = q.pop(0)
            for u in rh.imports[v]:
                if u not in S:
                    S.add(u)
                    q.append(u)
        if len(S) < target_n * 0.8:
            continue
        nodes = sorted(S)
        idx = {x: i for i, x in enumerate(nodes)}
        imps = [[idx[u] for u in rh.imports[x] if u in idx] for x in nodes]
        t = Trace("w", [rh.mods[x] for x in nodes], imps, np.ones(len(nodes)), np.ones(len(nodes)), np.ones(len(nodes)))
        if len(nodes) / t.depth().max() >= min_par:
            return nodes
    raise RuntimeError("no wide sub-closure found")


def predict(t: Trace, base: np.ndarray, label: str, reps: int = 20, rng_key: int = 0) -> list[dict]:
    gen = np.random.default_rng(rng_key)
    rows = []
    for c in (4, 8, 16):
        acc = {k: [] for k in ("one", "three", "three_fifo", "three_fixed_ns", "x1", "x3", "lb1", "lb3")}
        for r in range(reps):
            cost = base * np.exp(gen.normal(0, 0.25, t.n))
            o = float(np.exp(gen.uniform(np.log(0.004), np.log(0.1))))
            W, CP = float(cost.sum()), t.critical_path(cost)[0]
            one = simulate(t, Config([Machine(c)], task_overhead=o), cost)["makespan_s"]
            ms = [Machine(c, name=f"w{i}") for i in range(3)]
            net = dict(latency=0.0002, bandwidth=1.1e9, placement="est")
            three = simulate(t, Config(ms, task_overhead=o, **net), cost)["makespan_s"]
            fifo = simulate(t, Config(ms, task_overhead=o, priority="fifo", **net), cost)["makespan_s"]
            fixed = simulate(t, Config(ms, task_overhead=o, assign=by_namespace(t, cost, ms, level=3),
                                       latency=0.0002, bandwidth=1.1e9), cost)["makespan_s"]
            acc["one"].append(one)
            acc["three"].append(three)
            acc["three_fifo"].append(fifo)
            acc["three_fixed_ns"].append(fixed)
            acc["x1"].append(c * CP / W)
            acc["x3"].append(3 * c * CP / W)
            acc["lb1"].append(max(CP, W / c))
            acc["lb3"].append(max(CP, W / (3 * c)))

        def q(a):
            a = np.asarray(a)
            return [round(float(np.percentile(a, 5)), 3), round(float(np.median(a)), 3), round(float(np.percentile(a, 95)), 3)]
        one, three = np.array(acc["one"]), np.array(acc["three"])
        rows.append({"instance": label, "c": c, "x_one": q(acc["x1"]), "x_three": q(acc["x3"]),
                     "T_one_s": q(one), "T_three_s": q(three),
                     "speedup_three_vs_one": q(one / three),
                     "one_over_lb": q(one / np.array(acc["lb1"])), "three_over_lb": q(three / np.array(acc["lb3"])),
                     "fifo_over_blevel_three": q(np.array(acc["three_fifo"]) / three),
                     "fixed_namespace_over_dynamic_three": q(np.array(acc["three_fixed_ns"]) / three)})
        print(json.dumps(rows[-1]), flush=True)
    return rows


def main():
    syn = Trace.load(os.path.join(HERE, "data", "syn.trace.json.gz"))
    rows = predict(syn, syn.cost, "narrow (2,613-module synthetic, own times)")
    rh = Trace.load(os.path.join(HERE, "data", "rh.trace.json.gz"))
    gen = np.random.default_rng(7)
    body = syn.cost[syn.cost <= np.percentile(syn.cost, 99)]  # synthetic module times without the few heavy files
    k = 0
    while k < 3:
        nodes = sub_closure(rh, 3000, 60.0, gen)
        idx = {x: i for i, x in enumerate(nodes)}
        imps = [[idx[u] for u in rh.imports[x] if u in idx] for x in nodes]
        base = gen.choice(body, size=len(nodes), replace=True)
        t = Trace(f"wide-proxy-{k}", [rh.mods[x] for x in nodes], imps, rh.lines[nodes], rh.src_bytes[nodes], base)
        info = t.summary(base)
        if info["max_speedup"] < 60:
            continue
        print(json.dumps({"proxy": k, **info}), flush=True)
        rows += predict(t, base, f"wide proxy {k} (RH sub-closure, n={t.n}, W/CP={info['max_speedup']})", rng_key=k + 1)
        k += 1
    json.dump(rows, open(os.path.join(HERE, "results", "e1-predictions.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
