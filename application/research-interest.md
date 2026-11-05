# Research interest — answer for the form field "What research would you most like to work on, and why?"

> **About this text.** Anthropic's candidate AI guidance (anthropic.com/candidate-ai-guidance) says of written application answers: "Please create your first draft yourself, then use Claude to refine it." This text was drafted by Claude. The form's "AI Policy for Application" box asks the applicant to confirm they have read that guidance. The route this folder plans for (`checklist.md`, S6) is that Sean writes his own first draft of this answer and uses this file to check numbers and wording.
>
> Every number is from this repository as of the end of 5 November 2026 (`main` at `078e0bc`): program 1 in `programs/entangled-mind/`, program 4 in `programs/settled-science/`, and `ledger/`. The ledger numbers (scored bets, the Brier scores, the human column, the plants) are placeholders filled by `python3 site/numbers.py` from the generated ledger pages, so they cannot drift from the ledger; the rest are fixed results with their commits in the table below. The wording follows the audits' cuts and the panel review's Part 5 (`../paper/review-anthropic.md`): it says only what the record supports. It avoids mechanism words such as "consistency is memory", which the program 1 audit found the data cannot carry, and "cannot have read them", which the ss-b1 audit cut.
>
> **Mentors are named only where a result touches their work.** Jack Lindsey: introspection (our self-knowledge null). Samuel Marks: truth probes (Marks & Tegmark 2023, the probe our direction 5 used). Belinda Li: what language models represent (the same probe result). The answer names Model Psychology and Model Internals as the areas.
>
> **Reading level.** Every technical term is explained the first time it is used, in the sentence itself, so a panel member outside the sub-field can follow it.

---

I want to work on one question: when a model tells an overseer what it believes, how far can the overseer trust it? It sits where Model Psychology and Model Internals meet.

My first program tried to predict a model's wrong answers by encoding its competing claims as an entangled quantum state. Pre-registered tests (pass rules written before any data) on two Claude models killed it: the quantum version tied a plain classical copy, 0.83 against 0.84 on an accuracy score where 0.5 is a coin. The model's own stated confidence did as well as anything I built.

So I measured that confidence. On Haiku, the smallest Claude model, changing which questions came first moved its 0-to-100 rating by a median of 24.7 points, against 13.2 from asking twice. Haiku needed a separate confidence for each of six ways of asking on 86% of claims; on Opus, the largest, one shared answer predicted every format, though a yes-or-no guesser nearly matched it, so what Opus shares is a verdict more than a graded belief. On all three models, hiding the model's earlier answer made it repeat that answer far less often. Most of this is already in print, and I say which parts: three findings are partly new, none is new and replicated.

Model Psychology. No model showed a detectable advantage at judging its own errors. That touches Jack Lindsey's finding that a model's access to its own states is real but narrow. I want to know what a stated confidence number is a readout of, and how that changes with scale.

Model Internals. On an open-weight model, a truth probe (a small classifier trained on the model's internal activity, after Marks and Tegmark) moved with question order more than the stated rating did, but not in step with it; on three test items that half is undetermined. Whether an inside representation holds still while the words move is where Samuel Marks's probes and Belinda Li's work on representations meet my result.

The second thread is method. I ran all of this as a scored oversight system: Claude writes its odds before every pre-registered test, a fresh session tries to break every result, and my own blind odds and every steering decision are logged and scored. On <!--n:scored-->37<!--/n--> scored bets the engine's Brier score (how far its odds sat from what happened; 0 is perfect, always saying 50% scores <!--n:coin-->0.250<!--/n-->) is <!--n:brier-->0.156<!--/n-->, which this sample cannot separate from a coin. My own odds, scored on <!--n:human_n-->8<!--/n--> bets, are at <!--n:human_brier-->0.424<!--/n-->, behind the engine. Every checker is still a Claude model; a non-Claude audit is next.

My background is psychology, philosophy and four years leading AI pipeline engineering, not ML research. The record of what I killed, and why, is my evidence.

---

*Word count of the answer (between the rules): about 460 by `wc -w` with the placeholders rendered; trim to 400 when Sean redrafts it. The method paragraph is the one to cut if the form is tight; the panel review's Part 5 answers 1, 2 and 3 are its source.*

## Where each claim comes from

| claim | source |
|---|---|
| A2 0.83 vs F2 0.84, locked test | entangled-mind `49dd6f7`, `results/v2-run-1.md` |
| stated confidence G 0.83 (Haiku), 0.91 (Sonnet), level with the best structural model | `db2eb02` (Addendum D, pre-registered `f7afd8a`) |
| median span 24.7 points vs 13.2 from noise | `results/exp5-run-1.md` line 186, `75744dc` |
| six formats, 86% of 160 claims, Haiku | `1fd521d` (D38) |
| Opus F′ Q = 0.94 [0.90, 0.97], 68 claims; yes/no-verdict predictor Q 0.88, so "verdict" not "credence" | `a8be4b5` (D49), narrowing D50 `9cefab6`; `ledger/audits/em-dm2-opus.md` |
| repeat agreement falls when the earlier answer is hidden, on all three models | `programs/entangled-mind/results/gm2b-self-conditioning-40.md` (Haiku 86% → 36%); `ledger/audits/SUMMARY-1.md` claim 11; em-dm4 for Sonnet and Opus |
| "most already in print; three partly new; none new and replicated" | `../paper/novelty.md` (written `93f47af`, brought to 5 November on this branch) |
| no self-advantage on three models | `bc0f125` (D36, Haiku −0.055 [−0.103, −0.007]); `ba9f99c` (DM3, Sonnet × Opus, not detected); ledger rows em-gm1, em-dm3 |
| Lindsey: introspective access real but narrow (about 20%) | `related-work/self-evaluation-goodhart-introspection.md` (Lindsey 2025, Transformer Circuits Thread) |
| probe moves with order more than the rating, not in step; three gate items, one non-tracking (h191); verdict mixed, scored 0 | ledger row em-gm5; `ledger/audits/probe-dissociation-dp2.md` (DP2 verified DP1; verdict stands) |
| probe built after Marks & Tegmark 2023 | `CONTEXT.md` §1; `application/research-proposal.md`, mentor fit |
| <!--n:scored-->37<!--/n--> scored bets one per run, Brier <!--n:brier-->0.156<!--/n--> (always 0.5: <!--n:coin-->0.250<!--/n-->; hindsight base rate <!--n:hit_rate_ref-->0.184<!--/n-->; every row counted: <!--n:brier_all-->0.182<!--/n--> on <!--n:scored_all-->43<!--/n-->) | `ledger/brier.md` (rule 15, one scored bet per run, `CONTEXT.md` §3) |
| Sean's odds on <!--n:human_n-->8<!--/n--> scored bets, Brier <!--n:human_brier-->0.424<!--/n-->; <!--n:human_lines-->35<!--/n--> odds recorded, all blind | `ledger/brier.md`, `ledger/human-odds.jsonl`; the seven bets in `../paper/day-four.md` §7 |
| every checker a Claude model; no non-Claude audit yet | `ledger/scores.md` ("all 24 audits are Opus-family on Opus-family work"); `../paper/review-anthropic.md` Part 3 |
| background | `CONTEXT.md` §1 |

## Not used, on purpose

- **Scalable Oversight as a named area.** The answer names Model Psychology and Model Internals. Samuel Marks appears where the probe result touches his truth-probe work.
- "There is no stored credence to read out" (proposal.md). This holds for Haiku and is contradicted on Opus (D50).
- "Eleven pre-registered tests overnight." Five of them re-analysed data that had already been opened (D54, D54a).
- "Opus held one credence across formats (94%)." The audit cut "credence" to "verdict"; the answer says "verdict more than a graded belief" and gives the yes/no guesser.
- "With its earlier answers hidden, order still moved it about as much" (ratio 1.23, interval 0.75 to 2.02 on 40 items; `758609a`, D45). The interval is too wide for "about as much", and the sentence did not fit in 400 words; the panel review's Part 5, answer 4, has the supported wording.
- **Program 4's passes as the place the odds carried judgment.** Opus picked which way 116 published findings went 76% of the time (Brier 0.163) and beat a publication-bias shortcut; but a one-line "which version flatters the paper?" rule scored 90% to its 93% on the harder round, the same question alone beats human neuroscientists on a public benchmark (ss-b10c, new, unreplicated), and the items were written by the bettor's own family. Too many caveats for 400 words; the panel review's Part 5, answer 6, has the supported version.
- **The planted-fault catch rate** (<!--n:plants_caught-->15<!--/n--> of <!--n:plants_planted-->15<!--/n-->, `ledger/scores.md`). True and worth saying, but it is a same-family number and the sentence it belongs in is the non-Claude audit, which has not run.
- **"My steers were the highest-value decisions of the week."** A Claude session wrote that about a reconstructed steer. The scored count is helped 18 of 28 (`ledger/steers.md`), a reading by a Claude session, not a measurement; the answer uses the odds column instead.
- The audit counts from program 1 (0 of 39 verdicts reversed, 166 of 560 claims failed). Still true, but the ledger's wider view (<!--n:audited-->56<!--/n--> of <!--n:bets_total-->79<!--/n--> audited, <!--n:reversals-->4<!--/n--> reversed) does not fit alongside the method paragraph.
- **"The model's confidence was too low."** The ss-b1 audit cut it to an exploratory reading; its interval touches zero.
- The stage-by-stage quantum readout (0.63 → 0.49 against 0.68). It is exploratory, not pre-registered.
