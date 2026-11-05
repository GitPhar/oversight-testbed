# P3-16. Does 3 November's result come back when the circuit runs alone in its own job? (pre-registration)

Frozen at this file's commit time (America/Denver; the commit's author time is authoritative), in its own commit, before any circuit is built against the live device or submitted. DEVIATIONS.md D28. Budget **$0 API · ≤ 10 QPU s in total, ≤ 4 s per job (estimate 7.1 s: 2.28 + 2.28 + 2.56) · 1 laptop hour**. Hardware only through `entangled-mind/src/entangled_mind/backends.py::run_hardware`, which refuses at the 420 s hard stop. **Each job is submitted once, never resubmitted.**

## 0. The bet

| field | value |
|---|---|
| bet id | `ng-p3-16` |
| referee | `nature` |
| bet type | `standard` (program-level referee experiment under CONTEXT rule 7) |
| direction | `P3-16` (map/program-3-map.json, added 2026-11-04 22:55, commit 1d331a4) |
| source | `P1` (audit `ledger/audits/ng-p3-15.md`, "What would break it next") |
| engine odds, P(pass) | **5**, elicited 2026-11-04 22:54 in a fresh context from `map/odds-elicitation/rows-v1-p3-16.md` alone (template v1, single row; `map/odds-elicitation/v1-p3-16.md`). Unchanged by the lesson (below). |
| human odds, P(pass) | **no human odds**: `ledger/human-odds.jsonl` has no line for P3-16 at this commit (CONTEXT §3 rule 11; never asked for in a terminal). Q16 is on `map/human-odds.md` for the cockpit. |
| budget | $0 API · ≤ 10 QPU s total, ≤ 4 s per job · 1 laptop hour |
| approval | per `operators/hardware.md` "Who approves": this file states the budget, the design review checks it against the estimate, and the engine records its approval as a `budget_ruling` row in `ledger/spend.jsonl` citing st-16. *(Amended D29.)* `--submit` refuses until that file has a row with kind `budget_ruling`, bet `ng-p3-16`, resource `qpu_s`, an `under` field citing st-16 and `approved_qpu_s`. It also refuses if the planned total is above `approved_qpu_s`, and stops before any job that would take the billed seconds plus the remaining estimates above it. *(Amended D33, F5.)* **The ruling approves the stated ≤ 10 s.** The D29 gate counts whole billed seconds, and the seeded order runs A last. Approving only the 7.12 s estimate would stop the run before A after an ordinary 3 s bill for job C (design review, `dry3_gates.py`). *(Amended D35, O2.)* `--submit` also refuses unless `ledger/spend.jsonl` is committed and unchanged. |
| pre-mortem | "If this fails, the most likely reason is that 3 November's 0.50 was a passing state of the chip, so the lone barrier job reads about 0.30, like every arm on 4 November." Kind: `world`. |
| lesson | Correcting P8, P6: P3-15 never ran the circuit alone in its own job, the one 3 November feature no later run repeated. This bet runs it alone and shared, minutes apart on one evening, checks the shared arm against P3-15's 0.30, and its odds are 5% (from 5% on the map) because every 4 November arm read 0.25–0.32. |
| design review | before submission, a fresh auditor dry-runs this design (operators/design-review.md) → `ledger/design-reviews/ng-p3-16.md`, launched by the oversight-testbed session. **No submission before a go** (or a confirmed fix-first). `--submit` checks the review file's verdict in code. |
| auditor | fresh session per operators/auditor.md, after results |

**What was read for the lesson** (operators/learn.md, step 1; oversight-testbed at `1d331a4`): `ledger/bets.jsonl` (41 rows; 19 scored, 8 hits), `ledger/brier.md` (engine Brier 0.259 on 19), running base rate (8 + 1)/(19 + 2) = **0.43**, `ledger/lessons.jsonl` (P1–P12), and `ledger/audits/` through `ng-p3-15.md`, the newest nature-graded audit. **Why the odds stay far below the base rate** (learn.md: moving away needs a reason from the ledger). The base rate mixes programs. In this program the three bets given under 20% (em-gm1 15%, ng-p3-1 7%, ng-p3-15 7%) all missed. ng-p3-15 ran the 3 November circuit in eight arms over two jobs, and every arm read 0.27–0.32 against a prediction of 0.27. Its audit found the barrier inert on average and the grouping effect unreplicated. The fresh elicitor's 5% is kept.

**Which patterns, and how this bet answers them.**
- **P8 (unmatched comparisons).** "Alone in its job" has so far only been compared across days: 3 November alone against 4 November shared. Here A (alone) and C (shared) run minutes apart on the same qubits, with the same circuit and shot count. *(Amended D33, F3.)* A and CB differ in whether a second PUB (CN) shares the job, and probably its execution span. They are also separate jobs in a fixed seeded order (C, then B, then A), seconds to minutes apart.
- **P6 (a control that cannot fail).** C's barrier PUB must read within 0.05 of P3-15's pooled 0.2965. That fails if the chip has moved since, for example if 0.50 comes back everywhere.

## 1. In plain English

On 3 November, program 1's circuit made the chip say "yes" 50% of the time, about twice what the chip's own description predicts. Since then, eight versions of the same circuit, with and without a "barrier", in one big block or in small pieces, have all said "yes" 27–32% of the time, about as predicted. One thing about 3 November was never repeated: the circuit ran alone, the only thing in its job. In every later job, it shared the job with other circuits. This test runs it alone, twice (with the barrier, as on 3 November, and without), and once sharing a job with one other circuit, all within minutes. If running alone brings the 50% back, the surprise came from how the job was packaged. If it doesn't, "alone in its job" is crossed off, and 3 November's afternoon remains the main candidate among the things tested. That is a narrowing, not a proof.

## 2. Material

- **Circuit.** Program 1's Stage 1 gate list (`entangled-mind/window/data/hardware/dbl423dgg49c73dk0db0-0.json`), rebuilt by `p3sim.load_isa`, on its original physical qubits (clbit order 117, 125, 124, 123, 144, 136, 143, 141, 142). Built exactly as in P3-15 (`p3_15_repeat.base_isa`, `with_barrier`):
  - **barrier circuit:** one barrier across the nine qubits just before the measurements, as `measure_all()` placed it on 3 November;
  - **no-barrier circuit:** the archived gate list unchanged.
  - Checked before this commit on FakeFez (`--check`, structure only): identical gate lists apart from the one barrier; every instruction native.
- **Jobs** (`experiments/p3_16_lone.py`; 1,000 shots per PUB, passed as SamplerV2 PUB tuples through `run_hardware`, unchanged):
  - **A:** the barrier circuit, the only PUB in its job. This is 3 November's circuit, qubits, shot count and packaging.
  - **B:** the no-barrier circuit, the only PUB in its job.
  - **C:** both circuits as two PUBs in one job, their order seeded: **CB** (barrier) and **CN** (no barrier). This is P3-15's 1,000-shot condition, which its execution spans showed ran as one shared span.
  - The three jobs are submitted back to back, in a seeded order, one `run_hardware` call each. Each job's raw counts are written the moment it returns, then enriched with timestamps, execution spans and per-shot bitstrings (a free read of `job.result()`).
  - No readout-calibration PUBs: adding any would mean A no longer ran alone. P(yes) does not use readout mitigation (§4). P3-15's two runs measured readout error at most 0.028 per qubit on these qubits.
- **Matched comparison** (P8; *amended D33, F3*): A and CB differ in whether a second PUB (CN) shares the job, and probably its execution span. They are also separate jobs in a fixed seeded order (C, then B, then A), seconds to minutes apart. Same circuit, qubits and shots, the same evening. B against CN is the same contrast for the no-barrier circuit.
- **Does the manipulation take effect?** (P4) Whether a PUB ran "alone" is checked after the fact: the job holds exactly one PUB, and its execution spans hold only that PUB. For C, the spans show whether its two PUBs shared one span, as in P3-15. Both are reported. Whether the server treats a one-PUB job differently from a two-PUB job in any physical way (shot order, rep delay, warm-up) is not observable. That is the question.
- **Predictions** (as in P3-15): `NoiseModel.from_backend` of the live ibm_fez target read just before submission, 100,000 shots, seed `sim`, barrier and no barrier, each ALAP and ASAP. **New** (audit ng-p3-15, B9): the prediction file records, per qubit, IBM's measurement date for T1, T2 and readout error, not only the document's `last_update_date`. Committed (`data/p3-16-predictions.json`, circuits in `data/p3-16-circuits.qpy` with their SHA-256) before submission. `--submit` refuses otherwise. *(Added D35, O1.)* Just before each job, `--submit` also reads IBM's properties again (`refresh=True`, free), and the job's raw file records T1, T2 and readout error with their measurement dates, and the error and date of every CZ pair the circuit uses.
- **Seed** (operators/hardware.md): CURBY-Q latest completed round **28297, result pulse 2025-08-22 13:42 America/Denver** (checked 2026-11-04 22:56 with `experiments/curby_seed.mjs check`, before this commit). It is more than 24 h old, so **stalled**. **Seed: the first CURBy-RNG pulse timestamped after this commit.** Sub-seeds by `ledger/seed.py --purpose`: `order` (job order and the order inside C), `sim` (Aer seed). `seed32` is used. *Filled in by the seed commit, before anything is built against the live device:* `chain:` CURBy-RNG · `pulse index:` 1591823 · `pulse_time:` 2026-11-04 22:59:00 America/Denver · `previous pulse:` index 1591822 at 2026-11-04 22:58:00 (before the commit at 2026-11-04 22:58:49) · `randomness:` 0b4d17c04436da0c8d32af92fd9dc4312ae6986e6a4d28a57b26d76e1a8b8b19d3c74ffa12e0efe5e98087d05952c894e0cadd8a163b7a7c5c4ac9cfdcfb7434 · `client:` @buff-beacon-project/curby-client@1.2.0 via `experiments/curby_seed.mjs` · `certificate_verified:` false · `seed (order):` 9817816759113118711 · `seed32 (order):` 1288729591 · `seed (sim):` 9906516209171909807 · `seed32 (sim):` 1498893487. Record: `data/p3-16-seed.json`.

## 3. Calls

| step | what | calls | est. cost |
|---|---|---|---|
| 1 | seed commit | CURBy | $0 |
| 2 | design review by a fresh auditor (launched by the oversight-testbed session); then the engine's `budget_ruling` in `ledger/spend.jsonl` citing st-16 (D29) | 0 paid | $0 |
| 3 | `--predict`: read the live target (IBM API, 0 QPU s), build the three jobs, four predictions, per-qubit calibration dates; commit | 1 IBM read | laptop |
| 4 | `--submit`: refuses without a design-review go, without the engine's `budget_ruling` row (or if the planned total exceeds its `approved_qpu_s`; D29), unless `check_prereg.py --before-run` passes, if any code it runs is uncommitted, without committed predictions and a matching circuit hash, if any job's raw file or `Program 3 P3-16 job <X>` QPU-ledger entry exists, if any job's estimate is above 4 s or the total above 10 s, if `ledger/spend.jsonl` is not committed and unchanged (D35, O2), or under the reserve rule (cumulative + 1.5 × total estimate ≤ 300 s). Then three `run_hardware` jobs back to back. If one errors, it is recorded and the rest are **not** submitted. | 3 jobs | ≈ 7.1 QPU s |
| 5 | `--analyse` | 0 | laptop |

## 4. Statistics

- **P(yes)** per PUB: `readout.quantum_readout` on its raw counts. No readout mitigation. Binomial SE, √(p(1 − p)/n), n = 1,000.
- **Primary statistic:** P_A, and Δ = P_A − P_CB with z = Δ / √(SE_A² + SE_CB²).
- **Power:** at P ≈ 0.3, SE ≈ 0.0145 per PUB and 0.0205 per difference. A return to 0.50 in A with CB at 0.30 gives Δ = 0.20, z ≈ 9. The pass needs Δ ≥ 0.10 and z ≥ 3. At SE 0.0205 the binding condition is Δ ≥ 0.10 (z ≈ 4.9).
- **Secondary, reported, not scored:**
  1. **Alone against shared, no barrier:** B − CN. *(Amended D34, F4.)* This is the in-evening replicate of A − CB, a second lone job at a different time. It qualifies the pass sentence (§5) but not the verdict.
  2. **Barrier effect, alone:** A − B. **Barrier effect, shared:** CB − CN. Each unpooled, with a 90% CI. **Equivalence margin 0.05** (P2): "no difference larger than 0.05" only if the whole 90% CI lies inside (−0.05, +0.05). Power for that claim is poor. The CI half-width is ≈ 0.034, so with no true effect the CI falls inside the margin only about 56% of the time (|Δ̂| < 0.016). So "not inside the margin" is the expected outcome even with no effect, and is not read as evidence of one.
  3. **Control** (P6): CB within 0.05 of P3-15's pooled barrier 1,000-shot PUB, 0.2965 (runs 1 and 2, 0.311 and 0.282). It gates the reading, not the verdict (§5).
  4. **Back to back:** the time from the first job's start to the last job's finish. If it is more than 60 minutes (for example, from queueing), the write-up says the jobs were not back to back, and gives the spread.
  5. **C's spans:** whether CB and CN shared one execution span.
  6. Per-qubit marginals for every PUB against the predictions. Billed seconds against the estimate. The calibration dates.
- **Multiple comparisons:** one scored test. The secondaries are labelled, uncorrected.
- **One-item fragility** (P10): one circuit, one evening, by design. No repeat is pre-registered. A pass is reported as **pass, unreplicated**.

## 5. Pre-registered reading

1. **Pass:** P_A ≥ 0.40, Δ = P_A − P_CB ≥ 0.10, and z ≥ 3.
2. **Fail:** all three jobs complete and it is not a pass.
3. **Untestable:** any job errors (the rest are then not submitted), any job returns a PUB whose shot count differs from 1,000, or *(added D32, F2)* the budget gate (D29) stops before a job is submitted. The stop writes `{"job": X, "not_submitted": "<gate message>"}` raw files for that job and every later one. Nothing is resubmitted. *(In code: `untestable()`.)*

**"Within ±0.05"** *(defined D32, F2)* means the 90% CI of the difference (Δ ± 1.645 SE) lies inside (−0.05, +0.05). This holds everywhere in §4 and §5 and matches `_diff`/`_class`.

**The plain-English sentences, written now** (P9; *rewritten D31, F1 and D34, F4, before any data*). The write-up uses these and no stronger nouns. They are implemented in `evaluate()` in `p3_16_lone.py`, and `--worlds` runs the design review's eleven worlds through it (`data/p3-16-worlds.json`). Δ = P_A − P_CB; "clear" means |Δ| ≥ 0.10 with |z| ≥ 3; the order word is "earlier" if job C ran before A, else "later".
- *Pass:* "Run alone in its own job, the 3 November circuit again said 'yes' at least 40% of the time, clearly more than the same circuit sharing a job with one other circuit, in a separate job minutes <earlier/later>. The 3 November surprise came at least partly from the circuit running alone in its job, not only from that afternoon." Then one of *(F4)*:
  - B − CN clear and positive: "Both lone jobs (with and without the barrier) came back, and both were clearly above their shared-job twins."
  - otherwise: "Only the lone barrier job came back (B − CN = …). The pass rests on one job, so a passing state of the chip during that job is not ruled out."
- *Fail with P_A < 0.40*, by Δ:
  - within ±0.05: "Running the 3 November circuit (with its barrier) alone in its own job did not bring back 3 November's result, and for the barrier circuit, running alone or sharing a job made no difference larger than 0.05. This evening, running the barrier circuit alone in its own job did not raise its rate by more than 0.05 (assuming IBM's servers handled a one-circuit job the same way on 3 November)."
  - clear and positive: "Run alone, the barrier circuit said 'yes' clearly more often than sharing a job (Δ = …), but not the 40% of 3 November. Running alone raised the rate without bringing back 3 November's result."
  - positive otherwise: "Running the 3 November circuit (with its barrier) alone in its own job did not bring back 3 November's result. Running alone may make a smaller difference (Δ = …), which this test cannot pin down."
  - negative (not within): "Running the 3 November circuit (with its barrier) alone in its own job did not bring back 3 November's result. Run alone, it said 'yes' less often than sharing a job (Δ = …), a difference this test cannot pin down." If the negative Δ is clear, the ending is ", a clear difference." instead.
  - Then, *only if B, CB and CN are all below 0.40*: "Of the things the 4 November runs and this one varied (the barrier, the shot grouping, running alone), none brought back 3 November's result. The chip on that afternoon remains the main candidate among them, not a demonstrated cause."
  - If B ≥ 0.40: "Run alone without the barrier, the circuit said 'yes' at least 40% of the time (B = …), but with the barrier it did not. One lone job came back and the other did not."
  - If CB or CN ≥ 0.40: "The shared job came back (CB = …, CN = …) while the lone barrier job did not."
- *Fail with P_A ≥ 0.40 and P_CB ≥ 0.40*, by Δ:
  - within ±0.05: "The chip again said 'yes' about 40% of the time or more, alone or sharing a job. A large part of 3 November's result came back, and running alone was not what caused it."
  - positive otherwise: "The chip again said 'yes' about 40% of the time or more, alone or sharing a job. A large part of 3 November's result came back alone or sharing a job; running alone may add a smaller amount (Δ = …), which this test cannot pin down."
  - negative otherwise: "The chip again said 'yes' about 40% of the time or more, alone or sharing a job. A large part of 3 November's result came back alone or sharing a job; running alone did not add to it (Δ = …)."
- *Fail with P_A ≥ 0.40 and P_CB < 0.40:* "Run alone, the circuit again said 'yes' at least 40% of the time, but the shared-job version was not clearly lower (Δ = …, below the 0.10 bar or z < 3). Running alone may contribute, but this test cannot show that it caused 3 November's result."
- *(Secondary.) Barrier, alone (A − B):* clear and positive: "Run alone, the barrier raised the 'yes' rate by … ." Within ±0.05: "Run alone, the barrier made no difference larger than 0.05." Otherwise: "Run alone, the barrier may make a smaller difference (…), which this test cannot pin down."
- *Control failed (CB more than 0.05 from 0.2965):* add "The chip itself had moved since P3-15: the shared-job barrier circuit now gives … ." The A − CB contrast is still within this evening.
- *Not back to back (§4.4):* add "The three jobs ran over … minutes, not back to back."
- *(Added D35, O3.)* If C's execution spans show CB and CN in separate spans: add "The two shared-job circuits ran in separate spans."
- **Never:** "the afternoon was unusual" or "3 November was a fluke". One more evening cannot show that. Never "every" or "all".

**Dry run of the reading** (`--worlds`, 200 binomial draws per world; D31). Each world now selects a true sentence:
- W5 (0.38, 0.38, 0.26, 0.26) → "clearly more often … but not the 40%" (75%), "may make a smaller difference" (16%) or a pass (10%, from draws with A ≥ 0.40).
- W6 (only B up) → the barrier-circuit fail sentence plus "One lone job came back and the other did not" (100%). The "none brought back" sentence never appears.
- W7 (shared job up) → "less often …, a clear difference" plus "The shared job came back" and "control moved" (100%).
- W9 (0.48, 0.48, 0.40, 0.40) → "running alone may add a smaller amount" (50%), "not clearly lower" (36%) or a pass (15%). Never "was not what caused it".
- W10 (alone lower) → "less often" (97%) or within (3%).
- W0–W4 and W8 are as in the review, except that W0's negative draws now read "a difference this test cannot pin down".

## 6. What it cannot do

- It cannot recreate 3 November's calibration, time of day or queue. A ran alone, but it ran on a different evening.
- It cannot see what IBM's server does differently for a one-PUB job, only whether the result differs.
- No readout calibration is taken this evening (§2). Readout drift since P3-15 would move P(yes) for A and C alike, so it does not touch the primary contrast.
- One circuit, one set of nine qubits, one evening.

## 7. Stop rules

- `run_hardware` refuses at 420 s. `--submit` refuses on every condition in §3, step 4.
- Each job is submitted once. If one fails, the others are not submitted this session, and a later submission needs a DEVIATIONS row.

## 8. Ledger entry (filled now, completed after audit)

```json
{"id": "ng-p3-16", "program": "nature-graded", "direction": "P3-16",
 "title": "Does 3 November's result come back when the circuit runs alone in its own job?", "source": "P1",
 "engine_odds": 0.05, "engine_odds_at": "2026-11-04T22:54:53-07:00",
 "human_odds": null, "human_odds_note": "no human odds",
 "prereg_commit": "<this commit>", "budget_usd": 0, "qpu_s_budget": 10,
 "referee": "nature", "bet_type": "standard", "seed_source": "curby-rng", "beacon": null, "seed": null, "tiebreak": null,
 "premortem": "If this fails, the most likely reason is that 3 November's 0.50 was a passing state of the chip, so the lone barrier job reads about 0.30, like every arm on 4 November.", "premortem_kind": "world",
 "lesson": "ls-ng-p3-16", "design_review": {"path": "ledger/design-reviews/ng-p3-16.md", "verdict": null, "commit": null, "reviewer_model": null, "fix_deviations": [], "missed": null},
 "verdict": "open", "date": "2026-11-04", "result": null, "audit": null, "diagnosis": null}
```

## 9. Checklist before submission

- [x] Committed with its code and DEVIATIONS row only. Nothing built against the live device, nothing submitted.
- [x] Engine odds on record (map, 22:54). Human odds: none in `ledger/human-odds.jsonl`, so marked "no human odds".
- [x] Pass rule and verdict sentences applicable by a stranger.
- [x] Pre-mortem: one sentence, checkable, with kind.
- [x] Lesson row filled after reading the ledger, Brier scores, audits and lessons. The same sentence goes to `ledger/lessons.jsonl` as `ls-ng-p3-16` (appended by the oversight-testbed session).
- [ ] Design review **go** (or confirmed fix-first); the engine's `budget_ruling` in `ledger/spend.jsonl` citing st-16 (D29); `check_prereg.py ng-p3-16 … --before-run` passes.
- [x] §2 records CURBY-Q round 28297 (stalled) and names CURBy-RNG; the seed commit follows.
- [x] Budget caps, hard stop, reserve rule, review gate, budget-ruling gate and the commit-before-submit guard enforced in code.
- [x] DEVIATIONS.md D28; D29 (budget gate); D31–D35 (design review ng-p3-16, F1–F5, O1–O3).
