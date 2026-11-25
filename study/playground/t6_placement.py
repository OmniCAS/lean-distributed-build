import json, sys, numpy as np
sys.path.insert(0, '.')
import t6_calibrate as T
from sim.engine import Config, Machine, simulate
d = json.load(open('results/t6-mid-B1-c16-r1.json'))
ref = T.load_history('mid-A0-c16-r1')
t = T.trace_from_spec(T.os.path.join(T.E1, "..", "specs", "mid.spec.json.gz"), ref)
c = t.cost
sp = d['speed_ratio_vs_reference']; jn = d['first_task_s']; o = d['per_task_overhead_mean_s']
rows = {}
for label, joins in (("as run (late joins)", True), ("all workers ready at 0", False)):
    ms = [Machine(16, 1 / sp[w], start_at=(jn[w] if joins else 0.0)) for w in ("worker-1", "worker-2", "worker-3")]
    for pl in ("most_free", "est", "eft", "eft_wait"):
        vals = []
        for k in range(10):
            g = np.random.default_rng(k)
            actual = c * np.exp(g.normal(0, 0.25, t.n))
            vals.append(simulate(t, Config(ms, placement=pl, task_overhead=o, est_cost=c), actual)["makespan_s"])
        rows[(label, pl)] = vals
        print(f"{label:24s} {pl:9s} median {np.median(vals):6.1f}  range {min(vals):6.1f}-{max(vals):6.1f}", flush=True)
ms = [Machine(16) for _ in range(3)]
vals = [simulate(t, Config(ms, task_overhead=o), c * np.exp(np.random.default_rng(k).normal(0, 0.25, t.n)))["makespan_s"] for k in range(10)]
print(f"{'identical machines, ready at 0':34s} median {np.median(vals):6.1f}")
json.dump({f"{a}|{b}": v for (a, b), v in rows.items()}, open('results/t6-placement.json', 'w'), indent=1)
