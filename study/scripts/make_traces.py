"""Convert the existing measurements into study traces (study/data/*.trace.json.gz).

  osv   : P230 工程 (230 modules, depends on Mathlib); costs from the reference
          `lake build` (8 threads) and from the 4x2 lakeshard run; artifact sizes from the
          reference build directory.
  syn   : the 2,613-module synthetic project (costs from the 4x3 run's history).
  rh    : the Riemann-hypothesis archive's import graph (175,187 modules; lines only, no costs).

Graphs of Lake projects are read with lakeshard's import-header parser (read-only use of
core/lakeshard). The RH graph comes from playground/rh-dag/graph.bin (written by
scripts/dag_stats.py from import headers only).
"""
import json
import os
import pickle
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.dirname(HERE)
PROJ = os.path.dirname(STUDY)
sys.path.insert(0, STUDY)
sys.path.insert(0, os.path.join(STUDY, "..", "lakeshard", "src"))
from sim.trace import Trace  # noqa: E402

PG = os.path.join(PROJ, "playground")
OUT = os.path.join(STUDY, "data")


def lake_graph(project_dir):
    from lakeshard.project import LakeProject
    lp = LakeProject.load(project_dir)
    g = lp.graph()
    names = list(g.order)
    idx = {m: i for i, m in enumerate(names)}
    imps = [[idx[u] for u in g.modules[m].imports] for m in names]
    lines = np.array([g.modules[m].lines for m in names], dtype=np.float64)
    nb = np.array([g.modules[m].bytes for m in names], dtype=np.float64)
    return names, imps, lines, nb


def artifact_bytes(build_dir, names):
    out = np.full(len(names), np.nan)
    for i, m in enumerate(names):
        rel = m.replace(".", "/")
        tot = 0
        found = False
        for sub, exts in (("lib/lean", (".olean", ".olean.server", ".olean.private", ".ilean")),):
            for e in exts:
                p = os.path.join(build_dir, sub, rel + e)
                if os.path.exists(p):
                    tot += os.path.getsize(p)
                    found = True
        if found:
            out[i] = tot
    return out


def osv():
    names, imps, lines, nb = lake_graph(os.path.join(PG, "osv"))
    ref = json.load(open(os.path.join(PG, "stages", "c-ref.history.overwritten-by-c-dyn.json")))
    dyn = {}
    for line in open(os.path.join(PG, "stages", "c-dyn-4x2", "events.jsonl")):
        e = json.loads(line)
        dyn.update(e.get("module_seconds", {}))
    cost = np.array([ref.get(m, np.nan) for m in names])
    cost_dyn = np.array([dyn.get(m, np.nan) for m in names])
    ob = artifact_bytes(os.path.join(PG, "stages", "c-ref"), names)
    t = Trace("osv", names, imps, lines, nb, cost, ob,
              {"cost_source": "reference lake build, LEAN_NUM_THREADS=8, macOS 12 cores (stage c)",
               "cost_dyn_4x2": [None if np.isnan(x) else x for x in cost_dyn.tolist()],
               "ref_wall_s": 503.2, "ref_threads": 8})
    t.save(os.path.join(OUT, "p230.trace.json.gz"))
    return t


def syn():
    names, imps, lines, nb = lake_graph(os.path.join(PG, "proto", "syn2500"))
    hist = json.load(open(os.path.join(PG, "stages", "b2-dyn-4x3", "history.json")))
    cost = np.array([hist.get(m, np.nan) for m in names])
    t = Trace("syn", names, imps, lines, nb, cost, None,
              {"cost_source": "lakeshard 4x3 dynamic run (stage b2), Lake 'Built' times",
               "ref_wall_s": 277.6})
    t.save(os.path.join(OUT, "syn.trace.json.gz"))
    return t


def rh():
    with open(os.path.join(PG, "rh-dag", "graph.bin"), "rb") as fh:
        g = pickle.load(fh)
    n = len(g["mods"])
    t = Trace("rh", list(g["mods"]), [list(map(int, x)) for x in g["imports"]],
              np.array(g["lines"], dtype=np.float64), np.array(g["bytes"], dtype=np.float64),
              np.full(n, np.nan), None,
              {"cost_source": "none (lines only)", "ext_imports": list(map(int, g["ext"])),
               "closure": list(map(int, g["closure"]))})
    t.save(os.path.join(OUT, "rh.trace.json.gz"))
    return t


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    which = sys.argv[1:] or ["osv", "syn", "rh"]
    for w in which:
        t = globals()[w]()
        c = t.cost
        known = ~np.isnan(c)
        line = {"name": t.name, "modules": t.n, "edges": sum(len(i) for i in t.imports),
                "lines": int(np.nansum(t.lines)), "cost_known": int(known.sum())}
        if known.all():
            line.update(t.summary(c))
        print(json.dumps(line))
