"""lakeshard: split a Lean/Lake project along its import graph, build the shards on several
workers, move build outputs through a content-addressed store, and assemble and verify the result."""

__version__ = "0.2.0"

from .protocol import FileRef, ModuleRecord, Plan, ShardJob, ShardResult, ShardSpec  # noqa: E402,F401
