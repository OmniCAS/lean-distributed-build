"""Priority rules for the T2 tournament, as static keys (smaller = earlier) for priority="plan",
plus a local search over priority keys (an empirical 'near optimal' among list schedules)."""
from __future__ import annotations

import numpy as np

from .engine import Config, simulate
from .trace import Trace


def descendants_work(t: Trace, cost: np.ndarray) -> np.ndarray:
    """Own cost + total cost of all transitive importers (exact, bitsets; fine up to ~10^4)."""
    ch = t.children()
    reach = [0] * t.n
    for m in t.order()[::-1]:
        m = int(m)
        acc = 0
        for c in ch[m]:
            acc |= reach[c] | (1 << c)
        reach[m] = acc
    out = np.empty(t.n)
    c = np.asarray(cost, dtype=np.float64)
    for m in range(t.n):
        r, tot, i = reach[m], c[m], 0
        while r:
            low = r & -r
            j = low.bit_length() - 1
            tot += c[j]
            r ^= low
        out[m] = tot
    return out


def keys(t: Trace, est: np.ndarray, with_descendants: bool = True) -> dict:
    bl = t.bottom_level(est)
    blc = t.bottom_level(np.ones(t.n))
    outdeg = np.array([len(x) for x in t.children()], dtype=np.float64)
    k = {"blevel_time": -bl, "blevel_count": -(blc + 1e-6 * bl),
         "cp_misf": -(bl + 1e-6 * outdeg)}
    if with_descendants:
        k["succ_work"] = -descendants_work(t, est)
    return k


def local_search(t: Trace, cfg_kwargs: dict, cost: np.ndarray, start_key: np.ndarray, iters: int = 200,
                 frac: float = 0.05, sigma: float = 0.5, rng_key: int = 0) -> tuple[float, np.ndarray, list]:
    """Hill climbing on the priority key: perturb the keys of a random subset (multiplicative
    log-normal on |key|), keep the change if the simulated makespan does not get worse."""
    gen = np.random.default_rng(rng_key)
    key = np.asarray(start_key, dtype=np.float64).copy()
    best = simulate(t, Config(priority="plan", plan_key=key, **cfg_kwargs), cost)["makespan_s"]
    hist = [best]
    for _ in range(iters):
        cand = key.copy()
        idx = gen.random(t.n) < frac
        cand[idx] = cand[idx] * np.exp(gen.normal(0, sigma, idx.sum()))
        mk = simulate(t, Config(priority="plan", plan_key=cand, **cfg_kwargs), cost)["makespan_s"]
        if mk <= best:
            best, key = mk, cand
        hist.append(best)
    return best, key, hist
