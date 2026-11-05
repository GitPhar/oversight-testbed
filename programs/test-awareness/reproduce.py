#!/usr/bin/env python3
"""Program 6 (test-awareness): rebuild every results table and analysis from the archived call caches, and check them.

    python3 programs/test-awareness/reproduce.py      # from the repo root; stdlib and numpy only, no keys, no network

In plain English: each bet's script (experiments/ta_b1.py, ta_b2.py, ta_b3.py) has an `--analyse` step that makes no
calls. It reads the cached model answers (results/<bet>-calls.json) and the bet's seed, and writes
results/<bet>-analysis.json: the tables, statistics, verdict and leave-one-out checks. This script runs that same step
on a copy of the program taken at git HEAD, with keys removed, the network blocked and every package except numpy
stubbed out, and compares what it writes with the committed file, byte for byte.

Registered files (every one must be accounted for, or the run fails):
  results/ta-b*-analysis.json   rebuilt by the bet's own --analyse step and compared byte for byte
  results/*.md                  results write-ups: none committed yet. When one lands, its tables must be added here.
The call caches (results/*-calls.json, the cost probe's probe-calls.json) are inputs, not outputs.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # programs/
import repro_common as R  # noqa: E402

PROGRAM = "test-awareness"
BETS = {"ta-b1": "ta_b1", "ta-b2": "ta_b2", "ta-b3": "ta_b3"}


def main():
    tmp = R.snapshot([f"programs/{PROGRAM}"])
    try:
        root = tmp / "programs" / PROGRAM
        sys.path[:0] = [str(root / "experiments")]
        rep = R.Report(PROGRAM, root, results_globs=("results/*.md", "results/*-analysis*.json"))
        for bet, mod in BETS.items():
            name = f"results/{bet}-analysis.json"
            out = root / name
            if not out.exists():
                continue
            committed = out.read_text()
            out.unlink()                       # rebuilt from scratch, never left over from the commit
            m = __import__(mod)
            sys.path[:] = [p for p in sys.path if "/entangled-mind" not in p or p.startswith(str(tmp))]

            def analyse(m=m):
                sys.argv = [f"{m.__name__}.py", "--analyse"]
                m.main()
            rep.run(name, analyse)
            if out.exists():
                rep.compare(name, committed, out.read_text())
            elif name not in rep.seen:
                rep.error(name, RuntimeError("--analyse did not write the file"))
        return rep.finish()
    finally:
        R.cleanup(tmp)


if __name__ == "__main__":
    R.main_guard(main)
