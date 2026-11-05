#!/usr/bin/env python3
"""Regenerate the engine's ledger tables, brier.md, scores.md and the site data from archived files, and check them.

    python3 reproduce.py                  # regenerate in a scratch folder, compare with what is committed
    python3 reproduce.py --write          # also write brier.md and scores.md in place
    python3 reproduce.py --site-out DIR   # keep the laid-out site in DIR (default: a temporary folder, deleted)
    python3 reproduce.py --program-1 PY   # also run programs/entangled-mind/experiments/reproduce.py with interpreter PY
                                          #   (it needs that program's environment, e.g. /Users/seanpharris/entangled-mind/.venv/bin/python)

In plain English: every number the engine publishes about itself is computed from files in this repository. This
script recomputes all of them from those files, with no API key, no network and nothing but the Python standard
library, and says whether what is committed matches. It changes nothing unless asked to (--write).

What it does, in order:
  1. Reads every ledger file (bets, steers, human odds, shadows, plants, lessons, spend) and checks that each line
     parses, ids are unique, and every audit path, steer evidence path and plant reference points at a file that exists.
  2. Copies ledger/ to a scratch folder, runs ledger/brier.py and ledger/scores.py there, and compares brier.md and
     scores.md byte for byte with the committed ones.
  3. Recomputes the engine's and the human's Brier scores from bets.jsonl with separate code, and checks the
     headline numbers printed in brier.md.
  4. Runs `ledger/plants.py verify` (every revealed plant matches its sealed hash).
  5. Lays out the site with site/assemble.sh and checks that every data file the pages read is a byte-identical copy
     of its source (links followed), that the manifest lists what was copied, and that every bet's audit link resolves.
Exit 0 if everything reproduces, 1 otherwise. The last line says which.
"""
import argparse
import filecmp
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LEDGER = ROOT / "ledger"
JSONL = ["bets", "steers", "human-odds", "shadows", "plants", "lessons", "spend"]
# A clean environment: no keys, no tokens, nothing inherited that a script could lean on.
CLEAN_ENV = {"PATH": "/usr/bin:/bin:/usr/sbin:/sbin", "HOME": os.environ.get("HOME", "/tmp"), "LANG": "en_US.UTF-8",
             "TZ": "America/Denver", "PYTHONDONTWRITEBYTECODE": "1"}

problems, notes = [], []


def fail(msg):
    problems.append(msg)
    print(f"  FAIL  {msg}")


def ok(msg):
    print(f"  ok    {msg}")


def note(msg):
    notes.append(msg)
    print(f"  note  {msg}")


def run(cmd, cwd=ROOT):
    return subprocess.run(cmd, cwd=cwd, env=CLEAN_ENV, capture_output=True, text=True)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()[:12]


# ---------- 1. the ledger files ----------
def read_ledger():
    print("1. Ledger files")
    rows = {}
    for name in JSONL:
        p = LEDGER / f"{name}.jsonl"
        if not p.exists():
            fail(f"ledger/{name}.jsonl is missing")
            rows[name] = []
            continue
        out = []
        for i, line in enumerate(p.read_text().splitlines(), 1):
            if not line.strip():
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError as e:
                fail(f"ledger/{name}.jsonl line {i} does not parse: {e}")
        ids = [r.get("id") for r in out if r.get("id")]
        dup = sorted({i for i in ids if ids.count(i) > 1})
        if dup:
            fail(f"ledger/{name}.jsonl repeats ids: {', '.join(dup)}")
        rows[name] = out
        ok(f"ledger/{name}.jsonl: {len(out)} line(s)")
    bets = rows["bets"]
    for b in bets:
        ap = b.get("audit_path")
        if ap and not (ROOT / ap).is_file():
            fail(f"{b['id']}: audit_path {ap} does not resolve")
        rf = b.get("result_file")
        prog = ROOT / "programs" / b.get("program", "")
        if rf and not (prog / rf).is_file():
            note(f"{b['id']}: result_file programs/{b.get('program')}/{rf} is not in this checkout ({b.get('branch') or 'branch not stated'})")
    audited = [b for b in bets if b.get("audit_path")]
    if not any("audit_path" in p for p in problems):
        ok(f"{len(audited)} of {len(bets)} bets carry an audit; every audit path resolves")
    # Sean's cockpit odds (rule 11, st-18): a line committed before a bet's pre-registration must be in its row.
    sys.path.insert(0, str(LEDGER))
    import human_odds_match as hom
    ho_rows, ho_arr = hom.lines(), hom.arrivals()
    missing = [msg for ok_, msg in (hom.check_bet(b, ho_rows, ho_arr) for b in bets) if ok_ is False]
    for msg in missing:
        fail(msg)
    if not missing:
        ok(f"human odds: every bet pre-registered after a cockpit line for its direction carries it ({len(ho_rows)} line(s))")
    for s in rows["steers"]:
        for ev in s.get("evidence") or []:
            path = ev.split(" ")[0]
            if path.startswith(("ledger/", "map/", "operators/")) and not (ROOT / path).exists():
                note(f"{s['id']}: evidence {path} not found")
    return rows


# ---------- 2. regenerate brier.md and scores.md ----------
def regenerate(write):
    print("2. brier.md and scores.md, regenerated in a scratch copy of ledger/")
    tmp = Path(tempfile.mkdtemp(prefix="reproduce-ledger-"))
    try:
        scratch = tmp / "ledger"
        shutil.copytree(LEDGER, scratch, symlinks=True,
                        ignore=shutil.ignore_patterns("__pycache__", ".seals", "*.pyc"))
        for script in ("brier.py", "scores.py"):
            r = run([sys.executable, str(scratch / script)], cwd=tmp)
            if r.returncode:
                fail(f"ledger/{script} exited {r.returncode}: {r.stderr.strip()[-300:]}")
            else:
                ok(f"ledger/{script}: {r.stdout.strip().splitlines()[-1] if r.stdout.strip() else 'ran'}")
        for md in ("brier.md", "scores.md"):
            new, old = scratch / md, LEDGER / md
            if not new.exists():
                fail(f"{md} was not written")
            elif old.exists() and filecmp.cmp(new, old, shallow=False):
                ok(f"ledger/{md} reproduces byte for byte (sha256 {sha(old)})")
            else:
                if write:
                    shutil.copyfile(new, old)
                    note(f"ledger/{md} differed from the committed copy; rewritten in place (--write)")
                else:
                    fail(f"ledger/{md} differs from what the ledger generates; run with --write and commit")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ---------- 3. the Brier scores, recomputed independently ----------
def brier_check(bets):
    print("3. Brier scores, recomputed from bets.jsonl with separate code")
    sc = [b for b in bets if b.get("scored") and b.get("engine_odds") is not None and b.get("outcome") in (0, 1)]
    if not sc:
        fail("no scored bets")
        return
    eng = sum((b["engine_odds"] - b["outcome"]) ** 2 for b in sc) / len(sc)
    hits = sum(b["outcome"] for b in sc)
    base = hits / len(sc)
    clim = sum((base - b["outcome"]) ** 2 for b in sc) / len(sc)
    hum = [b for b in sc if b.get("human_odds") is not None]
    md = (LEDGER / "brier.md").read_text()
    m = re.search(r"engine's Brier score is ([0-9]+\.[0-9]+)", md)
    stated = float(m.group(1)) if m else None
    if stated is None:
        fail("brier.md: headline engine Brier not found")
    elif abs(stated - round(eng, 3)) > 1e-9:
        fail(f"brier.md says engine Brier {stated}, recomputed {eng:.3f}")
    else:
        ok(f"engine Brier {eng:.3f} on {len(sc)} scored bets ({hits} hits); hit-rate baseline {clim:.3f}; matches brier.md")
    if hum:
        h = sum((b["human_odds"] - b["outcome"]) ** 2 for b in hum) / len(hum)
        ok(f"human Brier {h:.3f} on {len(hum)} bets")
    else:
        ok("human Brier: no scored bet has human odds yet (ledger/human-odds.jsonl is the only source; its lines wait for their bets)")


# ---------- 4. plants ----------
def plants_check():
    print("4. Sealed plants")
    r = run([sys.executable, str(LEDGER / "plants.py"), "verify"])
    if r.returncode:
        fail(f"plants.py verify exited {r.returncode}: {(r.stdout + r.stderr).strip()[-300:]}")
    else:
        for line in r.stdout.strip().splitlines():
            ok(line)


# ---------- 5. the site data ----------
def site_check(out_dir, bets):
    print("5. Site data, laid out by site/assemble.sh")
    keep = out_dir is not None
    out = Path(out_dir) if keep else Path(tempfile.mkdtemp(prefix="reproduce-site-"))
    if out.exists() and keep:
        shutil.rmtree(out)
    try:
        r = run(["bash", str(ROOT / "site" / "assemble.sh"), str(out),
                 str(ROOT / "programs" / "entangled-mind"), str(ROOT / "programs" / "nature-graded")])
        if r.returncode:
            fail(f"site/assemble.sh exited {r.returncode}: {r.stderr.strip()[-300:]}")
            return
        ok(r.stdout.strip().splitlines()[-1])
        data = out / "data"
        pairs = [(data / "ledger", LEDGER), (data / "map", ROOT / "map"),
                 (data / "programs/entangled-mind/paper", ROOT / "programs/entangled-mind/paper")]
        n = bad = 0
        for dst, src in pairs:
            for f in sorted(p for p in src.rglob("*") if p.is_file() or p.is_symlink()):
                if "__pycache__" in f.parts or ".seals" in f.parts:
                    continue
                rel = f.relative_to(src)
                d = dst / rel
                n += 1
                if not d.is_file() or d.is_symlink():
                    bad += 1
                    fail(f"site data/{d.relative_to(data)} missing or still a link")
                elif not filecmp.cmp(f.resolve(), d, shallow=False):
                    bad += 1
                    fail(f"site data/{d.relative_to(data)} differs from {f.relative_to(ROOT)}")
        for name in ("README.md", "proposal.md", "CONTEXT.md"):
            n += 1
            if not filecmp.cmp(ROOT / name, data / "engine" / name, shallow=False):
                bad += 1
                fail(f"site data/engine/{name} differs from {name}")
        if not bad:
            ok(f"{n} data files are byte-identical copies of their sources (links followed)")
        man = json.loads((data / "manifest.json").read_text())
        listed = set(man.get("audits", []))
        have = {p.name for p in (data / "ledger" / "audits").glob("*.md")}
        if listed != have:
            fail(f"manifest audits {len(listed)} != files {len(have)}")
        else:
            ok(f"manifest lists {len(man['map'])} maps, {len(man['papers'])} papers, {len(listed)} audit files")
        dangling = [b["id"] for b in bets if b.get("audit_path") and not (data / b["audit_path"]).is_file()]
        if dangling:
            fail(f"audit links that would 404 on the site: {', '.join(dangling)}")
        else:
            ok("every bet's audit link resolves in the laid-out site")
        for page in ("index.html", "map.html", "cockpit.html", "calibration.html", "instruments.html", "kills.html"):
            if not (out / page).is_file():
                fail(f"site page {page} missing")
        svg = re.findall(r'src="([^"]+\.svg)"', (out / "index.html").read_text())
        for s in svg:
            if not (out / s).is_file():
                fail(f"index.html points at {s}, which the layout does not contain")
        if svg:
            ok(f"home page images present: {', '.join(svg)}")
    finally:
        if not keep:
            shutil.rmtree(out, ignore_errors=True)
        else:
            print(f"  kept  {out}")


def program_1(py):
    print("6. Program 1's own tables (programs/entangled-mind/experiments/reproduce.py)")
    em = ROOT / "programs" / "entangled-mind"
    env = dict(CLEAN_ENV, PYTHONPATH=str(em / "src"))
    r = subprocess.run([py, "experiments/reproduce.py"], cwd=em, env=env, capture_output=True, text=True)
    tail = (r.stdout + r.stderr).strip().splitlines()[-1:] or ["(no output)"]
    (ok if r.returncode == 0 else fail)(f"exit {r.returncode}: {tail[0]}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--write", action="store_true", help="write regenerated brier.md and scores.md in place")
    ap.add_argument("--site-out", help="keep the laid-out site in this folder")
    ap.add_argument("--program-1", metavar="PYTHON", help="also run program 1's reproduce.py with this interpreter")
    a = ap.parse_args()
    leaked = [k for k in os.environ if re.search(r"API_KEY|TOKEN|SECRET", k)]
    print(f"reproduce.py at {ROOT.name}, no network, no keys (child processes run with a clean environment"
          f"{'; ' + str(len(leaked)) + ' key-like variable(s) in this shell are not passed on' if leaked else ''})")
    rows = read_ledger()
    regenerate(a.write)
    brier_check(rows["bets"])
    plants_check()
    site_check(a.site_out, rows["bets"])
    if a.program_1:
        program_1(a.program_1)
    print()
    if problems:
        print(f"NOT REPRODUCED: {len(problems)} problem(s), {len(notes)} note(s)")
        sys.exit(1)
    print(f"ALL LEDGER TABLES AND SITE DATA REPRODUCED ({len(notes)} note(s))")


if __name__ == "__main__":
    main()
