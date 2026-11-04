# P3-1. Does a correctly scheduled noise model close the Stage 1 gap? (pre-registration)

Frozen at this file's commit time (America/Denver; the commit's author time is authoritative), in its own commit, before the simulation runs. DEVIATIONS.md D1. Budget **$0 API · 0 QPU s · < 1 laptop hour**. No model API is called.

## 0. The bet

| field | value |
|---|---|
| bet id | `ng-p3-1` |
| referee | `nature` (the event compares a simulator with what the chip did in program 1; the chip's archived outcome is the reference) |
| bet type | `standard` |
| direction | `P3-1` (map/program-3-map.json; oversight-testbed map/nature-graded.json) |
| source | `literature` (cluster D, Aer `from_backend` source) + program 1 result |
| engine odds, P(pass) | **0.07**, stated 2026-11-04T14:06:13-07:00 in map/program-3-map.json (template v1-batch). Elicitation check: paraphrase 0.12, negation (not pass) 0.85, incoherence 0.08. |
| human odds, P(pass) | **not recorded**: `map/human-odds.md` was blank at pre-registration, and Sean chose to proceed without his odds (2026-11-04, D0). Under the rule set the same day, this question is closed for human odds. |
| budget | $0 API · 0 QPU s · < 1 laptop hour |
| pre-mortem | "If this fails, the most likely reason is that idle relaxation over a roughly 10–20 µs circuit, against T1 ≈ 90–200 µs, is far too small to move P(yes) from 0.25 to 0.40." Kind: `world`. |
| auditor | fresh session per operators/auditor.md, after results |

## 1. In plain English

In program 1, IBM's own description of the chip predicted the circuit would answer "yes" 25% of the time. The chip said "yes" 50% of the time. One innocent explanation is a mistake in how we built the simulator: it only lets a waiting qubit decay if the circuit has been laid out in time first, and ours was not. We lay the same archived circuit out in time, step by step, as the chip runs it, load the chip's error rates from that afternoon, and simulate again. If the corrected simulator says 0.40 or more, most of the surprise was our set-up. If it still says about 0.25, the gap belongs to the chip, not to our simulator. The rival explanation, which this test cannot confirm but can leave standing, is that the chip's real errors are larger or of a different kind than its calibration reports.

## 2. Material

- **Circuit.** The as-run ISA circuit of Stage 1 job `dbl423dgg49c73dk0db0`, rebuilt gate for gate from `entangled-mind/window/data/hardware/dbl423dgg49c73dk0db0-0.json` (SHA-256 `a773bd6eae282e644f3ff62dc89cbfe3c3a758855872116f26b905458c8d4029`) by `experiments/p3sim.py::load_isa`. A structure-only check before this commit: 219 sx, 153 rz, 117 CZ, 5 x, 9 measure, depth 208, active qubits 117, 123, 124, 125, 136, 141, 142, 143, 144, all matching the archive. Disclosed: the archive's gate list omits the one pre-measurement barrier the original circuit had (its gate counts list it). ALAP scheduling aligns the final measurements without it. No simulation was run on it before this commit.
- **Device description.** `FakeFez` from qiskit-ibm-runtime 0.51.0 (offline snapshot, 2025-02-26), durations CZ 84 ns, sx/x 24 ns, measure 1.56 µs. On the 9 used qubits and 8 used CZ pairs, T1, T2, readout error, sx and x error, and CZ error are overwritten with the job-time snapshot in `entangled-mind/results/ibm-calibration.json` (SHA-256 `b47b92a5…9e65`; snapshot 2026-11-03 15:31:18-07:00), by `p3sim.overwrite_calibration`. Readout error is symmetric, from the snapshot's single `readout_error`, as `from_backend` builds it from a target. x error is set equal to sx error, since the snapshot has no separate x error.
- **Noise model.** `NoiseModel.from_backend(backend, thermal_relaxation=True)` (qiskit-aer 0.18.2): depolarising plus thermal relaxation per gate, relaxation on explicit `Delay`s, temperature 0. Simulated with `AerSimulator(method="density_matrix")`.
- **Scheduling.** `ALAPScheduleAnalysis` + `PadDelay` with the target's durations (qiskit 2.6.1). Delays on qubits the circuit never touches are dropped. A toy check before this commit (X, a 9.6 µs idle, measure; not the archived circuit) gave the expected 18% decay with scheduling and none without.
- **Readout statistic.** P(yes) by `entangled_mind.readout.quantum_readout` with the q01 web from `entangled-mind/results/pool-run-1.json`, exactly as Stage 1 computed it.
- **Archives read.** The circuit file above (gates, layout), the calibration snapshot above (job `dbl423dgg49c73dk0db0` entry), `stage1-run-1.json` (`arms.*.counts`, `arms.*.readout.p_yes`) for the comparison rows and per-qubit marginals. The hardware and noisy-sim P(yes) (0.502, 0.251) are already published in `stage1-run-1.md`. The scout already saw the hardware per-qubit marginals (map disclosure).
- **Seed** (operators/hardware.md): CURBY-Q latest completed round **28297, result pulse 2025-08-22 13:42 America/Denver** (checked 2026-11-04 15:30 with `experiments/curby_seed.mjs check`, before this commit). That is more than 24 hours old, so CURBY-Q is **stalled**. **Seed: the first CURBy-RNG pulse timestamped after this commit.** seed = the first 8 bytes of SHA-256(randomness ‖ `ng-p3-1`) by `ledger/seed.py --purpose sim`. Its `seed32` is Aer's `seed_simulator` for every run below. Nothing else is random. *Filled in by the seed commit, before any simulation:*
  `chain:` ___ · `pulse index:` ___ · `pulse_time:` ___ · `randomness:` ___ · `client:` ___ · `certificate_verified:` ___ · `seed (sim):` ___ · `seed32 (sim):` ___

## 3. Calls

| step | what | calls | est. cost |
|---|---|---|---|
| 1 | control: the P3-1 model, **unscheduled**, 100,000 shots | 0 API, 0 QPU | laptop |
| 2 | primary: the P3-1 model, **ALAP-scheduled**, 100,000 shots | 0 API, 0 QPU | laptop |
| 3 | exploratory: scheduled + ZZ phase 0.1 rad after every CZ (E2); scheduled with every error ×3 and T1, T2 ÷3 (E3); 20,000 shots each | 0 | laptop |

`experiments/p3_1_scheduled.py` runs all three and refuses to start until `data/p3-1-seed.json` exists. E1 (temperature > 0), on the map's list, is **not run**: FakeFez carries no qubit frequencies, which Aer's temperature option needs. Steps 1 and 2 alone decide the verdict.

## 4. Statistics

- **Primary statistic:** P(yes) of the scheduled run, 100,000 shots (binomial SE ≈ 0.0015).
- **Control:** P(yes) of the unscheduled run must lie within 0.251 ± 0.03, the archived Stage 1 noisy-sim value. This shows the reconstruction (FakeFez plus the overwritten snapshot) reproduces program 1's simulator.
- **Secondary, reported, not scored:** per-qubit P(1) for ideal, archived noisy sim, control, scheduled, E2, E3 and hardware; the scheduled circuit's duration; the number of delays inserted; E2 and E3 P(yes).
- **Multiple comparisons:** one scored test; none applied.
- **This model becomes "the P3-1-corrected simulator"** for every later program-3 noisy-sim prediction, whatever the verdict. It is the right construction (idle decay included), whether or not it closes the gap. A pass does not change that; a fail does not either.

## 5. Pre-registered reading

1. **Pass:** the control lies in [0.221, 0.281] and the scheduled P(yes) ≥ 0.40.
2. **Fail:** the control lies in [0.221, 0.281] and the scheduled P(yes) < 0.40.
3. **Untestable:** the control lies outside [0.221, 0.281]. The reconstruction does not reproduce program 1's simulator, so the comparison says nothing. Reported as untestable, not as a pass or a fail.
4. **Reported in every case:** control and scheduled P(yes) with SEs, the gap closed as a fraction, (scheduled − 0.251) / (0.502 − 0.251), the per-qubit table, E2 and E3.

## 6. What it cannot do

- It tests one omission (idle decay) in one simulator on one circuit. A fail does not show the chip's calibration is wrong in any particular way. It shows that this omission is not the explanation.
- FakeFez's durations are an offline snapshot. The real job's schedule was set by IBM's compiler, which may differ in alignment or measurement timing. Disclosed, not corrected.
- The job-time snapshot is a single calibration reading (Carroll et al. 2022: one T1 reading is a weak estimate). The rival explanation of drift between calibration and job stays open and is P3-3's subject.

## 7. Stop rules

- No API, no QPU. The script cannot reach the network.
- If the simulator raises an error, nothing is rerun with changed settings before a DEVIATIONS row is written.

## 8. Ledger entry (filled now, completed after audit)

```json
{"id": "ng-p3-1", "program": "nature-graded", "direction": "P3-1",
 "title": "Does a correctly scheduled noise model close the Stage 1 gap?", "source": "literature",
 "engine_odds": 0.07, "engine_odds_at": "2026-11-04T14:06:13-07:00",
 "human_odds": null, "human_odds_note": "not recorded: map/human-odds.md blank at pre-registration; Sean chose to proceed (nature-graded D0); closed for human odds",
 "prereg_commit": "<this commit>", "budget_usd": 0, "qpu_s_budget": 0,
 "referee": "nature", "bet_type": "standard", "seed_source": "curby-rng", "beacon": null, "seed": null, "tiebreak": null,
 "premortem": "If this fails, the most likely reason is that idle relaxation over a roughly 10–20 µs circuit, against T1 ≈ 90–200 µs, is far too small to move P(yes) from 0.25 to 0.40.", "premortem_kind": "world",
 "verdict": "open", "date": "2026-11-04", "result": null, "audit": null, "diagnosis": null}
```

## 9. Checklist before the first call

- [x] This file is committed with its code and its DEVIATIONS row only; nothing has been run.
- [x] Engine odds are on record (map, 14:06). Human odds: not recorded, by Sean's choice (D0).
- [x] The pass rule in §5 can be applied by a stranger.
- [x] The pre-mortem in §0 is one sentence, names a checkable mechanism, and carries its kind.
- [x] §2 records CURBY-Q's latest completed round and names CURBy-RNG by the 24-hour rule; the seed commit follows before any simulation.
- [x] Budget enforced in code: the script has no network or QPU path.
- [x] DEVIATIONS.md row D1.
