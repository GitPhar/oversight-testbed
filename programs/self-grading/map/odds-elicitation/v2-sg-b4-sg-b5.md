# Odds elicitation, template v2 (rule 14): sg-b4 (sg-d12) and sg-b5 (sg-d11)

2026-11-05 09:57 America/Denver. Two fresh contexts (claude-opus-5-5 subagents), one per bet, each told to read only `ledger/prior.md` at `73eb5cf` and handed the bet's own description: title, one sentence on what the parent found, assumption at stake, design, models, cost, the pass rule as frozen, the Prior work line, and its rows on prior.md's tables (self-grading, model referee, under $1, literature, layer 2). Neither was given the map's odds, any earlier bet on the direction, audit or review notes, Sean's odds, or the other bet's odds.

| bet | direction | prior | adjustment | engine odds | reason (verbatim) | map odds (remap pass, not v2) |
|---|---|---|---|---|---|---|
| sg-b4 | sg-d12 | 0.32 | −0.17 | 0.15 | Literature (0.13), under $1 (0.19) and model referee (0.22) rows point down. The pass needs four conditions to hold together, and Opus is underpowered (T≥3.0, n=30). I discount layer 2 (0.67, six bets). | 0.30 |
| sg-b5 | sg-d11 | 0.32 | −0.10 | 0.22 | Literature (0.13), under-$1 (0.19) and model-referee (0.22) rows outweigh layer 2 (0.67, few bets); conjunctive rule needs Opus, parent 6.0, barely above +5; Sonnet 1.4 unlikely. | 0.45 |

Both moves are revisions before data; both numbers stay (`engine_odds_first`, `engine_odds`). The negation and paraphrase check (scout.md) is not run for follow-ups re-elicited at pre-registration.

## Re-elicitation of sg-b4, 2026-11-05 10:24 (D16; between d277c6f at 10:22:26 and fdb2588 at 10:25:01)

Design review sg-b4 (D12) found the description's Prior work line too strong: both papers vary role together with turn structure (Tsui: "role attribution and turn position cannot be varied independently within this design"), so the literature predicts the bundle effect and is silent on a quoted copy that keeps the lead-in and labels. A new fresh context was given prior.md and the corrected description (also naming the drift check's estimated 6-15% false-untestable rate) and nothing else.

| bet | prior | adjustment | engine odds | reason (verbatim) |
|---|---|---|---|---|
| sg-b4 | 0.32 | −0.14 | 0.18 | Rows model 0.22, under-$1 0.19 and literature 0.13 sit below the prior. The rule needs both Haiku and Opus to pass two CI tests, and Opus's 3.0 bar uses only 30 studies. Layer 2's 0.67 is from 6 bets. |

In force: 0.18. Kept: map 0.30 (`engine_odds_first`), first v2 0.15 (`engine_odds_v2_first`).
