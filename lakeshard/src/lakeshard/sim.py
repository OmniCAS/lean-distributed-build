"""Estimate build time on P slots from per-module costs (list scheduling, longest path first)."""
from __future__ import annotations

import heapq

from .project import ProjectGraph


def critical_path(graph: ProjectGraph, costs: dict[str, float]) -> float:
    fin: dict[str, float] = {}
    for m in graph.order:
        fin[m] = costs[m] + max((fin[u] for u in graph.modules[m].imports), default=0.0)
    return max(fin.values(), default=0.0)


def simulate(graph: ProjectGraph, costs: dict[str, float], slots: int, latency_s: float = 0.0) -> dict:
    """Makespan with `slots` identical slots; `latency_s` is added between a module and its importers."""
    ch = graph.children()
    bl: dict[str, float] = {}
    for m in reversed(graph.order):
        bl[m] = costs[m] + max((bl[c] + latency_s for c in ch[m]), default=0.0)
    indeg = {m: len(i.imports) for m, i in graph.modules.items()}
    ready = [(-bl[m], m) for m, d in indeg.items() if d == 0]
    heapq.heapify(ready)
    pending: list[tuple[float, str]] = []
    running: list[tuple[float, str]] = []
    fin: dict[str, float] = {}
    free, now, done, n = slots, 0.0, 0, len(graph.modules)
    while done < n:
        while pending and pending[0][0] <= now:
            heapq.heappush(ready, (-bl[pending[0][1]], heapq.heappop(pending)[1]))
        while free and ready:
            _, m = heapq.heappop(ready)
            heapq.heappush(running, (now + costs[m], m))
            free -= 1
        now = min(x[0][0] for x in (running, pending) if x)
        while running and running[0][0] <= now:
            t, m = heapq.heappop(running)
            fin[m] = t
            free += 1
            done += 1
            for c in ch[m]:
                indeg[c] -= 1
                if indeg[c] == 0:
                    heapq.heappush(pending, (max(fin[u] for u in graph.modules[c].imports) + latency_s, c))
    total = sum(costs.values())
    mk = max(fin.values(), default=0.0)
    return {"slots": slots, "makespan_s": round(mk, 2), "work_s": round(total, 2),
            "speedup": round(total / mk, 2) if mk else 0.0,
            "critical_path_s": round(critical_path(graph, costs), 2)}
