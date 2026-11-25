"""RH archive: how the per-file fixed cost (start + `import Mathlib`) and merging small files
change the work, the critical path, the bound and the build time.

Cost of a file = F + 0.64 ms x (project modules in its import closure) + per-line part, where the
per-line part is the "heavy" model's (Mathlib's per-line rates drawn per file; scripts/rh_model.py)
and F is the fixed part: measured 6.1 s for `lean` + `import Mathlib` alone on one core; 2 and 4 s
stand for a faster import (or a lighter prelude), 8 s for import under heavy contention.

Merging: files in the same directory and at the same import depth are merged into one file, at
most k at a time (a merged file pays F once, its per-line parts add up). Modules at the same depth
cannot import each other and every import edge goes to a smaller depth, so the merged graph stays
acyclic. Also: chain contraction (a module with one importer that has no other import), which
loses no parallelism.
Times: 64-core machines, remaining longest path first, EST placement, 0.05 s per task, artifacts
broadcast (0.5 ms, 1.1 GB/s).  Usage: python rh_import_sensitivity.py
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from experiments import cluster  # noqa: E402
from sim.engine import Config, simulate  # noqa: E402
from sim.policies import contract_chains  # noqa: E402
from sim.trace import Trace  # noqa: E402

PER_MOD = (6.1 - 0.39) / 8908
CORES = (128, 512, 2048)


def times(t: Trace, c: np.ndarray) -> dict:
    out = {}
    for C in CORES:
        r = simulate(t, Config(cluster(C), placement="est", task_overhead=0.05, latency=0.0005, bandwidth=1.1e9), c)
        out[C] = r["makespan_s"]
    return out


def describe(t: Trace, c: np.ndarray, label: str, extra: dict) -> dict:
    W, (CP, path) = float(c.sum()), t.critical_path(c)
    row = {"case": label, **extra, "files": t.n, "W_core_h": W / 3600, "CP_h": CP / 3600, "max_speedup": W / CP}
    for C, v in times(t, c).items():
        row[f"T{C}_min"] = v / 60
    print(json.dumps({k: (round(v, 3) if isinstance(v, float) else v) for k, v in row.items()}), flush=True)
    return row


def merge(t: Trace, var: np.ndarray, clo: np.ndarray, F: float, k: int) -> tuple[Trace, np.ndarray]:
    depth = t.depth()
    groups: dict = {}
    for m in range(t.n):
        groups.setdefault((t.mods[m].rsplit(".", 1)[0], int(depth[m])), []).append(m)
    gid = np.empty(t.n, dtype=np.int64)
    members = []
    for key in sorted(groups):
        ms = groups[key]
        for i in range(0, len(ms), k):
            for m in ms[i:i + k]:
                gid[m] = len(members)
            members.append(ms[i:i + k])
    imps = [sorted({int(gid[u]) for m in g for u in t.imports[m]}) for g in members]
    cost = np.array([F + PER_MOD * max(clo[m] for m in g) + sum(var[m] for m in g) for g in members])
    lines = np.array([sum(t.lines[m] for m in g) for g in members])
    sb = np.array([sum(t.src_bytes[m] for m in g) for g in members])
    ob = None if t.out_bytes is None else np.array([sum(t.out_bytes[m] for m in g) for g in members])
    mt = Trace(f"rh-merged-{k}", [t.mods[g[0]] for g in members], imps, lines, sb, cost, ob)
    mt.order()
    return mt, cost


def main():
    rh = Trace.load(os.path.join(HERE, "data", "rh-heavy.trace.json.gz"))
    base = Trace.load(os.path.join(HERE, "data", "rh.trace.json.gz"))
    clo = np.maximum(np.array(base.meta["closure"], dtype=np.float64), 0)
    var = np.maximum(rh.cost - (0.39 + 5.7 + PER_MOD * clo), 0.0)
    rows = []
    for F in (2.0, 4.0, 6.1, 8.0):
        c = F + PER_MOD * clo + var
        rows.append(describe(rh, c, "as is", {"F_s": F}))
    for F in (6.1, 2.0):
        c = F + PER_MOD * clo + var
        ct, cc, _ = contract_chains(rh, c)
        rows.append(describe(ct, cc, "chain contraction", {"F_s": F}))
        for k in (2, 4, 8, 16, 32, 1000000):
            mt, mc = merge(rh, var, clo, F, k)
            rows.append(describe(mt, mc, f"merge same directory and depth, at most {k if k < 1000000 else 'all'}", {"F_s": F, "k": k}))
    json.dump(rows, open(os.path.join(HERE, "results", "rh-import-sensitivity.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
