# Prior work lines brought up to date: SV-8 and SV-12

Written 2026-11-05 (America/Denver) by a fresh subagent (claude-opus-5-5) that ran none of program 7's bets, pre-registrations or audits. Web reads only (WebSearch, WebFetch; arXiv PDFs without HTML were downloaded and converted with `pdftotext` in the session scratchpad). No model API was called and no local model was loaded. Every number below was checked against the paper's own text in this session. Format: `operators/scout.md` Step 2 (Read records) and Step 4 (the Prior work line).

**The two directions.**
- **SV-8**: does what the model does (backing down under "are you sure?", or passing under a penalty) add information about whether its stated belief is wrong, beyond the stated confidence itself? Measured as held-out log-loss of correctness with and without the behaviour. Draft pass rule (`odds-elicitation/rows-v1.md`): on at least 2 of 3 models, adding the behaviour improves held-out log-loss for correctness by at least 5%, with the CI above 0.
- **SV-12**: refit program 1's six-format data (Claude Haiku 5.5: a 0-100 rating, yes/no, buy a $100 ticket at a price, more likely than a coin, how many of 100 would be true, a 7-point verbal scale; 160 claims x 10 repeats) with Smolin and Wilder's single-latent model (per-format offset and slope), and score held-out-format concordance (their concordance index, macro-averaged over held-out formats). Hit if at least 0.85.

**Current lines, as checked.** SV-8's numbers for Yamin et al. are correct as written. Its Smolin and Wilder clause needs a qualifier: the under-5% figure conditions on the latent inferred from all 16 outputs, not on the stated number. SV-12's "0.8 to 0.95" is the reports-versus-decisions group holdout, not a held-out single format; the single-output holdout is in a figure only (details below).

## Searches

One line per search: terms; where; date.

1. `"outcome sufficiency" OR "sufficient statistic" elicited beliefs LLM actions reveal more than stated confidence 2026 arXiv Yamin Wilder follow-up`; WebSearch (standard); 2026-11-05. Hits: 2602.06286 (re-read), 2605.08556 (new; abstract read), 2511.13240 and 2608.24691 (already in the program's reads).
2. `abstention or answer flip as error signal beyond verbalized confidence LLM correctness prediction combine behavioral signals 2026`; WebSearch; 2026-11-05. Hits: 2604.22271 (new; read in part), 2606.29490 (read in full for `remap-2026-11-05-sv-b2.md`), 2603.22161 (already read).
3. `"Beliefs and Behavior in Language Models" Smolin Wilder latent belief concordance Claude`; WebSearch; 2026-11-05. Only the paper itself, plus 2511.01805 (belief shifts with context; not a refit; not opened). No paper refitting Claude data with the model was found.
4. `single latent belief across elicitation formats LLM coherence probability Likert betting Claude 2026 latent variable model credence`; WebSearch; 2026-11-05. Hits: Andrews & Sarkar 2026 (MIT economics PDF; new; read in part), 2405.21030 (conceptual; not opened), 2507.17951 (Bayesian updating; not opened), 2606.11016 (alphaxiv summary only; not opened). None refits Claude format data with a single latent.
5. Direct opens, 2026-11-05: arxiv.org/abs/2602.06286 (v1 6 Feb, v2 8 May, v3 7 Sep 2026) and /html/2602.06286v3; arxiv.org/abs/2609.07943 (v1 7 Sep 2026 only; no HTML) and the full PDF via curl and pdftotext; arxiv.org/abs/2605.08556; arxiv.org/abs and /html for 2604.22271; economics.mit.edu/sites/default/files/2026-09/main_0.pdf.

## Read records

### Beliefs and behavior in language models — Alex Smolin & Bryan Wilder, 2026, arXiv preprint, arXiv 2609.07943 (verified: v1 7 Sep 2026, only version; PDF only)
- read_depth: full for the parts SV-8 and SV-12 touch (PDF via pdftotext: main text, Supplementary A.1-A.5, C and D, figure captions); prompt catalogue E skimmed. Most per-model values are in figures only, and no figure value is reported here.
- what_tested: whether one scalar latent belief z per case, inferred from some of a model's outputs, predicts its other outputs.
- on_whom: Gemma 3 4B / 12B / 27B, Llama 3.1 70B, Qwen3 32B, DeepSeek V3.2, GLM-5, GPT-5.6 Luna, GPT-5.6 Terra (no Claude). Three domains (CKD screening, Werewolf, forecasting social-science experiments), 500 cases each. For each case and model, **one response per output** at temperature 1: one numerical probability, thirteen binary decisions (one plain decision, four threshold, four bet and four cost framings, with r in {2, 4, 9, 19}), and two five-category ordinal judgments (Likert, probability quintile). Complete-case retention 63.0-100%. Split about 64/16/20 train/validation/test by case, per model-domain cell.
- how_scored (the concordance index, from §Results and A.3): "the fraction of cases in which the true targets are correctly ranked by the predictions", which generalises AUROC to any output type. **Pairs are pairs of test cases**, one observed response per case and target. Concordance is computed separately for each held-out target and macro-averaged over targets, "excluding pairs tied on the observed target and assigning half credit when predictions tie". For a binary target it is therefore AUROC; the paper calls it AUROC where all targets are binary. Predictions are posterior-predictive expectations (expected category for ordinal outputs), with the latent inferred only from the observed group and the observation model not refitted.
- model: z's prior is a fitted log-density, piecewise linear in logit(z). The numerical probability is Beta(zφ, (1-z)φ), which anchors z's scale (E = z). Each binary output has logit Pr = α_j + β_j logit(z), with β_j > 0 and the nominal threshold not imposed. Each ordinal output is a proportional-odds logit with its own cutpoints and slope. Fitting is by maximum marginal likelihood (128-point Gauss-Legendre quadrature).
- result: in the primary analysis the held-out set is a **group**: all 13 decisions predicted from the three probability reports, or the reverse. For highly capable models, concordance is 0.8-0.95 and R² 60-90%; "Less capable LLMs score much less highly", with no per-model number in the text. Zero-shot across framings and domains: AUCs close to 1 for the most capable, much worse for weak models. The single numerical probability carries over 90% of the latent's excess concordance for the best models, much less for weak ones. A **single-output holdout** (H = one target, O = the other fifteen) appears only as the sensitivity comparison in Figure 7 (values in the figure only); a 1-D monotone spline and a 2-D latent gave nearly identical performance. Outcome sufficiency (Supplementary D): the normalised L1 statistic E|Cov(Y, D | Z)| / P(Y = 1), with **Z the posterior mean from all responses**, is "below 5% in relative terms" for highly capable models (figure). Quote: "excluding pairs tied on the observed target and assigning half credit when predictions tie".
- limits: no Claude; one response per case (no repeats); every decision is about the world; reasoning before every answer; per-output affine freedom means a format with a fixed offset still counts as coherent.
- borrow (SV-12): (1) map program 1's formats onto their observation families. The 0-100 rating is the Beta anchor; yes/no, the coin comparison and the ticket purchase are binary logits; the 7-point scale is an ordered logit; "how many of 100" is a second numeric report or a binned ordinal. (2) Their concordance is per case with one response. Program 1 has 10 repeats per claim, so the pre-registration must choose: score each repeat as a separate test row sharing its claim's z (pairs across claims only), or score the claim-mean response. These are not the same statistic. (3) A 20% test split of 160 claims is 32 claims, so cross-validated folds would give a usable interval. (4) Hold out the 0-100 rating only with care: it anchors z's scale. (SV-8): their outcome-sufficiency statistic conditions on the all-response latent, so it answers "is the latent sufficient", not "is the stated number sufficient".
- next_steps_it_suggests: authors: beyond single-shot binary decisions. For us: SV-12 asks whether "Haiku has no single credence" (program 1) is a disagreement about the criterion or about the model.
- predicts_for_us: SV-12: mixed (capable models reach 0.8-0.95 on group holdouts; weak models much lower; no rule places Haiku 5.5; the single-format holdout SV-12 uses has no number in the text). SV-8: weakly fail-leaning for capable models (a latent built from many outputs leaves under 5% relative outcome dependence in decisions), but that is not the stated number, and the decisions are world-directed.
- remap head: **design to borrow** for SV-12 (observation model, concordance definition, the repeats choice); for SV-8 a **correction**: the under-5% figure is not a test of the stated number's sufficiency.

### When agents say one thing and do another — Khurram Yamin, Jingjing Tang, Santiago Cortes-Gomez, Amit Sharma, Eric Horvitz & Bryan Wilder, 2026, arXiv preprint, arXiv 2602.06286 (verified: v1 6 Feb 2026, v2 8 May 2026, v3 7 Sep 2026)
- read_depth: partial (arXiv HTML v3, first 100,000 of 171,254 characters: framework, methods, Table 1 and main results; appendix tables not re-read)
- what_tested: whether an LLM's elicited probability is a sufficient summary of what its decisions reveal: sufficiency I(A; θ | p) = 0, monotonicity, iterated-expectation coherence, stability. Beliefs and actions are elicited "in separate context windows".
- on_whom: GPT-5 (minimal and high reasoning), DeepSeek-R1 671B, Llama-4 Scout 17B; four medical diagnosis tasks (structural heart disease, diabetes, and two expert pediatric Bayesian networks, fever and crying); 200 covariate-outcome pairs with five repetitions per task; actions: diagnose positive, diagnose negative, or defer.
- how_scored: kNN (k = 3) conditional mutual information with 500-resample bootstrap CIs; cross-validated random forest predicting the realised state θ from p alone against (A, p), reported as the relative reduction in MSE. **No log-loss is used.**
- result: "all model–dataset pairs reject the null", 16 of 16, with CIs strictly above zero. The average random-forest improvement from adding the action was GPT-5 minimal 6.15% [-1.22, 13.52], GPT-5 high 4.89% [1.25, 8.53], Llama 15.19% [6.11, 24.27], DeepSeek-R1 5.11% [-4.83, 15.06]. Only GPT-5 high and Llama have intervals excluding zero. By task: heart disease 16.33 [11.81, 20.85], crying 5.21 [-0.03, 10.45], fever 2.07 [0.30, 3.85], diabetes 7.73 [-4.93, 20.38]. Quote: "eliciting beliefs and actions in separate context windows".
- limits: no Claude; one clinical framing; the action is deferral in a vignette, not pushback or a pass under a stated penalty; MSE of the state, not log-loss of the model's correctness; the remaining 71k characters were not re-read this session.
- borrow: the nested comparison (p alone against p plus the action, cross-validated) is SV-8's design. SV-8 should report MSE (Brier) improvement alongside log-loss, so its number can be set next to theirs.
- next_steps_it_suggests: authors: validate elicited probabilities empirically rather than assume them.
- predicts_for_us: SV-8: mixed (improvements of 4.89-15.19% straddle the 5% bar, and two of four models' intervals include zero; the 2-of-3-models-with-CI-above-0 rule would have passed only narrowly on their data).
- remap head: **already shown** in direction (actions carry information beyond the stated probability), on non-Claude models with a deferral action. SV-8 adds Claude, pushback and pass actions, and log-loss.

### How LLMs detect and correct their own errors — Dharshan Kumaran, Viorica Patraucean, Simon Osindero, Petar Veličković & Nathaniel Daw, 2026, arXiv preprint, arXiv 2604.22271 (verified: v1 24 Apr 2026, v2 1 May 2026)
- read_depth: partial (arXiv HTML v2, first 100,000 of 159,094 characters: paradigm, behavioural results, probe and causal results)
- what_tested: a verify-then-correct paradigm. A TriviaQA answer and a 10-class verbal confidence (Phase 0); a fresh prompt asking "Verify your answer. Correct? (Y/N)" without the confidence (Phase 1); then a corrected answer (Phase 2). Also whether a post-answer activation (PANL) predicts error detection and correction beyond behaviour.
- on_whom: Gemma 3 27B (TriviaQA n = 7,227; MNLI dev n = 9,888, neutral 3,395), Qwen 2.5 7B (TriviaQA n = 3,500).
- how_scored: AUROC; likelihood-ratio tests of nested logistic models; d′ for error detection.
- result: first-attempt accuracy 75.5%, second 79.2%. Verbal confidence predicted first-answer correctness at AUROC 0.74 (log-probability 0.76). The model endorsed 98% of correct answers and 68% of wrong ones (d′ = 1.67). Verbal confidence predicted the Y/N verification response far beyond log-probability (.668 to .832; LR χ² = 839.4). Correction success among changed wrong answers was near chance for behavioural signals (verbal confidence .524). Quote: "verbal confidence predicts error detection far beyond token log-probabilities".
- limits: no test of whether the verification behaviour predicts correctness *beyond* verbal confidence (the direction SV-8 needs); two open models; no Claude.
- borrow: the Y/N self-verification is a third cheap "did" behaviour for SV-8's nested comparison, measured in a fresh context like ours.
- next_steps_it_suggests: authors: reasoning settings; more models.
- predicts_for_us: SV-8: no direct bearing (the needed comparison is not reported). Its finding that verification follows verbal confidence closely suggests the action may add little beyond the number, a weak fail-lean.
- remap head: **changes nothing** for the SV-8 line (the comparison SV-8 needs is not in the paper). It records a possible extra behaviour.

### Reported confidence tracks commitment more than correctness — Kumaran, 2026, arXiv 2606.29490 (full Read record in `remap-2026-11-05-sv-b2.md`)
- bearing on SV-8 only: on SimpleQA, abstention was higher after wrong answers than after right ones in every non-reasoning cell (Δ +0.028 to +0.195). Across the non-reasoning cells, verbal confidence residualised on log-probability kept tracking abstention while its link to correctness fell to chance (residual correctness AUROC median 0.49). So abstention carries correctness information that is not all routed through the verbal number. No log-loss comparison with and without the action is reported.
- predicts_for_us: SV-8: pass-leaning in direction (the action is partly driven by a correctness-tracking signal the verbal number lacks), with no size reported.
- remap head: **rival named** for SV-8's interpretation: if the action adds information, it may come from a log-probability-like signal rather than from "behaviour knowing more than words". SV-8 cannot separate these without logits, which Claude's API does not give; say so in the pre-registration.

### Dutch books for language models — Isaiah Andrews & Suproteem Sarkar, 2026, working paper, https://economics.mit.edu/sites/default/files/2026-09/main_0.pdf (MIT site, dated 2026-09; no arXiv id checked)
- read_depth: partial (PDF via pdftotext: abstract, §1, §4.1-4.2, model list; elicitation-variant results skimmed; per-model values in figures only)
- what_tested: coherence of probability forecasts over logically related events (stock-return bins, unions, complements), scored by the largest guaranteed Dutch-book profit per unit stake; no outcome labels needed.
- on_whom: 15 models including Claude Opus 4.7, Claude Opus 4.8, Claude Sonnet 5, Claude Opus 5, Claude Fable 5; 100 stock-days; 365,100 elicitations.
- result: baseline profit 0.002067 per unit stake for GPT-OSS-120B (95% CI [0.001471, 0.002737]); profit varies about 100-fold across models (0.002067 to 0.1994), while Brier scores range only 0.1966-0.2157 (Spearman 0.9143 between the two rankings). Quote: "irrelevant contextual details can increase incoherence by an order of magnitude".
- limits: coherence across events, not across elicitation formats for one event; no latent-belief refit; Claude values in a figure only.
- predicts_for_us: SV-12: no bearing on the pass rule (a different coherence notion); it confirms that recent Claude models' probabilistic coherence depends on the elicitation protocol, which is program 1's finding in another form.
- remap head: **changes nothing** for SV-12 (not a single-latent, cross-format refit).

### Can revealed preferences clarify LLM alignment and steering? — Yamin, Tang, Horvitz & Wilder, 2026, arXiv 2605.08556 (verified: v1 8 May 2026, v2 7 Sep 2026)
- read_depth: abstract (abstract page only)
- what it says: fits a discrete choice model to elicited probabilities and actions in four medical diagnosis domains; models are often internally consistent but misreport their own preferences and do not reliably adopt instructed ones. No numbers in the abstract.
- predicts_for_us: SV-8, SV-12: no bearing (preferences, not belief sufficiency or format coherence).
- remap head: **changes nothing**.

## SV-8: what each paper opened predicts for the pass rule

- Yamin et al. 2026 (2602.06286): mixed. Actions add 4.89-15.19% (MSE), straddling the 5% bar, and two of four intervals include zero.
- Smolin & Wilder 2026 (2609.07943): weakly fail for capable models, but it conditions on an all-response latent, not on the stated number, and uses world-directed decisions.
- Kumaran 2026 (2606.29490): pass-leaning in direction (abstention tracks correctness partly outside the verbal number); no size.
- Kumaran et al. 2026 (2604.22271): no direct bearing; verification follows verbal confidence closely.

**Proposed Prior work line (SV-8):** Mixed, straddling the bar. Yamin et al. 2026 (arXiv 2602.06286 v3; GPT-5 minimal/high, DeepSeek-R1, Llama-4 Scout; clinical diagnose-or-defer, separate contexts): sufficiency rejected in all 16 cells; adding the action cut random-forest MSE by 6.15, 4.89, 5.11 and 15.19%, intervals above zero only for GPT-5-high and Llama. Smolin and Wilder's under-5% residual conditions on an all-output latent, not the stated number. Adds Claude, pushback, log-loss.

**prior_work_predicts (SV-8):** mixed

## SV-12: what each paper opened predicts for the pass rule

- Smolin & Wilder 2026 (2609.07943): mixed. Capable models reach 0.8-0.95 on group holdouts; weak models score "much less highly"; single-format holdout values are in a figure only; no Claude.
- Andrews & Sarkar 2026: no bearing (event coherence, not format coherence); protocol dependence on Claude models.
- No paper since has refit Claude data with the single-latent model (searches 3 and 4).

**Proposed Prior work line (SV-12):** Mixed. Smolin and Wilder 2026 (arXiv 2609.07943; nine models, no Claude; one response per case and output, per-output offset and slope): concordance (pairs tied on the target dropped, prediction ties half credit, macro-averaged) reached 0.8-0.95 for capable models, but on reports-versus-decisions group holdouts; single-output holdouts are figure-only, and weak models score "much less highly". Where Haiku 5.5 falls is not in print. Adds a Claude refit (none found).

**prior_work_predicts (SV-12):** mixed
