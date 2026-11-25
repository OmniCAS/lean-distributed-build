"""A resident worker for the direct backend: registers, pulls module tasks, reports, heartbeats.

    lakeshard worker serve --coordinator http://HOST:PORT --id NAME --slots 3 --threads 1 \
        --workspace DIR [--token-file FILE]

`--slots` is how many `lean` processes run at once; `--threads` is `LEAN_NUM_THREADS` for each
(0 = Lean's default, all cores), unless the coordinator sets it for a task. The worker exits when
the coordinator says the build is finished, or when it cannot reach the coordinator for
`--give-up-s` seconds. The project, the toolchain and the dependencies' build outputs must be at
the same absolute paths as on the coordinator (see README, "Remote workers").
"""
from __future__ import annotations

import http.client
import json
import os
import socket
import sys
import threading
import time
from urllib.parse import urlsplit

from .direct import ModuleBuilder
from .protocol import BuildConfig, ModuleTask, dumps


class CoordinatorUnreachable(Exception):
    pass


class PullWorker:
    def __init__(self, url: str, worker_id: str, slots: int, threads: int, workspace: str,
                 token: str | None = None, claim_wait_s: float = 20.0, give_up_s: float = 300.0):
        self.url = url.rstrip("/")
        self._base = urlsplit(self.url).path.rstrip("/")
        self._local = threading.local()
        self.id, self.slots, self.threads = worker_id, max(1, slots), threads
        self.workspace = os.path.abspath(workspace)
        self.token = token
        self.claim_wait_s, self.give_up_s = claim_wait_s, give_up_s
        self.cond = threading.Condition()
        self.running: set[str] = set()  # task ids not yet acknowledged by the coordinator
        self.stop = threading.Event()
        self.builder: ModuleBuilder | None = None
        self.done_tasks = 0
        self.clock_offset: float | None = None  # worker clock - coordinator clock (lowest-latency sample)
        self.clock_rtt = float("inf")

    def _clock_sample(self, t_send: float, t_recv: float, server_time) -> None:
        """NTP-style: the coordinator stamped `server_time` between our send and receive."""
        if server_time is None:
            return
        rtt = t_recv - t_send
        if rtt <= self.clock_rtt:
            self.clock_rtt = rtt
            self.clock_offset = (t_send + t_recv) / 2 - float(server_time)

    def _conn(self, timeout: float) -> http.client.HTTPConnection:
        """One persistent connection per thread (claims, heartbeats and reports run on different threads)."""
        c = getattr(self._local, "conn", None)
        if c is None:
            u = urlsplit(self.url)
            c = http.client.HTTPConnection(u.hostname, u.port or 80, timeout=timeout)
            self._local.conn = c
        c.timeout = timeout
        if c.sock is not None:
            c.sock.settimeout(timeout)
        return c

    def _post(self, path: str, body: dict, timeout: float = 60.0) -> dict:
        data = dumps(body).encode()
        t0 = time.time()
        delay = 0.2
        while True:
            hdrs = {"Content-Type": "application/json", "Content-Length": str(len(data))}
            if self.token:
                hdrs["Authorization"] = f"Bearer {self.token}"
            try:
                conn = self._conn(timeout)
                conn.request("POST", self._base + path, body=data, headers=hdrs)
                r = conn.getresponse()
                out = r.read()
                if r.status == 200:
                    return json.loads(out)
                if r.status in (400, 401, 403, 404):
                    raise RuntimeError(f"coordinator refused {path}: {r.status} {out[:300]!r}")
                err: Exception = RuntimeError(f"{path}: HTTP {r.status} {out[:200]!r}")
            except (OSError, http.client.HTTPException) as e:
                err = e
                c = getattr(self._local, "conn", None)
                if c is not None:
                    c.close()
                self._local.conn = None
            if time.time() - t0 > self.give_up_s:
                raise CoordinatorUnreachable(f"{path}: {err}")
            time.sleep(delay)
            delay = min(5.0, delay * 2)

    def run(self) -> int:
        os.makedirs(self.workspace, exist_ok=True)
        t_send = time.time()
        resp = self._post("/v1/config", {"worker": self.id})
        self._clock_sample(t_send, time.time(), resp.get("server_time"))
        cfg = BuildConfig.from_dict(resp["config"])
        fp = None
        if cfg.fingerprint:  # prove that this machine's environment is the coordinator's
            from .direct import load_worker_project
            from .fingerprint import fingerprint
            wproj = load_worker_project(cfg, self.workspace)
            fp = fingerprint(wproj, cfg.toolchain_bin, wproj.graph(cfg.targets or None))
        resp = self._post("/v1/register", {"worker": self.id, "slots": self.slots, "threads": self.threads,
                                           "host": socket.gethostname(), "pid": os.getpid(), "fingerprint": fp})
        if resp.get("refused"):
            print(f"worker {self.id}: refused by the coordinator: {json.dumps(resp['refused'])}", file=sys.stderr)
            return 3
        self.builder = ModuleBuilder(cfg, self.id, self.workspace, self.threads, token=self.token)
        hb = threading.Thread(target=self._heartbeats, args=(cfg.heartbeat_s,), daemon=True)
        hb.start()
        workers: list[threading.Thread] = []
        try:
            while not self.stop.is_set():
                with self.cond:
                    while len(self.running) >= self.slots and not self.stop.is_set():
                        self.cond.wait(1.0)
                    free = self.slots - len(self.running)
                if self.stop.is_set():
                    break
                resp = self._post("/v1/claim", {"worker": self.id, "n": free, "wait_s": self.claim_wait_s,
                                                "clock_offset": self.clock_offset, "clock_rtt": self.clock_rtt},
                                  timeout=self.claim_wait_s + 60)
                for td in resp.get("tasks", []):
                    task = ModuleTask.from_dict(td)
                    with self.cond:
                        self.running.add(task.task_id)
                    t = threading.Thread(target=self._run_task, args=(task,), daemon=True)
                    t.start()
                    workers.append(t)
                if resp.get("refused"):
                    print(f"worker {self.id}: refused: {json.dumps(resp['refused'])}", file=sys.stderr)
                    return 3
                if resp.get("shutdown"):
                    break
        except CoordinatorUnreachable as e:
            print(f"worker {self.id}: giving up: {e}", file=sys.stderr)
            return 2
        finally:
            self.stop.set()
            for t in workers:
                t.join()
        return 0

    def _run_task(self, task: ModuleTask) -> None:
        res = self.builder.build(task)
        try:
            self._post("/v1/report", {"result": res})
        except Exception as e:  # noqa: BLE001
            print(f"worker {self.id}: could not report {task.task_id}: {e}", file=sys.stderr)
        with self.cond:
            self.running.discard(task.task_id)
            self.done_tasks += 1
            self.cond.notify_all()

    def _heartbeats(self, every_s: float) -> None:
        while not self.stop.wait(every_s):
            with self.cond:
                ids = sorted(self.running)
            try:
                t_send = time.time()
                resp = self._post("/v1/heartbeat", {"worker": self.id, "running": ids,
                                                    "clock_offset": self.clock_offset, "clock_rtt": self.clock_rtt},
                                  timeout=30)
                self._clock_sample(t_send, time.time(), resp.get("server_time"))
            except Exception:  # noqa: BLE001 - the main loop notices an unreachable coordinator
                continue
            for tid in resp.get("cancel", []):
                self.builder.cancel(tid)
            if resp.get("shutdown"):
                with self.cond:
                    idle = not self.running
                if idle:
                    self.stop.set()
                    with self.cond:
                        self.cond.notify_all()


def read_token(path: str | None) -> str | None:
    if not path:
        return os.environ.get("LAKESHARD_TOKEN") or None
    with open(path, encoding="utf-8") as fh:
        return fh.read().strip() or None
