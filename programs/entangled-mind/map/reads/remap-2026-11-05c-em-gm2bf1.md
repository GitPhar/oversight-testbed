# Re-scout around em-gm2bf1 (do claims that move most with question order also move most with answer format?)

- **Bet:** em-gm2bf1 · **Program:** entangled-mind (program 1) · **Map node:** gm2b-f1 · `secondary_of: em-gm3b` (CONTEXT.md §3 rule 15)
- **The result in one sentence:** On Haiku's 160 claims, a claim's order span and its format spread correlate (Spearman +0.34 [+0.16, +0.49]) and stay linked after the D71 guard (+0.25 [+0.09, +0.37]), but the guard frozen at pre-registration gives +0.09 [−0.09, +0.27], allowing for order-rating noise alone removes the link, it sits in gm2b's 30 items (gm2's 10: −0.09), and random tie-breaking or two dropped items take it under the bar: pass, unreplicated, fragile.
- **Date:** 2026-11-05 16:29 MST (from `date`)
- **Read by:** claude-opus-5-5, a fresh reader subagent of the 2026-11-05c remap session. Web reads only (WebSearch, WebFetch; PDFs read with `pdftotext` in the session scratchpad). No model API, no experiment, no local model.

**What the result now raises.** Whether the pass survives depends on what "noise" is allowed for, and the noise covariate W was computed from the same conversations as the order span S (ρ(S, W) 0.77). Two questions follow. Is W a nuisance that a guard should remove, or the very instability being measured? And does a guard built from the same draws remove too much (shared sampling error) or, if built from fewer draws, too little (residual confounding)? The searches went to statistics on controlling for noisy covariates, to the survey literature on whether the same people are susceptible to several response effects, and to LLM work on which items are prompt-sensitive.

**Already in the program's reads:** none of the papers below. gm2b-f1's Prior work line cites Zhu and Griffiths 2024 and AMEL (Temkit 2026) from the repo; AMEL is re-read in full here for its baseline-uncertainty result. The em-gm2bf1f1 design review cites Krosnick and Schuman 1988 from a search; it is read in full here.

## Searches

One line per search: terms; where; date.

1. `statistically controlling for confounding constructs is harder than you think Westfall Yarkoni measurement error partial correlation`; WebSearch (standard); 2026-11-05. PMC4816570 (read).
2. `Bassili Krosnick 2000 "Do strength-related attitude properties determine susceptibility to response effects" pdf`; WebSearch; 2026-11-05. Bassili and Krosnick 2000 only as catalogue records (not opened); Krosnick and Schuman 1988 PDF on Krosnick's Stanford page (read).
3. `AMEL accumulated message effects LLM judgments arXiv 2605.22714`; WebSearch; 2026-11-05. HTML v1 (re-read).
4. `anchoring bias large language models numeric estimates high low anchor anchoring index arXiv 2024 2025`; WebSearch; 2026-11-05. Owusu and Feldman, ACL 2026 (read).
5. `LLM belief consistency paraphrase same question format versus different elicitation format probability rating`; WebSearch; 2026-11-05. No paper correlates an item's sensitivity across two manipulations.
6. Direct opens, 2026-11-05: pmc.ncbi.nlm.nih.gov/articles/PMC4816570 (first 100,000 of 108,477 characters); web.stanford.edu Krosnick 1988 PDF (pdftotext, 12,734 words, all pages); arxiv.org/html/2410.12405 (first 100,000 of 111,745 characters); aclanthology.org/2026.acl-short.16.pdf (pdftotext, all pages); arxiv.org/html/2605.22714v1 (first 100,000 of 107,477 characters); arxiv.org/html/2406.12334 (first 100,000 characters).

**Field note.** Statistics (residual confounding) and survey methodology (attitude strength and response effects) both bear directly; LLM work measures per-item sensitivity to one manipulation at a time and relates it to the model's confidence, never one manipulation's sensitivity to another's. No paper found states our cross-manipulation correlation.

## Read records

### Statistically Controlling for Confounding Constructs Is Harder than You Think — Westfall & Yarkoni, 2016, PLoS ONE 11(3): e0152719, https://pmc.ncbi.nlm.nih.gov/articles/PMC4816570
- read_depth: partial (PMC full text, first 100,000 of 108,477 characters: simulations, Table 1, SEM remedy, reanalysis).
- what_tested: how often a regression that "controls for" a confound measured with error wrongly finds that a predictor adds something (incremental validity).
- on_whom: analytic error rates and simulations (30,000 runs per setting; n 50-5,000), an SEM simulation, and a reanalysis of the Eugene-Springfield community sample (n = 604).
- how_scored: Type I error rate of the incremental test.
- result: in the ice-cream example (n 120, covariate reliability 0.40) a spurious partial effect appeared 92% of the time; Table 1: n 120, r 0.5, reliability 0.4 gives 0.20 and reliability 0.8 gives 0.09; n 3,000, r 0.3: 0.48 and 0.16; errors are highest at moderate reliability (about 0.3-0.7) and grow with n; SEM with multiple indicators corrects it; with one indicator, fix the residual variance at an assumed reliability and run a sensitivity analysis.
- limitations: linear-Gaussian settings; the remedy needs a reliability estimate.
- borrow: two ways in for gm2bf1-f3: (1) a covariate taken from fewer, separate repeats is less reliable and so controls less, which can *inflate* a partial; (2) the fix is to estimate W's reliability (its split-half agreement) and correct the partial for it, reporting a sensitivity range.
- next_steps_it_suggests: SEM with several indicators per construct; reliability sensitivity analysis.
- predicts_for_us: gm2bf1-f3: a split-repeat guard can pass for the wrong reason (residual confounding from a less reliable W), so the rule must carry a reliability-corrected partial too; and the D71 guard's rise above the frozen one is the kind of covariate-set dependence this paper warns about.
- **design to borrow** (reliability-corrected partial), and **rival named** for any pass of a split-repeat guard: residual confounding.

### Attitude Intensity, Importance, and Certainty and Susceptibility to Response Effects — Krosnick & Schuman, 1988, Journal of Personality and Social Psychology 54(6): 940-952
- read_depth: full (PDF from Krosnick's Stanford page, via pdftotext).
- what_tested: whether people whose attitudes are intense, important or certain show smaller response effects (question order, response order, tone of wording, balance, acquiescence, middle alternative).
- on_whom: 27 split-ballot experiments in US national surveys; two within-subject re-interview experiments (n 678; 305 and 330).
- how_scored: the response effect's size in high against low strength groups; a meta-analysis over experiments.
- result: of 31 tests, 15 in the expected direction and 16 opposite; all experiments, average effect −0.4% (z 0.24, p .82); question order, 5 experiments, +2.8% (z 0.70); only the middle-alternative effect was moderated (+17.2%, z 4.80); in the within-subject studies the form effect was 16.5% (low intensity) against 13.5% (high), and 15.9% against 21.2% in the other group, both non-significant.
- limitations: strength measured by self-report after the manipulated question; between-person moderators, not item-level co-susceptibility; Bassili and Krosnick 2000 later added response latency and extremity (not opened).
- borrow: separate the claim's strength (extremity, noise) from its susceptibility, and test each response effect separately before pooling.
- next_steps_it_suggests: measure strength before the attitude question; within-subject designs.
- predicts_for_us: gm2bf1-f3: in people, strength-related properties do not consistently predict susceptibility, so a shared "weak belief" trait linking order and format effects is not the human default; in Haiku, by contrast, noise and extremity carry most of the order span (0.77, −0.79), so the human finding transfers poorly to the guard question.
- **changes nothing** for the draft rule; it supports reading each manipulation's driver separately.

### ProSA: Assessing and Understanding the Prompt Sensitivity of LLMs — Zhuo, Zhang, Fang, Duan, Lin & Chen, 2024, arXiv 2410.12405
- read_depth: partial (arXiv HTML, first 100,000 of 111,745 characters).
- what_tested: instance-level sensitivity to 12 semantic variants of the prompt (PromptSensiScore, PSS) and how it relates to the model's decoding confidence.
- on_whom: 8 open models (Llama3, Qwen1.5, InternLM2, Mistral-7B) on CommonsenseQA, ARC-Challenge, MATH, HumanEval; Claude-3.5-sonnet and GPT-4o on HumanEval (appendix); subjective tasks on five models.
- how_scored: PSS = mean absolute score difference between prompt pairs per instance; confidence = mean top-option token probability.
- result: robust instances show the highest decoding confidence and sensitive instances lower confidence (shown in a figure only, no numbers in the text); a model can be robust on some instances and sensitive on others; no correlation across perturbation types is reported; subjective PSS 0.013-0.036 (AlpacaEval) and 0.249-0.266 (Arena Hard).
- limitations: confidence analysis on three models only; no repeat baseline.
- borrow: decoding confidence as a covariate independent of the ratings that give S and W.
- next_steps_it_suggests: more few-shot settings; broader variants.
- predicts_for_us: gm2bf1-f3: sensitivity under any rewording concentrates where the model is unsure, which predicts that order span and format spread share a "how unsure" driver; that is the frozen guard's reading.
- **rival named**: both spreads track the model's own uncertainty.

### Anchoring Depends on Confidence and Post-Training in Language Models — Owusu & Feldman, 2026, ACL 2026 Short Papers, pp. 174-180
- read_depth: full (PDF via pdftotext).
- what_tested, on_whom, how_scored: as in `remap-2026-11-05c-em-bm9.md` (six Llama and Qwen variants, 50 anchoring questions, TVD).
- result: certainty predicts resistance (β −0.037 pooled, −0.052 mixed); accuracy does not once certainty is in (p = .48); the link is steeper after post-training (instruct interaction −0.072, p = .008).
- limitations: open 7-8B models; one manipulation.
- borrow: the model's baseline certainty, not its correctness, as the moderator to allow for.
- next_steps_it_suggests: mitigations; mechanisms.
- predicts_for_us: gm2bf1-f3: a third manipulation (anchors) is also driven by low certainty; predicts that once certainty is properly allowed for, little shared instability remains.
- **rival named** (the same uncertainty driver, on a different manipulation).

### AMEL: Accumulated Message Effects on LLM Judgments — Temkit, 2026, arXiv 2605.22714 (re-read for the uncertainty part)
- read_depth: partial re-read (arXiv HTML, first 100,000 of 107,477 characters).
- result (the part re-read): baseline uncertainty is binary entropy over 10 baseline repeats; high-entropy items (H > 0.76, n = 348) shift d −0.34, low (0 < H ≤ 0.76, n = 384) −0.18, deterministic (n = 5,591) −0.15; Spearman r 0.47 between baseline entropy and |shift|; pooled over models, not reported per Anthropic model.
- predicts_for_us: gm2bf1-f3: entropy from *baseline* repeats, separate from the shifted conversations, predicts the order-type shift; that is the separate-draws covariate gm2bf1-f3 proposes, and it predicts the covariate keeps much of its power when taken from other draws.
- **design to borrow**: measure the uncertainty covariate on draws separate from those that give the effect.

### Also opened, changes nothing here
- Errica et al. 2025 (arXiv 2406.12334): per-instance sensitivity to 30 rephrasings concentrates in some classes; no cross-perturbation correlation (record in `remap-2026-11-05c-em-gm3c.md`).

## What the re-scout changes

Adds **gm2bf1-f3**, the free test D88 and the audit named: take the order span from repeats 0-4 and the noise and extremity covariates from repeats 5-9 (and the reverse), so the guard no longer shares draws with the span. Westfall and Yarkoni make one addition necessary: the split covariate is less reliable, so the rule also needs a reliability-corrected partial, or a pass could be residual confounding. ProSA, Owusu-Feldman and AMEL predict a shared uncertainty driver. Re-prices gm2bf1-f2: D88 (F3) lists free Sonnet order archives on all 40 items, so it may need no new calls. Odds are elicited later.

## Novelty line (added; the results file and ledger row have none)

**Novelty:** partly new. Published LLM work finds that sensitivity to one manipulation at a time concentrates on items the model is unsure about: prompt variants (Zhuo et al. 2024, arXiv 2410.12405), numeric anchors (Owusu and Feldman 2026, ACL 2026 Short Papers 174-180) and earlier conversation turns (Temkit 2026, arXiv 2605.22714: high-entropy items d −0.34 against −0.15); that predicts the raw order-format correlation we found (+0.34) and agrees with our frozen guard, under which allowing for rating noise removes it. In people, attitude-strength measures did not predict susceptibility to response effects (Krosnick and Schuman 1988, JPSP 54:940, 27 experiments, average −0.4%). No paper found correlates an item's sensitivity to question order with its sensitivity to answer format, on any model; the guarded residual (+0.25 under D71) is that untested part, and it is fragile. Search: WebSearch for "LLM belief consistency paraphrase versus elicitation format", "Westfall Yarkoni controlling for confounding constructs", "attitude strength susceptibility to response effects", "anchoring bias LLM confidence", 2026-11-05; ProSA, AMEL and Westfall-Yarkoni HTML and the Krosnick-Schuman and Owusu-Feldman PDFs opened; claude-opus-5-5, 2026-11-05c remap re-scout.
