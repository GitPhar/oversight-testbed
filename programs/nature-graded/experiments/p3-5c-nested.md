# P3-5c. Corrected P3-5: is steering present given blur, and blur given steering? (pre-registration, not scored)

Frozen at this file's commit time (America/Denver; the commit's author time is authoritative), in its own commit, before this analysis touches the archived counts. DEVIATIONS.md D10. Budget **$0 API · 0 QPU s · ≤ 3 laptop hours**. Requested by Sean (2026-11-04: "Pre-register the corrected P3-5 too").

## 0. The bet

| field | value |
|---|---|
| bet id | `ng-p3-5c` |
| referee | `nature` (the chip's archived counts) |
| bet type | `standard`, **not scored**: a corrected re-analysis of ng-p3-5's archive, which this program (P3-5, first run) and its auditor (round 2, exploratory joint fits: steering terms improved the fit by 22, 89 and 116 on the three pairs) have already analysed. Odds stated now would not be odds before data. |
| direction | `P3-5` (map/program-3-map.json), corrected per `ledger/audits/ng-p3-5.md` "What would break it next" |
| source | `P1` (audit round 2) |
| engine odds | **not stated**, for the reason above. ng-p3-5 (0.42, fail) remains the scored bet. |
| human odds | not asked: P3-5 is closed for human odds (D0); this is not a new direction. |
| budget | $0 · 0 QPU s · ≤ 3 laptop hours |
| pre-mortem | "If this fails, the most likely reason is that the 14-knob fits land in different local optima across bootstrap samples, widening the null and hiding steering that the point fit shows, as in the synthetic 'both' case." Kind: `design`. |
| lesson | Correcting P5, P4: P3-5's steering family could not change purity, and its T1/T2 overwrite never took effect. This re-analysis nests both kinds in one 14-knob model, tests each given the other by bootstrap, loads T1/T2 with an assertion, and states no odds because this program and its auditor already analysed the archive; it is not scored. |
| design review | a fresh auditor dry-runs this design (operators/design-review.md) → `ledger/design-reviews/ng-p3-5c.md`, launched by the oversight-testbed session. **`--run` refuses without a go** (or confirmed fix-first). |
| auditor | fresh session per operators/auditor.md, after results |

**What was read for the lesson** (operators/learn.md; engine `main` at the pre-fold commit cb1962a and after): `ledger/bets.jsonl` (9 scored, 2 hits), `ledger/brier.md` (0.236), running base rate 0.27, `ledger/lessons.jsonl` P1–P10, and `ledger/audits/ng-p3-5.md`, the newest relevant audit, including its "What would break it next", which this design follows.

## 1. In plain English

P3-5 asked whether program 1's chip errors were *steering* (small systematic rotations) or *blurring* (random noise), by fitting each kind separately and seeing which fitted better. The audit found two flaws. The steering model could not make a state more mixed, but the chip's states were more mixed than the simulator's, so blurring could win by construction. And the simulator's starting state used the wrong decay times, because of the T1/T2 bug. This re-analysis fixes both. It fits one model that has both kinds of error. Then it asks two separate questions: is steering needed once blurring is allowed, and is blurring needed once steering is allowed? Each answer comes from a bootstrap, which asks how big an improvement noise alone would produce. The likely answer, given what the audit already saw, is that both kinds are present. This re-analysis exists to say that properly, not to win a bet.

## 2. Material

- **Archive** (the same fields as P3-5 §2): `programs/entangled-mind/results/witness-run-1.json`, `items[*].hardware_counts[0:9]` and `hardware.assignment_matrix`; the as-run setting circuits `programs/entangled-mind/window/data/hardware/dbl6e1d8mdtc73d5gesg-{0..38}.json`; the calibration snapshot `results/ibm-calibration.json`, entry `dbl6e1d8mdtc73d5gesg`.
- **Reference state ρ_ref per item:** the P3-1 construction with the D8 fix. T1/T2 are loaded and **asserted** equal to the snapshot (`reference_states_fixed`). The circuit is ALAP-scheduled, simulated exactly as a density matrix with readout excluded, and the state is taken by linear inversion.
- **Models:**
  - **coh** (7 knobs): P3-5's family (i).
  - **inc** (7 knobs): P3-5's family (ii), reparametrised with direct, bounded probabilities: p_X, p_Y, p_Z ∈ [0, 0.25] per qubit and p ∈ [0, 0.5]. P3-5's softmax start at −8 had vanishing gradients and under-fitted in the first synthetic dry run (D10).
  - **full** (14 knobs): inc applied after coh. Each nested model is full with the other's knobs at zero.
  - Fits are L-BFGS-B, 1 zero start + 10 random starts, plus warm starts from the nested optima, so that logL_full ≥ max(logL_coh, logL_inc).
- **Tests per item:**
  - **steering given blur:** LR_c = 2(logL_full − logL_inc), with a null from B = 100 parametric bootstrap samples drawn from the fitted inc state.
  - **blur given steering:** LR_i = 2(logL_full − logL_coh), with a null from the fitted coh state.
  - p = (1 + #{LR* ≥ LR}) / (B + 1). Refits are warm-started from the full-data optima, plus 2 random starts.
- **Seed** (operators/hardware.md): CURBY-Q latest completed round **28297, result pulse 2025-08-22 13:42 America/Denver** (checked 2026-11-04 17:30), so it is **stalled**. **Seed: the first CURBy-RNG pulse timestamped after this commit**, by `ledger/seed.py --purpose boot`. Its `seed32` seeds numpy's `default_rng` for every start, bootstrap and CV draw. *Filled in by the seed commit:*
  `chain:` ___ · `pulse index:` ___ · `pulse_time:` ___ · `randomness:` ___ · `client:` ___ · `certificate_verified:` ___ · `seed (boot):` ___ · `seed32 (boot):` ___
- **Code:** `experiments/p3_5c_fits.py` (`--synthetic [--fast]`, `--run`).
- **Synthetic dry run before this commit (D4; no archive).** Four known truths on a mixed reference, B = 20 (so p ≥ 0.048):
  - blur only: LR_c 4.2, p 0.71, so steering correctly not flagged; LR_i 2,118.
  - steering only: LR_c 114; LR_i 0.0, p 0.71, so blur correctly not flagged.
  - both: LR_c 46.5, LR_i 1,802.
  - neither: LR_c 5.0, LR_i 0.1.
  - Leave-one-setting-out CV gain for steering was −112 (blur only), +57 (steering only), **−13.8 (both)** and −2.7 (neither).
  - A full B = 100 synthetic run was started before this commit. Its output (`data/p3-5c-synthetic-B100.json`) is committed when it finishes, before `--run`, for the reviewer.

## 3. Calls

| step | what | cost |
|---|---|---|
| 1 | seed commit | $0 |
| 2 | design review (fresh auditor; oversight-testbed session) | $0 |
| 3 | `--run`: ρ_ref × 3, fits, 2 × 100 bootstraps per item, 9-fold CV per item, spectator check on h088 and h268 | laptop, ≈ 1–2 h |

## 4. Statistics

- **Primary, per item and per kind:** "present" iff the bootstrap p < 0.01; otherwise "not detected".
- **Secondary, reported, not gates:**
  - **Leave-one-setting-out CV** gain of full over inc (steering) and over coh (blur). *Demoted from co-primary before data* (D10): the synthetic dry run showed it penalises the 14-knob model when a whole basis is held out. It gave −13.8 on data that truly contain steering, so requiring it would miss steering exactly when both kinds are present.
  - The old 7-v-7 ΔlogL, for comparison with P3-5.
  - Negativity and purity of each fitted state against ρ_ref; fitted parameters.
  - **Spectator check** (the audit's second $0 check), on h088 and h268. Re-simulate the as-run circuits with 0.1 rad ZZ added only on CZ pairs that do not touch the measured pair, sample 4,000 shots per setting through the item's assignment matrix, and refit. Report whether LR_c exceeds the 99th percentile of that item's real bootstrap null. If it does not, this design cannot tell spectator steering from blur on the pair.
- **One-item fragility** (P10): per-item labels are reported separately. The CV table gives each held-out setting's contribution, so a label resting on one setting (as h088's did on XX in P3-5) is visible.
- **Multiple comparisons:** 6 tests (3 items × 2 kinds) at α = 0.01 each. Also reported against Bonferroni α = 0.01/6.

## 5. Pre-registered reading (sentences written now, P9)

Per item:
- **both present:** "On pair <id>, the chip's errors need both a steering and a blurring part; neither kind alone explains the counts."
- **steering only:** "On pair <id>, steering is needed and blurring adds nothing detectable once steering is allowed."
- **blur only:** "On pair <id>, blurring is needed and steering adds nothing detectable once blurring is allowed."
- **neither:** "On pair <id>, neither kind is detectably needed beyond the simulator's state."
- **Overall:** report the count of pairs in each class. Never "blur, not steering" or "steering, not blur" unless every pair says so. If the spectator check shows spectator steering absorbed as blur, add: "A blurring label here can also come from steering on other qubits in the circuit."
- **Untestable:** ρ_ref cannot be built, or an optimiser returns a non-finite likelihood on an item. That item is reported untestable.

Not scored. P3-5's scored verdict (fail, "incoherent better" as its §5.2 count) stands as recorded. This re-analysis is reported beside it, never in place of it (SUMMARY-2, cross-cutting finding 4).

## 6. What it cannot do

- It describes three pairs on one afternoon (3 November, which P3-15 asks about), with the noise model's reference state. "Present" means "needed by this 14-knob model on these counts", not a physical mechanism.
- Steering on spectators may still pass as blur. That is what the spectator check measures.

## 7. Stop rules

$0, no network: the script reads only local archives. `--run` refuses without the seed file and a design-review go.

## 8. Ledger entry

```json
{"id": "ng-p3-5c", "program": "nature-graded", "direction": "P3-5",
 "title": "Corrected P3-5: steering given blur, and blur given steering (nested, bootstrap)", "source": "P1",
 "engine_odds": null, "engine_odds_note": "not stated: corrected re-analysis of an archive already analysed by the program and its auditor",
 "human_odds": null, "human_odds_note": "P3-5 closed for human odds (D0); not a new direction",
 "prereg_commit": "<this commit>", "budget_usd": 0, "qpu_s_budget": 0, "scored": false,
 "referee": "nature", "bet_type": "standard", "seed_source": "curby-rng", "beacon": null, "seed": null, "tiebreak": null,
 "premortem": "If this fails, the most likely reason is that the 14-knob fits land in different local optima across bootstrap samples, widening the null and hiding steering that the point fit shows, as in the synthetic 'both' case.", "premortem_kind": "design",
 "lesson": "ls-ng-p3-5c", "design_review": {"path": "ledger/design-reviews/ng-p3-5c.md", "verdict": null},
 "replication_of": "ng-p3-5", "verdict": "open", "date": "2026-11-04"}
```

## 9. Checklist

- [x] Committed with its code and DEVIATIONS row only. This analysis has not touched the archived counts.
- [x] Lesson row filled after reading the ledger; the same sentence goes to `lessons.jsonl` as `ls-ng-p3-5c`.
- [ ] Design review go (or confirmed fix-first) before `--run`.
- [x] §2 records CURBY-Q round 28297 (stalled) and names CURBy-RNG; seed commit follows.
- [x] DEVIATIONS.md D10.
