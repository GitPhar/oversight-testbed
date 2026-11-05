# Nature-Graded (placeholder name)

Program 3 of a scalable-oversight testbed for AI-driven research (the engine: `GitPhar/oversight-testbed`, placeholder slug). Program 1 was [The Entangled Mind](https://github.com/GitPhar/entangled-mind). Program 2 is Other Minds.

"Nature-Graded" is a working name taken from the repository slug. The real title will come from this program's proposal once that reads right.

## What this is for, in plain English

The testbed's engine is an AI research agent. Before every experiment, it writes down how likely it thinks the experiment is to pass. Afterwards we check how good those odds were. That number, its calibration, says whether the engine's judgment about what is worth doing can be trusted.

The trouble is who does the grading. In program 1, what decided whether a bet passed was the behaviour of a language model. That is a referee built much the way the engine is built. An engine could look well calibrated there because it shares its referee's habits, not because its judgment is good. Its blind spots and the referee's would line up and never show.

This program gives the same engine a second referee that shares none of its habits: a quantum computer. When the engine bets that a circuit on IBM's `ibm_fez` chip will show a certain result, the chip settles it. The chip cannot be talked round, does not read the engine's write-up, and does not care what the engine expected. We then compare the engine's calibration with an AI referee (program 1) against its calibration with nature as referee (this program).

**The driving-test analogy.** Take one driver and two tests. In the first test the examiner learned to drive at the same school as the driver, from the same instructor. They make the same mistakes, so the examiner does not mark what they both miss. In the second test there is no examiner, only an icy road at night. The road grades you on whether the car stays on it. A driver who passes the first test and not the second cannot drive; they have learned to please one particular examiner. Here the engine is the driver and its judgment is the driving. Program 1 is the examiner from the same school. This program is the icy road. Same judgment, two referees.

## The quantum computer is the referee, not a tool

Every circuit in this program is small enough to simulate exactly on a laptop. The chip does no useful computation for us, so nothing here is a claim of quantum speedup or quantum advantage. **The hardware is used only as ground truth:** its outcomes are decided by physics, not by any model, including the engine's own simulator of the chip. Every write-up from this program will say so.

That simulator matters in its own right. In program 1, IBM's own noise model of `ibm_fez` predicted P(yes) = 0.25 for one circuit; the chip gave 0.50, about 12 standard errors away (`entangled-mind/results/stage1-run-1.md`). For most bets in this program, quantum theory already says what an ideal device would do. What the engine really bets on is how far the real device strays from its description of itself. That is the same kind of judgment the engine has to make about research in general.

## Status

Opened 2026-11-04 (America/Denver). Scouting is done. **Wave 1 ran on 2026-11-04** (four bets, each pre-registered and seeded from CURBy before its data; audited in round 2, entangled-mind audit2 `8091d01`, all verdicts stand; no model API called):

- **P3-1, fail.** Fixing the simulator's idle-decay omission moves its prediction from 0.267 to 0.268, not to 0.40. Idle decay does not explain the 3 November gap; other differences between our simulation and that run stay untested. The run kept FakeFez's 2025 T1/T2 by a bug (the verdict is unchanged with them fixed), and adopting this model as the program's corrected simulator is held until the fix is made and checked (`results/p3-1-scheduled-sim.md`).
- **P3-5, fail (incoherent better).** In program 1's entanglement data, a blurring model fits better than a steering model on two of three pairs. Both kinds of error are present on every pair, so this is not "blur, not steering" (`results/p3-5-coherent-fits.md`).
- **P3-2 and P3-3, untestable.** One 8-second chip job ran program 1's gate list on the same nine qubits, without the one pre-measurement barrier the 3 November circuit had and as 20 interleaved blocks of 100 shots instead of one block of 1,000. In P(yes), the gap was gone: the chip gave 0.246 against the simulator's 0.269 (it gave 0.502 on 3 November). Qubit by qubit, departures of up to 0.14 remain. Twirling and decoupling defaults for later waves: both off, by the pre-registered rule (`results/p3-2-3-job.md`).

So far, the program's starting surprise did not recur on the next day's run; whether 3 November was unusual is untested. The two runs also differed in that barrier and in how the shots were grouped. The cheapest next chip test separates those (the audit's suggestion): the 3 November circuit with and without its barrier, each as one 1,000-shot block and as interleaved blocks, repeated hours apart.

- `map/program-3-map.md` (and `.json`) has 14 ranked directions. Each one gives the assumption at stake, who has looked, the exact cheapest circuit-level test, its QPU cost, and the engine's odds stated before any data. The map ends with a month plan under the hard stop: about 146 s of chip time in three waves, up to 60 s more if conditions are met, and at least 120 s held back for replication.
- `map/odds-elicitation/` records how the engine's odds were taken. A fresh context saw only the direction rows. A seeded random half was re-asked with each pass rule paraphrased and with the question negated. The engine's own numbers moved by 11 points on average under negation, and by up to 30. That spread is published next to the odds.
- `map/human-odds.md` is the form for Sean's odds. He fills it in separately, before any data, in shuffled order, and it does not show the engine's numbers or ranking.
- `map/reads/` holds the scout's 81 Read records (47 read in full, 24 in part, 10 at abstract depth) in five clusters:
  - local friendliness and Wigner's friend;
  - sequential contextuality under Contextuality-by-Default;
  - Leggett–Garg and certified randomness;
  - Heron r2 device physics and noise-model gaps;
  - other cheap foundations tests.

**First steps, all pre-registered before they run:**
- Two free tests on program 1's archived hardware data: is the 0.25-vs-0.50 gap a flaw in how our simulator was set up, and are the chip's errors systematic or random?
- One 21-second device job: twirling, decoupling and layout checks on the same circuit.

**Then, if approved:**
- a check that the contextuality analysis from program 1 sees contextuality where physics guarantees it (about 59 s);
- the first "genuine" Wigner's-friend inequality on a quantum computer;
- a Leggett–Garg test with a clumsiness control (about 66 s for these two together).

## Budget

IBM Quantum Open Plan, 600 QPU seconds a month. The project's hard stop is 420 s cumulative. Program 1 used 46 s (Stage 1 pipe test, 2 s; entanglement witness, 44 s). Program 3's wave 1 job used 8 s (2026-11-04). That leaves **366 s** before the hard stop. Measured cost on `ibm_fez`: about 0.28 ms per shot plus 1–2 s per job.

## Rules inherited from the engine

- Odds before data, both sides, in writing.
- Cheapest falsifier first: archives before hardware.
- Every test is pre-registered in its own commit before its first submission, or before an archive is opened for analysis.
- QPU budgets are enforced in code, and the hard stop is refused in code (`entangled-mind/src/entangled_mind/backends.py`, `run_hardware`).
- Hardware is submitted only for a pre-registered, separately approved experiment.
- No result stands without an independent audit.
- Nothing disappears: dead directions stay on the map with a diagnosis.
- Plain English first.

## Reproducibility

One command, from the repository root, with Python 3 and numpy installed (no keys, no network, no IBM token):

    python3 programs/nature-graded/reproduce.py

The root `python3 reproduce.py` runs it too and prints one line for this program.

What it does. It takes a copy of the program as committed and rebuilds every table in every write-up in `results/`. No script writes those write-ups; they were written by hand after each run. So the script recomputes each number from the archive, rebuilds each table cell by cell, and compares it line for line with the committed table. Descriptive cells (a row's "what" text, column headers) are copied; every number is recomputed. Nothing is sent to the chip. The chip is a referee here, never a computational resource: its archived counts are inputs.

Where the numbers come from:
- **Chip runs** (P3-2/P3-3, P3-15, P3-16): the raw counts in `data/*-raw.json` and the archived simulator predictions in `data/*-predictions.json`. Each bet's own `--analyse` step runs on them, and its analysis (`results/p3-2-3-job.json`, `p3-15-repeat.json`, `p3-16-lone-job.json`) must come out byte for byte the same. The tables are rebuilt from that.
- **Simulator runs** (P3-1): the simulated counts archived in `results/p3-1-*.json`. P(yes), SE and per-qubit P(1) are recomputed from them. The simulations are not re-run.
- **Fits** (P3-5, P3-5c): the scipy fits and the simulated reference states are not re-run; their outputs in `results/p3-5-coherent-fits.json` and `p3-5c-nested.json` are the inputs. The saturated likelihood, every ΔlogL and LR, the bootstrap p-values and null percentiles (from the 1,000 archived null draws), the deviance, the χ² quantile and the labels are recomputed.
- **Program 1's numbers** (3 November): recomputed from its archived counts (`programs/entangled-mind/results/stage1-run-1.json`, `witness-run-1.json`). Cumulative QPU seconds come from its ledger (`results/ibm-usage.json`).

Two printing rules. A time printed to the second matches IBM's timestamp floored or rounded (the write-ups use both). A number that is an exact tie at the printed precision (815 of 1,000 shots, to two places) matches either rounding. The script counts every such cell.

Gaps: none. No table needs a file the archive lacks. The `.qpy` circuit files need qiskit to read, but no table depends on them.

Not checked, because the number does not come from this archive:
- `results/p3-1-rerun.md`, first table, column "auditor's fixed re-run" (4 cells): the auditor's own runs, not archived here.
- `results/p3-15-repeat.md`, first table, column "predictions" (2 cells): commit hashes, from git history, not from JSON.
