"""Build one module by calling `lean` directly, exactly as Lake would (see `lakeenv`).

Two storage modes:

- `shared`: all workers read and write one build directory (on NFS when the workers are separate
  machines). Lean writes into a private temporary directory inside the build directory; the
  outputs are then renamed into place, the `.olean` last, so whoever sees a module's `.olean` sees
  all its outputs (`rename` within one file system is atomic, also on NFS). Lake's metadata for the
  module (`.trace`, `*.hash`) is removed, so a later `lake build` cannot trust stale hashes.
  Before running `lean`, the worker checks that the outputs of the module's direct imports are
  visible; with `visibility_timeout_s > 0` it re-reads their directories (which makes an NFS
  client revalidate its cache) and waits up to that long.
- `store`: each worker builds into its own directory and exchanges outputs through the
  content-addressed store (as the Lake batch backend does); kept as the control.

The direct backend writes no Lake `.trace`/`.hash` files: Lake cannot yet reuse its outputs as up to
date (that is milestone M3).
"""
from __future__ import annotations

import json
import os
import shutil
import signal
import socket
import threading
import time

from .lakeenv import LakeWorkspace
from .project import LakeProject, module_rel
from .protocol import BuildConfig, FileRef, ModuleRecord, ModuleResult, ModuleTask
from .store import IntegrityError, open_store, sha256_file
from .worker import run_tracked

LAKE_META_SUFFIXES = (".trace", ".olean.hash", ".olean.server.hash", ".olean.private.hash", ".ilean.hash",
                      ".ir.sig.hash", ".ir.hash", ".c.hash", ".ltar")
ALL_OUTPUT_SUFFIXES = (".olean.server", ".olean.private", ".ir.sig", ".ir", ".ilean", ".c", ".olean")


def wait_visible(paths: list[str], timeout_s: float, poll_s: float = 0.5,
                 sizes: dict[str, int] | None = None) -> tuple[list[str], float]:
    """Wait until every path exists (with the given size, if any). Returns (still missing, seconds)."""
    t0 = time.time()

    def missing_now(ps):
        out = []
        for p in ps:
            try:
                st = os.stat(p)
            except FileNotFoundError:
                out.append(p)
                continue
            if sizes and p in sizes and st.st_size != sizes[p]:
                out.append(p)
        return out

    missing = missing_now(paths)
    while missing and time.time() - t0 < timeout_s:
        time.sleep(poll_s)
        for d in {os.path.dirname(p) for p in missing}:
            try:
                os.listdir(d)  # NFS: reading the directory revalidates the client's cached entries
            except OSError:
                pass
        missing = missing_now(missing)
    return missing, time.time() - t0


class ModuleBuilder:
    """Worker side of the direct backend; one per worker process, used by several slots at once."""

    def __init__(self, cfg: BuildConfig, worker_id: str, workspace: str, default_threads: int = 0,
                 token: str | None = None):
        self.cfg, self.worker_id, self.default_threads = cfg, worker_id, default_threads
        self.host = socket.gethostname()
        self.workspace = os.path.abspath(workspace)
        proj = load_worker_project(cfg, self.workspace)
        if cfg.storage == "shared":
            if not cfg.build_dir:
                raise ValueError("storage=shared needs a build directory")
            self.build_dir = os.path.abspath(cfg.build_dir)
        elif cfg.storage == "store":
            self.build_dir = os.path.join(self.workspace, "build")
        else:
            raise ValueError(f"unknown storage {cfg.storage!r}")
        os.makedirs(self.build_dir, exist_ok=True)
        self.ws = LakeWorkspace(proj, self.build_dir, cfg.toolchain_bin)
        self.ws.check_supported()
        self.store = open_store(cfg.store, token=token) if cfg.storage == "store" else None
        self.present: dict[str, str] = {}  # storage=store: key (or name) -> module, for outputs present here
        self.lock = threading.Lock()
        self.procs: dict[str, object] = {}
        self.cancelled: set[str] = set()
        self.tmp_root = os.path.join(self.build_dir, ".lakeshard-tmp")

    # --- cancellation (the coordinator gave the task to someone else)

    def cancel(self, task_id: str) -> None:
        with self.lock:
            self.cancelled.add(task_id)
            p = self.procs.get(task_id)
        if p is not None:
            try:
                os.killpg(p.pid, signal.SIGKILL)
            except (ProcessLookupError, PermissionError):
                pass

    # --- one task

    def build(self, task: ModuleTask) -> ModuleResult:
        t0 = time.time()
        threads = task.threads or self.default_threads
        res = ModuleResult(task.task_id, task.module, self.worker_id, ok=False, attempt=task.attempt,
                           started=t0, threads=threads, host=self.host)
        tmp = os.path.join(self.tmp_root, f"{self.cfg.run_id}-{task.task_id}-{os.getpid()}")
        try:
            if task.fail_on_purpose:
                raise RuntimeError("failure requested by the task (test hook)")
            m = task.module
            setup = self.ws.setup(m)
            if self.store is not None:
                self._fetch(task, res)
            else:
                self._wait_imports(m, setup["importArts"], res)
            final = self.ws.outputs(m)
            rel = {k: os.path.relpath(v, self.build_dir) for k, v in final.items()}
            outs = {k: os.path.join(tmp, r) for k, r in rel.items()}
            for p in outs.values():
                os.makedirs(os.path.dirname(p), exist_ok=True)
            setup_path = os.path.join(tmp, "ir", module_rel(m) + ".setup.json")
            with open(setup_path, "w", encoding="utf-8") as fh:
                json.dump(setup, fh)
            env = dict(os.environ)
            env.pop("LEAN_PATH", None)
            env["LEAN_PATH"] = self.ws.lean_path_str()
            if threads:
                env["LEAN_NUM_THREADS"] = str(threads)

            def started(proc, tid=task.task_id):
                with self.lock:
                    self.procs[tid] = proc
                    if tid in self.cancelled:
                        os.killpg(proc.pid, signal.SIGKILL)

            res.lean_start = time.time()
            code, out, wall, cpu, rss, timed_out = run_tracked(self.ws.lean_command(m, outs, setup_path), env,
                                                             task.timeout_s, on_start=started)
            res.lean_end = time.time()
            res.lean_s, res.cpu_s, res.max_rss_bytes, res.exit_code = wall, cpu, rss, code
            res.log_tail = out[-4000:]
            if code == 0 and self.ws.postpone_compile(m):
                code, out2, wall, cpu, rss, timed_out = run_tracked(self.ws.leanir_command(outs, setup_path), env,
                                                                  task.timeout_s, on_start=started)
                res.lean_s += wall
                res.cpu_s += cpu
                res.max_rss_bytes = max(res.max_rss_bytes, rss)
                res.exit_code = code
                res.log_tail = (out + out2)[-4000:]
                res.lean_end = time.time()
            with self.lock:
                self.procs.pop(task.task_id, None)
                was_cancelled = task.task_id in self.cancelled
            if was_cancelled:
                raise RuntimeError("cancelled by the coordinator")
            if timed_out:
                raise RuntimeError(f"lean timed out after {task.timeout_s:.0f} s")
            if code != 0:
                raise RuntimeError(f"lean exited with {code}: {_first_error(out)}")
            if self.cfg.keep_setup:
                outs[".setup.json"] = setup_path
                final[".setup.json"] = os.path.join(self.build_dir, "ir", module_rel(m) + ".setup.json")
            self._publish(m, outs, final, res, task.key)
            res.ok = True
        except Exception as e:  # noqa: BLE001 - reported to the coordinator
            res.error = f"{type(e).__name__}: {e}"
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
            res.ended = time.time()
            res.wall_s = res.ended - t0
        return res

    def _wait_imports(self, m: str, import_arts: dict, res: ModuleResult) -> None:
        """The outputs of the direct project imports must be visible here before `lean` starts."""
        paths = []
        for imp in self.ws.header(m).imports:
            loc = self.ws.locate(imp.module)
            if loc is not None and loc.is_root:
                paths.extend(p for part in import_arts.get(imp.module) or [] for p in part)
        missing, waited = wait_visible(sorted(set(paths)), self.cfg.visibility_timeout_s, self.cfg.visibility_poll_s)
        res.wait_s = waited
        if missing:
            raise RuntimeError(f"{len(missing)} imported outputs not visible after {waited:.1f} s, e.g. {missing[0]}")

    def _fetch(self, task: ModuleTask, res: ModuleResult) -> None:
        """Bring the outputs of the module's import closure into this worker's build directory.

        Modules already here (built or fetched earlier in this run) are not asked for again: within
        a run a module's outputs do not change (a rebuilt module has the same bytes)."""
        t = time.time()
        with self.lock:
            want = [u for u in task.needs if u not in self.present]
        recs = self.store.get_records(want) if want else {}
        missing = [u for u in want if u not in recs]
        if missing:
            raise RuntimeError(f"store has no outputs for {len(missing)} needed modules, e.g. {missing[:3]}")
        for u in want:
            r = recs[u]
            with self.lock:
                if u in self.present:
                    continue
            try:
                for f in r.files:
                    self.store.get_file(f, os.path.join(self.build_dir, f.path))
                    res.fetched_bytes += f.size
                    res.fetched_files += 1
            except IntegrityError:
                res.corrupt.append(u)  # the coordinator drops this record and rebuilds that module
                raise
            with self.lock:
                self.present[u] = r.module
        res.fetch_s = time.time() - t

    def _publish(self, m: str, outs: dict[str, str], final: dict[str, str], res: ModuleResult,
                 key: str = "") -> None:
        t = time.time()
        rel_base = module_rel(m)
        for d in ("lib/lean", "ir"):
            for suf in LAKE_META_SUFFIXES + ALL_OUTPUT_SUFFIXES:
                p = os.path.join(self.build_dir, d, rel_base + suf)
                if suf in final and final.get(suf) == p:
                    continue
                if os.path.lexists(p) and (suf in LAKE_META_SUFFIXES or suf not in final):
                    os.remove(p)  # stale Lake metadata, or an output this build does not produce
        order = [s for s in outs if s != ".olean"] + [".olean"]
        refs = []
        for suf in order:
            src, dst = outs[suf], final[suf]
            if not os.path.exists(src):
                raise RuntimeError(f"lean did not write {os.path.basename(dst)}")
            ref = FileRef(os.path.relpath(dst, self.build_dir), sha256_file(src), os.path.getsize(src))
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            os.replace(src, dst)
            refs.append(ref)
        res.outputs = sorted(refs, key=lambda r: r.path)
        if self.store is not None:
            files = []
            for ref in res.outputs:
                if ref.path.endswith(".setup.json"):
                    continue
                stored = self.store.put_file(os.path.join(self.build_dir, ref.path))
                stored.path = ref.path
                files.append(stored)
            rec = ModuleRecord(m, files, self.worker_id, res.task_id, key=key)
            self.store.put_record(rec)
            with self.lock:
                self.present[rec.ident] = m
        res.publish_s = time.time() - t


def load_worker_project(cfg: BuildConfig, workspace: str) -> LakeProject:
    """The project as the coordinator sees it (with its translation of a `lakefile.lean`)."""
    if cfg.lakefile_toml:
        os.makedirs(workspace, exist_ok=True)
        path = os.path.join(os.path.abspath(workspace), "lakefile.translated.toml")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(cfg.lakefile_toml)
        return LakeProject.load(cfg.project_dir, config=path)
    return LakeProject.load(cfg.project_dir)


def _first_error(out: str) -> str:
    for line in out.splitlines():
        try:
            msg = json.loads(line)
        except ValueError:
            continue
        if isinstance(msg, dict) and msg.get("severity") == "error":
            return f"{msg.get('fileName', '')}:{(msg.get('pos') or {}).get('line', '?')}: {str(msg.get('data', ''))[:300]}"
    return out.strip()[-300:]
