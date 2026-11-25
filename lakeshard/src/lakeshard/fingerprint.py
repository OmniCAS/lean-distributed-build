"""Environment fingerprint and per-module input keys (sha256), the basis of reuse.

The fingerprint covers what is the same for every module of one build: the toolchain (the
`lean-toolchain` line and `lean --githash`), the platform, the project's absolute path (Lean
stores the source path of modules with linter messages in their `.olean`), the project's Lake
configuration, `lake-manifest.json`, and a digest of each dependency's build (the `depHash` and
output hashes in the `.trace` files Lake keeps for every dependency module, e.g. Mathlib's 8,643;
cheap to read, and they change when the dependency build changes).

A module's input key is sha256 over the fingerprint, the module name, the sha256 of its source,
its library options and Lean arguments, and the keys of its project imports, so it changes
exactly when something the module's outputs depend on changes. The artifact store keeps records
by key: a build looks up every key first and builds only what is missing (resume after a crash,
incremental rebuild after an edit, and reuse across runs are the same lookup).

A worker computes the fingerprint of its own environment and is refused if it differs.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys

from .lakeenv import LakeWorkspace
from .project import LakeProject, ProjectGraph
from .store import sha256_file

SCHEMA = "lakeshard-fingerprint/1"
_GITHASH: dict[str, str] = {}


def lean_githash(toolchain_bin: str) -> str:
    if toolchain_bin not in _GITHASH:
        out = subprocess.run([os.path.join(toolchain_bin, "lean"), "--githash"], capture_output=True, text=True)
        _GITHASH[toolchain_bin] = out.stdout.strip()
    return _GITHASH[toolchain_bin]


def dependency_digest(lib_dir: str) -> dict:
    """sha256 over (path, depHash, outputs) of every `.trace` below a dependency's `lib/lean`."""
    h = hashlib.sha256()
    n = 0
    if os.path.isdir(lib_dir):
        entries = []
        for dp, _dn, fns in os.walk(lib_dir):
            for fn in fns:
                if fn.endswith(".trace"):
                    entries.append(os.path.join(dp, fn))
        for p in sorted(entries):
            try:
                with open(p, encoding="utf-8") as fh:
                    t = json.load(fh)
            except (OSError, ValueError):
                t = {"unreadable": True}
            h.update(os.path.relpath(p, lib_dir).encode())
            h.update(json.dumps([t.get("depHash"), t.get("outputs")], sort_keys=True).encode())
            n += 1
    return {"traces": n, "sha256": h.hexdigest()}


def fingerprint(project: LakeProject, toolchain_bin: str) -> dict:
    ws = LakeWorkspace(project, os.path.join(project.project_dir, ".lake", "build"), toolchain_bin)
    tc = os.path.join(project.project_dir, "lean-toolchain")
    mf = os.path.join(project.project_dir, "lake-manifest.json")
    manifest = []
    if os.path.exists(mf):
        with open(mf, encoding="utf-8") as fh:
            for p in json.load(fh).get("packages", []):
                manifest.append({k: p.get(k) for k in ("name", "type", "url", "rev", "inputRev", "dir")})
    parts = {
        "schema": SCHEMA,
        "toolchain": open(tc, encoding="utf-8").read().strip() if os.path.exists(tc) else "",
        "lean_githash": lean_githash(toolchain_bin),
        "platform": f"{sys.platform}-{platform.machine()}",
        "project_dir": project.project_dir,
        "lakefile_sha256": sha256_file(project.lakefile),
        "manifest": manifest,
        "dependencies": {p.name: dependency_digest(p.lib_dir) for p in ws.deps},
    }
    salt = os.environ.get("LAKESHARD_TEST_FINGERPRINT_SALT")  # test hook: simulate a different environment
    if salt:
        parts["test_salt"] = salt
    return {"sha256": hashlib.sha256(json.dumps(parts, sort_keys=True).encode()).hexdigest(), "parts": parts}


def fingerprint_diff(a: dict, b: dict) -> list[str]:
    """Names of the fingerprint parts that differ (for error messages)."""
    pa, pb = a.get("parts", {}), b.get("parts", {})
    return sorted(k for k in set(pa) | set(pb) if pa.get(k) != pb.get(k))


def module_keys(graph: ProjectGraph, project: LakeProject, fp_sha256: str) -> dict[str, str]:
    keys: dict[str, str] = {}
    for m in graph.order:
        info = graph.modules[m]
        lib = project.lib_of(m)
        d = {"v": 1, "fingerprint": fp_sha256, "module": m, "package": project.package,
             "source_sha256": sha256_file(os.path.join(project.project_dir, info.path)),
             "options": project.lean_options_of(lib) if lib else None,
             "args": project.lean_args_of(lib) if lib else None,
             "imports": [[u, keys[u]] for u in sorted(info.imports)]}
        keys[m] = hashlib.sha256(json.dumps(d, sort_keys=True).encode()).hexdigest()
    return keys
