"""Seal: turn the direct backend's outputs into a build directory that stock Lake accepts.

The direct backend writes `.olean`/`.ilean`/`.c` but not Lake's `.trace` and `.hash` files, and
Lake rebuilds any module without a trace whose input hash matches (only `lake build --old` falls
back to modification times, and it writes no traces). Instead of re-implementing Lake's hashing,
the seal step runs stock `lake build` with `LEAN_SYSROOT` pointing at a stand-in toolchain
directory: everything is a symbolic link to the real toolchain except `bin/lean`, which is
`sealshim.py`. For every module Lake "compiles", the shim copies the stored outputs into the
requested paths instead of running Lean; Lake then hashes them and writes its own traces. Modules
missing from the store are compiled by the real `lean` through the same shim, so sealing also
completes a partial build. Afterwards a plain `lake build --no-build` must succeed.

Sealing runs Lake, which reads the project configuration (a `lakefile.lean` is Lean code):
for untrusted projects run it in a sandbox. Lake's trace logs then show the shim's path instead
of the real `lean`, and warnings are not replayed by later `lake build`s (the shim prints none).
"""
from __future__ import annotations

import os
import shutil
import stat
import sys

from .project import LakeProject
from .worker import lake_env, run_tracked

SHIM = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sealshim.py")


def shim_sysroot(work_dir: str, toolchain_bin: str, python: str = sys.executable) -> str:
    """A directory that looks like the toolchain, with `bin/lean` replaced by the shim."""
    real_root = os.path.dirname(os.path.abspath(toolchain_bin))
    root = os.path.join(os.path.abspath(work_dir), "seal-sysroot")
    if os.path.lexists(root):
        shutil.rmtree(root)
    os.makedirs(os.path.join(root, "bin"))
    for e in os.listdir(real_root):
        if e != "bin":
            os.symlink(os.path.join(real_root, e), os.path.join(root, e))
    for e in os.listdir(toolchain_bin):
        if e != "lean":
            os.symlink(os.path.join(toolchain_bin, e), os.path.join(root, "bin", e))
    lean = os.path.join(root, "bin", "lean")
    with open(lean, "w") as fh:
        fh.write(f"#!/bin/sh\nexec '{python}' -I '{SHIM}' \"$@\"\n")
    os.chmod(lean, os.stat(lean).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return root


def lake_config(project: LakeProject, build_dir: str) -> str:
    cfg = os.path.abspath(build_dir).rstrip("/") + ".lakefile.toml"
    with open(cfg, "w", encoding="utf-8") as fh:
        fh.write(project.worker_lakefile(build_dir))
    return cfg


def seal(project_dir: str, store_dir: str, build_dir: str, toolchain_bin: str, work_dir: str,
         threads: int = 0, timeout_s: float = 24 * 3600, manifest: str | None = None,
         targets: list[str] | None = None) -> dict:
    """Stock `lake build` into `build_dir`, taking every module's outputs from `store_dir` (a store
    directory; records by input key from `manifest`, else by module name)."""
    proj = LakeProject.load(project_dir)
    os.makedirs(build_dir, exist_ok=True)
    cfg = lake_config(proj, build_dir)
    root = shim_sysroot(work_dir, toolchain_bin)
    log = os.path.join(os.path.abspath(work_dir), "seal-shim.log")
    if os.path.exists(log):
        os.remove(log)
    env = lake_env(toolchain_bin, threads)
    env.update({"LEAN_SYSROOT": root, "LAKE_OVERRIDE_LEAN": "true", "LAKESHARD_REAL_LEAN": os.path.join(toolchain_bin, "lean"),
                "LAKESHARD_SEAL_STORE": os.path.abspath(store_dir), "LAKESHARD_SEAL_LOG": log})
    if manifest:
        env["LAKESHARD_SEAL_MANIFEST"] = os.path.abspath(manifest)
    lake = os.path.join(toolchain_bin, "lake")
    tg = list(targets or [])
    code, out, wall, cpu, rss, _ = run_tracked([lake, "-d", proj.project_dir, "-f", cfg, "--no-ansi", "build"] + tg,
                                               env, timeout_s)
    with open(os.path.join(os.path.abspath(work_dir), "seal-lake.log"), "w", encoding="utf-8") as fh:
        fh.write(out)
    served = {"store": 0, "lean": 0}
    compiled: list[str] = []
    if os.path.exists(log):
        for line in open(log, encoding="utf-8"):
            how, _, mod = line.strip().partition(" ")
            served[how] = served.get(how, 0) + 1
            if how == "lean":
                compiled.append(mod)
    check_code, check_out, check_wall, *_ = run_tracked(
        [lake, "-d", proj.project_dir, "-f", cfg, "--no-ansi", "build", "--no-build"] + tg, lake_env(toolchain_bin),
        3600)
    return {"ok": code == 0 and check_code == 0, "lake_exit": code, "seconds": round(wall, 2), "cpu_s": round(cpu, 2),
            "from_store": served.get("store", 0), "compiled_by_lean": served.get("lean", 0),
            "compiled_modules": compiled[:50], "no_build_check": {"ok": check_code == 0, "seconds": round(check_wall, 2),
                                                                   "tail": check_out.strip().splitlines()[-1:]},
            "build_dir": os.path.abspath(build_dir), "output_tail": out.strip().splitlines()[-2:]}
