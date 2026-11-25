#!/usr/bin/env python3
"""Replay Lake's recorded `lean` command for given modules with different thread counts.

The command (LEAN_PATH + argv) is taken verbatim from the module's `.trace` log; only the output
paths (-o/-i/-c) are redirected to a scratch directory, and `-j k` / LEAN_NUM_THREADS=k are set.
Runs of one module with the different k are started together on disjoint pinned CPU sets
(k=1: 1 CPU, k=2: 2 CPUs, ...), so a module's curve is measured under the same conditions.
Writes one JSON line per run: wall, user/sys CPU, peak RSS, exit code, whether the produced
.olean equals the build's.

Usage: replay.py WORKSPACE OUT.jsonl SCRATCH "1:16 2:17-18 4:19-22 8:23-30" MODULE...
"""
import hashlib
import json
import os
import shlex
import subprocess
import sys
import time

WS, OUT, SCRATCH, SPEC = sys.argv[1:5]
MODS = sys.argv[5:]
SLOTS = [(int(a), b) for a, b in (x.split(":") for x in SPEC.split())]
BUILD = os.path.join(WS, ".lake", "build")


def command(mod):
    rel = mod.replace(".", "/")
    # the module may live in a dependency's build directory
    cands = [os.path.join(BUILD, "lib", "lean", rel + ".trace")]
    pk = os.path.join(WS, ".lake", "packages")
    for p in os.listdir(pk):
        cands.append(os.path.join(pk, p, ".lake", "build", "lib", "lean", rel + ".trace"))
    for tr in cands:
        if os.path.exists(tr):
            d = json.load(open(tr))
            for e in d.get("log", []):
                msg = e.get("message", "")
                if msg.startswith(".> "):
                    words = shlex.split(msg[3:])
                    env = {}
                    while words and "=" in words[0] and not words[0].startswith("/"):
                        k, v = words.pop(0).split("=", 1)
                        env[k] = v
                    return env, words, tr
    raise SystemExit(f"no recorded command for {mod}")


def sha(p):
    try:
        return hashlib.sha256(open(p, "rb").read()).hexdigest()
    except OSError:
        return None


out = open(OUT, "a")
for mod in MODS:
    env0, argv, tr = command(mod)
    procs = []
    for k, cpus in SLOTS:
        d = os.path.join(SCRATCH, f"j{k}")
        os.makedirs(d, exist_ok=True)
        a = list(argv)
        outs = {}
        for flag in ("-o", "-i", "-c"):
            i = a.index(flag)
            outs[flag] = a[i + 1]
            a[i + 1] = os.path.join(d, os.path.basename(a[i + 1]))
        a = ["taskset", "-c", cpus, "nice", "-n", "10"] + a[:1] + ["-j", str(k)] + a[1:]
        env = dict(os.environ)
        env.update(env0)
        env["LEAN_NUM_THREADS"] = str(k)
        t0 = time.perf_counter()
        p = subprocess.Popen(a, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        procs.append((k, cpus, p, t0, outs, a))
    pending = {p.pid: (k, cpus, p, t0, outs, a) for k, cpus, p, t0, outs, a in procs}
    while pending:
        pid, status, ru = os.wait4(-1, 0)
        if pid not in pending:
            continue
        k, cpus, p, t0, outs, a = pending.pop(pid)
        p.returncode = os.waitstatus_to_exitcode(status)
        wall = time.perf_counter() - t0
        new_olean = a[a.index("-o") + 1]
        rec = {"module": mod, "k": k, "cpus": cpus, "wall_s": round(wall, 3), "user_s": ru.ru_utime,
               "sys_s": ru.ru_stime, "max_rss_kb": ru.ru_maxrss, "exit": os.waitstatus_to_exitcode(status),
               "olean_same": sha(new_olean) == sha(outs["-o"]), "t": time.time()}
        out.write(json.dumps(rec) + "\n")
        out.flush()
        for f in os.listdir(os.path.dirname(new_olean)):
            os.remove(os.path.join(os.path.dirname(new_olean), f))
print("REPLAY_DONE")
