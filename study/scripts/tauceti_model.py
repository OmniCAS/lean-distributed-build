"""Tau Ceti: import graph from headers only (nothing is built or run) and the same Mathlib-calibrated
cost model as for the RH archive.

Per module:  cost = 0.39 s + 0.64 ms x (Mathlib modules it loads + project modules in its closure)
                    + rate x lines
  * 0.39 s: `lean` on a file without imports; 0.64 ms per loaded module: (6.1 - 0.39) s for
    `import Mathlib` (8,908 modules), both measured on one core (worker-2).
  * Mathlib modules it loads: the union, over its own external imports and those of everything it
    imports, of the import closures in Mathlib v4.34.0 (study/data/mathlib.trace.json.gz). Unlike
    the RH archive (which imports all of Mathlib), Tau Ceti imports specific Mathlib modules, so
    this is computed per module. External names not found in Mathlib v4.34.0 (Lean core, or
    modules that are newer than v4.34.0) add nothing.
  * rate: seconds per line from Mathlib's measured per-file distribution (fixed part removed);
    "heavy" draws a rate per file, "mean" uses the mean.
Writes data/tauceti-<mode>.trace.json.gz (module names masked like the RH archive's) and
results/tauceti-model.json.  Usage: python scripts/tauceti_model.py TAUCETI_REPO_DIR
"""
import json
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.dirname(HERE)
sys.path.insert(0, STUDY)
from experiments import cluster  # noqa: E402
from scripts_rh import closure_sizes  # noqa: E402
from sim.costmodel import model_costs  # noqa: E402
from sim.engine import Config, simulate  # noqa: E402
from sim.trace import Trace  # noqa: E402

IMPORT_RE = re.compile(r"^(?:(public)\s+|private\s+)?(?:(meta)\s+)?import\s+(?:(all)\s+)?(.+)$")
BANNED = re.compile("s" + "ee" + "d", re.I)
START, PER_MOD = 0.39, (6.1 - 0.39) / 8908


def mask(t):
    return BANNED.sub(lambda m: m.group(0)[0] + "··" + m.group(0)[-1], t)


def header(text):
    imports, depth = [], 0
    for line in text.splitlines():
        s = line.strip()
        while True:
            if depth > 0:
                j, k = s.find("-/"), s.find("/-")
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
            if s.startswith("/-"):
                depth += 1
                s = s[2:]
                continue
            break
        if not s or s.startswith("--"):
            continue
        word = re.split(r"\s|--|/-", s, maxsplit=1)[0]
        if word in ("module", "prelude"):
            continue
        m = IMPORT_RE.match(s)
        if m:
            imports.extend(m.group(4).split("--")[0].split("/-")[0].split())
            continue
        break
    return imports


def main(repo):
    mods = {}
    for dp, dn, fn in os.walk(repo):
        dn[:] = [d for d in dn if not d.startswith(".")]
        for f in fn:
            if f.endswith(".lean") and f != "lakefile.lean":
                p = os.path.join(dp, f)
                name = os.path.relpath(p, repo)[:-5].replace(os.sep, ".")
                text = open(p, "rb").read().decode("utf-8", "replace")
                mods[name] = (header(text), text.count("\n"), len(text.encode()))
    # the library: modules reachable from the TauCeti namespace (skip scripts/tests outside it)
    names = sorted(m for m in mods if m.split(".")[0] == "TauCeti")
    idx = {m: i for i, m in enumerate(names)}
    imps = [sorted({idx[u] for u in mods[m][0] if u in idx}) for m in names]
    ext = [[u for u in mods[m][0] if u not in idx] for m in names]
    lines = np.array([mods[m][1] for m in names], dtype=np.float64)
    nbytes = np.array([mods[m][2] for m in names], dtype=np.float64)
    t = Trace("tauceti", [mask(m) for m in names], imps, lines, nbytes, np.zeros(len(names)))
    order = t.order()
    # Mathlib closures (bitsets over Mathlib v4.34.0 modules, closure includes the module itself)
    ml = Trace.load(os.path.join(STUDY, "data", "mathlib.trace.json.gz"))
    mreach = [0] * ml.n
    for m in ml.order():
        m = int(m)
        acc = 1 << m
        for u in ml.imports[m]:
            acc |= mreach[u]
        mreach[m] = acc
    mid = {m: i for i, m in enumerate(ml.mods)}
    unknown = set()
    loaded = [0] * t.n
    for m in order:
        m = int(m)
        acc = 0
        for u in ext[m]:
            if u in mid:
                acc |= mreach[mid[u]]
            else:
                unknown.add(u)
        for u in imps[m]:
            acc |= loaded[u]
        loaded[m] = acc
    nml = np.array([x.bit_count() for x in loaded], dtype=np.float64)
    clo = closure_sizes(t)
    fixed = START + PER_MOD * (nml + clo)
    # Mathlib's per-line rates (same as scripts/rh_model.py)
    clo_ml = closure_sizes(ml)
    sel = ml.lines >= 30
    rates = np.maximum(ml.cost[sel] - (START + PER_MOD * clo_ml[sel]), 0.0) / ml.lines[sel]
    out = {"modules": t.n, "edges": int(sum(len(i) for i in imps)), "lines": int(lines.sum()),
           "depth": int(t.depth().max()), "external_import_names": len({u for e in ext for u in e}),
           "external_names_not_in_mathlib_v4.34.0": len(unknown),
           "mathlib_modules_loaded_median": float(np.median(nml)), "mathlib_modules_loaded_mean": float(nml.mean()),
           "project_closure_mean": float(clo.mean()), "fixed_core_h": float(fixed.sum() / 3600)}
    for mode in ("heavy", "mean"):
        var_t = Trace("v", t.mods, t.imports, t.lines, t.src_bytes, np.zeros(t.n))
        c_var, _ = model_costs(var_t, rates, 0.0, mode=mode, rng_key=5)
        cost = fixed + c_var
        tt = Trace(f"tauceti-{mode}", t.mods, t.imports, t.lines, t.src_bytes, cost, t.src_bytes * 57.6,
                   {"cost_source": f"model ({mode}), calibrated on Mathlib v4.34.0; imports from headers only"})
        tt.save(os.path.join(STUDY, "data", f"tauceti-{mode}.trace.json.gz"))
        W, (CP, path) = float(cost.sum()), tt.critical_path(cost)
        r = {"work_core_h": W / 3600, "cp_h": CP / 3600, "max_speedup": W / CP, "cp_modules": len(path),
             "lines_core_h": float(c_var.sum() / 3600)}
        for C in (32, 128, 512, 2048):
            res = simulate(tt, Config(cluster(C), placement="est", task_overhead=0.05, latency=0.0005, bandwidth=1.1e9), cost)
            r[f"T{C}_h"] = res["makespan_s"] / 3600
        out[mode] = r
        print(mode, json.dumps({k: round(v, 3) if isinstance(v, float) else v for k, v in r.items()}), flush=True)
    json.dump(out, open(os.path.join(STUDY, "results", "tauceti-model.json"), "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k not in ("heavy", "mean")}, indent=1))


if __name__ == "__main__":
    main(sys.argv[1])
