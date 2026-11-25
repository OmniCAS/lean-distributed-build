"""Backtest of the two-machine Mathlib run (worker-2 + worker-3, 16 + 16 cores, one `lean` thread each).

Measured: the tool on one machine 2,713 s, on two machines 1,606 s; predicted beforehand 2,388 s and
1,137 s (e1_two_machines.py). On two machines every module but the root `Mathlib` was done at
1,352 s; the root then fetched, one file per request, the 7,525 files of the modules built on the
other machine that its machine did not have yet (250 s), and ran `lean` for 3.7 s.

Everything below is read from the run records: per-module `lean` seconds of the one-machine run
(the costs), each machine's speed in the two-machine run relative to that, the per-task time that
is neither `lean` nor fetching (mostly the upload), when each worker started, seconds per fetched
file on each machine and files per module. The simulator then replays the two-machine run with
artifacts pushed ahead (no fetch cost), with the tool's on-demand fetch (one request per file), and
with the two fixes the tool line is considering (one batched request per task; parallel requests).
Usage: python e1_mathlib_backtest.py  ->  results/e1-mathlib-backtest.json
"""
from __future__ import annotations

import json
import math
import os
import sys
import tarfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from e1_expected import E1  # noqa: E402
from sim.engine import Config, Machine, simulate  # noqa: E402
from sim.trace import Trace  # noqa: E402

A1, B1 = "mathlib2-A1-c16-r1", "mathlib2-B1-c1616-r1"
POS = {"worker-1": 0, "worker-2": 1}  # tool numbering: worker-1 runs on worker-2 (hub), worker-2 on worker-3


def records(run):
    with tarfile.open(os.path.join(E1, "runs", run, "records.tgz")) as tf:
        recs = [json.loads(x) for x in tf.extractfile("modules.jsonl").read().decode().splitlines() if x.strip()]
    return {r["module"]: r for r in recs if r["ok"]}


def wall(run):
    return json.load(open(os.path.join(E1, "runs", run, "meta.json")))["result"]["wall_s"]


def subtrace(t: Trace, keep: list[str]) -> Trace:
    idx = {m: i for i, m in enumerate(t.mods)}
    new = {m: i for i, m in enumerate(keep)}
    imps = [sorted(new[t.mods[u]] for u in t.imports[idx[m]] if t.mods[u] in new) for m in keep]
    sel = np.array([idx[m] for m in keep])
    return Trace("mathlib-lib", keep, imps, t.lines[sel], t.src_bytes[sel], t.cost[sel], None, t.meta)


def main():
    full = Trace.load(os.path.join(HERE, "data", "mathlib.trace.json.gz"))
    a1, b1 = records(A1), records(B1)
    keep = [m for m in full.mods if m in a1]
    t = subtrace(full, keep)
    cost = np.array([a1[m]["lean_s"] for m in keep])
    ob = np.array([b1[m]["output_bytes"] for m in keep], dtype=np.float64)
    t = Trace(t.name, t.mods, t.imports, t.lines, t.src_bytes, cost, ob, t.meta)
    root = keep.index("Mathlib")

    # measured parameters of the two-machine run
    speed, first, files, fsec, other, nmod = {}, {}, {}, {}, {}, {}
    for m, r in b1.items():
        j = POS[r["worker"]]
        if a1[m]["lean_s"] > 0.5:
            speed.setdefault(j, []).append(math.log(r["lean_s"] / a1[m]["lean_s"]))
        first[j] = min(first.get(j, 1e9), r["start_t"])
        files[j] = files.get(j, 0) + r["fetched_files"]
        fsec[j] = fsec.get(j, 0.0) + r["fetch_s"]
        other.setdefault(j, []).append(r["wall_s"] - r["lean_s"] - r["fetch_s"])
        nmod[j] = nmod.get(j, 0) + 1
    ratio = {j: math.exp(sum(v) / len(v)) for j, v in speed.items()}
    per_file = {j: fsec[j] / files[j] for j in files}
    # each machine ends up fetching every module built on the other one exactly once (the root
    # imports everything), so files per module = files fetched by one machine / modules built on the other
    fpm = files[0] / nmod[1]
    over2 = float(np.mean([x for v in other.values() for x in v]))
    over1 = float(np.mean([r["wall_s"] - r["lean_s"] - r["fetch_s"] for r in a1.values()]))
    first1 = min(r["start_t"] for r in a1.values())
    params = {"speed_vs_one_machine_run": [round(ratio[0], 3), round(ratio[1], 3)],
              "first_start_s": [round(first[0], 1), round(first[1], 1)], "one_machine_first_start_s": round(first1, 1),
              "seconds_per_fetched_file": [round(per_file[0], 4), round(per_file[1], 4)],
              "files_per_module": round(fpm, 2), "task_overhead_s": round(over2, 3), "one_machine_task_overhead_s": round(over1, 3),
              "work_lean_core_s": {"one_machine": round(float(cost.sum())), "two_machines": round(sum(r["lean_s"] for r in b1.values()))},
              "trace_work_same_modules_core_s": round(float(full.cost[[full.mods.index(m) for m in keep]].sum()))}
    print(json.dumps(params), flush=True)

    def two(fetch_mode, **kw):
        ms = [Machine(16, 1 / ratio[0], start_at=first[0]), Machine(16, 1 / ratio[1], start_at=first[1])]
        base = dict(task_overhead=over2, bandwidth=1.1e9, record=True)
        if fetch_mode == "push":
            base.update(latency=0.0005)
        else:
            base.update(fetch="pull", latency=0.0)
        base.update(kw)
        r = simulate(t, Config(ms, **base), cost)
        fin = np.array(r["finish"])
        out = {}
        if "have" in r:
            # the root as in the run: on worker-2 (the hub), fetching every module the hub still lacks
            hub = POS[b1["Mathlib"]["worker"]]
            ran = int(r["machine"][root])
            rest = np.delete(fin, root)
            if ran == hub:
                w = float(r["start"][root] - np.max(rest)) - over2
            else:
                lack = ~r["have"][:, hub]
                lack[root] = False
                w = kw.get("latency", 0.0) + int(lack.sum()) * item_of(kw, hub) + float(ob[lack].sum()) / kw.get("bandwidth", 1.1e9)
                out["root_on_hub_missing_modules"] = int(lack.sum())
            out.update({"root_ran_on": ran, "root_on_hub_fetch_s": round(w, 1),
                        "makespan_if_root_on_hub_s": round(float(np.max(rest)) + over2 + w + cost[root] * ratio[hub], 1)})
        return {**out, "makespan_s": round(r["makespan_s"], 1),
                "all_but_root_s": round(float(np.max(np.delete(fin, root))), 1),
                "root_fetch_s": round(float(r["start"][root] - np.max(fin[t.imports[root]])), 1) if t.imports[root] else 0.0,
                "lower_bound_s": round(r["lower_bound_s"], 1), "fetch_tasks": r.get("fetch_tasks")}

    item = (fpm * per_file[0], fpm * per_file[1])

    def item_of(kw, j):
        v = kw.get("fetch_item_s", 0.0)
        return float(v[j]) if isinstance(v, tuple) else float(v)
    res = {"params": params, "measured": {"one_machine_s": wall(A1), "two_machines_s": wall(B1),
                                          "two_machines_all_but_root_s": round(max(r["done_t"] for m, r in b1.items() if m != "Mathlib"), 1),
                                          "root_fetch_s": b1["Mathlib"]["fetch_s"], "root_fetched_files": b1["Mathlib"]["fetched_files"]}}
    ms1 = [Machine(16, 1.0, start_at=first1)]
    r1 = simulate(t, Config(ms1, task_overhead=over1), cost)
    res["one_machine"] = {"simulated_s": round(r1["makespan_s"], 1), "lower_bound_s": round(r1["lower_bound_s"], 1)}
    # step by step from the prediction's inputs to the measured ones (artifacts pushed ahead)
    trace_cost = full.cost[[full.mods.index(m) for m in keep]]

    def step(c, speeds, over, starts):
        ms = [Machine(16, speeds[0], start_at=starts[0]), Machine(16, speeds[1], start_at=starts[1])]
        return round(simulate(t, Config(ms, task_overhead=over, latency=0.0005, bandwidth=1.1e9, placement="est"), c)["makespan_s"], 1)
    res["steps"] = {
        "prediction inputs: trace x 0.86, worker-3 1.28x worker-2, overhead 0.21 s, starts 13.0 / 22.4 s":
            step(trace_cost * 0.86, (1.0, 1.438 / 1.122), 0.21, (13.0, 22.4)),
        "+ measured one-thread lean times (0.93 x trace) and speeds (worker-3 1.03x worker-2)":
            step(cost, (1 / ratio[0], 1 / ratio[1]), 0.21, (13.0, 22.4)),
        "+ measured per-task overhead (upload) and worker starts": step(cost, (1 / ratio[0], 1 / ratio[1]), over2, (first[0], first[1])),
    }
    for k, v in res["steps"].items():
        print(k, v, flush=True)
    res["two_machines"] = {
        "pushed ahead (no fetch cost)": two("push"),
        "on demand, one request per file (the tool)": two("pull", fetch_item_s=item),
        "on demand, one batched request per task (33 ms + bytes at 1.1 GB/s)": two("pull", latency=per_file[0]),
        "on demand, one batched request per task (33 ms + bytes at 0.3 GB/s)": two("pull", latency=per_file[0], bandwidth=0.3e9),
        "on demand, 16 requests in parallel": two("pull", fetch_item_s=(item[0] / 16, item[1] / 16)),
    }
    # after the Nagle fix (c28f197): 0.8 ms per request instead of ~40 (loopback, measured by the tool line)
    rtt = 0.0008
    rest1 = float(np.mean([r["wall_s"] - r["lean_s"] - r["fetch_s"] - r["publish_s"] for r in a1.values()]))
    rest2 = float(np.mean([r["wall_s"] - r["lean_s"] - r["fetch_s"] - r["publish_s"] for r in b1.values()]))
    up = fpm * rtt + float(ob.mean()) / 1.1e9
    r1f = simulate(t, Config(ms1, task_overhead=rest1 + up), cost)
    over2_saved = over2
    over2 = rest2 + up  # used by two() for the root-on-hub estimate
    fixed = two("pull", task_overhead=over2, fetch_item_s=fpm * rtt)
    over2 = over2_saved
    res["after_nagle_fix"] = {"request_s": rtt, "task_overhead_s": [round(rest1 + up, 3), round(rest2 + up, 3)],
                              "one_machine_s": round(r1f["makespan_s"], 1), "two_machines": fixed}
    print("after the Nagle fix", json.dumps(res["after_nagle_fix"]), flush=True)
    for k, v in res["two_machines"].items():
        print(k, json.dumps(v), flush=True)
    print(json.dumps(res["one_machine"]), json.dumps(res["measured"]))
    json.dump(res, open(os.path.join(HERE, "results", "e1-mathlib-backtest.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
