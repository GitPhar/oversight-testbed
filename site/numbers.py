"""Fill the ledger numbers in the front-page documents from the generated ledger pages. No network, no keys.

    python3 site/numbers.py            # rewrite every stale placeholder in place
    python3 site/numbers.py --check    # exit 1 if any placeholder is stale or names an unknown number (CI runs this)
    python3 site/numbers.py --list     # print every number and its value

Why: on 2026-11-05 the front-page numbers, typed by hand, drifted from the ledger within hours (README said 26 scored
bets and Brier 0.217 when the ledger said 37 and 0.188). So the documents below no longer type a ledger number. Each
one is a marked placeholder,

    <!--n:brier-->0.158<!--/n-->

which renders as the bare number on GitHub and the site (HTML comments are hidden), and whose value comes only from
the machine-readable line that ledger/brier.py, ledger/scores.py and ledger/prior.py write at the end of brier.md,
scores.md and prior.md (`<!-- numbers (generated; read by site/numbers.py): {...} -->`). Those pages are themselves
checked byte for byte by reproduce.py, so a number here is as reproducible as the ledger. `python3 reproduce.py` and
the GitHub workflow fail when any placeholder is stale; `python3 reproduce.py --write` and ledger/merge_inbox.py
rewrite them.

Numbers available (see --list): bets_total, scored, hits, brier, hit_rate_ref, coin, scored_all, hits_all, brier_all,
secondary, ref_{model,nature,record}_{brier,n}, human_n, human_brier, human_n_all, human_brier_all, human_lines,
audited, audited_scored, reversals, withdrawn, unscored, plants_planted, plants_caught, plants_sealed,
plants_revealed, dr_total, dr_go, dr_fix, dr_redesign, dr_missed, premortem_failed, premortem_named, chip_s,
chip_stop, chip_left, api_usd, api_usd_exact, api_allowance, prior_rate, prior_hits, prior_n, prior_ci.
"""
import os
import sys

# This file shares its name with the standard library's `numbers`; drop its own folder from the import path so a
# library that imports `numbers` gets the real one.
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:] = [p for p in sys.path if os.path.abspath(p or ".") != _HERE]

import argparse  # noqa: E402
import json  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
from pathlib import Path  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ["ledger/brier.md", "ledger/scores.md", "ledger/prior.md"]
DOCS = ["README.md", "paper/plain-words.md", "paper/one-page.md", "application/one-page-plain.md"]
LINE = re.compile(r"<!-- numbers \(generated; read by site/numbers\.py\): (\{.*\}) -->")
PH = re.compile(r"<!--n:([a-z0-9_]+)-->(.*?)<!--/n-->", re.S)


def load_numbers(root=ROOT):
    nums = {}
    for s in SOURCES:
        m = LINE.search((Path(root) / s).read_text(encoding="utf-8"))
        if not m:
            raise SystemExit(f"{s}: no numbers line (regenerate it with python3 ledger/{Path(s).stem}.py)")
        for k, v in json.loads(m.group(1)).items():
            if k in nums and nums[k] != v:
                raise SystemExit(f"number {k} is given twice with different values")
            nums[k] = v
    return nums


def fill(text, nums):
    """(new text, stale [(key, old, new)], unknown [key])"""
    stale, unknown = [], []

    def rep(m):
        k, old = m.group(1), m.group(2)
        if k not in nums:
            unknown.append(k)
            return m.group(0)
        new = str(nums[k])
        if old != new:
            stale.append((k, old, new))
        return f"<!--n:{k}-->{new}<!--/n-->"
    return PH.sub(rep, text), stale, unknown


def strip(text):
    """The text with every placeholder's value blanked: two versions that differ only in numbers compare equal."""
    return PH.sub(lambda m: f"<!--n:{m.group(1)}--><!--/n-->", text)


def only_numbers_changed(path, root=ROOT):
    """True if the working copy of path differs from HEAD only inside placeholders (safe to commit by path)."""
    r = subprocess.run(["git", "-C", str(root), "show", f"HEAD:{path}"], capture_output=True, text=True)
    if r.returncode:
        return False
    return strip(r.stdout) == strip((Path(root) / path).read_text(encoding="utf-8"))


def run(check=False, root=ROOT, quiet=False):
    nums = load_numbers(root)
    bad, changed = False, []
    for d in DOCS:
        p = Path(root) / d
        text = p.read_text(encoding="utf-8")
        new, stale, unknown = fill(text, nums)
        n = len(PH.findall(text))
        for k in unknown:
            print(f"  FAIL  {d}: placeholder names an unknown number '{k}'")
            bad = True
        if stale:
            if check:
                for k, old, v in stale:
                    print(f"  FAIL  {d}: {k} is {old!r}, the ledger says {v!r}")
                bad = True
            else:
                p.write_text(new, encoding="utf-8")
                changed.append(d)
                if not quiet:
                    print(f"  ok    {d}: {len(stale)} of {n} placeholder(s) brought current")
        elif not quiet:
            print(f"  ok    {d}: {n} placeholder(s), all current")
    return (1 if bad else 0), changed


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    if a.list:
        for k, v in sorted(load_numbers().items()):
            print(f"{k:20} {v}")
        return 0
    code, _ = run(check=a.check)
    if a.check:
        print("ALL DOCUMENT NUMBERS CURRENT" if code == 0 else "STALE DOCUMENT NUMBERS: run python3 site/numbers.py and commit")
    return code


if __name__ == "__main__":
    sys.exit(main())
