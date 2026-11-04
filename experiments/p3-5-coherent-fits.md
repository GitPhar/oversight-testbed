# P3-5. Coherent or incoherent, from program 1's archived tomography (pre-registration)

Frozen at this file's commit time (America/Denver; the commit's author time is authoritative), in its own commit, before the hardware counts are opened for this analysis. DEVIATIONS.md D2. Budget **$0 API · 0 QPU s · < 1 laptop hour**.

## 0. The bet

| field | value |
|---|---|
| bet id | `ng-p3-5` |
| referee | `nature` (the chip's archived counts decide which error model fits) |
| bet type | `standard` |
| direction | `P3-5` (map/program-3-map.json) |
| source | `engine` (map tag E) |
| engine odds, P(pass) | **0.42**, stated 2026-11-04T14:06:13-07:00 in map/program-3-map.json (template v1-batch). Not in the elicitation-check half. |
| human odds, P(pass) | **not recorded**: Sean chose to proceed without his odds (D0); closed for human odds. |
| budget | $0 API · 0 QPU s · < 1 laptop hour |
| pre-mortem | "If this fails, the most likely reason is that the lost negativity comes mostly from depolarising-type decay, which the incoherent family's global depolarising term captures and local rotations plus one ZZ phase cannot." Kind: `world`. |
| auditor | fresh session per operators/auditor.md, after results |

## 1. In plain English

In program 1, the chip held two-qubit entanglement on all three test items, but less than the simulator expected. We still hold the detailed measurements: nine measurement settings per item, 4,000 shots each. Errors on a chip come in two broad kinds. *Steering* (coherent) errors rotate the state a little, the same way every time. *Blurring* (incoherent) errors scramble it randomly. We give each kind the same number of adjustable knobs, seven, fit both to the chip's counts, and see which explains them better. If steering wins clearly on at least two of the three items, the chip's errors are mostly systematic. That matters because IBM's reported error rates are averaged in a way that hides steering errors, and because it decides which error-suppression settings the later tests should use. If blurring wins, the reported rates are probably a fair description and the missing entanglement is ordinary decay.

## 2. Material

- **Archives read.** `entangled-mind/results/witness-run-1.json`: for each of the 3 items, `id`, `physical_qubits`, `hardware_counts[0:9]` (the 9 tomography settings, in the order XX, XY, XZ, YX, YY, YZ, ZX, ZY, ZZ, where the first letter is the clbit-0 qubit), `hardware.assignment_matrix` (from the item's 4 readout-calibration circuits on the same two qubits), and, for the report only, `hardware.negativity` and `noisy_sim.negativity`. The as-run setting circuits are `entangled-mind/window/data/hardware/dbl6e1d8mdtc73d5gesg-{0..38}.json` (`role`, `item`, `setting`, `gates`). The job-time calibration is `entangled-mind/results/ibm-calibration.json`, entry `dbl6e1d8mdtc73d5gesg`. The archived negativities (0.147, 0.063, 0.067 hardware; 0.171, 0.149, 0.118 noisy sim) are already published and were in the map row. No count, likelihood or fit on these data has been computed by this program before this commit.
- **Reference state ρ_ref per item:** the P3-1-corrected simulator (FakeFez + the witness job's calibration snapshot, ALAP-scheduled; `experiments/p3sim.py`, frozen by P3-1). Each of the 9 as-run setting circuits is simulated exactly as a density matrix, with the final measurements replaced by exact outcome probabilities on the two measured qubits, so readout error is excluded. Linear inversion, as in program 1's `witness_design.reconstruct` with no readout matrix, gives ρ_ref, projected to the nearest physical state. Before this commit, a structure-only check built ρ_ref for item h221 (trace 1, Hermitian). Its contents were not printed or inspected.
- **Families** (7 parameters each, both containing ρ_ref at the start point):
  - (i) **coherent:** ρ = U ρ_ref U†, U = (U_j ⊗ U_i)·exp(−iφ ZZ/2), with U_q = Rz(a)Ry(b)Rz(c);
  - (ii) **incoherent:** ρ = (1−p)·(Λ_j ⊗ Λ_i)(ρ_ref) + p·I/4, with Λ_q a Pauli channel (p_X, p_Y, p_Z by softmax against p_I) and p a sigmoid.
- **Measurement model:** P(outcome | setting) = A · diag(V ρ V†), with V the basis change (X: H; Y: H·S†) and A the archived hardware assignment matrix of that item. Multinomial log-likelihood over 9 settings × 4 outcomes.
- **Fitting:** L-BFGS-B. For each family and item: 1 start at ρ_ref (zero angles; logits −8), plus 20 random starts (angles U(−0.3, 0.3); logits U(−8, −2)) drawn from the seed. The best of the 21 is kept.
- **Code:** `experiments/p3_5_fits.py`. A dry run on synthetic counts only (`--synthetic`, before this commit; no archive) recovered the generating family both ways: ΔlogL +73 on coherent-generated data, −2,053 on incoherent-generated data.
- **Seed** (operators/hardware.md): CURBY-Q latest completed round **28297, result pulse 2025-08-22 13:42 America/Denver** (checked 2026-11-04 15:30, before this commit), so it is **stalled**. **Seed: the first CURBy-RNG pulse timestamped after this commit.** seed = the first 8 bytes of SHA-256(randomness ‖ `ng-p3-5`) by `ledger/seed.py --purpose starts`. Its `seed32` seeds numpy's `default_rng` for the random starts. *Filled in by the seed commit, before the archive is opened:*
  `chain:` ___ · `pulse index:` ___ · `pulse_time:` ___ · `randomness:` ___ · `client:` ___ · `certificate_verified:` ___ · `seed (starts):` ___ · `seed32 (starts):` ___

## 3. Calls

| step | what | calls | est. cost |
|---|---|---|---|
| 1 | ρ_ref per item (27 exact density-matrix simulations) | 0 | laptop, ~1.5 min |
| 2 | fit both families per item (primary) | 0 | laptop |
| 3 | secondary: the same fits with the ideal (noiseless) reduced state as reference | 0 | laptop |

## 4. Statistics

- **Primary statistic:** per item, ΔlogL = max logL(i) − max logL(ii). Unit: items (3).
- **Count:** the number of items with ΔlogL ≥ 10.
- **Uncertainty:** none beyond the threshold. ΔlogL ≥ 10 between two families with equal parameter counts is an AIC/BIC-equivalent margin far beyond chance (likelihood ratio e¹⁰).
- **Secondary, reported, not scored:** logL of ρ_ref unfitted and of the saturated multinomial; fitted φ and local angles; fitted p; the negativity of each fitted state against the archived hardware value; the same ΔlogL with the ideal reference.
- **Multiple comparisons:** one scored rule over 3 items; none applied.

## 5. Pre-registered reading

1. **Pass:** ΔlogL ≥ 10 on at least 2 of the 3 items (coherent family clearly better).
2. **Fail:** fewer than 2 items reach ΔlogL ≥ 10. Reported with the sign: "incoherent better" if ΔlogL ≤ −10 on at least 2 items; otherwise "neither clearly".
3. **Untestable:** ρ_ref cannot be built for an item, or an optimiser returns a non-finite likelihood. Untestable on 2 or more items makes the bet untestable.
4. **Reported in every case:** every item's ΔlogL, the four likelihoods, and the fitted parameters.

## 6. What it cannot do

- Each family has one global two-qubit term (ZZ phase versus depolarising). Real noise is a mixture, so a win means "better described by", not "is".
- The archived tomography was taken with no twirling and no DD. That is the condition the map asks about. Nothing here says what twirling would do (P3-2's question).
- Three items on three qubit pairs from one afternoon. No claim about the chip in general.
- ρ_ref inherits the corrected simulator's own gaps (P3-1 showed that it misses most of the Stage 1 departure). A family can partly win by repairing ρ_ref's errors of its own kind. The ideal-reference secondary shows how much the reference choice matters.

## 7. Stop rules

- No API, no QPU. If the simulator or the optimiser errors, nothing is rerun with changed settings before a DEVIATIONS row.

## 8. Ledger entry (filled now, completed after audit)

```json
{"id": "ng-p3-5", "program": "nature-graded", "direction": "P3-5",
 "title": "Coherent or incoherent, from the archived tomography", "source": "engine",
 "engine_odds": 0.42, "engine_odds_at": "2026-11-04T14:06:13-07:00",
 "human_odds": null, "human_odds_note": "not recorded: Sean chose to proceed (nature-graded D0); closed for human odds",
 "prereg_commit": "<this commit>", "budget_usd": 0, "qpu_s_budget": 0,
 "referee": "nature", "bet_type": "standard", "seed_source": "curby-rng", "beacon": null, "seed": null, "tiebreak": null,
 "premortem": "If this fails, the most likely reason is that the lost negativity comes mostly from depolarising-type decay, which the incoherent family's global depolarising term captures and local rotations plus one ZZ phase cannot.", "premortem_kind": "world",
 "verdict": "open", "date": "2026-11-04", "result": null, "audit": null, "diagnosis": null}
```

## 9. Checklist before the first call

- [x] Committed with its code and DEVIATIONS row only; no likelihood on the archived counts has been computed.
- [x] Engine odds on record (map, 14:06). Human odds: not recorded (D0).
- [x] Pass rule applicable by a stranger.
- [x] Pre-mortem: one sentence, checkable, with kind.
- [x] §2 records CURBY-Q round 28297 (stalled) and names CURBy-RNG; seed commit follows before the archive is opened.
- [x] No network or QPU path in the script.
- [x] DEVIATIONS.md D2.
