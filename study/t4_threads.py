"""T4: thread allocation with measured speedup curves (Mathlib).

Speedup S_m(k) = T_1 / T_k from the replays (worker-3: j1/j2/j4/j8, run together on disjoint
pinned cores). For a k between measured points the largest measured k' <= k is used. Modules
not replayed: the median measured curve if the module takes >= 5 s, no speedup below 1.5 s
(start + import dominate, and they are serial), linear in between.
Policies: 1 thread; 2 threads for everyone (C/2 slots); fixed 2/4 threads for modules on the
estimated critical path; adaptive (share idle cores: k = free/(ready+1), capped); adaptive only
for critical modules. Reported: makespan / 1-thread lower bound, extra core-seconds (k*T_k-T_1).
Usage: python t4_threads.py
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from experiments import cluster, md  # noqa: E402
from sim.engine import Config, simulate  # noqa: E402
from sim.policies import adaptive_critical, adaptive_threads, critical_threads  # noqa: E402
from sim.trace import Trace  # noqa: E402

KS = (1, 2, 4, 8)


def speedup_table(t: Trace, replay_path: str) -> np.ndarray:
    rs = [json.loads(line) for line in open(replay_path)]
    by: dict[str, dict] = {}
    for r in rs:
        by.setdefault(r["module"], {})[r["k"]] = r["wall_s"]
    meas = {m: [d[1] / d[k] for k in KS] for m, d in by.items() if all(k in d for k in KS)}
    med = np.median(np.array(list(meas.values())), axis=0)
    tab = np.ones((t.n, len(KS)))
    idx = {m: i for i, m in enumerate(t.mods)}
    for i in range(t.n):
        c = t.cost[i]
        w = 0.0 if c <= 1.5 else (1.0 if c >= 5 else (c - 1.5) / 3.5)
        tab[i] = 1 + w * (med - 1)
    for m, s in meas.items():
        tab[idx[m]] = np.maximum.accumulate(np.array(s))  # never slower with more threads
    return tab, med, len(meas)


def make_speedup(tab: np.ndarray):
    def f(m, k):
        j = 0
        for i, kk in enumerate(KS):
            if kk <= k:
                j = i
        return tab[m, j]
    return f


def main():
    t = Trace.load(os.path.join(HERE, "data", "mathlib.trace.json.gz"))
    tab, med, nmeas = speedup_table(t, os.path.join(HERE, "data", "runs", "replay-w3", "replay.jsonl"))
    sp = make_speedup(tab)
    c = t.cost
    W, CP = float(c.sum()), t.critical_path(c)[0]
    cp_k = {k: t.critical_path(c / tab[:, KS.index(k)])[0] for k in KS}
    print(json.dumps({"median_speedup_curve": dict(zip(KS, med.round(3).tolist())), "replayed": nmeas,
                      "CP_by_threads": {k: round(v, 1) for k, v in cp_k.items()}}))
    rows = []
    for C in (16, 32, 64, 128, 512, 2048):
        ms = cluster(C)
        L = max(CP, W / C)
        pol = {"1 thread": 1, "2 threads all": 2,
               "crit 2": critical_threads(2, 0.9, L), "crit 4": critical_threads(4, 0.9, L),
               "adaptive max 2": adaptive_threads(2), "adaptive max 4": adaptive_threads(4),
               "adaptive max 8": adaptive_threads(8), "adaptive crit max 4": adaptive_critical(4, 0.9, L)}
        r = {"cores": C, "x": C * CP / W, "LB_1thread_s": L}
        for name, th in pol.items():
            res = simulate(t, Config(ms, threads=th, speedup=sp, task_overhead=0.05), c)
            r[name] = res["makespan_s"] / L
            r[name + " extra_core_s%"] = 100 * (res["core_s"]["compute"] - W) / W
        rows.append(r)
        print(json.dumps({k: (round(v, 3) if isinstance(v, float) else v) for k, v in r.items()}), flush=True)
    json.dump({"curve": med.tolist(), "cp_by_threads": cp_k, "rows": rows},
              open(os.path.join(HERE, "results", "t4-mathlib.json"), "w"), indent=1)
    print(md(rows, ["cores", "x"] + [k for k in rows[0] if k not in ("cores", "x", "LB_1thread_s") and not k.endswith("%")]))


if __name__ == "__main__":
    main()
