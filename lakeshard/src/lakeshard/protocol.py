"""Plain, serialisable messages exchanged between the coordinator, the workers and the store.

Everything here is a dataclass of strings, numbers, lists and dicts, so it can go through JSON
files today and through an HTTP or queue front end later without changes to the core.
"""
from __future__ import annotations

import dataclasses
import json
from dataclasses import dataclass, field
from typing import Any

SCHEMA = "lakeshard/1"


def to_dict(obj: Any) -> Any:
    if dataclasses.is_dataclass(obj):
        return {f.name: to_dict(getattr(obj, f.name)) for f in dataclasses.fields(obj)}
    if isinstance(obj, list):
        return [to_dict(x) for x in obj]
    if isinstance(obj, dict):
        return {k: to_dict(v) for k, v in obj.items()}
    return obj


def dumps(obj: Any, indent: int | None = None) -> str:
    return json.dumps(to_dict(obj), indent=indent, ensure_ascii=False, sort_keys=False)


@dataclass
class FileRef:
    """One build output file of a module, addressed by content."""

    path: str  # relative to the build directory, e.g. "lib/lean/Foo/Bar.olean"
    sha256: str
    size: int

    @staticmethod
    def from_dict(d: dict) -> "FileRef":
        return FileRef(d["path"], d["sha256"], int(d["size"]))


@dataclass
class ModuleRecord:
    """All build outputs of one module (olean, ilean, c, Lake trace and hash files...).

    `key`: the module's input key (direct backend; see `fingerprint.py`). The store files a record
    under its key when it has one, otherwise under the module name (Lake batch backend)."""

    module: str
    files: list[FileRef]
    worker: str = ""
    shard: str = ""
    key: str = ""

    @staticmethod
    def from_dict(d: dict) -> "ModuleRecord":
        return ModuleRecord(d["module"], [FileRef.from_dict(x) for x in d["files"]],
                            d.get("worker", ""), d.get("shard", ""), d.get("key", ""))

    @property
    def ident(self) -> str:
        return self.key or self.module

    def digest(self) -> str:
        return ",".join(f"{f.path}:{f.sha256}" for f in sorted(self.files, key=lambda f: f.path))


@dataclass
class ShardSpec:
    id: str
    modules: list[str]
    deps: list[str]  # ids of shards whose modules this shard imports
    cost: float

    @staticmethod
    def from_dict(d: dict) -> "ShardSpec":
        return ShardSpec(d["id"], list(d["modules"]), list(d["deps"]), float(d["cost"]))


@dataclass
class Plan:
    schema: str
    project: str
    shards: list[ShardSpec]
    stats: dict = field(default_factory=dict)

    @staticmethod
    def from_dict(d: dict) -> "Plan":
        return Plan(d.get("schema", SCHEMA), d["project"], [ShardSpec.from_dict(s) for s in d["shards"]],
                    d.get("stats", {}))

    def save(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(dumps(self, indent=1))

    @staticmethod
    def load(path: str) -> "Plan":
        with open(path, encoding="utf-8") as fh:
            return Plan.from_dict(json.load(fh))


@dataclass
class ShardJob:
    """What a worker needs to build one shard. `needs` are modules whose outputs must be present."""

    job_id: str
    shard_id: str
    modules: list[str]
    needs: list[str]
    project_dir: str
    lakefile: str  # the project's lakefile.toml (the worker writes its own copy with its build dir)
    toolchain_bin: str
    threads: int = 0  # LEAN_NUM_THREADS for this job; 0 = leave unset
    timeout_s: float = 7200.0
    attempt: int = 1
    store: str = ""  # store location (a directory path today; a URL later)
    fail_on_purpose: bool = False  # test hook: report a failure without building

    @staticmethod
    def from_dict(d: dict) -> "ShardJob":
        return ShardJob(**{f.name: d[f.name] for f in dataclasses.fields(ShardJob) if f.name in d})


@dataclass
class ShardResult:
    job_id: str
    shard_id: str
    worker: str
    ok: bool
    records: list[ModuleRecord] = field(default_factory=list)
    built_modules: list[str] = field(default_factory=list)  # modules Lake actually compiled
    module_seconds: dict = field(default_factory=dict)  # per-module time reported by Lake
    wall_s: float = 0.0
    fetch_s: float = 0.0
    build_s: float = 0.0
    upload_s: float = 0.0
    cpu_s: float = 0.0
    max_rss_bytes: int = 0
    fetched_files: int = 0
    fetched_bytes: int = 0
    uploaded_files: int = 0
    uploaded_bytes: int = 0
    error: str = ""
    log_tail: str = ""

    @staticmethod
    def from_dict(d: dict) -> "ShardResult":
        kw = {f.name: d[f.name] for f in dataclasses.fields(ShardResult) if f.name in d}
        kw["records"] = [ModuleRecord.from_dict(r) for r in d.get("records", [])]
        return ShardResult(**kw)


# --- direct `lean` backend: one task = one module, workers pull tasks from the coordinator


@dataclass
class BuildConfig:
    """Sent to every worker when it registers: where the project, toolchain and outputs are."""

    run_id: str
    project_dir: str  # same absolute path on every worker
    toolchain_bin: str  # directory with `lean` (same toolchain on every worker)
    storage: str  # "shared": one build directory for all workers; "store": own directory + store
    build_dir: str = ""  # storage=shared: the shared build directory (e.g. on NFS)
    store: str = ""  # storage=store: artifact store location
    visibility_timeout_s: float = 0.0  # wait this long for files written elsewhere to appear (NFS)
    visibility_poll_s: float = 0.5
    heartbeat_s: float = 5.0
    keep_setup: bool = False  # keep each module's .setup.json next to its .c file (as Lake does)
    fingerprint: str = ""  # sha256 of the coordinator's environment fingerprint; workers must match it
    lakefile_toml: str = ""  # the TOML translation of a lakefile.lean project (workers load it from here)

    @staticmethod
    def from_dict(d: dict) -> "BuildConfig":
        return BuildConfig(**{f.name: d[f.name] for f in dataclasses.fields(BuildConfig) if f.name in d})


@dataclass
class ModuleTask:
    task_id: str
    module: str
    attempt: int = 1
    threads: int = 0  # LEAN_NUM_THREADS for this module; 0 = the worker's default
    timeout_s: float = 7200.0
    needs: list[str] = field(default_factory=list)  # storage=store: keys (or names) of the import closure
    key: str = ""  # the module's input key: its record is filed under it
    fail_on_purpose: bool = False  # test hook: report a failure without running lean

    @staticmethod
    def from_dict(d: dict) -> "ModuleTask":
        return ModuleTask(**{f.name: d[f.name] for f in dataclasses.fields(ModuleTask) if f.name in d})


@dataclass
class ModuleResult:
    task_id: str
    module: str
    worker: str
    ok: bool
    attempt: int = 1
    outputs: list[FileRef] = field(default_factory=list)  # paths relative to the build directory
    started: float = 0.0  # unix time
    wall_s: float = 0.0  # whole task on the worker
    lean_s: float = 0.0  # the lean process (plus leanir, if any)
    cpu_s: float = 0.0
    max_rss_bytes: int = 0
    wait_s: float = 0.0  # waiting for imported outputs to become visible
    fetch_s: float = 0.0  # storage=store: fetching imports from the store
    fetched_bytes: int = 0
    publish_s: float = 0.0  # moving outputs into place / uploading them
    threads: int = 0
    exit_code: int | None = None
    error: str = ""
    log_tail: str = ""
    host: str = ""  # the worker machine's host name
    lean_start: float = 0.0  # unix time on the worker's clock
    lean_end: float = 0.0
    ended: float = 0.0
    fetched_files: int = 0
    corrupt: list[str] = field(default_factory=list)  # store records whose objects failed their sha256

    @staticmethod
    def from_dict(d: dict) -> "ModuleResult":
        kw = {f.name: d[f.name] for f in dataclasses.fields(ModuleResult) if f.name in d}
        kw["outputs"] = [FileRef.from_dict(x) for x in d.get("outputs", [])]
        return ModuleResult(**kw)
