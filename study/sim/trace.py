"""A build trace: the import graph of a Lean project plus per-module data (lines, measured seconds).

Indices are 0..n-1; `imports[m]` are the internal modules m imports. Graph helpers are vectorised
by topological level so that 175k-module graphs stay fast (bottom levels in tens of milliseconds).
"""
from __future__ import annotations

import gzip
import json
from dataclasses import dataclass, field

import numpy as np


@dataclass
class Trace:
    name: str
    mods: list[str]
    imports: list[list[int]]
    lines: np.ndarray
    src_bytes: np.ndarray
    cost: np.ndarray  # measured seconds (one module, as built in the reference run); nan = unknown
    out_bytes: np.ndarray | None = None  # artifact bytes per module (olean+ilean+...), nan = unknown
    meta: dict = field(default_factory=dict)
    _cache: dict = field(default_factory=dict, repr=False)

    @property
    def n(self) -> int:
        return len(self.mods)

    # ---- structure -------------------------------------------------------------------------
    def children(self) -> list[list[int]]:
        if "children" not in self._cache:
            ch: list[list[int]] = [[] for _ in range(self.n)]
            for m, imps in enumerate(self.imports):
                for u in imps:
                    ch[u].append(m)
            self._cache["children"] = ch
        return self._cache["children"]

    def order(self) -> np.ndarray:
        """Topological order (imports before importers); raises on a cycle."""
        if "order" not in self._cache:
            indeg = np.array([len(i) for i in self.imports], dtype=np.int64)
            ch = self.children()
            stack = [m for m in range(self.n) if indeg[m] == 0]
            out = []
            while stack:
                m = stack.pop()
                out.append(m)
                for c in ch[m]:
                    indeg[c] -= 1
                    if indeg[c] == 0:
                        stack.append(c)
            if len(out) != self.n:
                raise ValueError("import graph has a cycle")
            self._cache["order"] = np.array(out, dtype=np.int64)
        return self._cache["order"]

    def depth(self) -> np.ndarray:
        """1 + longest import chain below m (roots have depth 1)."""
        if "depth" not in self._cache:
            d = np.ones(self.n, dtype=np.int64)
            for m in self.order():
                if self.imports[m]:
                    d[m] = 1 + max(d[u] for u in self.imports[m])
            self._cache["depth"] = d
        return self._cache["depth"]

    def _csr(self, which: str):
        key = "csr_" + which
        if key not in self._cache:
            adj = self.imports if which == "imports" else self.children()
            ptr = np.zeros(self.n + 1, dtype=np.int64)
            ptr[1:] = np.cumsum([len(a) for a in adj])
            idx = np.fromiter((u for a in adj for u in a), dtype=np.int64, count=int(ptr[-1]))
            self._cache[key] = (ptr, idx)
        return self._cache[key]

    def _levels(self, which: str):
        """Groups of nodes such that every neighbour (import or child) lies in an earlier group."""
        key = "lev_" + which
        if key not in self._cache:
            if which == "imports":
                lv = self.depth()
            else:
                h = np.ones(self.n, dtype=np.int64)
                ch = self.children()
                for m in self.order()[::-1]:
                    if ch[m]:
                        h[m] = 1 + max(h[c] for c in ch[m])
                lv = h
            groups = []
            srt = np.argsort(lv, kind="stable")
            bounds = np.searchsorted(lv[srt], np.arange(1, lv.max() + 2))
            for a, b in zip(bounds[:-1], bounds[1:]):
                groups.append(srt[a:b])
            self._cache[key] = groups
        return self._cache[key]

    def height(self) -> np.ndarray:
        self._levels("children")
        h = np.zeros(self.n, dtype=np.int64)
        for i, g in enumerate(self._levels("children")):
            h[g] = i + 1
        return h

    # ---- longest paths ---------------------------------------------------------------------
    def _longest(self, cost: np.ndarray, which: str, edge: float = 0.0) -> np.ndarray:
        """which='children': bottom level bl[m] = cost[m] + max(edge + bl[c]);
        which='imports': earliest finish ef[m] = cost[m] + max(edge + ef[u])."""
        ptr, idx = self._csr(which)
        out = np.zeros(self.n, dtype=np.float64)
        deg = ptr[1:] - ptr[:-1]
        for g in self._levels(which):
            has = g[deg[g] > 0]
            out[g] = cost[g]
            if len(has):
                # gather neighbour values for the nodes of this level that have neighbours
                starts = ptr[has]
                lens = deg[has]
                flat = idx[np.repeat(starts, lens) + (np.arange(lens.sum()) - np.repeat(np.cumsum(lens) - lens, lens))]
                mx = np.maximum.reduceat(out[flat], np.cumsum(lens) - lens)
                out[has] = cost[has] + edge + mx
        return out

    def bottom_level(self, cost: np.ndarray, edge: float = 0.0) -> np.ndarray:
        return self._longest(np.asarray(cost, dtype=np.float64), "children", edge)

    def earliest_finish(self, cost: np.ndarray, edge: float = 0.0) -> np.ndarray:
        return self._longest(np.asarray(cost, dtype=np.float64), "imports", edge)

    def critical_path(self, cost: np.ndarray) -> tuple[float, list[int]]:
        """Length and modules (in build order) of a longest weighted import chain."""
        cost = np.asarray(cost, dtype=np.float64)
        ef = self.earliest_finish(cost)
        m = int(np.argmax(ef))
        path = [m]
        while self.imports[m]:
            m = max(self.imports[m], key=lambda u: ef[u])
            path.append(m)
        return float(ef.max()), path[::-1]

    def summary(self, cost: np.ndarray) -> dict:
        cost = np.asarray(cost, dtype=np.float64)
        cp, path = self.critical_path(cost)
        w = float(cost.sum())
        return {"modules": self.n, "edges": int(sum(len(i) for i in self.imports)),
                "depth": int(self.depth().max()), "work_s": round(w, 1), "critical_path_s": round(cp, 1),
                "max_speedup": round(w / cp, 2) if cp else 0.0, "cp_modules": len(path)}

    # ---- io --------------------------------------------------------------------------------
    def to_json(self) -> dict:
        def arr(a):
            if a is None:
                return None
            return [None if (isinstance(x, float) and np.isnan(x)) else x for x in np.asarray(a).tolist()]
        return {"name": self.name, "mods": self.mods, "imports": self.imports, "lines": arr(self.lines),
                "src_bytes": arr(self.src_bytes), "cost": arr(self.cost), "out_bytes": arr(self.out_bytes),
                "meta": self.meta}

    def save(self, path: str) -> None:
        with gzip.open(path, "wt", encoding="utf-8") as fh:
            json.dump(self.to_json(), fh)

    @staticmethod
    def load(path: str) -> "Trace":
        with gzip.open(path, "rt", encoding="utf-8") as fh:
            d = json.load(fh)

        def arr(a, dt=np.float64):
            if a is None:
                return None
            return np.array([np.nan if x is None else x for x in a], dtype=dt)
        return Trace(d["name"], d["mods"], d["imports"], arr(d["lines"]), arr(d["src_bytes"]),
                     arr(d["cost"]), arr(d.get("out_bytes")), d.get("meta", {}))


def from_edges(n: int, edges: list[tuple[int, int]], cost, name: str = "test", out_bytes=None) -> Trace:
    """Small helper for tests: `edges` are (importer, imported)."""
    imps: list[list[int]] = [[] for _ in range(n)]
    for a, b in edges:
        imps[a].append(b)
    cost = np.asarray(cost, dtype=np.float64)
    ob = None if out_bytes is None else np.asarray(out_bytes, dtype=np.float64)
    return Trace(name, [f"M{i}" for i in range(n)], imps, np.ones(n), np.ones(n), cost, ob)


def random_dag(n: int, avg_deg: float, gen: np.random.Generator, window: int | None = None) -> Trace:
    """Random DAG: module i imports up to ~avg_deg earlier modules (optionally within a window)."""
    imps = []
    for i in range(n):
        if i == 0:
            imps.append([])
            continue
        k = min(i, gen.poisson(avg_deg))
        lo = 0 if window is None else max(0, i - window)
        imps.append(sorted(set(gen.integers(lo, i, size=k).tolist())))
    cost = gen.lognormal(0.0, 1.0, size=n)
    return Trace("random", [f"R{i}" for i in range(n)], imps, np.ones(n), np.ones(n), cost)
