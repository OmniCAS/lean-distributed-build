#!/usr/bin/env python3
"""Import graph of a Lake workspace from import headers only (nothing is run).

Every `*.lean` file of the root package and of `.lake/packages/*` becomes a module named after
its path (srcDir is the package root for Mathlib and all its dependencies). Writes JSON
{module: {pkg, path, imports, lines, bytes, is_module}} and, if a build directory exists,
artifact sizes per module and extension.

Usage: graph_remote.py WORKSPACE OUT.json
"""
import json
import os
import re
import sys

IMPORT_RE = re.compile(r"^(?:(public)\s+|private\s+)?(?:(meta)\s+)?import\s+(?:(all)\s+)?(.+)$")


def parse_header(text):
    is_module, imports, depth = False, [], 0
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
        if word == "module":
            is_module = True
            continue
        if word == "prelude":
            continue
        m = IMPORT_RE.match(s)
        if m:
            body = m.group(4).split("--")[0].split("/-")[0]
            imports.extend(body.split())
            continue
        break
    return is_module, imports


def scan(pkg, root, out):
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if not d.startswith(".")]
        for f in fn:
            if not f.endswith(".lean") or f == "lakefile.lean":
                continue
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, root)
            mod = rel[:-5].replace(os.sep, ".")
            data = open(p, "rb").read()
            text = data.decode("utf-8", "replace")
            is_mod, imps = parse_header(text)
            out.setdefault(mod, {"pkg": pkg, "path": os.path.relpath(p, WS), "imports": imps,
                                 "lines": text.count("\n"), "bytes": len(data), "is_module": is_mod})


def sizes(build, out):
    lib = os.path.join(build, "lib", "lean")
    ir = os.path.join(build, "ir")
    for base, exts in ((lib, (".olean", ".olean.server", ".olean.private", ".ilean", ".trace", ".hash")),
                       (ir, (".c", ".setup.json"))):
        for dp, _, fn in os.walk(base):
            for f in fn:
                for e in exts:
                    if f.endswith(e):
                        mod = os.path.relpath(os.path.join(dp, f[: -len(e)]), base).replace(os.sep, ".")
                        if mod in out:
                            out[mod].setdefault("sizes", {})
                            out[mod]["sizes"][e] = out[mod]["sizes"].get(e, 0) + os.path.getsize(os.path.join(dp, f))
                        break


WS = os.path.abspath(sys.argv[1])
res = {}
scan("mathlib", WS, res)
pk = os.path.join(WS, ".lake", "packages")
for name in sorted(os.listdir(pk)) if os.path.isdir(pk) else []:
    scan(name, os.path.join(pk, name), res)
    b = os.path.join(pk, name, ".lake", "build")
    if os.path.isdir(b):
        sizes(b, res)
if os.path.isdir(os.path.join(WS, ".lake", "build")):
    sizes(os.path.join(WS, ".lake", "build"), res)
json.dump(res, open(sys.argv[2], "w"))
print(len(res), "files")
