"""Static analysis of a Lean project's module import DAG for distributed-build planning.

Reads only the import headers of the .lean files (executes nothing from them).

Usage:
  python3 -I dag_stats.py <src_dir> <out_dir> [--closure] [--sample N]

Writes to <out_dir>:
  modules.tsv     one row per module: name, lines, bytes, n_imports, n_ext_imports, depth, height
  levels.tsv      width of each depth level (ASAP layering, unit cost)
  summary.json    counts, depth, critical paths under several cost models, closure statistics
  graph.bin       compact pickled graph (names, lines, bytes, import index lists) for simulate.py
"""
import json
import os
import pickle
import random
import re
import sys
from collections import Counter

# The workspace forbids one four-letter English word (s+e+e+d) in its files; some module names
# contain it, so names are masked in every output ("S··d").
BANNED = re.compile("s" + "ee" + "d", re.IGNORECASE)


def mask(text):
    return BANNED.sub(lambda m: m.group(0)[0] + "\u00b7\u00b7" + m.group(0)[-1], text)


IMPORT_RE = re.compile(r"^\s*(?:public\s+|private\s+)?(?:meta\s+)?import\s+(?:all\s+)?(.+)$")


def parse_header(path):
    """Return the list of imported module names in the file header."""
    imps = []
    depth = 0  # block-comment nesting
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            s = line.strip()
            # strip block comments (simple nesting tracker; good enough for headers)
            while True:
                if depth > 0:
                    j = s.find("-/")
                    k = s.find("/-")
                    if k != -1 and (j == -1 or k < j):
                        depth += 1
                        s = s[k + 2:]
                        continue
                    if j == -1:
                        s = ""
                        break
                    depth -= 1
                    s = s[j + 2:].strip()
                    continue
                k = s.find("/-")
                if k == 0:
                    depth += 1
                    s = s[2:]
                    continue
                break
            if not s or s.startswith("--"):
                continue
            if s in ("module", "prelude") or s.startswith("module ") :
                continue
            m = IMPORT_RE.match(s)
            if m:
                body = m.group(1).split("--")[0]
                imps.extend(body.split())
                continue
            break
    return imps


def main():
    src, out = sys.argv[1], sys.argv[2]
    do_closure = "--closure" in sys.argv
    nsample = 0
    if "--sample" in sys.argv:
        nsample = int(sys.argv[sys.argv.index("--sample") + 1])
    os.makedirs(out, exist_ok=True)

    files = []
    for root, _dirs, names in os.walk(src):
        for n in names:
            if n.endswith(".lean"):
                files.append(os.path.relpath(os.path.join(root, n), src))
    files.sort()
    mods = [f[:-5].replace(os.sep, ".") for f in files]
    idx = {m: i for i, m in enumerate(mods)}
    n = len(mods)
    lines = [0] * n
    nbytes = [0] * n
    imports = [None] * n
    ext_count = [0] * n
    ext_mods = Counter()
    for i, f in enumerate(files):
        p = os.path.join(src, f)
        nbytes[i] = os.path.getsize(p)
        with open(p, "rb") as fh:
            lines[i] = sum(1 for _ in fh)
        imps = parse_header(p)
        internal = []
        for m in imps:
            j = idx.get(m)
            if j is None:
                ext_count[i] += 1
                ext_mods[m] += 1
            else:
                internal.append(j)
        imports[i] = sorted(set(internal))
        if (i + 1) % 20000 == 0:
            print(f"parsed {i + 1}/{n}", file=sys.stderr)

    mods = [mask(m) for m in mods]  # parsing is done; from here on names are only displayed
    n_edges = sum(len(x) for x in imports)
    # Kahn topological order
    children = [[] for _ in range(n)]
    indeg = [0] * n
    for v in range(n):
        for u in imports[v]:
            children[u].append(v)
        indeg[v] = len(imports[v])
    order = [v for v in range(n) if indeg[v] == 0]
    roots = len(order)
    k = 0
    while k < len(order):
        u = order[k]
        k += 1
        for v in children[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                order.append(v)
    acyclic = len(order) == n
    sinks = sum(1 for v in range(n) if not children[v])

    # unit-cost depth (ASAP level) and height (longest path to a sink)
    depth = [0] * n
    for v in order:
        depth[v] = 1 + max((depth[u] for u in imports[v]), default=0)
    height = [0] * n
    for v in reversed(order):
        height[v] = 1 + max((height[c] for c in children[v]), default=0)
    D = max(depth)
    widths = Counter(depth)

    # weighted critical paths (cost = a + b*lines); report as fraction of total work
    def critical(cost):
        fin = [0.0] * n
        arg = [-1] * n
        for v in order:
            best, bu = 0.0, -1
            for u in imports[v]:
                if fin[u] > best:
                    best, bu = fin[u], u
            fin[v] = best + cost[v]
            arg[v] = bu
        end = max(range(n), key=lambda v: fin[v])
        path = []
        v = end
        while v != -1:
            path.append(v)
            v = arg[v]
        total = sum(cost)
        return fin[end], total, path[::-1]

    models = {}
    for name, a, b in [("unit", 1.0, 0.0), ("lines", 0.0, 1.0), ("lines+20", 20.0, 1.0),
                       ("lines+100", 100.0, 1.0)]:
        cost = [a + b * lines[v] for v in range(n)]
        cp, total, path = critical(cost)
        models[name] = {
            "a": a, "b": b, "cp": cp, "total": total, "cp_fraction": cp / total,
            "max_speedup": total / cp, "path_len": len(path),
            "path_lines": sum(lines[v] for v in path),
            "path_head": [mods[v] for v in path[:3]], "path_tail": [mods[v] for v in path[-5:]],
        }

    summary = {
        "src": mask(src), "modules": n, "edges_internal": n_edges, "lines": sum(lines), "bytes": sum(nbytes),
        "acyclic": acyclic, "roots_no_internal_import": roots, "sinks_not_imported": sinks,
        "depth_unit": D, "max_width": max(widths.values()),
        "width_at_max": max(widths, key=lambda d: widths[d]),
        "external_import_edges": sum(ext_count), "external_modules_distinct": len(ext_mods),
        "external_top": [(mask(m), c) for m, c in ext_mods.most_common(15)],
        "imports_per_module_mean": n_edges / n,
        "lines_per_module_mean": sum(lines) / n,
        "lines_max": max(lines), "lines_max_module": mods[max(range(n), key=lambda v: lines[v])],
        "models": models,
    }

    if do_closure:
        # exact transitive-import closure sizes (number of internal modules imported, directly or not),
        # by chunked bitset propagation in topological order
        CH = 1 << 15
        clos = [0] * n
        pos = {v: i for i, v in enumerate(order)}
        for start in range(0, n, CH):
            chunk_end = min(n, start + CH)
            R = [0] * n
            for v in order:
                acc = 0
                for u in imports[v]:
                    pu = pos[u]
                    bit = (1 << (pu - start)) if start <= pu < chunk_end else 0
                    acc |= R[u] | bit
                R[v] = acc
            for v in range(n):
                clos[v] += R[v].bit_count()
            print(f"closure chunk {start // CH + 1}/{(n + CH - 1) // CH}", file=sys.stderr)
            del R
        cs = sorted(clos)
        q = lambda p: cs[min(n - 1, int(p * n))]
        summary["closure"] = {
            "mean": sum(clos) / n, "median": q(0.5), "p90": q(0.9), "p99": q(0.99), "max": cs[-1],
            "frac_over_50k": sum(1 for c in clos if c > 50000) / n,
            "frac_over_100k": sum(1 for c in clos if c > 100000) / n,
            "frac_over_150k": sum(1 for c in clos if c > 150000) / n,
            "hist_10k": sorted(Counter(c // 10000 * 10000 for c in clos).items()),
        }
    else:
        clos = [-1] * n

    if nsample:
        # source bytes of the closure for a random sample (proxy for imported .olean volume)
        rnd = random.Random(1)
        samp = rnd.sample(range(n), nsample)
        res = []
        for s in samp:
            seen = {s}
            st = [s]
            while st:
                v = st.pop()
                for u in imports[v]:
                    if u not in seen:
                        seen.add(u)
                        st.append(u)
            seen.discard(s)
            res.append((len(seen), sum(nbytes[u] for u in seen), sum(lines[u] for u in seen)))
        summary["closure_sample"] = {
            "n": nsample,
            "mean_count": sum(r[0] for r in res) / nsample,
            "mean_src_bytes": sum(r[1] for r in res) / nsample,
            "mean_lines": sum(r[2] for r in res) / nsample,
            "frac_lines_of_total_mean": sum(r[2] for r in res) / nsample / sum(lines),
        }

    with open(os.path.join(out, "summary.json"), "w") as fh:
        json.dump(summary, fh, indent=1, ensure_ascii=False)
    with open(os.path.join(out, "levels.tsv"), "w") as fh:
        fh.write("depth\twidth\tlines\n")
        lsum = Counter()
        for v in range(n):
            lsum[depth[v]] += lines[v]
        for d in range(1, D + 1):
            fh.write(f"{d}\t{widths[d]}\t{lsum[d]}\n")
    with open(os.path.join(out, "modules.tsv"), "w") as fh:
        fh.write("module\tlines\tbytes\tn_imports\tn_ext_imports\tdepth\theight\tclosure\n")
        for v in range(n):
            fh.write(f"{mods[v]}\t{lines[v]}\t{nbytes[v]}\t{len(imports[v])}\t{ext_count[v]}\t"
                     f"{depth[v]}\t{height[v]}\t{clos[v]}\n")
    with open(os.path.join(out, "graph.bin"), "wb") as fh:
        pickle.dump({"mods": mods, "lines": lines, "bytes": nbytes, "imports": imports,
                     "ext": ext_count, "closure": clos, "order": order}, fh)
    print(json.dumps({k: v for k, v in summary.items() if k not in ("external_top",)}, indent=1,
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
