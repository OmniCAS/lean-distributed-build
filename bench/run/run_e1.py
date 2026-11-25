"""Run one E1 configuration on a few machines over SSH and fetch its records.

  python3 -B bench/run/run_e1.py NAME --hosts-file bench/run/hosts.json --project wide|mid|narrow \
      --mode lake|tool --hosts worker-1[,worker-2,worker-3] --cores C \
      [--priority bl|fifo|structure] [--history REMOTE_PATH] [--assign REMOTE_PATH] [--fetch-delay S]

Machines are named by role in a hosts file (see hosts.example.json): the SSH alias to reach each,
its address on the fast network, and its Python. The coordinator and the artifact store run on
the first host listed in --hosts; each host runs one worker pinned to CPUs 32..31+C with
`nice -n 10`. Everything lives under the same absolute directory (`base`) on every machine, which
must already hold: `lakeshard/` (this repository's snapshot), `tc/<version>/bin` (the Lean
toolchain), `src/<project>` (the generated project), and a `token` file shared by all machines.

  mode lake: plain `lake build` on one machine (the reference run, A0);
  mode tool: the lakeshard coordinator + one worker per host (A1 = one host, B1 = three hosts).

Records land in bench/results/runs/NAME/ (meta.json + records.tgz).
Derived from the script used for the runs in bench/results/ (machine names replaced by roles).
"""
import argparse
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
LOCAL = os.path.join(os.path.dirname(HERE), "results", "runs")


def ssh(alias, cmd, check=True, timeout=600, tries=6):
    """Run a command over SSH; retry when the connection itself fails (exit 255)."""
    r = None
    for k in range(tries):
        try:
            r = subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=15", alias, cmd],
                               capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            r = None
        if r is not None and r.returncode != 255:
            break
        time.sleep(5 * (k + 1))
    if r is None:
        raise RuntimeError(f"{alias}: timed out: {cmd[:200]}")
    if check and r.returncode != 0:
        raise RuntimeError(f"{alias}: {cmd[:200]}\n{r.stdout[-1000:]}{r.stderr[-1000:]}")
    return r.stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--hosts-file", required=True)
    ap.add_argument("--project", required=True, help="directory name under BASE/src")
    ap.add_argument("--mode", choices=["lake", "tool"], required=True)
    ap.add_argument("--hosts", default="worker-1")
    ap.add_argument("--cores", required=True, help="cores per host: one number, or one per host (8,8,16)")
    ap.add_argument("--priority", default="bl")
    ap.add_argument("--history")
    ap.add_argument("--assign")
    ap.add_argument("--fetch-delay", type=float, default=0.0)
    ap.add_argument("--target", action="append", default=[])
    ap.add_argument("--hub-cpus", default="56-63", help="CPUs for the coordinator on the first host")
    a = ap.parse_args()
    cfg = json.load(open(a.hosts_file))
    B, port, tcb = cfg["base"], cfg.get("port", 18765), cfg["toolchain_bin"]
    H = cfg["hosts"]
    env = f"PYTHONPATH={B}/lakeshard/src PYTHONDONTWRITEBYTECODE=1 LAKESHARD_TOOLCHAIN_BIN={tcb}"
    hosts = a.hosts.split(",")
    hub = hosts[0]
    cores = [int(x) for x in a.cores.split(",")]
    cores = cores * len(hosts) if len(cores) == 1 else cores
    assert len(cores) == len(hosts)
    cpus = f"32-{31 + cores[0]}"
    pdir = f"src/{a.project}"
    run = f"{B}/runs/{a.name}"
    local = os.path.join(LOCAL, a.name)
    os.makedirs(local, exist_ok=True)
    tg = "".join(f" --target {t}" for t in a.target)

    def loads():
        return {h: ssh(H[h]["ssh"], "cat /proc/loadavg").split()[:3] for h in H}

    meta = {"name": a.name, "project": a.project, "mode": a.mode, "hosts": hosts, "cores": cores,
            "priority": a.priority, "history": a.history, "assign": a.assign, "fetch_delay_s": a.fetch_delay,
            "started": time.strftime("%Y-%m-%dT%H:%M:%S"), "load_before": loads()}
    for h in hosts:
        ssh(H[h]["ssh"], f"rm -rf {run} && mkdir -p {run}")
    t0 = time.time()
    hs, py, addr = H[hub]["ssh"], H[hub]["python"], H[hub]["addr"]
    if a.mode == "lake":
        out = ssh(hs, f"cd {B} && {env} taskset -c {cpus} nice -n 10 {py} -m lakeshard reference "
                      f"{pdir} --build-dir {run}/ref --threads {cores[0]}{tg}", timeout=6 * 3600)
        meta["result"] = json.loads(out)
        ssh(hs, f"cd {run} && tar -czf records.tgz ref.history.json ref.log")
    else:
        extra = (f" --history {a.history}" if a.history else "") + (f" --assign {a.assign}" if a.assign else "") + \
                (f" --fetch-delay {a.fetch_delay}" if a.fetch_delay else "")
        ssh(hs, f"cd {B} && (setsid nohup env {env} taskset -c {a.hub_cpus} nice -n 10 {py} -m lakeshard build "
                f"{pdir} --backend lean --work {run}/work --listen {addr}:{port} --advertise-host {addr} "
                f"--local-workers 0 --token-file {B}/token --priority {a.priority} --wait-timeout 14400{extra}{tg} "
                f"> {run}/coordinator.log 2>&1 &)")
        for _ in range(120):
            if ssh(hs, f"test -f {run}/work/coordinator.json && echo yes", check=False).strip() == "yes":
                break
            time.sleep(0.5)
        else:
            raise RuntimeError("coordinator did not start: " + ssh(hs, f"tail -5 {run}/coordinator.log", False))
        for i, h in enumerate(hosts, 1):
            c = cores[i - 1]
            ssh(H[h]["ssh"], f"cd {B} && (setsid nohup env {env} taskset -c 32-{31 + c} nice -n 10 {H[h]['python']} -m "
                             f"lakeshard worker serve --coordinator http://{addr}:{port} --id worker-{i} --slots {c} "
                             f"--threads 1 --workspace {run}/ws-{i} --token-file {B}/token > {run}/worker-{i}.log 2>&1 &)")
        while ssh(hs, f"test -f {run}/work/report.json && echo yes", check=False).strip() != "yes":
            time.sleep(10)
        time.sleep(3)
        meta["result"] = json.loads(ssh(hs, f"cat {run}/work/report.json"))
        ssh(hs, f"cd {run}/work && tar -czf ../records.tgz report.json modules.jsonl events.jsonl manifest.json")
    meta["elapsed_s"] = round(time.time() - t0, 1)
    meta["load_after"] = loads()
    subprocess.run(["scp", "-q", "-o", "BatchMode=yes", f"{hs}:{run}/records.tgz", local], check=True)
    with open(os.path.join(local, "meta.json"), "w") as fh:
        json.dump(meta, fh, indent=1)
    r = meta["result"]
    print(json.dumps({"name": a.name, "wall_s": r.get("wall_s"), "ok": r.get("ok"), "elapsed_s": meta["elapsed_s"]}))


if __name__ == "__main__":
    sys.exit(main())
