"""Cost estimates and the shard plan: a partition of the modules whose quotient graph is acyclic."""
from __future__ import annotations

import json
import os

from .project import ProjectGraph
from .protocol import SCHEMA, Plan, ShardSpec


def estimate_costs(graph: ProjectGraph, history: dict[str, float] | None = None,
                   fixed: float = 2.0, per_line: float = 0.04, per_import: float = 0.0005) -> dict[str, float]:
    """Seconds of one core per module: measured times when known, else a + b*lines + c*closure."""
    history = history or {}
    clos = graph.closure_sizes() if per_import else {}
    out = {}
    for m, info in graph.modules.items():
        if m in history:
            out[m] = float(history[m])
        else:
            out[m] = fixed + per_line * info.lines + per_import * clos.get(m, 0)
    return out


def load_history(path: str | None) -> dict[str, float]:
    if not path or not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as fh:
        return {k: float(v) for k, v in json.load(fh).items()}


def make_plan(graph: ProjectGraph, costs: dict[str, float], target_cost: float | None = None,
              shards: int | None = None) -> Plan:
    """Group modules into shards of about `target_cost` seconds (or `shards` shards).

    Modules are visited in topological order. A module joins the open shard of one of its imports
    (the one holding most of its imports) when that keeps the shard under the target and cannot
    create a cycle between shards; otherwise it opens a new shard. Shard-level ancestry is kept as
    bitsets, so the test "would the shards form a cycle" is exact.
    """
    total = sum(costs.values())
    if target_cost is None:
        target_cost = total / max(1, shards or 1)
    target_cost = max(target_cost, 1e-9)
    shard_of: dict[str, int] = {}
    members: list[list[str]] = []
    cost: list[float] = []
    anc: list[int] = []  # bitset: shards each shard depends on (transitively)
    desc: list[int] = []  # bitset: shards that depend on each shard (transitively)
    for m in graph.order:
        imp_shards: dict[int, int] = {}
        for u in graph.modules[m].imports:
            s = shard_of[u]
            imp_shards[s] = imp_shards.get(s, 0) + 1
        chosen = None
        for s, _cnt in sorted(imp_shards.items(), key=lambda kv: (-kv[1], -cost[kv[0]], kv[0])):
            if cost[s] + costs[m] > target_cost and cost[s] > 0:
                continue
            # joining s adds edges s -> t for the other import shards t: a cycle iff t depends on s
            if any(t != s and (anc[t] >> s) & 1 for t in imp_shards):
                continue
            chosen = s
            break
        if chosen is None:
            chosen = len(members)
            members.append([])
            cost.append(0.0)
            anc.append(0)
            desc.append(0)
        shard_of[m] = chosen
        members[chosen].append(m)
        cost[chosen] += costs[m]
        new_anc = 0
        for t in imp_shards:
            if t != chosen:
                new_anc |= anc[t] | (1 << t)
        gained = new_anc & ~anc[chosen]
        if gained:
            affected = desc[chosen] | (1 << chosen)
            for r in _bits(affected):
                anc[r] |= gained
            for t in _bits(gained):
                desc[t] |= affected
    specs = []
    for i, mods in enumerate(members):
        deps = sorted({shard_of[u] for m in mods for u in graph.modules[m].imports} - {i})
        specs.append(ShardSpec(f"s{i:05d}", mods, [f"s{d:05d}" for d in deps], round(cost[i], 3)))
    plan = Plan(SCHEMA, graph.package, specs)
    check_plan(graph, plan)
    plan.stats = plan_stats(graph, plan, costs)
    return plan


def _bits(x: int):
    while x:
        b = x & -x
        yield b.bit_length() - 1
        x ^= b


def check_plan(graph: ProjectGraph, plan: Plan) -> None:
    """Every module in exactly one shard; shard dependencies complete; the shard graph is acyclic."""
    where: dict[str, str] = {}
    for s in plan.shards:
        for m in s.modules:
            if m in where:
                raise ValueError(f"{m} in two shards")
            where[m] = s.id
    missing = set(graph.modules) - set(where)
    if missing:
        raise ValueError(f"modules without shard: {sorted(missing)[:5]}")
    ids = {s.id: s for s in plan.shards}
    for s in plan.shards:
        need = {where[u] for m in s.modules for u in graph.modules[m].imports} - {s.id}
        if not need <= set(s.deps):
            raise ValueError(f"shard {s.id} misses dependencies {sorted(need - set(s.deps))}")
    state: dict[str, int] = {}

    def visit(sid: str) -> None:
        stack = [(sid, iter(ids[sid].deps))]
        state[sid] = 1
        while stack:
            cur, it = stack[-1]
            nxt = next(it, None)
            if nxt is None:
                state[cur] = 2
                stack.pop()
            elif state.get(nxt) == 1:
                raise ValueError(f"cycle through shards {cur} and {nxt}")
            elif nxt not in state:
                state[nxt] = 1
                stack.append((nxt, iter(ids[nxt].deps)))

    for s in plan.shards:
        if s.id not in state:
            visit(s.id)


def shard_order(plan: Plan) -> list[str]:
    ids = {s.id: s for s in plan.shards}
    indeg = {s.id: len(s.deps) for s in plan.shards}
    ch: dict[str, list[str]] = {s.id: [] for s in plan.shards}
    for s in plan.shards:
        for d in s.deps:
            ch[d].append(s.id)
    ready = sorted(k for k, v in indeg.items() if v == 0)
    out = []
    while ready:
        u = ready.pop()
        out.append(u)
        for v in ch[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                ready.append(v)
    assert len(out) == len(ids)
    return out


def bottom_levels(plan: Plan) -> dict[str, float]:
    """Cost of the heaviest shard chain starting at each shard (scheduling priority)."""
    ids = {s.id: s for s in plan.shards}
    ch: dict[str, list[str]] = {s.id: [] for s in plan.shards}
    for s in plan.shards:
        for d in s.deps:
            ch[d].append(s.id)
    bl: dict[str, float] = {}
    for sid in reversed(shard_order(plan)):
        bl[sid] = ids[sid].cost + max((bl[c] for c in ch[sid]), default=0.0)
    return bl


def plan_stats(graph: ProjectGraph, plan: Plan, costs: dict[str, float]) -> dict:
    # module-level critical path (lower bound on any schedule)
    fin: dict[str, float] = {}
    for m in graph.order:
        fin[m] = costs[m] + max((fin[u] for u in graph.modules[m].imports), default=0.0)
    bl = bottom_levels(plan)
    sizes = sorted(len(s.modules) for s in plan.shards)
    total = sum(costs.values())
    return {
        "modules": len(graph.modules), "shards": len(plan.shards),
        "edges": sum(len(i.imports) for i in graph.modules.values()),
        "shard_edges": sum(len(s.deps) for s in plan.shards),
        "total_cost_s": round(total, 1),
        "module_critical_path_s": round(max(fin.values(), default=0.0), 1),
        "shard_critical_path_s": round(max(bl.values(), default=0.0), 1),
        "max_speedup_module_level": round(total / max(fin.values(), default=1.0), 1) if fin else 0,
        "shard_size_min_median_max": [sizes[0], sizes[len(sizes) // 2], sizes[-1]] if sizes else [],
        "shard_cost_max_s": round(max(s.cost for s in plan.shards), 1) if plan.shards else 0,
    }


def shard_needs(graph: ProjectGraph, plan: Plan) -> dict[str, list[str]]:
    """Modules whose outputs must be present on a worker before it builds each shard."""
    out = {}
    for s in plan.shards:
        mods = set(s.modules)
        out[s.id] = sorted(graph.closure(s.modules) - mods)
    return out
