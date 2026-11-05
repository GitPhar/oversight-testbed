# em-gm3c

*Novelty check for em-gm3c (rule 13), written 2026-11-05 by a fresh claude-fable-5-1 subagent launched by the informed-engine session: web reads only, no model API, no repo edits; every number below comes from a page the session opened. Its Novelty line is in the results file and the ledger row.*

## Verdict
partly new
## Novelty line
Predicting a held-out prompt from the others is Smolin and Wilder's (2026, arXiv:2609.07943) own test: on nine non-Claude models they report held-out R2 of 60 to 90% for capable models, pooled R2 of about 0.6 to 0.8 zero-shot to an unseen framing, and much lower scores for less capable models. Our figure for Claude Haiku on its own claims is an R2 of 0.37 from the other five formats, or 39% of each format's split-half ceiling, below their range; the ceiling-normalised ratio appears nowhere we found. Verdict: partly new.
Search: WebSearch for "latent belief" "held-out" "framing" "LLM" and "cross-format prediction credence"; Smolin and Wilder PDF read in full.
## Papers opened
- Smolin, A., Wilder, B., 2026, Beliefs and Behavior in Language Models, https://arxiv.org/abs/2609.07943 (PDF). Held-out output prediction: concordance 0.8 to 0.95 and R2 60 to 90% for capable models; across-framing zero-shot pooled R2 about 0.6 to 0.8 for the most capable; "for less-capable models, such predictions are significantly less accurate". Models: DeepSeek V3.2, Gemma 3 4B/12B/27B, GLM-5, Llama 3.1 70B, Qwen3 32B, GPT-5.6 Luna and Terra.
- Kim, H., Kang, P., 2026, Same Answer, Different Confidence, https://arxiv.org/abs/2605.27752. Protocol sensitivity of confidence scores; does not compute cross-format recovery.
- Lei, G., Cooper, S. J., 2026, Elicitation Matters, https://arxiv.org/abs/2605.04764. Query protocol changes elicited belief; no held-out-format statistic.
## Not found / caveats
- No paper reporting a cross-format R2 normalised by a within-format split-half ceiling was found.
- Smolin and Wilder's R2 is per output on decision or probability targets in clinical, game and forecasting domains, so the numeric comparison with our 0.37 is only indicative.
