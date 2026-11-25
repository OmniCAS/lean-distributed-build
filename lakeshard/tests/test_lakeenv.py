"""What the direct backend passes to `lean`, compared with Lake's own choices."""
import json
import os

import pytest

from lakeshard import api
from lakeshard.lakeenv import LakeWorkspace
from lakeshard.project import LakeProject, flatten_lean_options, glob_matches
from lakeshard.synth import random_dag, write_module_system_project, write_project


def test_flatten_lean_options():
    assert flatten_lean_options({"autoImplicit": False, "linter": {"style": {"longLine": True}}}) == \
        {"autoImplicit": False, "linter.style.longLine": True}
    assert flatten_lean_options([["a", 1], {"name": "b.c", "value": "x"}]) == {"a": 1, "b.c": "x"}
    assert flatten_lean_options(None) == {}


def test_globs():
    assert glob_matches("A", "A") and not glob_matches("A", "A.B")
    assert glob_matches("A.+", "A.B.C") and not glob_matches("A.+", "A") and not glob_matches("A.+", "AB.C")
    assert glob_matches("A.*", "A") and glob_matches("A.*", "A.B")


def _toml(tmp_path, text):
    (tmp_path / "lakefile.toml").write_text(text)
    return LakeProject.load(str(tmp_path))


def test_module_library_options_and_args(tmp_path):
    p = _toml(tmp_path, 'name = "p"\nmoreLeanArgs = ["--m1"]\nweakLeanArgs = ["--w1"]\nbuildType = "debug"\n'
                        '[leanOptions]\nautoImplicit = false\nmaxHeartbeats = 10\n'
                        '[[lean_lib]]\nname = "Foo"\n'  # roots = [Foo]: Foo and everything below it
                        '[[lean_lib]]\nname = "Bar"\nglobs = ["Foo.Sub.+"]\nmoreLeanArgs = ["--m2"]\n'
                        'weakLeanArgs = ["--w2"]\nleanOptions = { maxHeartbeats = 20 }\n')
    # libraries are searched last to first (Lake's `Package.findModule?`)
    assert p.lib_of("Foo").name == "Foo" and p.lib_of("Foo.X").name == "Foo"
    assert p.lib_of("Foo.Sub.Y").name == "Bar" and p.lib_of("Other") is None
    bar = p.lib_of("Foo.Sub.Y")
    assert p.lean_options_of(bar) == {"debugAssertions": True, "autoImplicit": False, "maxHeartbeats": 20}
    assert p.lean_args_of(bar) == ["--w1", "--w2", "--m1", "--m2"]
    assert not p.unsupported


def test_unsupported_settings_are_refused(tmp_path):
    p = _toml(tmp_path, 'name = "p"\nprecompileModules = true\n[[lean_lib]]\nname = "Foo"\n')
    with pytest.raises(Exception, match="precompileModules"):
        LakeWorkspace(p, str(tmp_path / "b"), "/nonexistent").check_supported()


def _fake_dep(tmp_path):
    """A project with one dependency package `dep` whose modules are already 'built'."""
    root = tmp_path / "root"
    dep = root / ".lake" / "packages" / "dep"
    for rel, text in {"Dep/Pub.lean": "module\n\npublic import Dep.Base\nimport Dep.Hidden\n",
                      "Dep/Base.lean": "module\n", "Dep/Hidden.lean": "module\n",
                      "Dep/Old.lean": "import Dep.Base\n"}.items():
        (dep / os.path.dirname(rel)).mkdir(parents=True, exist_ok=True)
        (dep / rel).write_text(text)
        olean = dep / ".lake" / "build" / "lib" / "lean" / rel.replace(".lean", ".olean")
        olean.parent.mkdir(parents=True, exist_ok=True)
        olean.write_bytes(b"x")
    (root / "R").mkdir(parents=True)
    (root / "R" / "Legacy.lean").write_text("import Dep.Pub\nimport Lean\n")
    (root / "R" / "Mod.lean").write_text("module\n\npublic import Dep.Pub\nimport Dep.Old\n")
    (root / "lakefile.toml").write_text('name = "r"\n[[lean_lib]]\nname = "R"\nglobs = ["R.+"]\n')
    (root / "lake-manifest.json").write_text(json.dumps(
        {"version": "1.1.0", "packagesDir": ".lake/packages", "packages": [{"name": "dep", "type": "git"}]}))
    (root / "lean-toolchain").write_text("leanprover/lean4:v4.35.0\n")
    return LakeWorkspace(LakeProject.load(str(root)), str(tmp_path / "build"), "/tc/bin")


def test_import_arts_legacy_and_module(tmp_path):
    ws = _fake_dep(tmp_path)
    lib = ws.deps[0].lib_dir
    assert ws.lean_path() == [lib, str(tmp_path / "build" / "lib" / "lean")]
    # a non-module file gets every transitive workspace import, with all artifacts (Lean core skipped)
    arts = ws.import_arts("R.Legacy")
    assert sorted(arts) == ["Dep.Base", "Dep.Hidden", "Dep.Pub"]
    assert arts["Dep.Pub"] == [[f"{lib}/Dep/Pub.olean", f"{lib}/Dep/Pub.olean.server", f"{lib}/Dep/Pub.olean.private"],
                               [f"{lib}/Dep/Pub.ir.sig", f"{lib}/Dep/Pub.ir"]]
    # a module file follows only `public import` edges and gets the public artifacts
    arts = ws.import_arts("R.Mod")
    assert sorted(arts) == ["Dep.Base", "Dep.Old", "Dep.Pub"]  # Dep.Hidden is a private import of Dep.Pub
    assert arts["Dep.Pub"][0] == [f"{lib}/Dep/Pub.olean", f"{lib}/Dep/Pub.olean.server"]
    assert arts["Dep.Old"] == [[f"{lib}/Dep/Old.olean"]]  # a non-module dependency: one file
    setup = ws.setup("R.Mod")
    assert setup["isModule"] and setup["package"] == "r" and setup["name"] == "R.Mod"


@pytest.mark.lean
def test_setup_matches_lake_legacy(tmp_path, tc_bin):
    proj = tmp_path / "proj"
    write_project(str(proj), random_dag(25, max_imports=3, locality=6), warn_every=4)
    ref = api.reference_build(str(proj), str(tmp_path / "ref"))
    assert ref["ok"], ref
    res = api.check_setup(str(proj), str(tmp_path / "ref"))
    assert res["ok"] and res["checked_setup_files"] == 25 and res["checked_commands"] == 25, res


def _tc435():
    p = os.path.join(os.environ.get("ELAN_HOME", os.path.expanduser("~/.elan")), "toolchains",
                     "leanprover--lean4---v4.35.0", "bin")
    return p if os.path.exists(os.path.join(p, "lake")) else None


@pytest.mark.lean
def test_module_system_matches_lake(tmp_path):
    if _tc435() is None:
        pytest.skip("leanprover/lean4:v4.35.0 not installed")
    proj = tmp_path / "modsys"
    write_module_system_project(str(proj))
    ref = api.reference_build(str(proj), str(tmp_path / "ref"))
    assert ref["ok"], ref
    res = api.check_setup(str(proj), str(tmp_path / "ref"))
    assert res["ok"] and res["checked_setup_files"] == 6, res
    res = api.run(str(proj), str(tmp_path / "work"), workers=2, slots=2)  # build, seal, pack
    assert res["ok"] and res["seal"]["from_store"] == 6 and res["seal"]["no_build_check"]["ok"], res
    sealed = tmp_path / "work" / "sealed"
    ver = api.verify(str(proj), str(sealed), reference=str(tmp_path / "ref"))  # includes lake --no-build --rehash
    # 4 module files x 7 outputs (.olean .olean.server .olean.private .ilean .ir .ir.sig .c) + 2 plain x 3
    assert ver["compare"]["ok"] and ver["compare"]["identical_files"] == 34, ver
    assert ver["lake_no_build"]["ok"], ver
    for rel in ("ModSys/C", "ModSys/D", "Extra/X"):  # Lake's own input hashes
        a = json.load(open(sealed / "lib" / "lean" / (rel + ".trace")))
        b = json.load(open(tmp_path / "ref" / "lib" / "lean" / (rel + ".trace")))
        assert a["depHash"] == b["depHash"]
