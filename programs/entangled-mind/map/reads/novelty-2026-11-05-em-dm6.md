# em-dm6

*Novelty check for em-dm6 (rule 13), written 2026-11-05 by a fresh claude-fable-5-1 subagent launched by the informed-engine session: web reads only, no model API, no repo edits; every number below comes from a page the session opened. Its Novelty line is in the results file and the ledger row.*

## Verdict
partly new
## Novelty line
That verbalised-confidence ECE depends on how the question is asked is in print: Tian et al. (2023, arXiv:2305.14975, EMNLP) report claude-2 ECE from 0.048 to 0.238 across their prompt variants on SciQ, and Kim and Kang (2026, arXiv:2605.27752) call confidence "protocol-dependent" on open models, most of the shift coming from the instruction. A 2026 preprint (arXiv:2603.01239) finds Claude Sonnet 4.6's calibration error drifting across turns. None tests probability against frequency wording (a human precedent is Gigerenzer and Hoffrage, 1995, Psychological Review), finds a format effect on Sonnet but not Haiku, or reports a question-order null. Verdict: partly new.
Search: WebSearch for "verbalized confidence" with "frequency format", "out of 100", "question order", "multi-turn calibration ECE"; arXiv abstract pages opened and Tian et al. HTML read.
## Papers opened
- Tian, K. et al., 2023, Just Ask for Calibration, https://arxiv.org/html/2305.14975. Verb. 1S top-k, Verb. 2S, Ling. 1S variants; ECE differs across variants for the same model (claude-2 SciQ 0.048 to 0.238); says prompts "sometimes differ drastically in the calibration"; no probability versus frequency wording, no question order, no isolated multi-turn test.
- Kim, H., Kang, P., 2026, Same Answer, Different Confidence: Protocol Sensitivity in LLM Confidence Calibration, https://arxiv.org/abs/2605.27752 and html. Five open 7B to 9B models plus Qwen2.5 up to 72B; no Claude; 0 to 1 and 0 to 100 scales both show the context shift; "multi-turn dialogue" listed as untested.
- Harshavardhan, 2026, Self-Anchoring Calibration Drift in Large Language Models, https://arxiv.org/abs/2603.01239. Claude Sonnet 4.6, GPT-5.2, Gemini 3.1 Pro, 150 questions; Sonnet's calibration error drifts significantly across self-anchored turns; single-author preprint.
- Zhang, Z. et al., 2026, Confidence Should Be Calibrated More Than One Turn Deep, https://arxiv.org/abs/2604.05397 (ACL 2026). ECE@T per turn; user persuasion degrades multi-turn calibration; no fresh-versus-conversation comparison of identical questions on the abstract page.
- Xiong, M. et al., 2023, Can LLMs Express Their Uncertainty?, https://arxiv.org/abs/2306.13063. Prompting strategies change overconfidence; abstract does not state a format-dependence result.
- Xia, Y. et al., 2026, Calibration Is Not Enough, https://arxiv.org/abs/2601.08064. Robustness to prompt perturbation; finds common methods mostly robust; does not test frequency wording.
- Gigerenzer, G., Hoffrage, U., 1995, How to Improve Bayesian Reasoning Without Instruction: Frequency Formats, Psychological Review 102(4), 684-704 (PDF at pages.ucsd.edu). Human precedent: frequency formats raised Bayesian answers to "up to 50% of all inferences".
## Not found / caveats
- No paper comparing probability wording with "out of 100" frequency wording for LLM verbalised confidence was found.
- No paper reporting a question-order (forward versus reversed) null on aggregate ECE was found.
- Only the first 100,000 characters of the Kim and Kang HTML were read; Appendix B.1 details on the 0 to 100 scale were truncated.
- The parse losses in this bet's run have no outside precedent to cite.
