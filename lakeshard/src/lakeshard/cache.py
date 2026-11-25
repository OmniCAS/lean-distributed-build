"""The build cache: what `lakeshard run` produces and `lakeshard restore` consumes.

A cache is a directory:

    manifest.json        schema, source (repository, commit, path), package, toolchain,
                         environment fingerprint, build directory (relative to the package),
                         module -> input key, and every file: path (relative to the build
                         directory), sha256, size
    objects/ab/abcd...   the files, named by sha256 (copies, never links to the build directory)

The files are those of a sealed build directory (see `seal.py`): for every module its outputs
(`.olean`, `.ilean`, `.c`, and for `module` files `.olean.server`, `.olean.private`, `.ir`,
`.ir.sig`) and Lake's own `.trace` and `.hash` files, so after `restore` stock `lake build` finds
everything up to date. Lake's trace hashes do not depend on paths, so a checkout at another
path is accepted too (the `.olean` files then record the original path in linter messages).
The command lines Lake logs in its traces (with the build machine's paths) are removed.
"""
from __future__ import annotations

import json
import os
import shutil
import time

from .fingerprint import fingerprint, fingerprint_diff
from .project import LakeProject, ProjectError, ProjectGraph, module_output_files
from .store import IntegrityError, sha256_file
from .worker import lake_env, run_tracked

SCHEMA = "lakeshard-cache/1"
# parts of the fingerprint a restore must match (the path and lakefile hash may differ)
RESTORE_PARTS = ("toolchain", "lean_githash", "platform", "manifest", "dependencies", "test_salt")


def _place(src: str, dst: str) -> None:
    """Copy into the cache. Never a hard link: Lake rewrites files of the sealed build directory in
    place on the next seal, which would change an object under its sha256 name. (On APFS and
    similar file systems the copy is a cheap clone.)"""
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    tmp = f"{dst}.tmp{os.getpid()}"
    shutil.copyfile(src, tmp)
    os.replace(tmp, dst)


def _strip_trace_commands(path: str) -> None:
    """Drop the trace-level log entries (the command line, with this machine's paths) from a Lake
    `.trace`; Lake decides up-to-dateness from the hashes only, and replays only the log."""
    with open(path, encoding="utf-8") as fh:
        t = json.load(fh)
    log = t.get("log")
    if isinstance(log, list) and any(e.get("level") == "trace" for e in log if isinstance(e, dict)):
        t["log"] = [e for e in log if not (isinstance(e, dict) and e.get("level") == "trace")]
        tmp = f"{path}.tmp{os.getpid()}"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(t, fh, indent=1)
        os.replace(tmp, path)


def pack(project: LakeProject, graph: ProjectGraph, sealed_build_dir: str, cache_dir: str, fp: dict,
         keys: dict[str, str], source: dict | None = None, targets: list[str] | None = None) -> dict:
    t0 = time.time()
    files = []
    nbytes = 0
    for m in graph.order:
        for rel in module_output_files(sealed_build_dir, m):
            p = os.path.join(sealed_build_dir, rel)
            if rel.endswith(".trace"):
                _strip_trace_commands(p)
            sha = sha256_file(p)
            obj = os.path.join(cache_dir, "objects", sha[:2], sha)
            if not os.path.exists(obj):
                _place(p, obj)
            size = os.path.getsize(p)
            files.append({"path": rel, "sha256": sha, "size": size})
            nbytes += size
    tc = os.path.join(project.project_dir, "lean-toolchain")
    man = {"schema": SCHEMA, "created": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "source": source or {},
           "package": project.package, "toolchain": open(tc).read().strip() if os.path.exists(tc) else "",
           "fingerprint": fp, "build_dir": project.build_dir, "modules": dict(sorted(keys.items())),
           "targets": list(targets or []),
           "files": files, "file_count": len(files), "bytes": nbytes}
    with open(os.path.join(cache_dir, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(man, fh, indent=0)
    return {"cache": os.path.abspath(cache_dir), "files": len(files), "bytes": nbytes,
            "seconds": round(time.time() - t0, 2)}


def restore(cache_dir: str, checkout: str, toolchain_bin: str, check: bool = True, force: bool = False) -> dict:
    """Put the cache into the build directory of `checkout`; then (check) `lake build --no-build`."""
    t0 = time.time()
    with open(os.path.join(cache_dir, "manifest.json"), encoding="utf-8") as fh:
        man = json.load(fh)
    if man.get("schema") != SCHEMA:
        raise ValueError(f"not a lakeshard cache: {cache_dir}")
    try:
        proj = LakeProject.load(checkout)
    except ProjectError:
        if not os.path.exists(os.path.join(checkout, "lakefile.lean")):
            raise
        from .project import translate
        proj = LakeProject.load(checkout, config=translate(checkout, toolchain_bin))
    targets = man.get("targets") or None
    mine = fingerprint(proj, toolchain_bin, proj.graph(targets))
    diff = [k for k in fingerprint_diff(man["fingerprint"], mine) if k in RESTORE_PARTS]
    if diff and not force:
        return {"ok": False, "refused": "environment differs from the cache's", "parts": diff}
    if proj.package != man["package"]:
        return {"ok": False, "refused": f"package {proj.package!r} is not the cache's {man['package']!r}"}
    dest = os.path.join(proj.project_dir, proj.build_dir)
    n = nbytes = 0
    for f in man["files"]:
        src = os.path.join(cache_dir, "objects", f["sha256"][:2], f["sha256"])
        if not os.path.exists(src) or sha256_file(src) != f["sha256"]:
            raise IntegrityError(f"cache object for {f['path']} is missing or corrupt")
        dst = os.path.join(dest, f["path"])
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        tmp = f"{dst}.tmp{os.getpid()}"
        shutil.copyfile(src, tmp)
        os.replace(tmp, dst)
        n += 1
        nbytes += f["size"]
    out = {"ok": True, "build_dir": dest, "files": n, "bytes": nbytes, "seconds": round(time.time() - t0, 2),
           "same_path": man["fingerprint"]["parts"].get("project_dir") == proj.project_dir, "forced_parts": diff}
    if check:
        code, text, wall, *_ = run_tracked([os.path.join(toolchain_bin, "lake"), "-d", proj.project_dir, "--no-ansi",
                                            "build", "--no-build"], lake_env(toolchain_bin), 3600)
        out["lake_no_build"] = {"ok": code == 0, "seconds": round(wall, 2),
                                "tail": text.strip().splitlines()[-1:] if text.strip() else []}
        out["ok"] = code == 0
    return out
