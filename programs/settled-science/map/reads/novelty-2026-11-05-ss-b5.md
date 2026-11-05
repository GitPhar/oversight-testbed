# ss-b5

*Novelty check for ss-b5 (rule 13), written 2026-11-05 by a fresh claude-fable-5-1 subagent launched by the informed-engine session: web reads only, no model API, no repo edits; every number below comes from a page the session opened. Its Novelty line is in the results file and the ledger row.*

## Verdict
partly new
## Novelty line
Luo et al. 2024 (Nature Human Behaviour; arXiv 2403.03230) state that LLMs pick a real neuroscience abstract over an expert-altered one (81.4% versus experts 63.4%), with "reverse the direction of a result" among the edit types, and that accuracy falls on the local results text alone; they report no valence or fixed-wording baseline. Wen et al. 2025 (arXiv 2506.00794) predict which of two AI ideas wins, ruling out only an idea-complexity shortcut; SciPredict (arXiv 2604.10718) and Lee 2026 (arXiv 2604.06236) have no real-versus-flipped format. Our tool-less model beating an up-word rule and a swap-pair rule on single flipped sentences is a comparison none of them makes. Verdict: partly new. Search: arXiv abstract and HTML pages for the four leads plus the PMC full text of Luo et al.; WebSearch for "BrainBench critique positive results bias altered abstract direction swap LLM shortcut".
## Papers opened
- Luo et al. (39 authors, incl. Love), 2024, "Large language models surpass human experts in predicting neuroscience results", https://arxiv.org/abs/2403.03230, https://arxiv.org/html/2403.03230, https://pmc.ncbi.nlm.nih.gov/articles/PMC11860209/. Real versus altered Journal of Neuroscience abstracts, results changed only; LLM perplexity choice; LLMs 81.4%, experts 63.4%; "LLMs performed much worse when restricted to this local context"; memorization check via zlib ratio; no valence or direction-word analysis and no fixed-choice baseline. States the kind of result (model picks real over altered) but not our valence-rule comparison.
- Wen, Si, Chen, He, Feng, 2025, "Predicting Empirical AI Research Outcomes with Language Models", https://arxiv.org/abs/2506.00794. Pairwise idea comparison; fine-tuned GPT-4.1 plus retrieval at 77%, beats human experts; "our system does not exploit superficial features like idea complexity"; off-the-shelf models near chance. No sentence-flip format and no valence rule; does not state our result.
- Sehwag et al., 2026, "SciPredict: Can LLMs Predict the Outcomes of Scientific Experiments in Natural Sciences?", https://arxiv.org/abs/2604.10718. 405 tasks in physics, biology, chemistry; models 14-26%, experts about 20%. No real-versus-flipped format, no shortcut analysis; does not bear on our comparison.
- Lee, 2026, "LLMs Have Made Failure Worth Publishing", https://arxiv.org/abs/2604.06236. Position paper on negative results and LLMs inheriting "the positive bias of the literature". Does not test prediction or valence shortcuts; does not bear on it.
## Not found / caveats
- No critique or follow-up of BrainBench testing a positive-valence or up-word shortcut was found.
- Luo et al.'s local-context and sentence-swap numbers are in supplementary figures not included in the pages opened; only the qualitative statements are quoted.
- Wen et al. was read from the abstract only; the full paper may contain further shortcut checks.
