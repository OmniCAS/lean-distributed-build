"""A Lake project as data: its configuration, its modules and their import graph.

Only `lakefile.toml` is read (a `lakefile.lean` would have to be elaborated, i.e. run; convert it
with `lake translate-config toml` first). Source files are only scanned for their import headers.
"""
from __future__ import annotations

import os
import re
try:
    import tomllib
except ModuleNotFoundError:  # Python < 3.11 on a worker: the coordinator sends the parsed configuration
    tomllib = None
from dataclasses import dataclass, field

from .headers import parse_file


class ProjectError(Exception):
    pass


def toolchain_bin(project_dir: str, override: str | None = None) -> str:
    """Directory with `lean`, `lake`, `leanchecker` for the project's `lean-toolchain` (via elan)."""
    if override:
        return os.path.abspath(override)
    env = os.environ.get("LAKESHARD_TOOLCHAIN_BIN")
    if env:
        return env
    tc_file = os.path.join(project_dir, "lean-toolchain")
    if not os.path.exists(tc_file):
        raise ProjectError(f"no lean-toolchain in {project_dir}")
    tc = open(tc_file, encoding="utf-8").read().strip()
    name = tc.replace("/", "--").replace(":", "---")
    elan = os.environ.get("ELAN_HOME", os.path.expanduser("~/.elan"))
    path = os.path.join(elan, "toolchains", name, "bin")
    if not os.path.exists(os.path.join(path, "lake")):
        raise ProjectError(f"toolchain {tc} not installed at {path} (run `elan toolchain install {tc}`)")
    return path


def flatten_lean_options(v) -> dict:
    """Lake's TOML decoding of `leanOptions`: a table (nested tables give dotted names), or an array
    of `[name, value]` pairs or `{name, value}` tables. Values: string, boolean, natural number."""
    out: dict = {}

    def walk(prefix: str, x) -> None:
        if isinstance(x, dict):
            for k, y in x.items():
                walk(f"{prefix}.{k}" if prefix else k, y)
        else:
            out[prefix] = x

    if isinstance(v, dict):
        walk("", v)
    elif isinstance(v, list):
        for item in v:
            if isinstance(item, list) and len(item) == 2:
                out[str(item[0])] = item[1]
            elif isinstance(item, dict) and "name" in item:
                out[str(item["name"])] = item.get("value")
            else:
                raise ProjectError(f"cannot read leanOptions entry {item!r}")
    elif v is not None:
        raise ProjectError(f"leanOptions must be a table or an array, not {v!r}")
    return out


def _str_list(v) -> list[str]:
    if v is None:
        return []
    if isinstance(v, str):
        return [v]
    return [str(x) for x in v]


def name_is_prefix(prefix: str, name: str) -> bool:
    """`Lean.Name.isPrefixOf` on dotted names (by components)."""
    return name == prefix or name.startswith(prefix + ".")


def glob_matches(glob: str, mod: str) -> bool:
    """Lake globs: `A.B` (exactly), `A.B.+` (strict submodules), `A.B.*` (itself and submodules)."""
    if glob.endswith(".+"):
        return mod.startswith(glob[:-2] + ".")
    if glob.endswith(".*"):
        return name_is_prefix(glob[:-2], mod)
    return mod == glob


# Lake configuration keys the direct-`lean` backend does not reproduce (it refuses to run then).
DIRECT_UNSUPPORTED_KEYS = ("precompileModules", "dynlibs", "plugins", "extraDepTargets", "needs",
                           "nativeFacets", "defaultFacets")


@dataclass
class LeanLib:
    name: str
    src_dir: str  # relative to the package source directory
    roots: list[str]
    globs: list[str]
    lean_options: dict = field(default_factory=dict)  # flattened (dotted names)
    more_lean_args: list[str] = field(default_factory=list)
    weak_lean_args: list[str] = field(default_factory=list)
    build_type: str = ""  # "" = the package's
    unsupported: list[str] = field(default_factory=list)

    def is_buildable(self, mod: str) -> bool:
        """`LeanLibConfig.isBuildableModule`."""
        return (any(glob_matches(g, mod) for g in self.globs)
                or any(name_is_prefix(r, mod) and any(glob_matches(g, r) for g in self.globs)
                       for r in self.roots))


@dataclass
class ModuleInfo:
    name: str
    path: str  # source file, relative to the project directory
    imports: list[str]  # internal imports (modules of this project)
    external: list[str]  # imports from dependencies (Mathlib, ...)
    lines: int
    bytes: int


@dataclass
class ProjectGraph:
    project_dir: str
    package: str
    modules: dict[str, ModuleInfo]
    order: list[str]  # topological order: every module after its imports
    targets: list[str]  # modules selected by the default targets' globs

    def children(self) -> dict[str, list[str]]:
        ch: dict[str, list[str]] = {m: [] for m in self.modules}
        for m, info in self.modules.items():
            for u in info.imports:
                ch[u].append(m)
        return ch

    def depth(self) -> dict[str, int]:
        d: dict[str, int] = {}
        for m in self.order:
            d[m] = 1 + max((d[u] for u in self.modules[m].imports), default=0)
        return d

    def closure_sizes(self, chunk: int = 1 << 15) -> dict[str, int]:
        """Number of project modules each module imports, directly or not.

        Bitset propagation in topological order, `chunk` target modules at a time, so memory
        stays at about n * chunk / 8 bytes even for graphs with hundreds of thousands of modules.
        """
        pos = {m: i for i, m in enumerate(self.order)}
        n = len(self.order)
        sizes = dict.fromkeys(self.order, 0)
        for start in range(0, n, chunk):
            end = min(n, start + chunk)
            reach: dict[str, int] = {}
            for m in self.order:
                acc = 0
                for u in self.modules[m].imports:
                    pu = pos[u]
                    acc |= reach[u] | ((1 << (pu - start)) if start <= pu < end else 0)
                reach[m] = acc
            for m, r in reach.items():
                sizes[m] += r.bit_count()
        return sizes

    def closure(self, roots) -> set[str]:
        seen: set[str] = set()
        stack = list(roots)
        while stack:
            v = stack.pop()
            for u in self.modules[v].imports:
                if u not in seen:
                    seen.add(u)
                    stack.append(u)
        return seen


@dataclass
class LakeProject:
    project_dir: str
    lakefile: str
    package: str
    src_dir: str
    build_dir: str
    libs: list[LeanLib]
    default_targets: list[str]
    lean_options: dict  # flattened (dotted names)
    more_lean_args: list[str] = field(default_factory=list)
    weak_lean_args: list[str] = field(default_factory=list)
    build_type: str = "release"
    unsupported: list[str] = field(default_factory=list)  # keys the direct backend cannot reproduce

    @staticmethod
    def load(project_dir: str, config: str | None = None, data: dict | None = None) -> "LakeProject":
        """Read `lakefile.toml`, or `config`, or for a `lakefile.lean` project the translation
        `lakeshard translate` wrote to `.lake/lakeshard/lakefile.toml` (see `translated_config`)."""
        project_dir = os.path.abspath(project_dir)
        toml_path = config or os.path.join(project_dir, "lakefile.toml")
        if data is None and not os.path.exists(toml_path):
            lean_cfg = os.path.join(project_dir, "lakefile.lean")
            if os.path.exists(lean_cfg):
                tr = translated_config(project_dir)
                if not os.path.exists(tr) or os.path.getmtime(tr) < os.path.getmtime(lean_cfg):
                    raise ProjectError(f"{project_dir} is configured with lakefile.lean: run `lakeshard translate "
                                       f"{project_dir}` first (it runs Lake on lakefile.lean)")
                toml_path = tr
            else:
                raise ProjectError(f"no lakefile.toml in {project_dir}")
        if data is not None:
            cfg = data  # already parsed (sent by the coordinator to a worker without tomllib)
        else:
            if tomllib is None:
                raise ProjectError("reading lakefile.toml needs Python 3.11 (tomllib)")
            with open(toml_path, "rb") as fh:
                cfg = tomllib.load(fh)
        name = cfg.get("name")
        if not name:
            raise ProjectError("lakefile.toml has no package name")
        libs = []
        for lib in cfg.get("lean_lib", []):
            roots = lib.get("roots") or [lib["name"]]
            if isinstance(roots, str):
                roots = [roots]
            globs = lib.get("globs") or list(roots)
            if isinstance(globs, str):
                globs = [globs]
            libs.append(LeanLib(lib["name"], lib.get("srcDir", "."), list(roots), list(globs),
                                flatten_lean_options(lib.get("leanOptions")),
                                _str_list(lib.get("moreLeanArgs")), _str_list(lib.get("weakLeanArgs")),
                                str(lib.get("buildType", "")),
                                [f"lean_lib {lib['name']}: {k}" for k in DIRECT_UNSUPPORTED_KEYS if k in lib]))
        dt = cfg.get("defaultTargets") or [l.name for l in libs]
        unsupported = [k for k in DIRECT_UNSUPPORTED_KEYS if k in cfg]  # other target kinds are ignored
        return LakeProject(project_dir, toml_path, name, cfg.get("srcDir", "."),
                           cfg.get("buildDir", os.path.join(".lake", "build")), libs, list(dt),
                           flatten_lean_options(cfg.get("leanOptions")),
                           _str_list(cfg.get("moreLeanArgs")), _str_list(cfg.get("weakLeanArgs")),
                           str(cfg.get("buildType", "release")), unsupported)

    # --- per-module configuration, as Lake computes it (Lake/Config/{Module,LeanLib}.lean, 4.33-4.35)

    def lib_of(self, module: str) -> LeanLib | None:
        """The library a module belongs to: `Package.findModule?` searches the libraries last to first."""
        for lib in reversed(self.libs):
            if lib.is_buildable(module):
                return lib
        return None

    def lib_src_root(self, lib: LeanLib) -> str:
        return os.path.normpath(os.path.join(self.project_dir, self.src_dir, lib.src_dir))

    def lean_options_of(self, lib: LeanLib) -> dict:
        """buildType options ++ package `leanOptions` ++ library `leanOptions` (later entries win)."""
        bt = (lib.build_type or self.build_type or "release").lower()
        out: dict = {"debugAssertions": True} if bt == "debug" else {}
        out.update(self.lean_options)
        out.update(lib.lean_options)
        return out

    def lean_args_of(self, lib: LeanLib) -> list[str]:
        """`weakLeanArgs` (package, library) then `moreLeanArgs` (package, library), as Lake passes them."""
        return self.weak_lean_args + lib.weak_lean_args + self.more_lean_args + lib.more_lean_args

    # --- modules

    def _src_roots(self) -> list[str]:
        roots = []
        for lib in self.libs:
            r = os.path.normpath(os.path.join(self.project_dir, self.src_dir, lib.src_dir))
            if r not in roots:
                roots.append(r)
        if not roots:
            roots.append(os.path.normpath(os.path.join(self.project_dir, self.src_dir)))
        return roots

    def _find(self, module: str) -> str | None:
        rel = os.path.join(*module.split(".")) + ".lean"
        for r in self._src_roots():
            p = os.path.join(r, rel)
            if os.path.isfile(p):
                return p
        return None

    def _glob(self, lib: LeanLib, glob: str) -> list[str]:
        root = os.path.normpath(os.path.join(self.project_dir, self.src_dir, lib.src_dir))
        if glob.endswith(".+") or glob.endswith(".*"):
            base = glob[:-2]
            out = [base] if glob.endswith(".*") and self._find(base) else []
            d = os.path.join(root, *base.split("."))
            for dp, _dn, fns in os.walk(d):
                for fn in fns:
                    if fn.endswith(".lean"):
                        rel = os.path.relpath(os.path.join(dp, fn), root)[:-5]
                        out.append(".".join(rel.split(os.sep)))
            return sorted(out)
        return [glob] if self._find(glob) else []

    def graph(self, targets: list[str] | None = None) -> ProjectGraph:
        """The import graph of the default targets' modules, or of the given modules (each with its
        whole project import closure), e.g. one Mathlib module and everything it needs."""
        if targets:
            missing = [m for m in targets if self._find(m) is None]
            if missing:
                raise ProjectError(f"no source file for target modules {missing[:5]}")
            targets = list(dict.fromkeys(targets))
        else:
            targets = []
            for lib in self.libs:
                if lib.name not in self.default_targets:
                    continue
                for g in lib.globs:
                    for m in self._glob(lib, g):
                        if m not in targets:
                            targets.append(m)
        if not targets:
            raise ProjectError("no modules found for the default targets")
        mods: dict[str, ModuleInfo] = {}
        stack = list(targets)
        while stack:
            m = stack.pop()
            if m in mods:
                continue
            p = self._find(m)
            if p is None:
                continue
            imps, nl, nb = parse_file(p)
            internal, external = [], []
            for x in imps:
                (internal if self._find(x) else external).append(x)
            internal = sorted(set(internal))
            mods[m] = ModuleInfo(m, os.path.relpath(p, self.project_dir), internal, sorted(set(external)), nl, nb)
            stack.extend(u for u in internal if u not in mods)
        # topological order (Kahn), deterministic
        indeg = {m: len(i.imports) for m, i in mods.items()}
        ch: dict[str, list[str]] = {m: [] for m in mods}
        for m, i in mods.items():
            for u in i.imports:
                ch[u].append(m)
        ready = sorted(m for m, d in indeg.items() if d == 0)
        order = []
        while ready:
            nxt = []
            for u in ready:
                order.append(u)
                for v in ch[u]:
                    indeg[v] -= 1
                    if indeg[v] == 0:
                        nxt.append(v)
            ready = sorted(nxt)
        if len(order) != len(mods):
            raise ProjectError("import cycle among: " + ", ".join(sorted(m for m in mods if indeg[m] > 0)[:10]))
        return ProjectGraph(self.project_dir, self.package, mods, order, targets)

    # --- build directories

    def worker_lakefile(self, build_dir: str) -> str:
        """The project's lakefile.toml with `buildDir` set to an absolute directory."""
        text = open(self.lakefile, encoding="utf-8").read()
        lines = text.splitlines()
        out, in_table = [], False
        for ln in lines:
            if re.match(r"^\s*\[", ln):
                in_table = True
            if not in_table and re.match(r"^\s*buildDir\s*=", ln):
                continue
            out.append(ln)
        return f"buildDir = {quote_toml(os.path.abspath(build_dir))}\n" + "\n".join(out) + "\n"


def translated_config(project_dir: str) -> str:
    """Where `lakeshard translate` keeps the TOML translation of a project's `lakefile.lean`
    (inside Lake's own `.lake` directory; the project's files are not touched)."""
    return os.path.join(os.path.abspath(project_dir), ".lake", "lakeshard", "lakefile.toml")


def translate(project_dir: str, toolchain_bin: str) -> str:
    """`lake translate-config toml` of a `lakefile.lean` project (runs Lake, i.e. the configuration's
    Lean code; Lake documents the translation as lossy for non-declarative configuration, so the
    result is checked against real Lake builds: `check-setup`, and the restore's `--no-build`)."""
    import subprocess
    project_dir = os.path.abspath(project_dir)
    out = translated_config(project_dir)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    tmp = out + ".new"
    if os.path.exists(tmp):
        os.remove(tmp)
    env = dict(os.environ)
    env["PATH"] = toolchain_bin + os.pathsep + env.get("PATH", "")
    env.pop("LEAN_PATH", None)
    r = subprocess.run([os.path.join(toolchain_bin, "lake"), "translate-config", "toml", tmp], cwd=project_dir,
                       env=env, capture_output=True, text=True)
    if r.returncode != 0 or not os.path.exists(tmp):
        raise ProjectError(f"lake translate-config failed: {(r.stdout + r.stderr)[-1000:]}")
    os.replace(tmp, out)
    return out


def quote_toml(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def module_rel(module: str) -> str:
    return os.path.join(*module.split("."))


def module_output_files(build_dir: str, module: str) -> list[str]:
    """Paths (relative to build_dir) of the files Lake wrote for `module`, except `.setup.json`."""
    rel = module_rel(module)
    out = []
    for sub in ("lib/lean", "ir"):
        d = os.path.join(build_dir, sub, os.path.dirname(rel))
        base = os.path.basename(rel) + "."
        if not os.path.isdir(d):
            continue
        for fn in os.listdir(d):
            if fn.startswith(base) and not fn.endswith(".setup.json") and ".tmp" not in fn[len(base):]:
                full = os.path.join(d, fn)
                if os.path.isfile(full):
                    out.append(os.path.relpath(full, build_dir))
    return sorted(out)
