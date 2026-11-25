"""Stand-in for `lean` while stock Lake seals a build (see `seal.py`). Standard library only: it is
run by path with `python -I`, without the lakeshard package on the path.

When Lake asks it to compile a module (`<src> -o X.olean -i X.ilean [-c X.c] --setup S --json`),
it copies that module's outputs from the artifact store (a store directory) into the requested
paths (`.olean.server`, `.olean.private`, `.ir.sig`, `.ir` next to the `.olean`, as Lean names
them), checking each sha256, and exits 0. Lake then hashes the outputs and writes its own trace
files, exactly as after a real compilation. A module without outputs in the store, and every
other invocation (`--githash`, `--version`, ...), goes to the real `lean`.

Environment: LAKESHARD_REAL_LEAN (the real executable), LAKESHARD_SEAL_STORE (store directory),
LAKESHARD_SEAL_MANIFEST (optional: build manifest, records by input key instead of module name),
LAKESHARD_SEAL_LOG (optional: one line per module, "store" or "lean").
"""
import hashlib
import json
import os
import shutil
import sys


def _real(argv):
    real = os.environ["LAKESHARD_REAL_LEAN"]
    os.execv(real, [real] + argv)


def _log(module, how):
    p = os.environ.get("LAKESHARD_SEAL_LOG")
    if p:
        with open(p, "a") as fh:  # small appends are atomic enough for one line per module
            fh.write(f"{how} {module}\n")


def main(argv):
    if "--setup" not in argv or "-o" not in argv or "-i" not in argv:
        return _real(argv)
    with open(argv[argv.index("--setup") + 1], encoding="utf-8") as fh:
        module = json.load(fh)["name"]
    store = os.environ["LAKESHARD_SEAL_STORE"]
    ident = module
    if os.environ.get("LAKESHARD_SEAL_MANIFEST"):
        with open(os.environ["LAKESHARD_SEAL_MANIFEST"], encoding="utf-8") as fh:
            ident = json.load(fh)["modules"].get(module)
        if ident is None:
            _log(module, "lean")
            return _real(argv)
    h = hashlib.sha1(ident.encode("utf-8")).hexdigest()
    rec_path = os.path.join(store, "records", h[:2], h + ".json")
    if not os.path.exists(rec_path):
        _log(module, "lean")
        return _real(argv)
    with open(rec_path, encoding="utf-8") as fh:
        rec = json.load(fh)
    olean = argv[argv.index("-o") + 1]
    base = olean[: -len(".olean")]
    dest = {".olean": olean, ".ilean": argv[argv.index("-i") + 1], ".olean.server": olean + ".server",
            ".olean.private": olean + ".private", ".ir.sig": base + ".ir.sig", ".ir": base + ".ir"}
    if "-c" in argv:
        dest[".c"] = argv[argv.index("-c") + 1]
    for f in rec["files"]:
        suf = next((s for s in (".olean.server", ".olean.private", ".olean", ".ilean", ".ir.sig", ".ir", ".c")
                    if f["path"].endswith(s)), None)
        if suf is None or suf not in dest:
            continue
        src = os.path.join(store, "objects", f["sha256"][:2], f["sha256"])
        out = dest[suf]
        os.makedirs(os.path.dirname(out), exist_ok=True)
        tmp = out + f".tmp{os.getpid()}"
        shutil.copyfile(src, tmp)
        d = hashlib.sha256()
        with open(tmp, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                d.update(chunk)
        if d.hexdigest() != f["sha256"]:
            os.remove(tmp)
            sys.stderr.write(f"lakeshard seal: hash mismatch for {module} {suf}\n")
            return 1
        os.replace(tmp, out)
    _log(module, "store")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
