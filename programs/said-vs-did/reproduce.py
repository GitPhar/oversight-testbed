#!/usr/bin/env python3
"""Program 7 (said-vs-did): rebuild every results table and analysis from the archived call caches, and check them.

    python3 programs/said-vs-did/reproduce.py         # from the repo root; stdlib and numpy only, no keys, no network

In plain English: the wave-1 script (experiments/svd_wave1.py) has an `analyse <b1|b2|b3>` step that makes no calls. It
reads the cached model answers (results/sv-said-calls.json and results/sv-<bet>-calls.json) and writes
results/sv-<bet>-analysis.json: per-model AUROC against the dumb baselines, bootstrap intervals and the verdict. This
script runs that same step on a copy of the program taken at git HEAD, with keys removed, the network blocked and
every package except numpy stubbed out, and compares what it writes with the committed file, byte for byte.

Registered files (every one must be accounted for, or the run fails):
  results/sv-b*-analysis.json   rebuilt by svd_wave1.analyse() and compared byte for byte
  results/*.md                  results write-ups: none committed yet. When one lands, its tables must be added here.
As of this script's commit no call has been made for program 7, so there is nothing to rebuild yet.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # programs/
import repro_common as R  # noqa: E402

PROGRAM = "said-vs-did"


def main():
    tmp = R.snapshot([f"programs/{PROGRAM}"])
    try:
        root = tmp / "programs" / PROGRAM
        sys.path[:0] = [str(root / "experiments")]
        rep = R.Report(PROGRAM, root, results_globs=("results/*.md", "results/*-analysis*.json"))
        for step in ("b1", "b2", "b3"):
            name = f"results/sv-{step}-analysis.json"
            out = root / name
            if not out.exists():
                continue
            committed = out.read_text()
            out.unlink()
            import svd_wave1 as W
            rep.run(name, lambda: W.analyse(step))
            if out.exists():
                rep.compare(name, committed, out.read_text())
            elif name not in rep.seen:
                rep.error(name, RuntimeError("analyse did not write the file"))
        return rep.finish()
    finally:
        R.cleanup(tmp)


if __name__ == "__main__":
    R.main_guard(main)
