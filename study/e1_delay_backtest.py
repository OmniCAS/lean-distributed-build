"""Backtest of the two-machine fetch-delay runs, and what location-aware dispatch would recover.

Measured (wide instance, worker-2 + worker-3, 16 cores each, one run per cell): every task that has
to fetch an import from the other machine waits an extra 0 / 0.1 / 1 / 10 s (`--fetch-delay`).
The predictions made before these runs (e1_two_machines.py) used the simulator's default network
model: artifacts pushed to every machine as soon as they are built, and placement "est" (earliest
data-ready machine, i.e. location aware). The tool does neither: a worker takes the best ready
module whatever machine it is on (placement "most_free"), and a task fetches the missing artifacts
of its import closure when it starts (fetch="pull"), paying the delay once per such task.

This script replays every measured cell with both models, using each run's own measured machine
speeds (as in `e1_two_machines.py --recalibrate`) and, for the fixed placements B2 / B3, the actual
module -> machine split read from the run records. Then it predicts location-aware variants of the
dynamic dispatch at 1 s and 10 s.  Usage: python e1_delay_backtest.py -> results/e1-delay-backtest.json
"""
from __future__ import annotations

import json
import os
import sys
import tarfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from e1_expected import E1, SIGMA, instance  # noqa: E402
from e1_two_machines import measured, measured_speeds  # noqa: E402
from sim.engine import Config, Machine, simulate  # noqa: E402
from sim.trace import Trace  # noqa: E402

REPS = 10
POS = {"worker-1": 0, "worker-2": 1}  # the tool's numbering: worker-1 = worker-2's host (hub), worker-2 = worker-3


def records(run):
    with tarfile.open(os.path.join(E1, "runs", run, "records.tgz")) as tf:
        return [json.loads(x) for x in tf.extractfile("modules.jsonl").read().decode().splitlines() if x.strip()]


def with_bytes(t: Trace, run="wide2-B1-c16-r1") -> Trace:
    idx = {m: i for i, m in enumerate(t.mods)}
    ob = np.zeros(t.n)
    for r in records(run):
        if r["ok"]:
            ob[idx[r["module"]]] = r["output_bytes"]
    return Trace(t.name, t.mods, t.imports, t.lines, t.src_bytes, t.cost, ob, t.meta)


def actual_split(t: Trace, run) -> np.ndarray:
    idx = {m: i for i, m in enumerate(t.mods)}
    a = np.zeros(t.n, dtype=np.int64)
    for r in records(run):
        if r["ok"]:
            a[idx[r["module"]]] = POS[r["worker"]]
    return a


def sim(t, speeds, delay, model, assign=None, reps=REPS, extra=None):
    s2, s3 = speeds
    out, fetch = [], []
    for k in range(reps):
        x = t.cost * np.exp(np.random.default_rng(k).normal(0, SIGMA, t.n))
        ms = [Machine(16, 1 / s2, start_at=13.0, name="worker-2"), Machine(16, 1 / s3, start_at=22.4, name="worker-3")]
        kw = dict(task_overhead=0.21, est_cost=t.cost, bandwidth=1.1e9)
        if model == "push-est":       # the model the predictions were made with
            kw.update(latency=max(delay, 0.0005), placement="est")
        elif model == "pull-blind":   # the tool as built
            kw.update(latency=delay, fetch="pull", placement="most_free")
        elif model == "pull-est":     # location aware: earliest start counting the fetch
            kw.update(latency=delay, fetch="pull", placement="est")
        elif model == "pull-est-wait":  # same, and hold a module for a busy machine that has its imports
            kw.update(latency=delay, fetch="pull", placement="est", delay=0.0)
        elif model == "pull-etf":     # among the 64 best ready modules and the free machines, earliest start
            kw.update(latency=delay, fetch="pull", placement="etf")
        elif model == "push-blind":   # artifacts sent ahead as soon as built, placement blind
            kw.update(latency=max(delay, 0.0005), placement="most_free")
        elif model == "push-est-wait":  # sent ahead, earliest data-ready machine, wait up to half a transfer
            kw.update(latency=max(delay, 0.0005), placement="est", delay=delay / 2)
        if extra:
            kw.update(extra)
        if assign is not None:
            kw["assign"] = assign
            kw.pop("placement", None)
        r = simulate(t, Config(ms, **kw), x)
        out.append(r["makespan_s"])
        fetch.append(r.get("fetch_tasks"))
    med = float(np.median(out))
    return {"predicted_s": round(med, 1), "band_s": [round(min(float(np.percentile(out, 5)), 0.85 * med), 1),
                                                     round(max(float(np.percentile(out, 95)), 1.15 * med), 1)],
            "fetch_tasks": None if fetch[0] is None else int(np.median(fetch))}


RUNS = [("B1", 0.0, "wide2-B1-c16-r1"), ("B1", 0.1, "wide2-B1-c16-d0.1"), ("B1", 1.0, "wide2-B1-c16-d1"),
        ("B1", 10.0, "wide2-B1-c16-d10"), ("B2", 0.0, "wide2-B2-c16-r1"), ("B2", 1.0, "wide2-B2-c16-d1"),
        ("B2", 10.0, "wide2-B2-c16-d10"), ("B3", 0.0, "wide2-B3-c16-r1")]


def main():
    t = with_bytes(instance("wide"))
    rows = []
    for kind, d, run in RUNS:
        m = measured(run)
        if not m:
            continue
        sp = measured_speeds(run)[0]
        speeds = (sp["worker-1"], sp["worker-2"])
        recs = [r for r in records(run) if r["ok"]]
        row = {"run": run, "dispatch": kind, "delay_s": d, "measured_s": m,
               "measured_fetch_tasks": sum(1 for r in recs if r["fetched_files"] > 0),
               "speed_vs_reference": [round(speeds[0], 3), round(speeds[1], 3)]}
        assign = actual_split(t, run) if kind in ("B2", "B3") else None
        for model in ("push-est", "pull-blind"):
            r = sim(t, speeds, d, model, assign)
            r["error_pct"] = round(100 * (r["predicted_s"] - m) / m, 1)
            row[model] = r
        rows.append(row)
        print(json.dumps(row), flush=True)
    # location-aware variants of the dynamic dispatch (speeds of the undelayed run)
    sp = measured_speeds("wide2-B1-c16-r1")[0]
    speeds = (sp["worker-1"], sp["worker-2"])
    split = actual_split(t, "wide2-B2-c16-r1")
    pred = []
    for d in (0.0, 1.0, 10.0):
        row = {"delay_s": d}
        for model in ("pull-blind", "pull-est", "pull-etf", "pull-est-wait", "push-blind", "push-est", "push-est-wait"):
            row[model] = sim(t, speeds, d, model)
        row["fixed-namespace"] = sim(t, speeds, d, "pull-blind", split)
        pred.append(row)
        print(json.dumps(row), flush=True)
    json.dump({"backtest": rows, "location_aware": pred}, open(os.path.join(HERE, "results", "e1-delay-backtest.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
