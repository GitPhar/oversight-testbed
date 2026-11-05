# em-gm9

*Novelty check for em-gm9 (rule 13), written 2026-11-05 by a fresh claude-fable-5-1 subagent launched by the informed-engine session: web reads only, no model API, no repo edits; every number below comes from a page the session opened. Its Novelty line is in the results file and the ledger row.*

## Verdict
partly new
## Novelty line
That earlier turns shift a model's later judgments is in print: Temkit (2026, arXiv:2605.22714) finds binary verdicts drift toward planted prior answers across 12 models including Anthropic Haiku through Opus (d = -0.17), and Simhi et al. (2026, arXiv:2603.03308, ICML) report prior turns biasing later responses in three model families. Kang (2026, arXiv:2607.17219) audits question order with committed answers but found saturated outputs. None states our result: 0-100 ratings moving 12 to 23 points after the model's own earlier questions, read as no-signalling-in-time invasiveness, nor the null for a midway yes/no choice (no LLM replication of Kvam et al. 2015 found). Verdict: partly new.
Search: WebSearch for "no-signalling in time", "Leggett-Garg", "macrorealism", "question order effects" and "Kvam interference choice confidence" with "language model" or "LLM", then the arXiv abstract page of each hit.
## Papers opened
- Temkit, S.-A., 2026, AMEL: Accumulated Message Effects on LLM Judgments, https://arxiv.org/abs/2605.22714 and https://arxiv.org/html/2605.22714v1. Planted positive or negative histories shift later binary yes/no judgments (d = -0.17, Haiku -0.22 to Opus -0.17); does not separate the question from the recorded answer and uses planted, not the model's own, answers.
- Kang, P., 2026, Auditing Question-Order Effects in Large Language Models with the QQ Equality: Mechanism Characterization and a Saturation Caveat, https://arxiv.org/abs/2607.17219. Committed multi-turn forced-branch protocol on one open-weight model; most item pairs saturated, so no mechanism was identified; classical repetition can satisfy QQ exactly.
- Simhi, A., Barez, F., Tutek, M., Belinkov, Y., Cohen, S. B., 2026, Old Habits Die Hard: How Conversational History Geometrically Traps LLMs, https://arxiv.org/abs/2603.03308. Earlier turns bias later responses across three model families and six datasets; no 0-100 ratings and no question-versus-answer separation.
- Tjuatja, L. et al., 2024, Do LLMs exhibit human-like response biases? A case study in survey design, https://arxiv.org/html/2311.04076. Tests option order within one question, not an earlier question changing a later answer; does not bear on it directly.
- Guan, B. et al., 2025, The Order Effect: Investigating Prompt Sensitivity to Input Order in LLMs, https://arxiv.org/abs/2502.04134. Input order inside one prompt; does not bear on sequential questions.
- Dominguez-Olmedo, R., Hardt, M., Mendler-Dünner, C., 2024, Questioning the Survey Responses of Large Language Models, https://arxiv.org/abs/2306.07951. Answer-order and label biases in 43 models; does not bear on question order.
- Lei, G., Cooper, S. J., 2026, Elicitation Matters: How Prompts and Query Protocols Shape LLM Surrogates under Sparse Observations, https://arxiv.org/abs/2605.04764. Reports order-sensitive, non-monotonic confidence updates under sequential evidence; evidence order, not question order.
## Not found / caveats
- No paper applying no-signalling in time, Leggett-Garg or macrorealism to a language model was found; every hit was quantum physics.
- No LLM replication of Kvam, Pleskac, Yu and Busemeyer (2015) choice-then-confidence interference was found; Kumaran et al. (2025) on choice-supportive bias came up in search results but was not opened, so it is not cited.
- The Kang full text was not read; the abstract page did not say whether earlier answers are visible in context. The repo's own notes (paper/clonable-minds.md) say answers are committed as assistant turns.
