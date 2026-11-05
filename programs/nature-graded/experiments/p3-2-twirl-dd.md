# P3-2. Coherent or stochastic? Twirling and DD on the Stage 1 circuit (pre-registration)

Frozen at this file's commit time (America/Denver; the commit's author time is authoritative), in its own commit, before any circuit is submitted. DEVIATIONS.md D3. Budget **$0 API · ≤ 12 QPU s (one job, shared with P3-3; estimate 7.6 s) · 1 laptop hour**. Hardware only through `entangled-mind/src/entangled_mind/backends.py::run_hardware`, which refuses at the 420 s hard stop. **One job, never resubmitted**: the script refuses if raw results already exist.

## 0. The bet

| field | value |
|---|---|
| bet id | `ng-p3-2` |
| referee | `nature` |
| bet type | `standard` (a program-level referee experiment under CONTEXT rule 7; operators/hardware.md, "Program 3") |
| direction | `P3-2` (map/program-3-map.json) |
| source | `literature` (cluster D) |
| engine odds, P(pass) | **0.25**, stated 2026-11-04T14:06:13-07:00 in map/program-3-map.json (template v1-batch). Not in the elicitation-check half. |
| human odds, P(pass) | **not recorded**: Sean chose to proceed without his odds (D0); closed for human odds. |
| budget | $0 API · ≤ 12 QPU s for the shared job · 1 laptop hour |
| pre-mortem | "If this fails, the most likely reason is that the Stage 1 departure is stochastic, not coherent, so twirling leaves P(yes) near the untwirled arm (P3-5 already leaned incoherent)." Kind: `world`. |
| approval | Sean, 2026-11-04 session instruction: "the first chip job … about 12 QPU seconds … Do not submit a second job this session." |
| auditor | fresh session per operators/auditor.md, after results |

## 1. In plain English

Program 1's circuit came back from the chip saying "yes" about twice as often as the chip's own description predicted. P3-1 showed this was not our simulator set-up. If the extra error is a *steering* error (each gate over-rotates the same way every time), it can build up through the 117 two-qubit gates and push the answer a long way. Twirling surrounds every gate with random flips that cancel on paper but turn steady steering errors into random ones. So if twirling pulls the chip's answer at least halfway back toward the simulator, steering errors were the cause. We also try dynamical decoupling, pulses that protect idle qubits, and both together. All arms run interleaved in one job, so slow drift during the job cannot favour one arm. The rival explanations are that the extra error was random from the start (twirling then changes little) or that the chip has drifted since program 1 (the "no gap today" outcome below).

## 2. Material

- **Circuit.** The archived Stage 1 ISA circuit (P3-1, §2; SHA-256 of the archive `a773bd6e…4029`), on its original physical qubits 136, 143, 123, 142, 144, 141, 124, 125, 117 (clbit order 117, 125, 124, 123, 144, 136, 143, 141, 142).
- **Arms** (one job, `experiments/p3_2_3_job.py`; each arm is 20 circuit instances × 100 shots = 2,000 shots; all 200 instances are put in a seeded random order):
  - **A**, as run: the archived circuit, unchanged.
  - **B**, gate + measurement twirl: each CZ gets independent uniform random Paulis on its two qubits before it, and their CZ-conjugates after it. Each instance also gets a random 9-bit mask: an X before each masked measurement, with the bit flipped back in analysis. One-qubit runs are then re-synthesised into the native basis by `Optimize1qGatesDecomposition`, so every run's unitary is kept exactly. Checked before this commit on a toy circuit: 20 twirls, unitary unchanged. Checked on FakeFez: ideal P(yes) of a twirled, unmasked instance equals arm A's within shot noise. This is the user-level equivalent of SamplerV2's `twirling.enable_gates` + `enable_measure`, built into the circuits because `run_hardware` passes no options and options would apply to the whole job.
  - **B2**, gate twirl only (exploratory; separates gate twirling from readout symmetrisation).
  - **C**, DD XY4: ALAP-scheduled with the live target's durations; `PadDynamicalDecoupling` with X, Y, X, Y in every idle window long enough on the 9 circuit qubits. Y is sent as rz(π) then x. Checked: the unitary is unchanged, and every instruction is native.
  - **D**, B + C.
  - **R0, R1**, readout calibration: all-0 and all-1 on the 9 original qubits.
  - **M**, mirror (exploratory): a random Pauli P on each qubit, then the circuit U, then U†. The ideal outcome is P's bit-flip pattern. *Changed from the map's "U · P · U†"* (D3): U is not Clifford, so that order has no basis-state outcome.
  - **L1, L2**, arm A on two alternative layouts: P3-3's arms, pre-registered there.
- **Corrected-simulator prediction S** (the P3-1 construction on today's device): `NoiseModel.from_backend` of the **live** `ibm_fez` target at prediction time, with the circuit ALAP-scheduled with the live durations; 100,000 shots; seed `order`. S is computed, with the layouts, after both seed commits, and committed in a **prediction commit** (`data/p3-2-3-predictions.json`, plus every submitted circuit in `data/p3-2-3-circuits.qpy` with its SHA-256) before submission. The submit step refuses unless that file is committed, unchanged, and the circuit hash matches.
- **Calibration record:** the live T1, T2, readout, sx and CZ errors of every used qubit and pair, read at prediction time (in the prediction file), and at execution time (read afterwards with `backend.properties(datetime=<execution start>)`, as program 1 did).
- **Seed** (operators/hardware.md): CURBY-Q latest completed round **28297, result pulse 2025-08-22 13:42 America/Denver** (checked 2026-11-04 15:30, before this commit), so it is **stalled**. **Seed: the first CURBy-RNG pulse timestamped after this commit.** Sub-seeds by `ledger/seed.py --purpose`: `twirl` (Paulis and masks), `mirror` (mirror Paulis), `order` (the circuit order; also Aer's seed for S). The `seed32` of each is used. *Filled in by the seed commit, before anything is built or fetched:*
  `chain:` CURBy-RNG · `pulse index:` 1591393 · `pulse_time:` 2026-11-04 15:49:00 America/Denver · `previous pulse:` index 1591392 at 2026-11-04 15:48:00 (before the commit at 2026-11-04 15:48:03) · `randomness:` 5645e598ad28dce78f2f2643252e1a40c0b57308f888d4e4fb9602060aed0b69d06979c1b2f4cc04a61f4aa652a2cc572b030bed49df01010da57daa699f187f · `client:` @buff-beacon-project/curby-client@1.2.0 via `experiments/curby_seed.mjs` · `certificate_verified:` false · `seed (twirl):` 4299773254748777713 · `seed32 (twirl):` 2013703409 · `seed (mirror):` 5741302615905360373 · `seed32 (mirror):` 2031049205 · `seed (order):` 16074001768053448200 · `seed32 (order):` 3218316808. Record: `data/p3-2-seed.json`.

## 3. Calls

| step | what | calls | est. cost |
|---|---|---|---|
| 1 | seed commit (this bet), then P3-3's pre-registration and seed commit | CURBy | $0 |
| 2 | `--predict`: read the live target and properties (IBM API, 0 QPU s); choose layouts (P3-3 rule); build 200 circuits; simulate S, S_L1, S_L2 | 1 IBM read | laptop |
| 3 | prediction commit | — | — |
| 4 | `--submit`: refuses if the estimate exceeds 12 s, or if cumulative + 1.5 × estimate > 300 s (the map's reserve rule); then **one** `run_hardware` call (SamplerV2, one Batch, 200 circuits × 100 shots) | 1 job | est. 0.28 ms × 20,000 + 2 s = **7.6 s** |
| 5 | `--analyse` from saved raw counts | 0 | laptop |

## 4. Statistics

- **P(yes)** per arm: `readout.quantum_readout` on the arm's pooled counts (masked bits flipped back first). Raw counts; no readout mitigation in the primary.
- **SE** per arm: the standard deviation of the 20 instance-level P(yes) values ÷ √20. This captures shot noise, twirl randomness and drift between instances.
- **Primary statistic:** the movement of arm B toward S, relative to arm A: m_B = sign(P_A − S) · (P_A − P_B), with z_B = m_B / √(SE_A² + SE_B²).
- **Secondary, reported, not scored:** m and z for B2, C and D; per-qubit marginals for every arm; readout matrices from R0/R1; mirror success (P(all bits correct)); P_A against program 1's 0.502 (drift since Nov 3); the calibration at prediction and execution time; billed QPU seconds against the estimate (the map's re-costing rule).
- **Multiple comparisons:** one scored test. The secondaries are labelled exploratory.

## 5. Pre-registered reading

1. **Untestable (no gap to close):** |P_A − S| < 0.125. Today's device then agrees with its description too well for "halfway back" to mean anything. This is reported as a finding about drift since program 1.
2. **Pass:** |P_A − S| ≥ 0.125, m_B ≥ 0.125 and z_B ≥ 3.
3. **Fail:** |P_A − S| ≥ 0.125 and not a pass.
4. **Job failure:** if the job errors or returns fewer than 90% of its shots, every bet in it is untestable. It is **not** resubmitted this session.
5. **Reported in every case:** every arm's P(yes) ± SE, S, the gap, the four movements, the billed seconds.

**Rule for waves 2–3, fixed now** (the map's gating rule, written before wave 1 runs):
- **Gate + measurement twirling is the default** for waves 2–3 if P3-2 passes, or if |P_B − P_A| ≥ 0.05 at z ≥ 3 in either direction. Otherwise the default is no twirling. P3-7's mandatory measurement twirling is unaffected.
- **DD XY4 is the default** if m_C ≥ 0.05 at z ≥ 3. Otherwise it is off. P3-4, when it runs, can switch DD on by its own pre-registered rule; it cannot switch it off.
- If a default is on, every later noisy-sim prediction is rebuilt to match before that bet's pre-registration (the map's rule).

A pass is reported as **pass, unreplicated** (invariant 7).

## 6. What it cannot do

- Twirling turns coherent error into stochastic error, but it also changes the circuit's one-qubit gate counts slightly. Arm B2 against B separates the readout part. Nothing here separates "coherent" from "anything twirling happens to fix".
- One circuit, one afternoon. "Every" and "all" will not appear.
- DD here is the circuit-level XY4 placed by qiskit, not IBM's server-side implementation. The two may differ in placement.
- S uses the live calibration at prediction time. The job may run hours later. The execution-time calibration is reported, but S is not recomputed for scoring.

## 7. Stop rules

- `run_hardware` refuses at 420 s cumulative. `--submit` refuses above a 12 s estimate, under the reserve rule, without a committed prediction file, or if the job already ran.
- One job only. If it fails, no second job this session (Sean's instruction).
- The two P3-3 repeats (≥ 3 h apart) are not run this session (D0).

## 8. Ledger entry (filled now, completed after audit)

```json
{"id": "ng-p3-2", "program": "nature-graded", "direction": "P3-2",
 "title": "Coherent or stochastic? Twirling and DD on the Stage 1 circuit", "source": "literature",
 "engine_odds": 0.25, "engine_odds_at": "2026-11-04T14:06:13-07:00",
 "human_odds": null, "human_odds_note": "not recorded: Sean chose to proceed (nature-graded D0); closed for human odds",
 "prereg_commit": "<this commit>", "budget_usd": 0, "qpu_s_budget": 12,
 "referee": "nature", "bet_type": "standard", "seed_source": "curby-rng", "beacon": null, "seed": null, "tiebreak": null,
 "premortem": "If this fails, the most likely reason is that the Stage 1 departure is stochastic, not coherent, so twirling leaves P(yes) near the untwirled arm (P3-5 already leaned incoherent).", "premortem_kind": "world",
 "verdict": "open", "date": "2026-11-04", "result": null, "audit": null, "diagnosis": null}
```

## 9. Checklist before the first call

- [x] Committed with its code and DEVIATIONS row only. Nothing has been fetched from IBM or submitted.
- [x] Engine odds on record (map, 14:06). Human odds: not recorded (D0).
- [x] Pass rule applicable by a stranger.
- [x] Pre-mortem: one sentence, checkable, with kind.
- [x] §2 records CURBY-Q round 28297 (stalled) and names CURBy-RNG; seed commit follows.
- [x] QPU budget and hard stop enforced in code (`run_hardware`; `--submit` checks).
- [x] DEVIATIONS.md D3.
