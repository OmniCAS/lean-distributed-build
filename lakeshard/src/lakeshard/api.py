"""Library entry points. The CLI is a thin layer over these; a service would call them too."""
from __future__ import annotations

import json
import os
import secrets
import subprocess
import sys
import time

from .assemble import assemble as _assemble
from .coordinator import BuildOptions, Coordinator, DynamicCoordinator, LocalProcessExecutor, WorkerSpec
from .plan import estimate_costs, load_history, make_plan
from .project import LakeProject, toolchain_bin
from .protocol import Plan
from .sim import simulate
from .verify import compare_builds, lake_no_build, leanchecker_all
from .worker import BUILT_RE, _seconds, lake_env, run_tracked


def _write_history(hist_in: dict, measured: dict, path: str) -> None:
    hist = dict(hist_in)  # measured per-module times, for the next run's estimates
    hist.update(measured)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(hist, fh, indent=0, sort_keys=True)


def analyze(project_dir: str, history: str | None = None, slots: list[int] | None = None) -> dict:
    proj = LakeProject.load(project_dir)
    g = proj.graph()
    depth = g.depth()
    clos = g.closure_sizes()
    costs = estimate_costs(g, load_history(history))
    width: dict[int, int] = {}
    for d in depth.values():
        width[d] = width.get(d, 0) + 1
    cs = sorted(clos.values())
    out = {"project": proj.package, "modules": len(g.modules), "targets": len(g.targets),
           "edges": sum(len(i.imports) for i in g.modules.values()),
           "lines": sum(i.lines for i in g.modules.values()),
           "external_imports": sorted({x for i in g.modules.values() for x in i.external})[:20],
           "depth": max(depth.values()), "max_width": max(width.values()),
           "closure_median": cs[len(cs) // 2], "closure_max": cs[-1],
           "cost_source": "history" if history else "estimate (lines)",
           "estimates": [simulate(g, costs, p) for p in (slots or [1, 4, 16, 64, 256])]}
    return out


def plan(project_dir: str, target_cost: float | None = None, shards: int | None = None,
         history: str | None = None) -> Plan:
    g = LakeProject.load(project_dir).graph()
    return make_plan(g, estimate_costs(g, load_history(history)), target_cost=target_cost, shards=shards)


def build(project_dir: str, work_dir: str, workers: int = 2, threads: int = 0, plan_obj: Plan | None = None,
          schedule: str = "dynamic", batch_cost: float | None = None, target_cost: float | None = None,
          shards: int | None = None, store: str | None = None, history: str | None = None, retries: int = 2,
          timeout_s: float = 7200.0, fail_once: set | None = None, toolchain: str | None = None) -> dict:
    """Build every module on `workers` local worker processes and record what happened.

    schedule="dynamic" forms batches at run time (cost budget `batch_cost`, default: total
    estimated work / (6 * workers)); schedule="static" builds the shards of a plan (`plan_obj`, or
    one made with `target_cost`/`shards`).
    """
    proj = LakeProject.load(project_dir)
    g = proj.graph()
    work_dir = os.path.abspath(work_dir)
    os.makedirs(work_dir, exist_ok=True)
    hist_out = os.path.join(work_dir, "history.json")  # never overwrite a history given as input
    hist_in = load_history(history) if history else load_history(hist_out)
    costs = estimate_costs(g, hist_in)
    store = store or os.path.join(work_dir, "store")
    opts = BuildOptions(proj.project_dir, proj.lakefile, toolchain_bin(proj.project_dir, toolchain), store,
                        retries=retries, timeout_s=timeout_s, fail_once=set(fail_once or ()))
    ws = [WorkerSpec(f"w{i}", threads) for i in range(workers)]
    ex = LocalProcessExecutor(work_dir)
    events = os.path.join(work_dir, "events.jsonl")
    if schedule == "static" or plan_obj is not None:
        if plan_obj is None:
            plan_obj = make_plan(g, costs, target_cost=target_cost, shards=shards or max(1, workers * 4))
        plan_obj.save(os.path.join(work_dir, "plan.json"))
        report = Coordinator(g, plan_obj, ex, ws, opts, events_path=events).run()
        report["plan"] = plan_obj.stats
    elif schedule == "dynamic":
        total = sum(costs.values())
        opts.batch_cost = batch_cost or min(600.0, max(10.0, total / (6 * max(1, workers))))
        report = DynamicCoordinator(g, costs, ex, ws, opts, events_path=events).run()
    else:
        raise ValueError(f"unknown schedule {schedule!r}")
    report["store"] = store
    report["backend"] = "lake"
    _write_history(hist_in, report.pop("module_seconds"), hist_out)
    report["history"] = hist_out
    with open(os.path.join(work_dir, "report.json"), "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=1)
    return report


def build_direct(project_dir: str, work_dir: str, workers: int = 4, slots: int = 3, threads: int = 0,
                 storage: str = "store", build_dir: str | None = None, store: str | None = None,
                 history: str | None = None, retries: int = 2, timeout_s: float = 7200.0,
                 fail_once: set | None = None, toolchain: str | None = None, listen: str = "127.0.0.1:0",
                 local_workers: int | None = None, token_file: str | None = None,
                 visibility_timeout_s: float = 0.0, heavy_cost: float | None = None, heavy_threads: int = 0,
                 lease_s: float = 60.0, heartbeat_s: float = 5.0, keep_setup: bool = False,
                 wait_timeout_s: float | None = None, python: str = sys.executable,
                 advertise_host: str | None = None, reuse: bool = True, check_fingerprint: bool = True,
                 targets: list[str] | None = None) -> dict:
    """Build every module with one `lean` process per module; workers pull tasks over HTTP.

    The coordinator runs in this process. `local_workers` (default `workers`) worker processes
    with `slots` slots each are started here; more can join from other machines with
    `lakeshard worker serve --coordinator URL --token-file FILE` (written to `<work>/coordinator.json`).
    storage="store" (default): every worker has its own build directory; outputs go through the
    artifact store: served by the coordinator over HTTP from `<work>/store` when `store` is None,
    a directory every worker can read and write when `store` is a path, or another store server
    when `store` is an `http://` URL.
    storage="shared": all workers write into `build_dir` (default `<work>/build`).
    With a store, every module's record is filed under its input key (`fingerprint.py`); modules
    whose key is already in the store are not built again (`reuse=False` rebuilds everything).
    Workers whose environment fingerprint differs from the coordinator's are refused.
    """
    from .fingerprint import fingerprint as env_fingerprint, module_keys
    from .store import LocalStore, open_store
    from .lakeenv import LakeWorkspace
    from .protocol import BuildConfig
    from .scheduler import ModuleScheduler
    from .service import BuildService

    proj = LakeProject.load(project_dir)
    g = proj.graph(targets)
    tb = toolchain_bin(proj.project_dir, toolchain)
    work_dir = os.path.abspath(work_dir)
    os.makedirs(work_dir, exist_ok=True)
    build_dir = os.path.abspath(build_dir or os.path.join(work_dir, "build"))
    store_root = None
    if storage == "store" and not store:
        store_root = os.path.join(work_dir, "store")  # served by the coordinator
    elif store and not store.startswith(("http://", "https://")):
        store = os.path.abspath(store)
    lws = LakeWorkspace(proj, build_dir, tb)
    lws.check_supported(g)  # refuse early
    lws.check_imports(g)
    for m in g.modules:
        if proj.lib_of(m) is None:
            raise ValueError(f"{m} is imported but is not a buildable module of any lean_lib")
    hist_out = os.path.join(work_dir, "history.json")
    hist_in = load_history(history) if history else load_history(hist_out)
    costs = estimate_costs(g, hist_in)
    t_prep = time.time()
    fp = env_fingerprint(proj, tb)
    keys = module_keys(g, proj, fp["sha256"])
    if token_file and os.path.exists(token_file):
        token = open(token_file, encoding="utf-8").read().strip()
    else:
        token_file = token_file or os.path.join(work_dir, "token")
        token = secrets.token_hex(16)
        fd = os.open(token_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w") as fh:
            fh.write(token + "\n")
    cached: set[str] = set()
    if storage == "store" and reuse:
        st = LocalStore(store_root) if store_root else open_store(store, token=token)
        recs = st.get_records(list(keys.values()))
        for m, k in keys.items():
            r = recs.get(k)
            if r is not None and any(f.path.endswith(".olean") for f in r.files) and \
                    (not isinstance(st, LocalStore) or st.check_record(r)):
                cached.add(m)
    prep_s = time.time() - t_prep
    run_id = time.strftime("%Y%m%d-%H%M%S") + "-" + secrets.token_hex(3)
    cfg = BuildConfig(run_id, proj.project_dir, tb, storage, build_dir if storage == "shared" else "",
                      (store or "") if storage == "store" else "", visibility_timeout_s, 0.5, heartbeat_s, keep_setup,
                      fingerprint=fp["sha256"] if check_fingerprint else "",
                      lakefile_toml=open(proj.lakefile, encoding="utf-8").read()
                      if os.path.basename(proj.lakefile) != "lakefile.toml" or
                      os.path.dirname(proj.lakefile) != proj.project_dir else "")
    sched = ModuleScheduler(g, costs, retries=retries, lease_s=lease_s, timeout_s=timeout_s,
                            heavy_cost=heavy_cost if heavy_cost is not None else float("inf"),
                            heavy_threads=heavy_threads, needs_closure=storage == "store", fail_once=fail_once,
                            keys=keys if storage == "store" else None, done=cached)
    host, _, port = listen.rpartition(":")
    svc = BuildService(g, sched, cfg, work_dir, token=token, host=host or "127.0.0.1", port=int(port or 0),
                       store_root=store_root, advertise_host=advertise_host,
                       fingerprint=fp if check_fingerprint else None, keys=keys)
    if store_root:
        cfg.store = svc.url  # workers reach the store through the coordinator
    svc.start()
    with open(os.path.join(work_dir, "coordinator.json"), "w", encoding="utf-8") as fh:
        json.dump({"url": svc.url, "token_file": token_file, "run_id": run_id, "project_dir": proj.project_dir,
                   "toolchain_bin": tb, "storage": storage, "build_dir": cfg.build_dir, "store": cfg.store}, fh,
                  indent=1)
    n_local = workers if local_workers is None else local_workers
    procs = []
    src = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env = dict(os.environ)
    env["PYTHONPATH"] = src + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    os.makedirs(os.path.join(work_dir, "workers"), exist_ok=True)
    finished = False
    try:
        for i in range(n_local):
            wid = f"w{i}"
            log = open(os.path.join(work_dir, "workers", f"{wid}.log"), "w", encoding="utf-8")
            procs.append(subprocess.Popen(
                [python, "-m", "lakeshard", "worker", "serve", "--coordinator", svc.url, "--id", wid,
                 "--slots", str(slots), "--threads", str(threads), "--token-file", token_file,
                 "--workspace", os.path.join(work_dir, "workers", wid)],
                stdout=log, stderr=subprocess.STDOUT, env=env))
            log.close()
        finished = _wait_build(svc, sched, procs, wait_timeout_s)
        deadline = time.time() + 60
        for p in procs:  # they exit once they see `shutdown`
            try:
                p.wait(timeout=max(0.1, deadline - time.time()))
            except subprocess.TimeoutExpired:
                p.kill()
    finally:
        for p in procs:
            if p.poll() is None:
                p.kill()
        report = svc.report_dict()
        report["run_records"] = os.path.join(work_dir, "modules.jsonl")
        report["run_record_count"] = svc.write_records(report["run_records"])
        report["manifest"] = os.path.join(work_dir, "manifest.json")
        svc.write_manifest(report["manifest"])
        report["fingerprint"] = fp["sha256"]
        report["prepare_s"] = round(prep_s, 2)
        svc.stop()
    report.update({"finished": finished, "url": svc.url, "local_workers": n_local, "slots_per_worker": slots,
                   "threads_per_lean": threads, "retries": retries, "run_id": run_id,
                   "worker_exit_codes": [p.returncode for p in procs], "store_root": store_root})
    _write_history(hist_in, report.pop("module_seconds"), hist_out)
    report["history"] = hist_out
    with open(os.path.join(work_dir, "report.json"), "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=1)
    return report


def _wait_build(svc, sched, procs: list, timeout_s: float | None) -> bool:
    """Wait for the build; give up early when every local worker has exited and no other worker
    is alive (otherwise a crashed set of workers would leave the coordinator waiting forever)."""
    deadline = None if timeout_s is None else time.time() + timeout_s
    dead_since = None
    while True:
        if svc.wait(1.0):
            return True
        if deadline is not None and time.time() > deadline:
            return False
        if procs and all(p.poll() is not None for p in procs):
            with svc.cond:
                others = any(w["alive"] for wid, w in sched.workers.items()
                             if time.time() - w["last_seen"] < sched.lease_s)
            dead_since = dead_since or time.time()
            if not others and time.time() - dead_since > 2.0:
                return False


def _git(args: list[str], cwd: str | None = None) -> str:
    out = subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {out.stderr.strip()[:500]}")
    return out.stdout.strip()


def fetch_source(repo: str, rev: str | None = None, checkout: str | None = None) -> tuple[str, dict]:
    """The project directory to build and a description of the source. A local directory without
    `rev`/`checkout` is used in place; otherwise `repo` (URL or path) is cloned into `checkout`
    (kept between runs) and `rev` checked out."""
    if os.path.isdir(repo) and not rev and not checkout:
        d = os.path.abspath(repo)
        info = {"repo": d, "path": d}
        if os.path.isdir(os.path.join(d, ".git")):
            info["commit"] = _git(["rev-parse", "HEAD"], d)
            info["dirty"] = bool(_git(["status", "--porcelain"], d))
        return d, info
    if not checkout:
        raise ValueError("a repository URL needs --checkout (where to clone it; same path on every worker)")
    checkout = os.path.abspath(checkout)
    if not os.path.isdir(os.path.join(checkout, ".git")):
        _git(["clone", "--quiet", repo, checkout])
    elif rev:
        _git(["fetch", "--quiet", "origin"], checkout)
    if rev:
        _git(["checkout", "--quiet", "--detach", rev], checkout)
    return checkout, {"repo": repo, "rev": rev, "commit": _git(["rev-parse", "HEAD"], checkout), "path": checkout}


def run(repo: str, work_dir: str, rev: str | None = None, checkout: str | None = None,
        cache_dir: str | None = None, deps_command: str | None = None, leanchecker_jobs: int = 0,
        toolchain: str | None = None, targets: list[str] | None = None, **build_kw) -> dict:
    """Repository in, build cache out: source, (dependencies), build, seal, (kernel check), pack."""
    from .cache import pack
    from .seal import seal

    work_dir = os.path.abspath(work_dir)
    os.makedirs(work_dir, exist_ok=True)
    phases: dict[str, float] = {}
    t = time.time()
    project_dir, source = fetch_source(repo, rev, checkout)
    phases["source_s"] = round(time.time() - t, 2)
    out: dict = {"source": source, "phases": phases}
    if deps_command:
        t = time.time()
        r = subprocess.run(deps_command, shell=True, cwd=project_dir, capture_output=True, text=True)
        phases["dependencies_s"] = round(time.time() - t, 2)
        if r.returncode != 0:
            return {**out, "ok": False, "phase": "dependencies", "error": (r.stdout + r.stderr)[-2000:]}
    if not os.path.exists(os.path.join(project_dir, "lakefile.toml")) and \
            os.path.exists(os.path.join(project_dir, "lakefile.lean")):
        from .project import translate
        t = time.time()
        out["translated_config"] = translate(project_dir, toolchain_bin(project_dir, toolchain))
        phases["translate_s"] = round(time.time() - t, 2)
    proj = LakeProject.load(project_dir)
    g = proj.graph(targets)
    tb = toolchain_bin(proj.project_dir, toolchain)
    t = time.time()
    rep = build_direct(project_dir, os.path.join(work_dir, "build"), toolchain=toolchain, targets=targets, **build_kw)
    phases["build_s"] = round(time.time() - t, 2)
    out["build"] = {k: rep.get(k) for k in ("ok", "wall_s", "modules", "from_store", "built", "status", "slots",
                                            "lower_bound", "failed_modules", "skipped_count", "refused_workers",
                                            "failures", "run_records", "fingerprint")}
    if not rep["ok"]:
        return {**out, "ok": False, "phase": "build"}
    store_dir = rep.get("store_root") or rep.get("store")
    if not store_dir or "://" in store_dir:
        return {**out, "ok": False, "phase": "seal", "error": "sealing needs the store as a directory"}
    t = time.time()
    sealed = os.path.join(work_dir, "sealed")
    out["seal"] = seal(project_dir, store_dir, sealed, tb, work_dir, manifest=rep["manifest"], targets=targets)
    phases["seal_s"] = round(time.time() - t, 2)
    if not out["seal"]["ok"]:
        return {**out, "ok": False, "phase": "seal"}
    if leanchecker_jobs:
        t = time.time()
        v = verify(project_dir, sealed, lake_check=False, leanchecker_jobs=leanchecker_jobs, prefix_modules="skip",
                   toolchain=toolchain, targets=targets)
        out["kernel"] = {k: v["leanchecker"][k] for k in ("ok", "runs", "ok_runs", "prefix_modules", "seconds")}
        phases["kernel_s"] = round(time.time() - t, 2)
        if not v["leanchecker"]["ok"]:
            return {**out, "ok": False, "phase": "kernel", "failed": v["leanchecker"]["failed"]}
    with open(rep["manifest"], encoding="utf-8") as fh:
        bman = json.load(fh)
    t = time.time()
    cache_dir = os.path.abspath(cache_dir or os.path.join(work_dir, "cache"))
    out["cache"] = pack(proj, g, sealed, cache_dir, bman["fingerprint"], bman["modules"], source)
    phases["pack_s"] = round(time.time() - t, 2)
    out["ok"] = True
    phases["total_s"] = round(sum(v for k, v in phases.items() if k != "total_s"), 2)
    with open(os.path.join(work_dir, "run.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
    return out


def seal_build(project_dir: str, store: str, manifest: str | None, build_dir: str, work_dir: str,
               toolchain: str | None = None) -> dict:
    from .seal import seal
    proj = LakeProject.load(project_dir)
    os.makedirs(work_dir, exist_ok=True)
    return seal(proj.project_dir, store, build_dir, toolchain_bin(proj.project_dir, toolchain), work_dir,
                manifest=manifest)


def restore(cache_dir: str, checkout: str, check: bool = True, force: bool = False,
            toolchain: str | None = None) -> dict:
    from .cache import restore as _restore
    return _restore(cache_dir, checkout, toolchain_bin(os.path.abspath(checkout), toolchain), check, force)


def check_setup(project_dir: str, lake_build_dir: str, toolchain: str | None = None, limit: int = 20,
                targets: list[str] | None = None) -> dict:
    """Compare the setup files, command lines and LEAN_PATH of the direct backend with a real Lake build."""
    from .lakeenv import LakeWorkspace, compare_with_lake

    proj = LakeProject.load(project_dir)
    g = proj.graph(targets)
    ws = LakeWorkspace(proj, lake_build_dir, toolchain_bin(proj.project_dir, toolchain))
    out = compare_with_lake(ws, g.order, os.path.abspath(lake_build_dir), limit=limit)
    out["modules"] = len(g.modules)
    out["lean_version"] = ".".join(map(str, ws.version))
    return out


def assemble(project_dir: str, store: str, dest_build_dir: str, manifest: str | None = None,
             token: str | None = None, targets: list[str] | None = None) -> dict:
    """Copy every module's outputs from the store into one build directory. With the `manifest.json`
    of a direct build, records are looked up by input key; without it, by module name."""
    g = LakeProject.load(project_dir).graph(targets)
    idents = None
    if manifest:
        with open(manifest, encoding="utf-8") as fh:
            idents = json.load(fh)["modules"]
    return _assemble(g, store, dest_build_dir, idents=idents, token=token)


def verify(project_dir: str, build_dir: str, reference: str | None = None, rehash: bool = True,
           leanchecker_jobs: int = 0, fresh_root: str | None = None, toolchain: str | None = None,
           prefix_modules: str = "run", lake_check: bool = True, targets: list[str] | None = None) -> dict:
    """`lake_check=False` skips `lake build --no-build` (the direct backend writes no Lake traces)."""
    proj = LakeProject.load(project_dir)
    g = proj.graph(targets)
    tb = toolchain_bin(proj.project_dir, toolchain)
    out = {"lake_no_build": lake_no_build(proj, build_dir, tb, rehash=rehash, targets=targets)} if lake_check else {}
    if reference:
        out["compare"] = compare_builds(g, reference, build_dir)
    if leanchecker_jobs or fresh_root:
        out["leanchecker"] = leanchecker_all(proj, g, build_dir, tb, jobs=max(1, leanchecker_jobs),
                                             fresh_root=fresh_root, prefix_modules=prefix_modules)
    out["ok"] = all(v.get("ok", True) for v in out.values() if isinstance(v, dict))
    return out


def reference_build(project_dir: str, build_dir: str, threads: int = 0, toolchain: str | None = None,
                    targets: list[str] | None = None) -> dict:
    """A plain single-machine `lake build` into `build_dir` (for comparison and timing)."""
    proj = LakeProject.load(project_dir)
    tb = toolchain_bin(proj.project_dir, toolchain)
    os.makedirs(build_dir, exist_ok=True)
    cfg = os.path.abspath(build_dir).rstrip("/") + ".lakefile.toml"
    with open(cfg, "w", encoding="utf-8") as fh:
        fh.write(proj.worker_lakefile(build_dir))
    t0 = time.time()
    code, out, wall, cpu, rss, _ = run_tracked(
        [os.path.join(tb, "lake"), "-d", proj.project_dir, "-f", cfg, "--no-ansi", "build"] + list(targets or []),
        lake_env(tb, threads), 24 * 3600)
    secs = {}
    for mm in BUILT_RE.finditer(out):
        sec = _seconds(mm.group(2), mm.group(3))
        if sec is not None:
            secs[mm.group(1)] = sec
    base = os.path.abspath(build_dir).rstrip("/")
    hist = base + ".history.json"
    with open(hist, "w", encoding="utf-8") as fh:
        json.dump(secs, fh, indent=0, sort_keys=True)
    with open(base + ".log", "w", encoding="utf-8") as fh:  # full Lake output, for later analysis
        fh.write(out)
    return {"ok": code == 0, "exit": code, "wall_s": round(wall, 2), "cpu_s": round(cpu, 2),
            "max_rss_bytes": rss, "threads": threads, "build_dir": os.path.abspath(build_dir),
            "modules_built": len(secs), "module_seconds_sum": round(sum(secs.values()), 2), "history": hist,
            "output_tail": "\n".join(out.strip().splitlines()[-3:]), "started": t0}
