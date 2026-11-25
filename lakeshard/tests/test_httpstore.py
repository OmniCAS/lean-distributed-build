"""The artifact store over HTTP (no Lean needed)."""
import http.client
import threading

import pytest

from lakeshard.httpstore import HttpStore, serve_store
from lakeshard.protocol import FileRef, ModuleRecord
from lakeshard.store import IntegrityError


@pytest.fixture
def server(tmp_path):
    srv = serve_store(str(tmp_path / "root"), token="tok")
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    yield srv, f"http://127.0.0.1:{srv.server_address[1]}", tmp_path / "root"
    srv.shutdown()
    srv.server_close()


def test_roundtrip_records_and_integrity(server, tmp_path):
    srv, url, root = server
    st = HttpStore(url, token="tok", batch=3)  # small batches: the records query is split
    data = bytes(range(256)) * 9000  # > 1 chunk
    f = tmp_path / "a.olean"
    f.write_bytes(data)
    ref = st.put_file(str(f))
    assert st.has_object(ref.sha256) and not st.has_object("0" * 64)
    assert st.put_file(str(f)).sha256 == ref.sha256  # second upload of the same content is a no-op
    assert srv.endpoints.stats["puts_existing"] == 1
    ref.path = "lib/lean/A.olean"
    for i in range(7):
        st.put_record(ModuleRecord(f"M{i}", [ref], "w0", "t1"))
    recs = st.get_records([f"M{i}" for i in range(9)])
    assert sorted(recs) == [f"M{i}" for i in range(7)] and recs["M3"].files[0].sha256 == ref.sha256
    out = tmp_path / "out" / "A.olean"
    st.get_file(ref, str(out))
    assert out.read_bytes() == data
    # tamper with the object on the server: the client must refuse the download
    (root / "objects" / ref.sha256[:2] / ref.sha256).write_bytes(b"tampered")
    with pytest.raises(IntegrityError):
        st.get_file(ref, str(tmp_path / "out2" / "A.olean"))
    with pytest.raises(IntegrityError):
        st.get_file(FileRef("x", "1" * 64, 3), str(tmp_path / "out3" / "x"))


def test_server_checks_names_and_token(server):
    srv, url, _root = server
    port = srv.server_address[1]
    c = http.client.HTTPConnection("127.0.0.1", port)
    c.request("PUT", "/v1/store/objects/" + "ab" * 32, body=b"not that hash",
              headers={"Authorization": "Bearer tok", "Content-Length": "13"})
    r = c.getresponse()
    assert r.status == 400 and b"sha256" in r.read()
    c.request("HEAD", "/v1/store/objects/" + "ab" * 32)  # no token
    r = c.getresponse()
    r.read()
    assert r.status == 401
    with pytest.raises(ConnectionError):
        HttpStore(url, token="wrong", retries=0).get_records(["M"])
