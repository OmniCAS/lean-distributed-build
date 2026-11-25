"""T2: rule tournament across x = C*CP/W (identical cores, no communication, no overhead).

Rules: remaining longest path by time / by module count, descendant work, CP/MISF (ties by
number of importers), lookahead (remaining path + half the work released at once), release
order (FIFO, ~Lake), random (mean of 3), and a local search over priority keys starting from
remaining-path-by-time (the best list schedule we can find). ETF coincides with the
remaining-path rule here (every ready module can start now on any free core).
Bounds: max(CP, W/C) and Fernandez–Bussell.  Usage: python t2_tournament.py TRACE [ls_iters] [fb_grid]
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sim.bounds import fb_bound  # noqa: E402
from sim.engine import Config, Machine, simulate  # noqa: E402
from sim.rules import keys, local_search  # noqa: E402
from sim.trace import Trace  # noqa: E402

XS = (0.1, 0.2, 0.3, 0.5, 0.7, 0.85, 1.0, 1.2, 1.5, 2.0, 3.0, 5.0, 10.0)


def main(path: str, ls_iters: int, grid: int):
    t = Trace.load(path)
    c = t.cost
    W, CP = float(c.sum()), t.critical_path(c)[0]
    ks = keys(t, c, with_descendants=t.n <= 20000)
    rows = []
    seen = set()
    for x in XS:
        C = max(1, int(round(x * W / CP)))
        if C in seen:
            continue
        seen.add(C)
        ms = [Machine(C)]
        r = {"trace": t.name, "x": C * CP / W, "C": C, "simple_lb": max(CP, W / C)}
        r["fb_lb"] = fb_bound(t, c, C, grid=grid)["fb_s"]
        for name, k in ks.items():
            r[name] = simulate(t, Config(ms, priority="plan", plan_key=k), c)["makespan_s"]
        r["lookahead"] = simulate(t, Config(ms, priority="lookahead"), c)["makespan_s"]
        r["fifo"] = simulate(t, Config(ms, priority="fifo"), c)["makespan_s"]
        r["random"] = float(np.mean([simulate(t, Config(ms, priority="random", rng_key=i), c)["makespan_s"] for i in range(3)]))
        if ls_iters:
            r["local_search"] = local_search(t, {"machines": ms}, c, ks["blevel_time"], iters=ls_iters)[0]
        best = min(v for k, v in r.items() if k not in ("trace", "x", "C", "simple_lb", "fb_lb"))
        r["best_found"] = best
        rows.append(r)
        print(json.dumps({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()}), flush=True)
    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    json.dump(rows, open(os.path.join(HERE, "results", f"t2-{t.name}.json"), "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 150, int(sys.argv[3]) if len(sys.argv) > 3 else 256)
