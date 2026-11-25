"""Experiments for the seven questions. Each writes results/<q>-<trace>.json and prints Markdown.

  uv run --with numpy python experiments.py q1 data/mathlib.trace.json.gz
"""
from __future__ import annotations

import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sim.engine import Config, Machine, execute_static, simulate, simulate_ps  # noqa: E402
from sim.partition import by_hash, by_namespace, cut_fraction, greedy_locality  # noqa: E402
from sim.policies import (OnlineCorrection, adaptive_critical, adaptive_threads,  # noqa: E402
                          contract_chains, critical_threads, fit_lines, noisy, split_heavy)
from sim.trace import Trace  # noqa: E402

RES = os.path.join(HERE, "results")


def cluster(cores: int, per: int = 64) -> list[Machine]:
    if cores == 32:
        return [Machine(8, name="w1"), Machine(8, name="w2"), Machine(16, name="w3")]
    if cores <= per:
        return [Machine(cores)]
    return [Machine(per, name=f"m{i}") for i in range(cores // per)]


def md(rows: list[dict], cols: list[str] | None = None) -> str:
    if not rows:
        return ""
    cols = cols or list(rows[0])

    def f(x):
        if isinstance(x, float):
            return f"{x:.3f}" if abs(x) < 10 else f"{x:.1f}"
        return str(x)
    out = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for r in rows:
        out.append("| " + " | ".join(f(r.get(c, "")) for c in cols) + " |")
    return "\n".join(out)


def save(name: str, trace: Trace, obj) -> None:
    os.makedirs(RES, exist_ok=True)
    with open(os.path.join(RES, f"{name}-{trace.name}.json"), "w") as fh:
        json.dump(obj, fh, indent=1, default=float)


def lb(t: Trace, cost, ms) -> float:
    cap = sum(m.cores * m.speed for m in ms)
    return max(t.critical_path(cost)[0], float(np.sum(cost)) / cap)


# ---- Q1 time: task granularity ----------------------------------------------------------------
def q1(t: Trace, cost, cores_list=(32, 128, 512), overheads=(0.0, 0.05, 0.2, 0.5, 1.0, 2.0, 5.0),
       budgets=(5.0, 20.0, 60.0)):
    ct, cc, groups = contract_chains(t, cost)
    rows = []
    for C in cores_list:
        ms = cluster(C)
        L = lb(t, cost, ms)
        for o in overheads:
            r = {"cores": C, "overhead_s": o}
            r["per_module"] = simulate(t, Config(ms, task_overhead=o), cost)["makespan_s"] / L
            r["chains"] = simulate(ct, Config(ms, task_overhead=o), cc)["makespan_s"] / L
            for B in budgets:
                r[f"batch{int(B)}_mod"] = simulate(t, Config(ms, task_overhead=o, batch_budget=B), cost)["makespan_s"] / L
                r[f"batch{int(B)}_whole"] = simulate(t, Config(ms, task_overhead=o, batch_budget=B, release="batch"), cost)["makespan_s"] / L
            rows.append(r)
    info = {"modules": t.n, "after_chain_contraction": ct.n, "median_cost_s": float(np.median(cost)),
            "share_under_1s": float(np.mean(cost < 1.0)), "work_s": float(np.sum(cost))}
    save("q1", t, {"info": info, "rows": rows})
    print(json.dumps(info))
    print(md(rows))
    return rows


# ---- Q2 space: placement and network -------------------------------------------------------------
def q2(t: Trace, cost, setups=(("8+8+16", 32), ("4x64", 256), ("16x64", 1024)),
       latencies=(0.0002, 0.01, 0.1, 1.0, 5.0, 30.0), bandwidths=(1.1e9, 1.1e8, 1.2e7)):
    rows = []
    ob = t.out_bytes if t.out_bytes is not None else np.zeros(t.n)
    for name, C in setups:
        ms = cluster(C)
        L = lb(t, cost, ms)
        parts = {"hash": by_hash(t, ms), "namespace": by_namespace(t, cost, ms),
                 "chain_cluster": greedy_locality(t, cost, ms, weight=ob)}
        cuts = {k: cut_fraction(t, v) for k, v in parts.items()}
        for lat in latencies:
            for bw in bandwidths:
                r = {"setup": name, "latency_s": lat, "bandwidth_MBps": bw / 1e6}
                for pl in ("most_free", "est", "affinity"):
                    r[pl] = simulate(t, Config(ms, latency=lat, bandwidth=bw, placement=pl), cost)["makespan_s"] / L
                r["est_delay"] = simulate(t, Config(ms, latency=lat, bandwidth=bw, placement="est",
                                                    delay=0.5 * lat), cost)["makespan_s"] / L
                for k, a in parts.items():
                    r["fixed_" + k] = simulate(t, Config(ms, latency=lat, bandwidth=bw, assign=a), cost)["makespan_s"] / L
                rows.append(r)
        rows.append({"setup": name, "latency_s": "cut", **{"fixed_" + k: v for k, v in cuts.items()}})
    save("q2", t, {"rows": rows, "artifact_bytes_total": float(np.nansum(ob))})
    print(md(rows))
    return rows


# ---- Q3 structure: critical path, heavy files, imports ------------------------------------------
def transitive_redundant(t: Trace) -> np.ndarray:
    """For each module, which of its direct imports are implied by another import (bitsets)."""
    reach = [0] * t.n  # bitset of the strict import closure
    red = []
    for m in t.order():
        m = int(m)
        acc = 0
        for u in t.imports[m]:
            acc |= reach[u] | (1 << u)
        reach[m] = acc
    for m in range(t.n):
        imps = t.imports[m]
        r = []
        for u in imps:
            others = 0
            for v in imps:
                if v != u:
                    others |= reach[v]
            r.append(bool(others >> u & 1))
        red.append(r)
    return red


def q3(t: Trace, cost, fixed: float = 1.0, ks=(0, 1, 2, 5, 10, 20, 50, 100, 200), parts=(2, 4, 16),
       edge_iters=30, exact_redundancy=True):
    cost = np.asarray(cost, dtype=np.float64)
    W = float(cost.sum())
    cp, path = t.critical_path(cost)
    on = sorted(path, key=lambda m: -cost[m])
    pkg = t.meta.get("pkg")
    top = [{"module": t.mods[m], "seconds": float(cost[m]), "lines": int(t.lines[m]),
            "share_of_cp": float(cost[m] / cp)} for m in on[:10]]
    comp = {}
    for m in path:
        key = pkg[m] if pkg else t.mods[m].split(".")[0]
        comp[key] = comp.get(key, 0.0) + float(cost[m])
    res = {"work_s": W, "critical_path_s": cp, "max_speedup": W / cp, "cp_modules": len(path),
           "cp_top10": top, "cp_by_package": comp,
           "cp_small_modules_s": float(sum(cost[m] for m in path if cost[m] < 2 * fixed)),
           "depth": int(t.depth().max())}
    # depth floor: every module reduced to its fixed part
    floor = t.critical_path(np.minimum(cost, fixed))[0]
    res["depth_floor_s"] = floor
    split_rows = []
    for p in parts:
        for k in ks:
            c, log, extra = split_heavy(t, cost, k, p, fixed)
            cp2 = t.critical_path(c)[0]
            split_rows.append({"parts": p, "k": k, "cp_s": cp2, "max_speedup": (W + extra) / cp2,
                               "last_split": log[-1][0] if log else ""})
    res["split"] = split_rows
    # redundant (transitively implied) imports: removing them cannot change any longest path
    if exact_redundancy:
        red = transitive_redundant(t)
        nred = sum(sum(r) for r in red)
        imps2 = [[u for u, x in zip(t.imports[m], red[m]) if not x] for m in range(t.n)]
        t2 = Trace(t.name + "-tr", t.mods, imps2, t.lines, t.src_bytes, cost)
        res["redundant_edges"] = int(nred)
        res["edges"] = int(sum(len(i) for i in t.imports))
        res["cp_after_transitive_reduction_s"] = t2.critical_path(cost)[0]
        base = t2
    else:
        base = t
    # greedy removal of single critical imports (upper bound: assumes each removed import was unnecessary)
    imps = [list(x) for x in base.imports]
    cur = Trace(t.name + "-cut", t.mods, imps, t.lines, t.src_bytes, cost)
    edge_rows = []
    for it in range(edge_iters):
        cp0, path0 = cur.critical_path(cost)
        best = None
        for a, b in zip(path0[:-1], path0[1:]):  # b imports a
            imps[b].remove(a)
            cur._cache.clear()
            c1 = cur.critical_path(cost)[0]
            imps[b].append(a)
            if best is None or c1 < best[0]:
                best = (c1, a, b)
        cur._cache.clear()
        if best is None:
            break
        imps[best[2]].remove(best[1])
        cur._cache.clear()
        edge_rows.append({"removed": it + 1, "edge": f"{t.mods[best[2]]} -> {t.mods[best[1]]}",
                          "cp_s": best[0], "max_speedup": W / best[0]})
    res["edge_removal"] = edge_rows
    save("q3", t, res)
    print(json.dumps({k: v for k, v in res.items() if k not in ("split", "edge_removal", "cp_top10")}, indent=1))
    print(md(top))
    print(md(split_rows))
    print(md(edge_rows[:15]))
    return res


# ---- Q4 rules -----------------------------------------------------------------------------------
def q4(t: Trace, cost, cores_list=(4, 8, 16, 32, 64, 128), est=None, overhead=0.1, ps=True):
    rows = []
    est = cost if est is None else est
    for C in cores_list:
        ms = cluster(C)
        L = lb(t, cost, ms)
        r = {"cores": C, "W/C over CP": float(np.sum(cost)) / C / t.critical_path(cost)[0]}
        for pr in ("blevel", "fifo", "lpt", "random", "index"):
            r[pr] = simulate(t, Config(ms, priority=pr, est_cost=est, task_overhead=overhead), cost)["makespan_s"] / L
        if ps:
            r["os_share_C_procs"] = simulate_ps(t, cost + overhead, cores=C, max_jobs=C)["makespan_s"] / L
            r["os_share_2C_procs"] = simulate_ps(t, cost + overhead, cores=C, max_jobs=2 * C)["makespan_s"] / L
        plan = simulate(t, Config(ms, est_cost=est, record=True, task_overhead=overhead), est)
        r["static_plan"] = execute_static(t, plan, cost, ms, task_overhead=overhead)["makespan_s"] / L
        r["plan_order_dynamic"] = simulate(t, Config(ms, priority="plan", plan_key=plan["start"],
                                                     task_overhead=overhead), cost)["makespan_s"] / L
        rows.append(r)
    save("q4", t, {"rows": rows, "overhead_s": overhead})
    print(md(rows))
    return rows


# ---- Q6 estimates ------------------------------------------------------------------------------
def estimates(t: Trace, cost) -> dict:
    return {"exact": cost, "noise0.3": noisy(cost, 0.3, 1), "noise0.7": noisy(cost, 0.7, 2),
            "noise1.2": noisy(cost, 1.2, 3), "lines_linear": fit_lines(t.lines, cost, "linear"),
            "lines_loglog": fit_lines(t.lines, cost, "loglog"), "const": fit_lines(t.lines, cost, "const")}


def q6(t: Trace, cost, cores_list=(16, 32, 128), overhead=0.1, rerank=200):
    rows = []
    for C in cores_list:
        ms = cluster(C)
        L = lb(t, cost, ms)
        for name, e in estimates(t, cost).items():
            r = {"cores": C, "estimate": name,
                 "corr_log": float(np.corrcoef(np.log(np.maximum(e, 1e-3)), np.log(np.maximum(cost, 1e-3)))[0, 1])}
            r["dynamic"] = simulate(t, Config(ms, est_cost=e, task_overhead=overhead), cost)["makespan_s"] / L
            plan = simulate(t, Config(ms, est_cost=e, record=True, task_overhead=overhead), e)
            r["static"] = execute_static(t, plan, cost, ms, task_overhead=overhead)["makespan_s"] / L
            oc = OnlineCorrection(t, e)
            r["dynamic+correction"] = simulate(t, Config(ms, est_cost=e.copy(), task_overhead=overhead,
                                                         on_finish=oc.on_finish, on_rerank=oc.on_rerank,
                                                         rerank_every=rerank), cost)["makespan_s"] / L
            r["fifo"] = simulate(t, Config(ms, priority="fifo", task_overhead=overhead), cost)["makespan_s"] / L
            rows.append(r)
    save("q6", t, {"rows": rows})
    print(md(rows))
    return rows


# ---- Q5 threads ---------------------------------------------------------------------------------
def fit_amdahl(walls: dict) -> tuple[float, float]:
    """walls {k: seconds}: least squares T_k = a + b/k; returns (T_1 fit, parallel fraction p)."""
    ks = np.array(sorted(walls), dtype=np.float64)
    T = np.array([walls[k] for k in sorted(walls)])
    A = np.vstack([np.ones_like(ks), 1.0 / ks]).T
    a, b = np.linalg.lstsq(A, T, rcond=None)[0]
    a, b = max(a, 0.0), max(b, 0.0)
    return a + b, (b / (a + b) if a + b > 0 else 0.0)


def q5(t: Trace, cost, p, cores_list=(16, 32, 128, 512, 2048), overhead=0.1, kmax=16):
    from sim.engine import amdahl
    sp = amdahl(np.asarray(p, dtype=np.float64))
    rows = []
    for C in cores_list:
        ms = cluster(C)
        L = lb(t, cost, ms)
        cp_mt = t.critical_path(cost / np.array([sp(m, kmax) for m in range(t.n)]))[0]
        r = {"cores": C, "LB_1thread_s": L, "CP_at_k16_s": cp_mt}
        pol = {"k1": 1, "k2_all": 2, "k4_all": 4,
               "crit_k4": critical_threads(4, 0.9, L), "crit_k8": critical_threads(8, 0.9, L),
               "crit_k16": critical_threads(16, 0.9, L), "adaptive_k8": adaptive_threads(8),
               "adaptive_k16": adaptive_threads(16), "adaptive_crit_k16": adaptive_critical(16, 0.9, L)}
        for name, th in pol.items():
            res = simulate(t, Config(ms, threads=th, speedup=sp, task_overhead=overhead), cost)
            r[name] = res["makespan_s"] / L
            r[name + "_cpu"] = res["core_s"]["compute"] / float(np.sum(cost))
        rows.append(r)
    save("q5", t, {"rows": rows, "p_mean": float(np.mean(p))})
    print(md(rows, ["cores", "LB_1thread_s", "CP_at_k16_s"] + [k for k in rows[0] if not k.endswith("_cpu") and k not in ("cores", "LB_1thread_s", "CP_at_k16_s")]))
    return rows


# ---- Q7 extrapolation -----------------------------------------------------------------------------
def q7(t: Trace, cost, p=None, cores_list=(32, 128, 512, 2048), out_bytes=None, label=None):
    from sim.engine import amdahl
    sp = amdahl(np.asarray(p, dtype=np.float64)) if p is not None else None
    tt = t
    if out_bytes is not None:
        tt = Trace(t.name, t.mods, t.imports, t.lines, t.src_bytes, cost, out_bytes, t.meta, t._cache)
    rows = []
    W = float(np.sum(cost))
    cp = t.critical_path(cost)[0]
    for C in cores_list:
        ms = cluster(C)
        L = max(cp, W / C)
        net = dict(latency=0.0005, bandwidth=1.1e9)
        cfgs = {
            "naive (fifo, 0.5 s/task)": Config(ms, priority="fifo", task_overhead=0.5),
            "blevel": Config(ms, task_overhead=0.1, placement="est", **net),
        }
        if sp is not None:
            cfgs["blevel+threads"] = Config(ms, task_overhead=0.1, placement="est", speedup=sp,
                                             threads=adaptive_critical(16, 0.9, L), **net)
        for name, cfg in cfgs.items():
            r = simulate(tt, cfg, cost)
            rows.append({"trace": label or t.name, "cores": C, "config": name, "hours": r["makespan_s"] / 3600,
                         "ratio_to_LB": r["makespan_s"] / L, "bound": "CP" if cp >= W / C else "work",
                         "W/C_h": W / C / 3600, "CP_h": cp / 3600, "utilization": r["utilization"]})
    save("q7", t if label is None else Trace(label, [], [], np.zeros(0), np.zeros(0), np.zeros(0)), {"rows": rows})
    print(md(rows))
    return rows


if __name__ == "__main__":
    q, path = sys.argv[1], sys.argv[2]
    t = Trace.load(path)
    t0 = time.time()
    globals()[q](t, t.cost)
    print(f"({time.time() - t0:.1f} s)")
