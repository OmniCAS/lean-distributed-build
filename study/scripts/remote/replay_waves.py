#!/usr/bin/env python3
"""Run Lake's recorded `lean` commands for MODULES, 16 at a time on CPUS, in one of three modes:
  shared16  all processes share CPUS, LEAN_NUM_THREADS=16 / -j 16 (what `lake build` does)
  shared1   all processes share CPUS, 1 thread each
  pinned1   each process pinned to its own CPU, 1 thread each
Outputs go to a scratch directory. One JSON line per module + one summary line per mode.
Usage: replay_waves.py WORKSPACE OUT.jsonl SCRATCH CPUS MODE MODULE...
"""
import json
import os
import subprocess
import sys
import time

WS, OUT, SCRATCH, CPUS, MODE = sys.argv[1:6]
MODS = sys.argv[6:]
a, b = map(int, CPUS.split("-"))
cpus = list(range(a, b + 1))
W = len(cpus)

BUILD = os.path.join(WS, ".lake", "build")


def command(mod):
    """Lake's recorded command (env + argv) from the module's .trace log (same as replay.py)."""
    import shlex
    rel = mod.replace(".", "/")
    cands = [os.path.join(BUILD, "lib", "lean", rel + ".trace")]
    pk = os.path.join(WS, ".lake", "packages")
    for p in os.listdir(pk):
        cands.append(os.path.join(pk, p, ".lake", "build", "lib", "lean", rel + ".trace"))
    for tr in cands:
        if os.path.exists(tr):
            for e in json.load(open(tr)).get("log", []):
                msg = e.get("message", "")
                if msg.startswith(".> "):
                    words = shlex.split(msg[3:])
                    env = {}
                    while words and "=" in words[0] and not words[0].startswith("/"):
                        k, v = words.pop(0).split("=", 1)
                        env[k] = v
                    return env, words, tr
    raise SystemExit(f"no recorded command for {mod}")


def launch(mod, slot):
    env0, argv, _ = command(mod)
    d = os.path.join(SCRATCH, MODE, str(slot))
    os.makedirs(d, exist_ok=True)
    x = list(argv)
    for flag in ("-o", "-i", "-c"):
        i = x.index(flag)
        x[i + 1] = os.path.join(d, os.path.basename(x[i + 1]))
    k = 16 if MODE == "shared16" else 1
    pin = str(cpus[slot]) if MODE == "pinned1" else CPUS
    cmd = ["taskset", "-c", pin, "nice", "-n", "10"] + x[:1] + ["-j", str(k)] + x[1:]
    env = dict(os.environ)
    env.update(env0)
    env["LEAN_NUM_THREADS"] = str(k)
    return subprocess.Popen(cmd, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


out = open(OUT, "a")
t_all = time.perf_counter()
queue = list(MODS)
running = {}
free = list(range(W))
while queue or running:
    while queue and free:
        slot = free.pop()
        mod = queue.pop(0)
        p = launch(mod, slot)
        running[p.pid] = (mod, slot, time.perf_counter())
    pid, status, ru = os.wait4(-1, 0)
    if pid not in running:
        continue
    mod, slot, t0 = running.pop(pid)
    free.append(slot)
    out.write(json.dumps({"mode": MODE, "module": mod, "wall_s": round(time.perf_counter() - t0, 3),
                          "cpu_s": ru.ru_utime + ru.ru_stime, "exit": os.waitstatus_to_exitcode(status)}) + "\n")
    out.flush()
out.write(json.dumps({"mode": MODE, "summary": True, "total_wall_s": round(time.perf_counter() - t_all, 2),
                      "modules": len(MODS)}) + "\n")
print("WAVES_DONE", MODE)
