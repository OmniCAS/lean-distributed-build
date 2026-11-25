"""Write the narrow E1 instance (2,613 modules, W/CP ~ 5) from its spec, bench/specs/narrow.dag.json.

The spec was produced by gen_synthetic.py from a sub-closure of the RH archive's import graph; this
script writes the same Lean files without needing that graph. Every file imports only Lean core
and its own project imports. Contents (same rules as gen_synthetic.py): a value depending on the
imported values, its positivity proof by `omega`, and k = clamp(orig_lines // 25, 1, 40) small
`omega` theorems; every 10th module also gets an unused-variable warning.

Usage: python3 bench/gen/write_narrow.py bench/specs/narrow.dag.json OUT_DIR [--toolchain v4.34.0]
"""
import json
import os
import sys


def main():
    spec, out = sys.argv[1], sys.argv[2]
    tc = sys.argv[sys.argv.index("--toolchain") + 1] if "--toolchain" in sys.argv else "v4.34.0"
    d = json.load(open(spec))
    mods = d["modules"]
    os.makedirs(os.path.join(out, "src", "Syn"), exist_ok=True)
    with open(os.path.join(out, "lean-toolchain"), "w") as fh:
        fh.write(f"leanprover/lean4:{tc}\n")
    with open(os.path.join(out, "lakefile.toml"), "w") as fh:
        fh.write('name = "syn"\nsrcDir = "src"\ndefaultTargets = ["Syn"]\n'
                 'moreLeanArgs = ["--tstack=400000"]\n\n[leanOptions]\nautoImplicit = false\n'
                 'maxHeartbeats = 4000000\n\n[[lean_lib]]\nname = "Syn"\nglobs = ["Syn.+"]\n')
    for name, m in mods.items():
        i = int(name.split(".M")[1])
        body = [f"import {u}" for u in m["imports"]]
        body.append("")
        body.append(f"namespace {name}")
        val = " + ".join([f"{u}.val % 7" for u in m["imports"]] + ["1"])
        body.append(f"def val : Nat := {val}")
        body.append("theorem val_pos : 0 < val := by unfold val; omega")
        for k in range(max(1, min(40, m["orig_lines"] // 25))):
            body.append(f"theorem w{k} (a b : Nat) : a + b + {k} = b + a + {k} := by omega")
        if i % 10 == 0:
            body.append("theorem warned (h : 1 = 1) : True := trivial")
        body.append(f"end {name}")
        body.append("")
        with open(os.path.join(out, "src", "Syn", f"M{i}.lean"), "w") as fh:
            fh.write("\n".join(body))
    print(json.dumps({"modules": len(mods), "edges": sum(len(m["imports"]) for m in mods.values()), "root": d["root"]}))


if __name__ == "__main__":
    main()
