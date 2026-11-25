"""E1 wide-graph instance: a synthetic Lean project with the import structure of a sub-closure of
the archive's import graph; contents generated here, importing only Lean core (trusted code).

  python3 -B e1_gen.py spec graph.bin ROOT_ID spec.json.gz       (local: extract the sub-closure)
  python3 -B e1_gen.py write spec.json.gz OUT_DIR ALPHA KMAX      (server: write the project)

Module i gets k_i = clamp(round(lines_i * ALPHA), 1, KMAX) small `omega` theorems, so work is
weighted by the original file's line count (heavy-tailed). `set_option Elab.async false` makes
each file elaborate sequentially, so a module's time is its work (no hidden parallelism inside a
file). `val` adds at most 4 imported values, so no file has an `omega` problem that grows with
its number of imports. Module names keep the original directory structure under `E1.`
(namespaces inside the files are numbered). Python 3.8 compatible.
"""
import gzip
import json
import os
import pickle
import sys


def spec(graph_bin, root, out):
    g = pickle.load(open(graph_bin, "rb"))
    imports, mods, lines = g["imports"], g["mods"], g["lines"]
    seen, st = {root}, [root]
    while st:
        x = st.pop()
        for u in imports[x]:
            if u not in seen:
                seen.add(u)
                st.append(u)
    order = sorted(seen)  # graph.bin numbers modules topologically
    new = {v: i for i, v in enumerate(order)}
    d = {"root": mods[root], "names": ["E1." + mods[v] for v in order], "lines": [lines[v] for v in order],
         "imports": [sorted(new[u] for u in imports[v]) for v in order]}
    with gzip.open(out, "wt") as fh:
        json.dump(d, fh)
    print(json.dumps({"modules": len(order), "edges": sum(len(x) for x in d["imports"])}))


def write(spec_path, out, alpha, kmax):
    with gzip.open(spec_path, "rt") as fh:
        d = json.load(fh)
    names, lines, imports = d["names"], d["lines"], d["imports"]
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "lean-toolchain"), "w") as fh:
        fh.write("leanprover/lean4:v4.34.0\n")
    with open(os.path.join(out, "lakefile.toml"), "w") as fh:
        fh.write('name = "e1"\ndefaultTargets = ["E1"]\n\n[leanOptions]\nautoImplicit = false\n\n'
                 '[[lean_lib]]\nname = "E1"\nglobs = ["E1.+"]\n')
    total_k = 0
    ks = []
    for i, name in enumerate(names):
        k = max(1, min(kmax, int(round(lines[i] * alpha))))
        ks.append(k)
        total_k += k
        body = ["import " + names[j] for j in imports[i]]
        body += ["", "set_option Elab.async false", "", "namespace E1N.M%d" % i]
        terms = ["E1N.M%d.val %% 7" % j for j in imports[i][:4]] + ["1"]
        body.append("def val : Nat := " + " + ".join(terms))
        body.append("theorem val_pos : 0 < val := by unfold val; omega")
        for t in range(k):
            body.append("theorem w%d (a b : Nat) : a + b + %d = b + a + %d := by omega" % (t, t, t))
        body += ["end E1N.M%d" % i, ""]
        p = os.path.join(out, *name.split(".")) + ".lean"
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as fh:
            fh.write("\n".join(body))
    ks.sort()
    print(json.dumps({"modules": len(names), "theorems": total_k, "k_median": ks[len(ks) // 2],
                      "k_p99": ks[int(len(ks) * 0.99)], "k_max": ks[-1], "alpha": alpha, "kmax": kmax}))


if __name__ == "__main__":
    if sys.argv[1] == "spec":
        spec(sys.argv[2], int(sys.argv[3]), sys.argv[4])
    else:
        write(sys.argv[2], sys.argv[3], float(sys.argv[4]), int(sys.argv[5]))
