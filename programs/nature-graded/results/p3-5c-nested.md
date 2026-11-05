# P3-5c result: on all three archived pairs (one job, 3 November), the 16-knob model needs both a rotation-type and a blur-type term (not scored)

Pre-registration: `experiments/p3-5c-nested.md` (commit `930efe8`, 17:31; seed `03356ad`, CURBy-RNG 1591496). Design-review fixes D19–D25, recovery study D26 (`511ea05`); review `ledger/design-reviews/ng-p3-5c.md`: fix-first, confirmed (header typed 21:45; commit `709d8c1` at 21:38:51, which is the record; D11 holds). Run `experiments/p3_5c_fits.py --run`, about 21:47–22:50 on the laptop: archive counts only, $0, 0 QPU s. **Not scored; no odds stated.** P3-5's scored verdict (fail, odds 0.42) stands as recorded. This is reported beside it, never in place of it. Audited: `ledger/audits/ng-p3-5c.md` (249e0af; cuts applied in D30) and round 3, `ledger/audits/round-3/ng-p3-5c.md`.

## In plain English

*These are the sentences pre-registered in §5, applied as the rule says.*

On pair h221, the counts need both a rotation-type term (local rotations and a ZZ phase) and a blur-type term (random Pauli flips, uniform mixing and energy decay) beyond the simulator's state; neither alone fits as well. These are terms in a 16-knob model fitted to these counts, not identified physical mechanisms.

On pair h088, the counts need both a rotation-type term (local rotations and a ZZ phase) and a blur-type term (random Pauli flips, uniform mixing and energy decay) beyond the simulator's state; neither alone fits as well. These are terms in a 16-knob model fitted to these counts, not identified physical mechanisms. Even both terms together leave a misfit the model cannot explain (deviance 63.3 on 11 df), so part of what each term absorbs may be neither kind. At 0.1 rad, spectator rotations were too small to see on this pair, so this check cannot rule them out.

On pair h268, the counts need both a rotation-type term (local rotations and a ZZ phase) and a blur-type term (random Pauli flips, uniform mixing and energy decay) beyond the simulator's state; neither alone fits as well. These are terms in a 16-knob model fitted to these counts, not identified physical mechanisms.

Overall: both present on 3 of 3 pairs; rotation only, blur only and neither on none. These are three pairs from one job on one afternoon. 'Present' is a statement about fit, not size: with 36,000 shots per pair, the weakest label (rotation on h221) improves the log-likelihood by about one unit per 1,000 shots, and any extra knobs that absorb part of a mis-specified reference's error will be needed in this sense. The recovery study shows the test does not return 'both' by default for truths built from these two families; it cannot say that for errors outside them (readout drift, spectator rotations), which the spectator check and the h088 misfit show are live (audit round 3). This re-analysis was specified before it ran, but the archive had already been analysed by this program and its auditor, who saw both kinds of term on every pair; it is not a blind test.

*Which rules applied, so a stranger can check:*
- "Present" means bootstrap p < 0.01. All six tests (3 pairs × 2 kinds) reached B = 1,000 under the D20 extension and gave p = 0.001, the floor 1/(B + 1). Every observed LR is above the largest of its 1,000 null draws. So all six also pass the Bonferroni line, 0.0017.
- Misfit rule: full16 deviance against χ²₁₁'s 99th percentile, 24.7. Only h088 exceeds it (63.3). h221 gives 14.0 and h268 16.8. On h088 the bootstrap nulls are drawn from a model the counts reject, so its p-values are not calibrated as stated. Scaled by the overdispersion (deviance/df = 5.8), h088's LRs are 32 (rotation) and 42 (blur), still above the nulls' 99th percentiles of 17.5 and 9.9; h221's and h268's scaled LRs (30, 102; 156, 47) are clear too (round 2's scaling, confirmed in round 3).
- One-setting rule (D24): no setting carries more than half of any LR labelled present (the largest share is 0.43, YZ for rotation on h088), so no "rests mostly on setting" sentence and no drop-one refit. The weakest label is rotation on h221: two settings, XZ (15.5) and XY (11.0), carry 69% of its LR of 38.5. In the auditor's post-hoc refits, dropping XZ alone leaves 19.5 and dropping both leaves 13.8, against that null's 99th percentile of 13.0. The label survives every single and paired drop, but narrowly. *(Audit cut 4, D30.)*
- CV (secondary, D21): positive for both kinds on every pair, so the "CV disagrees" sentence does not apply.
- Spectator check (D23): on h088, 19 of 20 draws were invisible, so the "invisible" sentence applies. On h268, 20 of 20 were detected as rotation. §5 has no sentence for that outcome, so it appears only in the table.
- The "never 'blur, not steering' or the reverse" rule: no sentence says either.

**Novelty:** known. Tripathi et al. 2022 (Phys. Rev. Applied 18, 024068; arXiv 2108.04530) state that on IBM fixed-frequency transmons the always-on ZZ coupling "contributes to both coherent and incoherent crosstalk errors", alongside open-system decoherence; Carignan-Dugas et al. 2024 (Quantum 8, 1367; arXiv 2303.09945) measure "substantial coherent errors biased in Z" on three IBM chips next to decoherent error; Georgopoulos et al. 2021 (Phys. Rev. A 104, 062432) find operations "more or less erroneous than the hardware-calibrated parameters show". Our finding that ibm_fez pairs need both a rotation term and a blur term beyond the calibrated simulator is the same statement in the same direction, on a tunable-coupler Heron device. Search: WebSearch for "superconducting qubits coherent and incoherent errors gate set tomography IBM ZZ calibration noise model underpredicts", "ibm_fez Heron coherent errors", "gate set tomography IBM coherent stochastic"; arXiv abstract pages for each lead. *(Rule 13, CONTEXT.md §3; written by a fresh claude-fable-5-1 subagent launched by the informed-engine session, 2026-11-05, web reads only, no model API; its papers-opened list and caveats are in programs/nature-graded/map/reads/novelty-2026-11-05-ng-p3-5c.md.)*

## Tables

**Primary tests** (16-knob model; LR = 2 × log-likelihood gain; null from the parametric bootstrap, B = 1,000):

| pair (qubits) | rotation given blur: LR | null 99th pct | p | blur given rotation: LR | null 99th pct | p | labels |
|---|---|---|---|---|---|---|---|
| h221 (10, 9) | 38.5 | 13.0 | 0.001 | 128.8 | 9.0 | 0.001 | both present |
| h088 (44, 37) | 183.6 | 17.5 | 0.001 | 242.3 | 9.9 | 0.001 | both present |
| h268 (4, 16) | 237.6 | 17.3 | 0.001 | 72.0 | 8.8 | 0.001 | both present |

**Fit diagnostics:**

| pair | full16 deviance (11 df; q99 24.7) | top setting share, rotation | top setting share, blur | CV gain, rotation | CV gain, blur | negativity: ref / coh / inc9 / full16 |
|---|---|---|---|---|---|---|
| h221 | 14.0 | 0.40 (XZ) | 0.24 (YZ) | +7.7 | +86.0 | 0.179 / 0.176 / 0.137 / 0.145 |
| h088 | **63.3 (misfit)** | 0.43 (YZ) | 0.38 (XX) | +22.9 | +228.7 | 0.109 / 0.119 / 0.034 / 0.062 |
| h268 | 16.8 | 0.26 (XX) | 0.22 (YX) | +145.6 | +67.1 | 0.092 / 0.103 / 0.037 / 0.067 |

**Secondary 14-knob set** (frozen design, no decay): the same labels on every pair. Rotation LR 42.9, 183.6, 234.0; blur LR 128.8, 242.2, 68.4; all p = 0.001.

**The P3-5 comparison, three ways** (D25, F7; coherent 7-knob logL minus incoherent 7-knob logL, so positive favours steering):

| pair | P3-5 as published | P3-5 families, legacy reference | same, fixed T1/T2 | bounded 7-knob blur, fixed T1/T2 | 9-knob blur (with decay), fixed T1/T2 |
|---|---|---|---|---|---|
| h221 | −43.5 | −43.53 | −42.97 | −42.97 | −45.17 |
| h088 | −34.9 | −34.88 | −29.32 | −29.32 | −29.32 |
| h268 | +63.0 | +63.01 | +82.78 | +82.78 | +82.78 |

- The legacy line reproduces P3-5 to the published 0.1 on every pair. So review note 1 (rerun with P3-5's own starts if it missed by more than about 1) did not trigger.
- Fixing T1/T2 moves h088 by +5.6 and h268 by +19.8. The reparametrisation changes nothing to 0.001. Adding decay to the 7-knob blur family moves only h221 (−2.2).
- Whichever way it is computed, P3-5's head-to-head still favours blur on h221 and h088, and steering on h268. The nested tests above say why that contest was the wrong question: in the 16-knob model, each term is needed given the other on all three pairs.

**Spectator check** (D23; 0.1 rad ZZ on the 344 CZ pairs not touching the measured pair; 20 synthetic draws, classified with the pair's real-data null 99th percentiles):

| pair | trace distance to ρ_ref | detected as rotation | absorbed as blur | invisible |
|---|---|---|---|---|
| h088 | 0.009 | 0 | 1 | **19** |
| h268 | 0.037 | **20** | 0 | 0 |

**Noticed after the data; leads, not findings:**
- On h268, spectator rotations of 0.1 rad show up as *rotation*, not blur, in every draw. So on that pair, part of the rotation-type term could come from rotations on other qubits in the circuit, not only on the measured pair. §5 wrote no sentence for this outcome.
- h088's misfit (63.3 on 11 df) is the largest. h088 is also the pair whose blur term is biggest (LR 242) and whose fitted state loses the most negativity relative to the reference (0.109 → 0.062).
- On h221 and h268, a rotation model with four extra readout knobs makes the blur term unnecessary (LR 8.9 and 7.6). This needs 2.7–5% extra readout error per qubit, several times IBM's reported 0.2–0.9%, so it is unlikely here, but this design cannot exclude it (auditor, post hoc; D30).
- The run printed an overflow warning from P3-5's softmax incoherent family, inside the legacy comparison. That line still reproduces P3-5, so it did not change the result.

**Pre-mortem** ("the 14-knob fits land in different local optima across bootstrap samples, widening the null and hiding steering that the point fit shows"; kind `design`). For the auditor: no rotation-type term was hidden. Every rotation LR beat all 1,000 null draws, by a factor of 3 to 14 over the null's 99th percentile. The pre-mortem names the 14-knob set; the 16-knob primary behaves the same way.

Data: `results/p3-5c-nested.json` (fits, all bootstrap nulls, setting shares, spectator outcomes). Code: `experiments/p3_5c_fits.py --run`. Recovery evidence: `data/p3-5c-recovery.json`.
