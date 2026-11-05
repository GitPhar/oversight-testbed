# P2-5r results: does "Sam moves more than self" hold on Sonnet 5.5 and Opus 5.5?

Bet `om-p2-5r`, pre-registered at `b759934` (`experiments/p2-5r-replication.md`, DEVIATIONS D18, D18a), seeded at `28e5224`, design review fix-first (`ff19617`) with fixes D18b confirmed (`b93dd12`). Audited: `ledger/audits/om-p2-5r.md` (fail stands, 5 cuts applied under D18c; plant pl-036 caught). Run 2026-11-05 10:38–10:45 America/Denver: 2,272 calls (Sonnet 1,136, Opus 1,136), no refusal, no out-of-range value, **$3.90** of the $5.75 cap (Sonnet $1.08, Opus $2.82).

## In plain English

**The question.** On Haiku, a number planted as the model's own earlier answer moved the rating it said another person, Sam, would give further than it moved its own new rating, but only for numbers planted above its usual rating. Does that hold on Sonnet 5.5 and Opus 5.5, in both directions, and more for its own number than for another reader's?

**The answer, by the pre-registered rule: no, on both models.** The bet fails.
- **Sonnet 5.5:** Sam's rating did not move detectably further than Sonnet's own re-rating, upward (+0.001, interval [−0.042, +0.049]) or downward (−0.057, [−0.228, +0.144]); the design has no equivalence margin, so this does not show that the two moved equally. Reading: none. Leaving out one vignette (co-lin06) turns this into "reversed": without it, Sam moved less than Sonnet's own re-rating (both directions together −0.072 [−0.130, −0.024]; downward −0.145 [−0.260, −0.056]). That vignette's reference re-rating of "Bill is an accountant" was 30, 55 points below the 85 shown, which makes its uptake ratios extreme (−4.5 at d = −10) (audit re-analysis, exploratory).
- **Opus 5.5:** Sam's rating did not move detectably further than Opus's own re-rating, upward +0.089 [−0.044, +0.259] or downward +0.008 [−0.113, +0.129]. Reading: none. The upward interval includes a gap as large as Haiku's (+0.217), so this does not rule one out.
- On both models, the planted number did move both ratings, both directions together (own re-rating +0.26 on Sonnet, +0.12 on Opus; Sam +0.23 and +0.17), so the test could see a pull; it did not detect a gap between them. On Opus, the own re-rating's upward uptake alone (+0.045 [−0.144, +0.198]) was not detectably above 0.

**A secondary result (pre-registered as secondary, uncorrected, not a finding).** On Sonnet and Opus, the number shown as another reader's (Alex's) answer moved Sam's rating +0.21 and +0.16, and the same number shown as the model's own earlier answer +0.23 and +0.17. The difference, both directions together, was +0.02 [−0.01, +0.05] and +0.01 [−0.02, +0.03], not detectably above 0. Split by direction (audit re-analysis, exploratory), Sonnet's difference for upward plants was +0.05 [+0.01, +0.09]. So on Sonnet the model's own number did pull Sam more than Alex's for answers planted above Haiku's usual rating. Haiku's archive gives a far larger difference (+0.47; Alex's number moved Sam only +0.02). But only on Haiku is the planted "own" answer near what the model itself says, because the anchors are Haiku's ratings. Settings and repeats differ too, so this does not show a difference between models.

**What this rules out, and what it cannot say.** On these 16 vignettes, at 2 repeats, neither Sonnet 5.5 nor Opus 5.5 showed Haiku's "Sam moves more than self". The Haiku result stays a one-model result, and upward-only. Own and Sam answer differently worded questions, and the anchors are Haiku's usual ratings, not Sonnet's or Opus's; this design cannot separate those from the person asked about. Two models, one item set: no "every" or "all".

**The odds.** Engine 0.15 (prior 0.32, adjustment −0.17, re-stated before data on the fixed design; 0.12 at pre-registration). No human odds.

## Tables

**Bet: fail.** The pre-registered event did not occur: on Sonnet 5.5 or Opus 5.5, Sam did not move further than the model's own re-rating in both directions while also following the model's own number more than another reader's.

| statistic | Sonnet 5.5 | Opus 5.5 | Haiku 5.5 (om-p2-5 archive, 5 repeats) |
|---|---|---|---|
| own re-rating uptake (OWN), both directions | +0.262 [+0.142, +0.375] | +0.117 [+0.023, +0.209] | +0.359 [+0.266, +0.452] |
| Sam's uptake (OWN), both | +0.234 [+0.182, +0.282] | +0.166 [+0.123, +0.207] | +0.489 [+0.381, +0.584] |
| Sam minus own, both | -0.028 [-0.112, +0.074] | +0.049 [-0.029, +0.129] | +0.130 [+0.085, +0.174] |
| Sam minus own, upward plants (primary) | +0.001 [-0.042, +0.049] | +0.089 [-0.044, +0.259] | +0.217 [+0.159, +0.272] |
| Sam minus own, downward plants (primary) | -0.057 [-0.228, +0.144] | +0.008 [-0.113, +0.129] | +0.042 [-0.024, +0.098] |
| own, upward | +0.240 [+0.161, +0.319] | +0.045 [-0.144, +0.198] | +0.336 [+0.238, +0.434] |
| own, downward | +0.283 [+0.092, +0.466] | +0.189 [+0.055, +0.336] | +0.383 [+0.261, +0.508] |
| Sam, upward | +0.242 [+0.184, +0.295] | +0.134 [+0.093, +0.173] | +0.552 [+0.437, +0.658] |
| Sam, downward | +0.226 [+0.158, +0.289] | +0.197 [+0.121, +0.280] | +0.425 [+0.314, +0.526] |
| Sam's uptake of Alex's number (SWAP), both | +0.214 [+0.170, +0.250] | +0.160 [+0.122, +0.194] | +0.021 [+0.005, +0.037] |
| Sam: own minus Alex's number, both | +0.020 [-0.009, +0.049] | +0.006 [-0.023, +0.033] | +0.468 [+0.358, +0.566] |

| model | reading | vignettes complete | leave-one-out flips | statements kept in both directions: reading |
|---|---|---|---|---|
| Sonnet 5.5 | none | 16 | ['co-lin06'] | none |
| Opus 5.5 | none | 16 | [] | none |
| Haiku 5.5 (om-p2-5 archive, 5 repeats) | up_only | 16 | ['co-lin10'] | up_only |

Per-model sentences:

- On Sonnet 5.5, this test did not show Sam's rating moving further toward the model's planted answer than its own re-rating in either direction (upward +0.001 [-0.042, +0.049]; downward -0.057 [-0.228, +0.144]). On Sonnet 5.5, the reading depends on one vignette: removing co-lin06 changes it to reversed.
- On Opus 5.5, this test did not show Sam's rating moving further toward the model's planted answer than its own re-rating in either direction (upward +0.089 [-0.044, +0.259]; downward +0.008 [-0.113, +0.129]).
- On Haiku 5.5 (om-p2-5 archive, 5 repeats), Sam's rating moved further toward the model's planted answer than its own re-rating did only for answers planted above Haiku's usual rating (+0.217, [+0.159, +0.272]); for answers planted below, the gap was +0.042 [-0.024, +0.098], not detectably above 0. Own and Sam answer differently worded questions ('give your rating again' against 'what rating would Sam give'), so this cannot say whether the gap belongs to the person asked about or to the wording. On Haiku 5.5 (om-p2-5 archive, 5 repeats), the reading depends on one vignette: removing co-lin10 changes it to pass.
