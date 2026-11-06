# Rows handed to the odds elicitors, remap 2026-11-05c

Each fresh context received the template v2 instructions, `ledger/prior.md` at `34d6b1f` verbatim, and exactly one row below (the whole prompt is reproducible from `ledger/prior.md` at that commit plus the row). Nothing else: no earlier odds on the direction, no earlier bet on it, no audit or review notes beyond the parent's one-sentence finding, no human odds, no other follow-up's odds.

### P3-19

Title: Can extra readout error stand in for either error term in the 5 November job?
Assumption at stake: The rotation-type and blur-type terms P3-18 found on h088 and h268 are error in the chip's state, not readout error beyond that job's own 1,000-shot calibration.
Cheapest test (design): Run P3-17's frozen code and bounds (four readout knobs per pair, each qubit's readout error 0 to 3x the job's calibration value) on data/p3-18-raw.json, once ng-p3-17 is scored and audited.
Per pair, test blur given rotation+readout and rotation given blur+readout; parametric bootstrap at 2,000 shots, B = 100 extended to 1,000 if p <= 0.05, as in P3-18.
Models: none: archived chip counts, no model in the loop (rule 12 does not apply) — No model is called; the referee is the archived ibm_fez counts.
Cost: $0, 0 QPU s; laptop <= 6 h: P3-17 states <= 3 laptop hours for one bootstrapped term on 3 pairs, and this bootstraps two terms (blur and rotation) on 3 pairs, so 2 x 3 h = 6 h.
Draft pass rule (the event you give P(pass) for): On the 5 November job (data/p3-18-raw.json), with P3-17's readout knobs (each qubit's readout error allowed from 0 to 3x that job's calibration value, knob e in [-r, +2r]), both the rotation-type term (null from fitted inc9R) and the blur-type term (null from fitted cohR) are still needed, each bootstrap p < 0.01, on at least 2 of the 3 pairs. Untestable if any fit returns a non-finite log-likelihood or a bootstrap does not complete. Scoreable: yes.
What its parent result found (one sentence): Both kinds of error were needed on two of three pairs on 5 November and on all three on 3 November, but neither analysis allowed the chip to misread more than its own check said.
Prior work line (what published work predicts for this test): No prior statement found after WebSearch 'readout error miscalibration mistaken for decoherence two-qubit state tomography superconducting assignment matrix uncertainty' (2026-11-05). Nearest: Aasen et al. 2024 (arXiv 2312.04211, one KIT transmon) find readout error partly coherent in the x and y bases, which per-qubit classical knobs cannot absorb, so both terms should survive: pass. Adds: the readout rival on the second job, the one P3-18 scored.
Its row on each table of prior.md: program = nature-graded; referee = nature; cost tier = free ($0); source = literature; layer = layer 3.

### P3-20

Title: With the chip's two-qubit gates randomly twirled, does the rotation-type term go away?
Assumption at stake: The rotation-type term is coherent error in the two-qubit gate layers that a stochastic (Pauli) noise model cannot represent; if so, Pauli-twirling those layers turns it into blur and a blur-only model then suffices (Hashim et al. 2021).
Cheapest test (design): One ibm_fez job, interleaved: the 39 witness circuits as on 5 November (bare arm), plus the 27 tomography circuits with 2-qubit gate twirling by explicit Pauli frames (20 randomizations x 100 shots per setting, labels and per-shot memory kept; measurement twirling off so the calibration circuits still apply).
P3-18's 16-knob tests, unchanged, on each arm; the bare arm's labels are P3-18's replication, reported not scored.
Models: none: the chip is the referee, no model in the loop (rule 12 does not apply) — No model is called; ibm_fez's counts decide the bet.
Cost: about 36 QPU s, $0 API: shots = 27 x 2,000 (bare) + 27 x 2,000 (twirled) + 12 x 1,000 (calibration) = 120,000; 0.28 ms x 120,000 = 33.6 s + about 2 s per job = about 35.6 s; suggested cap 45 s (P3-18 billed 20.0 s against an estimate of 20.48 s).
Draft pass rule (the event you give P(pass) for): In one ibm_fez job, on at least 2 of the pairs whose bare arm needs the rotation-type term (P3-18's test, bootstrap p < 0.01), the twirled arm does not need it (p >= 0.01 under the same test, same B rule). Untestable if the bare arm needs the rotation term on fewer than 2 pairs, or if the pre-run worlds show the twirled arm cannot detect a surviving rotation of the bare arm's fitted size. Scoreable: yes.
What its parent result found (one sentence): Two chip jobs found a steady kind of error on most entangled pairs, and scrambling the gates on 4 November moved a different circuit, but no settled result has tested scrambling on these pairs.
Prior work line (what published work predicts for this test): Hashim et al. 2021 (arXiv 2010.00215, AQT transmons) found randomized compiling turns coherent into stochastic error, twirled circuits matching a Pauli model to about 10%; Carignan-Dugas et al. 2024 (arXiv 2303.09945, three IBM chips) find the coherent part predominantly ZZ, which two-qubit twirling tailors: pass. Qiskit gate twirling leaves single-qubit coherent error, also in P3-5c's rotation term: mixed. Adds: a twirled-versus-bare nested test on Heron tomography.
Its row on each table of prior.md: program = nature-graded; referee = nature; cost tier = free ($0); source = literature; layer = layer 3.
