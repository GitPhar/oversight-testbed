# Research interest — answer for the form field "What research would you most like to work on, and why?"

> **Read this before using it.** Anthropic's candidate AI guidance (anthropic.com/candidate-ai-guidance) says of written application answers: "Please create your first draft yourself, then use Claude to refine it." This text was drafted by Claude at your request. You will have to tick the form's "AI Policy for Application" box. So the safe way to use this file is as a fact sheet: write your own first draft, then check it against the numbers and wording below. Don't paste this in. The decision is yours; see `checklist.md`, item H3.
>
> Every number is from program 1 (`programs/entangled-mind/` in this repository; original repository `GitPhar/entangled-mind`, kept as the historical record) (`paper/record.md`, `results/`, `audits/SUMMARY.md`) or this repository (`ledger/brier.md`). The wording follows the audit's cuts (D51). It avoids mechanism words such as "consistency is memory" and "treats its answers as commitments", which the audit found the data cannot carry.

---

I want to work on one question: when a model tells an overseer what it believes, how far can the overseer trust it? It sits where Model Psychology, Model Internals and Scalable Oversight meet.

My first program set out to predict a model's errors by encoding its competing claims as an entangled quantum state. Pre-registered tests on two Claude models killed it. The learned quantum encoding tied a matched classical twin (AUROC 0.83 vs 0.84). Its one apparent edge, on Sonnet, was matched by a classical model. The model's own stated confidence did as well as anything I built.

So I measured that confidence directly. It did not hold still. In Haiku, changing which questions came before the main one, and in what order, moved its mean 0–100 rating across a median span of 24.7 points, against 13.2 from repeat noise. With its earlier answers edited out of the transcript, order still moved the final rating about as much (ratio 1.23 [0.75, 2.02], 40 items), and it repeated its first answer within 5 points 36% of the time instead of 86%. A number presented as its own earlier answer pulled its next rating. The same number presented as another person's did not. Across six answer formats, Haiku needed format-specific credences for 86% of claims. Opus did not: one credence predicted 94% of each held-out format's reproducible answer. No model showed a detectable advantage at judging its own errors.

Model Psychology: what is a stated credence a readout of, and how does that change with scale? Model Internals: does an internal truth representation hold still while the words move? My first probe on Llama-3-8B is unverified (its test step replayed its selection data); I want to do it properly. Scalable Oversight: calibration and honesty evaluations assume a stated number reads out a stored belief. If the transcript builds part of it, they partly measure the conversation.

The second thread is method. I ran this as a scored oversight system. Where Claude stated odds before data, they were no better than a coin (Brier 0.256, five bets). An independent audit session reversed none of 39 verdicts but failed 166 of 560 checked claims, mostly in prose. I want AI-driven research to be auditable like this.

My background is psychology, philosophy and four years leading AI pipeline engineering, not ML research. The record of what I killed, and why, is my evidence.

---

*Word count of the answer (between the rules): 399, by `wc -w`.*

## Where each claim comes from

| claim | source |
|---|---|
| A2 0.83 vs F2 0.84, locked test | entangled-mind `49dd6f7`, `results/v2-run-1.md` |
| Sonnet edge matched by F2+ (0.90 = 0.90); stated confidence G 0.83 (Haiku), 0.91 (Sonnet) | `db2eb02` (Addendum D, pre-registered `f7afd8a`) |
| median span 24.7 points vs 13.2 from noise | `results/exp5-run-1.md` line 186, `75744dc` |
| R = 1.23 [0.75, 2.02], 40 items; within-5 agreement 86% shown vs 36% hidden | `758609a` (D45), `results/gm2b-self-conditioning-40.md` |
| own vs another person's number | bm1 `e806ea4` (+0.37 [+0.17, +0.57]); at three distances `e2c3b90` (D47; own − other +0.46 [+0.21, +0.84]) |
| six formats, 86% of 160 claims, Haiku | `1fd521d` (D38) |
| Opus F′ Q = 0.94 [0.90, 0.97], 68 claims | `a8be4b5` (D49), narrowing D50 `9cefab6` |
| no self-advantage on three models | `bc0f125` (D36, −0.055 [−0.103, −0.007]); `ba9f99c` (DM3, Sonnet × Opus, not detected) |
| probe unverified, 500 of 500 replayed | `2161329` (D53) |
| Brier 0.256, five bets | this repo, `ledger/brier.md` |
| 0 of 39 reversed; 166 of 560 claims failed | entangled-mind `b009a15`, `audits/SUMMARY.md` |
| background | `CONTEXT.md` §1 |

## Not used, on purpose

- "There is no stored credence to read out" (proposal.md). This holds for Haiku and is contradicted on Opus (D50).
- "Eleven pre-registered tests overnight." Five of them re-analysed data that had already been opened (D54, D54a). The audit counts about four independent data collections.
- The stage-by-stage readout (0.63 → 0.49 against 0.68). It is exploratory, not pre-registered.
