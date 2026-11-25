"""T3: when does cutting the graph into machine-sized pieces beat dynamic dispatch?

Granularity g = median module time / per-transfer delay. The delay is a per-artifact latency L
(swept so that g = 1000 ... 0.1) on 10 GbE, and separately a bandwidth sweep at L = 0.2 ms.
Dynamic: most free machine (locality-blind), EST (top-priority module to the machine where its
data is earliest), ETF (best (module, machine) pair among the top 32 ready), EST + delay
scheduling (wait up to L/2 for the machine holding the data). Cluster first, then schedule
(each machine builds a fixed set, in remaining-path order): linear clustering (edge weight = the
delay) packed onto machines by work, whole namespaces, greedy import-chain clustering.
Usage: python t3_granularity.py TRACE
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from experiments import cluster  # noqa: E402
from sim.engine import Config, Machine, simulate  # noqa: E402
from sim.partition import by_namespace, clusters_to_machines, cut_fraction, greedy_locality, linear_clusters  # noqa: E402
from sim.trace import Trace  # noqa: E402


def setups(t: Trace):
    W, CP = float(t.cost.sum()), t.critical_path(t.cost)[0]
    out = [("8+8+16", cluster(32))]
    out.append(("16x8", [Machine(8, name=f"m{i}") for i in range(16)]))
    return out, W, CP


def run(t: Trace, ms, lat, bw, ob, parts_cache):
    c = t.cost
    L = max(t.critical_path(c)[0], float(c.sum()) / sum(m.cores for m in ms))
    net = dict(latency=lat, bandwidth=bw)
    r = {}
    r["most_free"] = simulate(t, Config(ms, **net), c)["makespan_s"] / L
    r["est"] = simulate(t, Config(ms, placement="est", **net), c)["makespan_s"] / L
    r["etf"] = simulate(t, Config(ms, placement="etf", etf_window=32, **net), c)["makespan_s"] / L
    r["est_delay"] = simulate(t, Config(ms, placement="est", delay=0.5 * lat, **net), c)["makespan_s"] / L
    key = (id(ms), round(lat, 6))
    if key not in parts_cache:
        edge = lat + float(np.nanmedian(ob)) / bw
        lc = clusters_to_machines(linear_clusters(t, c, edge), c, ms)
        parts_cache[key] = {"linear_cluster": lc, "namespace": by_namespace(t, c, ms),
                            "chain_cluster": greedy_locality(t, c, ms, weight=ob)}
    for k, a in parts_cache[key].items():
        r["fixed_" + k] = simulate(t, Config(ms, assign=a, **net), c)["makespan_s"] / L
    return r


def main(path):
    t = Trace.load(path)
    ob = t.out_bytes if t.out_bytes is not None else np.full(t.n, 1e6)
    t = Trace(t.name, t.mods, t.imports, t.lines, t.src_bytes, t.cost, np.nan_to_num(ob, nan=1e6), t.meta, t._cache)
    med = float(np.median(t.cost))
    sets, W, CP = setups(t)
    rows = []
    cache = {}
    for name, ms in sets:
        x = sum(m.cores for m in ms) * CP / W
        for g in (1000, 100, 30, 10, 3, 1, 0.3, 0.1):
            lat = med / g
            r = {"trace": t.name, "setup": name, "x": x, "g": g, "latency_s": lat, "bandwidth_MBps": 1100.0}
            r.update(run(t, ms, lat, 1.1e9, ob, cache))
            rows.append(r)
            print(json.dumps({k: (round(v, 3) if isinstance(v, float) else v) for k, v in r.items()}), flush=True)
        for bw in (1.1e8, 1.1e7, 3e6, 1.1e6):
            r = {"trace": t.name, "setup": name, "x": x, "g": None, "latency_s": 0.0002, "bandwidth_MBps": bw / 1e6}
            r.update(run(t, ms, 0.0002, bw, ob, cache))
            rows.append(r)
            print(json.dumps({k: (round(v, 3) if isinstance(v, float) else v) for k, v in r.items()}), flush=True)
        for k, a in cache[(id(ms), round(med / 1000, 6))].items():
            rows.append({"trace": t.name, "setup": name, "cut_" + k: cut_fraction(t, a)})
    json.dump(rows, open(os.path.join(HERE, "results", f"t3-{t.name}.json"), "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
