# P3-18: do both error terms show up again when the three entangled pairs are measured in a fresh chip job? (pre-registration)

Written and frozen 2026-11-05 (America/Denver; the commit's author time is the record), in its own commit, before any chip submission and before any calibration or property read for this bet. DEVIATIONS.md D42. Budget **≤ 24 QPU s** (estimate 20.5 s), $0 API, enforced in code; approval is the engine's `budget_ruling` row in `ledger/spend.jsonl` under st-16, after the design review. Stop rules in §7.

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). This session never asks Sean for odds or for a decision, in a terminal, a chat or a question dialog. His odds come only from `ledger/human-odds.jsonl` (the cockpit's downloads, committed); if a direction has no line there when its bet is pre-registered, the bet proceeds marked "no human odds". A decision this session would otherwise ask about, it makes under the written rules and states in its report and commit, where Sean can veto it from the cockpit.

> **The chip is a referee here, never a computational resource** (`operators/hardware.md`). Every circuit in this bet is simulable exactly on a laptop. The chip's counts decide a pre-registered bet about the chip itself; they are never used as an estimate, feature or prediction anywhere else.

> **Cockpit first, then this file.** P3-18's card is in `map/cockpit-cards.jsonl` (remap 2026-11-05). `ledger/human-odds.jsonl` was read immediately before this commit, after `python3 ledger/pickup_human_odds.py` (`9a75cc2`): it holds Sean's line for P3-18.

## 0. The bet

| field | value |
|---|---|
| bet id | `ng-p3-18` |
| referee | `nature` (the chip's counts decide it) |
| bet type | `standard` (a replication of ng-p3-5c's reading on a fresh job, not a simulator-vs-chip tiebreak) |
| direction | `P3-18` (`programs/nature-graded/map/program-3-map.json`, remap 2026-11-05) |
| source | `engine` (the remap's invariant-7 replication of ng-p3-5c) |
| engine odds, P(pass) | **60** after the lesson. Map (remap one pass, 2026-11-05 04:45): 60. v1 re-elicitation in a fresh context that saw only the direction's row and this file's pass rule (2026-11-05 about 06:25, before this commit): 72. |
| human odds, P(pass) | **55**, `ho-20261105-061152-7q5` (cockpit, saved 2026-11-05 06:11:52; committed `9a75cc2`). His card's event is this file's event (§5). |
| odds disclosure | The session that set the after-lesson odds (60, the map's number kept) had read Sean's line (55) before doing so; the v1 number (72) came from a fresh context that never saw it. Both are kept. |
| models | not all three, because no model is in the loop: the chip is the referee (rule 12 does not apply). |
| budget | 0 $ API · ≤ 24 QPU s (estimate 0.28 ms × 66,000 shots + 2 s = 20.5 s) · about 1 laptop hour for the fits |
| lesson | Correcting P8, P12: P3-5c's both-terms reading came from one job, and a fresh job differs in date, calibration and shots, not only in being fresh. This bet names that bundle, rebuilds the reference from the fresh calibration, checks pre-run worlds that pass and fail, and its odds are 60% (from 60% on the map) because P3-5c's wide margins offset the halved shots. |
| design review | before any submission, a fresh subagent dry-runs this design (`operators/design-review.md`) → `ledger/design-reviews/ng-p3-18.md`; `--submit` refuses without go (or a confirmed fix-first). |
| pre-mortem | If this fails, the most likely reason is that halved shots push h221's weak rotation term and one other pair's term below their nulls' 99th percentiles. Kind: `design`. |
| auditor | fresh session per `operators/auditor.md`, after results, with a sealed plant draw first (`operators/plant.md`) |

**Read before betting (operators/learn.md).** `ledger/bets.jsonl`, `ledger/brier.md`, `ledger/audits/` and `ledger/lessons.jsonl` at `9a75cc2`: 24 scored bets, 8 hits, Brier 0.223, running base rate 0.35; nature-graded 0 hits in 4 scored, every chip bet so far a miss on low odds; newest audit file `ledger/audits/sv-b3.md`; for this direction `ledger/audits/ng-p3-5c.md`, `round-3/ng-p3-5c.md`, `ng-p3-15.md`, `ng-p3-16.md`. Patterns: P8 (the fresh job differs from 3 November in more than "being a second job": date and time of day, IBM's calibration, half the tomography shots, a quarter of the calibration shots, possibly server-side handling; the claim is about that bundle) and P12 (`--worlds` shows before the run that the rule can pass and can fail at 2,000 shots). The odds stay at the map's 60 rather than moving to the base rate (P1) for a named reason from the archive: P3-5c's six LRs were 3–25 times their nulls' 99th percentiles, and the rule needs only 2 of 3 pairs.

## 1. In plain English

P3-5c refitted one chip job from 3 November and found that, on all three entangled qubit pairs, a model of the chip's errors needs both a "rotation-type" part and a "blur-type" part. That was one job on one afternoon, and this chip has read differently between runs before. This test runs the same circuits again, gate for gate on the same qubits, in one new job today, with half the shots, and fits exactly the same models. If both parts are needed again on at least two of the three pairs, P3-5c's reading held on a second job. If not, it may have belonged to that afternoon's job (or to its larger shot count) rather than to the chip. Either way, these are terms in a fitted model, not identified physical mechanisms, and two jobs are not "the chip in general".

## 2. Material

- **Backend:** `ibm_fez` (IBM Open Plan), one SamplerV2 job inside a Batch via `entangled_mind.backends.run_hardware` (its 420 s hard stop is refused in code).
- **Circuits:** the 39 archived ISA circuits of job `dbl6e1d8mdtc73d5gesg` (`programs/entangled-mind/window/data/hardware/`), rebuilt gate for gate by `p3sim.load_isa`, in the archived order: per pair (h221 on qubits 10, 9; h088 on 44, 37; h268 on 4, 16) nine tomography settings and four readout-calibration circuits. `--check` (no network) confirmed all 39 are ISA on FakeFez's target and that every circuit's gate counts equal the archive's. No twirling, no dynamical decoupling, no transpilation (as on 3 November).
- **Shots:** 2,000 per tomography PUB (3 November: 4,000), 1,000 per calibration PUB (3 November: 4,000); 66,000 in all.
- **Reference state ρ_ref:** P3-5c's construction (`C._bare_probs` + linear inversion, T1/T2 written and asserted), with this job's calibration in place of 3 November's: `--prepare` reads IBM's properties (`refresh=True`, free) for every active qubit (T1, T2, sx error, readout error) and every CZ pair, writes them in `p3sim.snapshot`'s format, builds the three ρ_ref and commits them, with the circuits (qpy) and their SHA-256, **before** `--submit`. `--submit` reads the properties again at submission and saves them beside the counts (reported, not used).
- **Assignment matrix A:** from this job's four calibration PUBs per pair (column k = the outcome frequencies for prepared bits k, Qiskit order), as program 1 built it.
- **Models and tests:** P3-5c's primary set (D19), unchanged: coh (7), inc9 (9), full16 (16); LR_rotation = 2 (logL_full16 − logL_inc9), null from the fitted inc9; LR_blur = 2 (logL_full16 − logL_coh), null from the fitted coh. Parametric bootstrap at 2,000 shots per setting (the job's own n), B = 100, extended to 1,000 if p ≤ 0.05. "Present" iff p < 0.01.
- **Seed** (`operators/hardware.md`). CURBY-Q latest completed round 28297, result pulse 2025-08-22 13:42 America/Denver (checked 2026-11-05 06:23): stalled. Seed: the first CURBy-RNG pulse timestamped after this commit; seed = the first 8 bytes of SHA-256(randomness ‖ ng-p3-18), unsigned big-endian; sub-seed by `ledger/seed.py --purpose boot` (bootstrap SeedSequence and fit starts). Nothing else is random: the circuit order is the archive's. `--worlds` uses the fixed root seed 2026110518 (synthetic only). *Filled in by the seed commit, before any data:* `chain:` ___ · `pulse index:` ___ · `pulse_time:` ___ · `randomness:` ___ · `client:` ___ · `certificate_verified:` ___ · `seed:` ___
- **Scale:** no graded scale (no model).

## 3. Calls

| step | what | QPU s | when |
|---|---|---|---|
| 1 | `--worlds`: pre-run worlds (below), synthetic counts only | 0 | before the design review |
| 2 | design review (fresh subagent); then the engine's budget ruling (`ledger/spend.jsonl`, under st-16), committed | 0 | before step 3 |
| 3 | `--prepare`: live target and IBM properties (free reads), circuits (qpy + hash), snapshot, three ρ_ref; committed | 0 | before step 4 |
| 4 | `--submit`: one job, 39 PUBs, 66,000 shots; raw counts written to `data/p3-18-raw.json` the moment `run_hardware` returns, then committed at once with the QPU usage ledger | ≤ 24 (est. 20.5) | once |
| 5 | `--analyse`: fits and bootstraps from the committed raw file | 0 | after step 4's commit |

**Gates in code.** `--prepare` refuses if any file it uses is uncommitted. `--submit` refuses unless: no raw file and no QPU-ledger entry "Program 3 P3-18" exist (never resubmitted); the design review says go (or fix-first confirmed); **every file it uses** (`SUBMIT_USES`: the code, the program-1 package and archive, this file, the seed, the prepared snapshot and circuits, the review, `ledger/spend.jsonl`, `check_prereg.py`) is committed and unchanged; a `budget_ruling` row for ng-p3-18 (resource qpu_s, under st-16) approves at least the estimate; `check_prereg.py ng-p3-18 … --before-run` passes; the circuit hash matches; the estimate is ≤ 24 s and ≤ the approval; the reserve rule holds (used + 1.5 × estimate ≤ 300 s). `--analyse` refuses unless the raw file and everything else it reads are committed and unchanged.

**Pre-run worlds (`--worlds`, P12 / D11).** At 2,000 shots per setting, on 3 November's reference states and assignment matrices (the fresh ones do not exist before the job): **W_both**, truth = P3-5c's published fitted full16 state, should pass; **W_neither**, truth = the reference state itself, should fail. Six draws per pair and world, classified against the 99th percentiles of one B = 100 null pair from the first draw. P(pass | W_both) and P(pass | W_neither) are reported (≥ 2 of 3, pairs treated as independent). If P(pass | W_both) < 0.10 or P(fail | W_neither) < 0.10, the design review decides before any submission.

## 4. Statistics

- **Primary:** per pair, the two labels (rotation present, blur present), each from its bootstrap p < 0.01. Unit: the pair. Nothing pooled across pairs.
- **Dumb baselines** (P3), scored beside the engine's and Sean's odds: (a) *carry-over*, "the chip did what it did on 3 November": P(pass) = 0.95; (b) the running base rate, 0.35. The dumbest world that must not pass is W_neither (the simulator's reference state is the whole story), checked by `--worlds`; P3-5c's recovery also labelled "neither" correctly on all three reference states at 4,000 shots.
- **Secondary** (reported, never promoted): whether all three pairs show both terms (the map's engine-only sub-bet, 0.40); goodness of fit (full16 deviance on 11 df against χ²₁₁'s 99th percentile); both LRs scaled by max(1, deviance/11) beside the nulls' 99th percentiles (round 3's misfit point); per-setting shares and the top setting of each LR; negativity of ρ_ref and of each fitted state; P3-5c's LRs and labels beside each pair; the properties at submission against those at preparation.
- **Multiple comparisons:** six primary tests (3 pairs × 2 terms), reported against α = 0.01 and Bonferroni 0.0017; the rule uses α = 0.01, as P3-5c did and as the card's event says.
- **Robustness committed now (P10):** the rule is "at least 2 of 3"; the result names which pairs carry it, and whether one pair's label flip would change the verdict (it would whenever exactly two pairs show both). If one setting carries more than half of a "present" LR, that pair's sentence adds "This rests mostly on setting <S>."

## 5. Pre-registered reading

The rule (`verdict()` in the code):

1. **Pass:** both terms present (each p < 0.01) on at least 2 of the 3 pairs.
2. **Fail:** both terms present on 0 or 1 pair.
3. **Untestable:** the job errors (recorded, never resubmitted); or a PUB returns under 90% of its shots; or the number of results differs from the number of circuits.

Sentences, used verbatim (`pair_sentence()`, `verdict()`; <date> is the job's run date in America/Denver):
- Pair, both: "On pair <P>, the fresh job's counts need both a rotation-type and a blur-type term beyond the simulator's state, as on 3 November. These are terms in a 16-knob model, not identified mechanisms."
- Pair, rotation only: "On pair <P>, the fresh job's counts need a rotation-type term but not a blur-type term."
- Pair, blur only: "On pair <P>, the fresh job's counts need a blur-type term but not a rotation-type term."
- Pair, neither: "On pair <P>, the fresh job's counts need neither term beyond the simulator's state."
- Pass: "Overall: both terms came back on <n> of 3 pairs in a fresh job on <date>, so P3-5c's 'both terms' reading held on a second job, not only on 3 November's afternoon. Two jobs on one chip are still not a description of the chip in general."
- Fail: "Overall: both terms came back on only <n> of 3 pairs in a fresh job on <date>, so P3-5c's 'both terms on every pair' did not hold on a second job; what 3 November's job showed may belong to that afternoon (or to that job's shot count) rather than to the chip."
- Untestable: "The fresh job could not answer the question (<reason>); nothing is said about the chip."

Reported in every case: the job id, billed QPU s, run times; per pair both LRs, p, B, null 99th percentiles and maxima; the secondaries in §4; the two dumb baselines. A pass is reported as **pass, unreplicated** beyond these two jobs.

## 6. What it cannot do

It cannot separate "a second job" from the bundle it comes with: another day and time, IBM's newer calibration (which also changes ρ_ref), half the tomography shots and a quarter of the calibration shots (so a fail could be a power loss: the pre-mortem's reading, which the `--worlds` power figure and the per-pair LRs will speak to). It cannot say the terms are physical mechanisms (P3-5c's limits: readout drift beyond A, spectator rotations, h088's misfit; P3-17 tests the first on the archive). It is one fresh job on one chip; "every", "all" and "the chip in general" will not appear.

## 7. Stop rules

- QPU: ≤ 24 s estimate cap and the engine's approval, both checked in code before submission; one job only; `run_hardware`'s 420 s hard stop is absolute. Every billed second is reported.
- A job error is recorded in the raw file and never resubmitted (untestable by §5.3).
- No model API; refusals n/a. $0.

## 8. Ledger entry (filled now, completed after audit)

```json
{"id": "ng-p3-18", "program": "nature-graded", "direction": "P3-18",
 "title": "Do both error terms show up again when the three entangled pairs are measured in a fresh chip job?",
 "source": "engine", "engine_odds": 0.60, "engine_odds_first": 0.60, "engine_odds_v1": 0.72,
 "human_odds": 0.55, "human_odds_at": "ho-20261105-061152-7q5",
 "prereg_commit": "<this commit>", "budget_usd": 0, "qpu_s_budget": 24,
 "referee": "nature", "bet_type": "standard", "seed_source": "curby-rng", "beacon": null, "seed": null, "tiebreak": null,
 "lesson": "ls-ng-p3-18", "design_review": {"path": "ledger/design-reviews/ng-p3-18.md", "verdict": null},
 "premortem_kind": "design", "verdict": "open", "date": "2026-11-05"}
```

## 9. Checklist before the first submission

- [x] This file is committed on its own; nothing has been submitted or read from IBM for this bet.
- [x] Lesson row filled after reading the ledger at `9a75cc2`; the same sentence goes to `ledger/lessons.jsonl` as `ls-ng-p3-18`.
- [ ] Design review go (or fix-first confirmed); `check_prereg.py ng-p3-18 … --before-run` passes (the code runs it).
- [ ] Budget ruling row in `ledger/spend.jsonl` (under st-16), committed.
- [x] Cockpit card exists; `ledger/human-odds.jsonl` read immediately before this commit; `human_odds_match.py nature-graded P3-18` printed 0.55, `ho-20261105-061152-7q5`.
- [x] Pass rule applicable by a stranger (`verdict()`; checked on synthetic label tables).
- [x] Pre-mortem one sentence, checkable, with its kind.
- [x] CURBY-Q stalled; seed commit follows this one before any data.
- [x] QPU budget and the "everything committed" gate are in code.
- [x] DEVIATIONS.md D42.
