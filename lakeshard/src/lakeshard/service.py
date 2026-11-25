"""The coordinator of the direct backend as a small HTTP service; workers pull tasks from it.

Why HTTP and not task files in the shared directory: the coordinator must decide, at the moment
a slot frees up, which ready module goes next (longest remaining path first), and every module of
a deep import chain waits for that decision. A long-polled HTTP request delivers it in
milliseconds and keeps all state in one process. Task files on NFS would need atomic claiming by
rename across clients and directory polling, and NFS attribute caching (typically 3-60 s) would
add that delay to every link of the chain (the simulations show 5-30 s per dependency doubling
the critical path of the Riemann-hypothesis archive). The service uses only the Python standard
library; the messages are the JSON of `lakeshard.protocol`. If sandboxes can reach the shared
directory but not each other over TCP, a file transport can implement the same four calls.

Endpoints (POST, JSON in and out; `Authorization: Bearer <token>` when a token is set):
- `/v1/config` `{worker}` -> `{config: BuildConfig}` (the worker then computes its fingerprint)
- `/v1/register` `{worker, slots, threads, host, pid, fingerprint}` -> `{config}`, or `{refused: why}`
  when the worker's environment fingerprint differs from the coordinator's
- `/v1/claim` `{worker, n, wait_s}` -> `{tasks: [ModuleTask], shutdown}` (waits up to `wait_s`)
- `/v1/report` `{result: ModuleResult}` -> `{accepted}`; a successful result is accepted only
  after the coordinator sees the reported outputs (shared directory) or records (store)
- `/v1/heartbeat` `{worker, running: [task ids], time}` -> `{cancel: [task ids], shutdown}`
- GET `/v1/status` -> counts
- `/v1/store/...` when the coordinator also serves the artifact store (see `httpstore.py`)

Every attempt is also kept as one run record (`records()`, written to `modules.jsonl`; format in
`docs/run-records.md`): coordinator-side times, the worker's own timestamps converted to the
coordinator's clock with an offset estimated from heartbeats, durations, CPU and memory.
"""
from __future__ import annotations

import hmac
import json
import os
import socket
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .direct import wait_visible
from .httpstore import StoreEndpoints, _discard_body
from .project import ProjectGraph
from .protocol import BuildConfig, ModuleResult, dumps, to_dict
from .scheduler import ModuleScheduler, lower_bound
from .store import open_store


class BuildService:
    def __init__(self, graph: ProjectGraph, scheduler: ModuleScheduler, config: BuildConfig, work_dir: str,
                 token: str | None = None, host: str = "127.0.0.1", port: int = 0, claim_wait_cap_s: float = 30.0,
                 store_root: str | None = None, advertise_host: str | None = None,
                 fingerprint: dict | None = None, keys: dict[str, str] | None = None):
        self.g, self.s, self.cfg = graph, scheduler, config
        self.work = os.path.abspath(work_dir)
        os.makedirs(self.work, exist_ok=True)
        self.token = token
        self.cond = threading.Condition()
        self.t0 = time.time()
        self.t_done: float | None = None
        self.claim_wait_cap_s = claim_wait_cap_s
        self.events = open(os.path.join(self.work, "events.jsonl"), "a", encoding="utf-8")
        self.worker_info: dict[str, dict] = {}
        self.module_seconds: dict[str, float] = {}
        self.ok_results: dict[str, dict] = {}
        self.failures: list[dict] = []
        self.totals = {"attempts": 0, "failed_attempts": 0, "stale_reports": 0, "lean_s": 0.0, "cpu_s": 0.0,
                       "max_rss_bytes": 0, "wait_s": 0.0, "fetch_s": 0.0, "fetched_bytes": 0, "publish_s": 0.0,
                       "confirm_s": 0.0, "output_bytes": 0}
        # the coordinator may serve the store itself; then it confirms outputs from the directory
        self.store_ep = StoreEndpoints(store_root) if store_root else None
        self.store = None
        if config.storage == "store":
            self.store = self.store_ep.store if self.store_ep else open_store(config.store, token=token)
        self.advertise_host = advertise_host
        self.fingerprint = fingerprint
        self.keys = keys or {}
        self.module_of_key = {k: m for m, k in self.keys.items()}
        self.refused: dict[str, dict] = {}
        self.dispatched: dict[str, tuple[float, float | None]] = {}  # task id -> (dispatch t, ready t)
        self.attempt_records: list[dict] = []
        self.clock: dict[str, list[float]] = {}  # worker -> samples of (worker clock - coordinator clock)
        self._stop = threading.Event()
        svc = self

        class Handler(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def log_message(self, *args):  # quiet
                pass

            def _reply(self, code: int, obj) -> None:
                data = json.dumps(to_dict(obj)).encode()
                self.send_response(code)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def _authorized(self) -> bool:
                if not svc.token:
                    return True
                got = self.headers.get("Authorization", "")
                return hmac.compare_digest(got, f"Bearer {svc.token}")

            def _store(self, method: str) -> bool:
                if svc.store_ep is None or not svc.store_ep.handles(self.path):
                    return False
                if not self._authorized():
                    _discard_body(self)
                    self._reply(401, {"error": "unauthorized"})
                    return True
                try:
                    svc.store_ep.handle(self, method)
                except Exception as e:  # noqa: BLE001
                    self._reply(500, {"error": f"{type(e).__name__}: {e}"})
                return True

            def do_HEAD(self):
                if not self._store("HEAD"):
                    self._reply(404, {"error": "not found"})

            def do_PUT(self):
                if not self._store("PUT"):
                    _discard_body(self)
                    self._reply(404, {"error": "not found"})

            def do_GET(self):
                if self._store("GET"):
                    return None
                if not self._authorized():
                    return self._reply(401, {"error": "unauthorized"})
                if self.path == "/v1/status":
                    return self._reply(200, svc.status())
                return self._reply(404, {"error": "not found"})

            def do_POST(self):
                if self._store("POST"):
                    return None
                if not self._authorized():
                    _discard_body(self)
                    return self._reply(401, {"error": "unauthorized"})
                n = int(self.headers.get("Content-Length") or 0)
                try:
                    body = json.loads(self.rfile.read(n) or b"{}")
                    fn = {"/v1/config": svc.config, "/v1/register": svc.register, "/v1/claim": svc.claim,
                          "/v1/report": svc.report, "/v1/heartbeat": svc.heartbeat}.get(self.path)
                    if fn is None:
                        return self._reply(404, {"error": "not found"})
                    return self._reply(200, fn(body))
                except Exception as e:  # noqa: BLE001
                    return self._reply(500, {"error": f"{type(e).__name__}: {e}"})

        self.httpd = ThreadingHTTPServer((host, port), Handler)
        self.httpd.daemon_threads = True
        self._threads: list[threading.Thread] = []

    @property
    def url(self) -> str:
        host, port = self.httpd.server_address[:2]
        if self.advertise_host:
            host = self.advertise_host
        elif host in ("0.0.0.0", "::"):
            host = socket.gethostname()
        return f"http://{host}:{port}"

    # --- lifecycle

    def start(self) -> None:
        self.t0 = time.time()
        self._log({"event": "start", "modules": len(self.g.modules), "storage": self.cfg.storage})
        for target in (self.httpd.serve_forever, self._housekeeping):
            t = threading.Thread(target=target, daemon=True)
            t.start()
            self._threads.append(t)

    def wait(self, timeout_s: float | None = None) -> bool:
        deadline = None if timeout_s is None else time.time() + timeout_s
        with self.cond:
            while not self.s.done():
                left = None if deadline is None else deadline - time.time()
                if left is not None and left <= 0:
                    return False
                self.cond.wait(timeout=1.0 if left is None else min(1.0, left))
        return True

    def stop(self, linger_s: float = 0.0) -> None:
        if linger_s:  # let workers see `shutdown` in their next claim or heartbeat
            time.sleep(linger_s)
        self._stop.set()
        self.httpd.shutdown()
        self.httpd.server_close()
        self.events.close()

    def _housekeeping(self) -> None:
        while not self._stop.wait(1.0):
            with self.cond:
                evs = self.s.expire(time.time())
                for ev in evs:
                    self.totals["failed_attempts"] += 1
                    self.failures.append({k: ev.get(k) for k in ("module", "worker", "attempt", "reason")})
                    self._log({"event": "expired", **ev})
                    disp, ready = self.dispatched.get(ev["task_id"], (None, None))
                    self.attempt_records.append({
                        "module": ev["module"], "attempt": ev["attempt"], "task_id": ev["task_id"], "ok": False,
                        "accepted": True, "worker": ev["worker"], "reason": ev.get("reason"),
                        "ready_t": self._rel(ready or self.t0), "dispatch_t": self._rel(disp),
                        "done_t": self._rel(time.time())})
                if evs:
                    self._mark_done()
                    self.cond.notify_all()

    def _log(self, ev: dict) -> None:
        ev = {"t": round(time.time() - self.t0, 3), **ev}
        self.events.write(json.dumps(ev, ensure_ascii=False) + "\n")
        self.events.flush()

    def _mark_done(self) -> None:
        if self.t_done is None and self.s.done():
            self.t_done = time.time()
            self._log({"event": "done", "counts": self.s.counts()})

    # --- endpoints

    def config(self, body: dict) -> dict:
        return {"config": self.cfg, "server_time": time.time()}

    def register(self, body: dict) -> dict:
        wid = body["worker"]
        if self.fingerprint is not None:
            from .fingerprint import fingerprint_diff
            fp = body.get("fingerprint") or {}
            if fp.get("sha256") != self.fingerprint["sha256"]:
                why = {"reason": "environment fingerprint differs",
                       "parts": fingerprint_diff(self.fingerprint, fp) if fp else ["missing"],
                       "host": body.get("host", "")}
                with self.cond:
                    self.refused[wid] = why
                    self._log({"event": "refused", "worker": wid, **why})
                return {"refused": why}
        with self.cond:
            now = time.time()
            self.s.register(wid, int(body.get("slots", 1)), now)
            self.refused.pop(wid, None)
            self.worker_info[wid] = {"slots": int(body.get("slots", 1)), "threads": int(body.get("threads", 0)),
                                     "host": body.get("host", ""), "pid": body.get("pid"), "tasks": 0,
                                     "failed": 0, "lean_s": 0.0, "cpu_s": 0.0, "max_rss_bytes": 0}
            self._log({"event": "register", "worker": wid, "slots": body.get("slots"), "host": body.get("host")})
            self.cond.notify_all()
        return {"config": self.cfg, "server_time": time.time()}

    def _note_clock(self, body: dict) -> None:
        """Keep the worker's own round-trip estimate of its clock offset (sent with claims and heartbeats)."""
        if body.get("clock_offset") is not None:
            self.clock[body["worker"]] = [float(body["clock_offset"])]
            if body["worker"] in self.worker_info:
                self.worker_info[body["worker"]]["clock_rtt_s"] = body.get("clock_rtt")
                self.worker_info[body["worker"]]["clock_offset_estimate_s"] = float(body["clock_offset"])

    def claim(self, body: dict) -> dict:
        wid, n = body["worker"], max(0, int(body.get("n", 1)))
        with self.cond:
            if wid in self.refused or wid not in self.worker_info:
                return {"tasks": [], "shutdown": False, "refused": self.refused.get(wid, {"reason": "not registered"})}
            self._note_clock(body)
        deadline = time.time() + min(float(body.get("wait_s", 0.0)), self.claim_wait_cap_s)
        with self.cond:
            while True:
                if self.s.done():
                    return {"tasks": [], "shutdown": True}
                tasks = self.s.claim(wid, n, time.time()) if n else []
                if tasks:
                    now = time.time()
                    for t in tasks:
                        ra = self.s.ready_at.get(t.module)
                        self.dispatched[t.task_id] = (now, ra)
                        self._log({"event": "dispatch", "task_id": t.task_id, "module": t.module, "worker": wid,
                                   "attempt": t.attempt, "threads": t.threads,
                                   "ready_t": round((ra or self.t0) - self.t0, 3)})
                    return {"tasks": tasks, "shutdown": False}
                left = deadline - time.time()
                if left <= 0:
                    return {"tasks": [], "shutdown": False}
                self.cond.wait(timeout=left)

    def heartbeat(self, body: dict) -> dict:
        with self.cond:
            now = time.time()
            self._note_clock(body)
            cancel = self.s.heartbeat(body["worker"], list(body.get("running", [])), now)
            return {"cancel": cancel, "shutdown": self.s.done(), "server_time": time.time()}

    def _confirm(self, res: ModuleResult, ident: str) -> str:
        """'' if the outputs are visible to the coordinator, else the reason."""
        if self.cfg.storage == "store":
            rec = self.store.get_records([ident]).get(ident)
            if rec is None or not any(f.path.endswith(".olean") for f in rec.files):
                return "no record with an .olean in the store"
            return ""
        paths = {os.path.join(self.cfg.build_dir, f.path): f.size for f in res.outputs}
        if not any(p.endswith(".olean") for p in paths):
            return "no .olean among the reported outputs"
        missing, waited = wait_visible(list(paths), self.cfg.visibility_timeout_s, self.cfg.visibility_poll_s,
                                       sizes=paths)
        if missing:
            return f"{len(missing)} outputs not visible to the coordinator after {waited:.1f} s, e.g. {missing[0]}"
        return ""

    def report(self, body: dict) -> dict:
        res = ModuleResult.from_dict(body["result"])
        t_report = time.time()
        with self.cond:  # a report is a sign of life; its task must not expire while we check outputs
            self.s.touch(res.worker, t_report)
            live = res.task_id in self.s.running and self.s.running[res.task_id].worker == res.worker
            ident = (self.s.running[res.task_id].task.key or res.module) if live else res.module
            if live:
                self.s.confirming.add(res.task_id)
        t = time.time()
        if res.ok and live:
            why = self._confirm(res, ident)
            if why:
                res.ok, res.error = False, why
        dropped = []
        for k in res.corrupt if live and self.store is not None else []:
            if self.store.drop_record(k):  # an import's stored outputs are corrupt: build that module again
                dropped.append(k)
        confirm_s = time.time() - t
        with self.cond:
            self.s.confirming.discard(res.task_id)
            for k in dropped:
                m = self.module_of_key.get(k)
                if m and self.s.invalidate(m, time.time()):
                    self._log({"event": "invalidated", "module": m, "key": k, "reason": "corrupt objects in the store"})
            kind = "corrupt" if res.corrupt else "error"
            ev = self.s.complete(res.task_id, res.ok, time.time(), res.error, kind=kind) if live else None
            rec = {k: v for k, v in json.loads(dumps(res)).items() if k not in ("outputs", "log_tail")}
            rec["confirm_s"] = round(confirm_s, 4)
            rec["accepted"] = ev is not None
            if ev is not None:
                rec.update({k: ev[k] for k in ("action", "released", "skipped", "class", "kind") if k in ev})
            if not res.ok:
                rec["log_tail"] = res.log_tail[-1500:]
            self._log({"event": "result", **rec})
            if ev is None:
                self.totals["stale_reports"] += 1
            else:
                self._account(res, confirm_s)
            self._record(res, t_report, time.time(), confirm_s, ev is not None)
            self._mark_done()
            self.cond.notify_all()
        return {"accepted": ev is not None}

    def _account(self, res: ModuleResult, confirm_s: float) -> None:
        tt = self.totals
        tt["attempts"] += 1
        for k in ("lean_s", "cpu_s", "wait_s", "fetch_s", "fetched_bytes", "publish_s"):
            tt[k] += getattr(res, k)
        tt["confirm_s"] += confirm_s
        tt["max_rss_bytes"] = max(tt["max_rss_bytes"], res.max_rss_bytes)
        wi = self.worker_info.setdefault(res.worker, {"slots": 0, "threads": 0, "host": "", "pid": None, "tasks": 0,
                                                      "failed": 0, "lean_s": 0.0, "cpu_s": 0.0, "max_rss_bytes": 0})
        wi["tasks"] += 1
        wi["lean_s"] += res.lean_s
        wi["cpu_s"] += res.cpu_s
        wi["max_rss_bytes"] = max(wi["max_rss_bytes"], res.max_rss_bytes)
        if res.ok:
            self.module_seconds[res.module] = round(res.lean_s, 3)
            tt["output_bytes"] += sum(f.size for f in res.outputs)
            self.ok_results[res.module] = {"worker": res.worker, "start": round(res.started - self.t0, 3),
                                           "lean_s": round(res.lean_s, 3), "wall_s": round(res.wall_s, 3)}
        else:
            tt["failed_attempts"] += 1
            wi["failed"] += 1
            self.failures.append({"module": res.module, "worker": res.worker, "attempt": res.attempt,
                                  "kind": "corrupt" if res.corrupt else "error", "error": res.error[:500]})

    # --- run records

    def _rel(self, t: float | None) -> float | None:
        return None if t is None else round(t - self.t0, 4)

    def clock_offset(self, worker: str) -> float:
        """Worker clock - coordinator clock, as estimated by the worker from its lowest-latency
        register/heartbeat round trip (error at most half that round trip); 0 if unknown."""
        if self.worker_info.get(worker, {}).get("host") == socket.gethostname():
            return 0.0  # same machine, same clock
        xs = self.clock.get(worker, [])
        return xs[-1] if xs else 0.0

    def _record(self, res: ModuleResult, t_report: float, t_done: float, confirm_s: float, accepted: bool) -> None:
        off = self.clock_offset(res.worker)
        disp, ready = self.dispatched.get(res.task_id, (None, None))
        w = lambda t: self._rel(t - off) if t else None  # noqa: E731 - worker clock -> coordinator clock
        self.attempt_records.append({
            "module": res.module, "attempt": res.attempt, "task_id": res.task_id, "ok": res.ok, "accepted": accepted,
            "worker": res.worker, "host": res.host, "threads": res.threads,
            "slots": self.worker_info.get(res.worker, {}).get("slots"),
            "ready_t": self._rel(ready or self.t0), "dispatch_t": self._rel(disp), "start_t": w(res.started),
            "lean_start_t": w(res.lean_start), "lean_end_t": w(res.lean_end), "end_t": w(res.ended),
            "report_t": self._rel(t_report), "done_t": self._rel(t_done),
            "wall_s": round(res.wall_s, 4), "wait_s": round(res.wait_s, 4), "fetch_s": round(res.fetch_s, 4),
            "lean_s": round(res.lean_s, 4), "publish_s": round(res.publish_s, 4), "confirm_s": round(confirm_s, 4),
            "cpu_s": round(res.cpu_s, 3), "max_rss_bytes": res.max_rss_bytes, "fetched_files": res.fetched_files,
            "fetched_bytes": res.fetched_bytes, "output_bytes": sum(f.size for f in res.outputs),
            "clock_offset_s": round(off, 4), "error": res.error[:300]})

    def records(self) -> list[dict]:
        with self.cond:
            return list(self.attempt_records)

    def write_manifest(self, path: str) -> dict:
        """Module -> input key of every module whose outputs are in the store after this run."""
        with self.cond:
            done = {m: self.keys.get(m, m) for m, v in self.s.state.items() if v == "done"}
        man = {"schema": "lakeshard-build-manifest/1", "fingerprint": self.fingerprint, "store": self.cfg.store,
               "modules": dict(sorted(done.items()))}
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(man, fh, indent=0)
        return man

    def write_records(self, path: str) -> int:
        recs = self.records()
        with open(path, "w", encoding="utf-8") as fh:
            for r in recs:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        return len(recs)

    # --- results

    def status(self) -> dict:
        with self.cond:
            return {"counts": self.s.counts(), "running": len(self.s.running), "workers": len(self.s.workers),
                    "elapsed_s": round(time.time() - self.t0, 1), "done": self.s.done()}

    def report_dict(self) -> dict:
        with self.cond:
            end = self.t_done or time.time()
            wall = end - self.t0
            counts = self.s.counts()
            slots = sum(w["slots"] for w in self.worker_info.values())
            lb = lower_bound(self.g, self.module_seconds, slots)
            lb["ratio"] = round(wall / lb["bound_s"], 3) if lb["bound_s"] else None
            tt = {k: (round(v, 3) if isinstance(v, float) else v) for k, v in self.totals.items()}
            failed = {m: self.s.failure_class.get(m, "") for m, v in self.s.state.items() if v == "failed"}
            skipped = sorted(m for m, v in self.s.state.items() if v == "skipped")
            return {"ok": counts.get("done", 0) == len(self.g.modules), "backend": "lean",
                    "from_store": len(self.s.cached), "built": len(self.module_seconds),
                    "failed_modules": failed, "skipped_modules": skipped[:200], "skipped_count": len(skipped),
                    "refused_workers": dict(self.refused),
                    "storage": self.cfg.storage, "build_dir": self.cfg.build_dir, "store": self.cfg.store,
                    "wall_s": round(wall, 2), "modules": len(self.g.modules), "status": counts,
                    "modules_built": counts.get("done", 0), "slots": slots, "lower_bound": lb, "totals": tt,
                    "workers": {w: dict(i, clock_offset_s=round(self.clock_offset(w), 4))
                                for w, i in self.worker_info.items()},
                    "store_server": dict(self.store_ep.stats) if self.store_ep else None,
                    "failures": self.failures[:100],
                    "module_seconds": dict(self.module_seconds)}
