# P3-3. Is the gap nine particular qubits, or one afternoon? (pre-registration)

Frozen at this file's commit time (America/Denver; the commit's author time is authoritative), in its own commit, before any circuit is submitted. DEVIATIONS.md D4. Its two arms (L1, L2) ride in P3-2's one job (`experiments/p3-2-twirl-dd.md`, §2–3, §7), so the job's budget, stop rules and failure rule are P3-2's. Budget **$0 API · its share of the ≤ 12 QPU s job (4,000 of 20,000 shots, ≈ 1.1 s)**.

## 0. The bet

| field | value |
|---|---|
| bet id | `ng-p3-3` |
| referee | `nature` |
| bet type | `standard` |
| direction | `P3-3` (map/program-3-map.json) |
| source | `literature` (cluster D) |
| engine odds, P(pass) | **0.12**, stated 2026-11-04T14:06:13-07:00 in map/program-3-map.json (template v1-batch). Not in the elicitation-check half. |
| human odds, P(pass) | **not recorded**: Sean chose to proceed without his odds (D0); closed for human odds. |
| budget | $0 API · ≈ 1.1 QPU s within P3-2's job |
| pre-mortem | "If this fails, the most likely reason is that the departure is device-wide (gate error under-reported on every qubit, as P3-5's fits and Heron model-scaling studies suggest), so other layouts depart as much as the original." Kind: `world`. |
| auditor | fresh session per operators/auditor.md, after results |

## 1. In plain English

Maybe program 1's surprise belongs to nine particular qubits, one of which (qubit 125) had unusually poor phase memory that afternoon. If so, the same circuit on two other sets of nine qubits should agree with the simulator much better. We pick the two sets by a rule written now: avoid every original qubit, pick the healthiest-looking sets by median T2, and let the seed break ties. Then we run them in the same job as the original. If both alternative sets cut the simulator-versus-chip gap to under half the original's, the surprise was local. If they don't, it is a property of the chip, or of the circuit, on any qubits. The second half of the map's question, whether the gap changes hours apart, needs a second job and is not run this session.

## 2. Material

- **Circuit:** the archived Stage 1 ISA circuit with every physical qubit p moved to its image under the layout map. Same gate list, same angles, same CZ pairs up to relabelling (`p3_2_3_job.remap`).
- **Layout rule** (`p3_2_3_job.choose_layouts`, on the live `ibm_fez` target read at prediction time):
  1. Healthy device graph: qubits with T1 and T2 reported and readout error < 0.05; CZ pairs with error < 0.02.
  2. Exclude all 9 original qubits (117, 123, 124, 125, 136, 141, 142, 143, 144). This includes the map's "exclude 125" and makes the sets genuinely "other".
  3. Candidates: every subgraph monomorphism of the circuit's interaction graph (the 8 CZ pairs: a path of 8 with a branch at 143) into the healthy graph.
  4. Rank by the median T2 of the 9 image qubits, descending. Ties, and the choice among relabellings of the same qubit set, go to a uniform random key from the seed.
  5. **L1** = rank 1. **L2** = the best-ranked candidate sharing no qubit with L1.
  - Checked before this commit, on FakeFez's offline snapshot (not the live device, structure only): 197 candidates; both layouts remap to native circuits.
  - *Specification of the map's rule:* the map says "exclude qubit 125; among chains of the original's connectivity, maximise median T2". Steps 1, 2 and 5 are added here (D4).
- **Predictions** S_L1 and S_L2: the P3-1 construction on the live target (as P3-2's S), 100,000 shots each, committed in the prediction commit before submission, with the layouts.
- **Seed** (operators/hardware.md): CURBY-Q latest completed round **28297, result pulse 2025-08-22 13:42 America/Denver** (checked 2026-11-04 15:30), so it is **stalled**. **Seed: the first CURBy-RNG pulse timestamped after this commit**, by `ledger/seed.py --purpose layout`; its `seed32` seeds the tie-break keys. *Filled in by the seed commit:*
  `chain:` CURBy-RNG · `pulse index:` 1591395 · `pulse_time:` 2026-11-04 15:51:00 America/Denver · `previous pulse:` index 1591394 at 2026-11-04 15:50:00 (before the commit at 2026-11-04 15:50:03) · `randomness:` 4d53a094d97a8ef0213b94084485f1af4759afdb5475443b7b25310b4e51dc0503d6d4d2a65cd31f00b35c80b2670e7458a137ce46839736d633a01ef6aef8a2 · `client:` @buff-beacon-project/curby-client@1.2.0 via `experiments/curby_seed.mjs` · `certificate_verified:` false · `seed (layout):` 695859889174533085 · `seed32 (layout):` 3820016605. Record: `data/p3-3-seed.json`.

## 3. Calls

Within P3-2's job (§3 there): arms L1 and L2, 20 instances × 100 shots each.

## 4. Statistics

- **P(yes)** per arm as in P3-2 (raw counts, pooled).
- **Primary statistic:** g_orig = |P_A − S| (the same-job original-layout gap, P3-2's arm A); g_L = |P_L − S_L| for L1 and L2.
- **Secondary, reported, not scored:** P_L − S_L signed; per-qubit marginals; the layouts' calibration at prediction and execution time; whether the alternative layouts' marginals drop like the original's.
- **The repeats ≥ 3 h apart** (the map's secondary drift check) are **not run** this session (D0).

## 5. Pre-registered reading

1. **Untestable:** g_orig < 0.10. With too small a same-job gap there is nothing to halve.
2. **Pass:** g_orig ≥ 0.10, g_L1 < g_orig / 2 and g_L2 < g_orig / 2.
3. **Fail:** g_orig ≥ 0.10 and not a pass.
4. **Job failure:** as P3-2 §5.4.
5. **Reported in every case:** P_A, S, P_L1, S_L1, P_L2, S_L2, the three gaps, and the layouts.

## 6. What it cannot do

- Two alternative layouts, one job, one afternoon. A pass says "these nine qubits", not which of them. A fail says "not specific to these nine", not why.
- The layouts were chosen to have *good* T2. A pass partly reflects healthier qubits, and that is the point of the rule. It is not a random sample of the chip.
- No drift test this session.

## 7. Stop rules

P3-2's (§7 there).

## 8. Ledger entry (filled now, completed after audit)

```json
{"id": "ng-p3-3", "program": "nature-graded", "direction": "P3-3",
 "title": "Is the gap nine particular qubits, or one afternoon?", "source": "literature",
 "engine_odds": 0.12, "engine_odds_at": "2026-11-04T14:06:13-07:00",
 "human_odds": null, "human_odds_note": "not recorded: Sean chose to proceed (nature-graded D0); closed for human odds",
 "prereg_commit": "<this commit>", "budget_usd": 0, "qpu_s_budget": "shared with ng-p3-2 (<= 12)",
 "referee": "nature", "bet_type": "standard", "seed_source": "curby-rng", "beacon": null, "seed": null, "tiebreak": null,
 "premortem": "If this fails, the most likely reason is that the departure is device-wide (gate error under-reported on every qubit, as P3-5's fits and Heron model-scaling studies suggest), so other layouts depart as much as the original.", "premortem_kind": "world",
 "verdict": "open", "date": "2026-11-04", "result": null, "audit": null, "diagnosis": null}
```

## 9. Checklist before the first call

- [x] Committed with its DEVIATIONS row only. Nothing fetched or submitted.
- [x] Engine odds on record. Human odds: not recorded (D0).
- [x] Pass rule applicable by a stranger.
- [x] Pre-mortem with kind.
- [x] §2 records CURBY-Q round 28297 (stalled) and names CURBy-RNG; seed commit follows.
- [x] DEVIATIONS.md D4.
