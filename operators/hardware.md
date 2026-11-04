# Quantum hardware: what it is for, sized honestly

Quantum hardware has two jobs in this testbed: **referee** and **seed source**. It is **never a computational resource**. The referee is our IBM chip (IBM Open Plan, 600 QPU s/month, project hard stop 420 s, 46 s used). The seed source is not our chip. It is NIST's Bell-test apparatus, reached through the CU Randomness Beacon (CURBy). This file is the whole policy. It follows CONTEXT.md §3 rule 7, ARCHITECTURE.md (the `Beacon` and `Tiebreak` objects, step 3 of the loop) and proposal.md.

## In plain English

Everything we can afford to run on the chip, a laptop can simulate exactly, faster and without noise. Our circuits use at most a few dozen qubits and a few hundred gates, inside 600 seconds a month. So the chip cannot make any of the engine's numbers better, and any claim that it did would be false. Program 1 spent its hardware budget showing exactly that: the entangled encoding tied a classical twin, and the learned version switched its own entanglement off.

What real quantum hardware *can* do for us is two narrower things.

1. **Settle an argument about the real world.** A simulator says what an ideal or modelled device would do. Only a real device says what this one does. When a claim rests on a simulated circuit and someone doubts that the simulation is enough, the chip decides. Before it does, the engine bets on whether the chip will agree with the simulator. That bet is scored, and over time it tells us when the chip was never needed.
2. **Choose our random splits for us.** If the session that runs a test also picks its random seed, it could, without meaning to, try seeds until the held-out set looks friendly. A seed taken from a public beacon *after* the pass rule is frozen cannot be shopped for, and anyone can check it later. When its quantum chain is running, CURBy's numbers come from a Bell test certified at NIST, so they are random in a sense a laptop's are not. **That chain has been stalled since 2025-08-22**, so for now our seeds come from CURBy's classical chain, which is public and timestamped but not certified. To be honest about it, the certification was always a bonus. What protects the test is that nobody in the loop chose the seed or could foresee it.

## Never a computational resource

The chip never computes a number that the engine, a program, or a paper uses as an estimate, feature, score or prediction. That rules out quantum feature maps, quantum kernels, "quantum-enhanced" anything, sampling used as a speed-up, and re-running classical-simulable circuits to look quantum. CONTEXT.md §3 rule 6 already forbids reviving program 1's quantum error-prediction encoding.

**Instrument experiments are separate and remain allowed.** In gold-map directions 7 (local friendliness) and 8 (sequential Peres–Mermin), the chip is the *object being measured*, a physical system whose behaviour is the result. Those are program-level experiments under rule 7, pre-registered and separately approved, with their own QPU budget. **Program 3 (`GitPhar/nature-graded`)** is the referee role at program scale. Each of its bets is a pre-registered prediction about the chip, and physics grades the engine's odds instead of a language model doing so. Its month plan (about 146 s in three waves, at least 120 s held for replication, `nature-graded/map/program-3-map.md`) is a program budget under rule 7, not the tiebreak cap below. Every QPU second, from either source, counts against the one 420 s hard stop. Whether hardware can serve the testbed beyond the two jobs above stays an open question, as Sean asked. This file closes only the "computational resource" reading.

## Job 1: the referee (bet type `tiebreak`)

**When to call it.** A result rests on a simulated circuit, and either of two things is true:
- the auditor, Sean or a reviewer disputes that the simulation is adequate, for example because the noise model omits crosstalk, leakage or drift;
- two simulators disagree, such as an ideal simulator and a noise model, or two noise models.

Never call it to make a result look stronger. It is called to decide.

**What is bet.** The event is always the same shape: *"Run on <backend>, the circuit's <pre-registered statistic> agrees with the <named simulator>'s prediction within <tolerance>."* Before any QPU second is spent:

1. The engine states P(agree) in the map, and Sean states his on the human-odds form, as for any bet.
2. A pre-registration (`operators/prereg-template.md`, bet type `tiebreak`) fixes the circuit (a file and its hash), the simulator and noise model (backend name and calibration snapshot date), the statistic and its tolerance, the number of shots, and the QPU budget.
3. The simulator's prediction is computed and committed *before* the chip runs, in the pre-registration or the commit right after it. A prediction written after the chip has run is worthless.

**Budget.** At most 60 QPU s per tiebreak and 120 s a month on tiebreaks, all inside the 420 s project hard stop. Each run records the backend's calibration data (T1, T2, readout and two-qubit error rates) at submission time.

**Scoring.** The outcome is 1 if the chip agrees within tolerance and 0 if not. Tiebreak bets enter the ledger like any bet. They are also reported separately in `ledger/scores.md` (agreement rate, Brier for each side, QPU s used), because the question they answer is different: does the engine know when the simulator is enough? A well-calibrated, high P(agree) is the result that saves QPU seconds. It says the next such dispute can be settled on the laptop.

**What a disagreement means.** If the chip disagrees, the *simulation* was inadequate for that circuit. It does not show a quantum advantage, and it does not make the chip's number the estimate the program uses. The program's claim is then restated, as a mechanism question, with the chip's result as evidence about the device.

## Job 2: the seed source (CURBy)

**The beacon.** CURBy (the CU Randomness Beacon) is run by the University of Colorado Boulder with NIST. It publishes 512-bit random strings whose randomness is certified by a loophole-free Bell test on entangled photons at NIST Boulder. Each pulse is hash-chained and timestamped with NIST's Twine protocol, so anyone can verify after the fact what was published and when. It runs two chains:
- **CURBY-Q**, the quantum, device-independent chain whose output is Bell-certified. **Use it when it is live.**
- **CURBy-RNG**, a classical chain in the style of the NIST Randomness Beacon that pulses every minute. It is timestamped and public but not quantum-certified. It is the fallback, and while CURBY-Q is stalled it is the seed source in practice.

**Status, 2026-11-04 14:56 America/Denver** (reported by the other-minds session on the first call of the client from this machine): CURBY-Q's latest completed round is 28297, with its result pulse at 2025-08-22 13:42 America/Denver. Round 28298 has sat at stage `request` since 2025-08-22 13:43 and never finished. CURBy-RNG is live, and its latest pulse was in the current minute.

The official client is `@buff-beacon-project/curby-client` (npm; version 1.2.0 when this file was written). `DIRNGClient` fetches and validates CURBY-Q rounds: chain and pulse signatures, and the causal ordering of the Bell-response and seed pulses. Full certificate verification uses the project's separate `curby_verify` tool. It was first called from this machine on 2026-11-04 by the other-minds session, which installed it in a scratch directory with `npm install --ignore-scripts`. The calls used were `DIRNGClient.latest()`, `DIRNGClient.fetchRound('pending')` and `Client.randomness()`. Each seed commit records the exact code and client version it used.

**Which draws use it.** Anything random that decides *what data a test sees*: train/test and held-out splits, item samples, the paraphrase and negation half in `operators/scout.md`, and the order of items or questions when order is randomised. Bootstrap resampling seeds may use it too, or a fixed constant stated in the pre-registration. The beacon is never used for anything that must stay secret, such as plant draws or seal salts: its output is public, so anyone could recompute the result (`operators/plant.md`).

**Protocol (two commits, both before any data):**

1. **Pre-registration commit.** First check CURBY-Q's latest *completed* round (`DIRNGClient.latest()`, a free public read that fixes nothing) and write its round number and result-pulse time into §2. Then choose the chain by rule:
   - **Live:** that round completed less than 24 hours before this commit. §2 says: *"Seed: the first CURBY-Q round whose pulse is timestamped after this commit."*
   - **Stalled:** that round is 24 hours old or more. §2 says: *"CURBY-Q stalled (latest completed round <n>, <time>). Seed: the first CURBy-RNG pulse timestamped after this commit."*

   Either way, §2 adds: *"seed = the first 8 bytes of SHA-256(randomness ‖ bet-id), read as an unsigned big-endian integer; sub-seeds per purpose as `ledger/seed.py` derives them."* The beacon block is left blank.
2. **Seed commit**, immediately after: fetch that round with the client, record the beacon block in the pre-registration (`chain`, `round` or pulse index, `pulse_time` in America/Denver, `randomness` as hex, `client` and its version, and `certificate_verified: true|false`), compute the seed with
   ```
   python3 /Users/seanpharris/oversight-testbed/ledger/seed.py <randomness-hex> <bet-id> [--purpose split]
   ```
   write it in, and commit with `Seed <bet-id>: <chain> <round or pulse index>`. On a stalled CURBY-Q, the seed commit can follow at once, because a CURBy-RNG pulse lands every minute. Nothing is drawn, fetched or opened between the two commits.

**Fallback for a live but slow chain.** If CURBY-Q was live at the pre-registration but no round completes within 6 hours of the commit, use the first **CURBy-RNG** pulse after that commit, and record `seed_source: curby-rng` (classical, not quantum-certified) and the reason. If both are down, wait. *(Amended 2026-11-04 15:05. The first version always waited 6 hours, which, with CURBY-Q stalled for over a year, delayed every bet by 6 hours and protected nothing. Bets pre-registered under the first version log a deviation, before any data, and take the first CURBy-RNG pulse after their pre-registration commit.)* A local random generator is never used for a split once a pre-registration names the beacon. A seed is never re-drawn.

**What the auditor checks** (`operators/auditor.md`, E23): the live/stalled choice follows from the CURBY-Q round recorded in §2 (the 24-hour rule); the pulse time is after the pre-registration commit's author time; it is the *first* such round or pulse on its chain (fetch the one before it and check that it predates the commit); the seed recomputes with `ledger/seed.py` and the recorded `purpose`; the split in the code uses that seed and no other. Any failure is a hole.

## Ledger fields: `ledger/bets.jsonl`

```json
"bet_type": "standard|tiebreak",
"seed_source": "curby-q|curby-rng|fixed|null",
"beacon": {"chain": "CURBY-Q", "round": 0, "pulse_time": "<YYYY-MM-DD HH:MM America/Denver>",
           "randomness": "<hex>", "purpose": "<the --purpose given to seed.py, or null>",
           "client": "@buff-beacon-project/curby-client@<version>",
           "certificate_verified": false, "seed_commit": "<sha>"},
"seed": 0,
"tiebreak": {"circuit": "<path>", "circuit_sha256": "<hex>", "simulator": "<name + noise model>",
             "statistic": "<name>", "sim_prediction": 0.0, "tolerance": 0.0, "shots": 0,
             "backend": "ibm_<name>", "calibration_snapshot": "<path>", "qpu_s_budget": 60,
             "qpu_s_used": null, "chip_result": null, "agree": null}
```

Standard bets have `tiebreak: null`. Shadow checks (`operators/veto.md`) are bet type `shadow` in their pre-registration and are recorded in `ledger/shadows.jsonl`, not here. Founding-week bets have `seed_source: null` with a `seed_note`, because their seeds were chosen by the session before this rule existed.

## Sizes, stated once

| | what it is | what it is not |
|---|---|---|
| IBM chip | a referee on whether a simulation describes this device; an apparatus for program-level foundations experiments (directions 7 and 8) | faster, better or "quantum-enhanced" computation of anything we use |
| CURBy CURBY-Q | a public, Bell-certified, timestamped seed that no one in the loop chose, when the chain is live (stalled since 2025-08-22) | a reason any split is statistically better than one from a good generator |
| CURBy-RNG | a public, timestamped seed that no one in the loop chose; the seed source in practice while CURBY-Q is stalled | quantum-certified |
| Budget | ≤ 60 QPU s per tiebreak, ≤ 120 s/month on tiebreaks, inside the 420 s hard stop; seeds cost $0 | a standing allowance to "try it on hardware" |
