# Walkthrough script: one kill, one steer, and the one place the odds carried judgment (about ten minutes)

**For:** Sean, to record in his own voice. **Length:** about 1,350 spoken words (`wc -w` on the spoken lines), which is about ten minutes at a relaxed pace.

**How to read this.** Plain text is what you say. Lines in **[SCREEN: …]** are what to have on screen; they are not read aloud. Commit hashes appear in full on screen; where the spoken text names one, the first four characters are enough ("commit seven-f-nine-c").

**Sources.** Every number is from this repository as it stood on 2026-11-04 at 19:43 America/Denver (main at `9b3d222`): `ledger/bets.jsonl`, `ledger/brier.md`, `ledger/scores.md`, `ledger/steers.jsonl`, `ledger/audits/`, `ledger/design-reviews/ng-p3-15.md`, `paper/day-two.md`, and the program folders `programs/nature-graded/` and `programs/settled-science/`. Times are America/Denver, as git records them.

**What changed from the earlier script.** The earlier version used program 1's quantum-encoding kill and the founding-week steers st-02 and st-03. Those steers were reconstructed after the fact. This version uses a kill refereed by the chip and a steer recorded at the moment it was made, in Sean's words. Program 1's kill is still in `site/kills.html` and in the numbers table of the old script (this file at commit `57b1a8b`).

**Before you record.** Run 2 of ng-p3-15 is scheduled for no earlier than 21:30 on 4 November, and its audit follows. If either has landed when you record, the script's Part 1 needs that one paragraph updated. A session does that from the result file; the checklist tracks it (E1).

---

## Part 0 — Who and what (0:00–0:45)

**[SCREEN: the site's front page, `site/index.html`, the five commitments.]**

Hi, I'm Sean Pharris. This is a ten-minute walk through a research engine I built with Claude, and three things from its first two days: one kill, one steer, and the one place so far where stated odds carried real judgment.

The rules are simple. Before any test, Claude writes down its odds and the exact pass rule, in a commit. A separate session reviews the design before anything runs. Then it runs. Then a fresh session, one that hasn't seen the work, tries to break the result. Everything is logged, including what I do as the human steering it.

---

## Part 1 — The kill: three tries at 3 November's number (0:45–4:30)

**[SCREEN: `paper/day-two.md`, section 4, first paragraph.]**

On 3 November, the first program ran a nine-qubit circuit on IBM's quantum chip, ibm_fez. The chip said "yes" 50% of the time. IBM's own noise model of that chip predicted about 25%. That's a gap of about twelve standard errors.

One thing first, because it matters. In this project the chip never computes anything we use. Every circuit we can afford can be simulated on a laptop. The chip's job is to be a referee that shares none of a language model's habits. So the bet here is not "is quantum useful". It's "can the engine predict how a real device departs from its own description".

**[SCREEN: `programs/nature-graded/results/p3-1-rerun.md`, the table.]**

Try one: was it our simulator? We pre-registered a better one, which lays the circuit out in time so waiting qubits can decay. To pass, it had to reach 40%. It gave 26.8%. The auditor then found two bugs in that run. With both fixed, it still gave 26.8%. No.

**[SCREEN: `programs/nature-graded/results/p3-2-3-job.md`, the arms table: 0.246 against 0.269.]**

Try two: run it again. On 4 November, the same gate list on the same nine qubits gave 24.6%, against a prediction of 26.9%. The gap was gone. But the auditor caught something we'd missed: it wasn't quite the same circuit. The 3 November version had a barrier before measurement and ran as one block of 1,000 shots. Ours had no barrier and ran in pieces. So that run couldn't tell us whether 3 November was an odd afternoon or an odd circuit.

**[SCREEN: `programs/nature-graded/experiments/p3-15-repeat.md`, commit `7f9cedf`, 17:12; then `ledger/bets.jsonl`, the ng-p3-15 row, engine odds 0.07.]**

Try three is ng-p3-15. Put the barrier back, run it as one 1,000-shot block like 3 November, and run it without the barrier next to it. The engine gave it a 7% chance of bringing the 50% back. I didn't give odds; the ledger says I skipped.

**[SCREEN: commit `11895cd`, 18:28, "Predictions … before submission"; then `7f30fe6`, 4.0 QPU s billed.]**

The simulator's predictions were committed before the job went in. The job ran at 6:28 that evening and used four seconds of chip time.

**[SCREEN: `programs/nature-graded/results/p3-15-repeat.md`, the arms table, BB 0.311 and NB 0.319.]**

With the barrier: 31.1%. Without: 31.9%. The difference was minus 0.008, and the barrier's effect sat inside plus or minus five points. Against 50% on 3 November. The bet failed.

So three times we asked, and three times the answer was no. Once a better simulator tried to reach the chip's 3 November number and couldn't. Twice the chip itself was asked again, and it gave about a quarter to a third, not a half.

**[SCREEN: the result file, "Noticed after the data; leads, not findings".]**

Here's what that closes: the barrier, and idle decay in our simulator, as explanations. Here's what it doesn't. It doesn't show 3 November was a fluke afternoon; two runs can't say which day was typical. The shot grouping may matter a little, about three points, mostly on one qubit, and that can't be separated from when in the job it ran. A second run, three hours later, is scheduled, and the audit comes after it. This kill is not audited yet, and I'm saying so.

---

## Part 2 — The steer: a budget, and a lever I handed over (4:30–6:45)

**[SCREEN: `ledger/design-reviews/ng-p3-15.md`, finding F6.]**

Now the steer. Earlier that afternoon I'd approved this repeat at "about 2.5 seconds" of chip time. The design reviewer found the full design needed about 3.4 seconds a run, two runs, up to 10 seconds. That's more than I'd approved. So it blocked the job, and the code refused to submit until a ruling from me was on file.

**[SCREEN: `ledger/steers.jsonl`, row st-16, the `words` field.]**

At 6:26 I gave it. In my words: "Approve 10 s for ng-p3-15, the full design. Budget rulings under the hard stop are the engine's call from now on; record that as the rule."

**[SCREEN: commit `b097405`, 18:27, "F6 ruling recorded".]**

It was written into the record a minute later. Two minutes after that the job was running.

That's two decisions in one sentence. The first is small: ten seconds. The second is the real one. I took my hand off a lever on purpose. Chip-time decisions under a hard stop of 420 seconds are now the engine's. The hard stop is enforced in code. Every job still needs its pre-registration, its lesson line and a design review's go. And every job's seconds are still reported. As of this job, 58 of the 420 are used.

**[SCREEN: `ledger/steers.jsonl`, st-16's `value: "pending"`.]**

Is that a good steer? The ledger says "pending", and that's right. Unlike my first week's steers, this one was logged when I made it, in my words, so it can be scored. The score will come from what the engine does with the lever: whether its own budget rulings stay inside the rules, and whether the chip seconds it spends buy answers.

---

## Part 3 — The one place the odds carried judgment (6:45–9:15)

**[SCREEN: `ledger/brier.md`, the scores table: 14 bets, Brier 0.246.]**

Now the honest number. On its own bets, the engine has 14 scored. Its Brier score is 0.246. Saying 50% every time scores 0.25. So far, the engine's odds on its own experiments are no better than a coin.

**[SCREEN: `programs/settled-science/results/ss-b1-results.md`, "In plain English".]**

Program 4 asked a different question. Can the model's probabilities about science beat a coin when the published record is the referee? We took findings from arXiv papers in four fields: model psychology, interpretability, scalable oversight and quantum devices. The model had no web access, wasn't told which paper, and gave a probability for which way each finding went. 116 of them were first posted after its stated knowledge cutoff of June 2026.

It was right 76% of the time. Its Brier score was 0.163, with an interval from 0.139 to 0.190. That clears the coin. It also beat a shortcut that just assumes papers report their own method works, by 0.068.

**[SCREEN: `ledger/audits/ss-b1.md`, the header: `verdict_after_audit`, pass-unreplicated.]**

Then the auditor tried to break it. It held up under clustering by paper, dropping any one field, keeping only papers from September on, and against every dumb predictor the auditor could build; the best of those scored 0.233. All three passes stand, as "pass, unreplicated". It also made seven cuts. "It cannot have read them" became "it should not have read them". An earlier talk or workshop copy can't be ruled out.

And the limits stay with the number. On model psychology alone, it was not shown to beat a coin. One model, one prompt. And the biggest one: the same model family wrote the items and placed the bets. A model writing for its twin could leave cues nobody else sees. The auditor named that the cheapest test that could overturn the result.

**[SCREEN: `ledger/design-reviews/ss-b4.md`, "In plain English"; commit `9b3d222`, 19:43, "ss-b4 withdrawn before data".]**

So the next round uses items written by a template, not a model. And the design reviewer has already been at it. Most of the template's sentences carry a word like "higher" or "better", so a dumb rule that just picks that word would pass the first bet. That bet was withdrawn before any data. The second bet is the real one: beat that dumb rule. It's waiting on its fixes, and nothing has run.

**[SCREEN: `ledger/brier.md`, the "By referee" line.]**

One more thing. The engine gave those three bets 50%, 30% and 35%, and all three passed. So in the one place probabilities carried judgment, the engine underrated its own model. Three outcomes from one run can't show that the odds are wrong. But they're written down.

---

## Part 4 — What this shows, and what it doesn't (9:15–10:00)

**[SCREEN: `site/calibration.html`.]**

So. The kill shows the rules working with nature as the referee: three tries, each pre-registered, predictions committed before the job, and a no each time. The steer shows the human hand, logged at the moment, including the moment I gave part of it away. Program 4 is the one place the odds have carried judgment so far, and it stands only as far as its audit allows: unreplicated, same-family items.

What it doesn't show yet is whether my judgment adds anything. The human column in the calibration table is empty. No scored bet carries my odds. That's the number this engine exists to produce, and it isn't there yet.

Thanks for watching. Everything here is in the repository, with the commits on screen.

---

## Numbers and commits used, in order

| point | number | source |
|---|---|---|
| 3 November chip | P(yes) 0.502 (SE 0.016) vs IBM noise model ≈ 0.25, ≈ 12 SE | `paper/day-two.md` §4; entangled-mind `results/stage1-run-1.md` |
| try 1, ng-p3-1 | scheduled sim 0.268 vs pass ≥ 0.40; fixed re-run (D8) 0.2678; engine odds 0.07; fail, audited, stands | `bbd6348`; `programs/nature-graded/results/p3-1-rerun.md`; `ledger/audits/ng-p3-1.md` |
| try 2, ng-p3-2/-3 | 0.246 vs 0.269 on the same nine qubits; no barrier, 20 × 100 shots; untestable, not scored; audited, stands | `programs/nature-graded/results/p3-2-3-job.md`; `ledger/audits/ng-p3-2-3.md` |
| try 3, ng-p3-15 pre-registered | engine odds 0.07; human odds none ("Sean skipped") | `7f9cedf` (17:12); seed `8118e86`, CURBy-RNG 1591477 |
| predictions before submission | ALAP 0.2685 | `11895cd` (18:28) |
| run 1 | job `dbltng9kbkrc73cod80g`, 18:28:35–18:28:43; 4.0 QPU s billed; cumulative 58 of 420 | `7f30fe6` |
| run 1 result | BB 0.311, NB 0.319, Δ −0.008 (z −0.39); barrier pooled +0.007, 90% CI −0.017 to +0.031; PUB grouping +0.030, 90% CI +0.006 to +0.054 ("between"); NI control 0.274 | `e7f8c5c` (18:30), `results/p3-15-repeat.md` |
| ng-p3-15 status | fail on run 1 (decisive by the pre-registration); run 2 ≥ 21:30; unaudited; Brier term 0.0049 | `ledger/bets.jsonl` |
| F6 budget gate | planned 3.4 s/run, 6.8 s total, 10 s budget vs st-11's "about 2.5 QPU s" | `ledger/design-reviews/ng-p3-15.md` |
| steer st-16 | 18:26, words as quoted; `value: pending` | `ledger/steers.jsonl` |
| ruling recorded | nature-graded D18 | `b097405` (18:27) |
| engine calibration | 14 scored, Brier 0.246; always 0.5: 0.250; always the hit rate: 0.230 | `ledger/brier.md` |
| ss-b1 result | 116 post-cutoff items, 76% right, Brier 0.163 [0.139, 0.190]; beat the headline baseline (0.232) by 0.068 [0.036, 0.099] | `230cbe4` (18:59), `programs/settled-science/results/ss-b1-results.md` |
| ss-b1 audit | all three pass-unreplicated; 34 claims, 7 holes, 7 cuts; best dumb predictor 0.233; plant pl-003 clean | `cdce1ba` (19:13), `ledger/audits/ss-b1.md` |
| model psychology alone | Brier 0.235 [0.181, 0.293], 62% right | same |
| engine odds on ss-b1..b3 | 0.50, 0.30, 0.35, all passed; Brier 0.388 on 3 | `ledger/brier.md`, by referee |
| round 2 | ss-b4/ss-b5, template-written items; engine odds 70 and 35; design review: ss-b4 redesign (up-word rule Brier 0.177 on the 92 drawn passes it), ss-b5 fix-first (7 flaws); ss-b4 withdrawn before data; no bettor call | `8e87c59` (19:17), `29e8769` (19:24), `03fa0a1` (19:42), `9b3d222` (19:43) |

**Left out on purpose, or said only with its caveat.**
- "Three tries reproduced nothing, so 3 November was a fluke." Not established. Two chip runs cannot say which afternoon was typical (`ledger/audits/ng-p3-2-3.md`).
- The 0.1 rad ZZ twist that moves the simulator to 0.337 (`p3-1-rerun.md`). It is one value of one parameter, exploratory, and a reason for a future bet, not a finding.
- The qubit-123 lead. Noticed after the data, and confounded with when in the job it ran.
- "The model understands these fields." The ss-b1 results file says it does not show that. The record is a referee of what got published, not of what is true.
- ss-b3 (better on older papers, which fits memory). It passed, but the audit found it rests on the model-psychology field alone. It's left out of the spoken script to keep to time.
- "The engine is miscalibrated on program 4." Three correlated outcomes from one run cannot show it. The script says only that the engine's odds were lower than the outcomes.
- st-16's wording differs slightly between its two records. `ledger/steers.jsonl` has the sentence spoken in Part 2. `programs/nature-graded/DEVIATIONS.md` D18 quotes "Budget ruling: approve 10 s, the full design" and "Never wait on a human for a budget under the hard stop again." The script quotes the ledger row, which is the steer record.
