"""Generate a synthetic Lean project with the import structure of a real sub-DAG.

The shape (which module imports which) is copied from graph.bin (dag_stats.py output); the file
contents are generated here and import only Lean core, so building them runs no third-party code.

Usage:
  python3 -I gen_synthetic.py <graph.bin> <out_dir> [--target-closure 1500] [--warn-every 10]

Picks the module whose import closure is closest to --target-closure, takes that closure plus the
module itself, and writes <out_dir>/{lakefile.toml,lean-toolchain,src/Syn/M<i>.lean,dag.json}.
Every --warn-every-th module gets an unused-variable warning, so that the effect of the source
path on .olean bytes (linter messages store the absolute file name) can be observed.
"""
import json
import os
import pickle
import sys


def arg(name, default, cast=int):
    if name in sys.argv:
        return cast(sys.argv[sys.argv.index(name) + 1])
    return default


def main():
    g = pickle.load(open(sys.argv[1], "rb"))
    out = sys.argv[2]
    target = arg("--target-closure", 1500)
    warn_every = arg("--warn-every", 10)
    imports, closure, lines, order = g["imports"], g["closure"], g["lines"], g["order"]
    n = len(imports)
    # deepest module among those with closure near the target
    cands = [v for v in range(n) if abs(closure[v] - target) <= target * 0.1]
    if not cands:
        raise SystemExit("no module with closure near target")
    depth = [0] * n
    for v in order:
        depth[v] = 1 + max((depth[u] for u in imports[v]), default=0)
    root = max(cands, key=lambda v: (depth[v], -abs(closure[v] - target)))
    seen = {root}
    st = [root]
    while st:
        v = st.pop()
        for u in imports[v]:
            if u not in seen:
                seen.add(u)
                st.append(u)
    sub = [v for v in order if v in seen]  # topological order
    new = {v: i for i, v in enumerate(sub)}
    os.makedirs(os.path.join(out, "src", "Syn"), exist_ok=True)
    with open(os.path.join(out, "lean-toolchain"), "w") as fh:
        fh.write("leanprover/lean4:v4.33.1\n")
    with open(os.path.join(out, "lakefile.toml"), "w") as fh:
        fh.write('name = "syn"\nsrcDir = "src"\ndefaultTargets = ["Syn"]\n'
                 'moreLeanArgs = ["--tstack=400000"]\n\n[leanOptions]\nautoImplicit = false\n'
                 'maxHeartbeats = 4000000\n\n[[lean_lib]]\nname = "Syn"\nglobs = ["Syn.+"]\n')
    dag = {}
    for v in sub:
        i = new[v]
        imps = sorted(new[u] for u in imports[v])
        name = f"Syn.M{i}"
        dag[name] = {"imports": [f"Syn.M{j}" for j in imps], "orig_lines": lines[v], "depth": depth[v]}
        body = [f"import Syn.M{j}" for j in imps]
        body.append("")
        body.append(f"namespace Syn.M{i}")
        val = " + ".join([f"Syn.M{j}.val % 7" for j in imps] + ["1"])
        body.append(f"def val : Nat := {val}")
        body.append("theorem val_pos : 0 < val := by unfold val; omega")
        work = max(1, min(40, lines[v] // 25))
        for k in range(work):
            body.append(f"theorem w{k} (a b : Nat) : a + b + {k} = b + a + {k} := by omega")
        if warn_every and i % warn_every == 0:
            body.append("theorem warned (h : 1 = 1) : True := trivial")
        body.append(f"end Syn.M{i}")
        body.append("")
        with open(os.path.join(out, "src", "Syn", f"M{i}.lean"), "w") as fh:
            fh.write("\n".join(body))
    with open(os.path.join(out, "dag.json"), "w") as fh:
        json.dump({"root": f"Syn.M{new[root]}", "modules": dag}, fh, indent=0)
    edges = sum(len(d["imports"]) for d in dag.values())
    print(json.dumps({"modules": len(sub), "edges": edges, "root": f"Syn.M{new[root]}",
                      "root_depth": depth[root], "orig_closure": closure[root]}))


if __name__ == "__main__":
    main()
