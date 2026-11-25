"""Module-level scheduling for the direct backend: a pure state machine (no I/O, no threads).

States: `waiting` (some import not done) -> `ready` -> `running` -> `done`, or `failed` / `skipped`.

- `claim(worker, n)`: up to n ready modules, the one with the longest remaining path first (`bl`:
  its own cost plus the heaviest chain of importers below it). A module that already failed on
  this worker is left for another live worker that has not failed it, if there is one.
- `complete(task, ok)`: ok -> done (the caller has already confirmed that the outputs exist), and
  importers whose imports are now all done become ready. Not ok -> back to ready, to be retried on
  another worker, until `retries` retries are used; then failed, and every module that imports it,
  directly or not, is skipped.
- `heartbeat` / `expire`: a worker not heard from for `lease_s` is presumed lost; its tasks count
  as failed attempts and go to other workers. A task running longer than its timeout plus a
  grace period is failed the same way. A worker that reports tasks the scheduler has given to
  someone else is told to cancel them.
- Heavy modules (estimated cost >= `heavy_cost`) can be given `heavy_threads` Lean threads; the
  rule is only a parameter for now (no tuning).
- `done`: modules whose outputs the store already has for their current input key (resume,
  incremental rebuild); they start as done and are never dispatched.
- Failure classes: a module that fails with an error on `source_failure_workers` different workers
  is a source problem and fails at once (its importers are skipped); lost workers, overdue tasks
  and corrupt inputs do not count towards that. `invalidate(m)` puts a done module back (its stored
  outputs turned out corrupt) so that it is rebuilt before its waiting importers.
"""
from __future__ import annotations

import heapq
import itertools
import math
from collections import defaultdict
from dataclasses import dataclass

from .project import ProjectGraph
from .protocol import ModuleTask

TERMINAL = ("done", "failed", "skipped")


@dataclass
class Running:
    task: ModuleTask
    worker: str
    started: float


class ModuleScheduler:
    def __init__(self, graph: ProjectGraph, costs: dict[str, float], retries: int = 2, lease_s: float = 60.0,
                 timeout_s: float = 7200.0, threads: int = 0, heavy_cost: float = math.inf, heavy_threads: int = 0,
                 needs_closure: bool = False, fail_once: set | None = None, overdue_grace_s: float = 120.0,
                 keys: dict[str, str] | None = None, done: set | None = None, source_failure_workers: int = 2,
                 priority: str = "bl", assign: dict[str, str] | None = None):
        self.g, self.costs = graph, costs
        self.retries, self.lease_s, self.timeout_s = retries, lease_s, timeout_s
        self.threads, self.heavy_cost, self.heavy_threads = threads, heavy_cost, heavy_threads
        self.needs_closure = needs_closure
        self.fail_once = set(fail_once or ())
        self.overdue_grace_s = overdue_grace_s
        self.keys = keys or {}
        self.source_failure_workers = source_failure_workers
        self.cached = set(done or ()) & set(graph.modules)
        self.failure_class: dict[str, str] = {}
        self.error_workers: dict[str, set] = defaultdict(set)
        if priority not in ("bl", "fifo", "structure"):
            raise ValueError(f"unknown priority {priority!r}")
        self.priority = priority  # bl: longest remaining path by cost; structure: by module count; fifo
        self.assign = dict(assign or {})  # fixed placement: module -> the only worker that may build it
        self._ready_seq = itertools.count()
        self.children = graph.children()
        self.bl: dict[str, float] = {}
        unit = priority == "structure"
        for m in reversed(graph.order):
            self.bl[m] = (1.0 if unit else costs[m]) + max((self.bl[c] for c in self.children[m]), default=0.0)
        self.state = dict.fromkeys(graph.modules, "waiting")
        self.indeg = {m: len(i.imports) for m, i in graph.modules.items()}
        self.ready: list[tuple[float, str]] = []
        self.attempts: dict[str, int] = defaultdict(int)
        self.avoid: dict[str, set] = defaultdict(set)
        self.running: dict[str, Running] = {}
        self.workers: dict[str, dict] = {}
        self.errors: dict[str, list[str]] = defaultdict(list)
        self.confirming: set[str] = set()  # task ids whose outputs the caller is checking; never expired
        self.ready_at: dict[str, float | None] = {}  # when each module last became ready (None: at start)
        self._seq = itertools.count(1)
        self._terminal = 0
        for m in self.cached:
            self.state[m] = "done"
            self._terminal += 1
        for m in graph.modules:
            self.indeg[m] = sum(1 for u in graph.modules[m].imports if u not in self.cached)
        for m, d in self.indeg.items():
            if d == 0 and self.state[m] == "waiting":
                self._make_ready(m)

    # --- workers

    def register(self, worker: str, slots: int, now: float) -> None:
        w = self.workers.setdefault(worker, {"slots": slots, "alive": True, "last_seen": now})
        w.update(slots=slots, alive=True, last_seen=now)

    def touch(self, worker: str, now: float) -> None:
        w = self.workers.setdefault(worker, {"slots": 0, "alive": True, "last_seen": now})
        w["alive"], w["last_seen"] = True, now

    def heartbeat(self, worker: str, running_ids: list[str], now: float) -> list[str]:
        """Record that `worker` is alive; return the ids it should cancel (no longer its tasks)."""
        self.touch(worker, now)
        return [t for t in running_ids if t not in self.running or self.running[t].worker != worker]

    def total_slots(self) -> int:
        return sum(w["slots"] for w in self.workers.values())

    # --- tasks

    def _make_ready(self, m: str, now: float | None = None) -> None:
        self.state[m] = "ready"
        self.ready_at[m] = now
        key = float(next(self._ready_seq)) if self.priority == "fifo" else -self.bl[m]
        heapq.heappush(self.ready, (key, m))

    def _others_can(self, m: str, worker: str) -> bool:
        return any(w != worker and info["alive"] and w not in self.avoid[m] for w, info in self.workers.items())

    def claim(self, worker: str, n: int, now: float) -> list[ModuleTask]:
        self.touch(worker, now)
        tasks: list[ModuleTask] = []
        held = []
        while self.ready and len(tasks) < n:
            item = heapq.heappop(self.ready)
            m = item[1]
            if self.state[m] != "ready":
                continue  # stale heap entry
            pinned = self.assign.get(m)
            if pinned is not None:
                if pinned != worker:
                    held.append(item)
                    continue
            elif worker in self.avoid[m] and self._others_can(m, worker):
                held.append(item)
                continue
            tasks.append(self._start(m, worker, now))
        for item in held:
            heapq.heappush(self.ready, item)
        return tasks

    def _start(self, m: str, worker: str, now: float) -> ModuleTask:
        self.attempts[m] += 1
        heavy = self.heavy_threads and self.costs[m] >= self.heavy_cost
        clos = sorted(self.g.closure([m])) if self.needs_closure else []
        task = ModuleTask(task_id=f"t{next(self._seq):07d}", module=m, attempt=self.attempts[m],
                          threads=self.heavy_threads if heavy else self.threads, timeout_s=self.timeout_s,
                          needs=[self.keys.get(u, u) for u in clos], key=self.keys.get(m, ""),
                          fail_on_purpose=m in self.fail_once and self.attempts[m] == 1)
        self.state[m] = "running"
        self.running[task.task_id] = Running(task, worker, now)
        return task

    def complete(self, task_id: str, ok: bool, now: float, error: str = "", kind: str = "error") -> dict | None:
        """Apply a task's outcome. Returns what happened, or None for a stale task (already reassigned).
        `kind` of a failure: "error" (lean or the worker failed), "lost", "overdue", "corrupt"."""
        r = self.running.pop(task_id, None)
        if r is None:
            return None
        m = r.task.module
        ev = {"module": m, "task_id": task_id, "worker": r.worker, "attempt": r.task.attempt, "ok": ok}
        if ok:
            self.state[m] = "done"
            self._terminal += 1
            released = []
            for c in self.children[m]:
                self.indeg[c] -= 1
                if self.indeg[c] == 0 and self.state[c] == "waiting":
                    self._make_ready(c, now)
                    released.append(c)
            ev["released"] = len(released)
            return ev
        self.avoid[m].add(r.worker)
        self.errors[m].append(error[:500])
        if kind == "error":
            self.error_workers[m].add(r.worker)
        ev["kind"] = kind
        if kind == "corrupt":
            self.attempts[m] -= 1  # not this module's fault: an import's stored outputs were bad
        if len(self.error_workers[m]) >= self.source_failure_workers:
            cls = "source"  # the same module fails on different machines: not the environment
        elif self.attempts[m] > self.retries:
            cls = "retries exhausted"
        else:
            if self.indeg[m] > 0:  # an import was invalidated meanwhile: wait for its rebuild
                self.state[m] = "waiting"
            else:
                self._make_ready(m, now)
            ev["action"] = "retry"
            return ev
        self.state[m] = "failed"
        self.failure_class[m] = cls
        self._terminal += 1
        ev["action"] = "failed"
        ev["class"] = cls
        ev["skipped"] = self._skip_down(m)
        return ev

    def invalidate(self, m: str, now: float) -> bool:
        """A done module's stored outputs are unusable: build it again before its waiting importers."""
        if self.state.get(m) != "done":
            return False
        self.cached.discard(m)
        self._terminal -= 1
        for c in self.children[m]:
            if self.state[c] in ("waiting", "ready", "running"):
                self.indeg[c] += 1
                if self.state[c] != "running":  # a running importer waits once its attempt ends
                    self.state[c] = "waiting"  # (a stale heap entry of a ready importer is skipped)
        self._make_ready(m, now)
        return True

    def _skip_down(self, m: str) -> int:
        n = 0
        stack = list(self.children[m])
        while stack:
            c = stack.pop()
            if self.state[c] in ("waiting", "ready"):
                self.state[c] = "skipped"
                self._terminal += 1
                n += 1
                stack.extend(self.children[c])
        return n

    def expire(self, now: float) -> list[dict]:
        """Fail the tasks of lost workers and overdue tasks; returns the resulting events."""
        out = []
        for wid, info in self.workers.items():
            if info["alive"] and now - info["last_seen"] > self.lease_s:
                info["alive"] = False
                for tid in [t for t, r in self.running.items() if r.worker == wid and t not in self.confirming]:
                    ev = self.complete(tid, False, now, f"worker {wid} lost (no heartbeat for {self.lease_s:.0f} s)",
                                       kind="lost")
                    if ev:
                        ev["reason"] = "worker lost"
                        out.append(ev)
        for tid, r in list(self.running.items()):
            if tid not in self.confirming and now - r.started > r.task.timeout_s + self.overdue_grace_s:
                ev = self.complete(tid, False, now, f"task overdue ({now - r.started:.0f} s)", kind="overdue")
                if ev:
                    ev["reason"] = "overdue"
                    out.append(ev)
        return out

    # --- progress

    def done(self) -> bool:
        return self._terminal == len(self.state)

    def counts(self) -> dict[str, int]:
        c: dict[str, int] = {}
        for s in self.state.values():
            c[s] = c.get(s, 0) + 1
        return c


def lower_bound(graph: ProjectGraph, seconds: dict[str, float], slots: int) -> dict:
    """max(critical path, total work / slots) from measured per-module seconds."""
    fin: dict[str, float] = {}
    for m in graph.order:
        fin[m] = seconds.get(m, 0.0) + max((fin[u] for u in graph.modules[m].imports), default=0.0)
    cp = max(fin.values(), default=0.0)
    work = sum(seconds.get(m, 0.0) for m in graph.modules)
    per_slot = work / slots if slots else math.inf
    return {"critical_path_s": round(cp, 2), "work_s": round(work, 2), "slots": slots,
            "work_per_slot_s": round(per_slot, 2), "bound_s": round(max(cp, per_slot), 2),
            "max_speedup": round(work / cp, 2) if cp else 0.0}
