"""Generate synthetic Lake projects with a given or random import graph, for tests and benchmarks.

The generated files import only Lean core and each other, so building them runs no foreign code.
"""
from __future__ import annotations

import json
import os
import random


def random_dag(n: int, max_imports: int = 4, locality: int = 30, roots: int = 3,
               random_state: int = 1) -> list[list[int]]:
    """imports[i] lists earlier modules; recent modules are preferred (gives deep, narrow chains)."""
    rnd = random.Random(random_state)
    imports: list[list[int]] = []
    for i in range(n):
        if i < roots:
            imports.append([])
            continue
        k = rnd.randint(1, max_imports)
        cand = set()
        for _ in range(k):
            j = i - 1 - min(i - 1, int(rnd.expovariate(1.0 / locality)))
            cand.add(max(0, j))
        imports.append(sorted(cand))
    return imports


def write_project(out: str, imports: list[list[int]], toolchain: str = "leanprover/lean4:v4.33.1",
                  package: str = "synth", lib: str = "Synth", work: list[int] | None = None,
                  warn_every: int = 10, heavy: dict[int, int] | None = None) -> dict:
    """Write lakefile.toml, lean-toolchain and one file per module; return a summary."""
    n = len(imports)
    work = work or [3] * n
    heavy = heavy or {}
    srcd = os.path.join(out, lib)
    os.makedirs(srcd, exist_ok=True)
    with open(os.path.join(out, "lean-toolchain"), "w") as fh:
        fh.write(toolchain + "\n")
    with open(os.path.join(out, "lakefile.toml"), "w") as fh:
        fh.write(f'name = "{package}"\ndefaultTargets = ["{lib}"]\nmoreLeanArgs = ["--tstack=400000"]\n\n'
                 f'[leanOptions]\nautoImplicit = false\n\n[[lean_lib]]\nname = "{lib}"\nglobs = ["{lib}.+"]\n')
    for i, imps in enumerate(imports):
        body = [f"import {lib}.M{j}" for j in imps] + ["", f"namespace {lib}.M{i}"]
        terms = [f"{lib}.M{j}.val % 7" for j in imps[:4]] + ["1"]
        body.append(f"def val : Nat := {' + '.join(terms)}")
        body.append("theorem val_pos : 0 < val := by unfold val; omega")
        for k in range(max(1, work[i])):
            body.append(f"theorem w{k} (a b : Nat) : a + b + {k} = b + a + {k} := by omega")
        for k in range(heavy.get(i, 0)):
            body.append(f"theorem h{k} : (List.range {40 + k}).foldl (· + ·) 0 = {sum(range(40 + k))} := by decide")
        if warn_every and i % warn_every == 0:
            body.append("theorem warned (h : 1 = 1) : True := trivial")
        body += [f"end {lib}.M{i}", ""]
        with open(os.path.join(srcd, f"M{i}.lean"), "w") as fh:
            fh.write("\n".join(body))
    summary = {"modules": n, "edges": sum(len(x) for x in imports), "toolchain": toolchain, "package": package}
    with open(os.path.join(out, "synth.json"), "w") as fh:
        json.dump(summary, fh)
    return summary


MODULE_SYSTEM_FILES = {
    "ModSys/A.lean": "module\n\npublic def ModSys.a : Nat := 1\n\ndef ModSys.secret : Nat := 2\n",
    "ModSys/B.lean": "module\n\npublic import ModSys.A\n\npublic def ModSys.b : Nat := ModSys.a + 1\n",
    "ModSys/C.lean": ("module\n\nimport all ModSys.A\npublic import ModSys.B\n\n"
                      "def ModSys.c : Nat := ModSys.b + ModSys.secret\n"),
    "ModSys/D.lean": "module\n\nmeta import ModSys.A\npublic import ModSys.C\n\npublic def ModSys.d : Nat := ModSys.b\n",
    "ModSys/E.lean": ("import ModSys.D\n\ndef ModSys.e : Nat := ModSys.d\n\n"
                      "theorem ModSys.warned (h : 1 = 1) : True := trivial\n"),
    "Extra/X.lean": "import ModSys.E\n\ntheorem Extra.x : ModSys.e = ModSys.e := rfl\n",
}


def write_module_system_project(out: str, toolchain: str = "leanprover/lean4:v4.35.0") -> dict:
    """A small project mixing `module` files (public/meta/all imports) and plain files, with two
    libraries that have different options and arguments; for checking the direct backend."""
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "lean-toolchain"), "w") as fh:
        fh.write(toolchain + "\n")
    with open(os.path.join(out, "lakefile.toml"), "w") as fh:
        fh.write('name = "modsys"\ndefaultTargets = ["ModSys", "Extra"]\nmoreLeanArgs = ["--tstack=400000"]\n'
                 'weakLeanArgs = ["-DmaxRecDepth=600"]\n\n[leanOptions]\nautoImplicit = false\n'
                 'linter.unusedVariables = true\n\n'
                 '[[lean_lib]]\nname = "ModSys"\nglobs = ["ModSys.+"]\n\n'
                 '[[lean_lib]]\nname = "Extra"\nglobs = ["Extra.+"]\nmoreLeanArgs = ["--tstack=300000"]\n'
                 'leanOptions = { maxHeartbeats = 300000, linter = { unusedVariables = false } }\n')
    for rel, text in MODULE_SYSTEM_FILES.items():
        p = os.path.join(out, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as fh:
            fh.write(text)
    return {"modules": len(MODULE_SYSTEM_FILES), "toolchain": toolchain}
