"""Content-addressed artifact store.

Objects are files named by their sha256; a module record lists the files a module produced.
Two implementations of the same five methods: `LocalStore` keeps both in a directory (a local
disk, or a directory every worker mounts), `HttpStore` (`httpstore.py`) talks to a store served
over HTTP by the coordinator or by `lakeshard store serve`. Every download is checked against its
sha256 on the receiving side.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import threading

from .protocol import FileRef, ModuleRecord


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


class IntegrityError(Exception):
    pass


class ArtifactStore:
    def put_file(self, path: str) -> FileRef: ...
    def get_file(self, ref: FileRef, dest: str) -> None: ...
    def put_record(self, rec: ModuleRecord) -> None: ...
    def get_records(self, modules: list[str]) -> dict[str, ModuleRecord]: ...
    def has_object(self, sha: str) -> bool: ...


def open_store(location: str, token: str | None = None) -> ArtifactStore:
    """A directory path (or `file://` URL) or an `http://` URL of a store server."""
    if location.startswith("file://"):
        location = location[len("file://"):]
    if location.startswith(("http://", "https://")):
        from .httpstore import HttpStore
        return HttpStore(location, token=token)
    if "://" in location:
        raise ValueError(f"unsupported store location {location!r}")
    return LocalStore(location)


class LocalStore(ArtifactStore):
    def __init__(self, root: str):
        self.root = os.path.abspath(root)
        os.makedirs(os.path.join(self.root, "objects"), exist_ok=True)
        os.makedirs(os.path.join(self.root, "records"), exist_ok=True)
        self._lock = threading.Lock()

    def _obj(self, sha: str) -> str:
        return os.path.join(self.root, "objects", sha[:2], sha)

    def _rec(self, module: str) -> str:
        h = hashlib.sha1(module.encode("utf-8")).hexdigest()
        return os.path.join(self.root, "records", h[:2], h + ".json")

    def has_object(self, sha: str) -> bool:
        return os.path.exists(self._obj(sha))

    def put_file(self, path: str) -> FileRef:
        sha = sha256_file(path)
        size = os.path.getsize(path)
        dst = self._obj(sha)
        if not os.path.exists(dst):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            tmp = f"{dst}.tmp{os.getpid()}.{threading.get_ident()}"
            shutil.copyfile(path, tmp)
            os.replace(tmp, dst)  # atomic: readers never see a partial object
        return FileRef("", sha, size)

    def get_file(self, ref: FileRef, dest: str) -> None:
        src = self._obj(ref.sha256)
        if not os.path.exists(src):
            raise IntegrityError(f"object {ref.sha256} missing for {ref.path}")
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        tmp = f"{dest}.tmp{os.getpid()}.{threading.get_ident()}"
        shutil.copyfile(src, tmp)
        if sha256_file(tmp) != ref.sha256:
            os.remove(tmp)
            raise IntegrityError(f"hash mismatch for {ref.path}")
        os.replace(tmp, dest)

    def put_record(self, rec: ModuleRecord) -> None:
        p = self._rec(rec.ident)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        tmp = f"{p}.tmp{os.getpid()}.{threading.get_ident()}"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump({"module": rec.module, "key": rec.key, "worker": rec.worker, "shard": rec.shard,
                       "files": [{"path": f.path, "sha256": f.sha256, "size": f.size} for f in rec.files]},
                      fh)
        os.replace(tmp, p)

    def get_records(self, idents: list[str]) -> dict[str, ModuleRecord]:
        """Records by key (direct backend) or by module name (batch backend)."""
        out = {}
        for m in idents:
            p = self._rec(m)
            if os.path.exists(p):
                with open(p, encoding="utf-8") as fh:
                    out[m] = ModuleRecord.from_dict(json.load(fh))
        return out

    def drop_record(self, ident: str) -> bool:
        """Forget a record whose objects turned out corrupt, and delete those of its objects that do
        not match their sha256 (objects are never rewritten, so a bad one must go before a rebuild
        can store it again). Good objects stay (other records may share them)."""
        p = self._rec(ident)
        if not os.path.exists(p):
            return False
        try:
            with open(p, encoding="utf-8") as fh:
                rec = ModuleRecord.from_dict(json.load(fh))
            for f in rec.files:
                o = self._obj(f.sha256)
                if os.path.exists(o) and sha256_file(o) != f.sha256:
                    os.remove(o)
        finally:
            os.remove(p)
        return True

    def check_record(self, rec: ModuleRecord) -> bool:
        """Every object of the record is present with the recorded size (cheap; no hashing)."""
        for f in rec.files:
            try:
                if os.path.getsize(self._obj(f.sha256)) != f.size:
                    return False
            except OSError:
                return False
        return True

    def size(self) -> tuple[int, int]:
        n = b = 0
        for dp, _dn, fns in os.walk(os.path.join(self.root, "objects")):
            for fn in fns:
                n += 1
                b += os.path.getsize(os.path.join(dp, fn))
        return n, b
