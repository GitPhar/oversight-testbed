#!/usr/bin/env python3
"""Program 5 (self-grading): rebuild every results table and analysis from the archived call caches, and check them.

    python3 programs/self-grading/reproduce.py        # from the repo root; stdlib and numpy only, no keys, no network

In plain English: each bet's script (experiments/sg_b1_placement.py, sg_b2_label.py, sg_b3_flaw.py) has an `analyse`
step that makes no calls. It reads the cached model answers (results/<bet>-write-calls*.json, <bet>-grade-calls*.json)
and writes results/<bet>-analysis*.json: the per-model differences, bootstrap intervals, readings and verdict. This
script runs that same step on a copy of the program taken at git HEAD, with keys removed, the network blocked and
every package except numpy stubbed out, and compares what it writes with the committed file, byte for byte.

Registered files (every one must be accounted for, or the run fails):
  results/*-analysis*.json   rebuilt by the bet's own analyse() and compared byte for byte
  results/*.md               results write-ups: none committed yet. When one lands, its tables must be added here.
The call caches and run logs are the inputs, not outputs, so they are not compared.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # programs/
import repro_common as R  # noqa: E402

PROGRAM = "self-grading"
BETS = {"sg-b1": "sg_b1_placement", "sg-b2": "sg_b2_label", "sg-b3": "sg_b3_flaw"}


def main():
    tmp = R.snapshot([f"programs/{PROGRAM}"])
    try:
        root = tmp / "programs" / PROGRAM
        sys.path[:0] = [str(root / "experiments")]
        rep = R.Report(PROGRAM, root, results_globs=("results/*.md", "results/*-analysis*.json"))
        for bet, mod in BETS.items():
            for pilot in (True, False):
                name = f"results/{bet}-analysis{'-pilot' if pilot else ''}.json"
                if not (root / name).exists():
                    continue
                m = __import__(mod)
                # sg_common puts /Users/seanpharris/entangled-mind/src on sys.path (the program's run-time client);
                # nothing outside the snapshot may be read here, so drop it again.
                sys.path[:] = [p for p in sys.path if "/entangled-mind" not in p or p.startswith(str(tmp))]
                r = rep.run(name, lambda: m.analyse(pilot))
                if r is not None:
                    rep.compare(name, (root / name).read_text(), json.dumps(r, indent=1))
        return rep.finish()
    finally:
        R.cleanup(tmp)


if __name__ == "__main__":
    R.main_guard(main)
