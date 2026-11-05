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
