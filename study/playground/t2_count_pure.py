import json, sys, numpy as np
sys.path.insert(0, '.')
from sim.trace import Trace
from sim.engine import Config, Machine, simulate
out = {}
for name, path in (("mathlib", "data/mathlib.trace.json.gz"), ("rh-heavy", "data/rh-heavy.trace.json.gz"), ("syn", "data/syn.trace.json.gz"), ("osv", "data/osv.trace.json.gz")):
    t = Trace.load(path); c = t.cost
    W, CP = float(c.sum()), t.critical_path(c)[0]
    blc = t.bottom_level(np.ones(t.n))
    rows = json.load(open(f"results/t2-{name}.json"))
    for r in rows:
        C = r["C"]
        mk = simulate(t, Config([Machine(C)], priority="plan", plan_key=-blc), c)["makespan_s"]
        r["blevel_count_pure"] = mk
        print(name, round(r["x"], 2), C, "count-only/best", round(mk / r["best_found"], 3), "time/best", round(r["blevel_time"] / r["best_found"], 3), flush=True)
    json.dump(rows, open(f"results/t2-{name}.json", "w"), indent=1)
