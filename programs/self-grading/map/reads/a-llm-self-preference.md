# Cluster A — LLM self-preference as judges
Reader: claude-opus-5-5, 2026-11-05 04:42 MST (America/Denver)

How these were read: each paper's arXiv HTML was opened with a web fetch tool that extracts from the full page text (pages over 100,000 characters were read in two passes). For the two newest preprints (Chae et al. 2026; Popov 2026) the PDF was downloaded and its text extracted, and every number below was checked against that text. All ten given arXiv IDs resolved to the named papers. Item 11 produced five papers (records 11a-11e). Fields searched: ML / LLM evaluation only. Other fields belong to other clusters.

### Panickssery self-recognition — Panickssery, Bowman & Feng, 2024, NeurIPS 2024 (proceedings PDF seen in search), https://arxiv.org/abs/2404.13076
- read_depth: full
- what_tested: whether LLM judges recognise their own summaries, whether they prefer them, and whether recognition causes the preference (fine-tuning for recognition, then measuring preference).
- on_whom: Llama-2-7b-chat, GPT-3.5, GPT-4 (temperature 0). 1,000 articles each from XSUM and CNN/DailyMail; fine-tuning used 500 train + 500 eval articles per dataset. Comparison sources were the other LLMs and human summaries.
- how_scored: pairwise (pick one of two; order swapped and confidences averaged) and individual (Yes/No for "is this yours", 1-5 Likert for quality).
- result: GPT-4 tells itself apart from two other LLMs and humans at 73.5% accuracy. Pairwise self-preference out of the box: GPT-4 0.705 (XSUM) and 0.912 (CNN); GPT-3.5 0.582 and 0.431; Llama 0.511 and 0.505. Fine-tuning pushes recognition above 90% and moves self-preference along with it, on a linear trend. Example-level Kendall's tau for GPT-3.5 on XSUM rose from 0.41 to 0.74. Order reversal rates: GPT-4 25%, GPT-3.5 58%, Llama 89%. **Label experiment (Section 3.5), the only one with identical text and only the label changed:** GPT-4 XSUM 0.73 with correct source labels vs 0.32 with reversed labels; GPT-4 CNN 0.94 vs 0.89; GPT-3.5 XSUM 0.61 vs 0.46; Llama showed no clear difference. Control fine-tunes (length, vowel count, readability, constant or random answers) fell on the same recognition-preference line.
- limits: no ground-truth or human quality control, so the self-preference may sometimes be deserved. Summarisation only, one prompt design. The causal claim is not shown at the level of single examples. No Claude models.
- borrow: the reversed-label control (own text labelled other, other text labelled own), which goes in our 2x2 of true source by stated label. The swapped-order averaging goes in every pairwise arm. We should record the order-reversal rate as a noise floor before we read any label effect.
- next_steps_it_suggests: paraphrase texts to block self-recognition and see whether the preference falls (an example-level causal test); add more tasks and frontier models.

### Wataoka self-preference metric — Wataoka, Takahashi & Ri, 2024 (v2 2025), arXiv preprint, https://arxiv.org/abs/2410.21819
- read_depth: full
- what_tested: a self-preference metric that conditions on human preference (an Equal Opportunity gap), and whether low perplexity explains the preference better than authorship does.
- on_whom: 8 judges (GPT-4, GPT-3.5-Turbo, Vicuna-7b/13b, Koala-13b, oasst-pythia-12b, dolly-v2-12b, stablelm-7b) on Chatbot Arena (the paper says 33,000 dialogues), with human labels. Perplexity analysis covers only the 6 open models; a Llama 2 / 3.1 follow-up has no human labels. No Claude models.
- how_scored: pairwise, using normalised P(A)/P(B), with positions swapped and averaged. Bias = P(judge picks it | it is the judge's own, humans prefer it) - P(judge picks it | it is another model's, humans prefer it).
- result: GPT-4: recall 0.945 when humans preferred its answer vs 0.425 otherwise, a gap of 0.520, the largest of all models. Demographic-parity bias: GPT-4 0.749, Vicuna-13b 0.382, GPT-3.5 0.191, Koala-13b 0.175; three models are slightly negative (dolly -0.069). Holding perplexity fixed, the self vs other win rates were similar for most open models, so the authors conclude perplexity matters more than authorship.
- limits: observational. Authorship was never manipulated with text held fixed. Perplexity is not available for the GPT models. The metric needs human labels, and Arena human labels are noisy.
- borrow: condition self-preference on an outside quality label (human or ground truth). Do not read a raw self-vs-other gap as bias. Where we can get logprobs, log the perplexity of each text as a covariate.
- next_steps_it_suggests: ensemble judges; down-weight a judge on texts where its own perplexity is low.

### Pride and Prejudice (self-refinement) — Xu, Zhu, Zhao, Pan, Li & Wang, 2024, arXiv preprint (v2; venue not verified), https://arxiv.org/abs/2402.11436
- read_depth: full
- what_tested: whether a model's self-scores exceed true quality, and whether that gap grows over rounds of self-refinement.
- on_whom: GPT-4, GPT-3.5-Turbo, Gemini, LLaMA2-7B (plus 13B/70B), Mixtral 8x7B, DeepSeekMoE 16B. 100 examples each from Flores-200 low-resource translation, CommonGen Hard and MATH. No Claude models.
- how_scored: Bias = mean(self-score - true quality), where true quality is BLEURT mapped to MQM, concept coverage, or correctness; plus distance skewness.
- result: Yor-En, iteration 0 to 10: GPT-4 bias 8.06 to 14.6; GPT-3.5 19.6 to 21.9; Gemini 9.62 to 17.6. Self-refinement improved fluency but not task quality. Self-rewarding with larger candidate pools raised bias. LLaMA2-70B plateaued after iteration 5 while 7B and 13B kept rising. External feedback (InstructScore, with a reference) lowered bias.
- limits: there is no "other-author" arm, so it measures self-overrating against ground truth rather than self versus other. Recognition and favouring are not separated. Authorship labels are not manipulated.
- borrow: a failure mode for our testbed's loop: repeated self-revision inflates the self-score while true quality stays flat. Wherever we grade over several rounds, track self-score minus a ground-truth score.
- next_steps_it_suggests: test bias toward models that share pretraining data, objective or family, and toward distilled models.

### Narcissistic evaluators — Liu, Moosavi & Lin, 2023 (v4 2024), arXiv preprint, https://arxiv.org/abs/2311.09766
- read_depth: full
- what_tested: whether likelihood-based metrics (BARTScore, T5Score, GPTScore, a Cohere scorer) give higher scores to summaries from their own model family.
- on_whom: 20 evaluators scoring 6 generator families; 500 documents each from CNN/DM and XSUM; human check on SummEval (100) and RoSE.
- how_scored: min-max normalised likelihood scores, reference-free and reference-based.
- result: the self-family diagonal is darker in the heatmaps (no effect sizes are tabulated), more so when scoring is reference-free. Human correlations were weak (e.g. Spearman 0.488 for BART-Base-CNN on RoSE).
- limits: does not transfer directly. These are likelihood metrics, not prompted judges, and there is no label manipulation. Kept only as evidence that sharing a model raises scores even without any recognition.
- borrow: none for the label design. The reference-free vs reference-based contrast suggests giving the judge a reference may shrink self-bias, which would be an optional arm.
- next_steps_it_suggests: more tasks, more evaluators, and a larger human evaluation.

### CoBBLEr — Koo, Lee, Raheja, Park, Kim & Kang, 2023 (v3 2024), arXiv preprint (venue not verified), https://arxiv.org/abs/2309.17012
- read_depth: full (both halves of the HTML)
- what_tested: six judge biases, including egocentric (self-preference), measured with anonymous aliases and again with real model names plus a "(You)" tag on the judge's own answer.
- on_whom: 16 models (GPT-4, ChatGPT, InstructGPT, LLaMA/LLaMAv2, Cohere, Falcon, Alpaca, Vicuna, Koala, etc.); 50 QA instructions (ELI5 + StrategyQA), 800 generations, 5,250 pairwise examples per evaluator. No Claude models.
- how_scored: proportion of comparisons where the judge picks its own answer. Order condition = aliases ("System Star/Square"); Compassion condition = real names, with "(You)" on its own.
- result (Order / Compassion): GPT-4 0.78 / 0.06; ChatGPT 0.58 / 0.17; InstructGPT 0.28 / 0.27; Koala 0.48 / 0.86; Vicuna 0.27 / 0.45; LLaMAv2 0.06 / 0.0. So naming the judge as author cut GPT-4's self-picks sharply and raised Koala's. The authors attribute GPT-4's drop to stronger position bias under names. Mean human-model rank-biased overlap was 0.44, against 0.54 between humans.
- limits: the pairs are not explicitly confirmed identical across conditions. The random baseline of 0.25 is not explained. The Compassion condition reveals every model's name, not only the self-label. Quality is controlled only loosely (BERTScore 0.81-0.86), and the authors concede egocentric picks may partly be earned. Many small models had low rates of valid responses.
- borrow: the label can push either way, and the strongest model rated itself less when named. Our pass rule must be two-sided. Report the parse/valid-response rate for each condition.
- next_steps_it_suggests: debias with chain-of-thought or alignment methods.

### CALM / Justice or Prejudice — Ye, Wang, Huang et al., 2024, arXiv preprint (v2; venue not verified), https://arxiv.org/abs/2410.02736
- read_depth: full (both halves of the HTML; the second half is prompt templates)
- what_tested: 12 judge biases, among them self-enhancement (scoring own vs others' answers with authorship hidden), compassion-fade (real names shown vs anonymised) and refinement-aware (a refined answer scored with vs without its refinement history).
- on_whom: judges ChatGPT, GPT-4-Turbo, GPT-4o, Claude-3.5, GLM-4, Qwen2. Self-enhancement n = 150; refinement n = 500; compassion n = 439.
- how_scored: 1-10 scores; ErrorRate = |1 - y_self/y_other|; robustness rate (RR) for label perturbations.
- result: self-enhancement (self / other / error): Claude-3.5 7.04 / 6.55 / 7.48; GPT-4o 7.01 / 6.89 / 1.74; Qwen2 7.64 / 6.58 / 16.1; ChatGPT 5.21 / 5.72 / 8.91. Refinement-aware (refined / +history): Claude-3.5 7.51 / 7.68; GPT-4o 7.44 / 7.20; ChatGPT 5.23 / 4.94. Compassion-fade RR: Claude-3.5 0.875, other models 0.835-0.877.
- limits: the self vs other gap compares different texts and has no quality control, so the "other" pool includes weaker generators. Self-enhancement is not label-only. The text does not give a named-vs-anonymised difference for compassion-fade. There is no limitations section.
- borrow: the refinement-aware arm, which bears directly on our testbed's revise-and-regrade loop: the same refined text scored with and without its history. ErrorRate is a scale-free summary.
- next_steps_it_suggests: use CALM to test future judge methods (nothing specific on self-enhancement).

### Legitimate vs harmful self-preference — Chen, Wei, Zhu, Feng & Meng, 2025 (v3 Dec 2025), arXiv preprint, https://arxiv.org/abs/2504.03846
- read_depth: full (both passes; LMArena numbers appear only in figures)
- what_tested: on tasks with verifiable answers, how much self-preference is legitimate (the judge's own answer is correct) vs harmful (its own answer is wrong).
- on_whom: 11 open judges (Qwen2.5 3B-72B, Llama 3.x, Gemma-2) plus 5 R1-distill reasoning judges; 7 fixed evaluatees; MATH500, MMLU (1K), MBPP+; about 12,848 LMArena samples. No Claude models.
- how_scored: pairwise A/B/tie, both orders. Metrics: self-preference ratio (SPR), legitimate self-preference ratio (LSPR), harmful self-preference propensity (HSPP).
- result: the correlation of task accuracy with SPR was 0.801 / 0.817 / 0.771, so stronger models prefer themselves more, mostly legitimately (LSPR 96.57% for Qwen2.5-72B on MATH500). Harmful self-preference is worse in strong models: Qwen2.5-72B HSPP 86% (MATH500) and 73% (MMLU), against SPR 55% and 52%. Long chain-of-thought lowered HSPP (MATH500, from a 29.53 baseline to 11.87-15.51; McNemar p < 0.01).
- limits: labels are never manipulated and recognition is not separated from preference. Pointwise scoring is not studied. The no-reasoning arm reads logits from a single token, so the arms differ in more than reasoning.
- borrow: use a task with known right answers and split self-preference into the cases where the model's own answer is right and those where it is wrong. Only the wrong-answer cases are harmful. This is the quality control most papers in this cluster lack.
- next_steps_it_suggests: test self-consistency, best-of-N and multi-agent verification; test pointwise and ranking formats; test same-family preference.

### MT-Bench self-enhancement — Zheng, Chiang, Sheng et al., 2023, arXiv preprint (v4; venue not verified), https://arxiv.org/abs/2306.05685
- read_depth: partial (Section 3.3 self-enhancement and its data context only, as briefed)
- what_tested: whether GPT-4, GPT-3.5 or Claude-v1, acting as judges, give their own answers higher win rates than humans do.
- on_whom: 6 models' answers to the 80 MT-bench questions; 58 expert human labellers (about 3K votes overall). No separate n for this analysis.
- how_scored: win rate excluding ties under each judge vs under humans (Figure 2b).
- result: GPT-4 gives itself a win rate 10% higher than humans give it; Claude-v1 gives itself 25% higher; GPT-3.5 does not favour itself. Both judges also favour some other models. "our study cannot determine whether the models exhibit a self-enhancement bias."
- limits: little data. There is no controlled manipulation, and the authors say one is hard because restyling changes quality.
- borrow: an early Claude datum (Claude-v1 +25%), useful only as history. Their point that restyling changes quality is why we hold the text fixed and vary only the label.
- next_steps_it_suggests: a controlled study of self-enhancement (left open).

### Preference leakage — Li, Sun, Huang et al., 2025 (v3 Mar 2026), arXiv preprint (ICLR ethics statement), https://arxiv.org/abs/2502.01534
- read_depth: full (the last 3K characters, part of the broader-impact section, were not read)
- what_tested: whether a judge favours student models trained on data from itself or a related model, and whether it can recognise those students.
- on_whom: generators/judges GPT-4o, Gemini-1.5-flash, LLaMA-3.3-70B; students Mistral-7B and Qwen-2.5-14B trained on 30K UltraFeedback prompts; Arena-Hard (500) and AlpacaEval 2.0 (805). Claude-3.5-Sonnet appears only as an extra judge in an appendix.
- how_scored: Preference Leakage Score, the judge's win rate for its related student relative to the pair average.
- result: PLS for GPT-4o & Gemini pairs was 23.6% (Mistral) and 27.9% (Qwen). Same model 23.6%, inheritance 19.3-22.3%, same family 8.9% / 2.8%. SFT 23.6%, DPO 5.2%, ICL -2.7%. Judges recognised their students near chance (about 30-53%), while a BERT classifier reached 82.4%. Removing style cues roughly halved PLS (17.5 to 9.0).
- limits: transfer to us is indirect, since the question is training contamination, not authorship labels. Label manipulation was not tested.
- borrow: favouritism can happen without self-recognition. If our models fail a "did you write this?" probe, that does not rule out a preference. Report a recognition probe next to the preference measure.
- next_steps_it_suggests: measure how much leaked preference each generator contributes; re-evaluate leaderboards with alternate judges.

### Inconsistent and biased evaluators — Stureborg, Alikaniotis & Suhara, 2024, arXiv preprint, https://arxiv.org/abs/2405.01724
- read_depth: full
- what_tested: familiarity (low-perplexity) bias, score-scale skew, anchoring across attributes, and inconsistency between samples in LLM summary judges.
- on_whom: gpt-3.5-turbo-0301 and gpt-4-0613 (GPT-4-Turbo in a case study); SummEval (100 articles x 16 summaries) and RoSE; over 560,000 outputs. No Claude models.
- how_scored: Kendall's tau against expert ratings; Krippendorff's alpha.
- result: GPT-4's Coherence-5 summaries average perplexity 5.34, against 6.36 for experts. Scoring attributes one after another anchors them: Coherence-Consistency r = 0.979 for GPT-4 vs 0.315 for humans. Inter-sample alpha was 0.587 for GPT-4 vs 0.659 between humans. On a 1-100 scale the scores pile up on 90 and 95; 1-10 was best (tau 0.428).
- limits: no authorship manipulation; GPT models only; summarisation only.
- borrow: use a 1-10 scale and one attribute per call (anchoring would contaminate a multi-attribute self-grade). Temperature 0 or repeated samples. Measure sampling noise within each condition before reading a label effect smaller than about 0.5.
- next_steps_it_suggests: generalise beyond GPT and summarisation.

### 11a. Self-attribution bias (monitors) — Khullar, Hopkins, Wang & Roger, 2026, arXiv preprint (NeurIPS 2025 workshop version "Language Models Rate Their Own Actions As Safer"), https://arxiv.org/abs/2603.04582
- read_depth: full (HTML v1, two passes; many per-model values are only in figures)
- what_tested: whether a model rates an action as more correct or safer when it is framed as its own. Framing was explicit (a "you wrote this" statement) or implicit (the action sits in the model's own earlier assistant turn, or the model rates in the same turn it generated). The design crosses on-policy with off-policy text.
- on_whom: Claude-3.5-Haiku, Claude-4-Sonnet, Claude-4.1-Opus, Gemini-2.5-Pro, Gemma-3-27B, GPT-4o, GPT-5 / -Mini / -Nano, GPT-OSS-20B / 120B. Tasks: SWE-bench patch correctness, prompt-injection PR approval, 200 computer-use risk scenarios, agentic-misalignment emails, 600 AITA dilemmas, 1,200 MMLU, 1,000 unanswerable MCQs, 600 Hendrycks Ethics. Most task n are not stated in the main text.
- how_scored: 0-10 ratings (shift from baseline); AUROC for code correctness; approve / block / escalate decisions.
- result: code-correctness AUROC 0.99 at the on-policy baseline vs 0.89 same-turn and 0.92 previous-turn; off-policy AUROC stayed 0.99. Self-attribution made approval of an injected patch about 5x more likely in one setting. Reversals against the bias's direction were 5-10x rarer than reversals with it. Reasoning budget did not reliably help. **Explicit label: identical insecure patches labelled self-authored, other-model or unlabelled scored "typically within 0.5/10" of each other; implicit (positional, on-policy) attribution drove the effect.** Off-policy harmfulness shifts (Table 1): Claude 3.5 Haiku +0.74, Opus 4.1 -0.46, Sonnet 4 -0.79 (sign convention unclear in the text).
- limits: simple prompts. Many-turn agentic settings and prompt compaction were not studied. The explicit-label models and n are not reported. Same-turn on-policy text is not identical across conditions by design.
- borrow: the closest prior to our seed question, and it matches our earlier finding that turn position mattered more than the label. Our design should cross label (self / other / none) with position (user turn vs prefilled earlier assistant turn) and with on- vs off-policy text.
- next_steps_it_suggests: study the mechanism; do not validate monitors only on static off-policy data.

### 11b. Bidirectional self/other labels — Chae, Kim, Jung, Choi & Jung, 2026 (v3 Oct 2026), EMNLP 2026 Findings per the arXiv page, https://arxiv.org/abs/2608.18091
- read_depth: full (PDF text; every number below was checked against it)
- what_tested: blind self-preference, then a 2x2 of true source (self / other) by displayed label ("your own selection" / "another language model", with no model names) on quality-matched, identical targets.
- on_whom: 10 judges, including Claude Opus 4.7, GPT-5.5, Gemini 3.1 Pro, Grok 4.3, DeepSeek-V4-Pro, Kimi K2.6, Llama 4 Maverick, Mistral Large 3 and two Qwen3.6 models. Exp 1: 9,000 runs. Exp 2: 40 matched pairs per judge, 4,800 runs. Replication: 90 research proposals style-normalised by Claude Haiku 4.5.
- how_scored: 1-7 on four dimensions; mixed-effects models.
- result: blind self-preference was +0.181 [0.13, 0.23], falling to +0.003 [-0.05, 0.06] once two low-discrimination judges were removed. **Label effect beta_L = +0.43 [+0.39, +0.47], p < .001. Actual source beta_A = +0.02 (p = .689).** All ten judges rated self-labels above other-labels. Claude Opus 4.7 deviated from baseline by +0.275 under the self-label and -0.023 (n.s.) under the other-label, a "self-boost" pattern. GPT-5.5 showed only an other-penalty (-0.340). Proposal replication: Overall +0.196, but Feasibility reversed (-0.116).
- limits: the judges selected constraints rather than writing text. Labels were explicit. One domain plus one replication, English only, and the rubric was not validated against humans.
- borrow: the full design. Quality-matching from blind scores, a crossed true-source x label design, and splitting the label effect into self-inflation and other-deflation by comparing each against a no-label baseline. This is the label-only test our seed question needs.
- next_steps_it_suggests: test implicit cues and verifiable tasks; test whether withholding or obfuscating attribution removes the bias.

### 11c. Same text, different filename — Popov, 2026 (v1 1 Nov 2026), arXiv preprint (econ.GN; pre-registered on AsPredicted), https://arxiv.org/abs/2611.01829
- read_depth: full (PDF text; every number below was checked against it)
- what_tested: whether a filename label (neutral, a human name, ChatGPT / Claude / Gemini, "_v2") changes the writing-quality score of an identical document; then self-preference on LLM-written text.
- on_whom: **anthropic/claude-sonnet-5.5**, openai/gpt-6.1-sol, google/gemini-4-argon via OpenRouter. Study 1: 4 human-written documents x 6 labels x 152 repetitions (10,944 observations, about $36). Study 2: 30 briefs x 3 generators = 90 texts x 8 labels x 12 repetitions (25,920 responses, $47.66).
- how_scored: 0-10 writing quality, one decimal; OLS with document fixed effects, Holm-corrected.
- result: own-family label vs rival labels (Study 1, H2): Sonnet -0.099, Sol -0.037, Argon +0.046 (all p < 0.001). Sonnet scored rival-labelled documents +0.279 above neutral. Study 2, unlabelled own text (H5): Sol +0.338 (29/30 briefs positive), **Sonnet -0.281 (5/25 briefs positive/negative), self-deprecating**, Argon +0.551. Own label on own text (H6): Sonnet +0.019 (p = 0.436), Sol +0.018, Argon +0.157. Label effects vary a lot by document (for Sonnet, -0.56 to +0.75).
- limits: 4 human documents by one author and 30 briefs. Filenames were sent as prompt text. Changing the harness shifted the marks. The labels name model families; there is no "you wrote this" wording.
- borrow: the direct prior on our model. Sonnet 5.5 may grade its own text lower, not higher, so our rule must be two-sided. The per-document effects are large, so we need many items and must report effects per item, not just the mean.
- next_steps_it_suggests: scrub metadata before judging; study mechanisms of context-specific bias; test whether human judges show the same.

### 11d. Label-induced bias (blog posts) — Saraf, Rezvani Boroujeni, Beaudry, Abedi & Bush, 2025, arXiv preprint, https://arxiv.org/abs/2508.21164
- read_depth: full (HTML v3, one pass)
- what_tested: blog posts scored with no labels, true labels, and two false-label permutations (labels rotated across models).
- on_whom: ChatGPT-4o, Gemini 2.5 Flash, Claude Sonnet 4; 10 titles x 3 models = 30 posts.
- how_scored: pick-the-best share; 0-10 scores for coherence, informativeness and conciseness.
- result: unlabelled self-pick rates: ChatGPT 50%, Gemini 45.3%, Claude 46.7%. With true labels Claude's self-pick rose to 60%. Claude's own text labelled "Gemini" fell to 18.48%. Gemini's preference for text labelled "Claude" rose from 11.32% to 51.35%. Swings reached 50 points in preference and 12 points in quality.
- limits: tiny n, no statistical tests, no human check. The labels are real brand names, so reputation is confounded with self. The figure references are inconsistent.
- borrow: a warning that brand names carry reputation. Our "other" label should be generic ("another model") rather than a brand, or brand should be its own arm.
- next_steps_it_suggests: more models and domains; find the source of the asymmetric bias.

### 11e. Authorship obfuscation — Mahbub & Feng, 2025, arXiv preprint, https://arxiv.org/abs/2512.05379
- read_depth: full (HTML v1; before/after self-preference rates appear only in figures)
- what_tested: whether light perturbations that hide authorship (2-word synonym swaps, judge paraphrasing, code restyling) reduce self-recognition and harmful self-preference.
- on_whom: Llama-3.1-8B, Qwen2.5-7B, Llama-4-Scout / Maverick, DeepSeek-V3 (plus 4 in the appendix); QuALITY (2,086 questions); MBPP+. Human check: 30 annotators, 2,500 judgments. No Claude models.
- how_scored: pairwise with unlabelled sources; harmful self-preference judged against gold answers; separate self-recognition queries.
- result: recognition and self-preference correlated, r = 0.63 (n = 6,667). Synonym swaps lowered recognition and harmful self-preference (p < .01). Annotators saw no quality change. Fully neutralising style through paraphrase increased harmful self-preference.
- limits: open models only; only the loss cases were studied; tone and length were not controlled.
- borrow: the 2-word synonym perturbation is a cheap recognition-breaker, which would be an arm in our test.
- next_steps_it_suggests: other obfuscation methods; white-box vs black-box comparison.

## Cluster synthesis
Established: judges often pick their own outputs, but much of that is earned or comes from familiarity. Chen et al. find it tracks accuracy, Wataoka et al. find it tracks low perplexity, and Chae et al.'s blind self-preference vanished once two low-discrimination judges were dropped. Recognition and preference correlate (Panickssery; Mahbub r = 0.63), yet preference can occur without recognition (Li et al.). The bias is worst when the judge's own answer is wrong (Chen HSPP 73-86%).

Open, and conflicting: does a stated label alone move scores? Chae: yes, +0.43 on a 7-point scale, all 10 judges, Opus 4.7 +0.275. Khullar: explicit "you wrote this" moved scores less than 0.5/10, and implicit turn position drove the effect. Popov: Sonnet 5.5 is self-deprecating (-0.281) and favours rival labels (+0.279). CoBBLEr: naming GPT-4 as author cut its self-picks from 0.78 to 0.06. Our own earlier results show the same split.

Candidate cheap tests:
1. **Label-only, three arms** (you wrote / another model wrote / none), identical off-policy texts in a user turn, 1-10 scale, two-sided. Counts against: |self - other| < 0.15 with a CI excluding 0.3.
2. **Label x turn position, 2x2** (text as a user turn vs as a prefilled earlier assistant turn). Counts against Khullar: the label effect is at least as large as the position effect.
3. **Crossed true source x label** on quality-matched pairs (Chae / Panickssery 3.5). Counts against recognition-driven bias: beta_A is about 0 while the label effect is not zero, or the reverse.
4. **Verifiable task** (math with known answers): self-preference split by own-correct vs own-wrong. Counts against harmful bias: the excess self-score appears only when the model's own answer is correct.
5. **2-word synonym swap** on the model's own text, unlabelled. Counts against recognition: the self-score is unchanged after the swap.
