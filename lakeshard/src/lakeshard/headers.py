"""Read the import header of a Lean source file without running anything from it.

The header grammar (Lean 4.35, `Lean.Parser.Module`) is
`module? prelude? ((public)? (meta)? import (all)? Ident)*`. An import is *exported* when it is
`public` or when the file is not a `module` (`Lean.Elab.headerToImports`). The parser here works
line by line: each `import` directive must start on its own line, as in every project seen so far.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

IMPORT_RE = re.compile(r"^(?:(public)\s+|private\s+)?(?:(meta)\s+)?import\s+(?:(all)\s+)?(.+)$")


@dataclass(frozen=True)
class Import:
    module: str
    is_exported: bool = True
    import_all: bool = False
    is_meta: bool = False


@dataclass
class Header:
    is_module: bool = False
    imports: list[Import] = field(default_factory=list)


def parse_header(text: str) -> Header:
    """The `module` flag and the imports (with their `public`/`meta`/`all` flags) of `text`."""
    h = Header()
    depth = 0  # block-comment nesting
    for line in text.splitlines():
        s = line.strip()
        while True:
            if depth > 0:
                j, k = s.find("-/"), s.find("/-")
                if k != -1 and (j == -1 or k < j):
                    depth += 1
                    s = s[k + 2:]
                    continue
                if j == -1:
                    s = ""
                    break
                depth -= 1
                s = s[j + 2:].strip()
                continue
            if s.startswith("/-"):
                depth += 1
                s = s[2:]
                continue
            break
        if not s or s.startswith("--"):
            continue
        word = re.split(r"\s|--|/-", s, maxsplit=1)[0]
        if word == "module":
            h.is_module = True
            continue
        if word == "prelude":
            continue
        m = IMPORT_RE.match(s)
        if m:
            body = m.group(4).split("--")[0]
            if "/-" in body:
                body = body.split("/-")[0]
            for name in body.split():
                h.imports.append(Import(name, is_exported=bool(m.group(1)) or not h.is_module,
                                        import_all=bool(m.group(3)), is_meta=bool(m.group(2))))
            continue
        break
    return h


def parse_imports(text: str) -> list[str]:
    """Return the modules imported in the header of `text` (in order, duplicates kept)."""
    return [i.module for i in parse_header(text).imports]


def read_header(path: str) -> Header:
    with open(path, "rb") as fh:
        return parse_header(fh.read().decode("utf-8", errors="replace"))


def parse_file(path: str) -> tuple[list[str], int, int]:
    """(imports, number of lines, number of bytes) of a source file."""
    with open(path, "rb") as fh:
        data = fh.read()
    text = data.decode("utf-8", errors="replace")
    return parse_imports(text), text.count("\n") + (0 if text.endswith("\n") or not text else 1), len(data)
