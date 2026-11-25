"""First look at a measured trace: work, critical path, bound, heaviest modules on the critical
path, how the reference run itself used its cores, and how well a plain simulation of that run
reproduces its wall time.  Usage: python scripts/first_look.py TRACE [cores]"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from sim.engine import Config, Machine, simulate, simulate_ps  # noqa: E402
from sim.trace import Trace  # noqa: E402

t = Trace.load(sys.argv[1])
C = int(sys.argv[2]) if len(sys.argv) > 2 else 16
c = t.cost
cp, path = t.critical_path(c)
W = float(c.sum())
pkg = t.meta.get("pkg", ["?"] * t.n)
out = {"modules": t.n, "edges": int(sum(len(i) for i in t.imports)), "depth": int(t.depth().max()),
       "lines": int(t.lines.sum()), "work_s": W, "work_core_h": W / 3600, "critical_path_s": cp,
       "max_speedup": W / cp, "cp_modules": len(path), "wall_s": t.meta.get("wall_s"),
       "by_package_work_s": {}}
for p in sorted(set(pkg)):
    out["by_package_work_s"][p] = float(sum(c[i] for i in range(t.n) if pkg[i] == p))
cpu = np.array([np.nan if x is None else x for x in t.meta.get("cpu_s", [None] * t.n)], dtype=float)
if np.isfinite(cpu).any():
    k = np.isfinite(cpu)
    out["cpu_sum_s"] = float(np.nansum(cpu))
    out["cpu_over_built"] = float(np.nansum(cpu[k]) / c[k].sum())
    out["sampled_modules"] = int(k.sum())
lb = max(cp, W / C)
out[f"lower_bound_{C}_s"] = lb
if out["wall_s"]:
    out[f"wall_over_lb_{C}"] = out["wall_s"] / lb
for name, r in (("blevel", simulate(t, Config([Machine(C)]))), ("fifo", simulate(t, Config([Machine(C)], priority="fifo"))),
                ("os_share_C", simulate_ps(t, c, cores=C, max_jobs=C))):
    out[f"sim_{name}_{C}_s"] = r["makespan_s"]
top = sorted(path, key=lambda m: -c[m])[:10]
out["cp_top10"] = [{"module": t.mods[m], "pkg": pkg[m], "seconds": float(c[m]), "lines": int(t.lines[m]),
                    "share_of_cp": float(c[m] / cp),
                    "cpu_s": None if not np.isfinite(cpu[m]) else float(cpu[m])} for m in top]
heavy = np.argsort(-c)[:15]
out["heaviest15"] = [{"module": t.mods[m], "seconds": float(c[m]), "on_cp": bool(m in set(path))} for m in heavy]
print(json.dumps(out, indent=1, ensure_ascii=False))
