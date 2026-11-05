# em-gm3b

*Novelty check for em-gm3b (rule 13), written 2026-11-05 by a fresh claude-fable-5-1 subagent launched by the informed-engine session: web reads only, no model API, no repo edits; every number below comes from a page the session opened. Its Novelty line is in the results file and the ledger row.*

## Verdict
partly new
## Novelty line
Smolin and Wilder (2026, arXiv:2609.07943) fit one latent belief to 16 prompts on nine models (Gemma 3, Llama 3.1 70B, Qwen3 32B, DeepSeek V3.2, GLM-5, GPT-5.6; no Claude) and find it reconstructs behaviour well only for the most capable, with weaker models showing framing effects and "monotonic but weak and noisy" links. Lu et al. (2025, arXiv:2504.19445) and Pawitan and Holmes (2024, arXiv:2412.15296) also report format-dependent or incoherent judgments. None states our result: on Claude Haiku's own claims, six formats disagree beyond any monotone lens, with rank reversals on 12 to 25% of pairs and a separate-belief model winning on 86% of claims. Verdict: partly new.
Search: WebSearch for "elicitation format", "latent belief", "credence", "betting odds", "yes/no versus rating" with "LLM", 2025 to 2026; arXiv abstract pages and the Smolin and Wilder PDF opened.
## Papers opened
- Smolin, A., Wilder, B., 2026, Beliefs and Behavior in Language Models, https://arxiv.org/abs/2609.07943 (PDF read in full). 16 outputs (three probability reports, 13 decisions) on 500 cases in three domains; held-out R2 60 to 90% and concordance 0.8 to 0.95 for capable models; "Less capable LLMs score much less highly"; weaker models show framing effects (higher thresholds under bet framing). No Claude model.
- Lu, Y.-L., Zhang, C., Wang, W., 2025, Systematic Bias in Large Language Models: Discrepant Response Patterns in Binary vs. Continuous Judgment Tasks, https://arxiv.org/abs/2504.19445. Binary formats give more "negative" judgments than continuous ones on the same items; a direction-of-bias result, not a test of monotone lenses.
- Pawitan, Y., Holmes, C., 2024, Confidence in the Reasoning of Large Language Models, https://arxiv.org/abs/2412.15296. GPT-4o, GPT-4-turbo, Mistral: concludes models lack "any internally coherent sense of confidence"; compares reconsideration and self-reported scores, not six formats.
- Pal, A. et al., 2025, Knowing What You Know Is Not Enough, https://arxiv.org/abs/2511.13240. Action-belief gap (betting against own stated confidence); related in kind, different test.
- Lei, G., Cooper, S. J., 2026, Elicitation Matters, https://arxiv.org/abs/2605.04764. Pointwise and joint query protocols induce different beliefs; a surrogate-modelling setting, not credence formats.
- Kim, H., Kang, P., 2026, Same Answer, Different Confidence: Protocol Sensitivity in LLM Confidence Calibration, https://arxiv.org/abs/2605.27752. Confidence scores are protocol-dependent on open 7B to 72B models; verbalised versus token confidence, not six verbal formats.
- Wolf, P. et al., 2026, Partition, Prompt, Aggregate, https://arxiv.org/abs/2607.15277. Violations of the law of total probability across prompts; a coherence test, not a format test.
## Not found / caveats
- No paper testing a Claude model with several elicitation formats on the same claims and a monotone-link model was found.
- Smolin and Wilder's criterion (held-out framings and decisions, R2 and concordance) differs from this bet's (held-out repeats, log-likelihood), as the results file already notes.
- The Wilder seminar page at tse-fr.eu returned 404 and was not read.
