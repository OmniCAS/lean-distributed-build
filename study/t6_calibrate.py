"""T6: calibrate the simulator on a real three-machine run (E1, mid graph: 3,156 modules).

Inputs (playground/e1): e1-spec.json.gz (graph), runs/<A0>/x/ref.history.json (per-module
seconds of the single-machine `lake build`, the information available before the run),
runs/<B1>/records.tgz (modules.jsonl of the three-machine run).

1. Backtest ladder: start from the prediction one would make from the reference run alone, then
   add, one at a time, what the run revealed: machine speeds, late joining, per-task overhead,
   and finally the realized per-module compile times. Each step's error vs the measured wall.
2. Critical-chain decomposition of the real run: from the last module back, each step either
   waited for its last import (dependency) or for a free slot (queueing); the chain's time splits
   exactly into start-up, compile, per-task overhead, queueing and release latency.
Usage: python t6_calibrate.py [A0_run B1_run A1_run SPEC]
"""
from __future__ import annotations

import gzip
import json
import math
import os
import statistics as S
import sys
import tarfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sim.engine import Config, Machine, simulate, simulate_ps  # noqa: E402
from sim.trace import Trace  # noqa: E402

E1 = os.path.join(HERE, "..", "bench", "results")


def load_history(run: str) -> dict:
    """Per-module seconds of a single-machine `lake build` reference run (extracted or in records.tgz)."""
    p = os.path.join(E1, "runs", run, "x", "ref.history.json")
    if os.path.exists(p):
        return json.load(open(p))
    with tarfile.open(os.path.join(E1, "runs", run, "records.tgz")) as tf:
        return json.loads(tf.extractfile("ref.history.json").read())


def load_records(run: str) -> list[dict]:
    with tarfile.open(os.path.join(E1, "runs", run, "records.tgz")) as tf:
        f = tf.extractfile("modules.jsonl")
        return [json.loads(x) for x in f.read().decode().splitlines() if x.strip()]


def trace_from_spec(spec_path: str, ref_hist: dict) -> Trace:
    spec = json.load(gzip.open(spec_path))
    names = spec["names"]
    cost = np.array([ref_hist.get(m, np.nan) for m in names], dtype=np.float64)
    cost[np.isnan(cost)] = np.nanmedian(cost)
    n = len(names)
    return Trace("e1-mid", names, [list(x) for x in spec["imports"]], np.array(spec["lines"], dtype=np.float64),
                 np.zeros(n), cost)


def chain_decomposition(recs: list[dict], t: Trace) -> dict:
    """Walk back from the module that finished last. For module m, the predecessor on the chain is
    its last-confirmed import if m became ready late (dependency), else the module whose finish
    freed the slot m got (approximated by: m waited in the queue)."""
    ok = {r["module"]: r for r in recs if r["ok"] and r["accepted"]}
    idx = {m: i for i, m in enumerate(t.mods)}
    m = max(ok, key=lambda x: ok[x]["done_t"])
    parts = {"compile": 0.0, "task_overhead": 0.0, "dispatch_latency": 0.0, "queue": 0.0, "release": 0.0}
    chain, hosts = [], {}
    while True:
        r = ok[m]
        chain.append(m)
        hosts[r["worker"]] = hosts.get(r["worker"], 0) + 1
        parts["compile"] += r["lean_s"]
        parts["task_overhead"] += r["wall_s"] - r["lean_s"]
        parts["dispatch_latency"] += r["start_t"] - r["dispatch_t"]
        parts["release"] += r["done_t"] - r["end_t"]
        parts["queue"] += r["dispatch_t"] - r["ready_t"]
        imps = [t.mods[u] for u in t.imports[idx[m]]]
        if not imps:
            parts["start"] = r["ready_t"]
            break
        last = max(imps, key=lambda u: ok[u]["done_t"])
        parts["release_gap"] = parts.get("release_gap", 0.0) + (r["ready_t"] - ok[last]["done_t"])
        m = last
    total = ok[chain[0]]["done_t"]
    return {"total_s": total, "modules_on_chain": len(chain), "hosts_on_chain": hosts,
            **{k: round(v, 2) for k, v in parts.items()},
            "check_sum": round(sum(parts.values()), 2)}


def main(a0="mid-A0-c16-r1", b1="mid-B1-c16-r1", a1="mid-A1-c16-r1", spec="../specs/mid.spec.json.gz"):
    ref = load_history(a0)
    t = trace_from_spec(os.path.join(E1, spec), ref)
    recs = load_records(b1)
    ok = [r for r in recs if r["ok"] and r["accepted"]]
    measured = max(r["done_t"] for r in ok)
    idx = {m: i for i, m in enumerate(t.mods)}
    hosts = sorted({r["worker"] for r in ok})  # role names as recorded by the run (worker-1, ...)
    roles = {h: h for h in hosts}
    ratio = {}
    for h in hosts:
        v = [r["lean_s"] / ref[r["module"]] for r in ok if r["worker"] == h and ref.get(r["module"], 0) > 0.3]
        ratio[h] = math.exp(S.mean(math.log(x) for x in v))
    join = {h: min(r["start_t"] for r in ok if r["worker"] == h) for h in hosts}
    over = float(np.mean([r["wall_s"] - r["lean_s"] + (r["start_t"] - r["dispatch_t"]) + (r["done_t"] - r["end_t"]) for r in ok]))
    ob = np.zeros(t.n)
    for r in ok:
        ob[idx[r["module"]]] = r.get("output_bytes", 0)
    t.out_bytes = ob
    c = t.cost
    W, CP = float(c.sum()), t.critical_path(c)[0]
    order = hosts
    net = dict(latency=0.0005, bandwidth=1.1e9, placement="est")
    steps = []

    def run(name, ms, cost=c, o=0.0, est=None):
        r = simulate(t, Config(ms, task_overhead=o, est_cost=est if est is not None else c, **net), cost)
        steps.append({"step": name, "predicted_s": round(r["makespan_s"], 1),
                      "error_pct": round(100 * (r["makespan_s"] - measured) / measured, 1)})
        print(json.dumps(steps[-1]), flush=True)

    run("0 reference-run times, 3 x 16 identical cores, no overhead", [Machine(16) for _ in order])
    run("1 + measured speed of each machine", [Machine(16, 1.0 / ratio[h]) for h in order])
    run("2 + late joining (first task on each machine)", [Machine(16, 1.0 / ratio[h], start_at=join[h]) for h in order])
    run(f"3 + per-task overhead ({over:.3f} s, measured mean)", [Machine(16, 1.0 / ratio[h], start_at=join[h]) for h in order], o=over)
    # 4: realized compile times: cost such that cost/speed on its real host = realized lean_s
    real = c.copy()
    for r in ok:
        real[idx[r["module"]]] = r["lean_s"] / ratio[r["worker"]]
    run("4 + realized per-module times (oracle)", [Machine(16, 1.0 / ratio[h], start_at=join[h]) for h in order], cost=real, o=over)
    # single-machine checks
    single = {}
    rec_a1 = load_records(a1)
    single["tool, one machine (measured)"] = max(r["done_t"] for r in rec_a1 if r["ok"])
    join1 = min(r["start_t"] for r in rec_a1 if r["ok"])
    over1 = float(np.mean([r["wall_s"] - r["lean_s"] for r in rec_a1 if r["ok"]]))
    single["tool, one machine (predicted)"] = simulate(t, Config([Machine(16, 1.0, start_at=join1)], task_overhead=over1), c)["makespan_s"]
    single["lake, one machine (measured)"] = json.load(open(os.path.join(E1, "runs", a0, "meta.json")))["result"]["wall_s"]
    single["lake, one machine (predicted: OS sharing, 16 jobs)"] = simulate_ps(t, c, cores=16, max_jobs=16)["makespan_s"]
    real1 = c.copy()
    for r in rec_a1:
        if r["ok"]:
            real1[idx[r["module"]]] = r["lean_s"]
    single["tool, one machine (oracle: realized times)"] = simulate(t, Config([Machine(16, 1.0, start_at=join1)], task_overhead=over1), real1)["makespan_s"]
    dec = chain_decomposition(recs, t)
    out = {"measured_s": measured, "W_ref_s": W, "CP_ref_s": CP, "x_three": 48 * CP / W,
           "speed_ratio_vs_reference": {roles.get(h, h): round(v, 3) for h, v in ratio.items()},
           "first_task_s": {roles.get(h, h): round(v, 1) for h, v in join.items()},
           "per_task_overhead_mean_s": over, "ladder": steps,
           "single_machine": {k: round(v, 1) for k, v in single.items()},
           "critical_chain_of_real_run": {**dec, "hosts_on_chain": {roles.get(h, h): v for h, v in dec["hosts_on_chain"].items()}}}
    json.dump(out, open(os.path.join(HERE, "results", f"t6-{b1}.json"), "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "ladder"}, indent=1))


if __name__ == "__main__":
    main(*sys.argv[1:])
