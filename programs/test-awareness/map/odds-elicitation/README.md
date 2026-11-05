# How the engine's odds for program 6 were elicited

Written 2026-11-05 (America/Denver), after the reads (eb3b40d) and before any program-6 data (the only calls so far are the 6-call machinery probe, DEVIATIONS T0, on content no direction uses).

## Procedure (odds template v1, `operators/scout.md`; variant `v1-batch`, as program 3)

1. **The rows.** The scout wrote one row per open direction (`rows-v1.md`, 11 rows), each with the assumption at stake, prior work, our data, the cheapest test, its cost and a draft pass rule, and the paraphrased pass rules (`rows-paraphrase.md`). Both are committed **before** any odds exist and before the random half is drawn.
2. **The random half.** Drawn from the first CURBy-RNG pulse timestamped after the rows commit (CURBY-Q stalled: latest completed round 28297, 2025-08-22 13:42). seed = `ledger/seed.py <randomness> ta-map --purpose elicit-half`; the half is `random.Random(seed).sample(sorted ids, 6)` (6 of 11). Filled in below by the next commit.
3. **The headline odds** (`v1.md`): one fresh subagent context (`claude-opus-5-5`) that reads only `rows-v1.md`, no reads files, no ranking, no weights, no human odds, no ledger. For each row in id order: a rationale of at most 100 words, then one integer from 1 to 99, P(pass), on the scale 0 = certainly will not pass, 100 = certainly will.
4. **The elicitation check:** two more fresh contexts on the drawn half: paraphrase (`check-paraphrase.md`, rules from `rows-paraphrase.md`) and negation (`check-negation.md`: P(the rule will **not** be met)). Headline odds stay the v1 numbers; spread and |P(pass) + P(not pass) − 100| are published.
5. **The ranking** is set afterwards by the scout in `../program-6-map.md`, and the odds are not revised after ranking.

**Departure from the template (as program 3):** one fresh context sees all 11 rows instead of one context per row, so cross-row anchoring is possible. Logged as `v1-batch`.

## The random half

`chain:` CURBy-RNG · `pulse_index:` 1592176 · `pulse_time:` 2026-11-05 04:52:00 America/Denver (11:52:00.152Z; previous pulse 1592175 at 04:51:00, before the rows commit f9136a9 at 04:51:57) · `randomness:` 198b86b6b26e2c55ad7a10f4a958d1bde543f82e8a66310056999dcef970a2c582e1ff4c88f1f1c8dc91be63976d6d88edb6bdc7a8c0805da82af5bf93cdf731 · `client:` @buff-beacon-project/curby-client@1.2.0 (`Client.randomness(1592176)`) · `certificate_verified:` false (classical chain) · `seed:` 13088965802074220129 (`--purpose elicit-half`).

Ids in numeric order (ta-d1 … ta-d11); `random.Random(13088965802074220129).sample(ids, 6)` → **ta-d2, ta-d3, ta-d4, ta-d5, ta-d7, ta-d8**.
