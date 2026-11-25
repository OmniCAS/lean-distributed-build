"""Lower bounds and exact optima for P | prec | Cmax (identical cores, no communication).

* simple_lb: max(CP, W/C).
* fb_bound: Fernandez–Bussell (1973). Every task j has, in a schedule of length CP, an earliest
  start e_j and a latest start l_j = CP - bl_j. Inside any window [a, b] at least
  r_j(a,b) = max(0, min(p_j, b-a, e_j+p_j-a, b-l_j)) of task j must run, whatever the schedule.
  Stretching the schedule to CP + D moves every latest start by D, so the window [a, b + D]
  still has to hold sum_j r_j(a,b); hence D >= sum_j r_j(a,b)/C - (b - a). The bound is
  CP + max over windows of that. Windows are taken between candidate points (all e_j, e_j+p_j,
  l_j, l_j+p_j, thinned to `grid` quantiles): any subset of windows still gives a valid bound.
  The window [0, CP] reproduces W/C, so fb_bound >= simple_lb.
* cpsat: exact optimum (or proven bounds within a time limit) with OR-Tools CP-SAT on integer
  durations (cost scaled and rounded; compare everything on the same rounded instance).
"""
from __future__ import annotations

import numpy as np

from .trace import Trace


def simple_lb(t: Trace, cost: np.ndarray, C: int) -> float:
    return max(t.critical_path(cost)[0], float(np.sum(cost)) / C)


def fb_bound(t: Trace, cost: np.ndarray, C: int, grid: int = 256, chunk: int = 2_000_000) -> dict:
    p = np.asarray(cost, dtype=np.float64)
    ef = t.earliest_finish(p)
    cp = float(ef.max())
    e = ef - p
    l = cp - t.bottom_level(p)
    pts = np.unique(np.concatenate([e, e + p, l, l + p, [0.0, cp]]))
    if len(pts) > grid:
        pts = np.unique(np.concatenate([np.quantile(pts, np.linspace(0, 1, grid)), [0.0, cp]]))
    n = len(p)
    best, arg = -np.inf, None
    for i, a in enumerate(pts[:-1]):
        b = pts[i + 1:]
        # process tasks in chunks so the (len(b) x n) matrix stays small
        R = np.zeros(len(b))
        step = max(1, chunk // max(1, len(b)))
        for s in range(0, n, step):
            pj, ej, lj = p[s:s + step], e[s:s + step], l[s:s + step]
            r = np.minimum.reduce([np.broadcast_to(pj, (len(b), len(pj))),
                                   (b - a)[:, None] + 0 * pj,
                                   np.broadcast_to(ej + pj - a, (len(b), len(pj))),
                                   b[:, None] - lj[None, :]])
            R += np.maximum(r, 0.0).sum(axis=1)
        val = R / C - (b - a)
        k = int(np.argmax(val))
        if val[k] > best:
            best, arg = float(val[k]), (float(a), float(b[k]))
    return {"fb_s": cp + max(best, 0.0), "cp_s": cp, "window": arg, "points": len(pts)}


def cpsat(t: Trace, cost: np.ndarray, C: int, time_limit: float = 30.0, scale: float = 10.0,
          hint_start: np.ndarray | None = None, workers: int = 8) -> dict:
    from ortools.sat.python import cp_model
    d = np.maximum(1, np.round(np.asarray(cost) * scale)).astype(int)
    n = t.n
    H = int(d.sum())
    m = cp_model.CpModel()
    s = [m.NewIntVar(0, H, f"s{j}") for j in range(n)]
    iv = [m.NewFixedSizeIntervalVar(s[j], int(d[j]), f"i{j}") for j in range(n)]
    for j in range(n):
        for u in t.imports[j]:
            m.Add(s[j] >= s[u] + int(d[u]))
    m.AddCumulative(iv, [1] * n, C)
    mk = m.NewIntVar(0, H, "mk")
    for j in range(n):
        m.Add(mk >= s[j] + int(d[j]))
    m.Minimize(mk)
    if hint_start is not None:
        for j in range(n):
            m.AddHint(s[j], int(round(hint_start[j] * scale)))
    sol = cp_model.CpSolver()
    sol.parameters.max_time_in_seconds = time_limit
    sol.parameters.num_search_workers = workers
    st = sol.Solve(m)
    ok = st in (cp_model.OPTIMAL, cp_model.FEASIBLE)
    return {"status": sol.StatusName(st), "optimal": st == cp_model.OPTIMAL,
            "best_s": sol.ObjectiveValue() / scale if ok else float("nan"),
            "bound_s": sol.BestObjectiveBound() / scale, "wall_s": sol.WallTime(),
            "durations": d / scale}
