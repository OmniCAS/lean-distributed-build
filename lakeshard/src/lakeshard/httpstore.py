"""The artifact store over HTTP: a client (`HttpStore`) and the server side (`StoreEndpoints`).

The server keeps a `LocalStore` directory and is mounted under `/v1/store` either inside the
coordinator (`lakeshard build --backend lean`, the default for `--storage store`) or on its own
(`lakeshard store serve`). Workers only connect outwards to it; nothing connects to a worker.

- `HEAD|GET /v1/store/objects/<sha256>`: an object (404 if absent), streamed;
- `PUT /v1/store/objects/<sha256>`: upload; the server hashes the body while writing it to a
  temporary file and keeps it only if the hash matches the name (400 otherwise); an existing
  object is not rewritten;
- `PUT /v1/store/records`: one `ModuleRecord` (JSON);
- `POST /v1/store/records/query` `{modules: [...]}` -> `{records: {module: ModuleRecord}}`.

The client keeps one persistent connection per thread, retries transport errors with backoff,
and checks the sha256 of every download before renaming it into place. Requests carry the
coordinator's bearer token when one is set.
"""
from __future__ import annotations

import hashlib
import hmac
import http.client
import json
import os
import re
import shutil
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

from .protocol import FileRef, ModuleRecord, to_dict
from .store import ArtifactStore, IntegrityError, LocalStore, sha256_file

PREFIX = "/v1/store"
OBJ_RE = re.compile(r"^/objects/([0-9a-f]{64})$")
CHUNK = 1 << 20


class StoreEndpoints:
    """Server side; `handle(h, method)` serves one request of a `BaseHTTPRequestHandler`."""

    def __init__(self, root: str):
        self.store = LocalStore(root)
        self.lock = threading.Lock()
        self.stats = {"objects_put": 0, "bytes_put": 0, "objects_get": 0, "bytes_get": 0, "puts_existing": 0}

    @staticmethod
    def handles(path: str) -> bool:
        return path.startswith(PREFIX + "/")

    def _count(self, **kw) -> None:
        with self.lock:
            for k, v in kw.items():
                self.stats[k] += v

    def handle(self, h: BaseHTTPRequestHandler, method: str) -> None:
        sub = h.path[len(PREFIX):].split("?", 1)[0]
        m = OBJ_RE.match(sub)
        if m:
            return self._object(h, method, m.group(1))
        if sub == "/records" and method == "PUT":
            rec = ModuleRecord.from_dict(json.loads(_read_body(h)))
            self.store.put_record(rec)
            return _send_json(h, 200, {"ok": True})
        if sub == "/records/drop" and method == "POST":
            idents = json.loads(_read_body(h)).get("idents", [])
            return _send_json(h, 200, {"dropped": [i for i in idents if self.store.drop_record(i)]})
        if sub == "/records/query" and method == "POST":
            mods = json.loads(_read_body(h)).get("modules", [])
            recs = self.store.get_records(mods)
            return _send_json(h, 200, {"records": {k: to_dict(v) for k, v in recs.items()}})
        _discard_body(h)
        return _send_json(h, 404, {"error": "not found"})

    def _object(self, h: BaseHTTPRequestHandler, method: str, sha: str) -> None:
        path = self.store._obj(sha)
        if method in ("GET", "HEAD"):
            try:
                fh = open(path, "rb")
            except FileNotFoundError:
                return _send_json(h, 404, {"error": "no such object"}, head=method == "HEAD")
            with fh:
                size = os.fstat(fh.fileno()).st_size
                h.send_response(200)
                h.send_header("Content-Type", "application/octet-stream")
                h.send_header("Content-Length", str(size))
                h.end_headers()
                if method == "GET":
                    shutil.copyfileobj(fh, h.wfile, CHUNK)
                    self._count(objects_get=1, bytes_get=size)
            return None
        if method != "PUT":
            _discard_body(h)
            return _send_json(h, 405, {"error": "method not allowed"})
        n = int(h.headers.get("Content-Length") or -1)
        if n < 0:
            return _send_json(h, 411, {"error": "Content-Length required"})
        if os.path.exists(path):
            _discard_body(h, n)
            self._count(puts_existing=1)
            return _send_json(h, 200, {"stored": False})
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tmp = f"{path}.tmp{os.getpid()}.{threading.get_ident()}"
        hasher = hashlib.sha256()
        left = n
        with open(tmp, "wb") as out:
            while left > 0:
                chunk = h.rfile.read(min(CHUNK, left))
                if not chunk:
                    break
                hasher.update(chunk)
                out.write(chunk)
                left -= len(chunk)
        if left or hasher.hexdigest() != sha:
            os.remove(tmp)
            return _send_json(h, 400, {"error": "body does not match its sha256" if not left else "short body"})
        os.replace(tmp, path)
        self._count(objects_put=1, bytes_put=n)
        return _send_json(h, 201, {"stored": True})


def _read_body(h: BaseHTTPRequestHandler) -> bytes:
    n = int(h.headers.get("Content-Length") or 0)
    return h.rfile.read(n) if n else b""


def _discard_body(h: BaseHTTPRequestHandler, n: int | None = None) -> None:
    left = int(h.headers.get("Content-Length") or 0) if n is None else n
    while left > 0:
        chunk = h.rfile.read(min(CHUNK, left))
        if not chunk:
            break
        left -= len(chunk)


def _send_json(h: BaseHTTPRequestHandler, code: int, obj, head: bool = False) -> None:
    data = json.dumps(obj).encode()
    h.send_response(code)
    h.send_header("Content-Type", "application/json")
    h.send_header("Content-Length", str(len(data)))
    h.end_headers()
    if not head:
        h.wfile.write(data)


def authorized(h: BaseHTTPRequestHandler, token: str | None) -> bool:
    if not token:
        return True
    return hmac.compare_digest(h.headers.get("Authorization", ""), f"Bearer {token}")


def serve_store(root: str, host: str = "127.0.0.1", port: int = 0, token: str | None = None):
    """A standalone store server (call `serve_forever()` on the result)."""
    ep = StoreEndpoints(root)

    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, *args):
            pass

        def _go(self, method):
            if not authorized(self, token):
                _discard_body(self)
                return _send_json(self, 401, {"error": "unauthorized"}, head=method == "HEAD")
            if not ep.handles(self.path):
                _discard_body(self)
                return _send_json(self, 404, {"error": "not found"}, head=method == "HEAD")
            return ep.handle(self, method)

        def do_GET(self):
            self._go("GET")

        def do_HEAD(self):
            self._go("HEAD")

        def do_PUT(self):
            self._go("PUT")

        def do_POST(self):
            self._go("POST")

    srv = ThreadingHTTPServer((host, port), Handler)
    srv.daemon_threads = True
    srv.endpoints = ep
    return srv


class HttpStore(ArtifactStore):
    """Client of a store server; `url` is the server's base URL (e.g. `http://hub:8765`)."""

    def __init__(self, url: str, token: str | None = None, timeout_s: float = 600.0, retries: int = 4,
                 batch: int = 2000):
        u = urlsplit(url)
        if u.scheme != "http":
            raise ValueError(f"only http:// store URLs are supported, not {url!r}")
        self.host, self.port = u.hostname, u.port or 80
        self.base = u.path.rstrip("/") + PREFIX
        self.token, self.timeout_s, self.retries, self.batch = token, timeout_s, retries, batch
        self._local = threading.local()

    def _conn(self) -> http.client.HTTPConnection:
        c = getattr(self._local, "conn", None)
        if c is None:
            c = http.client.HTTPConnection(self.host, self.port, timeout=self.timeout_s)
            self._local.conn = c
        return c

    def _drop(self) -> None:
        c = getattr(self._local, "conn", None)
        if c is not None:
            c.close()
        self._local.conn = None

    def _request(self, method: str, path: str, body=None, headers: dict | None = None, sink=None):
        """(status, data); `body` may be a callable returning a fresh body (for retries);
        `sink(response)` consumes a 200 response body instead of reading it into memory."""
        last: Exception | None = None
        for attempt in range(self.retries + 1):
            conn = self._conn()
            hdrs = dict(headers or {})
            if self.token:
                hdrs["Authorization"] = f"Bearer {self.token}"
            b = body() if callable(body) else body
            try:
                conn.request(method, self.base + path, body=b, headers=hdrs)
                r = conn.getresponse()
                if sink is not None and r.status == 200:
                    out = sink(r)
                    r.read()  # drain whatever the sink left, so the connection can be reused
                    return r.status, out
                return r.status, r.read()
            except (OSError, http.client.HTTPException) as e:
                last = e
                self._drop()
                time.sleep(min(5.0, 0.2 * 2 ** attempt))
            finally:
                if hasattr(b, "close"):
                    b.close()
        raise ConnectionError(f"store {self.host}:{self.port}{self.base}{path}: {last}")

    def has_object(self, sha: str) -> bool:
        status, _ = self._request("HEAD", f"/objects/{sha}")
        return status == 200

    def put_file(self, path: str) -> FileRef:
        sha = sha256_file(path)
        size = os.path.getsize(path)
        status, data = self._request("PUT", f"/objects/{sha}", body=lambda: open(path, "rb"),
                                     headers={"Content-Length": str(size),
                                              "Content-Type": "application/octet-stream"})
        if status not in (200, 201):
            raise IntegrityError(f"store refused {os.path.basename(path)}: {status} {data[:200]!r}")
        return FileRef("", sha, size)

    def get_file(self, ref: FileRef, dest: str) -> None:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        tmp = f"{dest}.tmp{os.getpid()}.{threading.get_ident()}"

        def sink(r):
            h = hashlib.sha256()
            with open(tmp, "wb") as out:
                while True:
                    chunk = r.read(CHUNK)
                    if not chunk:
                        break
                    h.update(chunk)
                    out.write(chunk)
            return h.hexdigest()

        status, got = self._request("GET", f"/objects/{ref.sha256}", sink=sink)
        if status != 200:
            raise IntegrityError(f"object {ref.sha256} missing for {ref.path} ({status})")
        if got != ref.sha256:
            os.remove(tmp)
            raise IntegrityError(f"hash mismatch for {ref.path}")
        os.replace(tmp, dest)

    def put_record(self, rec: ModuleRecord) -> None:
        data = json.dumps(to_dict(rec)).encode()
        status, out = self._request("PUT", "/records", body=data,
                                    headers={"Content-Type": "application/json", "Content-Length": str(len(data))})
        if status != 200:
            raise IntegrityError(f"store refused the record of {rec.module}: {status} {out[:200]!r}")

    def drop_record(self, ident: str) -> bool:
        data = json.dumps({"idents": [ident]}).encode()
        status, body = self._request("POST", "/records/drop", body=data,
                                     headers={"Content-Type": "application/json", "Content-Length": str(len(data))})
        return status == 200 and ident in json.loads(body).get("dropped", [])

    def get_records(self, modules: list[str]) -> dict[str, ModuleRecord]:
        out: dict[str, ModuleRecord] = {}
        for i in range(0, len(modules), self.batch):
            data = json.dumps({"modules": list(modules[i:i + self.batch])}).encode()
            status, body = self._request("POST", "/records/query", body=data,
                                         headers={"Content-Type": "application/json",
                                                  "Content-Length": str(len(data))})
            if status != 200:
                raise ConnectionError(f"store records query failed: {status} {body[:200]!r}")
            for k, v in json.loads(body)["records"].items():
                out[k] = ModuleRecord.from_dict(v)
        return out
