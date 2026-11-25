from lakeshard.headers import parse_imports


def test_plain_imports():
    assert parse_imports("import A\nimport B.C D\n\ndef x := 1\nimport E\n") == ["A", "B.C", "D"]


def test_comments_and_module_keywords():
    text = """/- a header comment
   import NotThis -/
-- line comment
module
public import A
import all B
public meta import C  -- trailing
prelude
theorem t : True := trivial
"""
    assert parse_imports(text) == ["A", "B", "C"]


def test_nested_block_comment():
    assert parse_imports("/- outer /- inner -/ still -/\nimport X\n") == ["X"]


def test_stops_at_first_command():
    assert parse_imports("import A\nopen B\nimport C\n") == ["A"]


def test_header_flags():
    from lakeshard.headers import Import, parse_header

    h = parse_header("module -- comment\n\npublic import A\nimport all B\nmeta import C\npublic meta import D E\n")
    assert h.is_module
    assert h.imports == [Import("A", True, False, False), Import("B", False, True, False),
                         Import("C", False, False, True), Import("D", True, False, True),
                         Import("E", True, False, True)]
    plain = parse_header("import A\nimport B\n")
    assert not plain.is_module and all(i.is_exported for i in plain.imports)  # non-module: all exported
