"""How long the top modules of the RH archive would wait for their imports, by fetch method.

Inputs measured on the two-machine Mathlib run (e1_mathlib_backtest.py): 7.4 files per module,
32.3 ms per file on the coordinator's host and 9.7 ms on the other machine when each file is one
request (the servers had Nagle on: about 40 ms per request; 0.8 ms after the fix); the root `Mathlib` still lacked 23% of the modules built on the other machine when it
started (1,017 of 4,346), the rest had been fetched by earlier tasks there.
RH (import graph only, nothing built): import closure sizes from study/data/rh.trace.json.gz;
artifact bytes from the model (59.4 GB in all) and from the public figure (about 94 GB of `.olean`
for the top modules, reports cited in docs/problem-and-roadmap.md).

A top module that starts on machine j must first fetch every module of its closure that j has
neither built nor fetched before: about closure x (1 - 1/k) x q for k machines, where q is the
share of the other machines' modules j still lacks (0.23 as in the Mathlib root, up to 1 for a
machine that has built only small modules). Usage: python rh_fetch_tail.py -> results/rh-fetch-tail.json
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sim.trace import Trace  # noqa: E402

FILES, PER_FILE, Q = 7.4, (0.0323, 0.0097), (0.23, 1.0)
FIXED = 0.0008  # per request after the Nagle fix (c28f197; loopback, measured by the tool line)


def main():
    rh = Trace.load(os.path.join(HERE, "data", "rh.trace.json.gz"))
    heavy = Trace.load(os.path.join(HERE, "data", "rh-heavy.trace.json.gz"))
    clo = np.array(rh.meta["closure"], dtype=np.float64)
    _, path = heavy.critical_path(heavy.cost)
    top = float(clo.max())
    out = {"modules": rh.n, "closure_max": int(top), "closure_over_150k": int((clo > 150000).sum()),
           "closure_over_100k": int((clo > 100000).sum()), "closure_over_50k": int((clo > 50000).sum()),
           "critical_path_modules": len(path),
           "critical_path_modules_closure_over_100k": int((clo[path] > 100000).sum()),
           "critical_path_modules_closure_over_50k": int((clo[path] > 50000).sum()),
           "mb_per_module": {"model": round(float(np.nansum(heavy.out_bytes)) / rh.n / 1e6, 3), "public": round(94e9 / rh.n / 1e6, 3)},
           "rows": []}
    for cores, k in ((128, 2), (512, 8), (2048, 32)):
        for q in Q:
            miss = top * (1 - 1 / k) * q
            row = {"cores": cores, "machines": k, "q": q, "missing_modules": round(miss),
                   "files": round(miss * FILES),
                   "one_request_per_file_h": [round(miss * FILES * p / 3600, 2) for p in PER_FILE],
                   "16_parallel_requests_min": [round(miss * FILES * p / 16 / 60, 1) for p in PER_FILE],
                   "one_request_per_file_after_nagle_fix_min": round(miss * FILES * FIXED / 60, 1)}
            for label, mb in out["mb_per_module"].items():
                gb = miss * mb / 1e3
                row[f"batched_{label}_GB"] = round(gb, 1)
                row[f"batched_{label}_s_at_1.1GBps_0.3GBps"] = [round(gb / 1.1, 0), round(gb / 0.3, 0)]
            out["rows"].append(row)
            print(json.dumps(row), flush=True)
    print(json.dumps({k: v for k, v in out.items() if k != "rows"}))
    json.dump(out, open(os.path.join(HERE, "results", "rh-fetch-tail.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
