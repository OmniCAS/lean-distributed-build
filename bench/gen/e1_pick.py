"""Pick the E1 wide-graph instance: a sub-closure of the archive's import graph (graph.bin) with
3,000-5,000 modules and the largest W/CP under the cost model c = c0 + t*k, k ~ original lines.
Usage: python3 -B e1_pick.py graph.bin out.json [--samples 400]"""
import json
import pickle
import random
import sys


def costs_for(lines, alpha, kmax, c0=0.2, t=0.015):
    k = max(1, min(kmax, round(lines * alpha)))
    return k, c0 + t * k


def topo(imports, nodes):
    """Topological order of `nodes` (graph.bin's numbering is NOT topological: an earlier version
    of this script assumed it was and underestimated CP by 2.3x)."""
    indeg = {v: sum(1 for u in imports[v] if u in nodes) for v in nodes}
    ch = {v: [] for v in nodes}
    for v in nodes:
        for u in imports[v]:
            ch[u].append(v)
    order = [v for v in nodes if indeg[v] == 0]
    i = 0
    while i < len(order):
        for c in ch[order[i]]:
            indeg[c] -= 1
            if indeg[c] == 0:
                order.append(c)
        i += 1
    assert len(order) == len(nodes)
    return order


def analyse(imports, nodes, lines, alpha, kmax):
    fin, W = {}, 0.0
    for v in topo(imports, nodes):
        k, c = costs_for(lines[v], alpha, kmax)
        W += c
        fin[v] = c + max((fin[u] for u in imports[v]), default=0.0)
    return W, max(fin.values())


def main():
    g = pickle.load(open(sys.argv[1], "rb"))
    imports, closure, lines, mods = g["imports"], g["closure"], g["lines"], g["mods"]
    n = len(imports)
    alpha = float(sys.argv[sys.argv.index("--alpha") + 1]) if "--alpha" in sys.argv else 1 / 25
    kmax = int(sys.argv[sys.argv.index("--kmax") + 1]) if "--kmax" in sys.argv else 400
    lo, hi = (float(x) for x in (sys.argv[sys.argv.index("--ratio") + 1].split(",") if "--ratio" in sys.argv
                                 else ["0", "1e9"]))
    cand = [v for v in range(n) if 3000 <= closure[v] + 1 <= 5000]
    random.Random(5).shuffle(cand)
    best = []
    for v in cand[: int(sys.argv[sys.argv.index("--samples") + 1]) if "--samples" in sys.argv else 400]:
        seen, st = {v}, [v]
        while st:
            x = st.pop()
            for u in imports[x]:
                if u not in seen:
                    seen.add(u)
                    st.append(u)
        W, CP = analyse(imports, seen, lines, alpha, kmax)
        if lo <= W / CP <= hi:
            best.append((W / CP, v, len(seen), W, CP))
    best.sort(key=lambda r: abs(r[3] - 9600))
    for r in best[:8]:
        print(f"W/CP {r[0]:.1f} root {mods[r[1]]} n {r[2]} W {r[3]:.0f} CP {r[4]:.0f}")
    json.dump([{"ratio": r[0], "root": r[1], "n": r[2], "W": r[3], "CP": r[4], "alpha": alpha, "kmax": kmax}
               for r in best[:20]], open(sys.argv[2], "w"))
    print(len(cand), "candidates,", len(best), "in the ratio range")


if __name__ == "__main__":
    main()
