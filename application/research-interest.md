# Research interest — answer for the form field "What research would you most like to work on, and why?"

> **About this text.** Anthropic's candidate AI guidance (anthropic.com/candidate-ai-guidance) says of written application answers: "Please create your first draft yourself, then use Claude to refine it." This text was drafted by Claude. The form's "AI Policy for Application" box asks the applicant to confirm they have read that guidance. The route this folder plans for (`checklist.md`, S6) is that Sean writes his own first draft of this answer and uses this file to check numbers and wording.
>
> Every number is from this repository as of 2026-11-05 (main at `7bfc24e`; numbers brought current by the review session): program 1 in `programs/entangled-mind/` (original repository `GitPhar/entangled-mind`, kept as the historical record), program 4 in `programs/settled-science/`, and `ledger/`. The wording follows the audits' cuts. It avoids mechanism words such as "consistency is memory", which the program 1 audit found the data cannot carry, and "cannot have read them", which the ss-b1 audit cut.
>
> **Mentors are named only where a result touches their work.** Jack Lindsey: introspection (our self-knowledge null). Samuel Marks: truth probes (Marks & Tegmark 2023, the probe our direction 5 used). Belinda Li: what language models represent (the same probe result). The answer names Model Psychology and Model Internals as the areas.

---

I want to work on one question: when a model tells an overseer what it believes, how far can the overseer trust it? It sits where Model Psychology and Model Internals meet.

My first program tried to predict a model's errors by encoding its competing claims as an entangled quantum state. Pre-registered tests on two Claude models killed it: the quantum encoding tied a matched classical twin (AUROC 0.83 vs 0.84). The model's own stated confidence did as well as anything I built.

So I measured that confidence. In Haiku, changing which questions came first moved its 0–100 rating across a median span of 24.7 points, against 13.2 from repeat noise. With its earlier answers edited out of the transcript, order still moved it, by an amount the data cannot pin down well (ratio of hidden to shown effect 1.23, with a 95% range of 0.75 to 2.02, 40 items). Haiku needed a separate confidence for each of six ways of asking on 86% of claims; on Opus one shared answer predicted every format (94% of each held-out format), though a guesser that only knew Opus's yes/no verdict came close (88%), so what Opus shares across formats is a verdict more than a graded belief. On all three models, hiding the model's earlier answer made it repeat that answer far less often. So the format effect narrows with scale, and the transcript effect does not.

Model Psychology. No model showed a detectable advantage at judging its own errors, on three models. That touches Jack Lindsey's finding that introspective access is real but narrow. I want to know what a stated credence is a readout of, and how that changes with scale.

Model Internals. On Llama-3-8B, a Marks–Tegmark-style truth probe moved with question order more than the stated rating did, but not in step with it; with only three gate items, the "not in step" half is undetermined. Whether an internal representation holds still while the words move is where Samuel Marks's probes and Belinda Li's work on what models represent meet my result. I want to test it properly.

The second thread is method. I ran all of this as a scored oversight system. The engine's odds on its own 21 scored bets are no better than a coin (Brier 0.220, against 0.250 for always saying 50% and 0.222 for guessing the pass rate). In one place, stated probabilities did carry judgment: on 116 findings published after its stated knowledge cutoff, the model's probabilities about which way each went scored Brier 0.163 [0.139, 0.190]. They beat a publication-bias shortcut too. The audit let that stand as unreplicated, with the item-writer from the same model family still open, and a one-line "which version flatters the paper" rule scored 90% to the bettor's 93% on the harder round.

My background is psychology, philosophy and four years leading AI pipeline engineering, not ML research. The record of what I killed, and why, is my evidence.

---

*Word count of the answer (between the rules): about 430 after the 2026-11-05 corrections, by `wc -w`; trim to 400 when Sean redrafts it.*

## Where each claim comes from

| claim | source |
|---|---|
| A2 0.83 vs F2 0.84, locked test | entangled-mind `49dd6f7`, `results/v2-run-1.md` |
| stated confidence G 0.83 (Haiku), 0.91 (Sonnet), level with the best structural model | `db2eb02` (Addendum D, pre-registered `f7afd8a`) |
| median span 24.7 points vs 13.2 from noise | `results/exp5-run-1.md` line 186, `75744dc` |
| R = 1.23 [0.75, 2.02], 40 items | `758609a` (D45), `results/gm2b-self-conditioning-40.md` |
| six formats, 86% of 160 claims, Haiku | `1fd521d` (D38) |
| Opus F′ Q = 0.94 [0.90, 0.97], 68 claims; yes/no-verdict predictor Q 0.88, so "verdict" not "credence" | `a8be4b5` (D49), narrowing D50 `9cefab6`; `ledger/audits/em-dm2-opus.md` |
| no self-advantage on three models | `bc0f125` (D36, Haiku −0.055 [−0.103, −0.007]); `ba9f99c` (DM3, Sonnet × Opus, not detected); ledger rows em-gm1, em-dm3 |
| Lindsey: introspective access real but narrow (about 20%) | `related-work/self-evaluation-goodhart-introspection.md` (Lindsey 2025, Transformer Circuits Thread); `proposal.md`, related work |
| probe moves with order more than the rating, not in step; three gate items, one non-tracking (h191); verdict mixed, scored 0 | ledger row em-gm5; `ledger/audits/probe-dissociation-dp2.md` (DP2 verified DP1; verdict stands) |
| probe built after Marks & Tegmark 2023 | `CONTEXT.md` §1; `application/research-proposal.md`, mentor fit |
| 21 scored bets, Brier 0.220 (always 0.5: 0.250; hindsight base rate 0.222) | `ledger/brier.md` |
| 116 post-cutoff findings, Brier 0.163 [0.139, 0.190]; beat the headline baseline by 0.068 [0.036, 0.099] | `programs/settled-science/results/ss-b1-results.md` (`230cbe4`, cuts applied `a585a88`) |
| pass-unreplicated; same-family writer open; flattery rule 90% vs 93% | `ledger/audits/ss-b1.md` (`cdce1ba`); `programs/settled-science/results/ss-b6-results.md` |
| background | `CONTEXT.md` §1 |

## Not used, on purpose

- **Scalable Oversight as a named area.** The answer names Model Psychology and Model Internals. Samuel Marks appears where the probe result touches his truth-probe work.
- "There is no stored credence to read out" (proposal.md). This holds for Haiku and is contradicted on Opus (D50).
- "Eleven pre-registered tests overnight." Five of them re-analysed data that had already been opened (D54, D54a).
- "The probe is unverified." That was true at 14:39 (D53). DP2 has since verified the probe run, with the verdict mixed. The answer says what DP2 found.
- The audit counts from program 1 (0 of 39 verdicts reversed, 166 of 560 claims failed). They are still true, but the ledger now has a wider view: 43 of 53 bets audited, 4 verdicts reversed (`ledger/brier.md`). Neither fits in 400 words alongside program 4.
- **"The model's confidence was too low."** The ss-b1 audit cut it to an exploratory reading; its interval touches zero.
- **The model-psychology field in program 4** (not shown to beat a coin, Brier 0.235 [0.181, 0.293] on 29 items). It touches Model Psychology directly, but it is a descriptive split of one run.
- The stage-by-stage quantum readout (0.63 → 0.49 against 0.68). It is exploratory, not pre-registered.
