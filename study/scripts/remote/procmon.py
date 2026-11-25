#!/usr/bin/env python3
"""Sample /proc for `lean` processes whose command line contains MATCH.

One JSON line per finished process (exact start from /proc/<pid>/stat, end = last time seen,
user/system CPU seconds, peak thread count, peak RSS), plus a machine line every few seconds
(load average, busy fraction of all CPUs and of the CPUs this build is pinned to).

Usage: procmon.py MATCH OUT_DIR [--interval 0.2] [--cpus 16-31]
Stops when OUT_DIR/STOP exists.
"""
import json
import os
import sys
import time

CLK = os.sysconf("SC_CLK_TCK")


def btime():
    for line in open("/proc/stat"):
        if line.startswith("btime"):
            return int(line.split()[1])
    return 0


def cpu_times():
    d = {}
    for line in open("/proc/stat"):
        if line.startswith("cpu") and line[3] != " ":
            p = line.split()
            v = list(map(int, p[1:]))
            d[int(p[0][3:])] = (sum(v), v[3] + v[4])
    return d


def parse_cpus(s):
    out = set()
    for part in s.split(","):
        if "-" in part:
            a, b = part.split("-")
            out.update(range(int(a), int(b) + 1))
        elif part:
            out.add(int(part))
    return out


def read_stat(pid):
    with open(f"/proc/{pid}/stat") as fh:
        s = fh.read()
    rest = s[s.rindex(")") + 2:].split()
    # rest[0] is field 3 (state); utime=14, stime=15, num_threads=20, starttime=22
    return int(rest[11]), int(rest[12]), int(rest[17]), int(rest[19])


def read_hwm(pid):
    try:
        for line in open(f"/proc/{pid}/status"):
            if line.startswith("VmHWM"):
                return int(line.split()[1])
    except OSError:
        pass
    return 0


def main():
    match, out = sys.argv[1], sys.argv[2]
    interval = 0.2
    pinned = set()
    args = sys.argv[3:]
    while args:
        a = args.pop(0)
        if a == "--interval":
            interval = float(args.pop(0))
        elif a == "--cpus":
            pinned = parse_cpus(args.pop(0))
    bt = btime()
    procs = open(os.path.join(out, "procs.jsonl"), "a")
    mach = open(os.path.join(out, "machine.jsonl"), "a")
    seen = set()
    live = {}
    last_mach = 0.0
    prev_cpu = cpu_times()
    while not os.path.exists(os.path.join(out, "STOP")):
        now = time.time()
        try:
            pids = [int(p) for p in os.listdir("/proc") if p.isdigit()]
        except OSError:
            pids = []
        for pid in pids:
            if pid in seen:
                continue
            seen.add(pid)
            try:
                with open(f"/proc/{pid}/comm") as fh:
                    comm = fh.read().strip()
                if comm != "lean":
                    continue
                with open(f"/proc/{pid}/cmdline", "rb") as fh:
                    argv = fh.read().split(b"\0")
                argv = [x.decode("utf-8", "replace") for x in argv if x]
                if not any(match in x for x in argv):
                    continue
                ut, st, nth, start = read_stat(pid)
            except (OSError, ValueError, IndexError):
                continue
            src = next((x for x in argv if x.endswith(".lean")), "")
            live[pid] = {"pid": pid, "src": src, "argv": argv, "start": bt + start / CLK,
                         "first_seen": now, "last_seen": now, "utime": ut / CLK, "stime": st / CLK,
                         "max_threads": nth, "hwm_kb": 0, "samples": 0}
        for pid in list(live):
            r = live[pid]
            try:
                ut, st, nth, _ = read_stat(pid)
                r["utime"], r["stime"] = ut / CLK, st / CLK
                r["max_threads"] = max(r["max_threads"], nth)
                r["threads"] = nth
                r["last_seen"] = now
                r["samples"] += 1
                if r["samples"] % 5 == 1:
                    r["hwm_kb"] = max(r["hwm_kb"], read_hwm(pid))
            except (OSError, ValueError, IndexError):
                procs.write(json.dumps(r) + "\n")
                procs.flush()
                del live[pid]
        if now - last_mach >= 2.0:
            cur = cpu_times()
            busy_all = busy_pin = 0.0
            n_pin = 0
            for c, (tot, idle) in cur.items():
                if c not in prev_cpu:
                    continue
                dt = tot - prev_cpu[c][0]
                b = 1 - (idle - prev_cpu[c][1]) / dt if dt > 0 else 0.0
                busy_all += b
                if c in pinned:
                    busy_pin += b
                    n_pin += 1
            prev_cpu = cur
            la = open("/proc/loadavg").read().split()
            mach.write(json.dumps({"t": now, "load1": float(la[0]), "busy_cpus_all": round(busy_all, 2),
                                   "busy_cpus_pinned": round(busy_pin, 2), "n_pinned": n_pin,
                                   "live_lean": len(live),
                                   "live_threads": sum(r.get("threads", 1) for r in live.values()),
                                   "live_cpu_s": round(sum(r["utime"] + r["stime"] for r in live.values()), 1)}) + "\n")
            mach.flush()
            last_mach = now
        time.sleep(interval)
    for r in live.values():
        procs.write(json.dumps(r) + "\n")
    procs.close()
    mach.close()


if __name__ == "__main__":
    main()
