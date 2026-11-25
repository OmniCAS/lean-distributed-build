"""Mathlib-calibrated cost model for the RH archive's graph (which has no measured times).

Per module:  cost = start + mathlib_import * loads_mathlib + per_module * closure + rate * lines
  start          0.39 s   `lean` on a file without imports (worker-3, measured)
  mathlib_import 5.7 s    `import Mathlib` minus start (6.1 s warm, measured, 1 thread)
  per_module     0.64 ms  per module of the project's own import closure ((6.1-0.39)/8,908)
  rate           seconds per line: Mathlib's per-file rates after removing Mathlib's own fixed
                 part (start + per_module * closure); "mean" = one rate, "heavy" = per-file rate
                 drawn from Mathlib's distribution (keeps heavy files)
`loads_mathlib`: the module has an external import (155,753 of 156,253 external import edges
are `import Mathlib`) or imports a module that does.

Writes data/rh-<mode>.trace.json.gz (same graph, modelled costs, artifact bytes estimated from
source bytes with Mathlib's ratio) and prints a summary.
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from sim.costmodel import model_costs  # noqa: E402
from sim.trace import Trace  # noqa: E402

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
START, ML_IMPORT, PER_MOD = 0.39, 5.7, (6.1 - 0.39) / 8908


def closure_sizes(t: Trace) -> np.ndarray:
    reach = [0] * t.n
    for m in t.order():
        m = int(m)
        acc = 0
        for u in t.imports[m]:
            acc |= reach[u] | (1 << u)
        reach[m] = acc
    return np.array([r.bit_count() for r in reach], dtype=np.float64)


ml = Trace.load(os.path.join(D, "mathlib.trace.json.gz"))
clo_ml = closure_sizes(ml)
fixed_ml = START + PER_MOD * clo_ml
sel = ml.lines >= 30
rates = np.maximum(ml.cost[sel] - fixed_ml[sel], 0.0) / ml.lines[sel]
ratio_bytes = float(np.nansum(ml.out_bytes) / ml.src_bytes.sum())

rh = Trace.load(os.path.join(D, "rh.trace.json.gz"))
clo = np.maximum(np.array(rh.meta["closure"], dtype=np.float64), 0)
ext = np.array(rh.meta["ext_imports"]) > 0
loads = ext.copy()
for m in rh.order():
    m = int(m)
    if not loads[m] and any(loads[u] for u in rh.imports[m]):
        loads[m] = True
fixed = START + ML_IMPORT * loads + PER_MOD * clo
summary = {"mathlib_rate_mean": float(rates.mean()), "mathlib_rate_median": float(np.median(rates)),
           "mathlib_rate_p99": float(np.percentile(rates, 99)), "mathlib_closure_mean": float(clo_ml.mean()),
           "artifact_per_source_byte": ratio_bytes, "rh_loads_mathlib": int(loads.sum()),
           "rh_closure_mean": float(clo.mean()), "rh_fixed_core_h": float(fixed.sum() / 3600)}
for mode in ("mean", "heavy"):
    var_t = Trace(rh.name, rh.mods, rh.imports, rh.lines, rh.src_bytes, np.zeros(rh.n))
    c_var, info = model_costs(var_t, rates, 0.0, mode=mode, rng_key=5)
    cost = fixed + c_var
    t = Trace(f"rh-{mode}", rh.mods, rh.imports, rh.lines, rh.src_bytes, cost, rh.src_bytes * ratio_bytes,
              {"cost_source": f"model ({mode}), calibrated on Mathlib v4.34.0 / worker-3", **{k: v for k, v in summary.items()}})
    t.save(os.path.join(D, f"rh-{mode}.trace.json.gz"))
    s = t.summary(cost)
    s["work_core_h"] = s["work_s"] / 3600
    s["cp_h"] = s["critical_path_s"] / 3600
    s["lines_core_h"] = float(c_var.sum() / 3600)
    summary[mode] = s
print(json.dumps(summary, indent=1))
