# Engine odds, elicitation check: negated question (fresh context)
Elicited: Wed Nov 4 14:06 MST 2026 (America/Denver). Model: Claude Opus 5.5 (claude-opus-5-5). Input: rows-negation.md only.

## P3-1
Rationale: Idle T1/T2 decay does push P(1) downward, which is the right direction. But a depth-208 circuit on Heron lasts roughly 10–20 µs. Against T1 ≈ 140 µs, that adds only about 5–15% extra relaxation and dephasing on idle qubits. It cannot plausibly take a marginal from 0.75 to 0.30 or close 60% of a 0.25 gap. Vezvaee's 2.3–4× scaling and Bautra's poor twin fidelity point the same way: calibration-based models badly underpredict deep-circuit error. A bad-TLS qubit in the snapshot could explain one qubit, not eight.
P(not pass): 85

## P3-4
Rationale: XY4 usually helps on IBM hardware, but the requirement is strong: recover half of a 0.086 gap. Item h221, whose pair is decoupled from the rest, already nearly matches the sim. That suggests h088's loss comes from gate errors in its 162-CZ entangling history, which DD cannot undo, more than from idle dephasing. Heron r2's tunable couplers also suppress static ZZ, which shrinks DD's typical gain. Statistical resolution is adequate, so the outcome turns on the physics, and a gain of ≥0.043 looks less likely than not.
P(not pass): 65

## P3-6
Rationale: With no entangling gates and phase-only settings (virtual Z plus basis pulses), the main leakage channels are readout crosstalk and drift between circuits. Both should be at or below the 1% level, well under the ≈0.03 lean-version detection threshold after a 4.5σ Bonferroni cut. Bednorz found ibm_kingston (also Heron r2) clean. Risks: ibm_fez is the weaker device, Rybotycki-type anomalies of unknown cause could be shifts of about 0.05, and some of the ~40 pairs may include a drifting or TLS-affected qubit.
P(not pass): 35

## P3-8
Rationale: The Haddara & Cavalcanti classification suggests genuine non-Bell LF facets exist when the friend's party has 3 settings. A quantum violation of some facet is plausible. But genuine LF inequalities typically have small quantum violations, and the known two-friend cases needed high visibility. A white-noise tolerance of ≥15% (visibility ≤ 0.85) is demanding, and the one-friend 3×2 case may have few or no useful facets. Enumeration and see-saw are feasible, so the risk lies in the threshold, not computability.
P(not pass): 70

## P3-11
Rationale: Ideal K3 = 1.5. MCM assignment errors of 1–2% and about 1% T1 decay per measurement scale the correlators by about 0.92–0.95, giving K3 ≈ 1.38–1.43. For a maximally mixed preparation, the marginals stay near zero under unital dynamics, so the CbD correction is small. With 24,000 shots per circuit, σ is about 0.01, and 5σ is easy. Disturbance on the eigenstate controls should be a few percent, well below K3 − 1 ≈ 0.4. The main risks are |+⟩ being counted as "classical", a larger-than-expected MCM disturbance, or implementation errors.
P(not pass): 25

## P3-12
Rationale: If the X measurement is done correctly (H, measure, H), a full projective measurement erases Z information. With about 200k pooled samples, σ is about 0.002, so |corr| < 0.01 should hold unless leakage accumulates. Leaked qubits read a constant outcome, which correlates their results. That effect is probably <0.5%. The harder clause is the control: consecutive Z-MCM agreement ≥95% pooled over ~50 qubits. With MCM errors of 1.5–3% and some poor qubits, I expect about 95–97%, close to the bar. Both clauses must hold.
P(not pass): 40

## P3-13
Rationale: The Theorem 2 rate is 0.054 at K3 = 1.31 and 0.115 at 1.40. At about 72,000 rounds the finite-size penalty leaves roughly 60–65% of the asymptotic rate. Reaching 0.05 bits per round therefore needs an asymptotic rate of about 0.08, meaning K3 ≳ 1.35. I expect raw MCM-based K3 ≈ 1.38–1.43, so passing is more likely than not. Risks: K3 comes out lower (leakage, MCM-induced transitions), the 99% finite-size bound is harsher than the photonic scaling suggests, or P3-11 itself is compromised.
P(not pass): 35
