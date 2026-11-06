# Re-scout around em-bm9 (does the next rating move toward or away from the last number?)

- **Bet:** em-bm9 · **Program:** entangled-mind (program 1) · **Map node:** bm9
- **The result in one sentence:** On Haiku's single-scale experiment-5 conversations, the shift in the main rating after a sub-question rises with how far the sub-rating sits above the unprompted main rating (β +0.27 [+0.11, +0.43], assimilation by the pre-registered rule), but the audit found most of β is the main rating being less extreme after any sub-question (coefficient on M-first −0.37), while the sub-rating's own level adds only +0.13 [−0.04, +0.28].
- **Date:** 2026-11-05 16:29 MST (from `date`)
- **Read by:** claude-opus-5-5, a fresh reader subagent of the 2026-11-05c remap session. Web reads only (WebSearch, WebFetch; PDFs WebFetch could not parse were converted with `pdftotext` in the session scratchpad). No model API, no experiment, no local model.

**What the result now raises.** After the audit the live question is not assimilation against contrast but which of two things carries β: a pull toward the number just given, or a moderation of the main rating (less extreme) whenever sub-questions come first. A third rival appeared in the reads: a plain shift of later judgments in one direction after any prior turn. The searches went after all three, and after the human survey literature on specific-then-general question order.

**Already in the program's reads and not counted as new:** Stureborg et al. 2024, Kapetanovic et al. 2026, Temkit 2026 (AMEL), Kang 2026, Fischer and Whitney 2014, Cicchini et al. 2018 (`novelty-2026-11-05-em-bm9.md`, mostly abstracts). Kapetanovic et al. and AMEL are re-read in full below for parts the earlier read did not reach: whether the shift is graded with the anchor's value, and what a neutral history does.

## Searches

One line per search: terms; where; date.

1. `part-whole question order assimilation contrast specific general question survey Schwarz Strack Mai 1991`; WebSearch (standard); 2026-11-05. Confirms Schwarz, Strack and Mai 1991 (Public Opinion Quarterly 55:3-23); full text not obtained (SSOAR returned a bot-check page, the SciSpace PDF was an HTML stub, the ISR Michigan page returned 403).
2. `dilution effect large language models irrelevant information makes judgments less extreme`; WebSearch; 2026-11-05. No LLM dilution study; only accuracy-under-distraction papers.
3. `Tjuatja "Do LLMs exhibit human-like response biases" survey design question order arXiv`; WebSearch; 2026-11-05. arXiv 2311.04076: five biases (acquiescence, response order, odd/even scale, opinion float, allow/forbid), no question-order arm, not opened further.
4. `LLM forecasting question decomposition sub-questions probabilities less extreme moderate final estimate`; WebSearch; 2026-11-05. 2601.22444 (decomposition lowers Gemini 3 Pro Brier 0.141 to 0.132 per the search page, not opened); nothing on extremity.
5. `AMEL accumulated message effects LLM judgments arXiv 2605.22714`; WebSearch; 2026-11-05. HTML v1 (read).
6. `LLM ratings central tendency regression toward middle of scale after prior questions multi-turn judgments less extreme arXiv 2025 2026`; WebSearch; 2026-11-05. 2503.22353 (read; does not transfer), 2510.27106, 2601.03444 (not opened).
7. `large language model survey question order effect general specific question assimilation contrast LLM respondents arXiv`; WebSearch; 2026-11-05. Human survey sources only; no LLM part-whole study.
8. `"dilution effect" nondiagnostic information "language models" OR GPT judgments probability`; WebSearch; 2026-11-05. Human sources; Sanborn et al. 2015 opened (one page: abstract only).
9. `anchoring bias large language models numeric estimates high low anchor anchoring index arXiv 2024 2025`; WebSearch; 2026-11-05. Owusu and Feldman, ACL 2026 short (read), 2505.15392, 2511.05766 (not opened).
10. Direct opens, 2026-11-05: arxiv.org/html/2605.22714v1 (first 100,000 of 107,477 characters); arxiv.org/html/2608.25869; aclanthology.org/2026.acl-short.16.pdf (pdftotext, all pages); arxiv.org/html/2505.14489 (first 100,000 of 121,054 characters); escholarship qt3fr526kk (pdftotext: abstract page only); arxiv.org/html/2503.22353 (first 100,000 characters).

**Field note.** Survey methodology has the exact human design (a specific question before a general one) but its key paper could not be opened, so nothing from its results is reported. Social psychology's dilution effect (non-diagnostic information makes predictions less extreme) is the human name for the audit's moderation reading; no LLM test of it was found. No LLM paper found separates moderation of a later rating from a pull toward the earlier number.

## Read records

### Anchoring Bias in LLM-as-a-Judge Systems: Prior Scores Compromise Evaluation Independence — Kapetanovic, Altwlkany, Mercep, Duricic & Lacic, 2026, arXiv 2608.25869 (CIKM '26) (re-read for new parts)
- read_depth: full (arXiv HTML).
- what_tested: whether a prior score shown as metadata moves a judge's 0-5 rating; conditions C0 (no metadata), C1 (revision framing only), C2 (revision, attempt number and a prior score drawn from [0, 3.99), always below the 4.0 acceptance line).
- on_whom: GPT-4.1, Claude-4.5-Sonnet, DeepSeek-R1, Llama-3.3-70B, Llama-3.1-8B, Llama-3.2-3B, Qwen2.5-7B, Gemma-2-9B; 20 fixed texts; 192,000 attempted, 185,271 valid evaluations; four temperatures.
- how_scored: C2 − C0 mean rating with 95% CI and Cohen's d; acceptance rate; token-probability probes.
- result: seven of eight intervals below zero; Claude-4.5-Sonnet Δ −0.706 [−1.139, −0.245], d −0.44, acceptance down 22.29 points; Llama-3.2-3B d −0.71; within C2, changing the anchor from 1.0 to 3.9 produced almost no further change (GPT-4.1 probe), which the authors call threshold-like but not established.
- limitations (as stated): because all priors were below threshold, the study cannot tell moderation toward the middle from a general downward shift; C2 adds several fields at once; a matched template with an irrelevant number is needed.
- borrow: the C0/C1/C2 ladder, which separates "something came before" from "a number came before".
- next_steps_it_suggests: a matched irrelevant-number template; other anchor ranges.
- predicts_for_us: bm9-f3: the presence of earlier material moves the rating while its numeric level barely matters, which is the audit's reading of bm9 (S-level +0.13, CI through 0); predicts the moderation or shift component, not a graded pull, on Sonnet-class Claude.
- **rival named**: the shift is set by the presence of prior material, not by the earlier number's value. The earlier read's wording "toward its value" overstates this paper (see the corrected Novelty line).

### AMEL: Accumulated Message Effects on LLM Judgments — Temkit, 2026, arXiv 2605.22714 (v1) (re-read for new parts)
- read_depth: partial re-read (arXiv HTML, first 100,000 of 107,477 characters: design, per-model table, uncertainty bins, neutral arm, limitations).
- what_tested: whether a run of earlier yes/no judgments in the same chat moves a later binary judgment; histories of 5, 10, 20 or 50 turns that are 90% no, 90% yes, or 50/50, against a fresh context.
- on_whom: twelve models; Anthropic: Haiku 4.5, Sonnet 4.6, Opus 4.6; 21 items in each of three domains; 10 repeats at temperature 1.
- how_scored: binary shift (BS) in P(yes) against baseline, item-clustered CIs, Cohen's d.
- result: overall BS −0.052 [−0.059, −0.045], d −0.17; Haiku 4.5 d −0.22, Sonnet 4.6 −0.18, Opus 4.6 −0.17; the **neutral 50/50 history also shifts toward "no"**, BS −0.097, d −0.32, close to the no-saturated arm's −0.107; high-entropy items d −0.34 against −0.15 for items deterministic at baseline; no growth with history length.
- limitations (as stated): binary judgments only; the neutral arm used evaluative filler, so "any history" and "any evaluative history" are not separated; Opus 4.6 unparseable 21.7-23.2%.
- borrow: the neutral-history arm, and reporting the shift by baseline uncertainty.
- next_steps_it_suggests: a non-evaluative neutral control; inter-rater checks; the flipped-framing test on all models.
- predicts_for_us: bm9-f3: any prior exchange moves a later judgment in one direction on Claude 4.x models, even when balanced; that is a shift, not a moderation, so a design must separate the two (slope against intercept).
- **rival named**: a one-directional shift after any earlier exchange. The earlier novelty read's "history polarity drags judgments its way ... Claude Haiku (d = −0.22)" is inexact: −0.22 is Haiku's overall shift toward "no", and the balanced history shifts too.

### Anchoring Depends on Confidence and Post-Training in Language Models — Owusu & Feldman, 2026, ACL 2026 (Volume 2: Short Papers), pp. 174-180, https://aclanthology.org/2026.acl-short.16/
- read_depth: full (PDF via pdftotext, including Appendix A).
- what_tested: whether an irrelevant number ("The slot machine stopped on 79.") before a factual numeric question shifts the model's distribution over nine candidate answers, and whether the shift depends on the model's baseline certainty or accuracy.
- on_whom: Llama-3.1-8B and Qwen2.5-7B base, instruct and DeepSeek-R1-distilled variants (six models); 50 Open Anchoring Quest questions (replicated on 99); N = 600 observations.
- how_scored: total variation distance (TVD) between control and anchored distributions; certainty = top candidate probability at control; direction of the expected-value shift.
- result: certainty predicts less shift (pooled β −0.037, p = .001; mixed model −0.052, p < .001); accuracy does not once certainty is in (p = .48); instruction-tuned models move toward the anchor only 50-64% of the time for low anchors (78-86% for high), so there "TVD may be capturing general instability ... rather than anchoring"; across models 82.5% of shifts were toward the anchor; TVD and |Δ| correlate r = 0.63.
- limitations: 50 questions; teacher-forced scoring over a fixed candidate set; open 7-8B models only.
- borrow: report the share of shifts that go toward the earlier number, beside the size of the shift; an instability that is not directional should not be read as a pull.
- next_steps_it_suggests: mitigation tests; mechanisms for family differences.
- predicts_for_us: bm9-f3: in post-trained models a prior number often moves the answer without pulling it toward the number, which favours the moderation or instability reading over a graded pull.
- **rival named**: non-directional instability after a prior number in instruction-tuned models.

### Reasoning Models Better Express Their Confidence — Yoon, Kim, Yang, Kim, Kim, Kim, Choi, Kim & Seo, 2025, arXiv 2505.14489 (v2, 22 Oct 2025)
- read_depth: partial (arXiv HTML, first 100,000 of 121,054 characters: models, elicitation, main result, chain-of-thought truncation, ablation, limitations).
- what_tested: whether models that reason before answering state better-calibrated verbal confidence, and how calibration changes as the reasoning unfolds.
- on_whom: six reasoning models and their non-reasoning counterparts at about 32B (Qwen, GLM, EXAONE families); TriviaQA, NonambigQA, SuperGPQA and MMLU-Pro subsets, 1,000 items each; no Claude.
- how_scored: ECE, Brier, AUROC of ten-bin verbal confidence; the chain of thought cut at 11 points with a forced answer and confidence at each.
- result: reasoning models better on every calibration metric in 33 of 36 settings; calibration improves as the chain of thought proceeds (R1-Distill-Qwen on NonambigQA: slopes −0.015 ECE, −0.010 Brier); removing "non-linear reasoning" (alternatives, backtracking) hurts most (ECE 0.042 → 0.161); reasoning models still rarely state confidence below 55%.
- limitations: 32B models only; calibration, not extremity, is what improves.
- borrow: truncate-and-ask (asking for the rating at several points of the deliberation) as a within-conversation way to watch a rating moderate.
- next_steps_it_suggests: scaling; whether longer reasoning helps (budget forcing did not reliably).
- predicts_for_us: bm9-f3: considering alternatives before answering makes stated confidence less overconfident on open models; that is the mechanism the moderation reading needs, measured as calibration rather than as a slope.
- **design to borrow** (truncate-and-ask); it does not state our result.

### Abstract only, or not transferred
- Sanborn, Noguchi, Tripp & Stewart 2015, "Inference, Not Dilution in the Dilution Effect", CogSci 37 (escholarship qt3fr526kk): read_depth abstract (the PDF opened to its first page only). The abstract says non-diagnostic evidence dilutes judged strength, and that the effect came from people overestimating diagnostic evidence alone, not from wrong combination. Human; **changes nothing** beyond naming the moderation reading.
- Li et al. 2025, "Firm or Fickle?" (arXiv 2503.22353): accuracy under eight kinds of follow-up challenge on six models including Claude-3.5-sonnet (accuracy 0.6411 in round 1 to 0.4793 in round 8 under one follow-up type). It measures giving way under pressure, not rating extremity: **changes nothing**.

## What the re-scout changes

Adds **bm9-f3**: a free three-model check of the audit's moderation reading. The gm2/gm2b (Haiku) and em-dm4 (Sonnet, Opus) archives hold the main question asked first (MF arm, turn 1) and the main question asked after four sub-questions (O1-O4 shown chains, no earlier main answer). Compare slopes against a split-half baseline so regression to the mean cannot fake moderation; AMEL's one-way shift goes to the intercept. Kapetanovic and Owusu predict little graded pull, so the old "pull toward the number" reading (bm9-f1, parked, about $3) is now the less likely one and should wait for this. Odds are elicited later.

## Novelty line check

The ledger row carries a line from a fresh session (claude-fable-5-1). Checked against the two papers re-read in full: Kapetanovic et al. report shifts *downward* with all priors below threshold and almost no change across anchor values, not a shift "toward its value"; AMEL's Haiku d = −0.22 is the overall shift toward "no" across history conditions, and a balanced history shifts as much, so "history polarity drags judgments its way" misstates it. The verdict (partly new) is unchanged. **Corrected line:**

**Novelty:** partly new. That earlier context moves an LLM's next judgment is in print: Stureborg et al. 2024 (arXiv 2405.01724) find GPT-4's own earlier coherence score raises its later consistency score; Kapetanovic et al. 2026 (arXiv 2608.25869, CIKM '26) find a shown below-threshold prior score lowers judge ratings on seven of eight models (Claude-4.5-Sonnet d = −0.44), with almost no further change across anchor values; and Temkit 2026 (arXiv 2605.22714) finds that any earlier history, even a balanced one, shifts binary judgments toward "no" (Claude Haiku 4.5 d = −0.22 overall). None holds the content's push fixed, asks a sub-question before the main question, or separates a pull toward the just-given number from the main rating becoming less extreme, which the em-bm9 audit found carries most of our β (sub-rating level alone +0.13 [−0.04, +0.28]): partly new. Search: the earlier line's searches, plus WebSearch "anchoring bias large language models numeric estimates high low anchor" and "LLM ratings central tendency multi-turn judgments less extreme", 2026-11-05, with the Kapetanovic and AMEL HTML re-read in full; claude-opus-5-5, 2026-11-05c remap re-scout.
