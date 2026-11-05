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
- **Models** *(amended D19, design review `ledger/design-reviews/ng-p3-5c.md` F1)*:
  - **coh** (7 knobs, *rotation-type*): P3-5's family (i), local rotations and a ZZ phase.
  - **inc9** (9 knobs, *blur-type*): amplitude damping γ_i, γ_j ∈ [0, 0.2] (energy decay beyond the simulator's), then Pauli flips p_X, p_Y, p_Z ∈ [0, 0.25] per qubit, then uniform mixing p ∈ [0, 0.5]. The frozen version had no damping. Damping is non-unital, and a rotation could partly imitate it, so the review's synthetic decay at γ = 0.03 was falsely flagged as steering in 6 of 24 draws.
  - **full16** (16 knobs): inc9 applied after coh. Each nested model is full16 with the other's knobs at zero.
  - **Secondary**, for continuity with the frozen design: inc7 (no damping) and full14.
  - Fits: L-BFGS-B, 1 zero start + 10 random starts, plus warm starts from the nested optima.
- **Tests per item:**
  - **rotation given blur:** LR_c = 2(logL_full16 − logL_inc9), null from the fitted inc9 state.
  - **blur given rotation:** LR_i = 2(logL_full16 − logL_coh), null from the fitted coh state.
  - Parametric bootstrap: **B = 100, extended to B = 1,000 whenever p ≤ 0.05** *(amended D20, F2)*, parallelised. Every p is reported with its floor 1/(B + 1) (0.0099 or 0.0010). The Bonferroni line 0.01/6 = 0.0017 is reachable only at B = 1,000.
- **Seed** (operators/hardware.md): CURBY-Q latest completed round **28297, result pulse 2025-08-22 13:42 America/Denver** (checked 2026-11-04 17:30), so it is **stalled**. **Seed: the first CURBy-RNG pulse timestamped after this commit**, by `ledger/seed.py --purpose boot`. Its `seed32` seeds numpy's `default_rng` for every start, bootstrap and CV draw. *Filled in by the seed commit:*
  `chain:` CURBy-RNG · `pulse index:` 1591496 · `pulse_time:` 2026-11-04 17:32:00 America/Denver · `previous pulse:` index 1591495 at 2026-11-04 17:31:00 (before the commit at 2026-11-04 17:31:33) · `randomness:` 27bba9e6c499e9a8a5647a0fcbdfd2947575e32c8a466e1f8b3daf80b95adeee2ba5836c348be9e0714f139e1b0edd4011d11494400f87c3729e7d1892e9731a · `client:` @buff-beacon-project/curby-client@1.2.0 via `experiments/curby_seed.mjs` · `certificate_verified:` false · `seed (boot):` 10131417812182473074 · `seed32 (boot):` 1446222194. Record: `data/p3-5c-seed.json`.
- **Code:** `experiments/p3_5c_fits.py` (`--recovery`, `--run`). `--run` refuses without the seed file, without a design-review go, and unless `ledger/check_prereg.py ng-p3-5c … --before-run` passes *(D25)*.
- **Dry-run record, corrected** *(D21, F3)*. The first synthetic dry run (B = 20, then B = 100, `data/p3-5c-synthetic-B100.json`) used a reference that is a ZZ eigenstate, on which the ZZ phase does nothing. It is **replaced as the D4 evidence by the D19 recovery study** (`data/p3-5c-recovery.json`). That study uses the **three real reference states** (T1/T2 loaded), synthetic counts (4,000 × 9 settings, a generic assignment matrix, no archive counts), and six truths: neither; blur only; rotation only; both; an XX rotation of 0.15 rad (outside the rotation family); and amplitude damping γ = 0.03 per qubit (outside the frozen blur family). It also has 8-draw false-flag rates for decay, and power at blur 0.25%, 0.5%, 1% per qubit and rotation norms 0.025, 0.05, 0.1 rad. **D10's reason for demoting CV is restated:** CV is a noisy single-draw quantity (−13.8 and +18.7 on two draws of the same truth). It is not shown to penalise the 16-knob model.
## 3. Calls

| step | what | cost |
|---|---|---|
| 1 | seed commit | $0 |
| 2 | design review (fresh auditor; oversight-testbed session) | $0 |
| 3 | `--run`: ρ_ref × 3, fits, 2 × 100 bootstraps per item, 9-fold CV per item, spectator check on h088 and h268 | laptop, ≈ 1–2 h |

## 4. Statistics

- **Primary, per item and per kind:** "present" iff the bootstrap p < 0.01 (B adaptive, D20); otherwise "not detected".
- **Secondary, reported, not gates:**
  - **Goodness of fit** *(D22, F4)*: the full16 deviance against the saturated likelihood, 2(logL_sat − logL_full16), on 27 − 16 = 11 df, compared with χ²₁₁'s 99th percentile (24.7). The 14-knob version uses 13 df.
  - **Per-setting shares** *(D24, F6)*: each setting's contribution to LR_c and LR_i at the fitted optima. If one setting carries more than half of an LR labelled present, the sentence adds "This rests mostly on setting <S>", and the bet refits with that setting dropped and reports whether the LR still exceeds the item's null 99th percentile (in-sample, not a gate).
  - **Spectator check** *(D23, F5)*, h088 and h268. 0.1 rad ZZ is added only on CZ pairs not touching the measured pair. Report the trace distance between that state and ρ_ref, and 20 synthetic draws through the item's assignment matrix, each classified with the item's real-data bootstrap 99th percentiles (q99_c, q99_i) into exactly one outcome:
    - **detected as rotation:** LR_c > q99_c;
    - **absorbed as blur:** LR_c ≤ q99_c and LR_i > q99_i;
    - **invisible:** neither.
    - The share of each outcome is reported.
  - **CV** *(D21)*: leave-one-setting-out held-out gain, a noisy secondary.
  - **The P3-5 comparison, three ways** *(D25, F7)*:
    - P3-5's own families and fit on the legacy (T1/T2-bug) reference, which should reproduce −43.5, −34.9, +63.0;
    - the same on the fixed reference (isolating the T1/T2 fix);
    - the bounded 7-knob blur family on the fixed reference (isolating the reparametrisation);
    - also the 9-knob family (adding decay).
  - The 14-knob secondary set's labels; negativity of each fitted state.
- **Multiple comparisons:** 6 tests (3 items × 2 kinds) at α = 0.01 each, also reported against Bonferroni 0.0017.

## 5. Pre-registered reading (sentences written now, P9; amended D22, F4)

Per item:
- **both present:** "On pair <id>, the counts need both a rotation-type term (local rotations and a ZZ phase) and a blur-type term (random Pauli flips, uniform mixing and energy decay) beyond the simulator's state; neither alone fits as well."
- **rotation only:** "On pair <id>, a rotation-type term is needed; once rotations are allowed, a blur-type term adds nothing this test could detect (in synthetic checks on these reference states it detected blur of 1% per qubit in only 2 to 6 of 8 draws, and blur of 0.25% per qubit in none, so this does not rule out blur of about 1% per qubit)."
- **blur only:** "On pair <id>, a blur-type term is needed; once blur is allowed, a rotation-type term adds nothing this test could detect (in synthetic checks on these reference states it detected rotations of 0.1 rad in every draw, and rotations of 0.025 rad in only 1 to 3 of 8)."
- **neither:** "On pair <id>, neither term is detectably needed beyond the simulator's state."
- Appended to every per-pair sentence: "These are terms in a 16-knob model fitted to these counts, not identified physical mechanisms."
- **CV disagrees** with a label: "On pair <id>, the <kind> term improves the in-sample fit (p = …) but not the prediction of a held-out setting (CV gain …); read the label as weaker."
- **One setting dominates** (D24): add "This rests mostly on setting <S>."
- **Misfit** (deviance above χ²₁₁'s 99th percentile): "Even both terms together leave a misfit the model cannot explain (deviance … on … df), so part of what each term absorbs may be neither kind."
- **Spectator "absorbed as blur"** (the majority of the 20 draws): "A blur-type label here can also come from rotations on other qubits in the circuit." **"Invisible":** "At 0.1 rad, spectator rotations were too small to see on this pair, so this check cannot rule them out."
- **Overall:** the count of pairs in each class, then, once: "This re-analysis was specified before it ran, but the archive had already been analysed by this program and its auditor, who saw both kinds of term on every pair; it is not a blind test." Never "blur, not steering" or the reverse unless every pair says so.
- **Untestable:** ρ_ref cannot be built, or an optimiser returns a non-finite likelihood on an item.

Not scored. P3-5's scored verdict stands as recorded. This re-analysis is reported beside it, never in place of it.

## 6. What it cannot do

- It describes three pairs on one afternoon (3 November, which P3-15 asks about), with the noise model's reference state. "Present" means "needed by this 16-knob model on these counts", not a physical mechanism. (The §0 lesson's "14-knob" describes the design as frozen at 930efe8; D19 made the primary model 16 knobs.)
- Steering on spectators may still pass as blur. That is what the spectator check measures.
- **Recovery study limits** (`data/p3-5c-recovery.json`, one draw per cell, 8 per rate; recorded before `--run`, D26):
  - Amplitude damping of 0.03 per qubit was **not** read as rotation by the primary test on any pair (1 false flag in 24 draws, against 6 in 24 for the frozen design). It was not detected as blur either (p 0.13, 0.09, 0.03), so decay of that size is invisible here, not mislabelled. The 14-knob secondary still labelled it rotation on h221, which is why it stays secondary.
  - An XX rotation of 0.15 rad, outside the rotation family, was labelled rotation on every pair, and also blur on h088 (p = 0.010). So a blur label beside a rotation label can partly be a rotation the family does not contain.
  - Power (8 draws per level, against the matching null's 99th percentile): blur 0.25% / 0.5% / 1% per qubit detected in 0 / 1 / 2–6 of 8; rotation norms 0.025 / 0.05 / 0.1 rad in 1–3 / 3–7 / 8 of 8. Blur power is lower than the design review's estimate (about 1% almost surely), because the blur family now includes decay.
  - The four in-family truths (neither, blur only, rotation only, both) were labelled correctly on every pair.

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
