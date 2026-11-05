# Re-scout around em-gm3c (predict each answer format from the other five)

- **Bet:** em-gm3c · **Program:** entangled-mind (program 1) · **Map node:** gm3c
- **The result in one sentence:** On Haiku's 160 claims the other five answer formats recover about 40% of what is reproducible in a sixth format (mean Q 0.39 [0.30, 0.50]; 0.40-0.44 on the audit's refits), so "little" against "partial" format-free belief is undetermined, while a usable single belief (Q above 0.75) is firmly excluded.
- **Date:** 2026-11-05 16:29 MST (from `date`)
- **Read by:** claude-opus-5-5, a fresh reader subagent of the 2026-11-05c remap session. Web reads only (WebSearch, WebFetch; PDFs WebFetch could not parse were converted with `pdftotext` in the session scratchpad). No model API, no experiment, no local model.

**What the result now raises.** The audit's firm part is that each format's reproducible answer is mostly not shared with the other five. The ceiling it is measured against is the *same prompt* repeated. So the result cannot yet say whether the unshared part belongs to the *format* (rating against yes/no against bet) or to *any change of wording*: a reworded prompt of the same format might recover no more than another format does. That rival, and whether a second latent dimension would absorb the unshared part, are what this re-scout searched for.

**Already in the program's reads and not counted as new:** Smolin and Wilder 2026 (2609.07943), Kim and Kang 2026 (2605.27752), Lei and Cooper 2026 (2605.04764) (`novelty-2026-11-05-em-gm3c.md`). Smolin and Wilder is re-read below for two parts the earlier read did not report: how their 16 outputs are built (near-duplicate framing families) and their two-dimensional latent check.

## Searches

One line per search: terms; where; date.

1. `LLM belief consistency paraphrase same question format versus different elicitation format probability rating`; WebSearch (standard); 2026-11-05. Hits: 2405.21030 (read), WASSA 2026 paraphrase paper (read), 2508.16846, 2511.13240, 2608.26327 (not opened). The search tool's own summary: no study crosses paraphrase with elicitation format.
2. `multitrait-multimethod LLM psychometrics method variance response format convergent validity language model`; WebSearch; 2026-11-05. Hits: 2307.00184 (MTMM across two personality inventories), 2510.11254, 2603.11279 (not opened); no LLM study treating response format as an MTMM method facet.
3. `Mizrahi "State of What Art" multi-prompt evaluation paraphrase instruction templates variance arXiv 2401.00595`; WebSearch; 2026-11-05. Benchmark-accuracy paraphrase variance; not opened (accuracy, not credence).
4. `"Measuring LLMs Sensitivity to Paraphrased Opinion Prompts" WASSA 2026`; WebSearch; 2026-11-05. ACL Anthology 2026.wassa-1.5 (read).
5. `Haller Vamvas Jäger 2024 "Yes, no, maybe?" response stability under paraphrasing political leaning arXiv`; WebSearch; 2026-11-05. COLM 2024 paper, no arXiv id found; 2504.17052 opened and found not to transfer (political stance under argument, no format arm).
6. Direct opens, 2026-11-05: aclanthology.org/2026.wassa-1.5.pdf (pdftotext, all 6 pages); arxiv.org/pdf/2609.07943 (pdftotext, 1,875 lines; sections Action spaces, Results, A.1, A.4 read); arxiv.org/html/2406.12334 (first 100,000 characters); arxiv.org/html/2405.21030; arxiv.org/html/2504.17052v3 (does not transfer).

**Field note.** Statistics/psychometrics (MTMM, method variance) returned designs but no LLM application with formats as the method facet. Survey methodology's paraphrase literature is human and not opened. No paper found compares paraphrase-within-format variation with between-format variation on the same items for an LLM's stated credence.

## Read records

### Measuring LLMs' Sensitivity to Paraphrased Opinion Prompt — Alhetelah & Ahmad, 2026, WASSA 2026 (ACL Anthology 2026.wassa-1.5), https://aclanthology.org/2026.wassa-1.5/
- read_depth: full (PDF via pdftotext, pages 52-59).
- what_tested: whether five LLMs give the same Yes/No/Neither answer to an opinion question and five meaning-preserving paraphrases of it.
- on_whom: GPT-3.5 Turbo, Claude 3.7 Sonnet, DeepSeek Reasoner, Gemini 2.0 Flash, LLaMA 3 70B; 200 opinion questions × (1 original + 5 paraphrases) = 1,200 prompts; paraphrases from GPT-4o-mini, checked by one author (about 7% adjusted).
- how_scored: consistency rate (share of a question group matching its majority answer), Cohen's κ between original and paraphrase answers, pairwise agreement between models; temperature 0, one call per prompt.
- result: mean consistency about 90-91% for DeepSeek and Gemini, "around 90%" for Claude 3.7 Sonnet; κ 0.665 Claude 3.7 Sonnet (highest), 0.642 Gemini, 0.638 DeepSeek, 0.312 LLaMA, 0.307 GPT-3.5; Claude's agreement with the other models 33-48%.
- limitations: temperature 0 only, so no same-prompt repeat baseline; one validator; one categorical format.
- borrow: the paraphrase-group design (one original and several validated paraphrases per item) for a reworded arm of our formats.
- next_steps_it_suggests: stochastic decoding settings, human-authored paraphrases, multi-turn settings.
- predicts_for_us: gm3c-f3: an older Claude model keeps its categorical answer across paraphrases well beyond chance (κ 0.665), which leans toward a reworded format recovering more than another format does; no bearing on the 0.75 bar, since there is no repeat ceiling and no graded answer.
- **design to borrow**: paraphrase groups with a validation step; our version adds what it lacks, a same-prompt repeat ceiling and graded answers.

### What Did I Do Wrong? Quantifying LLMs' Sensitivity and Consistency to Prompt Engineering — Errica, Siracusano, Sanvito & Bifulco, 2025 (NAACL 2025 per the WASSA paper's reference list; arXiv 2406.12334 v4), https://arxiv.org/html/2406.12334
- read_depth: partial (arXiv HTML, first 100,000 of 111,745 characters; definitions, Table 1, per-class analysis).
- what_tested: label-free sensitivity of classifiers to 30 meaning-preserving rephrasings of the task description, and consistency of predictions within a class.
- on_whom: Llama-3-70B-Instruct, Mixtral-8x7B, GPT-3.5-turbo, GPT-4o; TREC (500), CB (250), RTE (2,490), DBPedia (2,000), WoS (2,000); no Claude.
- how_scored: sensitivity = normalized entropy of the prediction distribution averaged over rephrasings; consistency = 1 − total variation distance between same-class predictions.
- result: e.g. Llama3 TREC simple sensitivity 0.127, consistency 0.693, micro-F1 0.848; GPT-4o TREC 1-shot 0.037 / 0.816 / 0.862; sensitivity and consistency correlate at −0.07; sensitivity concentrates in some classes (TREC Description, Entity, Number).
- limitations: temperature 0 and a fixed seed, so rephrasing variation is never set against sampling variation; classification only.
- borrow: entropy over rephrasings as a per-item sensitivity score; the observation that sensitivity is item- and class-specific.
- next_steps_it_suggests: extend beyond classification; higher moments; automatic prompt optimisation.
- predicts_for_us: gm3c-f3: wording sensitivity is real but uneven across items; no prediction for the share of a credence a rewording recovers.
- **changes nothing** for the draft rule (no repeat baseline, no graded credence); it supports reporting per-claim paraphrase recovery, not only the mean.

### Beliefs and Behavior in Language Models — Smolin & Wilder, 2026, arXiv 2609.07943 (re-read for new parts)
- read_depth: partial re-read (PDF via pdftotext; "Action spaces", "Results: Prediction", Appendix A.1 and A.4).
- what_tested (the parts re-read): 16 outputs per case: one numerical probability, two five-category ordinal judgments, and thirteen binary decisions, which are one domain decision plus "four probability-threshold, four point-payoff bet, and four asymmetric-error-cost variants" forming matched triplets at r ∈ {2, 4, 9, 19} (thresholds 33.3%, 20%, 10%, 5%).
- on_whom: nine non-Claude models, 500 cases in each of three domains (kidney disease, Werewolf, scientific forecasting).
- how_scored: group hold-outs (all decisions predicted from probability outputs, and the reverse), concordance and R²; across-framing zero-shot with a shared link in the implied threshold; Appendix A.4 a monotone-spline link and a two-dimensional latent; Figure 7 holds out one output with the other fifteen observed.
- result: capable models concordance 0.8-0.95 and R² 60-90%; across framings, domains or both, pooled R² about 0.6 to 0.8 for the most capable; the spline and two-dimensional models' predictive performance is "nearly identical to that of the original latent variable model".
- limitations: no Claude; the held-out framings in the zero-shot test are payoff-equivalent rewordings of the same decision, so they sit between a paraphrase and a format change.
- borrow: the matched-triplet idea (the same decision under three framings whose implied threshold is equal) for building reworded versions of our formats with their meaning pinned.
- next_steps_it_suggests: (from the paper's discussion) whether elicited probabilities suffice to summarise the belief.
- predicts_for_us: gm3c-f3: a reworded prompt with the same meaning is predicted well for capable models (0.6-0.8 pooled R² across framings), which favours a reworded format beating another format; a two-dimensional latent adds nothing on their data, so a second-latent follow-up is unlikely to rescue Q.
- **design to borrow** (matched rewordings) and **already shown** for the two-dimensional question on other models: no second-latent follow-up is drafted.

### Standards for Belief Representations in LLMs — Herrmann & Levinstein, arXiv 2405.21030 (v2, 14 March 2025)
- read_depth: full (arXiv HTML).
- what_tested: a conceptual paper proposing four criteria for a belief-like representation: accuracy, coherence, uniformity and use.
- on_whom: none new; cites probe results (Azaria and Mitchell probes falling from over 80% to 40-60% once negations are added).
- how_scored: n/a.
- result: coherence asks for "consistent answers on sentences with the same semantic content"; uniformity is consistency across domains; task formats are not discussed.
- limitations: no measurement of formats or of behavioural credences.
- borrow: the distinction between coherence under rewording and uniformity across domains, as names for the two readings gm3c-f3 separates.
- next_steps_it_suggests: tests of probes against these standards.
- predicts_for_us: no bearing on the draft rule.
- **changes nothing**: it names the standard (consistency under rewording) without a number.

### Not transferred
- PReSS (Kabir, Esterling & Dong, arXiv 2504.17052 v3): political stance under supporting or counter-arguments on 12 open models; no response-format or paraphrase-against-format comparison. One line, stopped.
- Haller, Vamvas & Jäger 2024 (COLM): found by search, 500 paraphrases per political-compass statement; not opened (no arXiv id found), so nothing is reported from it.

## What the re-scout changes

Adds **gm3c-f3**: reword two formats while keeping them the same format, and measure how much of the original each rewording recovers against the same split-half ceiling. If rewordings recover far more than other formats do, the unshared part is format-specific; if not, it is any-wording fragility, which changes what gm3b and gm3c mean. Drops a two-dimensional-latent archive test: Smolin and Wilder found it adds nothing, and the audit's cross-validated linear prediction (Q 0.435) largely bounds it for linear combinations. gm3c-f2 stays parked (Sonnet answered). The re-scout lowers no bar and moves no odds; odds are elicited later.

## Novelty line check

The ledger row and results file carry a line from a fresh session (claude-fable-5-1). Checked against the re-read of Smolin and Wilder: their held-out R² of 60 to 90% for capable models and pooled R² of about 0.6 to 0.8 zero-shot to an unseen framing are as stated in the text; no paper found reports a cross-format share normalised by a split-half ceiling. One precision the line does not need to carry: their main hold-out predicts a whole group of outputs (decisions from probability reports), their one-output-from-fifteen hold-out is Appendix Figure 7, and twelve of their outputs are matched rewordings of three decision framings. **Novelty line stands:**

**Novelty:** partly new. Predicting a held-out prompt from the others is Smolin and Wilder's (2026, arXiv:2609.07943) own test: on nine non-Claude models they report held-out R2 of 60 to 90% for capable models, pooled R2 of about 0.6 to 0.8 zero-shot to an unseen framing, and much lower scores for less capable models. Our figure for Claude Haiku on its own claims is an R2 of 0.37 from the other five formats, or 39% of each format's split-half ceiling, below their range; the ceiling-normalised ratio appears nowhere we found. Search: WebSearch for "latent belief" "held-out" "framing" "LLM" and "cross-format prediction credence"; Smolin and Wilder PDF read in full. (Checked and kept by claude-opus-5-5, 2026-11-05c remap re-scout; added search: "LLM belief consistency paraphrase versus elicitation format", WebSearch, 2026-11-05.)
