import pytest

from lakeshard.protocol import ModuleRecord
from lakeshard.store import IntegrityError, LocalStore


def test_roundtrip_and_integrity(tmp_path):
    st = LocalStore(str(tmp_path / "store"))
    f = tmp_path / "a.olean"
    f.write_bytes(b"hello" * 1000)
    ref = st.put_file(str(f))
    ref.path = "lib/lean/A.olean"
    st.put_record(ModuleRecord("A", [ref], "w0", "s0"))
    recs = st.get_records(["A", "B"])
    assert list(recs) == ["A"] and recs["A"].files[0].sha256 == ref.sha256
    out = tmp_path / "out" / "A.olean"
    st.get_file(ref, str(out))
    assert out.read_bytes() == f.read_bytes()
    # corrupt the object: the next download must fail
    obj = tmp_path / "store" / "objects" / ref.sha256[:2] / ref.sha256
    obj.write_bytes(b"tampered")
    with pytest.raises(IntegrityError):
        st.get_file(ref, str(tmp_path / "out2" / "A.olean"))
