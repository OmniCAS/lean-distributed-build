"""What Lake would pass to `lean` for one module: the `--setup` file, the arguments and `LEAN_PATH`.

Mirrors Lake 4.33-4.35 for a root package configured with `lakefile.toml`:

- `Lake/Build/Module.lean`: `fetchTransImportArts` (which imported modules go into `importArts`,
  and with which artifacts), `computeExportInfo` (the artifacts of one module), `recFetchPreSetup`
  and `mkModuleSetup` (name, package, `isModule`, options);
- `Lake/Build/Actions.lean`: `compileLeanModule` (`lean <weak args> <more args> <source> -o -i -c
  --setup --json`, environment `LEAN_PATH` only; `leanir` afterwards when
  `compiler.postponeCompile` is set on a `module` file);
- `Lake/Config/Workspace.lean`: `leanPath` (the library directories of all packages, the root
  package last, dependencies in the reverse of `lake-manifest.json` order).

Dependencies (Mathlib and its own dependencies, often configured with a `lakefile.lean`) are read
from `lake-manifest.json` and must already be built in their `.lake/build`. Their modules are
found through their `.olean` files and their headers are read from their sources. Nothing from
the project or its dependencies is executed. `lakeshard check-setup` compares all of this with
the `.setup.json` and `.trace` files of a real `lake build`.

Not reproduced (the direct backend refuses such projects or the result would differ):
`precompileModules`, `dynlibs`/`plugins`, `extraDepTargets`/`needs`, Lake's artifact cache
(`enableArtifactCache`, which makes Lake pass cache paths), the LLVM backend (`-b`).
"""
from __future__ import annotations

import json
import os
import re
import subprocess
try:
    import tomllib
except ModuleNotFoundError:  # Python < 3.11 (worker): dependencies keep the default layout
    tomllib = None
from dataclasses import dataclass, field

from .headers import Header, Import, read_header
from .project import LakeProject, ProjectError, module_rel

OUTPUT_SUFFIXES = (".olean", ".olean.server", ".olean.private", ".ilean", ".ir.sig", ".ir", ".c")


@dataclass
class Package:
    name: str
    dir: str  # absolute
    lib_dir: str  # absolute: <build dir>/lib/lean
    src_dirs: list[str] = field(default_factory=list)  # where module sources may be (dependencies)


@dataclass
class ModuleLoc:
    module: str
    package: Package
    src: str  # absolute source path
    lib_dir: str  # where its .olean/.ilean/.ir files are (or will be)
    ir_dir: str  # where its .c file is
    is_root: bool  # a module of the root package (built by us)


def lean_version(project_dir: str, toolchain_bin: str | None = None) -> tuple[int, int, int]:
    tc = os.path.join(project_dir, "lean-toolchain")
    if os.path.exists(tc):
        m = re.search(r"v?(\d+)\.(\d+)\.(\d+)", open(tc, encoding="utf-8").read())
        if m:
            return int(m.group(1)), int(m.group(2)), int(m.group(3))
    if toolchain_bin and os.path.exists(os.path.join(toolchain_bin, "lean")):
        out = subprocess.run([os.path.join(toolchain_bin, "lean"), "--version"], capture_output=True, text=True)
        m = re.search(r"version (\d+)\.(\d+)\.(\d+)", out.stdout)
        if m:
            return int(m.group(1)), int(m.group(2)), int(m.group(3))
    return (0, 0, 0)


def _dep_packages(proj: LakeProject) -> list[Package]:
    """Dependencies in `lake-manifest.json` order (= Lake's `Workspace.packages` after the root)."""
    mf = os.path.join(proj.project_dir, "lake-manifest.json")
    if not os.path.exists(mf):
        return []
    with open(mf, encoding="utf-8") as fh:
        man = json.load(fh)
    pkgs_dir = os.path.join(proj.project_dir, man.get("packagesDir") or os.path.join(".lake", "packages"))
    out = []
    for p in man.get("packages", []):
        if p.get("type") == "path":
            d = os.path.normpath(os.path.join(proj.project_dir, p["dir"]))
        else:
            d = os.path.join(pkgs_dir, p["name"])
        build = os.path.join(".lake", "build")
        src_dirs = [d]
        toml_path = os.path.join(d, "lakefile.toml")
        if os.path.exists(toml_path) and tomllib is not None:
            with open(toml_path, "rb") as fh:
                cfg = tomllib.load(fh)
            build = cfg.get("buildDir", build)
            base = os.path.join(d, cfg.get("srcDir", "."))
            src_dirs = [os.path.normpath(os.path.join(base, lib.get("srcDir", "."))) for lib in cfg.get("lean_lib", [])]
            src_dirs = list(dict.fromkeys(src_dirs + [os.path.normpath(base)]))
        out.append(Package(p["name"], d, os.path.join(d, build, "lib", "lean"), src_dirs))
    return out


class LakeWorkspace:
    """The root package (built into `build_dir`) and its already-built dependencies."""

    def __init__(self, project: LakeProject, build_dir: str, toolchain_bin: str,
                 version: tuple[int, int, int] | None = None):
        self.proj = project
        self.build_dir = os.path.abspath(build_dir)
        self.toolchain_bin = toolchain_bin
        self.version = version or lean_version(project.project_dir, toolchain_bin)
        self.root = Package(project.package, project.project_dir, os.path.join(self.build_dir, "lib", "lean"))
        self.deps = _dep_packages(project)
        self._loc: dict[str, ModuleLoc | None] = {}
        self._hdr: dict[str, Header] = {}
        self._arts: dict[str, list[str]] = {}

    # --- environment and arguments

    def lean_path(self) -> list[str]:
        """`Workspace.leanPath`: packages folded with `::`, i.e. the reverse of root-then-manifest order."""
        return [p.lib_dir for p in reversed(self.deps)] + [self.root.lib_dir]

    def lean_path_str(self) -> str:
        return os.pathsep.join(self.lean_path())

    def lean_exe(self) -> str:
        return os.path.join(self.toolchain_bin, "lean")

    # --- modules

    def locate(self, module: str) -> ModuleLoc | None:
        """The workspace module named `module` (None for Lean core modules and unknown names)."""
        if module in self._loc:
            return self._loc[module]
        rel = module_rel(module)
        loc = None
        lib = self.proj.lib_of(module)
        if lib is not None:
            loc = ModuleLoc(module, self.root, os.path.join(self.proj.lib_src_root(lib), rel + ".lean"),
                            self.root.lib_dir, os.path.join(self.build_dir, "ir"), True)
        else:
            for p in self.deps:  # Lake's `findModules`: first package that provides it
                if os.path.exists(os.path.join(p.lib_dir, rel + ".olean")):
                    src = next((os.path.join(s, rel + ".lean") for s in p.src_dirs
                                if os.path.isfile(os.path.join(s, rel + ".lean"))), "")
                    loc = ModuleLoc(module, p, src, p.lib_dir,
                                    os.path.join(os.path.dirname(os.path.dirname(p.lib_dir)), "ir"), False)
                    break
        self._loc[module] = loc
        return loc

    def header(self, module: str) -> Header:
        h = self._hdr.get(module)
        if h is None:
            loc = self.locate(module)
            if loc is None:
                raise ProjectError(f"module {module} is not in the workspace")
            if not loc.src or not os.path.isfile(loc.src):
                raise ProjectError(f"no source file for {module} in package {loc.package.name}")
            h = read_header(loc.src)
            self._hdr[module] = h
        return h

    def outputs(self, module: str, build_dir: str | None = None) -> dict[str, str]:
        """Output files Lean writes for a root-package module: suffix -> absolute path."""
        b = os.path.abspath(build_dir or self.build_dir)
        rel = module_rel(module)
        lib = os.path.join(b, "lib", "lean", rel)
        out = {".olean": lib + ".olean", ".ilean": lib + ".ilean", ".c": os.path.join(b, "ir", rel + ".c")}
        if self.header(module).is_module:
            out.update({".olean.server": lib + ".olean.server", ".olean.private": lib + ".olean.private",
                        ".ir.sig": lib + ".ir.sig", ".ir": lib + ".ir"})
        return out

    def _export_arts(self, module: str, all_arts: bool) -> list[list[str]]:
        """`ModuleExportInfo.arts` / `.allArts` (Lake `computeExportInfo`)."""
        loc = self.locate(module)
        base = os.path.join(loc.lib_dir, module_rel(module))
        if self.header(module).is_module:
            olean = [base + ".olean", base + ".olean.server"] + ([base + ".olean.private"] if all_arts else [])
            return [olean, [base + ".ir.sig", base + ".ir"]]
        return [[base + ".olean"]]

    def import_arts(self, module: str) -> dict[str, list[list[str]]]:
        """`fetchTransImportArts`: the artifacts of the transitively imported workspace modules."""
        h = self.header(module)
        non_module = not h.is_module
        s: dict[str, list[list[str]]] = {}
        for imp in h.imports:  # `ModuleImportInfo.addImport` (direct imports)
            if self.locate(imp.module) is None or imp.module == module:
                continue
            if non_module or imp.import_all:
                s[imp.module] = self._export_arts(imp.module, True)
            elif imp.module not in s:
                s[imp.module] = self._export_arts(imp.module, False)
        q: list[tuple[str, bool, bool]] = []
        for imp in reversed(h.imports):  # `directImports.foldrM`
            if self.locate(imp.module) is None:
                continue
            self._enqueue(non_module or imp.import_all, imp.is_meta, imp.module, q, non_module)
        if self.version >= (4, 35, 0):
            self._walk_435(s, q, non_module)
        else:
            self._walk_433(s, q, non_module)
        return s

    def _enqueue(self, import_all: bool, needs_meta: bool, of: str, q: list, non_module: bool) -> None:
        for imp in reversed(self.header(of).imports):  # `input.imports.foldr`, pushed onto the back
            if self.locate(imp.module) is None:
                continue
            reachable = import_all or imp.is_exported
            child_all = non_module or (import_all and imp.import_all)
            child_meta = needs_meta or (reachable and imp.is_meta)
            if reachable or child_meta:
                q.append((imp.module, child_all, child_meta))

    @staticmethod
    def _has(arts: list[list[str]], suffix: str) -> bool:
        return any(p.endswith(suffix) for p in arts[0])

    def _walk_435(self, s: dict, q: list, non_module: bool) -> None:
        all_visited: set[str] = set()
        meta_visited: set[str] = set()
        while q:
            mod, import_all, needs_meta = q.pop()
            do_all = import_all and mod not in all_visited
            do_meta = needs_meta and mod not in meta_visited
            existing = s.get(mod)
            if existing is not None and not (self._has(existing, ".olean.server") and (do_all or do_meta)):
                continue
            if import_all:
                all_visited.add(mod)
            if needs_meta:
                meta_visited.add(mod)
            want_all = mod in all_visited or (existing is not None and self._has(existing, ".olean.private"))
            s[mod] = self._export_arts(mod, want_all)
            self._enqueue(import_all, needs_meta, mod, q, non_module)

    def _walk_433(self, s: dict, q: list, non_module: bool) -> None:
        meta_visited: set[str] = set()
        while q:
            mod, import_all, needs_meta = q.pop()
            existing = s.get(mod)
            if existing is not None:
                nm = needs_meta and mod not in meta_visited
                if not ((import_all or nm) and self._has(existing, ".olean.server")
                        and not self._has(existing, ".olean.private")):
                    continue
            s[mod] = self._export_arts(mod, import_all)
            if import_all or needs_meta:
                meta_visited.add(mod)
            self._enqueue(import_all, needs_meta, mod, q, non_module)

    # --- the module's own configuration

    def module_config(self, module: str):
        lib = self.proj.lib_of(module)
        if lib is None:
            raise ProjectError(f"{module} is not a buildable module of any lean_lib of {self.proj.package}")
        return lib, self.proj.lean_options_of(lib), self.proj.lean_args_of(lib)

    def setup(self, module: str) -> dict:
        """The contents of the module's `.setup.json` (`mkModuleSetup`)."""
        _lib, options, _args = self.module_config(module)
        return {"name": module, "package": self.proj.package, "isModule": self.header(module).is_module,
                "importArts": self.import_arts(module), "dynlibs": [], "plugins": [], "options": options}

    def postpone_compile(self, module: str) -> bool:
        _lib, options, _args = self.module_config(module)
        return self.header(module).is_module and options.get("compiler.postponeCompile") is True

    def lean_command(self, module: str, outputs: dict[str, str], setup_path: str) -> list[str]:
        """`compileLeanModule`: arguments in Lake's order. `outputs` maps suffixes to paths."""
        loc = self.locate(module)
        _lib, _options, args = self.module_config(module)
        cmd = [self.lean_exe()] + list(args) + [loc.src, "-o", outputs[".olean"], "-i", outputs[".ilean"]]
        if not self.postpone_compile(module):
            cmd += ["-c", outputs[".c"]]
        return cmd + ["--setup", setup_path, "--json"]

    def leanir_command(self, outputs: dict[str, str], setup_path: str) -> list[str]:
        return [os.path.join(self.toolchain_bin, "leanir"), setup_path, outputs[".ir"], outputs[".c"]]

    def check_supported(self, graph=None) -> None:
        """Refuse settings the direct backend does not reproduce, in the libraries that are built."""
        used = {self.proj.lib_of(m).name for m in graph.modules if self.proj.lib_of(m)} if graph else None
        bad = list(self.proj.unsupported) + [u for lib in self.proj.libs if used is None or lib.name in used
                                             for u in lib.unsupported]
        if bad:
            raise ProjectError("the direct lean backend does not reproduce these Lake settings: " + ", ".join(bad))

    def check_imports(self, graph) -> None:
        """Every import from outside the project must be a built module of a dependency or of Lean
        itself (a dependency nothing imports, e.g. one used only by a tool, need not be built)."""
        core = os.path.join(os.path.dirname(self.toolchain_bin), "lib", "lean")
        missing = []
        for info in graph.modules.values():
            for x in info.external:
                if self.locate(x) is None and not os.path.exists(os.path.join(core, module_rel(x) + ".olean")):
                    missing.append(x)
        if missing:
            raise ProjectError(f"{len(set(missing))} imported modules are neither built in a dependency nor part of "
                               f"Lean, e.g. {sorted(set(missing))[:3]} (dependencies not built? e.g. `lake exe cache get`)")


def _norm_arts(arts: dict) -> dict:
    return {k: [[os.path.normpath(x) for x in part] for part in v] for k, v in arts.items()}


def compare_with_lake(ws: LakeWorkspace, modules: list[str], lake_build_dir: str, limit: int = 20) -> dict:
    """Compare the setup, command line and LEAN_PATH computed here with what Lake wrote.

    `lake_build_dir` must be the build directory of a real `lake build` of the same project
    (`ws.build_dir` should be the same directory, so that paths agree). Lake keeps
    `ir/<M>.setup.json`, and the `.trace` of each module it built logs the exact command line.
    """
    fields = ("name", "package", "isModule", "options", "dynlibs", "plugins", "importArts")
    counts = {f: 0 for f in fields + ("command", "lean_path")}
    checked = {"setup": 0, "command": 0}
    mismatches: list[dict] = []
    for m in modules:
        rel = module_rel(m)
        sp = os.path.join(lake_build_dir, "ir", rel + ".setup.json")
        if not os.path.exists(sp):
            continue
        with open(sp, encoding="utf-8") as fh:
            lake = json.load(fh)
        ours = ws.setup(m)
        checked["setup"] += 1
        for f in fields:
            a, b = lake.get(f, [] if f in ("dynlibs", "plugins") else None), ours.get(f)
            if f == "importArts":
                a, b = _norm_arts(a or {}), _norm_arts(b)
            if a != b:
                counts[f] += 1
                if len(mismatches) < limit:
                    d = {"module": m, "field": f}
                    if f == "importArts":
                        d["only_lake"] = sorted(set(a) - set(b))[:5]
                        d["only_ours"] = sorted(set(b) - set(a))[:5]
                        d["different"] = sorted(k for k in set(a) & set(b) if a[k] != b[k])[:5]
                    else:
                        d["lake"], d["ours"] = a, b
                    mismatches.append(d)
        tp = os.path.join(lake_build_dir, "lib", "lean", rel + ".trace")
        if not os.path.exists(tp):
            continue
        with open(tp, encoding="utf-8") as fh:
            trace = json.load(fh)
        msg = next((e.get("message", "") for e in trace.get("log", []) if "LEAN_PATH=" in e.get("message", "")), "")
        if not msg:
            continue
        line = msg.splitlines()[0]
        if line.startswith(".> "):
            line = line[3:]
        env, _, rest = line.partition(" ")
        checked["command"] += 1
        lp = env[len("LEAN_PATH="):]
        if lp != ws.lean_path_str():
            counts["lean_path"] += 1
            if len(mismatches) < limit:
                mismatches.append({"module": m, "field": "lean_path", "lake": lp, "ours": ws.lean_path_str()})
        ours_cmd = " ".join(ws.lean_command(m, ws.outputs(m, lake_build_dir), sp))
        if rest != ours_cmd:
            counts["command"] += 1
            if len(mismatches) < limit:
                mismatches.append({"module": m, "field": "command", "lake": rest, "ours": ours_cmd})
    return {"checked_setup_files": checked["setup"], "checked_commands": checked["command"],
            "mismatch_counts": counts, "mismatches": mismatches,
            "ok": checked["setup"] > 0 and not any(counts.values())}


__all__ = ["LakeWorkspace", "ModuleLoc", "Package", "compare_with_lake", "lean_version", "OUTPUT_SUFFIXES", "Import"]
