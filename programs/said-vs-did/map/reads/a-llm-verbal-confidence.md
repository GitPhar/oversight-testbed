# Reader A — LLM verbal confidence: numbers, words and calibration

2026-11-05 (America/Denver). Eleven assigned sources were read on arXiv HTML (`https://arxiv.org/html/<id>`) using a web-fetch tool. For long papers that tool reads only the first ~100,000 characters, so the appendix tail was not seen; those papers are marked partial. One web search returned three 2025–2026 hits. Each was checked on its arXiv abstract page (title, authors, dates, abstract), and only abstract content is recorded for them. No model API was called. Numbers come from the fetched text. A number visible only in a figure is noted and not given.

Depth tally: full 5 (Yona, Zhou 2023, Lin, Tian, Mielke); partial 6 (Kadavath, Zhou 2024, Xiong, Band, Steyvers, Kapoor); abstract 3 (Eikema, Cerda-Mardini, Petridis).

### Faithful hedging — Yona, Aharoni, Geva, 2024, arXiv preprint (v2), arXiv 2405.16908
- read_depth: full (HTML v2)
- what_tested:
  - Whether the hedging in an answer's wording matches the model's own uncertainty about that answer, on short-form knowledge QA.
  - Faithfulness of an assertion = 1 − |decisiveness − confidence|.
  - Decisiveness is how true the assertion seems from the wording alone, judged by Gemini Ultra with a few-shot prompt.
  - Confidence is the fraction of k=20 resampled answers that do not contradict the assertion.
  - Summary metrics: MFG (mean faithfulness) and cMFG (MFG conditioned on 10 confidence bins). A cMFG of 0.5 is what any strategy that ignores confidence gets.
- on_whom:
  - Models: Gemini Nano, Pro and Ultra; gpt-3.5-turbo; gpt-4-turbo.
  - Data: PopQA (n=932, filtered to non-ambiguous items) and the non-ambiguous subset of Natural Questions (n not found in text).
- how_scored: cMFG on non-punted answers. The confidence judge agreed with author labels at 0.97 on 100 examples.
- result:
  - Hedging: under vanilla decoding "all the models we tested did not generate any expressions of uncertainty".
  - Vanilla cMFG is about 0.52–0.57 for every model.
  - Prompting the model to hedge ("Uncertainty" prompt) raises the best cMFG to 0.70 (Gemini Ultra, PopQA). The few-shot "Uncertainty+" prompt gets 0.63 (GPT-4, PopQA).
  - Most other cells stay at 0.51–0.59. Table column order was inferred from the layout, and the text confirms the 0.70 and 0.63 values.
  - Punting rates: Vanilla 1%, Granularity 3%, Uncertainty 10%, Uncertainty+ 8%.
  - The decisiveness–confidence correlation is called "weak" (Fig. 4). No coefficient is given in the text.
- limits:
  - Covers only model (not data) uncertainty, and only explicit hedges.
  - Only closed models through an API, zero- and few-shot prompting, two QA datasets.
  - Confidence is defined by sample consistency, not by the model's own stated number. Words were never compared with a verbal number.
- borrow:
  - The decisiveness judge: an LLM reads only the wording and outputs P(true).
  - cMFG binned by confidence, with 0.5 as the confidence-blind baseline. This is the metric for any words-vs-number test of ours.
  - Here "confidence" would be our graded 0–100 rating, alongside or instead of resample agreement.
- next_steps_it_suggests:
  - Authors: data ambiguity; implicit vs explicit hedges; many-shot prompting; uncertainty estimates from internal representations.
  - For us: compare a Claude model's wording with its own stated 0–100 number for the same answer. Yona never did this. It is the cheapest direct reading of "says unsure / acts unsure" in language.
- transfer: transfers — same task type (short factual QA), black-box API method, and a metric that fits our ratings.

### Navigating the grey area — Zhou, Jurafsky, Hashimoto, 2023, arXiv v2 (venue not checked), arXiv 2302.13439
- read_depth: full (HTML v2)
- what_tested:
  - Whether certainty, uncertainty or evidential markers injected into a zero-shot prompt (50 templates, minimal pairs) change answer accuracy.
  - Whether models emit calibrated markers of their own (preliminary few-shot test, App. A.1).
  - Numeric certainty templates (§6).
- on_whom:
  - Models: GPT-3 ada, babbage, curie, davinci (main model); text-davinci-003; GPT-4.
  - Data: TriviaQA, Natural Questions (200 each), CountryQA (53), Jeopardy (200).
  - Also a Pile and Stack Exchange corpus analysis.
- how_scored: accuracy per template, ECE for the numeric templates, and macro-F1 of generated markers against correctness.
- result:
  - Accuracy on the same questions varies "by up to 80%" across templates (§4.1).
  - Weakeners average 47% accuracy and strengtheners 40% (four datasets).
  - TriviaQA: "I'm certain it's…" gets 42% and "I would need to double check but maybe it's…" gets 56%.
  - davinci on TriviaQA: Boosters 0.392 vs Hedges 0.468 (p<0.001); Factive verbs 0.347 vs Non-factive 0.468 (Table 1).
  - Numeric templates: ECE 0.30–0.50. "I'm 90% sure it's…" is correct 57% of the time on TriviaQA. In 21 of 28 templates, "100%" gave lower probability on the gold answer than "90%".
  - Generated markers: macro-F1 0.56 (uncertainty) and 0.53 (certainty) against a 0.45 random baseline. Accuracy is 74% with weakener generation vs 83% without.
- limits: older base models, few datasets, no multi-shot prompting, no long-form or dialogue, English only. The authors call calibration of generated markers weak.
- borrow:
  - Its "certainty marker as a prompt manipulation" design maps onto our transcript editing. Plant "I'm certain it's X" vs "maybe it's X" as the model's own earlier turn vs another person's, then measure the next 0–100 rating.
  - The finding that "100%" behaves worse than "90%" warns against reading 100 on our scale literally.
- next_steps_it_suggests:
  - Authors: multi-shot prompting, long-form generation, cross-lingual hedges, idiomatic vs literal markers.
  - For us: a planted hedge word is a cheap new arm for program 1's planted-number finding. Does a word move the model's later number as a planted number did?
- transfer: partly — old models and accuracy as the outcome, but the marker taxonomy and minimal-pair design transfer directly.

### Relying on the unreliable — Zhou, Hwang, Ren, Sap, 2024, arXiv v2 (venue not checked), arXiv 2401.06730
- read_depth: partial (main text and early appendix; last ~17k characters of appendix not read)
- what_tested:
  - How often LMs put certainty or uncertainty markers in answers, and how accurate marked answers are.
  - How people rely on markers, in a control setting plus calibrated, overconfident and underconfident interactive settings.
  - Whether RLHF reward models and preference data penalise uncertainty.
- on_whom:
  - Models: text-davinci-003, GPT-3.5-Turbo, GPT-4, LLaMA-2 7B/13B/70B, Claude-1, Claude-2, Claude-Instant-1.
  - Data: 284 MMLU questions × 49 prompts, 125,244 queries.
  - Humans: Prolific, n=25 in the control setting and 25 in each interactive setting.
  - Reward model: OpenAssistant deberta-v3-large-v2 on 183 QA pairs. Four preference datasets, including Anthropic HH.
- how_scored: regex marker coding; answer accuracy; user reliance (accept vs look up); reward-model scores.
- result:
  - Only 5% of base-template answers carry any marker (Table 1 gives 6%).
  - Marker emission rises to 16% with chain-of-thought and 65% with an explicit epistemic-marker prompt.
  - 20% of generations contain strengtheners and 14% weakeners.
  - 53% of strengthened answers are correct vs 32% of weakened ones, so words carry some signal. The abstract gives a 47% average error rate among confident responses.
  - Users rely on about 90% of strengthened answers and look up about 90% of weakened ones.
  - In the overconfident setting, users relied on incorrect confident answers 73% of the time.
  - Reward model mean scores: plain 4.03, strengtheners 0.82, weakeners −1.86.
  - Per-model breakdowns are figure-only.
- limits: English only; US participants; regex coding; recruited participants rather than real users. No numeric confidence was elicited alongside the words, so word–number agreement is not measured.
- borrow:
  - The strengthener/weakener regex lexicon, for coding Claude's free-text answers cheaply without a judge.
  - Their 5% base rate is the prior to beat when we look for spontaneous hedging on the hard pool.
- next_steps_it_suggests:
  - Authors: non-English hedging; online threshold adjustment; more varied training sources; a marker classifier; interventions on preference data.
  - For us: test whether the rare Claude hedges land on the items it rates low. Hedge rate by bins of the model's own 0–100 rating.
- transfer: transfers — includes Claude-family models, MMLU-style items and a cheap coding scheme.

### Uncertainty in words — Lin, Hilton, Evans, 2022, arXiv v2 (abstract page lists no venue), arXiv 2205.14334
- read_depth: full (HTML v2)
- what_tested:
  - Whether GPT-3, after finetuning, states calibrated confidence for its own arithmetic answers, as a number or in words.
  - Compared with the answer logit and an "indirect logit", under distribution shift (CalibratedMath, 21 sub-tasks).
- on_whom: GPT-3 175B (davinci). Finetuned on about 10k Add-subtract examples. Evaluation set sizes not stated.
- how_scored: MSE and MAD calibration error (in %) on shifted evaluation sets.
- result:
  - Trained on Add-subtract, verbalized numbers get MSE 22.0 / MAD 16.4 on Multi-answer. The answer logit gets 37.4 / 33.7 and the constant baseline 34.1 / 31.1.
  - On Multiply-divide, verbalized numbers get 15.5 / 19.0, vs answer logit 10.4 / 9.4 and constant 15.3 / 8.5. Verbalized numbers lose here (Table 1).
  - Verbalized words (greedy): Multi-answer 29.0 / 24.0; Multiply-divide 12.7 / 10.6 (Tables 2 and 4).
  - Ordered labels "lowest…highest" did no better than arbitrary names (App. B.1).
  - Few-shot curves are figure-only.
- limits: one model; arithmetic only; supervised finetuning; MAD is not a proper scoring rule; verbalized output can overfit to tokens seen in training.
- borrow:
  - The two-format design (number vs word category for the same answer) and the shift split: calibrate on one question family, test on another.
  - Our hard pool's science and factual halves can play the same role.
- next_steps_it_suggests:
  - Authors: other domains, models other than GPT-3, reinforcement learning, more diverse distributions.
  - For us: words vs numbers differ in calibration by shift condition, so any words-vs-number test should report both halves of the pool separately.
- transfer: partly — finetuned GPT-3 on arithmetic, but the number-vs-word comparison is ours to run unfinetuned.

### Know what they know — Kadavath et al., 2022, arXiv preprint (v4), arXiv 2207.05221
- read_depth: partial (main text and early appendix; last ~39k characters not read)
- what_tested:
  - Multiple-choice calibration.
  - P(True): the model judges its own sampled answer, optionally after seeing 5 of its own samples.
  - P(IK): a trained value head predicts whether the model will answer correctly. Tested out of distribution, with source documents and hints.
- on_whom:
  - Anthropic pretrained LMs at 800M, 3B, 12B and 52B; a brief look at RLHF policies.
  - Data: BIG-Bench MC, MMLU, TruthfulQA, LogiQA, QuALITY, TriviaQA, LAMBADA, HumanEval, GSM8k, arithmetic.
- how_scored: AUROC, Brier, ECE and RMS calibration error. ECE and RMS values are figure-only.
- result:
  - 52B P(IK), trained on all tasks except GSM8k: TriviaQA AUROC 0.873 / Brier 0.145; GSM8k 0.752 / 0.121 (Table 1).
  - P(IK) on an obscure question rises from 18% to 78% when a relevant Wikipedia article is prepended.
  - Self-knowledge vs difficulty: each 12B model's P(IK) is slightly higher on its own correct answers (0.463 vs 0.408; 0.477 vs 0.409), "only about 6%".
  - RLHF policies needed temperature T=2.5 to be calibrated.
- limits:
  - Pretrained models only. The probe signal is not a stated behaviour.
  - The authors did not test whether models act on or say this knowledge. They name deception as unaddressed.
  - P(IK) may partly reflect question difficulty.
- borrow:
  - The "show the model its own samples, then ask P(True)" variant. It is a transcript-editing arm we already have ("shown").
  - The cross-model own-vs-other comparison parallels program 1's judge × author result.
- next_steps_it_suggests:
  - Authors: return to natural-language P(IK); "distill calibration back into" natural-language answers.
  - For us: this is the classic statement that knowing is not saying. Nothing here links P(True) to hedging or abstaining.
- transfer: partly — base models with logit access, but its own-vs-other control matches our judge × author design.

### Just ask for calibration — Tian et al., 2023, arXiv v2 (venue not checked), arXiv 2305.14975
- read_depth: full (HTML v2)
- what_tested:
  - In RLHF models, verbalized confidence vs conditional token probability.
  - Variants: one-stage vs two-stage prompts, top-k guesses, chain-of-thought.
  - Linguistic expressions ("likely" etc.) mapped to numbers in two ways: by a human survey (Ling. 1S-human) or by measured held-out accuracy (Ling. 1S-opt).
- on_whom:
  - Models: gpt-3.5-turbo, gpt-4, claude-1, claude-2, Llama-2-70b-chat.
  - Data: TriviaQA (1,000), SciQ (1,000), TruthfulQA (817).
- how_scored: ECE, temperature-scaled ECE and Brier, and selective-prediction AUC. Correctness judged by GPT-4 or GPT-3.5.
- result:
  - gpt-3.5-turbo, TriviaQA: label prob ECE 0.140, AUC 0.869; Verb. 1S top-2 ECE 0.050, AUC 0.894.
  - SciQ: label prob 0.256; Ling. 1S-opt 0.064, but its AUC is 0.674 vs 0.752. Better calibration came with worse discrimination.
  - TruthfulQA: 0.451 vs Ling. 1S-opt 0.125.
  - gpt-4 SciQ: Ling. 1S-opt ECE 0.028 vs label prob 0.219.
  - Human-survey word mappings are less reliable. On Llama-2-70B, Ling. 1S-human TriviaQA ECE is 0.179, worse than label prob at 0.151.
  - Claude-1 "verbalizes poorly"; Claude-2 is "a bit stronger than gpt-3.5-turbo".
  - Expression usage rates are figure-only.
- limits: factual recall only; short-form; closed models; strong sensitivity to prompt format (1-stage vs 2-stage).
- borrow:
  - Ling. 1S-opt: fit each word's numeric value from the model's own accuracy when it uses that word. This gives a per-model word dictionary to set against its stated numbers.
  - Its prompt-format sensitivity is a confound we already know from program 1.
- next_steps_it_suggests:
  - Authors: find what makes verbalization calibrated; reduce format sensitivity; long-form; reasoning tasks.
  - For us: words are calibrated only once a mapping is learned from accuracy. The question is whether Claude's word for an answer agrees with its own number for the same answer.
- transfer: transfers — black-box, includes Claude models, same question types.

### Can LLMs express uncertainty — Xiong et al., 2024, arXiv v2 (venue not checked), arXiv 2306.13063
- read_depth: partial (main text and early appendix; last ~19k characters not read)
- what_tested: black-box confidence elicitation. Prompting (vanilla, CoT, self-probing, multi-step, top-k) × sampling (self-random, paraphrase, misleading) × aggregation (consistency, average confidence, pair-rank).
- on_whom:
  - Models: GPT-3, GPT-3.5-turbo, GPT-4, Vicuna 13B, LLaMA-2 70B.
  - Data: 8 datasets across 5 reasoning types (n not found in fetched text).
- how_scored: ECE, AUROC, AUPRC.
- result:
  - Vanilla verbalized ECE (×10², mean of 8 datasets): GPT-3 52.0, GPT-3.5 37.7, GPT-4 18.0.
  - GPT-4 AUROC is 62.7, "close to" random.
  - Confidences cluster at 80–100% in multiples of 5 (figure-only distributions).
  - GPT-4 with CoT on GSM8K gets ECE 0.064 by saying 100% for every sample, so low ECE need not mean discrimination.
  - GPT-3.5 Self-Random (M=5) vs CoT (M=1): ECE 18.7 vs 25.0, AUROC 73.0 vs 56.4. On GSM8K, AUROC goes 54.8→92.7.
- limits: unique-answer QA only. The authors say no method consistently wins, and all struggle on professional knowledge.
- borrow:
  - Always report AUROC next to ECE; the all-100% trap.
  - Resample agreement as a behaviour-side confidence to set against the stated number.
- next_steps_it_suggests:
  - Authors: mix black-box and white-box signals.
  - For us: agreement across samples is itself a behaviour. Does the stated number predict it? (Program 1 measured repeat consistency only as memory.)
- transfer: transfers — black-box API methods and our metric set.

### Linguistic calibration of dialogue — Mielke, Szlam, Dinan, Boureau, 2022, TACL (per arXiv comments field), arXiv 2012.14983
- read_depth: full (HTML v2)
- what_tested:
  - Whether BlenderBot's expressed confidence (annotated DK / LO / HI) matches correctness on closed-book TriviaQA.
  - A calibrator that predicts correctness from internal representations.
  - Controllable generation that forces the expressed confidence.
- on_whom:
  - BlenderBot 2.7B; TriviaQA (76,523 train / 9,961 valid).
  - Crowd annotation: 2,000 Train items × 1 annotator; 2,000 Valid × 3; 5,000 Test × 3.
- how_scored: human-annotated confidence class vs correctness; calibrator ECE.
- result:
  - Vanilla accuracy is 4.8%. 29.45% of answers are HI, and only 14% of HI answers are correct.
  - Calibrator ECE 0.018.
  - With calibrator-controlled generation, HI-answer correctness rises from 13.7% to 38.9% (p<10⁻⁶). Overall accuracy 4.8%→5.1% (n.s.).
  - Annotators all agree on the confidence class for only 43.60% of Valid items.
- limits: one weak model with very low accuracy; one dataset; DK vs LO hard to tell apart even for humans.
- borrow:
  - The three-class DK / LO / HI coding scheme for free-text answers.
  - The warning that human coders agree on confidence class less than half the time, so code with a fixed judge and report agreement.
- next_steps_it_suggests:
  - Authors: build calibration into the model by retraining; consider the whole response distribution.
  - For us: confidence words can be fixed after the fact by a separate predictor. The words and the knowledge are separable channels.
- transfer: partly — 2020-era chit-chat model, but the coding scheme and annotation-agreement caution transfer.

### Linguistic calibration of long-form — Band, Li, Ma, Hashimoto, 2024, arXiv v2 (venue not checked), arXiv 2404.00474
- read_depth: partial (main text; appendix D with human-study n and agreement statistics not read)
- what_tested:
  - Training Llama 2 7B (SFT, then decision-based RL) so its long-form text lets a reader make calibrated forecasts on related questions.
  - Scored by a surrogate reader's log loss.
- on_whom:
  - Llama 2 7B.
  - Data: TriviaQA (in-distribution); Jeopardy, SciQ, BioASQ (out of distribution); 500 FactScore biographies.
  - Human readers (n in App. D, not read).
- how_scored: the reader's forecast ECE and accuracy.
- result:
  - TriviaQA ECE with human readers: 0.163 (SFT) vs 0.116 (RL). With a simulated reader: 0.166 vs 0.108.
  - Biographies: 0.301 vs 0.266.
  - These values are taken from figure captions. Accuracy frontiers are figure-only.
- limits: white-box finetuning only; mostly unambiguous percentage statements; QA as a proxy for decisions.
- borrow: the reader-forecast definition of calibration. A downstream reader's use of the words is the target, which is a behaviour-facing metric. A Claude judge can act as the reader.
- next_steps_it_suggests:
  - Authors: how humans vs LMs read ambiguous confidence words; decision-relevant QA.
  - For us: needs finetuning we cannot do. Only the metric is borrowed.
- transfer: partly — training method is out of reach; the reader metric transfers.

### What LLMs know vs what people think — Steyvers et al., 2025, Nature Machine Intelligence (arXiv v2, 13 Feb 2025, verified on abstract page), arXiv 2401.13835
- read_depth: partial (main text and appendices to ~100k of 109k characters)
- what_tested:
  - Calibration and discrimination gaps between people's confidence in LLM answers and the model's internal (token-probability) confidence.
  - Effects of explanation length and of hedge phrases written into explanations.
- on_whom:
  - Models: GPT-3.5, PaLM2, GPT-4o-mini.
  - Data: 350 MMLU and 336 TriviaQA questions.
  - 301 Prolific participants (41–60 per experiment), plus 81 in Experiment 3.
- how_scored: ECE and AUC for model and humans; Bayes factors for comparisons.
- result:
  - Model AUC: 0.751 (GPT-3.5), 0.746 (PaLM2), 0.781 (GPT-4o).
  - Human AUC with default explanations: 0.589, 0.602, 0.592.
  - ECE, model vs human: .104 vs .264; .154 vs .291; .141 vs .165.
  - Explanations rewritten with "I am not sure / somewhat sure / sure", using thresholds on model confidence, raise human AUC to .652–.694 and lower ECE to .111–.225.
  - Long vs short explanations raise confidence (BF=25) without better discrimination.
- limits: MC and short-answer only; two-prompt pipeline. Confidence comes from token probability, not the model's own words.
- borrow: the three-level phrase set and thresholding, as a fixed hedge scale for a judge to code Claude's answers. Also explanation length as a confound for decisiveness scoring.
- next_steps_it_suggests:
  - Authors: longer open-ended questions; one-step generation; root causes (RLHF preference bias, answer commitment).
  - For us: people read the words, not the number. The overseer-facing quantity is the wording, which is why words-vs-number agreement matters.
- transfer: partly — human-reader study, but the phrase scale and length confound transfer.

### Must be taught — Kapoor et al., 2024, arXiv v3 (venue not checked), arXiv 2406.08391
- read_depth: partial (main text and early appendix; last ~32k characters not read)
- what_tested:
  - Whether prompting gives good uncertainty for open-ended answers.
  - Finetuning on graded correct/incorrect examples (probe, LoRA, LoRA+prompt).
  - Transfer across subject and format; cross-model uncertainty estimation; a user study.
- on_whom:
  - Models: LLaMA-2 7B/13B, Mistral 7B and their instruct variants.
  - Data: ~20,000 training examples from 16 benchmarks; MMLU; SelfAware; LiveCodeBench (62).
  - User study: n=181.
- how_scored: ECE and AUROC; human reliance in the user study.
- result:
  - KL-regularised tuning lowers mean ECE from 29.9% to 10.8% across six models, with AUROC 70.2%→71.6% (Table 1).
  - About 1,000 labelled examples suffice to beat baselines.
  - Most method comparisons, cross-model heatmaps and user-study effects are figure-only.
- limits: open-weight models only; GPT-3.5 used as grader; user study preliminary and numeric-only.
- borrow:
  - The cross-model finding (one model's features estimate another's correctness) restates program 1's AUROC 0.93 vs 0.85 result.
  - Cite it as prior support. There is nothing new to run.
- next_steps_it_suggests:
  - Authors: one model that answers and estimates; confidence-based rewards.
  - For us: none beyond the cross-model control.
- transfer: partly — finetuning is out of reach; the cross-model result corroborates program 1.

### 2025–2026 search hits
Search: "LLM verbal hedging words consistency with numeric confidence faithful uncertainty expression 2025 arXiv" (one search). Three hits recorded. Each was verified on its arXiv abstract page before recording, and only the abstract was read.

### Faithful Uncertainty Tuning — Eikema, Ilia, de Souza, Zerva, Aziz, 2025, arXiv preprint (v1, 14 Oct 2025, verified), arXiv 2510.12587
- read_depth: abstract (verification pass only; full text not opened within the one-search budget)
- what_tested:
  - The "faithfulness gap": answers are unhedged, or hedged in ways that do not reflect variability across repeated queries.
  - Faithful Uncertainty Tuning (FUT) finetunes on the model's own samples, with hedges ("possibly", "likely") matched to sample consistency.
- on_whom: "multiple models and datasets", open-domain QA. Names not in the abstract.
- how_scored: not stated in the abstract.
- result: no numbers in the abstract. It claims a substantially reduced faithfulness gap, preserved accuracy, robustness to the choice of hedge words, and extension to numerical expressions.
- limits: abstract only; finetuning method.
- borrow: the claim that the gap "affects even strong LLMs" is a prediction we can check on Claude without finetuning, using Yona's metric.
- next_steps_it_suggests: if read in full, its hedge-vs-number analysis is the closest published words-vs-number comparison. Worth a full read before we design the test.
- transfer: partly — method needs finetuning; the definition of the gap transfers.

### Consistent but miscalibrated — Cerda-Mardini, Chandar, Madathil, 2026, arXiv preprint (v2, 10 Jul 2026, verified), arXiv 2607.03882
- read_depth: abstract
- what_tested:
  - Nine LLMs pick a verbal descriptor for a given probability and uncertainty, drawn from Beta distributions.
  - Six domain contexts, ten temperatures, ten repeats.
- on_whom: nine LLMs (names not in the abstract).
- how_scored: consistency and calibration of chosen descriptors. Details not in the abstract.
- result: no numbers in the abstract. Models are consistent but miscalibrated, and weaker on uncertainty than on likelihood. Giving precomputed parameters does not fix the miscalibration, which the authors attribute to the verbalization step.
- limits: abstract only. The numbers are external, not the model's own confidence.
- borrow: the "number → word" direction as a task. Give a Claude model its own earlier 0–100 rating and ask for the matching word. This separates translation error from self-knowledge error.
- next_steps_it_suggests: verbalization can be miscalibrated even when the number is handed over, so a words-vs-number gap is not automatically a gap in self-knowledge. Control for it.
- transfer: partly — translation of given numbers, not self-reported confidence.

### How unlikely is "unlikely" — Petridis, Pelechrinis, Obradovic, 2026, arXiv preprint (v1, 26 Aug 2026, verified), arXiv 2608.26327
- read_depth: abstract
- what_tested:
  - Word → number mapping for 11 verbal probability expressions across 19 models, against human benchmarks.
  - Two settings: forced single number vs with explanation.
  - A "roundtrip" test (word → number → word) of internal consistency.
- on_whom: 19 models (names not in the abstract).
- how_scored: agreement with human norms and roundtrip coherence. Details not in the abstract.
- result:
  - No numbers in the abstract.
  - Models keep the human ordering and recover three anchor points. "Possible" has the highest variance.
  - There is a systematic upward bias on "unlikely" and "improbable".
  - Explanations cut variance within a model but increase divergence between models.
  - Frontier models are coherent in both directions.
- limits: abstract only; the dictionary task does not involve the model's own answers.
- borrow: the roundtrip test as a cheap per-model dictionary. We need each Claude model's own word → number mapping before scoring whether its hedges match its ratings.
- next_steps_it_suggests: build the dictionary first (a few dozen calls). The negative-end bias predicts that Claude's "unlikely" will read as a higher number than people take it to mean.
- transfer: transfers — cheap, black-box, and needed as a calibration step for our words-vs-number test.

## Cluster summary

**Settled:**
- Without prompting, RLHF models almost never hedge. Zhou 2024 found markers in 5% of base answers. Yona found none under vanilla decoding.
- When verbalized confidence is asked for, the numbers cluster at 80–100 and are overconfident (Xiong). They can still beat token probabilities on ECE (Tian), but ECE can look good while discrimination stays near chance (Xiong; Tian SciQ).
- Hedge words, when present, carry some signal: 53% vs 32% accuracy for strengthened vs weakened answers (Zhou 2024). Their match to the model's own resample consistency is weak, with cMFG about 0.52–0.70 against a 0.5 baseline (Yona).
- Words become calibrated only once a mapping is fitted from accuracy (Tian Ling-opt), or after finetuning (Lin, Mielke, Band, Kapoor, Eikema).
- People act on the words and the length of the explanation, not on a number (Steyvers; Zhou 2024).
- Older Claude models are in the data: Claude-1 verbalizes poorly and Claude-2 does better (Tian). Claude-1, Claude-2 and Claude-Instant appear in Zhou 2024 (per-model values figure-only).

**Not looked at, and reachable cheaply with our instruments:**
1. **Within-model agreement between a model's words and its own stated number for the same answer.** Yona compares words with resample consistency. Tian compares words with accuracy through a fitted mapping. Petridis and Cerda-Mardini map words to numbers outside any self-report. No source read here scores a Claude answer's hedging against that model's own 0–100 rating for the same item.
2. **Whether transcript manipulations move words and numbers together.** Program 1 found planted own-numbers taken up. Zhou 2023 shows markers in the prompt change accuracy, but no one plants a hedge as the model's own earlier turn.
3. **Whether either channel predicts a behaviour** (abstaining, asking, holding an answer under pushback). This is an empty field in this cluster. Every source scores calibration against correctness or a reader's forecast, not against the model's own next action. That is cluster B's ground.
4. **Current Claude models.** None of these sources tests any Claude model newer than Claude-2.

**Fields that returned nothing:**
- No source tested whether stated confidence predicts the model's later actions.
- No source compared hedges with the same model's verbal number on the same item.
- No source tested hedge words under transcript or attribution manipulation.

## Candidate next steps

Call counts are given, not dollar figures. Each step's cost should be checked with a short cost probe before running, against the program's $5 total and about $1.50 per test.

1. **Words vs own number (Yona's metric with our rating as confidence).**
   - Setup: 100 hard-pool items × 3 models. Call 1: free-text answer with no confidence request. Call 2 (fresh context, answer shown as the model's own): graded 0–100 rating. Haiku scores decisiveness from the wording alone; the decisiveness judge is fixed across all models.
   - Calls: about 600 answer/rating calls plus 300 short Haiku judge calls.
   - Metric: cMFG of decisiveness against the rating, and the hedge rate by rating quartile.
   - Counts against "words don't match numbers": cMFG ≥ 0.75 on all three models, with hedge rate in the bottom rating quartile at least 3× the top quartile.
   - Counts against "words track numbers": cMFG ≤ 0.55, as Yona's vanilla rows found.
2. **Per-model hedge dictionary and roundtrip (Petridis / Tian Ling-opt).**
   - Setup: each model maps 11 hedge words to 0–100 (5 repeats) and maps 10 numbers back to words. That gives about 60 calls per model, about 180 in total, all short.
   - Use the dictionary to convert step 1's hedges into numbers, then compare each with the stated rating.
   - Counts against using hedges as a confidence channel: dictionary-mapped hedge values differ from the same item's stated rating by more than 20 points on average. A stable roundtrip (word → number → same word ≥ 90%) would mean any step-1 gap is not a vocabulary problem.
3. **Planted hedge vs planted number (Zhou 2023 markers × program 1's planted-answer arm).**
   - Setup: 60 items. Plant the model's own earlier answer with "I'm certain it's X", "maybe it's X", or a plain "X". Also credit the same wording to another person. Then take a 0–100 rating.
   - Calls: 6 arms × 60 × 3 models ≈ 1,080 short calls. Run Opus on a 30-item subset if the probe says cost is high.
   - Counts against "words are a live channel": the own-attributed certain-vs-maybe shift is under 5 points while a planted number moved the rating in program 1. A shift of the same size as the number-plant would mean the word works like the number.
4. **Does asking for a number change the words?** (Tian's format sensitivity)
   - Setup: same 100 items. Free-text answer with vs without "also give 0–100 confidence" in the same turn; score decisiveness for both.
   - Calls: about 600.
   - Counts against "reporting a number changes the words": mean decisiveness differs by less than 0.05 and hedge rate by less than 3 points between conditions.
5. **Resample consistency as behaviour (Xiong self-random, Kadavath "shown").**
   - Setup: 50 items × 5 samples at temperature 1 on Haiku and Sonnet, and 3 on Opus. Ask whether the stated rating from a separate call predicts sample agreement.
   - Calls: about 650.
   - Counts against the number predicting this behaviour: AUROC of the rating for predicting majority agreement is under 0.6.
