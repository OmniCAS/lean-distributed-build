"""Checks on an assembled build: Lake accepts it as up to date, it matches a reference build byte
for byte, and the Lean kernel accepts every module again (`leanchecker`)."""
from __future__ import annotations

import concurrent.futures as cf
import os
import subprocess
import time

from .project import LakeProject, ProjectGraph, module_output_files, module_rel
from .store import sha256_file
from .worker import lake_env, run_tracked


def _config_for(project: LakeProject, build_dir: str) -> str:
    cfg = os.path.abspath(build_dir).rstrip("/") + ".lakefile.toml"
    with open(cfg, "w", encoding="utf-8") as fh:
        fh.write(project.worker_lakefile(build_dir))
    return cfg


def lake_no_build(project: LakeProject, build_dir: str, toolchain_bin: str, rehash: bool = True,
                  targets: list[str] | None = None) -> dict:
    """`lake build --no-build [--rehash] [targets]` (default targets) against `build_dir`."""
    cfg = _config_for(project, build_dir)
    cmd = [os.path.join(toolchain_bin, "lake"), "-d", project.project_dir, "-f", cfg, "--no-ansi", "build",
           "--no-build"] + (["--rehash"] if rehash else []) + list(targets or [])
    code, out, wall, cpu, rss, _ = run_tracked(cmd, lake_env(toolchain_bin), 3600)
    return {"ok": code == 0, "exit": code, "seconds": round(wall, 2), "rehash": rehash,
            "output_tail": out.strip().splitlines()[-1] if out.strip() else ""}


def compare_builds(graph: ProjectGraph, reference_dir: str, test_dir: str,
                   suffixes=(".olean", ".ilean", ".c", ".olean.server", ".olean.private", ".ir", ".ir.sig")) -> dict:
    """Compare the outputs of every module (traces and hash files excluded: they hold paths)."""
    same = 0
    diff, missing = [], []
    for m in graph.order:
        for rel in module_output_files(reference_dir, m):
            if not rel.endswith(suffixes):
                continue
            a, b = os.path.join(reference_dir, rel), os.path.join(test_dir, rel)
            if not os.path.exists(b):
                missing.append(rel)
            elif sha256_file(a) == sha256_file(b):
                same += 1
            else:
                diff.append(rel)
    return {"identical_files": same, "different": diff[:50], "different_count": len(diff),
            "missing": missing[:50], "missing_count": len(missing), "ok": not diff and not missing}


def lean_path(project: LakeProject, build_dir: str, toolchain_bin: str) -> str:
    cfg = _config_for(project, build_dir)
    out = subprocess.run([os.path.join(toolchain_bin, "lake"), "-d", project.project_dir, "-f", cfg, "env",
                          "printenv", "LEAN_PATH"], env=lake_env(toolchain_bin), capture_output=True, text=True,
                         check=True)
    return out.stdout.strip()


def split_prefix_modules(modules: list[str]) -> tuple[list[str], list[str]]:
    """(plain, prefixes): `prefixes` are modules that are also a namespace prefix of other modules.

    `leanchecker A.B` checks A.B *and every module whose name starts with A.B*, so for a module
    like a library root `Foo` next to `Foo.Bar` one run re-checks the whole subtree.
    """
    names = set(modules)
    prefixes = {".".join(m.split(".")[:k]) for m in modules for k in range(1, len(m.split(".")))} & names
    return [m for m in modules if m not in prefixes], [m for m in modules if m in prefixes]


def leanchecker_all(project: LakeProject, graph: ProjectGraph, build_dir: str, toolchain_bin: str,
                    jobs: int = 4, modules: list[str] | None = None, fresh_root: str | None = None,
                    prefix_modules: str = "run") -> dict:
    """Replay every module's declarations through the kernel (`leanchecker M`), `jobs` at a time.

    Each run trusts the module's imports as loaded from their .olean files; since every module is
    replayed in its own run, together they cover the whole project. Modules that are also a name
    prefix of others are run after the rest (`prefix_modules="run"`, which re-checks their
    subtree) or skipped (`"skip"`, reported). `fresh_root` additionally runs `leanchecker --fresh`
    on one module (replays its whole closure, imports included).
    """
    lp = lean_path(project, build_dir, toolchain_bin)
    env = lake_env(toolchain_bin)
    env["LEAN_PATH"] = lp
    checker = os.path.join(toolchain_bin, "leanchecker")
    plain, prefixes = split_prefix_modules(modules or graph.order)
    runs = plain + (prefixes if prefix_modules == "run" else [])
    t0 = time.time()

    def one(m: str):
        code, out, wall, cpu, rss, _ = run_tracked([checker, m], env, 7200)
        return m, code, wall, rss, out[-300:]

    failed, max_rss = [], 0
    with cf.ThreadPoolExecutor(max(1, jobs)) as ex:
        for m, code, wall, rss, out in ex.map(one, runs):
            max_rss = max(max_rss, rss)
            if code != 0:
                failed.append({"module": m, "exit": code, "output": out})
    res = {"modules": len(plain) + len(prefixes), "runs": len(runs), "ok_runs": len(runs) - len(failed),
           "prefix_modules": prefixes, "prefix_modules_mode": prefix_modules, "failed": failed[:20],
           "seconds": round(time.time() - t0, 2), "jobs": jobs, "max_rss_bytes": max_rss, "ok": not failed}
    if fresh_root:
        code, out, wall, cpu, rss, _ = run_tracked([checker, "--fresh", fresh_root], env, 7200)
        res["fresh"] = {"root": fresh_root, "ok": code == 0, "seconds": round(wall, 2), "max_rss_bytes": rss,
                        "output_tail": out[-300:]}
        res["ok"] = res["ok"] and code == 0
    return res


def olean_bytes(graph: ProjectGraph, build_dir: str) -> int:
    n = 0
    for m in graph.order:
        p = os.path.join(build_dir, "lib", "lean", module_rel(m) + ".olean")
        if os.path.exists(p):
            n += os.path.getsize(p)
    return n
