#!/usr/bin/env python3
"""Lay out Mathlib and its dependencies from GitHub source tarballs (codeload), without git
network access (git over HTTPS from the worker host is unusably slow and flaky).

Each dependency is unpacked at exactly the revision of Mathlib's lake-manifest.json into
.lake/packages/<name>, committed as a local snapshot (with `origin` set to the manifest URL), and
the manifest's `rev` is replaced by the snapshot commit, so Lake finds every package at the
manifest revision and never fetches. Sources are byte-identical to the upstream revisions.
The original manifest is kept as lake-manifest.upstream.json.

Usage: setup_tarballs.py ROOT TAG
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
import time

ROOT, TAG = sys.argv[1], sys.argv[2]
SRC = os.path.join(ROOT, "src")
ML = os.path.join(ROOT, "mathlib4")
LOG = os.path.join(ROOT, "logs", "sources.jsonl")
os.makedirs(SRC, exist_ok=True)
os.makedirs(os.path.dirname(LOG), exist_ok=True)


def fetch(url, dest):
    for i in range(8):
        r = subprocess.run(["curl", "-sSfL", "--max-time", "900", "-o", dest + ".part", url])
        if r.returncode == 0:
            os.replace(dest + ".part", dest)
            return
        time.sleep(10 * (i + 1))
    raise SystemExit(f"download failed: {url}")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def unpack(tgz, dest):
    tmp = dest + ".unpack"
    shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(tmp)
    with tarfile.open(tgz) as tf:
        tf.extractall(tmp)
    (top,) = os.listdir(tmp)
    shutil.rmtree(dest, ignore_errors=True)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    os.replace(os.path.join(tmp, top), dest)
    os.rmdir(tmp)


def git(cwd, *args):
    return subprocess.run(["git", "-c", "user.name=snapshot", "-c", "user.email=snapshot@localhost",
                           "-c", "init.defaultBranch=main", *args], cwd=cwd, check=True,
                          capture_output=True, text=True).stdout.strip()


log = open(LOG, "a")
tgz = os.path.join(SRC, f"mathlib4-{TAG}.tar.gz")
if not os.path.exists(tgz):
    fetch(f"https://codeload.github.com/leanprover-community/mathlib4/tar.gz/refs/tags/{TAG}", tgz)
if not os.path.exists(os.path.join(ML, "lakefile.lean")):
    unpack(tgz, ML)
log.write(json.dumps({"name": "mathlib", "rev": TAG, "sha256": sha256(tgz)}) + "\n")

man_path = os.path.join(ML, "lake-manifest.json")
up_path = os.path.join(ML, "lake-manifest.upstream.json")
if not os.path.exists(up_path):
    shutil.copy(man_path, up_path)
man = json.load(open(up_path))
for p in man["packages"]:
    if p["type"] != "git":
        continue
    url, rev, name = p["url"], p["rev"], p["name"]
    owner_repo = url.removeprefix("https://github.com/").removesuffix(".git")
    t = os.path.join(SRC, f"{name}-{rev}.tar.gz")
    if not os.path.exists(t):
        fetch(f"https://codeload.github.com/{owner_repo}/tar.gz/{rev}", t)
    dest = os.path.join(ML, ".lake", "packages", name)
    if not os.path.isdir(os.path.join(dest, ".git")):
        unpack(t, dest)
        git(dest, "init", "-q")
        git(dest, "add", "-A", "-f")
        git(dest, "commit", "-q", "-m", f"snapshot of {owner_repo}@{rev}")
        git(dest, "remote", "add", "origin", url)
    snap = git(dest, "rev-parse", "HEAD")
    log.write(json.dumps({"name": name, "url": url, "rev": rev, "sha256": sha256(t), "snapshot": snap}) + "\n")
    log.flush()
    p["rev"] = snap
json.dump(man, open(man_path, "w"), indent=2)
print("SOURCES_DONE")
