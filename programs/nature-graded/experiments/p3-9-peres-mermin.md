# P3-9: does program 1's contextuality check see contextuality on the chip, where physics says it must be there? Sequential Peres–Mermin under the exact CbD 2.0 linear program (pre-registration)

Written and frozen 2026-11-05 (America/Denver; the commit's author time is the record), in its own commit, before any chip submission for this bet. DEVIATIONS.md D48. Budget **≤ 45 QPU s** (estimate 28.9 s nominal; 43.3 s with ×1.5 contingency for dynamic circuits), $0 API, enforced in code; approval is the engine's `budget_ruling` row in `ledger/spend.jsonl` under st-16, after the design review. Stop rules in §7.

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). This session never asks Sean for odds or for a decision, in a terminal, a chat or a question dialog. His odds come only from `ledger/human-odds.jsonl` (the cockpit's downloads, committed); if a direction has no line there when its bet is pre-registered, the bet proceeds marked "no human odds". A decision this session would otherwise ask about, it makes under the written rules and states in its report and commit, where Sean can veto it from the cockpit. Sean's judgment is recorded and scored as steers in `ledger/steers.jsonl`: seed questions, vetoes, added questions and architecture decisions.

> **The chip is a referee and the object measured here, never a computational resource** (`operators/hardware.md`, "Instrument experiments"). Every circuit is three qubits and is simulated exactly on a laptop (§2). The chip's counts decide a pre-registered bet about this device; they are never used as an estimate, feature or prediction anywhere else. Sean's decision (steer st-24; handoff 2026-11-05 §2.3): this is the chip's one foundations experiment (the cap of steer st-19, "at most one"); P3-10 is not run.

> **Cockpit first, then this file.** P3-9's card was committed on its own (`7996d98`) before this file. Sean's line for P3-9 was already in `ledger/human-odds.jsonl` (`ho-20261105-051140-7pv`, saved 05:11:40, from the 12-card cockpit). `python3 ledger/pickup_human_odds.py` ran at the drafting session's start and again in the session that finished this file (after merging main, `2031f33`), and found nothing new both times. `ledger/human-odds.jsonl` was read again immediately before this commit (`python3 ledger/human_odds_match.py nature-graded P3-9`).

## 0. The bet

| field | value |
|---|---|
| bet id | `ng-p3-9` |
| referee | `nature` (the chip's counts decide it) |
| bet type | `standard` (a foundations instrument check, not a simulator-vs-chip tiebreak; the simulator's prediction is committed and reported beside the result) |
| direction | `P3-9` (`programs/nature-graded/map/program-3-map.json`; gold map direction 8) |
| source | `literature` (reads cluster B: Kirchmair 2009, Kumar 2025, Kelleher & Holweck 2025, Massé 2021; plus program 1's CbD check) |
| prior work | **On every platform tried, Peres–Mermin exceeds its noncontextual bound of 4 in χ.** Two trapped ions with each observable read out sequentially: 5.46(4) (Kirchmair et al. 2009, Nature 460:494, arXiv:0904.1655). Google Willow (superconducting) with mid-circuit measurement and reset: 5.618 ± 0.005 (Kumar et al. 2025, arXiv:2512.02284; no CbD, marginal or signalling analysis). IBM Heron r2 ibm_kingston, product-only readout: 5.31, no error bars (Kelleher & Holweck 2025, arXiv:2505.21243). 2019-era 5-qubit IBM devices: about 4.99 (Laghaout et al. 2022, Eur. J. Phys. 43:055401, arXiv:2009.10751). **CbD:** the only CbD treatment of PM hardware data, Massé 2021 (arXiv:2105.13821, unrefereed; an adapted, not exact, formula), leaves Kirchmair's data contextual by 0.566; the exact CbD 2.0 LP gives CNT2 ≥ 0.141 on the same published numbers under every completion (`map/reads/p3-9-desk-work-2026-11-05.md`, `8b95dbd`). **Prior work predicts a pass for both input states.** No exact CbD LP has been applied to PM data from superconducting hardware, and no CbD analysis of sequential superconducting PM data was found (three searches, 2026-11-05, in the desk-work note, the third in another field's words: "state-independent contextuality … sequential QND … signalling disturbance correction"). **What this bet adds:** the exact CbD 2.0 LP with a CNT2 bootstrap on sequential mid-circuit-measurement data from an IBM Heron r2 (ibm_fez), in both measurement orders and for two input states; program 1's check pointed where physics fixes the answer. It is an instrument check, not a new physics claim. The engine's odds (80) sit near what the prior work predicts; the 20 points left for a fail price the device's mid-circuit measurement and reset errors, which no published IBM PM test exposed to CbD. |
| engine odds, P(pass) | **80** (rule 14, template v2: prior 0.32 + adjustment +0.48; reason "Low nature-graded/nature/literature rows (0.20, 0.13) are novel-claim bets; here QM, every published PM platform, and the simulator margin (CNT2 0.22, holds to ε=0.03) all predict pass."; fresh context, prior.md at `73eb5cf`; recorded `8bf9942`, `map/odds-elicitation/v2-p3-9.md`). First stated on the map: 40 (template v1-batch, 2026-11-04 14:06, a different draft event). Both kept. |
| human odds, P(pass) | **90**, `ho-20261105-051140-7pv` (cockpit, saved 2026-11-05 05:11:40). His card's event: "For both input states (|00⟩ and a Bell state), the exact CbD linear program rejects noncontextuality, with CNT2's bootstrap 99% lower bound above 0." This file's scored event is the same with "in both measurement orders" added (§5, D48): a tightening, so a pass here implies his card's event (CbD 2.0 Theorem 3). His card's event is reported as a secondary. |
| models | not all three, because no model is in the loop: the chip is the referee and the object measured (rule 12 does not apply). |
| budget | 0 $ API · ≤ 45 QPU s (estimate 0.28 ms × 96,000 shots + 2 s = 28.9 s; ×1.5 = 43.3 s) · about 1 laptop hour |
| lesson | Correcting P6, P12: program 1's CbD check never showed it could say 'contextual' or refuse a fake, and a bet physics decides buys calibration, not information. This bet checks the LP on Kirchmair's data and a χ-6 cheat, runs passing and failing worlds, and its odds are 80% (from 40% on the map) because physics and four platforms predict pass. |
| design review | before any submission, a fresh subagent dry-runs this design (`operators/design-review.md`, checks D1–D12) → `ledger/design-reviews/ng-p3-9.md`; it must say go, and it checks the budget against the hard stop. `--submit` refuses without go (or a confirmed fix-first). |
| pre-mortem | If this fails, the most likely reason is that ancilla 4's mid-circuit readouts and resets disturb the data qubits enough, growing with each later measurement, that CNT2 reaches 0 in at least one of the four systems. Kind: `design`. |
| auditor | fresh session per `operators/auditor.md`, after results, with a sealed plant draw first (`operators/plant.md`) |

**Read before betting (operators/learn.md).** `ledger/bets.jsonl`, `ledger/brier.md`, `ledger/audits/` and `ledger/lessons.jsonl` at `73eb5cf`, and `ledger/prior.md` (regenerated by `python3 ledger/prior.py`; unchanged). The record: 37 scored bets, 12 hits, Brier 0.188, running base rate 0.32. Nature-graded is 1 hit in 5 scored (ng-p3-18's pass). The newest audit file by commit is `ledger/audits/ng-p3-18.md` (`4f07a2f`, reveal note `3a7f38f`). Patterns read: P1–P17. Program 1's CbD record: experiment 5, rank-2 Γ on 80 claim–question pairs, 1 with Γ > 0 (`programs/entangled-mind/results/exp5-run-1.md`). This file was finished after merging main into the branch (`2031f33`). There, `ledger/prior.md` reads 0.25, not 0.32, because rule 15 now counts one scored bet per run. The engine's odds were elicited at `73eb5cf` and recorded at `8bf9942`, before this file. They are copied here, not re-elicited (rule 14: odds are copied from where they were first written).

## 1. In plain English

Program 1 asked whether a language model's answer to one question depends on what else was asked alongside it. The check it used is called Contextuality-by-Default (CbD), and it found nothing beyond chance. A check that never finds anything could be a check that cannot find anything. So this test points the same kind of check at a textbook quantum experiment, the Peres–Mermin square, where quantum theory says the effect must be there whatever state the qubits start in.

On the chip, two qubits are measured three observables at a time, one after another, through a third "ancilla" qubit, in six different groupings and in both orders, for two starting states. Then CbD's exact linear program asks whether any non-quantum (noncontextual) explanation fits the counts, once each measurement's own disturbance of the next is allowed for.

Physics and every published experiment predict that it finds the effect. What could stop it is the chip's own noise: mid-circuit readouts and resets that disturb the qubits enough for CbD to explain the result away. If that happens, the verdict says the chip's noise spoiled the check, never that quantum theory failed.

## 2. Material

- **Backend:** `ibm_fez` (IBM Open Plan, Heron r2), one SamplerV2 job inside a Batch via `entangled_mind.backends.run_hardware` (its 420 s hard stop is refused in code). No twirling, no dynamical decoupling (P3-2's default rule; SamplerV2's defaults, no options passed).
- **Qubits:** physical triple **(3, 4, 5)**: data qubit "1" = 3, ancilla = 4, data qubit "2" = 5. Chosen before this commit by the rule in `p3_9_pm.candidates` from IBM's properties read free at 2026-11-05 10:09 (`--select`, `data/p3-9-prepared.json`, committed `b1a06a5`).
  - The rule considers every triple whose ancilla is CZ-coupled to both data qubits (data qubits in index order).
  - Eligible: every error reported, ancilla readout ≤ 5%, both CZ errors ≤ 2%, T1 and T2 ≥ 50 µs on all three.
  - Score = 3 × ancilla readout error + 2.5 × (CZ(d1, a) + CZ(a, d2)); lowest wins, ties by (a, d1, d2).
  - 94 triples were eligible. The winner scored 0.0198: ancilla readout 0.24%, CZ 0.17% and 0.33%, T1/T2 200/215, 216/148, 213/182 µs. The runner-up was (129, 130, 131) at 0.0212.
  - If the triple is not runnable at submission, the bet is untestable (§5.3); it is never re-chosen.
- **Observables:** the square of Kirchmair et al. 2009: rows R1 = (Z1, Z2, Z1Z2), R2 = (X2, X1, X1X2), R3 = (Z1X2, X1Z2, Y1Y2); columns C1 = (Z1, X2, Z1X2), C2 = (Z2, X1, X1Z2), C3 = (Z1Z2, X1X2, Y1Y2). Each line's quantum product is +I except C3 (−I). χ = ⟨R1⟩ + ⟨R2⟩ + ⟨R3⟩ + ⟨C1⟩ + ⟨C2⟩ − ⟨C3⟩. The noncontextual bound is 4; quantum theory gives 6 for every state.
- **The measurement block** (`p3_9_pm.logical`), identical for an observable in every context.
  - Rotate each data qubit the Pauli touches so it becomes Z: X → H; Y → S†, then H.
  - CNOT each touched data qubit onto the ancilla; rotate back (X → H; Y → H, then S).
  - Measure the ancilla mid-circuit into classical bit j (the j-th observable measured; bit 1 = eigenvalue −1), then reset the ancilla.
  - A barrier separates blocks, so no gate crosses from one block to the next.
  - One classical register `meas`, three bits; all three outcomes of every context are recorded per shot.
- **Input states:** |00⟩ (nothing applied); the Bell state (|00⟩ + |11⟩)/√2, prepared through the ancilla: H(d1); CX(d1, a); CX(a, d2); CX(d1, a), which returns the ancilla to |0⟩.
- **Circuits:** 6 lines × 2 orders (forward = the line's order; reverse = last to first) × 2 states = **24 circuits**.
  - Mapped onto (3, 4, 5) and translated to ibm_fez's basis at optimisation level 0, so no gate is merged or moved.
  - Stored as `data/p3-9-circuits.qpy`, SHA-256 `51f1fe692ccacaf9…` (the full hash is in `data/p3-9-prepared.json`). `--submit` refuses on any mismatch.
  - Gate counts per circuit: 4–9 CZ, 3 mid-circuit measurements, 3 resets.
  - Circuit order within the job: a permutation drawn from the beacon seed's `order` purpose (`p3_9_pm.job_order`); counts are put back in canonical order before analysis.
- **Shots:** 4,000 per circuit, **96,000** in all.
- **Seed** (operators/hardware.md): CURBY-Q latest completed round **28297**, result pulse 2025-08-22 13:42:38 America/Denver. It was checked with `experiments/curby_seed.mjs check` (client 1.2.0) twice before this commit: by the drafting session, and again at `checked_at_utc` 2026-11-05T23:18:25Z (16:18 America/Denver), with the same round. That is more than 24 h old (stalled), so the seed is **the first CURBy-RNG pulse timestamped after this commit**. seed = the first 8 bytes of SHA-256(randomness ‖ bet-id), read as an unsigned big-endian integer; sub-seeds per purpose as `ledger/seed.py` derives them, purposes `order` (circuit order in the job) and `boot` (bootstrap). *Filled in by the seed commit, before any data:*
  `chain:` CURBy-RNG · `pulse index:` 1592865 · `pulse_time:` 2026-11-05 16:21:00 America/Denver · `previous pulse:` index 1592864 at 2026-11-05 16:20:00 (before the commit at 2026-11-05 16:20:14, `96cccf4`) · `randomness:` 78430e9b52c177dc3a355ea0d7edaacad9d857a55b8e9c668141c05a8ab15d9a70cbcf9ecb5668cbfeed3b70f8ac539d721988f7f295b77aaa93586d1b596f21 · `client:` @buff-beacon-project/curby-client@1.2.0 via `experiments/curby_seed.mjs` · `certificate_verified:` false · `seed (order):` 17761473774835708074 · `seed32 (order):` 1015001258 · `seed (boot):` 13690150415164649744 · `seed32 (boot):` 3784192272. Record: `data/p3-9-seed.json` (written by `experiments/seed_commit.py ng-p3-9 96cccf4 order boot`).
- **Simulator prediction** (committed `b1a06a5`, before this file and before any submission; `data/p3-9-prepared.json`, 200,000 simulated shots per circuit):

  | system (state, order) | ideal (density-matrix, no noise): χ / CNT2 / Δ0 | noisy (`AerSimulator.from_backend(live ibm_fez)`): χ / CNT2 / Δ0 |
  |---|---|---|
  | \|00⟩, forward | 6.000 / 0.250 / 0.003 | 5.787 / 0.227 / 0.013 |
  | \|00⟩, reverse | 6.000 / 0.248 / 0.007 | 5.785 / 0.227 / 0.024 |
  | Bell, forward | 6.000 / 0.250 / 0.003 | 5.718 / 0.226 / 0.006 |
  | Bell, reverse | 6.000 / 0.248 / 0.007 | 5.721 / 0.220 / 0.029 |

  (The ideal Δ0 is sampling noise at 200,000 shots; its true value is 0.) The noisy model holds IBM's reported gate, readout and T1/T2 errors on the qubits each instruction acts on. It has **no model of mid-circuit-measurement crosstalk, of reset error beyond the ancilla's readout, or of the data qubits' decay while they sit idle**. The ISA circuits carry no delays, so Aer adds no noise to an idle qubit.
  - The idle time: each block's ancilla measure plus reset takes 1.560 + 1.584 = 3.14 µs (`FakeFez` target durations), so the data qubits idle about 6.3 µs before the third measurement.
  - At the triple's T2 of 182–215 µs (prepared snapshot), that costs at most about 3.4% of an observable's contrast (1 − exp(−6.3/182)). That is a flip rate of at most about 1.7%, inside the flip0.03 world below (3%, 6%, 9%), which passes 19 of 20.
  - So the omitted decay alone does not move the predicted verdict. The crosstalk and reset errors IBM does not report are the gap the chip referees (the pre-mortem). Reported beside the result: the measured χ and CNT2 against these predictions.
- **Analysis code:** `experiments/cbd_lp.py` (the exact CbD 2.0 LP and CNT2; desk work `8b95dbd`) and `experiments/p3_9_pm.py` (`2bc6c32` and this commit). `--check` (offline) passes:
  - the LP equals the KDL 2015 criterion on 180 random cyclic systems;
  - Kirchmair's published numbers give minimum CNT2 0.141;
  - the χ = 6 "cheat" gives CNT2 0 in all four systems, and so do 30 noncontextual models with context- and position-dependent flips of up to 10%;
  - the ideal simulation of the 24 logical circuits gives χ 6.000 and CNT2 0.250;
  - the full 2¹⁸ LP equals the reduced LP;
  - the rule gives one verdict on all 81 label combinations.
- **Encoding for CNT2:** variable = 1 iff the eigenvalue −1 was recorded. The pass decision (CNT2 > 0) does not depend on this choice; CNT2's size does.

## 3. Calls

| step | what | QPU s | cost |
|---|---|---|---|
| select (done, `b1a06a5`) | free reads of IBM properties and target; qubit rule; circuits; simulator prediction | 0 | $0 |
| worlds (done, before this commit) | P(pass) under five named worlds from the committed prediction (§4) | 0 | $0 |
| submit | one job, 24 PUBs × 4,000 shots; calibration snapshot of the triple at submission and at run time (free reads); raw counts written to `data/p3-9-raw.json` the moment `run_hardware` returns | ≤ 45 (estimate 28.9) | $0 |
| analyse | CNT2 per system, bootstrap, verdict sentences → `results/p3-9-peres-mermin.json` | 0 | $0 |

The one job is the whole bet; there is no second job. A crash after submission never resubmits: `data/p3-9-submitting.json` is written before `run_hardware` and blocks any later `--submit`.

## 4. Statistics

- **Unit:** a *system* is one (input state, order) pair: the six lines measured in that order, as a 6-context CbD system of 18 binary random variables (9 connections of 2). There are four systems: |00⟩-forward, |00⟩-reverse, Bell-forward, Bell-reverse. Order is not folded into context. By CbD 2.0 Theorem 3, a contextual single-order system makes the order-folded 12-context system contextual too, so analysing each order on its own is at least as strict as folding. The folded LP (2³⁶ joint values, 5⁹ after the threshold reduction) is not computed.
- **Primary statistic:** for each system, **CNT2** (Kujala & Dzhafarov 2019, eq. 38–40), computed by `cbd_lp.cnt2`'s exact LP (HiGHS), from the 8-cell outcome frequencies of each of its six circuits.
- **Uncertainty:** a nonparametric bootstrap, B = 1,000. Each draw resamples each circuit's 4,000 shots multinomially from its observed frequencies, independently across circuits. The draws are seeded from the beacon's `boot` sub-seed (`numpy.random.SeedSequence(seed).generate_state(1000)`, one generator per draw). The **99% lower bound** is the 10th smallest of the 1,000 CNT2 values; the same for χ.
- **Zero:** CNT2 ≤ 1e-6 counts as zero (P13: the boundary is never compared in plain floating point; HiGHS's feasible optima are below 1e-9).
- **Secondary, reported, never promoted:**
  - χ per system with its bootstrap SE and 99% lower bound;
  - Δ0 (Massé's connection discrepancy);
  - Massé's CNTX (his adapted formula, for comparison);
  - each observable's mean in each context (the 9-connection table, both orders);
  - the number of bootstrap draws with CNT2 = 0;
  - measured against predicted χ and CNT2;
  - Sean's card event (both states, either order) — implied by a pass, and by CbD 2.0 Theorem 3 also by one order per state;
  - χ against Kelleher & Holweck's 5.31 on another Heron r2.
- **Multiple comparisons:** the pass rule is a conjunction of four tests, each at the 99% level; no correction is applied, because a conjunction can only make passing harder.
- **Dumb baselines** (P3), named and shown not to pass the rule:
  - (a) **"χ > 4"** without CbD: the cheat (fixed context-dependent answers) has χ = 6.000 and CNT2 0 (`--check`; world "cheat" below), so a χ-only reading would be passed by a noncontextual system with signalling.
  - (b) **Carry-over:** "physics and published hardware say pass", P = 0.95, reported beside the odds in scoring.
  - (c) The running base rate, 0.32.
- **D11 worlds** (`--worlds`, from the committed noisy prediction; 20 simulated 4,000-shot datasets per world, each run through the full rule with a 100-draw bootstrap; `data/p3-9-worlds.json`, committed with this file). With 100 bootstrap draws, the 99% lower bound is the smallest of the 100 draws; each P(pass) is from 20 datasets, so it is coarse (about ±0.1).

  | world | what it is | P(pass) | true χ (four systems) | true CNT2 (four systems) | labels seen in 20 datasets |
  |---|---|---|---|---|---|
  | `noisy_sim` | the committed noisy prediction itself (the hypothesis holds) | **1.00** | 5.72–5.79 | 0.220–0.227 | all contextual |
  | `flip0.03` | extra outcome flips of 3%, 6%, 9% on the 1st, 2nd and 3rd measurement (the pre-mortem's disturbance, growing with each later measurement) | **0.95** | 3.88–3.93 | 0.044–0.087 | one |00⟩-forward dataset below; the rest contextual |
  | `flip0.04` | flips of 4%, 8%, 12% (noise spoils it) | **0.00** | 3.36–3.40 | 0 in |00⟩-forward and Bell-reverse; 0.045 in the other two | |00⟩-forward and Bell-reverse below in all 20; the other two contextual |
  | `flip0.05` | flips of 5%, 10%, 15% | **0.00** | 2.88–2.92 | 0–0.006 | all below |
  | `cheat` | noncontextual: fixed, context-dependent answers, χ = 6 | **0.00** | 6.00 | 0 | all absorbed |

  Reading:
  - The rule passes in the world the committed simulator predicts. It still passes with up to 3/6/9% extra disturbance, which is two to five times the omitted idle decay's at most 1.7% (§2).
  - It fails at 4/8/12% or more, and a noncontextual system with χ = 6 never passes it.
  - So the bet can pass (P ≥ 0.95 in the hypothesis world) and can fail (P = 1 in the noise-spoils and cheat worlds); D11 holds.
  - The step between 3% and 4% is sharp. A fail needs mid-circuit errors several times what IBM's calibration reports, so the engine's 0.80 prices that unreported error, not a coin.
  - In `flip0.03`, χ's true value is below 4, yet CNT2 is above 0. The linear program finds contextuality among its other noncontextuality constraints, so a pass need not mean the raw Peres–Mermin sum beat 4. The verdict says so when that happens (§5.3).
  - Spot check by the finishing session: datasets 0 and 1 of `flip0.03` and `flip0.04` were recomputed from the committed code and gave the same labels as the file (dataset 1 of `flip0.03` is its one below).
- **Leave-one-out (P10):** for each system, the point CNT2 is recomputed six times, each time with one of its six circuits replaced by the noisy simulator's prediction for that circuit. This is reported, not a gate. If replacing one circuit moves the point CNT2 across zero, the write-up names that line ("rests on line <L>").
- **Robustness committed now:** the analysis is unpooled by state and order (four systems, never pooled). The auditor may re-run the LP with the other encoding (1 = eigenvalue +1); the pass decision must not change.

## 5. Pre-registered reading

The sentences are produced by `p3_9_pm.verdict()` (`--check` prints them for every label combination). Each system gets one label:
- **contextual:** CNT2's 99% lower bound > 1e-6;
- **absorbed:** not contextual, and χ's 99% lower bound > 4 (the raw sum beat the classical bound, but CbD's correction for the measured disturbance absorbed it);
- **below:** neither (the raw sum did not clearly clear 4).

1. **Pass:** all four systems contextual. Sentence: "Pass: for both input states, in both measurement orders, the exact CbD linear program rejects noncontextuality with CNT2's bootstrap 99% lower bound above 0. Program 1's check sees contextuality on this chip where physics says it must be. This is an instrument check on one chip, one qubit triple and one job, not a new fact about quantum theory, and it says nothing about language models." Outcome 1. Reported as **pass, unreplicated** (invariant 7).
2. **Fail:** any system not contextual. Outcome 0. The headline is one of:
   - "the check saw contextuality for <state> in both orders, but not for <the other state> in both orders"; or
   - "in some of the four systems but not for both input states in both orders"; or
   - "in none of the four systems".

   It is followed by one of two noise sentences. **When noise spoils it** (every miss is `absorbed`): "Wherever it missed, the raw sum still beat the classical bound, so what failed is the chip's measurement quality under CbD's correction, not quantum theory." If any miss is `below`: "Where the raw sum did not clear 4, the chip's sequential measurements were too noisy for this test, which says nothing against quantum theory."
3. **Per-system sentences, always printed:**
   - contextual: "For <state> <order>, the exact CbD linear program rejects noncontextuality (CNT2's 99% lower bound <x> > 0)." If χ's lower bound is ≤ 4, add: "There the Peres-Mermin sum itself did not clearly beat 4 …: the linear program found the contextuality in the full set of noncontextuality constraints, not in the Peres-Mermin inequality alone."
   - absorbed: "… the raw Peres-Mermin sum still beat the classical bound of 4 (99% lower bound <x>), but the chip's measurements disturbed each other enough that CbD could not tell the result from a noncontextual system with that disturbance (CNT2's 99% lower bound <y>): noise spoiled the check here, not quantum theory."
   - below: "… the chip's measurements were too noisy for even the raw Peres-Mermin sum to clear the classical bound of 4 (99% lower bound <x>): noise spoiled the check here, not quantum theory."
   - If one order passed and the other did not for a state: "… so the order of the measurements mattered on this chip (by CbD 2.0 Theorem 3 the system with order folded into context is still contextual for that input)."
4. **Untestable** (not scored): any one of
   - the job was not submitted (a stop before submission: the reserve rule, the hard stop, a circuit not ISA on the live target);
   - the job errored or returned no counts;
   - the wrong number of circuits came back;
   - any circuit returned under 90% of its 4,000 shots.

   Sentence: "The test could not be run as pre-registered (<reason>), so it says nothing about the check or the chip; it is not scored."
5. **Reported in every case:** the four systems' χ (with SE), CNT2 (point, 99% lower bound, bootstrap median, draws at zero), Δ0 and Massé's CNTX; the connection table; measured against simulated values; the job id, billed QPU seconds, execution timestamps, and the triple's calibration at submission and at run time.

## 6. What it cannot do

- It cannot show anything about quantum theory: a fail is about this device's measurements. Nor does it say anything about language models: it checks the instrument program 1 used, on a system where the answer is known.
- It cannot close the compatibility loophole or memory-based classical models of sequential measurements (Gühne et al. 2010; Jerger et al. 2016). It is a single-system sequential test on one chip, with crosstalk between neighbouring qubits not excluded.
- One chip, one qubit triple, one job, one afternoon. "Every", "all chips" or "superconducting hardware" will not appear in the write-up.
- CbD 2.0's contextuality is a property of the observed system as CbD defines it. A pass shows that the bunches are incompatible with the multimaximal couplings of the connections, given the disturbance actually measured. It does not separate disturbance from other causes of inconsistent connectedness, and does not need to.
- The order-folded 12-context system is not analysed beyond Theorem 3's implication (§4).
- The noisy simulator omits mid-circuit-measurement crosstalk and reset error, so a gap between measured and predicted χ is about that omission, the calibration or the device. It is not a quantum advantage, and nothing here is one.

## 7. Stop rules

- QPU cap in code: `--submit` refuses if the estimate exceeds 45 s, if 45 s exceeds the approved `budget_ruling`, if cumulative billed seconds plus 45 would pass the **420 s hard stop**, or if cumulative plus 1.5 × the estimate would pass the 300 s reserve line. `run_hardware` refuses at 420 s regardless.
- `--submit` also refuses:
  - without a design-review go;
  - if any file it uses is uncommitted or changed;
  - if `ledger/check_prereg.py ng-p3-9 … --before-run` fails;
  - on a circuit hash mismatch;
  - if this bet already has a raw file, a marker, or a QPU ledger entry.
- One job only; never resubmitted. A client error after submission leaves the marker and is resolved by looking the job up by id (a free read); the counts are retrieved, never re-run.
- Untestable conditions as in §5.4.

## 8. Ledger entry (filled now, completed after audit)

```json
{"id": "ng-p3-9", "program": "nature-graded", "direction": "P3-9", "map": "program-3-map",
 "title": "Does program 1's contextuality check see contextuality on the chip, where physics says it must be? Sequential Peres-Mermin under exact CbD 2.0",
 "source": "literature", "odds_event": "for both input states (|00> and the Bell state) and in both measurement orders, the exact CbD 2.0 LP rejects noncontextuality: CNT2's bootstrap 99% lower bound > 1e-6 in all four systems",
 "engine_odds": 0.80, "engine_odds_first": 0.40, "engine_odds_at": "2026-11-05 (8bf9942)",
 "odds_prior": 0.32, "odds_adjustment": 0.48, "odds_reason": "Low nature-graded/nature/literature rows (0.20, 0.13) are novel-claim bets; here QM, every published PM platform, and the simulator margin (CNT2 0.22, holds to ε=0.03) all predict pass.",
 "odds_prior_commit": "73eb5cf", "odds_template": "v2",
 "human_odds": 0.90, "human_odds_at": "ho-20261105-051140-7pv",
 "prereg_commit": "<this commit>", "test": "experiments/p3-9-peres-mermin.md", "budget_usd": 0, "cost_usd": 0, "qpu_s_budget": 45,
 "steer": "st-24 (Sean: P3-9 is the chip's one foundations experiment; st-19's cap)", "dumb_baselines": {"carry_over": 0.95, "running_base_rate": 0.32},
 "referee": "nature", "bet_type": "standard", "seed_source": "curby-rng", "beacon": null, "seed": null, "tiebreak": null,
 "lesson": "ls-ng-p3-9", "design_review": {"path": "ledger/design-reviews/ng-p3-9.md", "verdict": null},
 "premortem": "If this fails, the most likely reason is that ancilla 4's mid-circuit readouts and resets disturb the data qubits enough, growing with each later measurement, that CNT2 reaches 0 in at least one of the four systems.",
 "premortem_kind": "design", "prior_work_predicts": "pass",
 "novelty": null, "novelty_line": null, "novelty_by": null, "novelty_at": null,
 "verdict": "open", "date": "2026-11-05", "result": null, "audit": null}
```

## 9. Checklist before the first submission

- [x] This file is committed on its own; nothing has been submitted. (The free IBM reads, circuits and simulator prediction were committed before it, `b1a06a5`.)
- [x] §0's prior work row states a predicted outcome (pass) with citations and a described search; what the bet adds is stated (rule 13, D12).
- [x] Lesson in §0, after reading the ledger at `73eb5cf`; the same sentence goes to `ledger/lessons.jsonl` as `ls-ng-p3-9`.
- [ ] Design review go (or confirmed fix-first) in `ledger/design-reviews/ng-p3-9.md`; `python3 ledger/check_prereg.py ng-p3-9 . programs/nature-graded/experiments/p3-9-peres-mermin.md --before-run` passes.
- [x] Cockpit card committed before this file (`7996d98`); `ledger/human-odds.jsonl` read immediately before this commit; Sean's 0.90 copied.
- [x] Engine odds on record before this commit (`8bf9942`).
- [x] §5 can be applied by a stranger: `verdict()` gives one verdict on every label combination (`--check`).
- [x] Pre-mortem: one sentence, a checkable mechanism, kind `design`.
- [x] One scale direction: not applicable (no graded prompt; the chip's ±1 outcomes).
- [x] §2 records CURBY-Q's latest completed round and names the chain by the 24-hour rule; the seed commit follows this one before any data.
- [x] Budget, hard stop, reserve line and one-job rule enforced in code (§7).
- [x] DEVIATIONS.md row D48.
- [ ] Budget ruling in `ledger/spend.jsonl` under st-16, after the design review. Its id is the next free `br-NNN` above main and every sibling worktree, read immediately before writing. The drafting session's `br-007` is taken (ss-b13); br-001 to br-019 were in use when this file was finished.
- [ ] *(after the result)* The Novelty line (rule 13) is written by a fresh session before the results file is audited.
