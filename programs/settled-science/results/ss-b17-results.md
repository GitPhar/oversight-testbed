# ss-b17 results: the flattery question in a second wording, Haiku and Sonnet, all 200 BrainBench items

Pre-registration `ad2d924` (`experiments/ss-b17.md`, D81); the second wording frozen at `4173f67` (SHA-256 `72c5be33…`). Design review `ledger/design-reviews/ss-b17.md`: fix-first (`e8e4db8`), a $0.077 pilot of Haiku's call-to-call noise (D82, br-023), fixes D83 and D85, confirmed go (`42216f9`, 17:10). Budget ruling br-020, on Sean's budget steer. The run started after the confirmation: first call 2026-11-05 17:11:51, last 17:17:16 America/Denver (`t_utc` in `bettor/bbv2-ratings.jsonl`; run commit `d883d07`).

## In plain English

BrainBench (Luo et al., 2024) shows a real neuroscience abstract beside a copy an expert rewrote so the results come out differently; 171 neuroscientists picked the real one 63.4% of the time. ss-b10c asked two Claude models one sentence's worth of question, which version is "better news for the paper's own idea", and with every pair shown both ways round found Haiku right 76.2% and Sonnet 88.2% on all 200 pairs. This bet asked the same thing in different words, written and frozen before any call: which version's findings make the authors' own idea look better supported, and so would please the authors more.

- **The result held on both models. The bet passes (unreplicated).** Haiku picked the real abstract **72.5%** of the time (95% interval 67.0% to 77.8%), 3.8 points below its 76.2% with the first wording; Sonnet **87.0%** (82.2% to 91.5%), 1.2 points below its 88.2%. Both beat the neuroscientists' 63.4%, and both stayed within the 5 points the rule allowed.
- **Haiku's margin is thin, and its answers moved more than its score.** Haiku's lower bound is 67.0%, under 4 points above the experts; leaving out one journal section (Neurobiology of Disease) would put it outside the rule, and the bootstrap over sections puts its lower bound at 63.9%. Its total barely moved, but it gave the same item score under both wordings on only 70.5% of the items, below the about 81.8% that call-to-call noise alone gives (measured by the pilot). So the new sentence changed which items Haiku got right; the gains and losses roughly cancelled.
- **Sonnet hardly moved:** the same pick on 97.0% of the items.
- **The window cannot tell a small change from none.** The rule asks for a point estimate within 5 points; the committed dry run shows a true 5-point move would pass about half the time. And the program's forecasting prompt, a different question, run through the same comparison would also have met the rule on Haiku (81.0%, +4.8 points) though not on Sonnet (94.5%, +6.2). So matching accuracy shows ss-b10c's number was not an accident of one sentence; it does not show the models answered the same question both times.
- **The position habit is still there:** with the second wording Haiku was right 83.8% with the real abstract first and 47.8% with it second.

**What this does and does not show.** ss-b10c's result was not tied to its one sentence, on two Claude models, to within what 200 items can show. It still does not show how the models pick: by valence, by biological plausibility, or from memory of papers that were public before they were trained. One benchmark, one more wording, one model family.

**Novelty:** partly new. Luo et al. (2024, arXiv 2403.03230v4, *Nature Human Behaviour*) scored 15 open-weight models (Galactica 6.7B, 30B and 120B; Falcon-40B and 180B; Llama-2 7B, 13B and 70B; Mistral-7B; base and chat or instruct versions; GPT-2, TinyLlama, Phi-3 and their LoRA-tuned BrainGPT in the supplement) by the perplexity of each abstract, each scored on its own under one fixed prefix ("You are a neuroscientist with deep knowledge in neuroscience. Here is an abstract from a neuroscience publication:"). Its controls were local context only, results sentences swapped within a subfield, memorisation (zlib-perplexity ratio against a Gettysburg Address anchor, publication date against difficulty), calibration, and items written by GPT-4; it asked no model a question in words ("Our approach diverged from the popular approach of prompting models for responses through natural language"), so it ran no valence or flattery question, no option-order test and no second prompt wording, and it tested no Claude or other closed model. The kind of result is in print: Hua et al. (2025, arXiv 2509.01790; 7 LLMs, 6 benchmarks, 12 templates) trace much prompt sensitivity to log-likelihood scoring and rigid answer matching, with "a substantial reduction in performance variance" when an LLM judge reads the answers, which agrees with our near-equal totals; JudgeSense (Bellibatlu, Raff and Zhang, 2026, arXiv 2604.23478v3; 25 judges including claude-haiku-4-5 and claude-sonnet-4-5) finds "rewording moves a judge's verdict by more than its own decoding noise does", the pattern in Haiku's item scores (70.5% the same against an 81.8% noise floor), though on its two pairwise tasks the cost did not clear its threshold; Mizrahi et al. (2024, arXiv 2401.00595) and Sclar et al. (2023, arXiv 2310.11324; up to 76 accuracy points from formatting, LLaMA-2-13B, few-shot) report larger brittleness elsewhere. Nearest on the task, Chen, Hu and Lu (2025, arXiv 2504.01167) carried Luo's real-versus-reversed design to 1,261 conclusions from 276 field experiments on GPT models and found that conclusion sentiment, interacting with topic, predicted accuracy, but they asked which conclusion is true, not which flatters the authors; in metascience terms, Fanelli (2012, *Scientometrics* 90:891) found 85.9% of papers that tested a hypothesis in 2007 reported support for it, the base rate that would let "pick the version better for the authors' idea" beat chance, yet no paper found tests that rule on a real-versus-altered task, or its robustness to a second wording, which is what this bet adds. Search: "BrainBench" with shortcut, valence, positive result, prompting chat models, follow-up; "LLM distinguish real from altered scientific findings prompt wording"; "LLM bias toward positive results predicting experimental outcomes"; "LLM-as-a-judge pairwise robustness to prompt paraphrase"; "sycophancy paraphrased prompt confirmation bias scientific results"; "positive results bias heuristic forecasting replication"; "Fanelli negative results are disappearing"; general web search, then arxiv.org abstract and HTML pages, the Scientometrics PDF on gwern.net, 2026-11-05. Model: claude-opus-5-5 (a fresh subagent that did not run ss-b17).

### The pre-registered sentences (§5, as amended by D83 and D85; generated by `scoring/score_b17.py`)

| bet | engine odds | human odds | verdict |
|---|---|---|---|
| ss-b17 | 45 (prior 0.25 + 0.20, v2, after the design-review fixes; 37 first, D83) | none | **pass, unreplicated** |

> On BrainBench's 200 abstract pairs, each shown in both orders with the two ratings averaged, the flattery question in a second wording (fixed before any call: which version's findings make the authors' own idea look better supported) picked the published abstract more often than the 171 neuroscientists did (63.4%) on both models, and within 5 points of the first wording on each: Haiku 72.5% [67.0, 77.8], against 76.2% with the first wording (difference -3.8 points, [-9.2, 1.8]); Sonnet 87.0% [82.2, 91.5], against 88.2% with the first wording (difference -1.2 points, [-4.0, 1.5]). So ss-b10c's accuracy was not tied to its one sentence, to within what 200 items can show (a point estimate; a true 5-point move passes about 53.0% of the time). A different question, the program's forecasting prompt, run through the same comparison would also have come close, so matching accuracy does not show the models answered the same question both times; this design still cannot tell valence from plausibility or memory of the papers.
>
> Haiku gave the same pick under both wordings on 77.0% of the items, and the same item score on 70.5% (call noise alone gives about 81.8% the same item score); with the second wording it was right 83.8% with the original shown first and 47.8% with it second (Option-1 pull +10.1 points; +13.0 with the first wording).
>
> On the 100 items ss-b10c's rule was read on, Haiku's second-wording accuracy was 74.0% [66.0, 81.5], against ss-b10c's 77.5% (a reported row).
>
> Run through the same comparison, Haiku's forecasting prompt (ss-b10c, a different question) scores 81.0%, +4.8 points from the first wording, same pick on 73.5%, and would meet the rule (a reference row).
>
> On Haiku, leaving out the Neurobiology of Disease section(s) would change whether it meets the rule.
>
> Sonnet gave the same pick under both wordings on 97.0% of the items, and the same item score on 93.0% (call noise alone gives about 88.8% the same item score); with the second wording it was right 94.2% with the original shown first and 73.0% with it second (Option-1 pull +7.3 points; +7.4 with the first wording).
>
> On the 126 items ss-b10c's rule was read on, Sonnet's second-wording accuracy was 88.1% [82.5, 93.7], against ss-b10c's 89.7% (a reported row).
>
> Run through the same comparison, Sonnet's forecasting prompt (ss-b10c, a different question) scores 94.5%, +6.2 points from the first wording, same pick on 90.5%, and would not meet the rule (a reference row).
>
> Both wordings ask a model to judge which version is better for the paper's own idea; a pass shows the result is not tied to one sentence, not that the models answer by valence rather than plausibility or memory of the papers, which were public before these models were trained. Haiku and Sonnet ran with thinking off, as in ss-b10c.
>


## Tables

Generated by `scoring/score_b17.py` from `items/brainbench/items.jsonl`, `bettor/bbv2-ratings.jsonl` and `bettor/bbb-ratings.jsonl` (`scoring/b17-tables.md`, `scoring/b17-scores.json`).

| model | wording | n | accuracy, orders averaged | item 95% CI | section-cluster CI | original first | original second | Option-1 pull (points) | right both / first only / second only |
|---|---|---|---|---|---|---|---|---|---|
| Haiku | second (ss-b17) | 200 | 0.725 | [0.670, 0.777] | [0.639, 0.851] | 0.838 | 0.477 | +10.1 | 68 / 79 / 4 |
| Haiku | first (ss-b10c) | 200 | 0.762 | [0.705, 0.818] | [0.697, 0.819] | 0.917 | 0.425 | +13.0 | 79 / 101 / 2 |
| Sonnet | second (ss-b17) | 200 | 0.870 | [0.823, 0.915] | [0.819, 0.923] | 0.943 | 0.730 | +7.3 | 143 / 44 / 1 |
| Sonnet | first (ss-b10c) | 200 | 0.882 | [0.840, 0.922] | [0.829, 0.931] | 0.950 | 0.733 | +7.4 | 141 / 46 / 0 |

| model | C1: lower bound > 0.634 | second − first wording | 95% CI | C2: within 0.05 | same pick | meets the rule |
|---|---|---|---|---|---|---|
| Haiku | 0.670 (yes) | -0.037 | [-0.092, +0.018] | yes | 0.770 | yes |
| Sonnet | 0.823 (yes) | -0.013 | [-0.040, +0.015] | yes | 0.970 | yes |

**Verdict: pass.**

| model | reference: forecasting prompt as the 'second wording' | n | accuracy | − first wording | same pick | would meet the rule |
|---|---|---|---|---|---|---|
| Haiku | ss-b10c bettor | 200 | 0.810 | +0.048 | 0.735 | yes |
| Sonnet | ss-b10c bettor | 200 | 0.945 | +0.062 | 0.905 | no |

| model | ss-b10c's scored items | second wording | 95% CI | first wording |
|---|---|---|---|---|
| Haiku | 100 | 0.740 | [0.660, 0.815] | 0.775 |
| Sonnet | 126 | 0.881 | [0.825, 0.937] | 0.897 |

| section | n | Haiku second | Haiku first | Sonnet second | Sonnet first |
|---|---|---|---|---|---|
| Behavioral/Cognitive | 75 | 0.713 | 0.787 | 0.887 | 0.907 |
| Cellular/Molecular | 25 | 0.880 | 0.860 | 0.920 | 0.920 |
| Development/Plasticity/Repair | 24 | 0.771 | 0.792 | 0.833 | 0.854 |
| Neurobiology of Disease | 25 | 0.860 | 0.780 | 0.960 | 0.960 |
| Systems/Circuits | 51 | 0.578 | 0.657 | 0.794 | 0.804 |

| model | leave-one-item-out flips | leave-one-section-out flips |
|---|---|---|
| Haiku | none | Neurobiology of Disease |
| Sonnet | none | none |

## What it cannot do

- **Two sentences are not all sentences.** Both were written by Claude sessions; a pass shows the result survives one other wording.
- **Valence, plausibility and memory** are not separated by changing the sentence.
- **C2 is a point estimate**, not an equivalence test (a true 5-point move passes about half the time).
- **Sonnet's noise was not measured**; the dry run gave it Haiku's.
- No "LLMs", "every model" or "all" claim.

## Process and spend

| step | model | calls | cost | refusals |
|---|---|---|---|---|
| review pilot (D82; not test data) | Haiku, first wording, 80 excluded items × 2 orders × 2 draws | 320 | $0.077 | 0 |
| 1 | Haiku, second wording, 200 items × 2 orders | 400 | $0.106 | 0 |
| 2 | Sonnet, second wording, 200 items × 2 orders | 400 | $2.005 | 0 |
| | **total for the bet** | 800 | **$2.111** of the $2.25 cap | 0 |
