"""Schedule shard jobs on workers, retry failures, and record what happened.

The coordinator talks to workers only through an `Executor` (submit a `ShardJob`, collect
`ShardResult`s). `LocalProcessExecutor` runs each job as a separate worker process on this
machine, every worker with its own workspace; a remote executor (HTTP, queue, ssh) can replace it.

Two schedules:
- static: the shards of a precomputed `Plan` (acyclic shard graph); a shard starts when all the
  shards it imports from are done.
- dynamic (default): batches are formed at run time from modules whose imports are all built,
  highest remaining-path first, extended along their import chains up to a cost budget. Nothing
  waits for an unrelated module just because a static plan put them together.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass, field

from .plan import bottom_levels, shard_needs
from .project import ProjectGraph
from .protocol import Plan, ShardJob, ShardResult, dumps


@dataclass
class WorkerSpec:
    id: str
    threads: int = 0  # LEAN_NUM_THREADS for jobs on this worker (0 = Lean's default)


class Executor:
    def submit(self, worker: WorkerSpec, job: ShardJob) -> None: ...
    def poll(self, timeout: float) -> list[ShardResult]: ...
    def shutdown(self) -> None: ...


class LocalProcessExecutor(Executor):
    """One OS process per job; worker state lives in `<work>/workers/<id>/`."""

    def __init__(self, work_dir: str, python: str = sys.executable, kill_grace_s: float = 120.0):
        self.work = os.path.abspath(work_dir)
        self.python = python
        self.grace = kill_grace_s
        self.running: dict[str, tuple[subprocess.Popen, ShardJob, WorkerSpec, str, float]] = {}
        os.makedirs(os.path.join(self.work, "jobs"), exist_ok=True)

    def workspace(self, worker_id: str) -> str:
        return os.path.join(self.work, "workers", worker_id)

    def submit(self, worker: WorkerSpec, job: ShardJob) -> None:
        jp = os.path.join(self.work, "jobs", f"{job.job_id}.json")
        rp = os.path.join(self.work, "jobs", f"{job.job_id}.result.json")
        lp = os.path.join(self.work, "jobs", f"{job.job_id}.log")
        with open(jp, "w", encoding="utf-8") as fh:
            fh.write(dumps(job))
        ws = self.workspace(worker.id)
        os.makedirs(ws, exist_ok=True)
        log = open(lp, "w", encoding="utf-8")
        src = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        env = dict(os.environ)
        env["PYTHONPATH"] = src + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        p = subprocess.Popen([self.python, "-m", "lakeshard", "worker", "run", "--job", jp, "--result", rp,
                              "--workspace", ws, "--worker-id", worker.id],
                             stdout=log, stderr=subprocess.STDOUT, env=env)
        log.close()
        self.running[job.job_id] = (p, job, worker, rp, time.time())

    def poll(self, timeout: float) -> list[ShardResult]:
        deadline = time.time() + timeout
        while True:
            done = []
            for jid, (p, job, worker, rp, t0) in list(self.running.items()):
                if p.poll() is None and time.time() - t0 > job.timeout_s + self.grace:
                    p.kill()
                    p.wait()
                if p.poll() is not None:
                    del self.running[jid]
                    if os.path.exists(rp):
                        with open(rp, encoding="utf-8") as fh:
                            done.append(ShardResult.from_dict(json.load(fh)))
                    else:
                        done.append(ShardResult(jid, job.shard_id, worker.id, ok=False,
                                                error=f"worker process exited with {p.returncode} and no result"))
            if done or not self.running or time.time() >= deadline:
                return done
            time.sleep(0.02)

    def shutdown(self) -> None:
        for p, *_ in self.running.values():
            p.kill()
        self.running.clear()


@dataclass
class BuildOptions:
    project_dir: str
    lakefile: str
    toolchain_bin: str
    store: str
    retries: int = 2
    timeout_s: float = 7200.0
    locality_weight: float = 0.3
    batch_cost: float = 60.0  # dynamic schedule: estimated seconds of work per batch
    max_batch: int = 2000  # dynamic schedule: modules per batch (keeps the lake command line short)
    fail_once: set = field(default_factory=set)  # test hook: shard ids (static) or batch numbers (dynamic)


class _Accounting:
    def __init__(self, workers: list[WorkerSpec], events_path: str | None):
        self.t0 = time.time()
        self.per_worker = {w.id: {"jobs": 0, "failed": 0, "busy_s": 0.0, "fetched_bytes": 0, "uploaded_bytes": 0}
                           for w in workers}
        self.totals = {"cpu_s": 0.0, "fetch_s": 0.0, "build_s": 0.0, "upload_s": 0.0, "fetched_bytes": 0,
                       "uploaded_bytes": 0, "max_rss_bytes": 0, "jobs": 0}
        self.module_seconds: dict[str, float] = {}
        self.failures: list[dict] = []
        self.events = open(events_path, "a", encoding="utf-8") if events_path else None

    def record(self, r: ShardResult, attempt: int) -> None:
        self.totals["jobs"] += 1
        pw = self.per_worker[r.worker]
        pw["jobs"] += 1
        pw["busy_s"] += r.wall_s
        pw["fetched_bytes"] += r.fetched_bytes
        pw["uploaded_bytes"] += r.uploaded_bytes
        for k in ("cpu_s", "fetch_s", "build_s", "upload_s", "fetched_bytes", "uploaded_bytes"):
            self.totals[k] += getattr(r, k)
        self.totals["max_rss_bytes"] = max(self.totals["max_rss_bytes"], r.max_rss_bytes)
        self.module_seconds.update(r.module_seconds)
        if not r.ok:
            pw["failed"] += 1
            self.failures.append({"shard": r.shard_id, "worker": r.worker, "attempt": attempt,
                                  "error": r.error[:500]})
        if self.events:
            ev = {k: v for k, v in json.loads(dumps(r)).items() if k != "records"}
            ev["t"] = round(time.time() - self.t0, 3)
            ev["modules"] = len(r.records)
            self.events.write(json.dumps(ev, ensure_ascii=False) + "\n")
            self.events.flush()

    def close(self) -> None:
        if self.events:
            self.events.close()

    def report(self, **kw) -> dict:
        out = {"wall_s": round(time.time() - self.t0, 2), "totals": self.totals, "per_worker": self.per_worker,
               "failures": self.failures, "module_seconds": self.module_seconds}
        out.update(kw)
        return out


def _job(opts: BuildOptions, w: WorkerSpec, job_id: str, sid: str, modules: list[str], needs: list[str],
         attempt: int, fail: bool) -> ShardJob:
    return ShardJob(job_id=job_id, shard_id=sid, modules=modules, needs=needs, project_dir=opts.project_dir,
                    lakefile=opts.lakefile, toolchain_bin=opts.toolchain_bin, threads=w.threads,
                    timeout_s=opts.timeout_s, attempt=attempt, store=opts.store, fail_on_purpose=fail)


class Coordinator:
    """Static schedule over the shards of a `Plan`."""

    def __init__(self, graph: ProjectGraph, plan: Plan, executor: Executor, workers: list[WorkerSpec],
                 opts: BuildOptions, events_path: str | None = None):
        self.g, self.plan, self.ex, self.workers, self.o = graph, plan, executor, workers, opts
        self.events_path = events_path
        self.shards = {s.id: s for s in plan.shards}
        self.needs = shard_needs(graph, plan)
        self.bl = bottom_levels(plan)
        self.children: dict[str, list[str]] = {s.id: [] for s in plan.shards}
        for s in plan.shards:
            for d in s.deps:
                self.children[d].append(s.id)

    def run(self) -> dict:
        acc = _Accounting(self.workers, self.events_path)
        remaining = {sid: len(s.deps) for sid, s in self.shards.items()}
        ready = {sid for sid, k in remaining.items() if k == 0}
        status: dict[str, str] = {}
        attempts: dict[str, int] = {}
        avoid: dict[str, set] = {}
        present: dict[str, set] = {w.id: set() for w in self.workers}
        busy: dict[str, str | None] = {w.id: None for w in self.workers}
        blmax = max(self.bl.values(), default=1.0) or 1.0
        seq = 0

        def pick(w: WorkerSpec) -> str | None:
            cands = [s for s in ready if w.id not in avoid.get(s, set())] or list(ready)
            cands.sort(key=lambda s: -self.bl[s])
            best, best_score = None, -1.0
            for s in cands[:16]:
                need = self.needs[s]
                overlap = (len(present[w.id].intersection(need)) / len(need)) if need else 1.0
                score = self.bl[s] / blmax + self.o.locality_weight * overlap
                if score > best_score:
                    best, best_score = s, score
            return best

        def skip_down(sid: str) -> None:
            stack = list(self.children[sid])
            while stack:
                c = stack.pop()
                if c not in status:
                    status[c] = "skipped"
                    stack.extend(self.children[c])

        try:
            while len(status) < len(self.shards):
                for w in self.workers:
                    if busy[w.id] is None and ready:
                        sid = pick(w)
                        ready.discard(sid)
                        attempts[sid] = attempts.get(sid, 0) + 1
                        seq += 1
                        busy[w.id] = sid
                        self.ex.submit(w, _job(self.o, w, f"j{seq:06d}-{sid}-a{attempts[sid]}", sid,
                                               self.shards[sid].modules, self.needs[sid], attempts[sid],
                                               sid in self.o.fail_once and attempts[sid] == 1))
                if all(b is None for b in busy.values()) and not ready:
                    for sid in self.shards:
                        status.setdefault(sid, "skipped")
                    break
                for r in self.ex.poll(timeout=1.0):
                    busy[r.worker] = None
                    sid = r.shard_id
                    acc.record(r, attempts[sid])
                    if r.ok:
                        status[sid] = "ok"
                        present[r.worker].update(self.needs[sid])
                        present[r.worker].update(self.shards[sid].modules)
                        for c in self.children[sid]:
                            remaining[c] -= 1
                            if remaining[c] == 0 and c not in status:
                                ready.add(c)
                    elif attempts[sid] <= self.o.retries:
                        avoid.setdefault(sid, set()).add(r.worker)
                        ready.add(sid)
                    else:
                        status[sid] = "failed"
                        skip_down(sid)
        finally:
            self.ex.shutdown()
            acc.close()
        counts: dict[str, int] = {}
        for v in status.values():
            counts[v] = counts.get(v, 0) + 1
        built = sum(len(self.shards[s].modules) for s, v in status.items() if v == "ok")
        return acc.report(ok=built == len(self.g.modules), schedule="static", shards=len(self.shards),
                          status=counts, modules=len(self.g.modules), modules_built=built,
                          workers=[w.id for w in self.workers], threads_per_worker=[w.threads for w in self.workers])


class DynamicCoordinator:
    """Batches formed at run time from ready modules (see module docstring)."""

    def __init__(self, graph: ProjectGraph, costs: dict[str, float], executor: Executor,
                 workers: list[WorkerSpec], opts: BuildOptions, events_path: str | None = None):
        self.g, self.c, self.ex, self.workers, self.o = graph, costs, executor, workers, opts
        self.events_path = events_path
        self.children = graph.children()
        self.bl: dict[str, float] = {}
        for m in reversed(graph.order):
            self.bl[m] = costs[m] + max((self.bl[ch] for ch in self.children[m]), default=0.0)

    def run(self) -> dict:
        g, o = self.g, self.o
        acc = _Accounting(self.workers, self.events_path)
        indeg = {m: len(i.imports) for m, i in g.modules.items()}
        ready = {m for m, d in indeg.items() if d == 0}
        done: set[str] = set()
        running: set[str] = set()
        status: dict[str, str] = {}  # final: ok | failed | skipped
        attempts: dict[str, int] = {}
        solo: set[str] = set()  # modules to build alone after a failed batch
        avoid: dict[str, set] = {}
        present: dict[str, set] = {w.id: set() for w in self.workers}
        busy: dict[str, list[str] | None] = {w.id: None for w in self.workers}
        blmax = max(self.bl.values(), default=1.0) or 1.0
        seq = 0
        batches = 0

        def form_batch(w: WorkerSpec) -> list[str]:
            cands = [m for m in ready if w.id not in avoid.get(m, set())] or list(ready)
            cands.sort(key=lambda m: -self.bl[m])
            first, best = None, -1.0
            for m in cands[:16]:
                need = g.modules[m].imports
                overlap = (len(present[w.id].intersection(need)) / len(need)) if need else 1.0
                score = self.bl[m] / blmax + o.locality_weight * overlap
                if score > best:
                    first, best = m, score
            batch, inb, cost = [first], {first}, self.c[first]
            if first in solo:
                return batch
            # extend: descendants that become buildable inside the batch first, then other ready modules
            pool = [m for m in cands if m != first and m not in solo]
            while cost < o.batch_cost and len(batch) < o.max_batch:
                chain = [ch for b in batch for ch in self.children[b]
                         if ch not in inb and ch not in solo and ch not in status and ch not in running
                         and all(u in done or u in inb for u in g.modules[ch].imports)]
                nxt = max(chain, key=lambda m: self.bl[m]) if chain else None
                if nxt is None:
                    while pool and pool[0] in inb:
                        pool.pop(0)
                    if not pool:
                        break
                    nxt = pool.pop(0)
                batch.append(nxt)
                inb.add(nxt)
                cost += self.c[nxt]
            return batch

        def skip_down(m: str) -> None:
            stack = list(self.children[m])
            while stack:
                c = stack.pop()
                if c not in status:
                    status[c] = "skipped"
                    ready.discard(c)
                    stack.extend(self.children[c])

        try:
            while len(status) < len(g.modules):
                for w in self.workers:
                    if busy[w.id] is None and ready:
                        batch = form_batch(w)
                        for m in batch:
                            ready.discard(m)
                            running.add(m)
                            attempts[m] = attempts.get(m, 0) + 1
                        seq += 1
                        batches += 1
                        sid = f"b{seq:06d}"
                        needs = sorted(g.closure(batch) - set(batch))
                        assert all(u in done for u in needs), "scheduler bug: batch needs unbuilt modules"
                        busy[w.id] = batch
                        self.ex.submit(w, _job(o, w, f"j{seq:06d}-{sid}", sid, batch, needs,
                                               max(attempts[m] for m in batch), sid in o.fail_once))
                if all(b is None for b in busy.values()) and not ready:
                    for m in g.modules:
                        status.setdefault(m, "skipped")
                    break
                for r in self.ex.poll(timeout=1.0):
                    batch = busy[r.worker] or []
                    busy[r.worker] = None
                    acc.record(r, max((attempts.get(m, 1) for m in batch), default=1))
                    running.difference_update(batch)
                    if r.ok:
                        present[r.worker].update(batch)
                        present[r.worker].update(g.closure(batch))
                        for m in batch:
                            done.add(m)
                            status[m] = "ok"
                        for m in batch:
                            for ch in self.children[m]:
                                indeg[ch] -= 1
                                if indeg[ch] == 0 and ch not in status:
                                    ready.add(ch)
                        continue
                    for m in batch:
                        if attempts[m] <= o.retries:
                            avoid.setdefault(m, set()).add(r.worker)
                            if len(batch) > 1:
                                solo.add(m)  # isolate the failing module on the retry
                            if indeg[m] == 0:  # chain members wait until their imports are built
                                ready.add(m)
                        else:
                            status[m] = "failed"
                            skip_down(m)
        finally:
            self.ex.shutdown()
            acc.close()
        counts: dict[str, int] = {}
        for v in status.values():
            counts[v] = counts.get(v, 0) + 1
        return acc.report(ok=counts.get("ok", 0) == len(g.modules), schedule="dynamic", batches=batches,
                          batch_cost_s=o.batch_cost, status=counts, modules=len(g.modules),
                          modules_built=counts.get("ok", 0), workers=[w.id for w in self.workers],
                          threads_per_worker=[w.threads for w in self.workers])
