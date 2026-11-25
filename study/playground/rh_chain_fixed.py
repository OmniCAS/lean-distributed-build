import json, sys, numpy as np
sys.path.insert(0, '.')
import rh_import_sensitivity as R
from sim.trace import Trace
from sim.policies import contract_chains
rh = Trace.load('data/rh-heavy.trace.json.gz'); base = Trace.load('data/rh.trace.json.gz')
clo = np.maximum(np.array(base.meta['closure'], dtype=np.float64), 0)
var = np.maximum(rh.cost - (0.39 + 5.7 + R.PER_MOD * clo), 0.0)
rows = []
for F in (6.1, 2.0):
    c = F + R.PER_MOD * clo + var
    ct, _, groups = contract_chains(rh, c)
    cc = np.array([F + R.PER_MOD * max(clo[m] for m in g) + sum(var[m] for m in g) for g in groups])
    rows.append(R.describe(ct, cc, "chain contraction (merged file pays F once)", {"F_s": F}))
json.dump(rows, open('results/rh-chain-contraction.json', 'w'), indent=1)
