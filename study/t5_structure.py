"""T5: the critical chain file by file (Mathlib). For each module on the critical path, the new
critical path if only that one module changes: (a) 2 threads (measured curve), (b) split into 4
independent files (each pays the fixed start+import part, 0.39 s + 0.64 ms per closure module),
(c) its import edge to the previous module on the chain is removed (if that import were not
needed). Also: how many modules are near-critical (slack <= 2/5/10% of CP), which is why
speeding up the critical chain alone soon stops helping.  Usage: python t5_structure.py"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sim.trace import Trace
from t4_threads import speedup_table
from scripts_rh import closure_sizes  # noqa


def main():
    t = Trace.load(os.path.join(HERE, "data", "mathlib.trace.json.gz"))
    c = t.cost
    tab, med, _ = speedup_table(t, os.path.join(HERE, "data", "runs", "replay-w3", "replay.jsonl"))
    fixed = 0.39 + 0.00064 * closure_sizes(t)
    cp, path = t.critical_path(c)
    ef = t.earliest_finish(c)
    bl = t.bottom_level(c)
    slack = cp - (ef + bl - c)
    near = {f"slack<={int(q*100)}%": int((slack <= q * cp).sum()) for q in (0.0, 0.02, 0.05, 0.10)}
    rows = []
    for pos, m in enumerate(path):
        r = {"module": t.mods[m], "seconds": float(c[m])}
        c2 = c.copy(); c2[m] = c[m] / tab[m, 1]
        r["threads2_cp"] = t.critical_path(c2)[0]
        c3 = c.copy(); c3[m] = max(fixed[m], (c[m] - fixed[m]) / 4 + fixed[m])
        r["split4_cp"] = t.critical_path(c3)[0]
        if pos > 0:
            prev = path[pos - 1]
            imps = [list(x) for x in t.imports]
            imps[m].remove(prev)
            t2 = Trace("cut", t.mods, imps, t.lines, t.src_bytes, c)
            r["cut_edge_cp"] = t2.critical_path(c)[0]
        rows.append(r)
    best = sorted(rows, key=lambda r: min(r["threads2_cp"], r["split4_cp"], r.get("cut_edge_cp", 1e9)))[:12]
    out = {"cp_s": cp, "cp_modules": len(path), "near_critical": near, "n": t.n,
           "fixed_part_on_cp_s": float(sum(fixed[m] for m in path)), "rows": rows}
    json.dump(out, open(os.path.join(HERE, "results", "t5-mathlib.json"), "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "rows"}))
    for r in best:
        print(f"{r['module'][:60]:60s} {r['seconds']:5.0f}  thr2 {cp - r['threads2_cp']:5.1f}  split4 {cp - r['split4_cp']:5.1f}  cut {cp - r.get('cut_edge_cp', cp):5.1f}")


if __name__ == "__main__":
    main()
