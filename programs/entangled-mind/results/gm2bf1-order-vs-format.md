# gm2b-f1: do claims that move with question order also move with answer format? (Haiku, archive)

Pre-registered in `experiments/gm2bf1-order-vs-format.md`. Archive only; $0.

## In plain English

(Hand-written after the run; excluded from reproduce.py's comparison.)

**The question.** Program 1 found two ways Haiku's answer about a statement moves when it shouldn't: with the order the questions come in, and with the format the question is asked in. Are the same statements the unstable ones in both? We took Haiku's 160 deliberation claims, which appear in both archives. For each claim we measured how far its 0–100 rating moved across four question orders (10 conversations per order), and how far its rank among the 160 claims moved across six answer formats.

**What we found.** By the pre-registered rule, yes, partly: **pass, unreplicated.**
- The two measures are correlated: Spearman ρ = 0.34 [0.16, 0.49] (40 items carrying their claims, item-cluster bootstrap). The bar was 0.30 with the interval above 0.
- Allowing for how extreme each claim's rating was in both archives and how noisy its ratings were in the order conversations (the guard as fixed by the design review, D71), it is 0.25 [0.09, 0.37]. The guard as first frozen in the pre-registration, which allowed only for the format archive's extremity and the order noise, gives 0.09 [−0.09, 0.27] and would have failed. Allowing for the order noise alone gives 0.08 [−0.09, 0.26]. So the pass depends on which allowance is made, and noise alone accounts for the link.
- Dropping any one item does not change the verdict, but dropping two (h126 and h158) takes ρ to 0.27, below the bar, and ρ's interval runs down to 0.16. The link is in gm2b's 30 items (ρ 0.42) and absent from gm2's 10 (ρ −0.09).
- With Haiku's earlier answers hidden in the order conversations (secondary), the numbers are about the same: 0.33, and 0.20 after the allowance.
- Most of the order span goes with rating noise (ρ 0.77 with the within-order SD) and with mid-scale ratings (−0.79 with extremity in the order archive). The format spread goes with them less (0.38 and −0.23). The link between the two spreads is the part left over.

**Audit.** `ledger/audits/em-gm2bf1.md` (`a33652b`): the pass stands as pass, unreplicated, and is fragile, as the bullets above now say; its five cuts are applied verbatim (D75).

**What it means.** On these claims, being unstable under question order and being unstable under answer format partly go together after allowing for extremity in both archives and for rating noise in the order conversations. Allowing for that noise alone, they do not. That fits the idea that the model holds no stable answer about some claims, but this design does not show one cause. A shared cause not measured here, such as how ambiguous a claim's wording is, would produce the same pattern. The allowance cannot remove the boring explanation completely. In the design review's dry run, worlds with no shared instability passed this rule 0–10% of the time (6–10% where mid-scale claims wobble more in both). Those worlds understate how closely the order span follows rating noise (ρ 0.37–0.58 against the real 0.77), and in none of them did the review's guard come out above the original one, as it does here. So that rate is not a measured false-pass rate for these data. Two binary formats put 90 claims on one tied rank, so part of the format spread is tie position. With those ties broken at random instead of shared, ρ falls to about 0.24 (0.17–0.32) and reaches the 0.30 bar in 5% of tie orders; without the bet format (F3), ρ is 0.29. One model (Haiku), these 160 claims.

| claims | Spearman ρ(order span, format spread) [95%] | partial ρ given extremity and noise [95%] | verdict |
|---|---|---|---|
| 160 (40 items) | +0.336 [+0.159, +0.487] | +0.246 [+0.092, +0.368] | pass |

Secondary (cannot change the verdict):

- Order span vs extremity ρ -0.240; format spread vs extremity ρ -0.234; order span vs within-order SD ρ +0.772; format spread vs within-order SD ρ +0.377; order span vs order-archive extremity ρ -0.787; format spread vs order-archive extremity ρ -0.226.
- With earlier answers hidden (redacted): ρ +0.325, partial +0.202.
- Median order span 15.1 points; median format spread 0.165 (rank units).
- Items whose removal flips the verdict: none.
- Archive sha256: `gm2-conversations.json` e9d59385c62d2e48; `gm2b-conversations.json` a7cbe10e6329cfe7; `gm3b-calls.json` 0a5a27a4fda3b662.

**Novelty:** partly new. Published LLM work finds that sensitivity to one manipulation at a time concentrates on items the model is unsure about: prompt variants (Zhuo et al. 2024, arXiv 2410.12405), numeric anchors (Owusu and Feldman 2026, ACL 2026 Short Papers 174-180) and earlier conversation turns (Temkit 2026, arXiv 2605.22714: high-entropy items d −0.34 against −0.15); that predicts the raw order-format correlation we found (+0.34) and agrees with our frozen guard, under which allowing for rating noise removes it. In people, attitude-strength measures did not predict susceptibility to response effects (Krosnick and Schuman 1988, JPSP 54:940, 27 experiments, average −0.4%). No paper found correlates an item's sensitivity to question order with its sensitivity to answer format, on any model; the guarded residual (+0.25 under D71) is that untested part, and it is fragile. Search: WebSearch for "LLM belief consistency paraphrase versus elicitation format", "Westfall Yarkoni controlling for confounding constructs", "attitude strength susceptibility to response effects", "anchoring bias LLM confidence", 2026-11-05; ProSA, AMEL and Westfall-Yarkoni HTML and the Krosnick-Schuman and Owusu-Feldman PDFs opened; claude-opus-5-5, 2026-11-05c remap re-scout. *(Rule 13; written by a fresh claude-opus-5-5 reader subagent of the 2026-11-05c remap session, which ran none of these bets; its searches and reads are in programs/entangled-mind/map/reads/remap-2026-11-05c-em-gm2bf1.md.)*

## Pre-registered reading: **pass**

On Haiku's 160 deliberation claims, the claims whose rating moved more with question order tended also to be the ones whose rank moved more across answer formats (Spearman ρ = +0.34), and this held after allowing for how extreme the claim's rating was in both archives and how noisy its ratings were in the order conversations.
