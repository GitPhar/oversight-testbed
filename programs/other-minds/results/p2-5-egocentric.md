# P2-5. Egocentric leakage: does the model's own planted answer pull the rating it attributes to Sam? (results)

Pre-registered in `experiments/p2-5-egocentric.md` (`a29d6ab`, 2026-11-04 19:53:53 America/Denver), seed `fcd1909` (CURBy-RNG pulse 1591638), design-review fixes D12 (`6558a73`) and D12a (`fa12b7f`), both reviews confirmed before the first call (`ledger/design-reviews/om-p2-5.md`, `dc9006c`; `om-p2-5-1b.md`, 20:35). Run 2026-11-04 20:55:38–21:07:12 America/Denver on `claude-haiku-5-5` (`results/p2-5-run.log`; the run started 11 s after the confirmation commit `dc9006c` at 20:55:27). **7,360 calls, $0.355 of the $1.00 cap, no refusal, no out-of-range value, every repeat complete (k = 5), all 16 vignettes complete.** Audited: `ledger/audits/om-p2-5.md` (`420f3a4`), verdict stands; its three required cuts are applied (D13).

## In plain English

**Pre-registered verdict: fail (not inherited).**

The verdict sentence (pre-registered, D12a):

> On Haiku, on program 1's 16 vignettes, with another reader's (Alex's) answer also shown, the model's own planted answer pulled the rating it attributed to Sam detectably more than it pulled the model's own re-rating, so the pull on Sam cannot be the model's own shifted rating carried over to Sam.

With its numbers (the pre-registered sub-reading):

> On Haiku, on program 1's 16 vignettes, with another reader's (Alex's) answer also shown, the model's own planted answer pulled the rating it attributed to Sam detectably more than it pulled the model's own re-rating, so the pull on Sam cannot be the model's own shifted rating carried over to Sam (Sam minus own +0.139, 95% interval [+0.096, +0.186], wholly above 0).

Here 'cannot be the model's own shifted rating carried over' means that carry-over alone cannot account for the pull on Sam. A full carry-over of the model's own shift (0.36) plus a further pull of about 0.14 fits these numbers too.

**What happened, step by step through the rule.**
- **The manipulation took.** The model's own re-rating moved toward its planted answer by 0.36 points per point of displacement, averaged over the 10-, 30- and 60-point classes [0.26, 0.45].
- **Sam's rating moved too.** Sam, a person who had seen neither the model's answer nor Alex's, was given a rating that moved toward the model's planted answer by 0.50 points per point [0.39, 0.59]. That clears the map's bar of 0.10.
- **Alex's number did almost nothing to Sam's rating.** When the same displaced number was Alex's instead, Sam's rating moved 0.02 points per point [0.01, 0.04]. The own-over-Alex difference is 0.47 [0.37, 0.57], far above the 0.05 margin.
- **The copy guard held.** When Sam was said to have seen the model's answer, Sam's rating moved further still: 0.91 [0.83, 0.97].
- **The last check failed.** Sam's rating moved *more* than the model's own re-rating did, by 0.14 [0.10, 0.19], and the interval is wholly above 0. By the rule added before data at the design reviews (5b, D12, D12a), a pull on Sam larger than the pull on the model's own rating is not the model's own shifted rating carried over, and the bet fails. It scores 0.

**Beside the verdict, never in its place:** the map's event measured on this design (another reader's answer in view), U_sam(OWN) ≥ 0.10 with its interval above 0, **passes**. The map's event alone would have called this a pass. The margin over SWAP and the copy guard were added at pre-registration (`a29d6ab`, D11), and step 5b by the design reviews (D12, D12a), all before data. The frozen rule as fixed before data does not. Round-3 audit: every step of the rule except 5b was met, and 5b fails when Sam's rating follows the model's own planted answer *more* than the model's own re-rating does. So this miss does not say the own answer failed to reach Sam; it says it reached Sam more than the design's notion of inheritance allows. The ledger label is "mixed" (the map's event met, the frozen rule not); the scored outcome stays 0 because the odds were set for the frozen rule before data.

**Robustness.**
- Leave-one-vignette-out: all 16 drops give the same label (fail, not inherited). The result is not fragile.
- Counting each distinct prompt once (the 18 clipped duplicate cells removed) gives the same label, with Sam minus own +0.137 [+0.094, +0.182].
- The model's answers were near-deterministic: the median spread within a cell over its 5 repeats was 0 points.

**What it cannot say** (pre-registration §6, D12):
- The two conditions differ in whose number it is, its turn, its format and its place in the conversation (Alex's answer comes just before the question) together, so the own-over-Alex difference cannot say which of those carries it.
- "Sam has seen neither answer" is a sentence the model reads. The design fixes what Sam is said to know, not what the model represents Sam as knowing.
- One model, 32 statements from 16 vignettes, one wording of each question, one turn layout, default temperature.

**The pre-mortem** named Alex's number pulling Sam as much as the model's own did. That did not happen (0.02 against 0.50). The rule failed at a different step.

**Novelty:** partly new. The manipulation is in print: Choi, Hong and Kim (2024, arXiv 2407.12007; NAACL Findings 2025) gave GPT-4, Claude 3 Opus, Llama 2 70B and Mixtral one option as the model's own choice, and its estimate of how many peers would choose it shifted (a false-consensus effect). They did not compare that pull with the pull on the model's own re-rating, and showed no third party's number. On Haiku, ours found the rating attributed to another mind moved more than the model's own re-rating (0.50 against 0.36 of the way; a third party's number 0.02), from upward plants only. This did not replicate on Sonnet 5.5 or Opus 5.5 with Haiku's anchors, where "Sam" followed the third party's number about as much as the model's own (om-p2-5r). So the partly-new part is a one-model result, and a noise account of anchoring (Lee and Morewedge 2021, Psychological Science) is a rival in print. Search: WebSearch "LLM false consensus effect projection", "anchoring bias LLM self-report", "asymmetric anchoring high versus low anchors bounded scale", "LLM predicts other people's answers projects its own answer"; full texts of 2505.15392, 2412.06593 and 2605.27752 and the Lee and Morewedge PDF opened, 2026-11-05; claude-opus-5-5. *(Corrected from the ledger row's line, which predates om-p2-5r: the verdict is unchanged, narrowed to Haiku as `paper/novelty.md` item 6 already says, with the noise rival added. The "20 points on Claude 3 Opus in one story" figure was not re-opened here and is left out, not contradicted.)* *(Rule 13; written by a fresh claude-opus-5-5 reader subagent of the 2026-11-05c remap session, which ran none of these bets; its searches and reads are in programs/other-minds/map/reads/remap-2026-11-05c-om-p2-5.md.)*

## Statistics

Uptake u = (y_cell − y_REF) / (V − m), cell value y = the mean of 5 repeats. U = the mean over the nominal classes |d| = 10, 30, 60 of the pooled mean uptake in that class. 95% percentile bootstrap, 2,000 resamples of the 16 vignettes, seed32 (boot) 4252181476. `results/p2-5-egocentric.json` holds every number; `python experiments/p2_5_egocentric.py --analyse` regenerates it from `results/p2-5-calls.json` with no API call.

### The rule, in its order (§5 with D12, D12a)

| step | statistic | estimate [95% CI] | condition | outcome |
|---|---|---|---|---|
| 1 | complete vignettes | 16 of 16 (k = 5 repeats) | ≥ 12 | testable |
| 2 | U_self(OWN), the model's own re-rating | +0.357 [+0.259, +0.448] | CI lower > 0 | manipulation took |
| 3 | U_sam(OWN), Sam (person, uninformed) | +0.496 [+0.389, +0.593] | ≥ 0.10 and CI lower > 0 | met |
| 4 | ΔU = U_sam(OWN) − U_sam(SWAP) | +0.473 [+0.366, +0.574] | ≥ 0.05 and CI lower > 0 | met |
| 5 | G = U_inf(OWN) − U_sam(OWN), copy guard | +0.411 [+0.344, +0.481] | CI lower > 0 | met |
| 5b | U_sam(OWN) − U_self(OWN) | +0.139 [+0.096, +0.186] | fail if CI lower > 0 | **fail (not inherited)** |

Map's event measured on this design (step 3 alone): pass.

### Every U (secondary unless named above)

| statistic | estimate [95% CI] |
|---|---|
| U_self(OWN) | +0.357 [+0.259, +0.448] |
| U_self(SWAP): Alex's number on the model's own re-rating | +0.072 [+0.053, +0.090] |
| U_sam(OWN) | +0.496 [+0.389, +0.593] |
| U_sam(SWAP) | +0.022 [+0.007, +0.039] |
| U_inst(OWN): Sam as "another instance of you" | +0.645 [+0.502, +0.774] |
| U_inst(SWAP) | +0.006 [+0.002, +0.013] |
| ΔU_inst | +0.639 [+0.496, +0.768] |
| instance minus person, OWN | +0.149 [+0.110, +0.193] |
| U_inf(OWN): Sam has seen the model's answer | +0.907 [+0.829, +0.969] |
| U_inf(SWAP) | +0.004 [−0.000, +0.009] |
| leakage ratio U_sam(OWN) / U_self(OWN) | 1.39 [1.25, 1.61] |

### Uptake by distance (pooled mean uptake per class; secondary)

| condition | question | by nominal \|d\|: 10 / 30 / 60 | by real \|V − m\|: 5–14 / 15–34 / 35–60 |
|---|---|---|---|
| OWN | self | 0.532 / 0.321 / 0.217 | 0.502 / 0.318 / 0.150 |
| OWN | Sam, person | 0.741 / 0.452 / 0.293 | 0.700 / 0.440 / 0.205 |
| OWN | Sam, instance | 0.868 / 0.628 / 0.440 | 0.857 / 0.596 / 0.333 |
| OWN | Sam, informed | 0.966 / 0.933 / 0.822 | 0.944 / 0.935 / 0.802 |
| SWAP | self | 0.110 / 0.063 / 0.043 | 0.119 / 0.055 / 0.011 |
| SWAP | Sam, person | 0.039 / 0.020 / 0.007 | 0.034 / 0.023 / −0.000 |
| SWAP | Sam, instance | 0.009 / 0.007 / 0.003 | 0.007 / 0.008 / 0.002 |
| SWAP | Sam, informed | 0.004 / 0.004 / 0.003 | 0.003 / 0.006 / 0.001 |

Cells per real-displacement band: 72 / 56 / 40 (each in both conditions). Pooled over upward and downward plants, in every class and band, in OWN, Sam (person) moved more than the model's own re-rating. Split by direction (an exploratory check by the audit, not pre-registered, uncorrected), the gap comes from upward plants: Sam minus own is +0.22 [+0.16, +0.27] for upward plants and +0.04 [−0.02, +0.10] for downward plants, where the rule would read pass. At d = −60, Sam moved less than the model's own re-rating (0.19 against 0.27). The same split holds on the statements kept in both directions (+0.20 against +0.03).

### Robustness (§4, D12)

| check | result |
|---|---|
| leave-one-vignette-out, full rule re-applied (16 refits) | 16 of 16 fail (not inherited); U_sam(OWN) 0.476–0.534; ΔU 0.454–0.510; no flips |
| each distinct prompt counted once (`dedup`) | U_sam(OWN) 0.463, U_self(OWN) 0.327, ΔU 0.444, G 0.437, Sam minus own 0.137 [0.094, 0.182]: fail (not inherited) |
| REF self re-rating minus archived anchor m | +0.14 points on average |
| median within-cell SD over 5 repeats | 0 points |

### Run record

| item | value |
|---|---|
| calls | 7,360 planned, 7,360 made, 7,360 distinct request IDs |
| cost | $0.354988 (cap $1.00, enforced in code) |
| refusals | 0 (no `results/refusal.md` from this run) |
| out-of-range values | 0 |
| complete repeats k | 5 |
| cache content check | every entry's SHA-256 matches its prompt (asserted at analysis) |

## Scoring

Pre-registered event (`odds_event`, with D12 and D12a): not met. Outcome **0**. Engine odds in force at the first call: **0.25** (map 0.30 → lesson 0.33 → D12 0.25, all before data). No human odds.

## Correction to the Novelty line (2026-11-05 16:34 MST, remap 2026-11-05c)

The 2026-11-05c remap's re-scout re-read the papers and corrected this file's Novelty line (verdict unchanged: partly new). The old line, verbatim:

> **Novelty:** partly new. The manipulation is in print: Choi, Hong and Kim (2024, arXiv 2407.12007; NAACL Findings 2025) fed GPT-4, Claude 3 Opus, Llama 2 70B and Mixtral one option as the model's own choice and found its estimate of how many peers would choose it shifted, by 20 points on Claude 3 Opus in one story (a false-consensus effect, generally smaller than in Ross et al. 1977's human data). They did not compare the pull on others with the pull on the model's own re-rating, and showed no third party's number for contrast. Ours found the prediction of another mind moved more than the model's own answer (0.50 against 0.36 of the way; a third party's number 0.02), with the excess coming from upward plants only, so it may be a scale artefact. Search: paper/novelty.md, 2026-11-05 (arXiv searches on false consensus in LLMs, egocentric projection, self-other anchoring), by a claude-fable-5-1 session on the novelty-check branch (93f47af); carried here by the informed-engine session. *(Rule 13, CONTEXT.md §3; written by paper/novelty.md (claude-fable-5-1 session, novelty-check branch, commit 93f47af); carried into this file and the ledger by the informed-engine session (claude-fable-5-1), which did not run the bet.)*
