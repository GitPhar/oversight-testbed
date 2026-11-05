# Program 4 map: the published-record referee

Written 2026-11-04 17:12 America/Denver, before any drafted item had been read by this session, before any leakage-check call and before any bettor call.

## In plain English

The engine bets on findings that are already published, with the outcome hidden. A separate, tool-less session reads a masked question about each finding and says how likely each direction is; the published abstract then decides it. Because the papers are already out, hundreds of bets settle in a day at no experimental cost. The answers that count are from papers posted after the bettor's training cutoff (July–November 2026), so it cannot have read them. Older papers are scored separately, with the caveat that the bettor may simply remember them.

Three bets are stated here, with the engine's odds, before any data:

| id | event the odds are for | engine P(pass) |
|---|---|---|
| ss-b1 | On the post-cutoff items, the bettor's Brier score has a 95% bootstrap upper bound below 0.25 (it beats always saying 50%). | **50** |
| ss-b2 | On the post-cutoff items, the bettor beats the publication-bias baseline (0.75 on the paper's headline side where one is tagged, 0.5 elsewhere): paired difference in Brier with 95% upper bound below 0. | **30** |
| ss-b3 | The pre-cutoff items score better than the post-cutoff items: Brier(pre) − Brier(post) with 95% upper bound below 0 (a memory signal). | **35** |

Odds template: written by the item-writer session itself in one pass, in id order, before ranking, rationale under 100 words each (below). This is not the v1 fresh-context template of `operators/scout.md`; it departs from it because the item-writer is the only engine session in this program. The departure is recorded in DEVIATIONS.md D1.

## Rationales (each under 100 words)

- **ss-b1 (50).** A frontier model has broad priors about which way results in these fields usually go, and about a third of items may be "the proposed method helps" items that a prior about publication favours. Masking removes wording cues, and post-cutoff items cannot be recalled. Beating 0.25 with the CI's upper end below it needs a Brier near 0.21 at about 100 items. My unadjusted guess was 60; lesson P1 (odds too high where the engine had a story; running base rate 0.22) moves it to 50.
- **ss-b2 (30).** Beating a baseline that already exploits publication bias requires real field knowledge beyond "papers report that their method works". Many items are descriptive, where the baseline says 0.5 and any skill counts; but the paired CI must clear 0. Moderate odds, lowered for P1.
- **ss-b3 (35).** Pre-cutoff papers could be recognised despite masking, which would show as a better score. But masking removes titles and method names, the pre set is smaller (wider CI), and recall of directional detail from abstracts is patchy. A real gap of about 0.06 would be needed to clear the CI.

Human odds: not recorded for ss-b1 to ss-b3. Sean's part in this program is the 20-item form at direction level (`human/form.md`), which scores his calls against the same published record, item by item.

## Round 2 (written 2026-11-04 19:17 America/Denver, before any round-2 item exists and before any paper for it was opened)

ss-b1 used items written by the same model family as the bettor. The audit's cheapest overturning test is a writer outside that family. No other provider's key was looked for: this session's permission rules block credential exploration. So the round-2 writer is **no model at all**: a fixed, deterministic template (`protocol/template-writer.md`). It takes one comparative result sentence from each paper's abstract and offers it beside the same sentence with its one direction word swapped.

| id | event the odds are for | engine P(pass) |
|---|---|---|
| ss-b4 | On at least 60 post-cutoff template-written items, the bettor's Brier score has a 95% bootstrap upper bound below 0.25: ss-b1's pass, replicated with a writer outside the bettor's family. | **70** |
| ss-b5 | On the same items, the bettor beats a dumb rule that puts 0.75 on whichever option carries the "up" word (higher, more, better, …): paired Brier difference with 95% upper bound below 0. | **35** |

Rationales (each under 100 words):
- **ss-b4 (70).** ss-b1 scored 0.163 with curated, context-rich items. Template items give one sentence and no methods summary, and some will be weaker results. But result sentences in abstracts often state the direction a field expects ("outperforms", "higher accuracy than"), and the bettor knows that. I expect a Brier near 0.20 on about 100 items, which clears 0.25 more often than not. I am not lowering toward the ledger's pooled base rate: in ss-b1 that move cost Brier 0.16 → 0.25, and that rate pools other referees.
- **ss-b5 (35).** Abstracts mostly report improvements, so the up-word rule may itself score near 0.21. Beating it needs real knowledge of which direction each finding went, on single sentences. That is possible, but below even odds.

## Round 2b: the valence comparator (written 2026-11-04 20:09 America/Denver, before any valence call)

The ss-b5 audit's open rival is that the bettor "picks the version that flatters the paper", not that it knows results. Test it: on the same 92 items, in the same option order, a fresh no-tools claude-opus-5-5 at the bettor's setting is asked only *which sentence makes the paper's own method or result look better*. Its probability on the published sentence becomes a third comparator. No other provider's key was looked for.

| id | event the odds are for | engine P(pass) |
|---|---|---|
| ss-b6 | Both legs' paired Brier upper bounds below 0 on at least 60 items: raw (bettor minus valence rule) and recalibrated (each side's rating plus the up word, same leave-one-out logistic); untestable if gate G1 fails (rater favours the up word on fewer than half its non-50 ratings). | **35** (first 25; revised before data, D33/D37: moved toward the running base rate (0.41) before data, a move that needs no further reason (operators/learn.md).) |

Rationale (under 100 words): the audit found most of the bettor's down-word hits were sentences where the down word is the paper's win ("lower noise", "costing less"), and three of its four misses reported limitations. Published sentences mostly report wins, so a flattery rule should score close to the bettor. To beat it, the bettor would need to be right where the published sentence is unflattering, and there are few such items. Below even odds.
