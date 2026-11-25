"""Control experiment (distcc-style): stock Lake schedules, only its `lean` processes run elsewhere.

    lakeshard forward serve --listen HOST:PORT --token-file F --log jobs.jsonl
    lakeshard forward agent --hub http://HOST:PORT --id NAME --slots 16 --token-file F
    lakeshard forward sysroot --dir D --hub http://HOST:PORT --token-file F    # then:
    LAKE_OVERRIDE_LEAN=true LEAN_SYSROOT=D LEAN_NUM_THREADS=<all slots> lake build ...

Lake finds `lean` in `LEAN_SYSROOT` (with `LAKE_OVERRIDE_LEAN=true`); there `bin/lean` is a shim
that posts every compile command (`<src> -o … -i … -c … --setup … --json`, with its `LEAN_PATH`) to
the hub and blocks until an agent has run it; other invocations go to the real `lean`. Agents
pull commands (so no machine has to accept connections), wait until the import files named in
the setup file are visible (the build directory is on a file system all machines share, e.g.
NFS), run the real `lean` with one thread, and return output and exit code. Afterwards the shim
waits until the outputs are visible on the machine where Lake runs. The project source must be
at the same path everywhere. Lake's own job pool (`LEAN_NUM_THREADS`) bounds the commands in flight;
the order is Lake's (whatever becomes ready first).
"""
from __future__ import annotations

import itertools
import json
import os
import socket
import stat
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .direct import wait_visible
from .httpstore import _send_json, authorized

SHIM = os.path.join(os.path.dirname(os.path.abspath(__file__)), "forwardshim.py")


class Forwarder:
    def __init__(self, log_path: str | None = None):
        self.cond = threading.Condition()
        self.pending: list[dict] = []
        self.results: dict[str, dict] = {}
        self.seq = itertools.count(1)
        self.t0 = time.time()
        self.log = open(log_path, "a", encoding="utf-8") if log_path else None
        self.agents: dict[str, dict] = {}

    def exec(self, req: dict, timeout_s: float = 6 * 3600) -> dict:
        jid = f"j{next(self.seq):07d}"
        job = {"job_id": jid, "argv": req["argv"], "env": req.get("env", {}), "cwd": req.get("cwd"),
               "submitted": time.time()}
        with self.cond:
            self.pending.append(job)
            self.cond.notify_all()
            deadline = time.time() + timeout_s
            while jid not in self.results:
                if not self.cond.wait(timeout=max(0.1, deadline - time.time())) and time.time() > deadline:
                    return {"code": 124, "out": "", "err": "forward: timed out"}
            res = self.results.pop(jid)
        if self.log:
            rec = {"job_id": jid, "module": res.get("module"), "agent": res.get("agent"),
                   "submit_t": round(job["submitted"] - self.t0, 3), "start_t": round(res["started"] - self.t0, 3),
                   "end_t": round(res["ended"] - self.t0, 3), "wait_s": res.get("wait_s"), "lean_s": res.get("lean_s"),
                   "code": res["code"]}
            with self.cond:
                self.log.write(json.dumps(rec) + "\n")
                self.log.flush()
        return res

    def take(self, agent: str, n: int, wait_s: float) -> list[dict]:
        deadline = time.time() + wait_s
        with self.cond:
            self.agents.setdefault(agent, {"taken": 0})
            while not self.pending and time.time() < deadline:
                self.cond.wait(timeout=deadline - time.time())
            out, self.pending = self.pending[:n], self.pending[n:]
            self.agents[agent]["taken"] += len(out)
            return out

    def done(self, res: dict) -> None:
        with self.cond:
            self.results[res["job_id"]] = res
            self.cond.notify_all()


def serve(listen: str, token: str | None, log_path: str | None):
    fw = Forwarder(log_path)
    host, _, port = listen.rpartition(":")

    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, *a):
            pass

        def do_POST(self):
            if not authorized(self, token):
                return _send_json(self, 401, {"error": "unauthorized"})
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)) or b"{}")
            if self.path == "/v1/exec":
                return _send_json(self, 200, fw.exec(body))
            if self.path == "/v1/take":
                return _send_json(self, 200, {"jobs": fw.take(body["agent"], int(body.get("n", 1)),
                                                              float(body.get("wait_s", 20)))})
            if self.path == "/v1/done":
                fw.done(body)
                return _send_json(self, 200, {"ok": True})
            return _send_json(self, 404, {"error": "not found"})

    srv = ThreadingHTTPServer((host or "127.0.0.1", int(port or 0)), Handler)
    srv.daemon_threads = True
    srv.forwarder = fw
    return srv


def _post(url: str, path: str, body: dict, token: str | None, timeout: float) -> dict:
    import urllib.request
    req = urllib.request.Request(url.rstrip("/") + path, data=json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json"})
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def _setup_paths(argv: list[str]) -> tuple[str, list[str]]:
    """Module name and the import artifact paths named by the command's setup file."""
    try:
        with open(argv[argv.index("--setup") + 1], encoding="utf-8") as fh:
            setup = json.load(fh)
    except (ValueError, OSError):
        return "", []
    paths = [p for arts in setup.get("importArts", {}).values() for part in arts for p in part]
    return setup.get("name", ""), paths


def agent(hub: str, agent_id: str, slots: int, lean: str, token: str | None, visibility_timeout_s: float = 120.0):
    sem = threading.Semaphore(slots)

    def run(job: dict) -> None:
        try:
            t0 = time.time()
            module, imports = _setup_paths(job["argv"])
            missing, waited = wait_visible(imports, visibility_timeout_s, 0.5) if imports else ([], 0.0)
            env = dict(os.environ)
            env.update(job.get("env", {}))
            env["LEAN_NUM_THREADS"] = "1"
            t1 = time.time()
            if missing:
                code, out, err = 1, "", f"forward agent {agent_id}: {len(missing)} imports not visible, e.g. {missing[0]}"
            else:
                r = subprocess.run([lean] + job["argv"][1:], env=env, cwd=job.get("cwd") or None,
                                   capture_output=True, text=True)
                code, out, err = r.returncode, r.stdout, r.stderr
            t2 = time.time()
            _post(hub, "/v1/done", {"job_id": job["job_id"], "code": code, "out": out, "err": err, "agent": agent_id,
                                    "module": module, "started": t0, "ended": t2, "wait_s": round(waited, 3),
                                    "lean_s": round(t2 - t1, 3)}, token, 120)
        finally:
            sem.release()

    while True:
        sem.acquire()
        try:
            jobs = _post(hub, "/v1/take", {"agent": agent_id, "n": 1, "wait_s": 20}, token, 80).get("jobs", [])
        except OSError:
            sem.release()
            time.sleep(2)
            continue
        if not jobs:
            sem.release()
            continue
        threading.Thread(target=run, args=(jobs[0],), daemon=True).start()


def make_sysroot(d: str, toolchain_bin: str, hub: str, token_file: str | None, python: str = sys.executable) -> str:
    """Like the seal's stand-in toolchain: links to the real one, `bin/lean` = the forwarding shim."""
    real_root = os.path.dirname(os.path.abspath(toolchain_bin))
    d = os.path.abspath(d)
    os.makedirs(os.path.join(d, "bin"), exist_ok=True)
    for e in os.listdir(real_root):
        if e != "bin" and not os.path.lexists(os.path.join(d, e)):
            os.symlink(os.path.join(real_root, e), os.path.join(d, e))
    for e in os.listdir(toolchain_bin):
        if e != "lean" and not os.path.lexists(os.path.join(d, "bin", e)):
            os.symlink(os.path.join(toolchain_bin, e), os.path.join(d, "bin", e))
    lean = os.path.join(d, "bin", "lean")
    with open(lean, "w") as fh:
        fh.write(f"#!/bin/sh\nexport LAKESHARD_FORWARD_HUB='{hub}' LAKESHARD_REAL_LEAN='{toolchain_bin}/lean'"
                 f" LAKESHARD_FORWARD_TOKEN_FILE='{token_file or ''}'\nexec '{python}' -I '{SHIM}' \"$@\"\n")
    os.chmod(lean, os.stat(lean).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return d


def main(argv: list[str]) -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="lakeshard forward")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("serve")
    s.add_argument("--listen", required=True)
    s.add_argument("--token-file")
    s.add_argument("--log")
    a = sub.add_parser("agent")
    a.add_argument("--hub", required=True)
    a.add_argument("--id", default=socket.gethostname())
    a.add_argument("--slots", type=int, default=1)
    a.add_argument("--lean", required=True, help="the real lean executable on this machine")
    a.add_argument("--token-file")
    r = sub.add_parser("sysroot")
    r.add_argument("--dir", required=True)
    r.add_argument("--toolchain-bin", required=True)
    r.add_argument("--hub", required=True)
    r.add_argument("--token-file")
    args = ap.parse_args(argv)
    tok = open(args.token_file).read().strip() if getattr(args, "token_file", None) else None
    if args.cmd == "serve":
        srv = serve(args.listen, tok, args.log)
        print(json.dumps({"listen": f"{srv.server_address[0]}:{srv.server_address[1]}"}), flush=True)
        srv.serve_forever()
    elif args.cmd == "agent":
        agent(args.hub, args.id, args.slots, args.lean, tok)
    else:
        print(make_sysroot(args.dir, args.toolchain_bin, args.hub, args.token_file))
    return 0
