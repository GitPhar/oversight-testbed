# Sean's odds for program 3

**Fill this in before any program-3 test is pre-registered.** Each question names one event that a test will settle yes or no. For each, give a number from **0 to 100** for how likely you think the event is: 0 = certainly won't happen, 100 = certainly will (the same one direction as every scale in this project).

How your numbers are used:
- They are scored against the outcomes (Brier score), next to the engine's.
- The two sets of scores are published side by side.
- Here the outcomes are decided by IBM's quantum chip, not by a language model. One exception, Q3, is decided by a calculation. Q3 is the only one the chip doesn't decide, and it is scored separately.

The engine's own numbers are deliberately left off this form, and so is its ranking. Program 1 showed that a number you have just seen pulls the next number you give. The questions are in a shuffled order (seed 20261105) so the order doesn't hint at a ranking either. If you have already read `program-3-map.md` or `odds-elicitation/`, say so in the box below. Your numbers still count, and that fact is recorded with them.

You can dictate the answers. For each one, give a number and, if you have one, a sentence of why. Skip any you have no feel for; a blank is recorded as "no odds", not as 50.

A guide, if it helps: 5 = I'd be amazed. 25 = I doubt it. 50 = coin flip. 75 = I expect it. 95 = I'd be amazed if not.

- Date and time filled in (America/Denver): ______
- Had you seen the engine's odds before filling this in? yes / no / some of them: ______

**Two things that may help.**
1. Quantum theory has never failed a test, so for most of these questions the physics is not in doubt. What is in doubt is whether this particular chip is clean enough to show it.
2. In program 1, the chip's own simulator predicted 0.25 for one circuit and the chip gave 0.50.

---

**Q1 (P3-12). Do quick repeated measurements remember each other?**
- **Test:** On about 50 qubits at once, we measure each qubit eight times in a row, alternating between two incompatible kinds of measurement. Quantum theory says each result forgets the ones before it. One proposal (Hossenfelder, a test of "superdeterminism") says there could be a short memory.
- **Event:** The results show no memory: every correlation is below 0.01. A control run, repeating the *same* measurement, agrees with itself at least 95% of the time.
- **Cost:** about 6 seconds of chip time.

Your odds (0–100): ____ Why: ____

**Q2 (P3-1). Was our simulator just built wrong?**
- **Background:** In program 1, the chip gave 0.50 where its simulator said 0.25. One possible reason is that our simulator let qubits sit idle with no decay at all, because of a missing setting.
- **Test:** We redo the simulation on the laptop with idle decay switched on.
- **Event:** The corrected simulation gives 0.40 or more, which closes most of the gap without touching the chip.
- **Cost:** free.

Your odds: ____ Why: ____

**Q3 (P3-8). A new kind of Wigner's-friend inequality, on paper.**
- **Background:** Experts say that with only *one* "friend", these experiments reduce to an ordinary Bell test. A 2024 theorem suggests that stops being true when the experimenter has three choices instead of two. Nobody has written such an inequality down.
- **Test:** A computer search, on the laptop.
- **Event:** The search finds such an inequality, and quantum theory breaks it by a margin that survives at least 15% noise.
- **Cost:** free. This one is decided by mathematics, not by the chip, so it is scored separately.

Your odds: ____ Why: ____

**Q4 (P3-4). Can a standard noise-cancelling trick bring back lost entanglement?**
- **Background:** In program 1, the chip held about half the entanglement its simulator predicted.
- **Test:** We rerun one of those measurements with "dynamical decoupling" (pulses that protect idle qubits) switched on and off.
- **Event:** Decoupling recovers at least half of the missing entanglement.
- **Cost:** about 9 seconds.

Your odds: ____ Why: ____

**Q5 (P3-9). Does the contextuality analysis from program 1 work where physics says it must?**
- **Background:** Program 1 used a method called Contextuality-by-Default on the model's ratings and found nothing. Here we point the same method at the chip, running a textbook contextuality experiment (the Peres–Mermin square), measuring one thing after another.
- **Event:** The method says "contextual" for both starting states, even after it subtracts the disturbance each measurement causes to the next.
- **Cost:** about 42 seconds.

Your odds: ____ Why: ____

**Q6 (P3-6). Does one qubit "hear" the settings on its neighbour?**
- **Background:** On older IBM chips, a qubit's results shifted slightly depending on what was done to a different qubit. Nobody knows why. A newer chip of our type (ibm_kingston) was clean. Ours, ibm_fez, has never been checked.
- **Event:** ibm_fez is clean: no qubit pair shows a shift beyond the statistical threshold.
- **Cost:** about 13 seconds.

Your odds: ____ Why: ____

**Q7 (P3-5). Do the chip's errors steer the qubits, or just blur them? (old data)**
- **Background:** We already hold the detailed state measurements from program 1's entanglement test.
- **Test:** We fit two explanations to those data, each with the same number of adjustable knobs. One is "steering" errors (the chip systematically rotates the state a little). The other is "blurring" errors (random noise).
- **Event:** Steering fits clearly better on at least 2 of the 3 items.
- **Cost:** free.

Your odds: ____ Why: ____

**Q8 (P3-7). Wigner's friend on the chip, the strong version.**
- **Background:** A "friend" is a small group of qubits that records a measurement, and is later un-recorded. Quantum theory predicts a violation of a "genuine" local-friendliness inequality, one that is stronger than an ordinary Bell test. That would mean that what the friend observed cannot be an absolute fact for everyone (given locality and free choice). It has been shown with photons, but never on any quantum computer. The settings come from a public randomness source, not from the chip.
- **Event:** The violation shows up clearly (5 standard errors) with a friend of at least 1 qubit, and all the safety checks pass.
- **Cost:** about 37 seconds.

Your odds: ____ Why: ____

**Q9 (P3-2). Are the chip's errors "steering" errors that scrambling removes?**
- **Test:** We rerun the program 1 circuit with "twirling" on and off. Twirling randomly scrambles the gates so that systematic errors turn into random ones.
- **Event:** Twirling moves the chip's answer at least halfway back toward what the simulator predicted.
- **Cost:** about 6 seconds.

Your odds: ____ Why: ____

**Q10 (P3-10). The simplest contextuality check for the program 1 method.**
- **Test:** A four-measurement version of Q5, small enough that the method's verdict is exactly right in theory.
- **Event:** It says "contextual" clearly (99.9% confidence) in both measurement orders.
- **Cost:** about 15 seconds.

Your odds: ____ Why: ____

**Q11 (P3-14). Is the quantum state "real", or just our knowledge?**
- **Background:** One family of theories says a quantum state is only partial knowledge about some hidden real state. In those theories, two quantum states overlap entirely because the hidden states overlap. Photon experiments ruled out the strongest such theories, but only by assuming the detectors miss photons fairly. A chip has no missed detections.
- **Event:** The chip rules them out clearly (a 5-standard-error margin) without that assumption.
- **Cost:** about 21 seconds.

Your odds: ____ Why: ____

**Q12 (P3-11). Does a single qubit fail the "common-sense realism" test, fairly?**
- **Background:** The Leggett–Garg test asks whether a qubit has a definite value even between looks, and whether looking can be harmless. Earlier IBM tests could not rule out that the looking itself caused the effect ("clumsiness").
- **Test:** We add a pre-registered clumsiness check and the program 1 disturbance correction.
- **Event:** The qubit still fails the realism test clearly, by more than clumsiness could explain.
- **Cost:** about 29 seconds.

Your odds: ____ Why: ____

**Q13 (P3-13). Can that same qubit certify random numbers?**
- **Test:** Using the data from Q12, a published formula turns a strong enough realism violation into "certified" random bits.
- **Event:** The data certify at least 0.05 random bits per run after a strict small-sample correction.
- **Cost:** free on top of Q12.

Your odds: ____ Why: ____

**Q14 (P3-3). Is the program 1 surprise about the chip, or about nine particular qubits on one afternoon?**
- **Test:** We rerun the program 1 circuit on two other sets of nine qubits, chosen in advance, and repeat it hours apart.
- **Event:** On both other sets, the chip agrees with its simulator at least twice as well as on the original set.
- **Cost:** about 6 seconds.

Your odds: ____ Why: ____

---

**Optional, one line each:**
- **Which test would you cut first, and why?** ____
- **Is there a question about the chip, or about reality, that you'd add?** ____

---

*For the session recording this form:*
1. Commit this file unchanged, with the time, to `oversight-testbed/ledger/human-odds/program-3-<date>.md`, before any program-3 pre-registration.
2. Copy each number, divided by 100, into the matching bet's `human_odds`.
3. Q3 (P3-8) goes to the ledger with `referee: mathematics` and is reported apart from the nature-graded column.
