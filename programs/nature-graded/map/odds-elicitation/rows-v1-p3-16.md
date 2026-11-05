# Direction row for odds elicitation: P3-16 (template v1, single row)

Written 2026-11-04 by the program-3 session, before any P3-16 data. The elicitor sees only this file.

## P3-16. Does 3 November's result come back when the circuit runs alone in its own job?

- **Assumption at stake:** that program 1's large chip-versus-simulator gap on 3 November was a property of the chip that afternoon, and not of the job it ran in: a single circuit, alone, as the only item in its job.
- **What our data say:**
  - 3 November (program 1): a 9-qubit, 117-CZ circuit on ibm_fez qubits 117, 123, 124, 125, 136, 141, 142, 143, 144. It had a barrier across all nine qubits just before the measurements and ran as one block of 1,000 shots, the only circuit in its job. P(yes) = 0.502 ± 0.016. The device's noise model predicted about 0.25–0.27.
  - 4 November, wave 1: the same gates on the same qubits without the barrier, as 20 pieces of 100 shots interleaved with other circuits in a 200-item job. P(yes) = 0.246 ± 0.008, against a prediction of 0.269.
  - 4 November, P3-15: two jobs 3 hours apart, each holding 32 items: {barrier, no barrier} × {one 1,000-shot block, 10 × 100-shot pieces}, plus readout checks. The barrier 1,000-shot block read 0.311 and 0.282, the no-barrier block 0.319 and 0.311, and the 100-shot pieces 0.27–0.31. Prediction 0.27. So neither the barrier nor block-versus-pieces brought back 0.50. In both jobs IBM's server ran the two 1,000-shot blocks together, in one execution span, before everything else, even when the submitted order put them last.
  - Between the two P3-15 jobs, individual qubits' P(1) moved by up to about 0.2 while P(yes) moved by at most 0.03. IBM's published per-qubit calibration had not been re-measured since 12:04 that day.
  - The one 3 November feature no 4 November job reproduced is that the circuit ran alone in its own job.
- **Cheapest test:** three jobs, submitted back to back in a seeded order, on the same nine qubits, 1,000 shots per circuit: (A) the barrier circuit alone in its own job (3 November exactly); (B) the no-barrier circuit alone in its own job; (C) both circuits as two items in one job (the P3-15 condition). About 7.1 QPU s in total (0.28 ms per shot plus about 2 s per job).
- **Draft pass rule (the event):** job A gives P(yes) ≥ 0.40, **and** it exceeds the barrier circuit in job C by at least 0.10 at z ≥ 3.
