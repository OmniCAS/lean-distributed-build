# lakeshard

Split a Lean 4 / Lake project along its import graph, build the pieces on several workers, move
the build outputs between them through a content-addressed store, then assemble one build
directory and check it.

The aim is to make very large Lean repositories (hundreds of thousands of modules) buildable in
the time of their critical path instead of the time one machine needs for all the work.

Status: 0.2. Two backends: batches of modules built by stock `lake build` (0.1), and one `lean`
process per module with Lake's exact arguments (0.2): resident workers pull tasks from a small
HTTP coordinator, each keeps its own build directory, and outputs move through an artifact store
that the coordinator serves over HTTP (or a directory, or a separate store server). Both are
tested on one machine (see "Stages" below); the worker command for other machines is in "Remote
workers"; runs on real separate machines have not been done yet.

## Install

```bash
uv venv .venv && uv pip install --python .venv/bin/python -e ".[dev]"
```

No runtime dependencies beyond the Python standard library (3.11+). Building needs the project's
Lean toolchain installed through elan.

## Commands

```bash
lakeshard analyze PROJECT                      # modules, edges, depth, critical-path estimates
lakeshard plan PROJECT --shards 32 --out plan.json
lakeshard reference PROJECT --build-dir REF    # plain single-machine lake build, timed
lakeshard build PROJECT --work WORK --workers 4 --threads 3          # Lake batch backend
lakeshard build PROJECT --work WORK --backend lean --workers 4 --slots 3 --threads 3   # direct backend
lakeshard worker serve --coordinator URL --id NAME --slots 3 --threads 3 --workspace DIR --token-file F
lakeshard store serve --root DIR --listen HOST:PORT --token-file F   # a store server of its own
lakeshard run REPO --work WORK [--rev R --checkout DIR] [--cache OUT] [--deps-command CMD]   # repository in, cache out
lakeshard restore CACHE --checkout DIR          # put a cache into a checkout; stock lake build is then up to date
lakeshard seal PROJECT --store DIR --manifest M --build-dir OUT --work W   # stock Lake writes the traces
lakeshard check-setup PROJECT --lake-build-dir REF   # direct backend's lean calls vs a real lake build
lakeshard assemble PROJECT --store WORK/store --dest OUT
lakeshard verify PROJECT --build-dir OUT --reference REF --leanchecker-jobs 8 [--prefix-modules skip]
lakeshard synth OUT --modules 200              # synthetic project for tests and benchmarks
```

`build` options (Lake batch backend, the default): `--schedule dynamic|static`, `--batch-cost SECONDS`
(dynamic), `--plan` / `--shards` / `--target-cost` (static), `--retries`, `--timeout`, `--store DIR`,
`--fail-once ID` (test hook: the first attempt of that batch or shard fails).

`build --backend lean` options: `--workers N` (started on this machine), `--slots K` (`lean`
processes per worker), `--threads T` (`LEAN_NUM_THREADS` per `lean`), `--storage store|shared`
(default `store`), `--store DIR|http://HOST:PORT` (default: `WORK/store`, served by the coordinator
over HTTP), `--build-dir DIR` (`shared` only, default `WORK/build`), `--listen HOST:PORT`,
`--advertise-host NAME` (how workers reach the coordinator), `--local-workers N` (0: only remote
workers), `--token-file F`, `--visibility-timeout S` (`shared` on NFS),
`--heavy-cost S --heavy-threads T` (more threads for modules estimated at >= S seconds; not tuned),
`--lease S`, `--keep-setup`, `--retries`, `--timeout`, `--history`, `--fail-once MODULE`.

All commands print JSON. `build` writes `WORK/report.json`, `WORK/events.jsonl` (one line per
job), `WORK/history.json` (measured seconds per module, used for later cost estimates) and keeps
each worker's workspace under `WORK/workers/`.

## How it works

1. **Graph.** `lakefile.toml` is read with `tomllib`; the modules of the default targets and their
   imports are found by reading only the import headers of the source files. Nothing from the
   project is executed. (`lakefile.lean` is not supported: convert it with
   `lake translate-config toml`.)
2. **Costs.** Measured seconds per module when known (`history.json`), otherwise
   `2 s + 0.04 s/line + 0.5 ms per imported project module`.
3. **Schedule.**
   - `dynamic` (default): when a worker is free, the coordinator takes the ready module with the
     longest remaining path (preferring modules whose imports the worker already holds) and
     extends the batch along its import chain, then with other ready modules, up to a cost budget.
     After a failed batch its modules are retried one by one on another worker.
   - `static`: a precomputed plan. Modules are visited in topological order and join the shard of
     their imports while that keeps the shard under the target cost and cannot create a cycle
     between shards (shard ancestry is tracked exactly with bitsets). `check_plan` verifies the
     partition and acyclicity.
4. **Worker.** Each worker has a persistent workspace with its own build directory. For a job it
   writes a copy of the project's `lakefile.toml` with `buildDir` set to that directory, fetches
   the outputs of every module the batch imports (`.olean`, `.ilean`, `.c`, Lake's `.trace` and
   `.hash` files) from the store, checking their sha256, runs stock `lake build +M ...` for the
   batch, and uploads the new outputs. Lake accepts the fetched outputs as up to date because the
   traces depend on content hashes, not on paths; the worker fails the job if Lake rebuilds
   anything outside the batch.
5. **Store.** Objects named by sha256 plus one record per module (`ModuleRecord`: file paths and
   hashes). `LocalStore` is a directory; other stores implement the same five methods.
6. **Assemble and verify.** All records are copied into one build directory. `verify` runs
   `lake build --no-build --rehash` against it, compares `.olean`/`.ilean`/`.c` byte for byte with a
   reference build, and replays every module through the kernel with `leanchecker` (optionally
   `leanchecker --fresh` on a root module).

### Direct `lean` backend (`--backend lean`)

One task = one module. The worker writes the module's `--setup` JSON and runs
`lean <weakLeanArgs> <moreLeanArgs> <absolute source> -o … -i … -c … --setup … --json` with
`LEAN_PATH` set, exactly as Lake 4.33-4.35 does (`lakeshard/lakeenv.py` follows Lake's
`fetchTransImportArts`, `computeExportInfo`, `mkModuleSetup`, `compileLeanModule` and
`Workspace.leanPath`): module name, package name, `isModule`, the module's library options
(build type, package and library `leanOptions`), `importArts` (every transitive workspace import
for a plain file; `public`/`meta`/`all` edges for `module` files; dependency modules such as
Mathlib's with their `.olean`, `.olean.server`, `.olean.private`, `.ir.sig`, `.ir`), and
`LEAN_PATH` (dependencies in reverse manifest order, then the project). `lakeshard check-setup`
compares all of it with the `.setup.json` files and `.trace` command lines of a real `lake build`.
Only `lakefile.toml` projects; dependencies must already be built (e.g. `lake exe cache get`);
`precompileModules`, `dynlibs`, `plugins`, `needs`/`extraDepTargets`, other target kinds and Lake's
artifact cache are refused or not reproduced. No Lake `.trace`/`.hash` files are written, so Lake
does not yet accept these outputs as up to date (milestone M3).

- **Storage.** `store` (default, the cross-machine form): every worker has its own local build
  directory. Before `lean` it fetches the outputs of the module's import closure that it does not
  have yet (sha256 checked); afterwards it uploads the module's outputs and record. The store is
  an interface (`ArtifactStore`) with two implementations: a directory (`LocalStore`, e.g. a disk
  every worker mounts) and HTTP (`HttpStore`, `httpstore.py`), served by default by the
  coordinator itself from `WORK/store` under `/v1/store/...`, or by `lakeshard store serve`. The
  server verifies each upload against its name and never rewrites an object. Workers only
  connect outwards (to the coordinator and the store); nothing connects to a worker.
  `shared` (the S1 form, kept as a control): all workers read and write one build directory.
  In both, `lean` writes into a private temporary directory and the outputs are then renamed
  into place, the `.olean` last; the module's stale Lake metadata (`.trace`, `*.hash`) is removed.
  The coordinator releases importers only after it sees the record in the store (or, `shared`,
  the reported files with the reported sizes; `--visibility-timeout S` lets workers and the
  coordinator re-read directories on NFS and wait up to S seconds).
- **Scheduling** (`lakeshard/scheduler.py`, a pure state machine): ready modules by longest
  remaining path (measured seconds from `--history`, else the line-count estimate); a failed
  module is retried on a worker that has not failed it (when one is alive), and after `--retries`
  retries everything importing it is skipped; a worker not heard from for `--lease` seconds is
  presumed lost and its tasks go elsewhere; a worker still running a reassigned task is told to
  cancel it; late results of reassigned tasks are ignored.
- **Workers** (`lakeshard/pullworker.py`) are resident processes: register, long-poll `claim` for
  as many tasks as they have free slots, `report` each result, `heartbeat` every 5 s, over
  persistent HTTP connections (one per thread). A build whose local workers have all exited is
  stopped instead of waiting forever.
- **Transport: HTTP**, standard library only, JSON messages from `lakeshard.protocol`
  (`BuildConfig`, `ModuleTask`, `ModuleResult`), a random bearer token (`WORK/token`). Chosen
  over task files in the shared directory because every link of an import chain waits for a
  dispatch decision: a long-polled request delivers it in milliseconds from one process that
  holds all state, whereas files on NFS need cross-client claiming by rename and directory
  polling, and NFS attribute caching (3-60 s) would add that delay to every dependency (the
  simulations show 5-30 s per dependency doubling the critical path of a deep archive). If
  sandboxes share a directory but cannot reach each other over TCP, a file transport can
  implement the same four calls.
- **Report** (`WORK/report.json`): wall time, per-module `lean` seconds (also `WORK/history.json`),
  CPU, largest RSS, waits, failures, store traffic, and the lower bound max(critical path, total
  work / slots) with the ratio wall / bound. `WORK/events.jsonl`: one line per dispatch, result
  and expiry. `WORK/modules.jsonl`: one run record per attempt (ready, dispatch, start, `lean`,
  end, report and release times on the coordinator's clock; fetch, compile and upload durations;
  CPU; peak memory; host; threads), format in `docs/run-records.md`.

### Repository in, cache out (`lakeshard run`, `lakeshard restore`)

`run` goes through: source (a directory used in place, or a Git URL or path cloned into
`--checkout` at `--rev`), an optional dependency step (`--deps-command`, e.g. `lake exe cache get`),
the environment fingerprint and module keys, the direct build (reusing everything already in the
store), the seal, an optional kernel check (`--leanchecker-jobs N`), and packing. It writes
`WORK/run.json` with the time of every phase.

- **Keys and reuse** (`fingerprint.py`). The fingerprint covers the toolchain (`lean-toolchain`,
  `lean --githash`), platform, project path, Lake configuration, `lake-manifest.json` and a digest
  of each dependency's build (the `depHash`/output hashes in its `.trace` files). A module's key is
  sha256 over the fingerprint, its name, the sha256 of its source, its library options and
  arguments, and the keys of its project imports. The store files records under keys; a build
  first looks up every key and builds only the missing modules, so a rerun after a crash resumes,
  an edited file rebuilds exactly its downstream modules, and identical inputs are never built
  twice.
- **Seal** (`seal.py`, `sealshim.py`). The direct backend writes no Lake traces, and Lake rebuilds
  a module without a matching trace (`lake build --old` accepts outputs by modification time but
  writes no traces). So the seal runs stock `lake build` with `LAKE_OVERRIDE_LEAN=true` and
  `LEAN_SYSROOT` pointing to a copy of the toolchain directory made of symbolic links whose
  `bin/lean` is a shim: for each module Lake asks to compile, the shim copies the stored outputs
  (sha256 checked) into place; modules missing from the store go to the real `lean`. Lake computes
  and writes its own `.trace` and `.hash` files; their input hashes equal those of a plain
  `lake build` (checked on Lean 4.33.1 and 4.35.0, `module` files included), and
  `lake build --no-build` must then pass. Sealing runs Lake on the project configuration: run it
  where the project is trusted.
- **Cache** (`cache.py`): `manifest.json` (source, package, toolchain, fingerprint, module keys,
  every file with its sha256) and `objects/` named by sha256: all outputs of the sealed build
  directory, Lake's traces and hash files included (the command lines Lake logs in traces, which
  carry the build machine's paths, are removed).
- **Restore** refuses a checkout whose toolchain, platform, manifest or dependency builds differ
  (`--force` to override), checks the sha256 of every file, copies the files into the checkout's
  build directory and runs `lake build --no-build`. Lake's input hashes do not depend on paths, so
  a checkout at another path is accepted (its `.olean` files then name the original path in
  linter messages).
- **Robustness** (each with a test in `tests/test_robustness.py` or `tests/test_direct_end_to_end.py`):
  killing the whole build and rerunning resumes from the store; a module that fails on two
  different workers is classified as a source error and only its importers are skipped; a
  worker whose fingerprint differs is refused (`/v1/config` first, then `/v1/register` with the
  worker's own fingerprint); an object that fails its sha256 when a worker fetches it makes the
  coordinator drop that record and object and rebuild the module before its importers; lost
  workers and late results are handled as before; every attempt is recorded.

- **`lakefile.lean` projects** (Mathlib itself): `lakeshard translate PROJECT` (done by `run`
  automatically) runs `lake translate-config toml` into `PROJECT/.lake/lakeshard/lakefile.toml`
  (inside Lake's own `.lake`; the project's files are untouched) and every command then reads
  that; workers receive the text with their configuration. Lake calls its translation lossy for
  non-declarative configuration, so it is only trusted as far as it is checked: `check-setup`
  against a real Lake build, and `restore`, whose `lake build --no-build` runs with the original
  `lakefile.lean`. Targets other than libraries (executables, scripts) are ignored.
- **A part of a project**: `--target MODULE` (repeatable) on `run`, `build`, `reference`,
  `verify`, `assemble`, `check-setup` builds those modules and their project imports only, e.g. a
  Mathlib sub-closure; the seal then runs `lake build MODULE ...`.

Not yet: the seal's traces carry no warnings for later `lake build`s to replay.

### Remote workers (direct backend)

Machines are called by role here: `hub` runs the coordinator, `worker-1`, `worker-2`, ... run
workers. `<shared>` is a directory every machine mounts at the same path, `<local>` a directory
on one machine only.

Every worker keeps its own local build directory and reaches the coordinator and the artifact
store over HTTP; no shared file system is needed and nothing connects to a worker, so the
coordinator (which serves the store too) goes on a machine the workers can reach.

On `hub` (no local workers, listening on an address the workers can reach):

```bash
lakeshard build <project> --backend lean --work <local>/work --listen 0.0.0.0:8765 --advertise-host hub --local-workers 0
```

`<local>/work/coordinator.json` holds the URL; copy `<local>/work/token` to each worker and run there:

```bash
lakeshard worker serve --coordinator http://hub:8765 --id worker-1 --slots 8 --threads 2 --workspace <local>/worker-1 --token-file <local>/token
```

Preconditions on every worker machine (not checked automatically yet):

1. the project source at the **same absolute path** as on `hub` (Lean stores the source path of
   modules with linter messages in their `.olean`), e.g. a checkout of the same commit there;
2. the **same toolchain** at the same path (`elan toolchain install` of the project's
   `lean-toolchain`; the coordinator sends the path of its `bin` directory);
3. the **dependencies built** at the same paths (`<project>/.lake/packages/*/.lake/build`, e.g. from
   `lake exe cache get`), identical to those on `hub`;
4. TCP from the worker to the coordinator's port (and to the store server's, if it is separate);
   with `--store <shared>/store` instead, that directory at the same path; with `--storage
   shared`, the build directory mounted read-write at the same path (and `--visibility-timeout`);
5. a local disk with room for the project's outputs (`--workspace`); Linux machines building Mathlib-sized closures
   may need a higher `vm.max_map_count` than the default 65530.

Workers run the project's code (tactics, metaprograms): run them in sandboxes without credentials.

### Rules that make outputs identical

- The project source must be at the **same absolute path** on every worker. Lean 4.33 stores the
  source path of modules with linter messages in their `.olean` (`lintLogExt`). On one machine
  all simulated workers share the project directory and differ only in `buildDir`.
- Same toolchain and same dependency builds (e.g. Mathlib from its official cache) everywhere.
- Lake's own hashes are 64-bit and not meant to resist an adversary; the store uses sha256.

### Trust

Workers run the project's code (its tactics and metaprograms), so treat them as untrusted and run
them in sandboxes for untrusted projects. A wrong or tampered output can only make the final
check fail: the result should be judged by the kernel on a trusted machine (`leanchecker`, an
export plus independent kernels, `lake comparator`), not by the fact that it was built.

## Library and protocol

```python
from lakeshard import api
api.analyze(project)                      # dict
plan = api.plan(project, shards=32)       # lakeshard.protocol.Plan
report = api.build(project, work, workers=4, threads=3)
api.assemble(project, store, dest)
api.verify(project, dest, reference=ref, leanchecker_jobs=8)
```

`api.build_direct(project, work, workers=4, slots=3, threads=3, storage="shared")` runs the direct
backend; `api.check_setup(project, lake_build_dir)` compares its `lean` calls with Lake's.

Messages (`lakeshard.protocol`, all JSON-serialisable dataclasses): `Plan` / `ShardSpec`,
`ShardJob` (modules to build, modules needed, project and toolchain, store location),
`ShardResult` (records produced, timings, CPU, peak RSS, bytes moved, error),
`ModuleRecord` / `FileRef`. The coordinator talks to workers only through an `Executor`
(`submit(worker, job)`, `poll()`); `LocalProcessExecutor` starts one OS process per job with
`python -m lakeshard worker run --job job.json --result result.json --workspace DIR`.
A remote executor or an HTTP service would send the same job JSON.

## Stages

| Stage | What | Result |
|---|---|---|
| a | tiny synthetic project (tests) | `pytest`: 40 modules, 3 worker processes, static and dynamic schedules, injected failure retried, assembled build identical to `lake build`, `--no-build --rehash` and `leanchecker` pass |
| b | one machine simulating several workers on synthetic projects with the shape of real import graphs | 2,613 modules: 4 workers x 3 threads, 343 s (`lake build` 278 s); 7,839 files identical; `--no-build --rehash` and `leanchecker` (2,613/2,613) pass |
| c | a mid-sized private project that depends on Mathlib (230 modules) | 4 x 2: 597 s (`lake build` 8 threads 503 s; critical path 444 s, so at most 4.65x on any number of machines); 690 files identical; `--no-build --rehash` and `leanchecker` pass |
| S1 | direct `lean` backend, pull workers over HTTP, shared build directory (one machine) | `lean` calls identical to Lake's (setup, command line, `LEAN_PATH`) for 40 + 316 + 6 + 230 modules; outputs identical to `lake build` (120, 948, 34 files); 316 modules 18.3 s vs `lake build` 17.8 s, 1.05 of the lower bound |
| S2 | per-worker build directories, artifact store over HTTP (directory or HTTP implementation), run records | 40 and 316 modules identical to `lake build` (120, 948 files); 316 modules 17.7 s vs `lake build` 17.8 s; 121 MB fetched over HTTP in 2.1 s in total |
| S3 | repository in, cache out: `run`, `restore`, input keys and resume, seal (stock Lake writes the traces), fingerprint checks, `lakefile.lean`, `--target` | traces equal to plain `lake build` (40-module project, `module` project, Mathlib sub-closure 96 / 96); Mathlib-based project: build 456 s on 8 slots, 690 files identical, `--no-build --rehash` passes; robustness items each tested |
| d | separate machines | not started (S4) |

## Design notes

- `docs/design.zh.md` (Chinese): how others batch-build large Lean repositories (primary sources), the
  mechanism this tool relies on, the exploration log with measurements, and the planned split between
  infrastructure and model orchestration.
- `docs/research/`: the research notes behind it (Omega Institute's sharded build, Isabelle's cluster
  build, Mathlib/Lake caching, analysis tools).
- `docs/stages.md`: measurements of stages a-c and S1-S3.
- `docs/run-records.md`: the per-attempt run records (`modules.jsonl`) for schedule analysis and simulator calibration.
- `docs/plan.zh.md` (Chinese): goal (repository in, build cache out), pipeline, robustness rules, acceptance tiers, steps S1-S5 and the decision record.

## Tests

```bash
.venv/bin/python -m pytest -q          # tests marked `lean` need leanprover/lean4:v4.33.1 via elan
```
