"""Expected values for the two-machine queue (in progress since worker-1 became unavailable).

Machines: worker-2 runs the coordinator, the store and every one-machine run (A0, A1);
worker-3 (does not accept incoming connections) is the second machine. Same model and calibration
as e1_expected.py: speed vs the E1 reference machine worker-1 = 1.438 (worker-2) and 1.122
(worker-3) times the time; first task 13.0 s on the coordinator's host and 22.4 s on the other
(one-machine runs 14.6 s); per-task overhead 0.21 s with two machines, 0.044 s with one; noise
sigma 0.12 per module. Mathlib: the trace was measured on worker-2 itself (plain lake build, 16
threads per lean), so worker-2 = 1.0 and worker-3 = 1.438/1.122 = 1.28 times faster; the tool runs
each lean with 1 thread, which on Mathlib files took 0.86 of the time (single-file replays; the
16-way direct comparison gave 0.75-0.81, so this is the conservative end).
Usage: python e1_two_machines.py  ->  results/e1-two-machines.json
       python e1_two_machines.py --recalibrate  ->  results/e1-two-machines-recalibrated-wide.json
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from e1_expected import E1, SIGMA, instance  # noqa: E402
from sim.engine import Config, Machine, simulate, simulate_ps  # noqa: E402
from sim.partition import by_namespace, greedy_locality  # noqa: E402
from sim.trace import Trace  # noqa: E402

SPEED = {"e1": (1 / 1.438, 1 / 1.122), "mathlib": (1.0, 1.438 / 1.122)}
TOOL_FACTOR = {"e1": 1.0, "mathlib": 0.86}


def run(t: Trace, cell: dict, kind: str, reps: int) -> dict:
    s2, s3 = SPEED[kind]
    vals = []
    blc = -t.bottom_level(np.ones(t.n))
    for k in range(reps):
        x = t.cost * np.exp(np.random.default_rng(k).normal(0, SIGMA, t.n))
        if cell["mode"] == "lake":
            vals.append(simulate_ps(t, x / s2, cores=cell["c"], max_jobs=cell["c"])["makespan_s"])
            continue
        x = x * TOOL_FACTOR[kind]
        if cell["hosts"] == 1:
            ms, o = [Machine(cell["c"], s2, start_at=14.6)], 0.044
        else:
            ms = [Machine(cell["c"], s2, start_at=13.0, name="worker-2"), Machine(cell["c"], s3, start_at=22.4, name="worker-3")]
            o = 0.21
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
        vals.append(simulate(t, Config(ms, **kw), x)["makespan_s"])
    v = np.array(vals)
    med = float(np.median(v))
    return {**cell, "predicted_s": round(med, 1),
            "band_s": [round(min(float(np.percentile(v, 5)), 0.85 * med), 1), round(max(float(np.percentile(v, 95)), 1.15 * med), 1)]}


CELLS = (
    [dict(inst="wide", run="wide2-A0-c16-r1", mode="lake", hosts=1, c=16),
     dict(inst="wide", run="wide2-A1-c16-r1", mode="tool", hosts=1, c=16),
     dict(inst="wide", run="wide2-B1-c16-r1", mode="tool", hosts=2, c=16),
     dict(inst="wide", run="wide2-B4-c16-r1", mode="tool", hosts=2, c=16, priority="fifo"),
     dict(inst="wide", run="wide2-B1s-c16-r1", mode="tool", hosts=2, c=16, priority="structure"),
     dict(inst="wide", run="wide2-B1-c8-r1", mode="tool", hosts=2, c=8),
     dict(inst="wide", run="wide2-A1-c8-r1", mode="tool", hosts=1, c=8),
     dict(inst="wide", run="wide2-B1-c4-r1", mode="tool", hosts=2, c=4),
     dict(inst="wide", run="wide2-B4-c4-r1", mode="tool", hosts=2, c=4, priority="fifo"),
     dict(inst="wide", run="wide2-A1-c4-r1", mode="tool", hosts=1, c=4),
     dict(inst="narrow", run="narrow2-A0-c16-r1", mode="lake", hosts=1, c=16),
     dict(inst="narrow", run="narrow2-A1-c16-r1", mode="tool", hosts=1, c=16),
     dict(inst="narrow", run="narrow2-B1-c16-r1", mode="tool", hosts=2, c=16),
     dict(inst="narrow", run="narrow2-A1-c4-r1", mode="tool", hosts=1, c=4),
     dict(inst="narrow", run="narrow2-B1-c4-r1", mode="tool", hosts=2, c=4),
     dict(inst="wide", run="wide2-B2-c16-r1", mode="tool", hosts=2, c=16, assign="namespace"),
     dict(inst="wide", run="wide2-B3-c16-r1", mode="tool", hosts=2, c=16, assign="chains"),
     dict(inst="wide", run="wide2-B1-c16-d0.1", mode="tool", hosts=2, c=16, delay=0.1),
     dict(inst="wide", run="wide2-B1-c16-d1", mode="tool", hosts=2, c=16, delay=1.0),
     dict(inst="wide", run="wide2-B2-c16-d1", mode="tool", hosts=2, c=16, assign="namespace", delay=1.0),
     dict(inst="wide", run="wide2-B1-c16-d10", mode="tool", hosts=2, c=16, delay=10.0),
     dict(inst="wide", run="wide2-B2-c16-d10", mode="tool", hosts=2, c=16, assign="namespace", delay=10.0),
     dict(inst="mathlib", run="mathlib2-A0-c16-r1", mode="lake", hosts=1, c=16),
     dict(inst="mathlib", run="mathlib2-A1-c16-r1", mode="tool", hosts=1, c=16),
     dict(inst="mathlib", run="mathlib2-B1-c1616-r1", mode="tool", hosts=2, c=16),
     dict(inst="mathlib", run="mathlib2-B4-c1616-r1", mode="tool", hosts=2, c=16, priority="fifo")]
)


RERUN = {"wide2-A0-c16-r1": "wide2-A0-c16-r2"}  # the first timing of this run was lost; it was run again


def measured(run_name):
    p = os.path.join(E1, "runs", run_name, "meta.json")
    if not os.path.exists(p) and run_name in RERUN:
        p = os.path.join(E1, "runs", RERUN[run_name], "meta.json")
    if not os.path.exists(p):
        return None
    return json.load(open(p)).get("result", {}).get("wall_s")


def measured_speeds(run, a0="wide-A0-c16-r1"):
    """Time ratio of each worker in `run` vs the reference A0 run (geometric mean over modules > 0.5 s),
    plus the first start time per worker and the mean per-task overhead. The tool numbers workers by
    position in --hosts: its "worker-1" is worker-2 (the coordinator's host), its "worker-2" is worker-3."""
    import math
    import t6_calibrate as T
    ref = T.load_history(a0)
    ok = [r for r in T.load_records(run) if r["ok"]]
    by, first = {}, {}
    for r in ok:
        first[r["worker"]] = min(first.get(r["worker"], 1e9), r["start_t"])
        if ref.get(r["module"], 0) > 0.5:
            by.setdefault(r["worker"], []).append(math.log(r["lean_s"] / ref[r["module"]]))
    return ({w: math.exp(sum(v) / len(v)) for w, v in by.items()}, first,
            sum(r["wall_s"] - r["lean_s"] for r in ok) / len(ok))


def recalibrate():
    """Re-run the measured wide cells with the machine speeds measured in each run itself
    (worker-2 was 1.16-1.19 instead of 1.438 during this queue). -> results/e1-two-machines-recalibrated-wide.json"""
    t = instance("wide")
    rows = []
    for cell in CELLS:
        m = measured(cell["run"])
        if cell["inst"] != "wide" or cell["mode"] != "tool" or not m or cell.get("delay"):
            continue  # the fetch-delay cells need the on-demand fetch model: e1_delay_backtest.py
        sp, first, over = measured_speeds(cell["run"])
        s2 = sp["worker-1"]
        s3 = sp.get("worker-2", 1.122)
        SPEED["e1"] = (1 / s2, 1 / s3)
        r = run(t, cell, "e1", 10)
        rows.append({"run": cell["run"], "speed_vs_reference": [round(s2, 3), round(s3, 3)],
                     "predicted_s": r["predicted_s"], "measured_s": m,
                     "error_pct": round(100 * (r["predicted_s"] - m) / m, 1)})
        print(json.dumps(rows[-1]), flush=True)
    json.dump(rows, open(os.path.join(HERE, "results", "e1-two-machines-recalibrated-wide.json"), "w"), indent=1)


def main():
    insts = {"wide": instance("wide"), "narrow": instance("narrow"),
             "mathlib": Trace.load(os.path.join(HERE, "data", "mathlib.trace.json.gz"))}
    rows = []
    for cell in CELLS:
        kind = "mathlib" if cell["inst"] == "mathlib" else "e1"
        r = run(insts[cell["inst"]], cell, kind, 5 if kind == "mathlib" else 10)
        r["measured_s"] = measured(cell["run"])
        if r["measured_s"]:
            r["error_pct"] = round(100 * (r["predicted_s"] - r["measured_s"]) / r["measured_s"], 1)
            r["within_band"] = r["band_s"][0] <= r["measured_s"] <= r["band_s"][1]
        rows.append(r)
        print(json.dumps(r), flush=True)
    json.dump(rows, open(os.path.join(HERE, "results", "e1-two-machines.json"), "w"), indent=1)


if __name__ == "__main__":
    recalibrate() if sys.argv[1:] == ["--recalibrate"] else main()
