"""Shared harness for every program's reproduce.py (programs/<name>/reproduce.py).

In plain English: a program's reproduce.py rebuilds each results table from the JSON archived in the repository and
checks it against the committed table. This module does the parts every program needs in the same way:

  1. snapshot(): copies the program's files as they are at git HEAD into a temporary folder (`git archive`), so files
     a running session has not committed cannot leak in, and so nothing is written into the working tree;
  2. lockdown(): removes key-like environment variables and blocks the network (socket), and serves a stub for every
     package outside the standard library and numpy (anthropic, dotenv, qiskit, scipy, ...). A stub imports, so a
     module whose table writer needs only json can be loaded; anything that touches it raises at once, so no table
     can quietly depend on an API call, a simulator or a package a clean environment does not have;
  3. Report: each table is recorded as matched, mismatched, skipped (not a table: a log, a refusal record), or a gap
     (the table needs a file the archive does not contain; the README says so under "Reproducibility"). Every file in
     the program's results folders must be registered one of these ways, so a new results file nobody taught the script
     about fails instead of passing unseen.

Last line of output, and exit status:
  ALL TABLES REPRODUCED (...)                              exit 0
  PARTLY REPRODUCED: ... (documented gaps, README)         exit 2   every table that can be rebuilt matched
  NOT REPRODUCED: first mismatch <file>: <what differs>    exit 1

Standard library only (numpy is imported by the programs' own code, not here).
"""
import difflib
import importlib.abc
import importlib.machinery
import io
import os
import re
import shutil
import socket
import subprocess
import sys
import tarfile
import tempfile
import types
from pathlib import Path

ENGINE = Path(__file__).resolve().parents[1]

# Packages a clean environment does not have. numpy is allowed; everything else outside the standard library is stubbed.
STUBBED = ("anthropic", "dotenv", "qiskit", "qiskit_aer", "qiskit_ibm_runtime", "scipy", "rustworkx", "httpx",
           "requests", "matplotlib", "pandas", "sklearn", "torch", "transformers", "openai", "entangled_mind.llm",
           "entangled_mind.backends")


class Blocked(RuntimeError):
    pass


def _blocked(what):
    def f(*_a, **_k):
        raise Blocked(f"reproduce: {what} is blocked (tables must come from archived JSON, stdlib and numpy only)")
    return f


class _Stub(types.ModuleType):
    """A module that imports but raises on any real use. `load_dotenv` is a no-op: loading keys is what we refuse."""

    def __getattr__(self, name):
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)
        if name == "load_dotenv":
            return lambda *a, **k: False
        return _StubObject(f"{self.__name__}.{name}")


class _StubObject:
    def __init__(self, name):
        self._name = name

    def __call__(self, *a, **k):
        raise Blocked(f"reproduce: {self._name} was called; it is not available in a clean environment "
                      "(stdlib and numpy only)")

    def __getattr__(self, name):
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)
        return _StubObject(f"{self._name}.{name}")

    def __mro_entries__(self, bases):          # `class X(stubbed.Base)` still defines X; using it raises
        return (object,)

    def __repr__(self):
        return f"<blocked {self._name}>"


class _StubFinder(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    def __init__(self, names):
        self.names = tuple(names)

    def find_spec(self, fullname, path=None, target=None):
        if any(fullname == n or fullname.startswith(n + ".") for n in self.names):
            return importlib.machinery.ModuleSpec(fullname, self, is_package=True)
        return None

    def create_module(self, spec):
        m = _Stub(spec.name)
        m.__path__ = []
        return m

    def exec_module(self, module):
        pass


def lockdown(extra_stubs=()):
    """No keys, no network, no packages beyond the standard library and numpy."""
    for k in list(os.environ):
        if re.search(r"API_KEY|TOKEN|SECRET|ANTHROPIC|IBM_QUANTUM|QISKIT_IBM", k):
            os.environ.pop(k)
    class _NoSocket(socket.socket):           # a class, so modules that subclass socket (ssl) still import
        def __init__(self, *a, **k):
            raise Blocked("reproduce: network access (socket) is blocked")
    socket.socket = _NoSocket
    socket.create_connection = _blocked("network access (create_connection)")
    socket.getaddrinfo = _blocked("network access (getaddrinfo)")
    names = STUBBED + tuple(extra_stubs)
    for n in list(sys.modules):
        if any(n == s or n.startswith(s + ".") for s in names):
            del sys.modules[n]
    sys.meta_path.insert(0, _StubFinder(names))


def snapshot(paths):
    """Extract `paths` (repo-relative) as they are at git HEAD into a fresh temporary folder; return its root."""
    tmp = Path(tempfile.mkdtemp(prefix="reproduce-"))
    data = subprocess.run(["git", "-C", str(ENGINE), "archive", "HEAD", "--", *paths],
                          check=True, capture_output=True).stdout
    with tarfile.open(fileobj=io.BytesIO(data)) as tf:
        tf.extractall(tmp, filter="data")
    return tmp


def tables_of(text):
    """The markdown tables in a text, each as a list of its lines (rows starting with '|')."""
    out, cur = [], []
    for line in text.splitlines():
        if line.lstrip().startswith("|"):
            cur.append(line.rstrip())
        elif cur:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def quiet(fn, *a, **k):
    """Run a writer with its printing captured; return (result, captured stdout)."""
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        return fn(*a, **k), buf.getvalue()
    finally:
        sys.stdout = old


class Report:
    def __init__(self, program, root, results_globs=("results/*.md",)):
        """`root` is the program folder inside the snapshot; `results_globs` name every file that must be registered."""
        self.program, self.root = program, Path(root)
        self.expected = sorted({p.relative_to(self.root).as_posix()
                                for g in results_globs for p in self.root.glob(g) if p.is_file()})
        self.seen, self.rows = set(), []      # rows: (kind, name, detail)

    # ----- recording -----
    def _row(self, kind, name, detail=""):
        self.seen.add(name)
        self.rows.append((kind, name, detail))
        label = {"match": "match", "diff": "DIFF ", "skip": "skip ", "gap": "GAP  ", "error": "FAIL "}[kind]
        print(f"  {label} {name}{('  (' + detail + ')') if detail else ''}")

    def compare(self, name, committed, regenerated, what="file"):
        """Byte comparison of two texts (or of two lists of table lines). Records match or diff."""
        if isinstance(committed, list):
            committed, regenerated = "\n".join(committed), "\n".join(regenerated)
        if committed == regenerated:
            self._row("match", name, what if what != "file" else "")
            return True
        d = [l for l in difflib.unified_diff(committed.splitlines(), regenerated.splitlines(), "committed",
                                             "regenerated", n=0, lineterm="")][2:]
        first = next((l for l in d if l.startswith(("-", "+"))), "(whitespace or line endings)")
        self._row("diff", name, f"{what}: {first[:160]}")
        for l in d[:8]:
            print(f"          {l[:200]}")
        return False

    def compare_tables(self, name, committed_text, regenerated_tables, which=None):
        """Every regenerated table must appear, line for line, among the committed file's tables.
        `which` (optional) is a list of indices into the committed file's tables, one per regenerated table."""
        have = tables_of(committed_text)
        ok = True
        for i, t in enumerate(regenerated_tables):
            if which is not None:
                j = which[i]
                if j >= len(have):
                    self._row("diff", name, f"table {j + 1} is missing from the committed file")
                    return False
                if have[j] != t:
                    return self.compare(name, have[j], t, what=f"table {j + 1}")
            elif t not in have:
                near = max(have, key=lambda h: difflib.SequenceMatcher(None, "\n".join(h), "\n".join(t)).ratio(),
                           default=[])
                return self.compare(name, near, t, what=f"regenerated table {i + 1} (nearest committed table shown)")
        self._row("match", name, f"{len(regenerated_tables)} table(s)")
        return ok

    def skip(self, name, reason):
        """Not a table: a log, a refusal record, a call cache. Stated, never silently ignored."""
        self._row("skip", name, reason)

    def gap(self, name, reason, missing=()):
        """The table needs a file the archive does not have. Checks the file really is absent: if it has since been
        committed, the gap is stale and is reported as a failure so someone teaches the script to rebuild it."""
        present = [m for m in missing if (self.root / m).exists()]
        if present:
            self._row("error", name, f"listed as a gap, but {', '.join(present)} is now archived: rebuild it")
        else:
            self._row("gap", name, reason)

    def error(self, name, exc):
        self._row("error", name, f"{type(exc).__name__}: {exc}"[:300])

    def run(self, name, fn):
        """Call fn() with its printing captured; on an exception record it against `name` and return None."""
        try:
            return quiet(fn)[0]
        except Exception as e:  # noqa: BLE001
            self.error(name, e)
            return None

    # ----- summary -----
    def finish(self):
        for name in self.expected:
            if name not in self.seen:
                self._row("error", name, "results file not registered in reproduce.py (rebuild it, or list it as a "
                                         "skip or a gap with a reason)")
        bad = [r for r in self.rows if r[0] in ("diff", "error")]
        tables = [r for r in self.rows if r[0] in ("match", "diff", "gap", "error")]
        matched = [r for r in self.rows if r[0] == "match"]
        gaps = [r for r in self.rows if r[0] == "gap"]
        skips = [r for r in self.rows if r[0] == "skip"]
        print()
        if bad:
            k, name, detail = bad[0]
            print(f"NOT REPRODUCED: first mismatch {name}: {detail}"
                  + (f" ({len(bad) - 1} more)" if len(bad) > 1 else ""))
            return 1
        if gaps:
            print(f"PARTLY REPRODUCED: {len(matched)} of {len(tables)} table file(s) rebuilt and matched; "
                  f"{len(gaps)} need file(s) the archive lacks ({', '.join(g[1] for g in gaps)}; README, "
                  f"Reproducibility){'; ' + str(len(skips)) + ' log(s) skipped' if skips else ''}")
            return 2
        print(f"ALL TABLES REPRODUCED ({len(matched)} table file(s)"
              + (f"; {len(skips)} non-table file(s) skipped with reasons" if skips else "")
              + ("; no results tables written yet" if not tables else "") + ")")
        return 0


def main_guard(fn):
    """Run a program's main(snapshot_root) with lockdown and cleanup; exit with its status."""
    lockdown()
    sys.dont_write_bytecode = True
    code = 1
    try:
        code = fn()
    finally:
        sys.stdout.flush()
    sys.exit(code)


def cleanup(tmp):
    shutil.rmtree(tmp, ignore_errors=True)
