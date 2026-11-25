"""Share of import edges implied by another import (transitively redundant), by sampling edges.
Usage: python scripts/sampled_redundancy.py TRACE [samples]"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from sim.trace import Trace

t = Trace.load(sys.argv[1])
S = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
gen = np.random.default_rng(11)
edges = [(m, u) for m in range(t.n) for u in t.imports[m]]
idx = gen.choice(len(edges), size=min(S, len(edges)), replace=False)
depth = t.depth()
red = 0
for i in idx:
    m, u = edges[i]
    # is u reachable from another import v of m? only search nodes deeper than u
    stack = [v for v in t.imports[m] if v != u and depth[v] > depth[u]]
    seen = set(stack)
    found = False
    while stack and not found:
        v = stack.pop()
        for w in t.imports[v]:
            if w == u:
                found = True
                break
            if w not in seen and depth[w] > depth[u]:
                seen.add(w)
                stack.append(w)
    red += found
p = red / len(idx)
se = (p * (1 - p) / len(idx)) ** 0.5
print(json.dumps({"trace": t.name, "edges": len(edges), "sampled": len(idx), "redundant_share": round(p, 4),
                  "stderr": round(se, 4), "redundant_edges_est": int(p * len(edges))}))
