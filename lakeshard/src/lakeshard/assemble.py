"""Put the outputs of every module, as recorded in the store, into one build directory."""
from __future__ import annotations

import os
import time

from .project import ProjectGraph
from .store import open_store


def assemble(graph: ProjectGraph, store_location: str, dest_build_dir: str, idents: dict | None = None,
             token: str | None = None) -> dict:
    """`idents`: module -> record key (from a build manifest); default: records filed by module name."""
    t0 = time.time()
    store = open_store(store_location, token=token)
    ids = {m: (idents or {}).get(m, m) for m in graph.modules}
    by_id = store.get_records(sorted(set(ids.values())))
    recs = {m: by_id[i] for m, i in ids.items() if i in by_id}
    missing = sorted(set(graph.modules) - set(recs))
    files = nbytes = 0
    for m in graph.order:
        r = recs.get(m)
        if r is None:
            continue
        for f in r.files:
            store.get_file(f, os.path.join(dest_build_dir, f.path))  # verifies sha256
            files += 1
            nbytes += f.size
    return {"build_dir": os.path.abspath(dest_build_dir), "modules": len(recs), "missing": missing,
            "files": files, "bytes": nbytes, "seconds": round(time.time() - t0, 2), "ok": not missing}
