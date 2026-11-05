# gm2b-f1: do claims that move with question order also move with answer format? (Haiku, archive)

Pre-registered in `experiments/gm2bf1-order-vs-format.md`. Archive only; $0.

## In plain English

(Hand-written after the run; excluded from reproduce.py's comparison.)

**The question.** Program 1 found two ways Haiku's answer about a statement moves when it shouldn't: with the order the questions come in, and with the format the question is asked in. Are the same statements the unstable ones in both? We took Haiku's 160 deliberation claims, which appear in both archives. For each claim we measured how far its 0–100 rating moved across four question orders (10 conversations per order), and how far its rank among the 160 claims moved across six answer formats.

**What we found.** By the pre-registered rule, yes, partly: **pass, unreplicated.**
- The two measures are correlated: Spearman ρ = 0.34 [0.16, 0.49] (40 items carrying their claims, item-cluster bootstrap). The bar was 0.30 with the interval above 0.
- The correlation survives the boring explanation, that claims rated near the middle wobble more in both, as do noisy ones. Allowing for how extreme each claim's rating was in both archives, and how noisy its ratings were in the order conversations, it is 0.25 [0.09, 0.37].
- Dropping any one item does not change the verdict.
- With Haiku's earlier answers hidden in the order conversations (secondary), the numbers are about the same: 0.33, and 0.20 after the allowance.
- Most of the order span goes with rating noise (ρ 0.77 with the within-order SD) and with mid-scale ratings (−0.79 with extremity in the order archive). The format spread goes with them less (0.38 and −0.23). The link between the two spreads is the part left over.

**What it means.** On these claims, being unstable under question order and being unstable under answer format partly go together, beyond how mid-scale or noisy a claim is. That fits the idea that the model holds no stable answer about some claims, but this design does not show one cause. A shared cause not measured here, such as how ambiguous a claim's wording is, would produce the same pattern. The allowance cannot remove the boring explanation completely. In the design review's dry run, built on measured numbers, worlds with no shared instability still pass this rule 6–10% of the time. Two binary formats put 90 claims on one tied rank, so part of the format spread is tie position. One model (Haiku), these 160 claims.

| claims | Spearman ρ(order span, format spread) [95%] | partial ρ given extremity and noise [95%] | verdict |
|---|---|---|---|
| 160 (40 items) | +0.336 [+0.159, +0.487] | +0.246 [+0.092, +0.368] | pass |

Secondary (cannot change the verdict):

- Order span vs extremity ρ -0.240; format spread vs extremity ρ -0.234; order span vs within-order SD ρ +0.772; format spread vs within-order SD ρ +0.377; order span vs order-archive extremity ρ -0.787; format spread vs order-archive extremity ρ -0.226.
- With earlier answers hidden (redacted): ρ +0.325, partial +0.202.
- Median order span 15.1 points; median format spread 0.165 (rank units).
- Items whose removal flips the verdict: none.
- Archive sha256: `gm2-conversations.json` e9d59385c62d2e48; `gm2b-conversations.json` a7cbe10e6329cfe7; `gm3b-calls.json` 0a5a27a4fda3b662.

## Pre-registered reading: **pass**

On Haiku's 160 deliberation claims, the claims whose rating moved more with question order tended also to be the ones whose rank moved more across answer formats (Spearman ρ = +0.34), and this held after allowing for how extreme the claim's rating was in both archives and how noisy its ratings were in the order conversations.
