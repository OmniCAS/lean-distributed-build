"""Build one shard: fetch the outputs it imports, run `lake build` on its modules, upload the results.

A worker owns a workspace directory that persists between jobs (its build directory and a list of
modules already present), so modules fetched or built once are not fetched again. The project
source must be at the same absolute path on every worker: Lean 4.33 stores the source path of
modules with linter messages in their .olean files.
"""
from __future__ import annotations

import json
import os
import re
import signal
import subprocess
import sys
import threading
import time

from .project import LakeProject, module_output_files
from .protocol import ModuleRecord, ShardJob, ShardResult
from .store import open_store

BUILT_RE = re.compile(r"\[\d+/\d+\] Built (\S+)(?: \(([\d.]+)(ms|s|min)\))?")


def _seconds(num: str | None, unit: str | None) -> float | None:
    if num is None:
        return None
    x = float(num)
    return x / 1000 if unit == "ms" else x * 60 if unit == "min" else x


def run_tracked(cmd: list[str], env: dict, timeout_s: float, cwd: str | None = None, on_start=None):
    """Run a command; return (exit code, output, wall s, cpu s, max RSS bytes, timed out).

    `on_start(proc)` is called once the process exists (e.g. to register it for cancellation; the
    process is the leader of its own process group)."""
    t0 = time.time()
    proc = subprocess.Popen(cmd, env=env, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            start_new_session=True)
    if on_start is not None:
        on_start(proc)
    chunks: list[bytes] = []
    reader = threading.Thread(target=lambda: chunks.append(proc.stdout.read()))
    reader.start()
    timed_out = [False]

    def kill():
        timed_out[0] = True
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass

    timer = threading.Timer(timeout_s, kill)
    timer.start()
    _pid, status, ru = os.wait4(proc.pid, 0)
    timer.cancel()
    reader.join()
    proc.returncode = os.waitstatus_to_exitcode(status)
    rss = ru.ru_maxrss if sys.platform == "darwin" else ru.ru_maxrss * 1024
    out = b"".join(chunks).decode("utf-8", errors="replace")
    return proc.returncode, out, time.time() - t0, ru.ru_utime + ru.ru_stime, rss, timed_out[0]


def lake_env(toolchain_bin: str, threads: int = 0) -> dict:
    env = dict(os.environ)
    env["PATH"] = toolchain_bin + os.pathsep + env.get("PATH", "/usr/bin:/bin")
    if threads:
        env["LEAN_NUM_THREADS"] = str(threads)
    env.pop("LEAN_PATH", None)
    return env


def run_shard(job: ShardJob, workspace: str, worker_id: str) -> ShardResult:
    t_start = time.time()
    res = ShardResult(job.job_id, job.shard_id, worker_id, ok=False)
    workspace = os.path.abspath(workspace)
    build_dir = os.path.join(workspace, "build")
    os.makedirs(build_dir, exist_ok=True)
    present_path = os.path.join(workspace, "present.json")
    present: dict[str, str] = {}
    if os.path.exists(present_path):
        with open(present_path, encoding="utf-8") as fh:
            present = json.load(fh)
    try:
        if job.fail_on_purpose:
            raise RuntimeError("failure requested by the job (test hook)")
        proj = LakeProject.load(job.project_dir)
        cfg = os.path.join(workspace, "lakefile.toml")
        with open(cfg, "w", encoding="utf-8") as fh:
            fh.write(proj.worker_lakefile(build_dir))
        store = open_store(job.store)

        # 1. fetch what the shard imports
        t = time.time()
        recs = store.get_records(job.needs)
        missing = [m for m in job.needs if m not in recs]
        if missing:
            raise RuntimeError(f"store has no outputs for {len(missing)} needed modules, e.g. {missing[:3]}")
        for m in job.needs:
            r = recs[m]
            if present.get(m) == r.digest():
                continue
            for f in r.files:
                store.get_file(f, os.path.join(build_dir, f.path))
                res.fetched_files += 1
                res.fetched_bytes += f.size
            present[m] = r.digest()
        res.fetch_s = time.time() - t

        # 2. build the shard's modules with stock Lake
        cmd = [os.path.join(job.toolchain_bin, "lake"), "-d", job.project_dir, "-f", cfg, "--no-ansi",
               "build"] + ["+" + m for m in job.modules]
        code, out, wall, cpu, rss, timed_out = run_tracked(cmd, lake_env(job.toolchain_bin, job.threads),
                                                         job.timeout_s, cwd=workspace)
        res.build_s, res.cpu_s, res.max_rss_bytes = wall, cpu, rss
        res.log_tail = out[-4000:]
        for mm in BUILT_RE.finditer(out):
            res.built_modules.append(mm.group(1))
            sec = _seconds(mm.group(2), mm.group(3))
            if sec is not None:
                res.module_seconds[mm.group(1)] = sec
        if timed_out:
            raise RuntimeError(f"lake build timed out after {job.timeout_s:.0f} s")
        if code != 0:
            raise RuntimeError(f"lake build exited with {code}")
        outside = sorted(set(res.built_modules) - set(job.modules))
        if outside:
            # Lake rebuilt modules that should have come from the store: their outputs did not match
            raise RuntimeError(f"lake rebuilt {len(outside)} modules outside the shard, e.g. {outside[:3]}")

        # 3. upload the shard's outputs
        t = time.time()
        for m in job.modules:
            files = []
            for rel in module_output_files(build_dir, m):
                ref = store.put_file(os.path.join(build_dir, rel))
                ref.path = rel
                files.append(ref)
                res.uploaded_files += 1
                res.uploaded_bytes += ref.size
            if not any(f.path.endswith(".olean") for f in files):
                raise RuntimeError(f"no .olean produced for {m}")
            rec = ModuleRecord(m, files, worker_id, job.shard_id)
            store.put_record(rec)
            res.records.append(rec)
            present[m] = rec.digest()
        res.upload_s = time.time() - t
        res.ok = True
    except Exception as e:  # noqa: BLE001 - reported to the coordinator
        res.error = f"{type(e).__name__}: {e}"
    finally:
        tmp = present_path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(present, fh)
        os.replace(tmp, present_path)
        res.wall_s = time.time() - t_start
    return res


def main_run(job_path: str, result_path: str, workspace: str, worker_id: str) -> int:
    with open(job_path, encoding="utf-8") as fh:
        job = ShardJob.from_dict(json.load(fh))
    res = run_shard(job, workspace, worker_id)
    from .protocol import dumps
    tmp = result_path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write(dumps(res))
    os.replace(tmp, result_path)
    return 0 if res.ok else 1
