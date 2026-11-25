"""Thread policies, estimate models, online correction and graph transformations."""
from __future__ import annotations

import numpy as np

from .trace import Trace


# ---- threads --------------------------------------------------------------------------------
def fixed(k: int):
    return k


def critical_threads(k_hi: int, theta: float, target: float):
    """k_hi threads for modules whose estimated remaining path reaches theta * target from now
    (they can extend the makespan), 1 thread otherwise."""
    def f(st, m):
        return k_hi if st.now + st.bl[m] >= theta * target else 1
    return f


def adaptive_threads(k_max: int):
    """Share idle cores: k = free cores / (ready modules + 1), capped at k_max. Gives extra
    threads only when there are fewer ready modules than free cores (tail, narrow levels)."""
    def f(st, m):
        tot = int(st.free.sum())
        return max(1, min(k_max, tot // (st.n_ready + 1)))
    return f


def adaptive_critical(k_max: int, theta: float, target: float):
    a = adaptive_threads(k_max)

    def f(st, m):
        return a(st, m) if st.now + st.bl[m] >= theta * target else 1
    return f


# ---- estimates ------------------------------------------------------------------------------
def noisy(cost: np.ndarray, sigma: float, rng_key: int = 0) -> np.ndarray:
    """Multiplicative log-normal error (median-unbiased), e.g. history from an older commit."""
    gen = np.random.default_rng(rng_key)
    return cost * np.exp(gen.normal(0.0, sigma, size=len(cost)))


def fit_lines(lines: np.ndarray, cost: np.ndarray, kind: str = "linear") -> np.ndarray:
    """Estimate from line counts alone. linear: least squares cost ~ a + b*lines (a >= 0);
    loglog: log cost ~ a + b log(lines+1). Fitted on the same trace (an optimistic case)."""
    x = np.asarray(lines, dtype=np.float64)
    y = np.asarray(cost, dtype=np.float64)
    if kind == "linear":
        A = np.vstack([np.ones_like(x), x]).T
        a, b = np.linalg.lstsq(A, y, rcond=None)[0]
        a = max(a, 0.0)
        return a + b * x
    if kind == "loglog":
        lx, ly = np.log(x + 1), np.log(np.maximum(y, 1e-3))
        b, a = np.polyfit(lx, ly, 1)
        resid = ly - (a + b * lx)
        return np.exp(a + b * lx + resid.var() / 2)  # mean-unbiased
    if kind == "const":
        return np.full_like(y, y.mean())
    raise ValueError(kind)


class OnlineCorrection:
    """Learn a multiplicative factor per namespace group from finished modules and apply it to
    the estimates of unfinished ones at every re-rank. Group = first `level` name components."""

    def __init__(self, trace: Trace, est0: np.ndarray, level: int = 2, prior: float = 5.0):
        self.est0 = np.asarray(est0, dtype=np.float64).copy()
        names = [".".join(m.split(".")[:level]) for m in trace.mods]
        uniq = {g: i for i, g in enumerate(sorted(set(names)))}
        self.g = np.array([uniq[x] for x in names])
        self.G = len(uniq)
        self.act = np.zeros(self.G)
        self.pred = np.zeros(self.G)
        self.cnt = np.zeros(self.G)
        self.prior = prior

    def on_finish(self, st, m):
        g = self.g[m]
        self.act[g] += st.cost[m]
        self.pred[g] += self.est0[m]
        self.cnt[g] += 1

    def on_rerank(self, st):
        tot = self.act.sum() / max(self.pred.sum(), 1e-9) if self.pred.sum() > 0 else 1.0
        den = self.cnt + self.prior
        w = np.divide(self.cnt, den, out=np.zeros_like(self.cnt), where=den > 0)
        ratio = np.where(self.pred > 0, self.act / np.maximum(self.pred, 1e-9), tot)
        f = w * ratio + (1 - w) * tot
        new = self.est0 * f[self.g]
        st.est[:] = np.where(st.done, st.cost, new)


# ---- graph transformations ------------------------------------------------------------------
def contract_chains(trace: Trace, cost: np.ndarray) -> tuple[Trace, np.ndarray, list[list[int]]]:
    """Merge u -> v whenever v is u's only importer and u is v's only import (no parallelism is
    lost: v can never run concurrently with u). Returns the contracted trace, its costs and the
    groups (original indices, in build order)."""
    ch = trace.children()
    imps = trace.imports
    head = {}
    groups = []
    for m in trace.order():
        m = int(m)
        if len(imps[m]) == 1 and len(ch[imps[m][0]]) == 1:
            g = head[imps[m][0]]
            groups[g].append(m)
            head[m] = g
        else:
            head[m] = len(groups)
            groups.append([m])
    gi = np.array([head[m] for m in range(trace.n)])
    new_imps = [sorted({int(gi[u]) for u in imps[g[0]]}) for g in groups]
    c = np.array([sum(cost[m] for m in g) for g in groups])
    lines = np.array([sum(trace.lines[m] for m in g) for g in groups])
    sb = np.array([sum(trace.src_bytes[m] for m in g) for g in groups])
    ob = None
    if trace.out_bytes is not None:
        ob = np.array([np.nansum([trace.out_bytes[m] for m in g]) for g in groups])
    t = Trace(trace.name + "-chains", [trace.mods[g[0]] for g in groups], new_imps, lines, sb, c, ob,
              {"contracted_from": trace.n})
    return t, c, groups


def split_heavy(trace: Trace, cost: np.ndarray, k: int, parts: int, fixed: float) -> tuple[np.ndarray, list, float]:
    """Ideal 'structural cut': k times, take the heaviest module on the current critical path and
    split it into `parts` independent files (same imports, importers import all parts); each part
    costs (cost - fixed)/parts + fixed, where `fixed` is the per-file import/start cost.
    Returned as a modified cost vector (a module = its slowest part) + the work added."""
    c = np.asarray(cost, dtype=np.float64).copy()
    log = []
    extra = 0.0
    for _ in range(k):
        cp, path = trace.critical_path(c)
        m = max(path, key=lambda x: c[x])
        if c[m] <= 2 * fixed:
            break
        new = (c[m] - fixed) / parts + fixed
        extra += (parts - 1) * fixed
        log.append((trace.mods[m], float(c[m]), float(new), cp))
        c[m] = new
    return c, log, extra
