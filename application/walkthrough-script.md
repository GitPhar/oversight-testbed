# Walkthrough script: one kill, one steer (about ten minutes)

**For:** Sean, to record in his own voice. **Length:** about 1,400 spoken words, which is about ten minutes at a relaxed pace.

**How to read this.** Plain text is what you say. Lines in **[SCREEN: …]** are what to have on screen; they are not read aloud. Commit hashes appear in full on screen. When the script shows one in the spoken text, reading out the first four characters is enough ("commit four-nine-d-d").

**Sources.** Every number is from entangled-mind `paper/record.md`, `results/`, `DEVIATIONS.md` and `audits/SUMMARY.md`, or from this repository's `ledger/`. Times are America/Denver, as git records them.

**Before you record.** Check the two **[SEAN: …]** notes in Part 2. They mark places where only your memory can confirm the record.

---

## Part 0 — Who and what (0:00–0:45)

**[SCREEN: the site's front page, `site/index.html`, showing the five commitments.]**

Hi, I'm Sean Pharris. This is a ten-minute walk through two moments from the first week of a research project I ran with Claude.

The project has a simple rule. Before any test, Claude writes down its odds and the exact pass rule, in a commit. Then it runs the test. Then a separate session, one that hasn't seen the work, tries to break the result. Everything is logged, including what I do as the human steering it.

I'll show you one kill and one steer. The kill is my own starting idea. The steer is the moment the project turned toward the thing that turned out to be interesting.

---

## Part 1 — The kill: the quantum encoding (0:45–5:00)

**[SCREEN: entangled-mind `paper/record.md`, top of the November 3 table.]**

The idea was mine, from October 25th. When a language model reasons, it holds competing claims: "it's probably this, but maybe that." My idea was to encode those claims as qubits, with entangling gates between claims that contradict each other. If the model is torn, the entangled state should show it, and that should flag the model's wrong answers better than ordinary methods.

**[SCREEN: commit `afe1c1b`, 2026-11-03 12:54, the pre-registration.]**

On November 3rd at 12:54 we pre-registered five hypotheses. The main one, H2, said the entangled readout would detect the model's errors better than the controls.

**[SCREEN: `results/stage2-run-2.md`, commit `3204d10`, 15:14.]**

The first real test came at 3:14 that afternoon, on 80 hard test questions. AUROC is a score where 0.5 is a coin flip and 1 is perfect. The entangled arm scored 0.55. The same circuit with no entangling gates scored 0.68. A shuffled web of relations scored 0.65, and just counting contradictions scored 0.64. All three controls scored higher on point estimate. H2 failed.

**[SCREEN: commit `655a8f8`, the witness result: negativity 0.147, 0.063, 0.067.]**

Here's the part I want to be careful about. We ran the circuit on real IBM quantum hardware, a machine called ibm_fez, and certified that the states really were entangled, on three of three items. That took 44 seconds of hardware time, plus 2 seconds for the first run. So the entanglement was real. It just didn't help.

**[SCREEN: `results/v2-run-1.md`, commit `49dd6f7`, 18:50.]**

So we gave the quantum version every chance. Version two let the quantum model learn its own settings from training data, and we built a classical twin with the same number of parameters. On a locked test set of 209 questions, the quantum model scored 0.83 and the classical twin 0.84. The difference was minus 0.007, with an interval from minus 0.079 to plus 0.062. A tie. And the telling part: the strengths it learned for the entangling links came out small, 0.12 and 0.21 where version one used 1. Given the choice, the model turned its own entanglement almost off.

**[SCREEN: commit `b584386`, 20:58: A2 0.90, F2 0.82, +0.078 [+0.018, +0.137].]**

Then, at 8:58 that night, came the moment that could have fooled us. On a second model, Claude Sonnet, the quantum model beat its twin: 0.90 against 0.82. The difference was plus 0.078, with an interval from plus 0.018 to plus 0.137, which excludes zero. On its face, that's a quantum win.

**[SCREEN: commit `f7afd8a`, 21:03, "Pre-register the coupling ablation … before scoring".]**

Five minutes later, before anyone looked further, we pre-registered a test to explain it. That's commit f-7-a-f. If the edge came from entanglement, setting the links to zero should destroy it. And a classical model given the same per-claim readout should fall behind.

**[SCREEN: commit `db2eb02`, 21:30.]**

At 9:30 the answer came back. Setting the links to zero changed the score by minus 0.006, which is nothing. The classical model with the same readout scored 0.90, level with the quantum one. So the edge came from how each single claim was read out, and a classical model does that just as well. The same check on the first model's held-out edges, at 9:50, commit a-9-a-b, gave the same answer.

**[SCREEN: `db2eb02` again, the arm G line: 0.91.]**

There's one more number here, and it mattered later. Simply asking the model how confident it was scored 0.83 on Haiku and 0.91 on Sonnet. That's as good as anything we built.

**[SCREEN: `site/kills.html`, the quantum-encoding entry and its diagnosis.]**

So the hypothesis is closed, and the diagnosis stays on the map: the entanglement is physically real, and it does no work on this task. The project's rules now say never to revive this encoding. Next to that rule sits another one: never lower a pre-registered bar after seeing data. Without that second rule, the Sonnet result at 8:58 would have been the headline.

---

## Part 2 — The steer: the pivot to sequential judgment (5:00–9:15)

**[SCREEN: `ledger/steers.jsonl`, entries st-02 and st-03.]**

Now the steer. Being honest about this part matters, so first, how it was recorded. In that first week my steers weren't logged when I made them. They were reconstructed afterwards from the session. Their times are approximate, and none of them is scored.

**[SEAN: confirm from memory that you said the st-02 sentence before 19:21 on November 3rd. The ledger has no time for it.]**

Some time that day, as the quantum results kept failing, I set a rule. The ledger doesn't have the time. The rule was: "Never lower the bar. Don't stumble into a quantum win. Find where quantum would have to win, and test it there."

**[SCREEN: commit `851040f`, 19:21, `paper/next-steps.md`, section 2, "Why the project pivots to sequential judgment".]**

Thirty-one minutes after the version-two tie, Claude wrote the pivot down, in commit eight-five-one-oh. The argument was this. The evidence for quantum models of human thinking was never about classifying one judgment. It's about what one judgment does to the next: question-order effects, like Wang and Busemeyer's surveys, and a choice changing later confidence, like Kvam and colleagues in 2015. If quantum structure is going to show up anywhere, it's in sequences. And the document wrote down, before any data, what each outcome would mean.

**[SCREEN: experiment 3 row in the record: 85% of items same answer in all 5 runs; 27 of 218 pairs differ.]**

There was a measurement lesson too. Yes-or-no questions don't move this model: on 85% of items it gave the same answer in all five runs. So the new tests used 0-to-100 ratings.

**[SCREEN: commit `2c2ef6c` (20:15, frozen) and commit `75744dc` (22:24, result).]**

Experiment 5 was frozen at 8:15 that night: 40 questions, each a chain of ratings in twelve different orders and arrangements. It came in at 10:24, after 12,600 conversations and $1.93. On the quantum question, the answer was no again. There was no quantum signature, and a plain classical chain did just as well. It was issued as a tie. The independent audit the next day re-issued it, under its own frozen rule, as classical. That's commit oh-seven-seven-f.

**[SCREEN: `results/exp5-run-1.md`, line 186.]**

But look at what the sequences showed. Which questions came first, and in what order, moved the model's main rating across a median span of 24.7 points. Repeat noise alone gives about 13. 60 of 80 claim-question pairs showed an order effect, against about 27 expected by chance, and 40 survive a strict correction. The quantum account failed, and the order effects were real.

**[SCREEN: commit `bffc4ab`, 23:14.]**

That same night we caught our own artefact. A near-zero quantum signature, which looked like a near-miss for the quantum account, came from pooling two directions of the rating scale. On one scale direction, it disappears. The order effects survive, on 12 of 16 pairs.

**[SEAN: confirm that the "keep pushing, where's the gold, broaden" steer came after experiment 5's result at 22:24 and before the gold map at 23:11.]**

**[SCREEN: commit `eae3975`, 23:11, `paper/gold-map.md`, the ranking table.]**

That's when I gave the second steer: "Keep pushing. Where's the gold? Broaden to adjacent research." At 11:11 that night Claude produced the gold map: eleven directions, each with the assumption at stake, the cheapest test, its cost, and a stated probability.

**[SCREEN: commit `758609a`, `results/gm2b-self-conditioning-40.md`.]**

One of them was direction 2: is the order effect caused by the question, or by the model seeing its own earlier answers? We tested it by editing the transcript to hide those answers. On all 40 items, hiding them left the order effect about the same size. The ratio was 1.23, with an interval from 0.75 to 2.02. With its first answer visible, the model repeated it within 5 points 86% of the time. With it hidden, 36%. The first ten items had suggested a bigger ratio, 1.91. The 40-item replication corrected that, and we wrote the correction down.

**[SCREEN: commit `a8be4b5`, Opus F′ Q = 0.94 [0.90, 0.97].]**

And to be fair to the other side: on Haiku, six ways of asking needed six different credences for 86% of claims. Opus held one usable credence across formats. It predicted 94% of each held-out format. So this narrows as models get stronger, and the paper now says so.

**[SCREEN: `ledger/brier.md`, the scored-bets table.]**

Before data, the engine gave direction 2 a 25% chance and direction 3 a 25% chance. Both hit. That's one reason the engine's calibration so far is no better than a coin, on five bets.

---

## Part 3 — What this shows, and what it doesn't (9:15–10:00)

**[SCREEN: `site/calibration.html`.]**

So, one kill and one steer. The kill shows the rules working: a tempting result got a pre-registered test before anyone celebrated it. The steer shows the human hand. I can't prove the steer helped. There's no counterfactual, it wasn't logged when I made it, and the "helped" in the ledger is a Claude session's judgment, not a score. That's exactly why, from the next program on, my own odds go down before the data, separately from Claude's, and get scored the same way.

Thanks for watching. Everything here is in the repositories, with the commits on screen.

---

## Numbers and commits used, in order

| point | number | commit |
|---|---|---|
| pre-registration, H1–H5 | — | `afe1c1b` (11-03 12:54) |
| H2 fails | A 0.55, C 0.68, D 0.65, E 0.64 | `3204d10` (15:14) |
| hardware | Stage 1, 2 QPU s; witness 3/3, N = 0.147, 0.063, 0.067, 44 QPU s | `98d6ac6` (16:07), `655a8f8` (16:08) |
| v2 tie | A2 0.83 vs F2 0.84; −0.007 [−0.079, +0.062]; k 0.12, 0.21 | `49dd6f7` (18:50) |
| Sonnet edge | A2 0.90 vs F2 0.82; +0.078 [+0.018, +0.137] | `b584386` (20:58) |
| ablation pre-registered | — | `f7afd8a` (21:03) |
| ablation result | κ = 0: −0.006 [−0.029, +0.013]; F2+ 0.90; G 0.91 | `db2eb02` (21:30) |
| Haiku held-out edges | F2+ − A2 −0.019 | `a9ab42c` (21:50) |
| pivot written | — | `851040f` (19:21) |
| exp 3 saturation | 85% same in 5/5; 27 of 218 pairs differ | `3241667` (18:10) |
| exp 5 frozen / result | 12,600 conversations, $1.93; 60/80 pairs, ~27 by chance, 40 Holm; span 24.7 vs 13.2 | `2c2ef6c` (20:15), `75744dc` (22:24) |
| one-scale rerun | q −0.146 [−0.439, +0.137]; 12 of 16 pairs | `bffc4ab` (23:14) |
| exp 5 re-issued classical | anchor (a) q −0.345 [−0.517, −0.181] | `077f42e` (11-04 13:18) |
| gold map | 11 directions | `eae3975` (23:11) |
| direction 2, 40 items | R 1.23 [0.75, 2.02]; 86% vs 36%; first 10 items 1.91 | `758609a` (11-04 09:18); first 10 `4c5c34f` |
| Opus format arm | F′ Q 0.94 [0.90, 0.97], 68 claims | `a8be4b5` |
| engine odds | directions 2 and 3 at 0.25, both hit; Brier 0.256, n = 5 | `ledger/brier.md` |

**Left out on purpose.**
- The stage-by-stage readout (0.63 → 0.49 against 0.68). It is a striking picture, but it is exploratory and was not pre-registered. If you show it, say so.
- The phrase "consistency is memory". The audit flags it as a mechanism claim; the script says what was measured instead.
