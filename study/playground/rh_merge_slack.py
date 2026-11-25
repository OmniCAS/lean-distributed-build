"""Slack-aware merging: only files whose slack (CP - longest path through them) is at least a
fraction of CP are merged (same directory and depth, at most k per file); near-critical files
stay as they are. Merged file pays F once."""
import json, sys, numpy as np
sys.path.insert(0, '.')
import rh_import_sensitivity as R
from sim.trace import Trace
rh = Trace.load('data/rh-heavy.trace.json.gz'); base = Trace.load('data/rh.trace.json.gz')
clo = np.maximum(np.array(base.meta['closure'], dtype=np.float64), 0)
var = np.maximum(rh.cost - (0.39 + 5.7 + R.PER_MOD * clo), 0.0)
depth = rh.depth()
rows = []
for F in (6.1, 2.0):
    c = F + R.PER_MOD * clo + var
    cp = rh.critical_path(c)[0]
    slack = cp - (rh.earliest_finish(c) + rh.bottom_level(c) - c)
    for frac in (0.25, 0.5):
        for k in (4, 16, 64):
            groups = {}
            gid = np.empty(rh.n, dtype=np.int64); members = []
            for m in range(rh.n):
                key = (rh.mods[m].rsplit('.', 1)[0], int(depth[m])) if slack[m] >= frac * cp else ('#', m)
                groups.setdefault(key, []).append(m)
            for key in sorted(groups, key=str):
                ms = groups[key]
                for i in range(0, len(ms), k):
                    for m in ms[i:i + k]: gid[m] = len(members)
                    members.append(ms[i:i + k])
            imps = [sorted({int(gid[u]) for m in g for u in rh.imports[m]}) for g in members]
            cost = np.array([F + R.PER_MOD * max(clo[m] for m in g) + sum(var[m] for m in g) for g in members])
            mt = Trace('m', [rh.mods[g[0]] for g in members], imps, np.ones(len(members)), np.zeros(len(members)), cost)
            rows.append(R.describe(mt, cost, f"slack-aware merge: slack >= {frac:.2f} CP, at most {k}", {"F_s": F, "k": k, "slack_frac": frac,
                                   "share_mergeable": float((slack >= frac * cp).mean())}))
json.dump(rows, open('results/rh-merge-slack.json', 'w'), indent=1)
