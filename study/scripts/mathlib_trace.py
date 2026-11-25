"""Turn one measured `lake build` (Lake log + /proc samples + header graph) into a study trace.

Inputs (a run directory fetched from the worker host):
  graph.json     from graph_remote.py (headers; artifact sizes if run after the build)
  lake.log       Lake's non-interactive output ("✔ [i/N] Built X (1.2s)")
  procs.jsonl    procmon.py: per `lean` process start, last-seen, CPU, peak threads, peak RSS
  machine.jsonl  procmon.py: load and busy CPUs every 2 s
  t_start, t_end wall clock of the `lake build` call

cost[m]      = Lake's "Built" seconds (wall time of that module's job in this run)
meta.cpu_s   = user+sys CPU seconds of its `lean` process (nan if not sampled)
meta.start/end = process start (exact) and last time seen (+-0.2 s), relative to t_start

Usage: python mathlib_trace.py RUN_DIR OUT.trace.json.gz [name]
"""
import json
import os
import re
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from sim.trace import Trace  # noqa: E402

BUILT = re.compile(r"\[(\d+)/(\d+)\] Built (\S+)(?: \(([^)]*)\))?")
UNIT = {"ms": 1e-3, "s": 1.0, "m": 60.0, "h": 3600.0}


def parse_dur(s):
    if not s:
        return np.nan
    tot = 0.0
    for num, u in re.findall(r"([\d.]+)\s*(ms|s|m|h)", s):
        tot += float(num) * UNIT[u]
    return tot


def load(run_dir, name="mathlib"):
    g = json.load(open(os.path.join(run_dir, "graph.json")))
    built = {}
    for line in open(os.path.join(run_dir, "lake.log"), encoding="utf-8", errors="replace"):
        m = BUILT.search(line)
        if m and m.group(3) in g:
            built[m.group(3)] = parse_dur(m.group(4))
    names = [x for x in g if x in built]
    # topological order with Lean-core imports dropped
    idx = {m: i for i, m in enumerate(names)}
    missing = {}
    imps = []
    for m in names:
        row = []
        for u in g[m]["imports"]:
            if u in idx:
                row.append(idx[u])
            elif u in g:
                missing[u] = missing.get(u, 0) + 1  # in the workspace but not rebuilt (shouldn't happen)
        imps.append(sorted(set(row)))
    t0 = float(open(os.path.join(run_dir, "t_start")).read())
    t1 = float(open(os.path.join(run_dir, "t_end")).read())
    by_path = {}
    root = None
    for line in open(os.path.join(run_dir, "procs.jsonl")):
        r = json.loads(line)
        src = r["src"]
        if root is None and "/mathlib4/" in src:
            root = src[: src.index("/mathlib4/") + len("/mathlib4/")]
        by_path.setdefault(src, []).append(r)
    n = len(names)
    cpu = np.full(n, np.nan)
    start = np.full(n, np.nan)
    end = np.full(n, np.nan)
    thr = np.full(n, np.nan)
    hwm = np.full(n, np.nan)
    for i, m in enumerate(names):
        rs = by_path.get((root or "") + g[m]["path"], [])
        if rs:
            r = max(rs, key=lambda x: x["last_seen"] - x["start"])
            cpu[i] = r["utime"] + r["stime"]
            start[i] = r["start"] - t0
            end[i] = r["last_seen"] - t0
            thr[i] = r["max_threads"]
            hwm[i] = r["hwm_kb"] * 1024.0
    ob = np.full(n, np.nan)
    for i, m in enumerate(names):
        s = g[m].get("sizes")
        if s:
            ob[i] = sum(v for k, v in s.items() if k in (".olean", ".olean.server", ".olean.private"))

    def lst(a):
        return [None if np.isnan(x) else round(float(x), 3) for x in a]
    meta = {"wall_s": t1 - t0, "pkg": [g[m]["pkg"] for m in names], "cpu_s": lst(cpu), "start": lst(start),
            "end": lst(end), "max_threads": lst(thr), "peak_rss": lst(hwm),
            "ilean_bytes": [g[m].get("sizes", {}).get(".ilean") for m in names],
            "c_bytes": [g[m].get("sizes", {}).get(".c") for m in names],
            "missing_internal_imports": missing,
            "cost_source": "Lake 'Built' seconds of this run"}
    t = Trace(name, names, imps, np.array([g[m]["lines"] for m in names], dtype=np.float64),
              np.array([g[m]["bytes"] for m in names], dtype=np.float64),
              np.array([built[m] for m in names], dtype=np.float64), ob, meta)
    t.order()  # checks acyclicity
    return t


if __name__ == "__main__":
    t = load(sys.argv[1], sys.argv[3] if len(sys.argv) > 3 else "mathlib")
    t.save(sys.argv[2])
    print(json.dumps(t.summary(t.cost)))
