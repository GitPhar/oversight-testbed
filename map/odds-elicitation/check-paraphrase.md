# Engine odds, elicitation check: paraphrased pass rules (fresh context)
Elicited: Wed Nov 4 14:06 MST 2026 (America/Denver). Model: Claude Opus 5.5 (claude-opus-5-5). Input: rows-paraphrase.md only.

## P3-1
Rationale: Depth 208 on Heron is roughly 10 µs. With T1 around 140 µs and comparable T2, ALAP idle decay adds only a few percent relaxation and dephasing per qubit. That is far too little to pull one marginal from 0.75 to 0.30 or to move P(yes) from 0.25 to at least 0.40. Overwriting with the job-time calibration helps only if that snapshot itself shows some badly degraded qubits. The literature says calibration-derived models need 2.5 to 4 times scaling, which points to unmodelled coherent errors, crosstalk or leakage, not missing idle decay. A small chance that the snapshot shows a TLS-hit qubit.
P(pass): 12

## P3-4
Rationale: Passing needs DD-on negativity to reach at least about 0.106 from about 0.063, recovering half of the 0.086 hardware-to-simulation gap. The CI on the difference is roughly ±0.017, so the bootstrap condition holds if the effect is real. Heron's tunable couplers suppress static ZZ, which limits what DD can fix. Some of the gap is likely gate error, leakage and non-Markovian noise that DD cannot touch. Vezvaee's scaling drop (3.8 to 2.4) suggests DD matters on Heron, but a half-gap recovery on one item is ambitious.
P(pass): 30

## P3-6
Rationale: With 10,000 shots, SE is about 0.005, so the flag threshold is around 0.022 to 0.025 after Bonferroni. The tests are idle with phase-only settings, so the remaining mechanisms are readout crosstalk, drift between circuits and TLS fluctuations. Bednorz found ibm_kingston (also Heron r2) clean, but ibm_torino and the Eagle devices were not. ibm_fez is the weakest Heron r2, and 40 pairs give many chances for one bad pair or a drift event. Roughly a coin flip, leaning slightly toward clean at this sensitivity.
P(pass): 50

## P3-8
Rationale: Haddara and Cavalcanti's classification suggests genuine (non-Bell) facets exist in the one-friend, three-setting scenario, and enumeration at this size is feasible on a laptop. Two hurdles remain: quantum theory must violate a genuine facet, and the violation must survive at least 15% white noise. Known genuine LF inequality violations (Bong et al.) are fairly fragile, and partial determinism of one setting further limits the quantum advantage. The existence of a facet is likely; the noise-tolerance threshold is the main risk.
P(pass): 30

## P3-11
Rationale: With mid-circuit errors of about 1 to 2%, final readout of 0.7% and slight T1 loss during measurement, I expect K3 around 1.38 to 1.43. With a maximally mixed preparation, the CbD marginal differences should be small (a few hundredths summed, mainly readout asymmetry and decay bias). Pooled statistics (24,000+ shots per correlator) give σ near 0.01, so the 5σ condition is easy. Disturbance on |0⟩/|1⟩ eigenstates should be a few percent, well below K3−1 ≈ 0.3. The risks are pathological mid-circuit measurement behaviour or definitional surprises in the disturbance metric.
P(pass): 72

## P3-12
Rationale: Projective mid-circuit measurements should erase memory across the intervening non-commuting measurement. Pooled SE (~50 qubits × 4,000 shots) is about 0.002, so 0.01 is a tight absolute bound on systematics. Leakage (leaked states read as 1 repeatedly) and, if correlations are uncentred, the T1/readout bias in ⟨z⟩² could approach 0.005 to 0.01. A few poor qubits among 50 could dominate the pooled value. The control (95% consecutive agreement) should pass at about 97 to 98% repeatability. Moderate chance that some correlation at lag 2, 4 or 6 crosses 0.01.
P(pass): 50

## P3-13
Rationale: The pass needs a finite-size rate of at least 0.05 bits per round at 72,000 rounds. The asymptotic rate is 0.115 at K3 = 1.40 and 0.054 at 1.31. Photonic data showed about 68% of the asymptotic rate at 10⁵ runs, so at 72,000 rounds with 99% confidence the factor might be about 0.55 to 0.65. If hardware K3 is about 1.40 or more, the rate is about 0.065 (pass). At K3 around 1.35 it is borderline, and below that it fails. My K3 expectation is about 1.38 to 1.42 without readout mitigation, which makes this close to even.
P(pass): 50
