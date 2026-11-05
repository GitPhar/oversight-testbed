# P3-15. What made 3 November different: the afternoon, or the circuit's barrier and shot grouping? (pre-registration)

Frozen at this file's commit time (America/Denver; the commit's author time is authoritative), in its own commit, before any circuit is built against the live device or submitted. DEVIATIONS.md D9. Budget **$0 API · ≤ 5 QPU s per run, 2 runs (estimate 3.4 s each, 6.8 s total) · 1 laptop hour**. Hardware only through `entangled-mind/src/entangled_mind/backends.py::run_hardware`, which refuses at the 420 s hard stop. **Each run is submitted once, never resubmitted.**

## 0. The bet

| field | value |
|---|---|
| bet id | `ng-p3-15` |
| referee | `nature` |
| bet type | `standard` (program-level referee experiment under CONTEXT rule 7) |
| direction | `P3-15` (map/program-3-map.json, added 2026-11-04 17:00, commit c6e2945) |
| source | `P1` (audit round 2, `ledger/audits/ng-p3-2-3.md`, "What would break it next") |
| engine odds, P(pass) | **7**, elicited 2026-11-04 17:00:05 in a fresh context from `map/odds-elicitation/rows-v1-p3-15.md` alone (template v1, single row; `map/odds-elicitation/v1-p3-15.md`). Unchanged by the lesson (below). |
| human odds, P(pass) | **none**: Sean skipped this direction's question (2026-11-04 ~17:00, `map/human-odds.md` Q15). Recorded as no odds, not 50. |
| budget | $0 API · ≤ 5 QPU s per run × 2 · 1 laptop hour |
| approval | Sean, 2026-11-04 (oversight-testbed steer st-11): "run the wave-2 repeat test under the lesson and design-review rules, first run now, second at least 3 hours later." |
| pre-mortem | "If this fails, the most likely reason is that IBM's servers already schedule measurements as late as possible, so the barrier changes nothing and both 1,000-shot blocks read about 0.25, as 4 November did." Kind: `world`. |
| lesson | Correcting P8, P6, P10: 3 and 4 November differed in barrier, shot grouping and date. This bet varies barrier and grouping within one job, checks its no-barrier arm against 4 November's 0.246, and repeats hours later, and its odds are 7% (from 7% on the map) because ng-p3-1 found idle timing does not move this circuit. |
| design review | before the first submission, a fresh auditor dry-runs this design (operators/design-review.md) → `oversight-testbed/ledger/design-reviews/ng-p3-15.md`, launched by the oversight-testbed session. **No submission before a go** (or a confirmed fix-first). `--submit` checks the review file's verdict in code. The review also checks the D8 `overwrite_calibration` fix; this bet's predictions do not call it (§2). |
| auditor | fresh session per operators/auditor.md, after results |

**What was read for the lesson** (operators/learn.md, step 1; oversight-testbed `cb1962a`): `ledger/bets.jsonl` (27 rows; 9 scored, 2 hits), `ledger/brier.md` (engine Brier 0.236; always-base-rate 0.173), running base rate (2 + 1)/(9 + 2) = **0.27**, `ledger/lessons.jsonl` (P1–P10), and `ledger/audits/` through `SUMMARY-2.md` and `ng-p3-2-3.md`, the newest read. **Why the odds stay below the base rate** (learn.md: moving away needs a reason from the ledger). ng-p3-1 (re-run, D8) found that idle timing moves this circuit's predicted P(yes) by about 0.000, and the barrier can act only through measurement timing (§2). ng-p3-2's 4 November no-barrier run matched its simulator. The bets given under 20% so far (em-gm1 15%, ng-p3-1 7%, ng-p3-3 12%) all missed or were untestable. The fresh elicitor's 7% is kept, not lowered further.

## 1. In plain English

On 3 November the chip answered "yes" 50% of the time on program 1's circuit, about twice what its own description predicts. On 4 November it answered 25%, about what the description predicts. But the two runs differed in three ways at once. The 3 November circuit had a "barrier" making all nine qubits wait and be measured together at the end; ours did not. The 3 November run was one block of 1,000 shots; ours was 20 small pieces mixed among other circuits. And they were a day apart. This test varies the first two inside one job, so the day is the same for every arm, and then repeats the whole job at least three hours later. If restoring the barrier brings the 50% back, the surprise was how the circuit was built. If it doesn't, and the barrier and grouping make no difference, the surprise belonged to the chip on 3 November (or to something neither run varied). The barrier can only matter if IBM's servers measure qubits early when no barrier stops them, and nothing we have read says whether they do.

## 2. Material

- **Circuit.** Program 1's Stage 1 gate list (`entangled-mind/window/data/hardware/dbl423dgg49c73dk0db0-0.json`, SHA-256 `a773bd6e…4029`), rebuilt by `p3sim.load_isa`, on its original physical qubits (clbit order 117, 125, 124, 123, 144, 136, 143, 141, 142).
  - **No-barrier arms (N):** exactly as submitted on 4 November.
  - **Barrier arms (B):** the same, plus one barrier across the nine qubits immediately before the first measurement. That is where `measure_all()` put it in program 1 (`entangled_mind/encoder.py:162`). The archive's gate list had dropped it.
  - Checked before this commit on FakeFez (structure only): one barrier on 9 qubits; otherwise identical gate lists; every instruction native.
- **Does the manipulation take effect?** (P4) Offline, in Qiskit's schedulers on FakeFez durations: under ALAP, all nine measurements start at 8.052 µs with or without the barrier. Under ASAP, without the barrier they start at 3.300, 3.732, 4.164, 5.436, 6.360, 7.512, 7.836, 8.028 and 8.052 µs, and with it all at 8.052 µs. So the barrier changes the executed schedule only if IBM's server-side scheduling lets measurements run early. That cannot be checked offline, and it is the pre-mortem. The prediction file records both schedules' simulated P(yes).
- **Arms, per run** (`experiments/p3_15_repeat.py`; 32 PUBs, 5,000 shots):
  - **BB**, barrier, one PUB × 1,000 shots: *(amended D14)* 3 November's circuit, qubits and single 1,000-shot PUB, inside a 32-PUB job (3 November's ran alone).
  - **NB**, no barrier, one PUB × 1,000.
  - **BI**, barrier, 10 PUBs × 100, interleaved.
  - **NI**, no barrier, 10 × 100, interleaved: *(amended D14)* 4 November's circuit, qubits and 100-shot pieces (10, not 20, in a 32-PUB job, not a 200-PUB one).
  - *(Added D14.)* After the job, the raw file also saves each PUB's per-shot bitstrings and the job's execution spans (a free read of `job.result()`). **BB (and NB) count as a contiguous block only if no execution span containing that PUB's shots contains another PUB.** Otherwise the block-against-interleaved contrast is reported as "PUB grouping", not "grouping in time", and the grouping sentences say so.
  - **R0, R1**, readout calibration all-0 and all-1, 5 × 100 each, interleaved.
  - The job's three units [BB, NB, interleaved section] go in a seeded order, as do the 30 pieces of the interleaved section. Per-PUB shot counts are passed as SamplerV2 PUB tuples through `run_hardware`, unchanged. `run_hardware`'s usage row logs its `shots` argument (100), not the per-PUB counts, so the result file gives the true shots.
  - **Matched comparisons** (P8): BB against NB differ only in the barrier (same job, same qubits, same grouping, adjacent in time only if the seeded order makes them so). B against N pooled, and block against interleaved pooled, each differ in one factor, averaged over the other. Run 1 against run 2 differ only in date and time (and the seeded order).
- **Predictions** (the P3-2 construction, **not** `p3sim.overwrite_calibration`): `NoiseModel.from_backend` of the live ibm_fez target read just before each run, 100,000 shots, seed `sim`. *(Amended D13.)* Four predictions: barrier and no barrier, each ALAP and ASAP. The predicted barrier effect is barrier_ALAP − nobarrier_ALAP if IBM schedules ALAP, and barrier_ASAP − nobarrier_ASAP if ASAP. On FakeFez these are 0.000 and about +0.011 (design review ng-p3-15), both far below the Δ ≥ 0.10 bar. Both are reported beside the measured Δ. Committed per run (`data/p3-15-run<k>-predictions.json`, with the circuits in `data/p3-15-run<k>-circuits.qpy` and their SHA-256) before that run is submitted. `--submit` refuses otherwise.
- **Seed** (operators/hardware.md): CURBY-Q latest completed round **28297, result pulse 2025-08-22 13:42 America/Denver** (checked 2026-11-04 17:11 with `experiments/curby_seed.mjs check`, before this commit). It is more than 24 h old, so **stalled**. **Seed: the first CURBy-RNG pulse timestamped after this commit.** Sub-seeds by `ledger/seed.py --purpose`: `order1`, `order2` (each run's PUB order), `sim` (Aer seed). `seed32` is used. *Filled in by the seed commit, before anything is built against the live device:*
  `chain:` CURBy-RNG · `pulse index:` 1591477 · `pulse_time:` 2026-11-04 17:13:00 America/Denver · `previous pulse:` index 1591476 at 2026-11-04 17:12:00 (before the commit at 2026-11-04 17:12:21) · `randomness:` 5b452d1f5554a696970609f549a64db8db115d0c7ab66cc9204faca8b03cfb81233e101745d7c69ab55800cb3f27d5cf9d69e94f235a636ebe7a78e791caa187 · `client:` @buff-beacon-project/curby-client@1.2.0 via `experiments/curby_seed.mjs` · `certificate_verified:` false · `seed (order1):` 499467276445145335 · `seed32 (order1):` 1970395383 · `seed (order2):` 411795150628068766 · `seed32 (order2):` 4184481182 · `seed (sim):` 11843306263413918700 · `seed32 (sim):` 1290931180. Record: `data/p3-15-seed.json`.

## 3. Calls

| step | what | calls | est. cost |
|---|---|---|---|
| 1 | seed commit | CURBy | $0 |
| 2 | design review by a fresh auditor (launched by the oversight-testbed session) | 0 paid | $0 |
| 3 | `--predict 1`: read the live target (IBM API, 0 QPU s), build run 1's 32 PUBs, three predictions; commit | 1 IBM read | laptop |
| 4 | `--submit 1`: refuses without a go, without `check_prereg.py --before-run` passing, without a committed prediction file, if the raw file or a `Program 3 P3-15 run 1` QPU-ledger entry already exists, above a 5 s estimate, or under the reserve rule (cumulative + 1.5 × estimate ≤ 300 s); then one `run_hardware` job. The raw counts are written the moment it returns (amended D15) | 1 job | ≈ 3.4 QPU s |
| 5 | `--predict 2`, commit; `--submit 2` refuses until ≥ 3.0 h after run 1's job finished | 1 IBM read, 1 job | ≈ 3.4 QPU s |
| 6 | `--analyse` | 0 | laptop |

If the session ends before run 2, run 2 is reported as not run. Run 1 alone decides the verdict.

## 4. Statistics

- **P(yes)** per arm: `readout.quantum_readout` on the arm's pooled raw counts. No readout mitigation. Binomial SE, √(p(1 − p)/n).
- **Primary statistic** (run 1): P_BB, and Δ = P_BB − P_NB with z = Δ / √(SE_BB² + SE_NB²).
- **Secondary, reported, not scored:**
  1. **Barrier effect, pooled:** (BB + BI) − (NB + NI), 2,000 shots a side, with a 90% CI. **Equivalence margin 0.05** (P2): "no barrier effect larger than 0.05" only if the whole 90% CI lies inside (−0.05, +0.05). Power: SE ≈ 0.014, so the CI half-width is ≈ 0.023. With no true effect, the CI falls inside the margin about 95% of the time.
  2. **Grouping effect, pooled:** (BB + NB) − (BI + NI), same margin.
  3. **Control** (P6): NI (*amended D14*: 4 November's circuit, qubits and 100-shot pieces, in a smaller job) should be within 0.05 of 4 November's 0.246. It fails if the device has moved since (it would reject, for example, a return to 3 November's 0.50). It gates the reading, not the verdict (§5).
  4. **Drift** (run 2 − run 1) per arm and pooled, with 90% CIs; "stable within 0.05" only if both pooled B and N CIs lie inside ±0.05.
  5. Per-qubit marginals for every arm against the predictions, qubit 125 especially. Readout matrices from R0/R1. Billed against estimated seconds.
- **Multiple comparisons:** one scored test. The secondaries are labelled.
- **One-item fragility** (P10): this is one circuit by design, so leave-one-item-out does not apply. Its stand-in is run 2. If run 2's primary label (the same rule applied to run 2) differs from run 1's, the verdict is reported as **"run 1's label, unstable across runs"**.

## 5. Pre-registered reading

1. **Pass:** run 1 gives P_BB ≥ 0.40, Δ ≥ 0.10 and z ≥ 3.
2. **Fail:** run 1 completes and is not a pass.
3. **Untestable:** run 1's job errors, returns fewer than 90% of its 5,000 shots, or returns any PUB with a shot count different from its label (e.g. the server ignored per-PUB shots). It is not resubmitted. *(Implemented in code, D12.)*

**The plain-English sentences, written now** (P9). The write-up uses these and no stronger nouns.
- *Pass:* "With the barrier restored and run as one 1,000-shot block, the chip again said 'yes' at least 40% of the time, clearly more than the same circuit without the barrier in the same job. The 3 November surprise came at least partly from how the circuit was built (the barrier), not only from that afternoon."
- *Fail with BB < 0.40, and the pooled barrier effect within ±0.05:* "Restoring the barrier did not bring back 3 November's result, and in this job the barrier made no difference larger than 0.05 (assuming IBM's servers treated 3 November's identical submission the same way). The surprise was not the barrier." *(Amended D11.)* Then, **only if the pooled grouping effect is also within ±0.05**, add: "It belonged to something this test held fixed or could not vary: the chip on 3 November, or a difference neither run had."
- *Fail with BB < 0.40, and the barrier effect neither within ±0.05 nor large enough to pass:* "Restoring the barrier did not bring back 3 November's result. The barrier may make a smaller difference (Δ = …), which this job cannot pin down."
- *(Added D11.) Fail with BB ≥ 0.40 and NB ≥ 0.40* (3 November's value returns without the barrier): "The chip again said 'yes' about half the time, with or without the barrier. 3 November's result came back, and the barrier was not what caused it." If BI and NI are also ≥ 0.40, add: "It came back in every arm, so on this run it belonged to the chip, not to how the circuit was built or grouped."
- *(Added D11; secondary.) Grouping:* if the pooled block − interleaved effect is ≥ 0.10 with z ≥ 3: "Running the circuit as one 1,000-shot PUB gave a higher 'yes' rate than running it in 100-shot pieces (difference …), in the same job. Shot grouping, not only the day, contributed." If it is within ±0.05: "Shot grouping made no difference larger than 0.05." Otherwise: "Grouping may make a smaller difference (…), which this job cannot pin down." If BB was not a contiguous block (§2, D14), "grouping" in these sentences is "PUB grouping".
- *Control failed (NI more than 0.05 from 0.246):* add "The chip itself had moved since 4 November: the 4 November configuration now gives … ." Any barrier contrast is still within this job.
- *Run 2 agrees and drift is stable within ±0.05:* add "Three hours later the chip gave the same answers within 0.05."
- *Run 2 disagrees:* the verdict is labelled "unstable across runs" (§4), and the drift is reported.
- **Never:** "the afternoon was unusual", unless a later series of runs shows it. Two days cannot.

A pass is reported as **pass, unreplicated** until run 2 agrees (invariant 7).

## 6. What it cannot do

- It cannot see IBM's server-side schedule. If the barrier changes nothing, this test cannot say whether that is because IBM schedules ALAP or because early measurement does not matter.
- It cannot recreate 3 November's "own job" exactly: BB shares a job with 31 other PUBs. *(Amended D14.)* BB is a single PUB of 1,000 shots. Whether those shots ran back to back is known only after the job, from its execution spans (§2). The write-up says "one 1,000-shot block" only if they did.
- It cannot reproduce 3 November's calibration. If neither the barrier nor the grouping matters, "the afternoon" stays the remaining candidate *among the things varied*, not a demonstrated cause.
- One circuit, one set of nine qubits. "Every" and "all" will not appear.

## 7. Stop rules

- `run_hardware` refuses at 420 s. `--submit` refuses without a design-review go, without committed predictions, if the run already ran, above a 5 s estimate, under the reserve rule, or (for run 2) before 3.0 h.
- Each run is submitted once. If a run fails, it is not resubmitted this session.

## 8. Ledger entry (filled now, completed after audit)

```json
{"id": "ng-p3-15", "program": "nature-graded", "direction": "P3-15",
 "title": "What made 3 November different: the afternoon, or the circuit's barrier and shot grouping?", "source": "P1",
 "engine_odds": 0.07, "engine_odds_at": "2026-11-04T17:00:05-07:00",
 "human_odds": null, "human_odds_note": "Sean skipped (no odds), map/human-odds.md Q15, 2026-11-04 ~17:00",
 "prereg_commit": "<this commit>", "budget_usd": 0, "qpu_s_budget": 10,
 "referee": "nature", "bet_type": "standard", "seed_source": "curby-rng", "beacon": null, "seed": null, "tiebreak": null,
 "premortem": "If this fails, the most likely reason is that IBM's servers already schedule measurements as late as possible, so the barrier changes nothing and both 1,000-shot blocks read about 0.25, as 4 November did.", "premortem_kind": "world",
 "lesson": "ls-ng-p3-15", "design_review": {"path": "ledger/design-reviews/ng-p3-15.md", "verdict": null, "commit": null, "reviewer_model": null, "fix_deviations": [], "missed": null},
 "verdict": "open", "date": "2026-11-04", "result": null, "audit": null, "diagnosis": null}
```

## 9. Checklist before the first submission

- [x] Committed with its code and DEVIATIONS row only. Nothing built against the live device, nothing submitted.
- [x] Engine odds on record (map, 17:00:05). Human odds: skipped by Sean.
- [x] Pass rule and verdict sentences applicable by a stranger.
- [x] Pre-mortem: one sentence, checkable, with kind.
- [x] Lesson row filled after reading the ledger, brier, audits and lessons; the same sentence goes to `ledger/lessons.jsonl` as `ls-ng-p3-15` (appended by the oversight-testbed session).
- [ ] Design review **go** (or confirmed fix-first) before `--submit 1`; `check_prereg.py ng-p3-15 … --before-run` passes.
- [x] §2 records CURBY-Q round 28297 (stalled) and names CURBy-RNG; the seed commit follows.
- [x] QPU budget, hard stop, review gate and 3 h gap enforced in code.
- [x] DEVIATIONS.md D9.
