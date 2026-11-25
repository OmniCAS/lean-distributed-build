"""Backup plan (not measured): one machine vs two machines, for when only worker-2 and worker-3
remain. Same model and calibration as e1_expected.py.

  one machine  = worker-3 (the faster of the two): plain `lake build` and the tool, c cores;
  two machines = worker-2 (runs the coordinator and store; worker-3 does not accept incoming
                 connections) + worker-3, c cores each.
Speeds vs the E1 reference machine (worker-1): worker-2 1.438, worker-3 1.122 times the time. For
Mathlib the trace was measured on worker-2 itself, so worker-2 = 1.0 and worker-3 = 1.438/1.122.
Start of the first task: 13.0 s on the coordinator's host, 22.4 s on the other (single machine
14.6 s); per-task overhead 0.21 s (two machines), 0.044 s (one machine); noise sigma 0.12.
Usage: python e1_two_machines.py  ->  results/e1-two-machines.json
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from e1_expected import SIGMA, instance  # noqa: E402
from sim.engine import Config, Machine, simulate, simulate_ps  # noqa: E402
from sim.trace import Trace  # noqa: E402


def cell(t, cost, label, kind, c, s2, s3, reps):
    vals = []
    for k in range(reps):
        x = cost * np.exp(np.random.default_rng(k).normal(0, SIGMA, t.n))
        if kind == "lake-one":
            vals.append(simulate_ps(t, x / s3, cores=c, max_jobs=c)["makespan_s"])
        elif kind == "tool-one":
            vals.append(simulate(t, Config([Machine(c, s3, start_at=14.6)], task_overhead=0.044), x)["makespan_s"])
        else:
            ms = [Machine(c, s2, start_at=13.0, name="worker-2"), Machine(c, s3, start_at=22.4, name="worker-3")]
            vals.append(simulate(t, Config(ms, task_overhead=0.21, est_cost=cost, placement="est",
                                           latency=0.0005, bandwidth=1.1e9), x)["makespan_s"])
    v = np.array(vals)
    med = float(np.median(v))
    return {"instance": label, "config": kind, "c": c, "predicted_s": round(med, 1),
            "band_s": [round(min(float(np.percentile(v, 5)), 0.85 * med), 1), round(max(float(np.percentile(v, 95)), 1.15 * med), 1)]}


def main():
    rows = []
    for name in ("wide", "narrow"):
        t = instance(name)
        for c in (8, 16):
            for kind in (["lake-one"] if c == 16 else []) + ["tool-one", "tool-two"]:
                rows.append(cell(t, t.cost, name, kind, c, 1 / 1.438, 1 / 1.122, 10))
                print(json.dumps(rows[-1]), flush=True)
    ml = Trace.load(os.path.join(HERE, "data", "mathlib.trace.json.gz"))
    for c in (8, 16):
        for kind in (["lake-one"] if c == 16 else []) + ["tool-one", "tool-two"]:
            rows.append(cell(ml, ml.cost, "mathlib", kind, c, 1.0, 1.438 / 1.122, 5))
            print(json.dumps(rows[-1]), flush=True)
    json.dump(rows, open(os.path.join(HERE, "results", "e1-two-machines.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
