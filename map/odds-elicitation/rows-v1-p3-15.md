# Direction row for odds elicitation: P3-15 (template v1, single row)

Written 2026-11-04 by the program-3 session, before any P3-15 data. The elicitor sees only this file.

## P3-15. What made 3 November different: the afternoon, or the circuit's barrier and shot grouping?

- **Assumption at stake:** that program 1's large chip-versus-simulator gap on 3 November was a property of the chip that afternoon (drift), and not of how that run's circuit was built or grouped.
- **What our data say:**
  - 3 November (program 1): a 9-qubit, 117-CZ circuit on ibm_fez qubits 117, 123, 124, 125, 136, 141, 142, 143, 144. It had a barrier across all nine qubits just before the measurements and ran as one block of 1,000 shots in a job of its own. P(yes) = 0.502 ± 0.016. The device's own noise model predicted about 0.25–0.27.
  - 4 November (wave 1, P3-2/P3-3): the same gate list on the same nine qubits, but **without** the pre-measurement barrier (the archive had dropped it), run as 20 pieces of 100 shots interleaved with other circuits in one job. P(yes) = 0.246 ± 0.008, against a prediction of 0.269 from that afternoon's calibration. Qubit 125 still read 0.14 below the simulator; the other eight were within about 0.05.
  - In Qiskit's own schedulers: with ALAP scheduling, all nine measurements happen at the same time (8.05 µs) with or without the barrier. With ASAP scheduling, removing the barrier lets qubits be measured early (from 3.3 µs). How IBM's servers schedule a submitted circuit is not documented in anything we have read.
  - A laptop re-simulation with idle decay switched on changed the predicted P(yes) by about 0.000 (P3-1), so in the noise model, idle time alone does not move this circuit's answer.
- **Cheapest test:** one job now on the same nine qubits, with four arms: {barrier, no barrier} × {one 1,000-shot block, 10 × 100-shot pieces interleaved}, plus readout calibration (all-0, all-1). An identical second job at least 3 hours later. About 3.4 QPU s per job.
- **Draft pass rule (the event):** in the first job, the 3 November configuration (barrier, one 1,000-shot block) gives P(yes) ≥ 0.40, **and** it exceeds the no-barrier 1,000-shot block in the same job by at least 0.10 at z ≥ 3.
