# Biomimetic (rev. 1 §3.9): contrast or assimilation on the single-scale QQ conversations

Pre-registered in `experiments/bm9-contrast.md` (D42), committed before the archive was opened for this analysis. Anchor (a) only; $0.

## In plain English

**The question.** When the model rates a sub-question and then the main question, does the main rating move toward the number it just gave (assimilation) or away from it (contrast)? The logical push of the claim's content is held fixed.

**What we found.** Assimilation.
- **Level effect.** The shift in M rises with how far the S rating sits above the unprompted M: +0.27 [+0.11, +0.43] per point, on top of the content push (+7.7). Separating the two terms, most of this is M being less extreme after S (coefficient on M-first −0.37); the coefficient on the S level alone is +0.13 [−0.04, +0.28].
- **Replication.** The single-scale run 2 gives the same figure, +0.27 [+0.05, +0.58].
- **Within the same question,** conversations where the model happened to rate the sub-question higher also tend to give a main rating that follows it in the content's direction (correlation +0.17 and +0.34).

**What it means.** By the pre-registered rule this is assimilation (β > 0), and no contrast appears. The statistic does not by itself separate a pull toward S from M becoming less extreme after S. As revision 2 of the map notes, this does not test divisive normalization.

**Novelty:** partly new. That earlier context moves an LLM's next judgment is in print: Stureborg et al. 2024 (arXiv 2405.01724) find GPT-4's own earlier coherence score raises its later consistency score; Kapetanovic et al. 2026 (arXiv 2608.25869, CIKM '26) find a shown below-threshold prior score lowers judge ratings on seven of eight models (Claude-4.5-Sonnet d = −0.44), with almost no further change across anchor values; and Temkit 2026 (arXiv 2605.22714) finds that any earlier history, even a balanced one, shifts binary judgments toward "no" (Claude Haiku 4.5 d = −0.22 overall). None holds the content's push fixed, asks a sub-question before the main question, or separates a pull toward the just-given number from the main rating becoming less extreme, which the em-bm9 audit found carries most of our β (sub-rating level alone +0.13 [−0.04, +0.28]): partly new. Search: the earlier line's searches, plus WebSearch "anchoring bias large language models numeric estimates high low anchor" and "LLM ratings central tendency multi-turn judgments less extreme", 2026-11-05, with the Kapetanovic and AMEL HTML re-read in full; claude-opus-5-5, 2026-11-05c remap re-scout. *(Rule 13; written by a fresh claude-opus-5-5 reader subagent of the 2026-11-05c remap session, which ran none of these bets; its searches and reads are in programs/entangled-mind/map/reads/remap-2026-11-05c-em-bm9.md.)*

## d_M = α + β·L + γ·C across (item, claim) pairs

d_M: M after S minus M first; L: S level minus M-first level; C: yes-ward content push of the S rating. Secondary: within-pair correlation of S and the following M, signed by the claim's lean (positive = M follows S the way content implies). 95% item-cluster bootstrap CIs.

| set | pairs | β (level) | γ (content) | signed within-pair corr (pairs with variance) | reading |
|---|---|---|---|---|---|
| run 1, anchor (a), 40 items | 80 | +0.268 [+0.109, +0.427] | +7.7 [+0.8, +16.0] | +0.17 [+0.05, +0.29] (76) | assimilation |
| run 2, anchor (a), 10 items (replication) | 20 | +0.274 [+0.046, +0.584] | +7.7 [-8.4, +31.8] | +0.34 [+0.09, +0.56] (20) | assimilation |

## Pre-registered reading (primary set): **assimilation**

## Correction to the Novelty line (2026-11-05 16:37 MST, remap 2026-11-05c)

The 2026-11-05c remap's re-scout re-read Kapetanovic et al. 2026 and AMEL in full and corrected this file's Novelty line (verdict unchanged: partly new): Kapetanovic's shown prior score lowers ratings almost regardless of its value, rather than pulling them toward it, and AMEL's −0.22 for Claude Haiku 4.5 is the overall shift toward "no", not a polarity drag. The old line, verbatim:

> **Novelty:** partly new. That numbers already in an LLM's context pull its next rating toward them is in print: Stureborg et al. 2024 (arXiv 2405.01724) find GPT-4's own earlier coherence score raises its later consistency score, Kapetanovic et al. 2026 (arXiv 2608.25869) find a shown prior score shifts judge ratings toward its value (d up to 0.71), and Temkit 2026 (arXiv 2605.22714) finds history polarity drags judgments its way across 12 models including Claude Haiku (d = -0.22). None holds the content's logical push fixed, tests a sub-question-then-main-question pair, or pits assimilation against contrast as we do: partly new. Search: WebSearch for "LLM sequential ratings assimilation serial dependence", "LLM-as-judge prior score anchoring", "LLM survey question order assimilation contrast"; arXiv abstracts and the Stureborg HTML opened; Fischer and Whitney and Cicchini via Europe PMC. *(Rule 13, CONTEXT.md §3; written by a fresh claude-fable-5-1 subagent launched by the informed-engine session, 2026-11-05, web reads only, no model API; its papers-opened list and caveats are in programs/entangled-mind/map/reads/novelty-2026-11-05-em-bm9.md.)*
