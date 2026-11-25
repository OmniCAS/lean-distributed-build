"""Stand-in for `lean` in the forwarding experiment (see `forward.py`). Standard library only.

A compile command goes to the hub and is run by an agent on some machine; then the shim waits
until the outputs are visible here (the build directory is shared, e.g. over NFS, and a client
may still hold a stale view of a directory), prints the output and exits with the exit code.
Everything else (`--githash`, `--print-prefix`, ...) runs the real `lean` here.
"""
import json
import os
import sys
import time
import urllib.request


def main(argv):
    real = os.environ["LAKESHARD_REAL_LEAN"]
    if "--setup" not in argv or "-o" not in argv:
        os.execv(real, [real] + argv)
    tok_file = os.environ.get("LAKESHARD_FORWARD_TOKEN_FILE")
    token = open(tok_file).read().strip() if tok_file else None
    body = {"argv": [real] + argv, "cwd": os.getcwd(), "env": {"LEAN_PATH": os.environ.get("LEAN_PATH", "")}}
    req = urllib.request.Request(os.environ["LAKESHARD_FORWARD_HUB"].rstrip("/") + "/v1/exec",
                                 data=json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json"})
    if token:
        req.add_header("Authorization", "Bearer " + token)
    with urllib.request.urlopen(req, timeout=6 * 3600) as r:
        res = json.loads(r.read())
    if res.get("code") == 0:
        outs = [argv[argv.index(f) + 1] for f in ("-o", "-i", "-c") if f in argv]
        t0 = time.time()
        while time.time() - t0 < 120:
            missing = [p for p in outs if not os.path.exists(p)]
            if not missing:
                break
            for d in {os.path.dirname(p) for p in missing}:
                try:
                    os.listdir(d)  # revalidate this client's view of the directory (NFS)
                except OSError:
                    pass
            time.sleep(0.5)
    sys.stdout.write(res.get("out", ""))
    sys.stderr.write(res.get("err", ""))
    return int(res.get("code", 1))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
