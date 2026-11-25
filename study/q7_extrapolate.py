"""Q7: Mathlib and the RH archive on 32 (8+8+16), 128, 512 and 2,048 cores (64-core machines),
plus the Mathlib predictions for the three-machine S4 run.

Configs: "Lake-like" (release order, 0.1 s per task, 1 thread), "recommended" (remaining longest
path, EST placement, 0.05 s per task), "recommended + threads" (+ adaptive threads, at most 2).
Network: 0.5 ms per artifact, 1.1 GB/s per receiving machine, every artifact pushed to every
machine (Mathlib: measured artifact sizes; RH: source bytes x Mathlib's ratio, 59 GB in all).
Thread speedups: measured curves (Mathlib replays); for RH the curve applies to the per-line part
only (the 6 s import is serial).  Usage: python q7_extrapolate.py
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from experiments import cluster, md  # noqa: E402
from scripts_rh import closure_sizes  # noqa: E402
from sim.engine import Config, Machine, simulate  # noqa: E402
from sim.policies import adaptive_threads  # noqa: E402
from sim.trace import Trace  # noqa: E402
from t4_threads import KS, make_speedup, speedup_table  # noqa: E402


def rh_table(rh: Trace, med: np.ndarray) -> np.ndarray:
    fixed = 0.39 + 5.7 + 0.00064 * np.maximum(np.array(rh.meta.get("closure", np.zeros(rh.n))), 0)
    var = np.maximum(rh.cost - fixed, 0.0)
    tab = np.ones((rh.n, len(KS)))
    for j in range(len(KS)):
        tab[:, j] = rh.cost / (fixed + var / med[j])
    return tab


def run(t: Trace, c: np.ndarray, sp, cores_list, label: str) -> list[dict]:
    W, CP = float(c.sum()), t.critical_path(c)[0]
    rows = []
    for C in cores_list:
        ms = cluster(C)
        L = max(CP, W / C)
        net = dict(latency=0.0005, bandwidth=1.1e9)
        cfgs = {"Lake-like": Config(ms, priority="fifo", task_overhead=0.1, **net),
                "recommended": Config(ms, placement="est", task_overhead=0.05, **net),
                "recommended+threads": Config(ms, placement="est", task_overhead=0.05, speedup=sp,
                                               threads=adaptive_threads(2), **net)}
        for name, cfg in cfgs.items():
            r = simulate(t, cfg, c)
            rows.append({"trace": label, "cores": C, "x": C * CP / W, "config": name, "hours": r["makespan_s"] / 3600,
                         "minutes": r["makespan_s"] / 60, "ratio_to_1thread_LB": r["makespan_s"] / L,
                         "bound": "CP" if CP >= W / C else "W/C", "utilization": r["utilization"]})
            print(json.dumps({k: (round(v, 3) if isinstance(v, float) else v) for k, v in rows[-1].items()}), flush=True)
    return rows


def main():
    ml = Trace.load(os.path.join(HERE, "data", "mathlib.trace.json.gz"))
    tab, med, _ = speedup_table(ml, os.path.join(HERE, "data", "runs", "replay-w3", "replay.jsonl"))
    ml.out_bytes = np.nan_to_num(ml.out_bytes, nan=0.0)
    rows = run(ml, ml.cost, make_speedup(tab), (32, 128, 512, 2048), "Mathlib")
    # S4 calibration predictions: worker-1/2 at speed 1.06 (2.5 vs 2.35 GHz), worker-3 at 1.0
    pred = []
    W, CP = float(ml.cost.sum()), ml.critical_path(ml.cost)[0]
    for label, factor in (("costs as in the 16-thread reference build", 1.0),
                          ("each lean with 1 thread (replay: 0.86 x)", 0.86)):
        c = ml.cost * factor
        for slots_name, ms in (("8+8+16 slots, 1 thread", [Machine(8, 1.06), Machine(8, 1.06), Machine(16, 1.0)]),
                               ("single machine, 16 slots", [Machine(16, 1.0)]),
                               ("single machine, 32 slots", [Machine(32, 1.0)])):
            for o in (0.004, 0.05, 0.2):
                r = simulate(ml, Config(ms, placement="est", task_overhead=o, latency=0.0005, bandwidth=1.1e9), c)
                f = simulate(ml, Config(ms, priority="fifo", task_overhead=o, latency=0.0005, bandwidth=1.1e9), c)
                pred.append({"costs": label, "setup": slots_name, "overhead_s": o, "blevel_min": r["makespan_s"] / 60,
                             "fifo_min": f["makespan_s"] / 60})
                print(json.dumps(pred[-1]), flush=True)
    rh = Trace.load(os.path.join(HERE, "data", "rh-heavy.trace.json.gz"))
    rh0 = Trace.load(os.path.join(HERE, "data", "rh.trace.json.gz"))
    rh.meta["closure"] = rh0.meta["closure"]
    rtab = rh_table(rh, med)
    rows += run(rh, rh.cost, make_speedup(rtab), (32, 128, 512, 2048), "RH (model)")
    json.dump({"rows": rows, "s4_mathlib_predictions": pred}, open(os.path.join(HERE, "results", "q7.json"), "w"), indent=1)
    print(md(rows, ["trace", "cores", "x", "config", "minutes", "ratio_to_1thread_LB", "bound", "utilization"]))


if __name__ == "__main__":
    main()
