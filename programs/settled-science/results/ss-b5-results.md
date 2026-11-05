# ss-b5 results: round 2, items written by a template rather than a model

Pre-registration `29e8769` (`experiments/ss-b4.md`), seed `e8f921e`, design review `ledger/design-reviews/ss-b4.md`: ss-b4 redesign, so withdrawn; ss-b5 fix-first, then go after D23–D30. The run followed `dd7cab3`. **Audited** (`ledger/audits/ss-b5.md`, engine `1335a0f`): the pass stands as pass-unreplicated; cuts 2–8 are applied here (DEVIATIONS D31; cut 1 was a sealed plant, pl-004, caught, and not applied).

## In plain English

Round 1's items were written by the bettor's own model family, which might have picked findings it finds easy. Round 2 removed that writer. A fixed rule, committed before any round-2 paper was fetched, took one comparative result sentence from each recent arXiv abstract. It set that sentence beside the same sentence with its one direction word flipped ("higher" and "lower", "more" and "less", "outperforms" and "underperforms"). The bettor (the same tool-less model at the same setting) said which sentence was the real one. A Claude leakage checker dropped 146 of the 243 sentences the rule produced, because their wording gave the direction away: a number in 54 of them, and contrasting context in the sentence ('fewer … than', 'the strongest baseline') in most of the rest. The beacon then drew 92 of the 97 that were left.

**The bettor picked the published sentence 93% of the time** (86 of 92), with a Brier score of 0.070 (interval 0.050 to 0.093). This is a task of telling an author's sentence from a one-word flip of it, which a language model can often do by reading the sentence; the pass is about that task, not about forecasting findings (see below; round-3 audit).

That beats two dumb rules fixed before any bet:
- one that leans 75% toward the "higher / more / better" wording, Brier 0.177, which it beat by 0.107;
- one that knows only which word pair was flipped and how often each pair's "up" word is the published one, Brier 0.165, which it beat by 0.095.

Both margins clear zero, and no single item or query bucket changes the verdict. The margin comes entirely from the 21 items where the published sentence carries the 'down' word, where the up-word rule is wrong: the bettor was right on 17 of them. On the other 71 it was no better than the up-word rule (−0.005 [−0.022, 0.014]) and slightly worse than the swap-pair rule (+0.018 [−0.001, 0.039]). Removing 9 chosen down-word items would flip the verdict. Leave-one-out checks cannot see that.

**This shows less than it might seem.** Picking the real sentence can come from knowing which way the finding went. It can also come from reasoning inside the sentence (the flipped version often contradicts the rest of it), or from a sense of which wording reads as published. The test cannot separate these. Where the published sentence carried the less usual 'down' word, the bettor was still right on 17 of 21 (Brier 0.113). That rules out a habit of favouring 'up' words. It does not rule out a habit of picking whichever version makes the paper look good: most of these hits are cases where the down word is the paper's win ('lower noise', 'shorter circuits', 'costing less'), and three of the four misses are sentences reporting a limitation. It fits that habit, reasoning within the sentence and knowledge of the result equally well.

**It does not answer the audit's question about round 1.** The audit asked whether round 1's Claude-written items were made easy by their writer. Round 2 changes the item format as well as the writer: single sentences with no methods summary, instead of a curated question and methods. The two rounds' scores (0.070 here, 0.163 in round 1) are not comparable as evidence on that question.

**ss-b4 was withdrawn before any bet.** Its bar, beating always-50%, is passed on these items by the up-word rule alone (0.177) and by five other trivial rules. Its number appears below only as a descriptive secondary.

**The bettor ran with adaptive thinking at effort low (the least thinking claude-opus-5-5 allows), with its reasoning hidden; every result here is about the bettor at that setting.** (D18, D20. Median output was 116 tokens per call in all, visible answer included.)

### The pre-registered sentence (D25)

| bet | engine odds | verdict | sentence |
|---|---|---|---|
| ss-b5 | 25 (first 35; revised before data, D24) | **pass, unreplicated** | On 92 comparative sentences from arXiv abstracts first posted after its stated knowledge cutoff of June 2026 (34 of them in July–August), each shown beside the same sentence with one direction word flipped (chosen by a fixed template; a Claude leakage checker dropped 146 of 243 candidates), the bettor beat a rule that puts 75% on the 'higher / more / better' wording (paired Brier difference −0.107 [−0.151, −0.064]) and a rule that uses only which comparative word was flipped (−0.095 [−0.147, −0.046]). This does not separate knowing the result from reasoning within the sentence or recognising the published wording, and it does not show whether round 1's items were made easier by their Claude writer. |
| ss-b4 | 70 | **withdrawn before data** (D23; not scored) | Descriptive secondary only: the bettor's Brier is 0.070 against the up-word rule's 0.177. On these items always-50% is not a meaningful bar. |

On the 58 items posted from September on, the bettor still beats both rules (−0.123 [−0.182, −0.065]; −0.115 [−0.188, −0.048]).

**Scope (D20):** the bettor ran with adaptive thinking at effort low, with its reasoning hidden. Every result here is about the bettor at that setting.

Robustness, pre-registered (D16, D28):
- **Leave-one-item-out:** no flips.
- **Leave-one-query-bucket-out:** ss-b5 passes without interpretability (n = 65), without model psychology (62), without quantum devices (78) and without scalable oversight (71). It is not fragile.

**Novelty:** partly new. Luo et al. 2024 (Nature Human Behaviour; arXiv 2403.03230) state that LLMs pick a real neuroscience abstract over an expert-altered one (81.4% versus experts 63.4%), with "reverse the direction of a result" among the edit types, and that accuracy falls on the local results text alone; they report no valence or fixed-wording baseline. Wen et al. 2025 (arXiv 2506.00794) predict which of two AI ideas wins, ruling out only an idea-complexity shortcut; SciPredict (arXiv 2604.10718) and Lee 2026 (arXiv 2604.06236) have no real-versus-flipped format. Our tool-less model beating an up-word rule and a swap-pair rule on single flipped sentences is a comparison none of them makes. Search: arXiv abstract and HTML pages for the four leads plus the PMC full text of Luo et al.; WebSearch for "BrainBench critique positive results bias altered abstract direction swap LLM shortcut". *(Rule 13, CONTEXT.md §3; written by a fresh claude-fable-5-1 subagent launched by the informed-engine session, 2026-11-05, web reads only, no model API; its papers-opened list and caveats are in programs/settled-science/map/reads/novelty-2026-11-05-ss-b5.md.)*

## Tables

Generated by `scoring/score.py --r2` (`scoring/r2-tables.md`, `scoring/r2-scores.json`).

| measure | n | Brier | 95% CI | share right |
|---|---|---|---|---|
| **bettor** | 92 | **0.070** | [0.050, 0.093] | 0.93 |
| up-word rule (0.75 on "higher / more / better") | 92 | 0.177 | — | — |
| swap-pair rule (D24) | 92 | 0.165 | — | — |
| always 50% | 92 | 0.250 | — | 0.50 |

Bettor minus the up-word rule: −0.107 [−0.151, −0.064]. Bettor minus the swap-pair rule: −0.095 [−0.147, −0.046].

### By query bucket (secondary, against the up-word rule only; not the ss-b5 test)

Buckets are the keyword query each paper came from, not true fields. At least four "scalable-oversight" items are not about AI (r2-015, -018, -033, -035), and several "interpretability" items use probes outside AI (r2-072, -075, -092) (D26).

| query bucket | n | Brier | 95% CI | share right | up-word rule Brier | bettor − rule [95% CI] |
|---|---|---|---|---|---|---|
| interpretability | 27 | 0.072 | [0.048, 0.100] | 0.96 | 0.211 | −0.138 [−0.236, −0.048] |
| model psychology | 30 | 0.085 | [0.043, 0.139] | 0.90 | 0.146 | −0.061 [−0.121, −0.013] |
| quantum devices | 14 | 0.035 | [0.016, 0.057] | 1.00 | 0.241 | −0.206 [−0.333, −0.091] |
| scalable oversight | 21 | 0.068 | [0.025, 0.127] | 0.90 | 0.134 | −0.066 [−0.149, 0.010] |

### Calibration

| confidence in the favoured side | n | mean confidence | share right |
|---|---|---|---|
| 0.5–0.6 | 4 | 0.57 | 0.25 |
| 0.6–0.7 | 15 | 0.65 | 0.93 |
| 0.7–0.8 | 18 | 0.74 | 0.94 |
| 0.8–0.9 | 32 | 0.84 | 0.97 |
| 0.9–1.0 | 23 | 0.95 | 1.00 |

Mean confidence was 0.81, against 0.93 right. That is descriptive, and no test was pre-registered on it.

### Order check (secondary)

46 items were asked twice with the options reversed. The bettor chose the same side 98% of the time. Its two probabilities summed to within 4.2 points of 100 on average. It showed a pull toward whichever option is shown first of +1.1 points [0.3, 1.9]. That is small, uncorrected for the other secondaries, and rests on a few pairs: without the four largest, the interval includes zero (23 pulls up, 11 down; sign test p = 0.06). Round 1's was −0.4 [−1.2, 0.4]; the difference was not tested.

### Exploratory (not pre-registered)

| subset | n | right | Brier | 95% CI | bettor − up-word rule [95% CI] | bettor − swap-pair rule [95% CI] |
|---|---|---|---|---|---|---|
| the published sentence has the "up" word | 71 | 69 (0.97) | 0.057 | [0.041, 0.077] | −0.005 [−0.022, 0.014] | +0.018 [−0.001, 0.039] |
| the published sentence has the "down" word | 21 | 17 (0.81) | 0.113 | [0.052, 0.186] | −0.450 [−0.510, −0.376] | −0.477 [−0.577, −0.374] |
| more/less items | 45 | 44 (0.98) | 0.061 | [0.040, 0.088] | — | — |
| other word pairs | 47 | 42 (0.89) | 0.078 | [0.047, 0.116] | — | — |

## What it cannot do (from the pre-registration §6, with D25, D26 and D29)

- **The leakage checker is a Claude model, and it dropped 60% of the template's items.** The writing involved no Claude, but the selection still did.
- **Unlike round 1 (ss-b2), no baseline here encodes "the published sentence makes the paper look good".** A bettor using only that would not be excluded.
- **Single sentences, no methods summary; query buckets, not fields.**
- **One doubtful item kept.** r2-041's comment names ACM Collective Intelligence 2026. That conference used double-blind review: full papers were due 2026-06-15 and decisions came 2026-07-31. It allowed preprints during review, but none is known; arXiv v1 is 2026-08-04 (D29, D30). Removing the item changes nothing.
- **It scores the published wording, not the truth.** It covers one bettor model at one setting.

## Process and spend

| step | calls | cost | refusals |
|---|---|---|---|
| round-2 leakage check (claude-sonnet-5-5) | 243 | $0.72 | 0 |
| round-2 bettor, primary | 92 | $0.44 | 0 |
| round-2 bettor, order check | 46 | $0.22 | 0 |
| **program total, both rounds** | — | **$3.40** of the $5.00 cap | 0 |

## What would break it next

1. Done: `ledger/audits/ss-b5.md`.
2. **A valence comparator** (the audit's cheapest reversal test, about $0.45): a fresh no-tools model asked which sentence makes the paper look better, scored as a third comparator.
3. **Separate "knows the result" from "reads the sentence".** Re-ask the same 92 items with the sentence's other clauses removed, keeping only the clause that holds the swapped word. If the score holds, sentence-internal coherence is not doing the work. About $0.60.
4. **The audit's question about round 1, asked properly.** Have a non-Claude writer, or Sean, write post-cutoff items to the round-1 item spec. That needs another provider's key or Sean's time; the template cannot do it.
