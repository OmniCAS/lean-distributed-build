"""Command line: `lakeshard <command> ...` (see `lakeshard --help`)."""
from __future__ import annotations

import argparse
import json
import os
import sys

from . import __version__, api
from .protocol import Plan


def _print(obj) -> None:
    print(json.dumps(obj, indent=1, ensure_ascii=False) if not isinstance(obj, str) else obj)


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if argv[:1] == ["forward"]:  # control experiment: stock Lake with forwarded lean processes
        from .forward import main as forward_main
        return forward_main(argv[1:])
    ap = argparse.ArgumentParser(prog="lakeshard", description=__doc__)
    ap.add_argument("--version", action="version", version=f"lakeshard {__version__}")
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("analyze", help="import graph statistics and time estimates")
    a.add_argument("project")
    a.add_argument("--history", help="JSON of measured seconds per module")
    a.add_argument("--slots", default="1,4,16,64,256")

    p = sub.add_parser("plan", help="split the project into shards")
    p.add_argument("project")
    p.add_argument("--target-cost", type=float, help="seconds of work per shard")
    p.add_argument("--shards", type=int, help="number of shards (alternative to --target-cost)")
    p.add_argument("--history")
    p.add_argument("--out", required=True)

    b = sub.add_parser("build", help="build the project on several workers")
    b.add_argument("project")
    b.add_argument("--target", action="append", default=[], help="only these modules (and their imports)")
    b.add_argument("--work", required=True, help="work directory (plan, store, workers, logs)")
    b.add_argument("--backend", choices=["lake", "lean"], default="lake",
                   help="lake: batches of modules per `lake build` (default); lean: one `lean` per module")
    b.add_argument("--workers", type=int, default=2, help="local worker processes")
    b.add_argument("--threads", type=int, default=0,
                   help="LEAN_NUM_THREADS (lake: per worker, also Lake's job count; lean: per lean process)")
    b.add_argument("--slots", type=int, default=3, help="lean: concurrent lean processes per worker")
    b.add_argument("--storage", choices=["store", "shared"], default="store",
                   help="lean: per-worker build directories + artifact store (default), or one shared build directory")
    b.add_argument("--build-dir", help="lean, shared storage: the shared build directory (default <work>/build)")
    b.add_argument("--listen", default="127.0.0.1:0", help="lean: coordinator address HOST:PORT (0 = any port)")
    b.add_argument("--local-workers", type=int, help="lean: workers started here (default --workers; 0 = remote only)")
    b.add_argument("--token-file", help="lean: shared secret for workers (default: a new one in <work>/token)")
    b.add_argument("--visibility-timeout", type=float, default=0.0,
                   help="lean: seconds to wait for outputs written elsewhere to appear (NFS)")
    b.add_argument("--heavy-cost", type=float, help="lean: modules estimated at >= this many seconds ...")
    b.add_argument("--heavy-threads", type=int, default=0, help="... get this many Lean threads")
    b.add_argument("--lease", type=float, default=60.0, help="lean: seconds without heartbeat before a worker is lost")
    b.add_argument("--keep-setup", action="store_true", help="lean: keep each module's .setup.json (as Lake does)")
    b.add_argument("--wait-timeout", type=float, help="lean: give up after this many seconds")
    b.add_argument("--priority", choices=["bl", "fifo", "structure"], default="bl",
                   help="lean: ready modules by longest remaining path (measured or estimated seconds), "
                        "first ready first, or longest remaining path counted in modules")
    b.add_argument("--assign", help="lean: JSON module -> worker id; each module only on its worker (static split)")
    b.add_argument("--fetch-delay", type=float, default=0.0,
                   help="lean, experiments: seconds added to every task that fetches imports")
    b.add_argument("--schedule", choices=["dynamic", "static"], default="dynamic")
    b.add_argument("--batch-cost", type=float, help="dynamic: estimated seconds of work per batch")
    b.add_argument("--plan", help="static: use this plan.json instead of planning")
    b.add_argument("--target-cost", type=float)
    b.add_argument("--shards", type=int)
    b.add_argument("--store", help="artifact store: a directory, or http://HOST:PORT of `lakeshard store serve` "
                                   "(default: <work>/store; for --backend lean served by the coordinator over HTTP)")
    b.add_argument("--advertise-host", help="lean: host name or address workers use to reach the coordinator")
    b.add_argument("--history")
    b.add_argument("--retries", type=int, default=2)
    b.add_argument("--timeout", type=float, default=7200.0, help="seconds per shard job")
    b.add_argument("--fail-once", action="append", default=[],
                   help="test: shard/batch id (lake) or module (lean) whose first attempt fails")
    b.add_argument("--toolchain-bin")

    rn = sub.add_parser("run", help="repository in, build cache out (direct backend, seal, pack)")
    rn.add_argument("repo", help="a project directory, or a Git URL/path with --checkout")
    rn.add_argument("--target", action="append", default=[], help="only these modules (and their imports)")
    rn.add_argument("--work", required=True)
    rn.add_argument("--rev", help="commit, tag or branch to build")
    rn.add_argument("--checkout", help="where to clone the repository (same absolute path on every worker)")
    rn.add_argument("--cache", help="cache directory to write (default <work>/cache)")
    rn.add_argument("--deps-command", help="shell command run in the project first, e.g. 'lake exe cache get'")
    rn.add_argument("--leanchecker-jobs", type=int, default=0, help="replay every module in the kernel, N at a time")
    rn.add_argument("--workers", type=int, default=4)
    rn.add_argument("--slots", type=int, default=3)
    rn.add_argument("--threads", type=int, default=0)
    rn.add_argument("--store", help="artifact store directory kept between runs (default <work>/build/store)")
    rn.add_argument("--listen", default="127.0.0.1:0")
    rn.add_argument("--advertise-host")
    rn.add_argument("--local-workers", type=int)
    rn.add_argument("--retries", type=int, default=2)
    rn.add_argument("--history")
    rn.add_argument("--no-reuse", action="store_true", help="rebuild modules already in the store")
    rn.add_argument("--toolchain-bin")

    tr = sub.add_parser("translate", help="translate a lakefile.lean into .lake/lakeshard/lakefile.toml (runs Lake)")
    tr.add_argument("project")
    tr.add_argument("--toolchain-bin")

    asg = sub.add_parser("assign", help="a static split of the modules over workers (experiments)")
    asg.add_argument("project")
    asg.add_argument("--method", choices=["namespace", "chains"], required=True)
    asg.add_argument("--workers", required=True, help="comma-separated worker ids")
    asg.add_argument("--slots", type=int, default=16, help="chains: slots per worker")
    asg.add_argument("--depth", type=int, default=2, help="namespace: name components per block")
    asg.add_argument("--transfer", type=float, default=0.5, help="chains: assumed seconds per cross-worker import")
    asg.add_argument("--history")
    asg.add_argument("--target", action="append", default=[])
    asg.add_argument("--out", required=True)

    se = sub.add_parser("seal", help="stock lake build that takes every module's outputs from a store")
    se.add_argument("project")
    se.add_argument("--store", required=True, help="store directory")
    se.add_argument("--manifest", help="manifest.json of a direct build")
    se.add_argument("--build-dir", required=True)
    se.add_argument("--work", required=True)
    se.add_argument("--toolchain-bin")

    rs = sub.add_parser("restore", help="put a cache into a checkout so that stock lake build is up to date")
    rs.add_argument("cache")
    rs.add_argument("--checkout", required=True)
    rs.add_argument("--no-check", action="store_true", help="skip `lake build --no-build` afterwards")
    rs.add_argument("--force", action="store_true", help="restore although the environment differs")
    rs.add_argument("--toolchain-bin")

    s = sub.add_parser("assemble", help="put every module's outputs from the store into one build dir")
    s.add_argument("project")
    s.add_argument("--target", action="append", default=[], help="only these modules (and their imports)")
    s.add_argument("--store", required=True)
    s.add_argument("--dest", required=True)
    s.add_argument("--manifest", help="manifest.json of a direct build (records by input key)")
    s.add_argument("--token-file")

    v = sub.add_parser("verify", help="check an assembled build")
    v.add_argument("project")
    v.add_argument("--target", action="append", default=[], help="only these modules (and their imports)")
    v.add_argument("--build-dir", required=True)
    v.add_argument("--reference", help="build dir of a plain lake build to compare with")
    v.add_argument("--no-rehash", action="store_true")
    v.add_argument("--leanchecker-jobs", type=int, default=0)
    v.add_argument("--fresh-root", help="also run leanchecker --fresh on this module")
    v.add_argument("--prefix-modules", choices=["run", "skip"], default="run",
                   help="modules that are also a name prefix of others (leanchecker re-checks their subtree)")
    v.add_argument("--no-lake-check", action="store_true",
                   help="skip `lake build --no-build` (direct-backend outputs carry no Lake traces)")
    v.add_argument("--toolchain-bin")

    c = sub.add_parser("check-setup", help="compare the direct backend's lean invocations with a real Lake build")
    c.add_argument("project")
    c.add_argument("--target", action="append", default=[], help="only these modules (and their imports)")
    c.add_argument("--lake-build-dir", required=True, help="build directory of a plain `lake build`")
    c.add_argument("--limit", type=int, default=20)
    c.add_argument("--toolchain-bin")

    r = sub.add_parser("reference", help="plain single-machine lake build into a build dir (timed)")
    r.add_argument("project")
    r.add_argument("--target", action="append", default=[], help="only these modules (and their imports)")
    r.add_argument("--build-dir", required=True)
    r.add_argument("--threads", type=int, default=0)
    r.add_argument("--toolchain-bin")

    y = sub.add_parser("synth", help="write a synthetic Lake project")
    y.add_argument("out")
    y.add_argument("--modules", type=int, default=100)
    y.add_argument("--max-imports", type=int, default=4)
    y.add_argument("--locality", type=int, default=30)
    y.add_argument("--work", type=int, default=3, help="small theorems per module")
    y.add_argument("--toolchain", default="leanprover/lean4:v4.33.1")
    y.add_argument("--random-state", type=int, default=1)

    st = sub.add_parser("store", help="artifact store server")
    stsub = st.add_subparsers(dest="scmd", required=True)
    sts = stsub.add_parser("serve", help="serve a store directory over HTTP")
    sts.add_argument("--root", required=True)
    sts.add_argument("--listen", default="127.0.0.1:0", help="HOST:PORT")
    sts.add_argument("--token-file", help="require this bearer token")

    w = sub.add_parser("worker", help="worker side (used by executors)")
    wsub = w.add_subparsers(dest="wcmd", required=True)
    wr = wsub.add_parser("run", help="run one shard job file")
    wr.add_argument("--job", required=True)
    wr.add_argument("--result", required=True)
    wr.add_argument("--workspace", required=True)
    wr.add_argument("--worker-id", required=True)
    ws = wsub.add_parser("serve", help="resident worker of the lean backend: pull tasks from a coordinator")
    ws.add_argument("--coordinator", required=True, help="http://HOST:PORT")
    ws.add_argument("--id", required=True, help="worker name (unique per build)")
    ws.add_argument("--slots", type=int, default=1)
    ws.add_argument("--threads", type=int, default=0, help="LEAN_NUM_THREADS per lean process (0 = default)")
    ws.add_argument("--workspace", required=True, help="local directory for this worker")
    ws.add_argument("--token-file", help="file with the coordinator's token (or env LAKESHARD_TOKEN)")
    ws.add_argument("--give-up-s", type=float, default=300.0, help="exit when the coordinator is unreachable this long")

    args = ap.parse_args(argv)
    if args.cmd == "analyze":
        _print(api.analyze(args.project, args.history, [int(x) for x in args.slots.split(",")]))
    elif args.cmd == "plan":
        pl = api.plan(args.project, args.target_cost, args.shards, args.history)
        pl.save(args.out)
        _print(pl.stats)
    elif args.cmd == "build" and args.backend == "lean":
        rep = api.build_direct(args.project, args.work, workers=args.workers, slots=args.slots, threads=args.threads,
                               storage=args.storage, build_dir=args.build_dir, store=args.store,
                               history=args.history, retries=args.retries, timeout_s=args.timeout,
                               fail_once=set(args.fail_once), toolchain=args.toolchain_bin, listen=args.listen,
                               local_workers=args.local_workers, token_file=args.token_file,
                               visibility_timeout_s=args.visibility_timeout, heavy_cost=args.heavy_cost,
                               heavy_threads=args.heavy_threads, lease_s=args.lease, keep_setup=args.keep_setup,
                               wait_timeout_s=args.wait_timeout, advertise_host=args.advertise_host,
                               targets=args.target or None, priority=args.priority,
                               assign=json.load(open(args.assign)) if args.assign else None,
                               fetch_delay_s=args.fetch_delay)
        _print({k: v for k, v in rep.items() if k not in ("workers",)})
        return 0 if rep["ok"] else 1
    elif args.cmd == "run":
        res = api.run(args.repo, args.work, rev=args.rev, checkout=args.checkout, cache_dir=args.cache,
                      deps_command=args.deps_command, leanchecker_jobs=args.leanchecker_jobs,
                      toolchain=args.toolchain_bin, workers=args.workers, slots=args.slots, threads=args.threads,
                      store=args.store, listen=args.listen, advertise_host=args.advertise_host,
                      local_workers=args.local_workers, retries=args.retries, history=args.history,
                      reuse=not args.no_reuse, targets=args.target or None)
        _print(res)
        return 0 if res["ok"] else 1
    elif args.cmd == "assign":
        from .plan import assign_by_chains, assign_by_namespace, assignment_stats, estimate_costs, load_history
        from .project import LakeProject
        g = LakeProject.load(args.project).graph(args.target or None)
        costs = estimate_costs(g, load_history(args.history))
        ws = args.workers.split(",")
        a = (assign_by_namespace(g, costs, ws, args.depth) if args.method == "namespace"
             else assign_by_chains(g, costs, ws, args.slots, args.transfer))
        with open(args.out, "w") as fh:
            json.dump(a, fh)
        _print({"method": args.method, **assignment_stats(g, costs, a)})
    elif args.cmd == "translate":
        from .project import toolchain_bin, translate
        _print({"config": translate(args.project, toolchain_bin(os.path.abspath(args.project), args.toolchain_bin))})
    elif args.cmd == "seal":
        res = api.seal_build(args.project, args.store, args.manifest, args.build_dir, args.work, args.toolchain_bin)
        _print(res)
        return 0 if res["ok"] else 1
    elif args.cmd == "restore":
        res = api.restore(args.cache, args.checkout, check=not args.no_check, force=args.force,
                          toolchain=args.toolchain_bin)
        _print(res)
        return 0 if res["ok"] else 1
    elif args.cmd == "check-setup":
        res = api.check_setup(args.project, args.lake_build_dir, args.toolchain_bin, args.limit, args.target or None)
        _print(res)
        return 0 if res["ok"] else 1
    elif args.cmd == "build":
        rep = api.build(args.project, args.work, workers=args.workers, threads=args.threads,
                        plan_obj=Plan.load(args.plan) if args.plan else None, schedule=args.schedule,
                        batch_cost=args.batch_cost, target_cost=args.target_cost,
                        shards=args.shards, store=args.store, history=args.history, retries=args.retries,
                        timeout_s=args.timeout, fail_once=set(args.fail_once), toolchain=args.toolchain_bin)
        _print({k: v for k, v in rep.items() if k not in ("per_worker",)})
        return 0 if rep["ok"] else 1
    elif args.cmd == "assemble":
        from .pullworker import read_token
        res = api.assemble(args.project, args.store, args.dest, args.manifest, read_token(args.token_file),
                           args.target or None)
        _print(res)
        return 0 if res["ok"] else 1
    elif args.cmd == "verify":
        res = api.verify(args.project, args.build_dir, args.reference, not args.no_rehash,
                         args.leanchecker_jobs, args.fresh_root, args.toolchain_bin, args.prefix_modules,
                         lake_check=not args.no_lake_check, targets=args.target or None)
        _print(res)
        return 0 if res["ok"] else 1
    elif args.cmd == "reference":
        res = api.reference_build(args.project, args.build_dir, args.threads, args.toolchain_bin, args.target or None)
        _print(res)
        return 0 if res["ok"] else 1
    elif args.cmd == "synth":
        from .synth import random_dag, write_project
        imps = random_dag(args.modules, args.max_imports, args.locality, random_state=args.random_state)
        _print(write_project(args.out, imps, toolchain=args.toolchain, work=[args.work] * args.modules))
    elif args.cmd == "worker" and args.wcmd == "run":
        from .worker import main_run
        return main_run(args.job, args.result, args.workspace, args.worker_id)
    elif args.cmd == "store" and args.scmd == "serve":
        from .httpstore import serve_store
        from .pullworker import read_token
        host, _, port = args.listen.rpartition(":")
        srv = serve_store(args.root, host or "127.0.0.1", int(port or 0), token=read_token(args.token_file))
        print(json.dumps({"url": f"http://{srv.server_address[0]}:{srv.server_address[1]}", "root": args.root}),
              flush=True)
        try:
            srv.serve_forever()
        except KeyboardInterrupt:
            pass
        return 0
    elif args.cmd == "worker" and args.wcmd == "serve":
        from .pullworker import PullWorker, read_token
        return PullWorker(args.coordinator, args.id, args.slots, args.threads, args.workspace,
                          token=read_token(args.token_file), give_up_s=args.give_up_s).run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
