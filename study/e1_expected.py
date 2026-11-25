"""Expected values for every cell of experiment E1 (the run queue), with tolerances.

Inputs known before a run: the instance's graph, its single-machine `lake build` reference times
(the A0 run), and machine parameters calibrated once on the mid-graph three-machine run:
speed vs the reference machine (worker-1 1.022, worker-2 1.438, worker-3 1.122), the time each
worker starts its first task (13.0, 22.4, 29.3 s; single-machine runs 14.6 s) and the per-task
overhead (0.21 s across machines, 0.044 s on one machine with a local store).

Per cell: 10 replicas with per-module noise (log-normal sigma 0.12, measured between runs); predicted = median,
band = [p5, p95] widened to at least +-15% (one run of a critical-path-bound build varies that
much). Instances: mid (3,156 modules), wide (4,333), narrow (2,613; its reference times are
from the macOS run, so its absolute times are only indicative: compare ratios).
Usage: python e1_expected.py  ->  results/e1-expected.json
"""
from __future__ import annotations

import gzip
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sim.engine import Config, Machine, simulate, simulate_ps  # noqa: E402
from sim.partition import by_namespace, greedy_locality  # noqa: E402
from sim.trace import Trace  # noqa: E402
from t6_calibrate import E1, load_history  # noqa: E402

SPEED = {"worker-1": 1.022, "worker-2": 1.438, "worker-3": 1.122}
JOIN = {"worker-1": 13.0, "worker-2": 22.4, "worker-3": 29.3}
JOIN1, OVER3, OVER1 = 14.6, 0.21, 0.044
SIGMA = 0.12  # measured run-to-run noise per module on one machine (log sd 0.11-0.14)


def instance(name):
    if name in ("mid", "wide"):
        spec = json.load(gzip.open(os.path.join(E1, "..", "specs", "mid.spec.json.gz" if name == "mid" else "wide.spec.json.gz")))
        ref = load_history("mid-A0-c16-r1" if name == "mid" else "wide-A0-c16-r1")
        names, imps = spec["names"], spec["imports"]
    else:
        dag = json.load(open(os.path.join(E1, "..", "specs", "narrow.dag.json")))["modules"]
        names = list(dag)
        idx = {m: i for i, m in enumerate(names)}
        imps = [[idx[u] for u in dag[m]["imports"]] for m in names]
        syn = Trace.load(os.path.join(HERE, "data", "syn.trace.json.gz"))
        ref = dict(zip(syn.mods, syn.cost.tolist()))
    c = np.array([ref.get(m, np.nan) for m in names], dtype=np.float64)
    c[np.isnan(c)] = np.nanmedian(c)
    return Trace(name, names, [list(x) for x in imps], np.ones(len(names)), np.zeros(len(names)), c)


def three(c, start=True):
    return [Machine(c, 1.0 / SPEED[w], start_at=JOIN[w] if start else 0.0, name=w) for w in ("worker-1", "worker-2", "worker-3")]


def run_cell(t: Trace, cell: dict, reps: int = 10) -> dict:
    vals = []
    blc = -t.bottom_level(np.ones(t.n))
    for k in range(reps):
        cost = t.cost * np.exp(np.random.default_rng(k).normal(0, SIGMA, t.n))
        if cell["mode"] == "lake":
            vals.append(simulate_ps(t, cost, cores=cell["c"], max_jobs=cell["c"])["makespan_s"])
            continue
        if cell["hosts"] == 1:
            ms = [Machine(cell["c"], 1.0 / SPEED["worker-1"], start_at=JOIN1)]
            o = OVER1
        else:
            ms = three(cell["c"])
            o = OVER3
        kw = dict(task_overhead=o, est_cost=t.cost, latency=cell.get("delay", 0.0005), bandwidth=1.1e9)
        if cell.get("priority") == "fifo":
            kw["priority"] = "fifo"
        elif cell.get("priority") == "structure":
            kw["priority"], kw["plan_key"] = "plan", blc
        if cell.get("assign") == "namespace":
            kw["assign"] = by_namespace(t, t.cost, ms, level=3)
        elif cell.get("assign") == "chains":
            kw["assign"] = greedy_locality(t, t.cost, ms)
        else:
            kw["placement"] = "est"
        vals.append(simulate(t, Config(ms, **kw), cost)["makespan_s"])
    v = np.array(vals)
    med = float(np.median(v))
    lo, hi = float(np.percentile(v, 5)), float(np.percentile(v, 95))
    return {**cell, "predicted_s": round(med, 1), "band_s": [round(min(lo, 0.85 * med), 1), round(max(hi, 1.15 * med), 1)]}


CELLS = (
    [dict(inst="mid", run="mid-A0-c16-r1", mode="lake", hosts=1, c=16),
     dict(inst="mid", run="mid-A1-c16-r1", mode="tool", hosts=1, c=16),
     dict(inst="mid", run="mid-B1-c16-r1", mode="tool", hosts=3, c=16)]
    + [dict(inst="wide", run="wide-A0-c16-r1", mode="lake", hosts=1, c=16)]
    + [dict(inst="wide", run=f"wide-A1-c{c}-r1", mode="tool", hosts=1, c=c) for c in (16, 8, 4)]
    + [dict(inst="wide", run=f"wide-B1-c{c}-r1", mode="tool", hosts=3, c=c) for c in (16, 8, 4)]
    + [dict(inst="wide", run="wide-B1s-c16-r1", mode="tool", hosts=3, c=16, priority="structure"),
       dict(inst="wide", run="wide-B4-c16-r1", mode="tool", hosts=3, c=16, priority="fifo"),
       dict(inst="wide", run="wide-B4-c4-r1", mode="tool", hosts=3, c=4, priority="fifo"),
       dict(inst="wide", run="wide-B2-c16-r1", mode="tool", hosts=3, c=16, assign="namespace"),
       dict(inst="wide", run="wide-B3-c16-r1", mode="tool", hosts=3, c=16, assign="chains")]
    + [dict(inst="wide", run=f"wide-B1-c16-d{d}", mode="tool", hosts=3, c=16, delay=float(d)) for d in ("0.1", "1", "10")]
    + [dict(inst="wide", run=f"wide-B3-c16-d{d}", mode="tool", hosts=3, c=16, assign="chains", delay=float(d)) for d in ("1", "10")]
    + [dict(inst="narrow", run="narrow-A0-c16-r1", mode="lake", hosts=1, c=16),
       dict(inst="narrow", run="narrow-A1-c16-r1", mode="tool", hosts=1, c=16),
       dict(inst="narrow", run="narrow-B1-c16-r1", mode="tool", hosts=3, c=16),
       dict(inst="narrow", run="narrow-A1-c4-r1", mode="tool", hosts=1, c=4),
       dict(inst="narrow", run="narrow-B1-c4-r1", mode="tool", hosts=3, c=4)]
)


def measured(run):
    p = os.path.join(E1, "runs", run, "meta.json")
    if not os.path.exists(p):
        return None
    r = json.load(open(p)).get("result", {})
    return r.get("wall_s")


def main():
    insts = {k: instance(k) for k in ("mid", "wide", "narrow")}
    rows = []
    for cell in CELLS:
        t = insts[cell["inst"]]
        r = run_cell(t, cell)
        r["measured_s"] = measured(cell["run"])
        if r["measured_s"]:
            r["error_pct"] = round(100 * (r["predicted_s"] - r["measured_s"]) / r["measured_s"], 1)
            r["within_band"] = r["band_s"][0] <= r["measured_s"] <= r["band_s"][1]
        rows.append(r)
        print(json.dumps(r), flush=True)
    info = {k: {"modules": t.n, "W_s": float(t.cost.sum()), "CP_s": t.critical_path(t.cost)[0]} for k, t in insts.items()}
    json.dump({"params": {"speed": SPEED, "join_s": JOIN, "join_single_s": JOIN1, "overhead_three_s": OVER3,
                          "overhead_single_s": OVER1}, "instances": info, "cells": rows},
              open(os.path.join(HERE, "results", "e1-expected.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
