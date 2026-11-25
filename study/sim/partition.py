"""Static spatial partitions: which machine builds which module, decided before the build."""
from __future__ import annotations

import zlib

import numpy as np

from .engine import Machine
from .trace import Trace


def _caps(machines: list[Machine]) -> np.ndarray:
    c = np.array([m.cores * m.speed for m in machines], dtype=np.float64)
    return c / c.sum()


def by_hash(trace: Trace, machines: list[Machine]) -> np.ndarray:
    """Hash sharding by module name, weighted by capacity (what a naive sharder does)."""
    caps = np.cumsum(_caps(machines))
    u = np.array([zlib.crc32(m.encode()) / 2**32 for m in trace.mods])
    return np.searchsorted(caps, u, side="right").clip(0, len(machines) - 1)


def by_namespace(trace: Trace, cost: np.ndarray, machines: list[Machine], level: int = 2) -> np.ndarray:
    """Whole namespace groups (first `level` name components) per machine, balanced by
    estimated work (largest group first onto the machine with the most remaining capacity)."""
    names = [".".join(m.split(".")[:level]) for m in trace.mods]
    groups: dict[str, list[int]] = {}
    for i, g in enumerate(names):
        groups.setdefault(g, []).append(i)
    caps = _caps(machines) * float(np.sum(cost))
    load = np.zeros(len(machines))
    out = np.zeros(trace.n, dtype=np.int64)
    for g, idx in sorted(groups.items(), key=lambda kv: -sum(cost[i] for i in kv[1])):
        j = int(np.argmax(caps - load))
        out[idx] = j
        load[j] += sum(cost[i] for i in idx)
    return out


def greedy_locality(trace: Trace, cost: np.ndarray, machines: list[Machine], eps: float = 0.05,
                    weight: np.ndarray | None = None) -> np.ndarray:
    """Import-chain clustering: in build order, put each module on the machine that built most of
    its direct imports (by `weight`, e.g. artifact bytes), as long as that machine stays within
    (1 + eps) of its share of the work; otherwise on the machine with the most spare share."""
    w = np.ones(trace.n) if weight is None else np.nan_to_num(np.asarray(weight, dtype=np.float64), nan=1.0)
    caps = _caps(machines) * float(np.sum(cost)) * (1 + eps)
    load = np.zeros(len(machines))
    out = np.full(trace.n, -1, dtype=np.int64)
    M = len(machines)
    for m in trace.order():
        m = int(m)
        score = np.zeros(M)
        for u in trace.imports[m]:
            score[out[u]] += w[u]
        ok = load + cost[m] <= caps
        if ok.any() and score.max() > 0:
            s = np.where(ok, score, -1.0)
            j = int(np.argmax(s)) if s.max() > 0 else int(np.argmax(caps - load))
        else:
            j = int(np.argmax(caps - load))
        out[m] = j
        load[j] += cost[m]
    return out


def cut_fraction(trace: Trace, assign: np.ndarray) -> float:
    """Share of import edges that cross machines."""
    tot = cross = 0
    for m, imps in enumerate(trace.imports):
        for u in imps:
            tot += 1
            cross += assign[u] != assign[m]
    return cross / tot if tot else 0.0


def linear_clusters(trace: Trace, cost: np.ndarray, edge: float, passes: int = 4) -> np.ndarray:
    """Linear clustering (Kim & Browne 1988): take the heaviest path (node costs plus `edge` per
    edge) among unclustered modules as one cluster, repeat. To stay fast on 10^4-10^5 modules,
    each pass computes path lengths once and then peels paths greedily in decreasing order
    (a path stops where it meets a module already clustered in this pass); the next pass
    recomputes on what is left. The last pass takes everything. Returns cluster ids."""
    n = trace.n
    ch = trace.children()
    order = trace.order()
    c = np.asarray(cost, dtype=np.float64)
    cl = np.full(n, -1, dtype=np.int64)
    k = 0
    for ps in range(passes):
        left = int((cl < 0).sum())
        if not left:
            break
        bl = np.full(n, -np.inf)
        nxt = np.full(n, -1, dtype=np.int64)
        for m in order[::-1]:
            m = int(m)
            if cl[m] >= 0:
                continue
            best, arg = 0.0, -1
            for x in ch[m]:
                if cl[x] < 0 and edge + bl[x] > best:
                    best, arg = edge + bl[x], x
            bl[m] = c[m] + best
            nxt[m] = arg
        quota = left if ps == passes - 1 else max(1, left // 2)
        taken = 0
        for m in np.argsort(-bl):
            m = int(m)
            if taken >= quota or not np.isfinite(bl[m]):
                break
            if cl[m] >= 0:
                continue
            while m >= 0 and cl[m] < 0:
                cl[m] = k
                taken += 1
                m = int(nxt[m])
            k += 1
    return cl


def clusters_to_machines(cl: np.ndarray, cost: np.ndarray, machines: list[Machine]) -> np.ndarray:
    """Pack clusters onto machines, largest first, onto the machine with most spare capacity."""
    k = int(cl.max()) + 1
    work = np.bincount(cl, weights=cost, minlength=k)
    caps = _caps(machines) * float(np.sum(cost))
    load = np.zeros(len(machines))
    where = np.zeros(k, dtype=np.int64)
    for g in np.argsort(-work):
        j = int(np.argmax(caps - load))
        where[g] = j
        load[j] += work[g]
    return where[cl]
