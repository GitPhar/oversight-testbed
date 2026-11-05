# sg-b6: same-run re-grade, does sg-b4's turn-role reading on Haiku hold when every grade comes from one run? (result)

Pre-registered in `experiments/sg-b6-samerun.md` (`738472c`, 2026-11-05 11:40 America/Denver), direction sg-d13. The seed is CURBy-RNG pulse 1592585 (`08043ce`).
- **Design review** (`ledger/design-reviews/sg-b6.md`): fix-first with 2 flaws (`20c8185`), no pilot. The fixes are D23 (`124b665`), confirmed go at 12:02 (`4a55e29`), before the first call.
- **Run:** 2026-11-05, 12:05:20 to 12:08:53 America/Denver. **960 calls, complete, no refusal, $0.642** of the $0.80 cap. The program has spent **$5.93 of $7.65** (budget ruling br-016, D19).
- **Odds:** engine 55 (v2, re-elicited before data under D23; the first v2 number was 16; the map stated none). Sean's odds: 55 (`ho-20261105-112945-5te`).
- **Audit:** pending.

## In plain English

**Pre-registered verdict: mixed.** In the pre-registered words (§5.3):

> On Haiku 5.5, with every grade taken in one run, the change was +5.26 points [+2.02, +8.43], which neither clears the 6.3 bar with the guard met nor lies wholly below it: this test cannot say whether sg-b4's Haiku reading holds on a same-run comparison.

**What was done.**
- sg-b4 showed Haiku its own writing conversation as a quoted copy and found it docked a planted exaggeration 6.8 points (of 100) more there than in its own reply, against a bar of 6.3. Its own-reply grades came from sg-b3's run an hour earlier.
- Here every grade was taken in one sitting: Haiku graded its own reply and the quoted copy, each with and without the exaggeration, on all 60 studies, every version twice. Sonnet and Opus graded the same four versions once, on sg-b4's 30 studies.
- The measure, T, is how much more the exaggeration cost in the quoted copy than in the model's own reply, both from this run.

**What the numbers say.**
- **Haiku:** in its own reply the exaggeration cost 67.7 points, in the quoted copy 73.0. T = +5.3 [+2.0, +8.4]. That is below its 6.3 bar, and the interval runs from 2.0 to 8.4, so it neither clears the bar nor rules it out. The flawed text itself scored 4.15 points lower in the quoted copy [+0.9, +7.5], so the guard held.
- **Haiku graded fresh in the same run** docked the exaggeration 11.5 points more than in its own reply [+8.7, +14.4]: sg-b3's blunting came back in this run at about the same size (sg-b3: 12.6). The quoted copy took away 46% of it, just under the half the bar asks for.
- **Opus** (30 studies, reported, not scored): T = +5.0 [+3.8, +6.1], against its 3.0 bar, reading turn role. On a same-run comparison Opus's sg-b4 result holds, and is larger (sg-b4: +4.0 on the same studies).
- **Sonnet** (reported): T = +0.7 [−0.9, +2.2]; it showed almost no blunting in sg-b3, and almost none to remove here.

**Why Haiku's number fell.** On the same studies sg-b4's cross-run T was +6.8; this run's is +5.3. The fall is split between the two cells. Haiku's own-reply penalty came out 0.8 points larger than in sg-b3's run [−0.6, +2.4], and its quoted-copy penalty 0.7 smaller than in sg-b4's run [−1.9, +0.2]. Neither shift alone is distinguishable from zero. The −4.3-point drift sg-b4 measured on 10 studies did not reappear across all 60.

**How strong it is.**
- Haiku's two repeats agree in direction: T is +4.9 on the first repeat alone and +5.7 on the second. 55% of its grades were identical across the two repeats, and the rest moved by 4.5 points (SD), mostly on the flawed texts.
- Haiku's median T is +5.0 and its 10% trimmed mean +5.3, both below the bar; one tie. Dropping any one study or any one domain does not change the reading.
- Opus's reading is not fragile either way; its median T is +4.5.

**So, on this test:** with every grade from one run, the quoted copy still made Haiku clearly stricter about the exaggeration than its own reply (T above 0), but by less than the half of its blunting that sg-b4's bar asked for, and the interval cannot say whether the true change is above or below that bar. sg-b4's Haiku half therefore does not hold up as a clean pass on a same-run comparison: it reads undetermined. Opus's half does hold, more strongly than in sg-b4. The record of sg-b4 itself is unchanged (its verdict was read on its own rule and audited).

**What this does not show** (§6):
- The quoted copy still differs from the own reply in role, message count, header sentence, quoted blocks and where the grade question sits: the change is about that bundle, as sg-b4's was.
- Two repeats on Haiku, one on Sonnet and Opus; Sonnet's and Opus's repeat noise is not measured here.
- Opus and Sonnet on 30 studies; their readings are reported, not scored.
- The exaggeration was planted, one wording, at the end. Three models from one family, one item set. Not "models", not "every".
- **Multiplicity:** one scored reading with a gate and a guard; no correction.

**Novelty:** partly new. Papers in print already show, in our direction, that a model goes easier on the same text in its own assistant turn than in a user turn (Khullar, Hopkins, Wang and Roger 2026, arXiv 2603.04582 v1, strongest on-policy; Tsui 2025, arXiv 2507.02778 v3), and they show the rival this test removes: LLM judges disagree with themselves across identical runs (Haldar and Hockenmaier 2025, Rating Roulette, arXiv 2510.27106: Krippendorff's alpha 0.265 to 0.563 over three runs on MT-Bench, three open-weight judges; Norman, Rivera and Hughes 2026, arXiv 2606.19544 v1: test-retest above 0.95 alongside position bias above 0.10), and human rating separates drift within a session from "scale instability" across sessions (Quellmalz 1980, CSE Report 136, abstract only). The nearest case of a self-favouring effect shrinking under a stricter comparison is Roytburg et al. 2026 (arXiv 2601.22548 v2: "only 51% of initial findings retain statistical significance" once a judge's votes for its own wrong answers are set against its votes for outcome-matched other models' wrong answers), which changes the baseline, not the run, and reports no repeated runs. A direct search found nothing in print that re-measures a quoted-copy leniency gap with every cell graded in one run, set against the same gap read across runs. Here Haiku 5.5's gap stays above zero but is 46% of its same-run blunting, under the 6.3 bar with an interval that cannot rule the bar out (its fall from sg-b4 is split between the two cells, neither shift distinguishable from zero, so run-to-run noise is neither shown nor ruled out as the cause), while Opus 5.5's holds at about its full size (+5.0, against sg-b4's +4.0). Search: WebSearch and arXiv abs/HTML, 2026-11-05: "LLM judge self-attribution bias same run versus cross run"; "LLM-as-a-judge test-retest reliability between sessions drift"; "monitor leniency own assistant turn versus quoted transcript in user message"; "self-preference bias replication measurement artifact"; "LLM evaluation nondeterminism score shift baseline from earlier run"; "batch effects high-throughput data"; "rater drift within-session versus between-session". By a fresh claude-opus-5-5 Novelty session (subagent).

## Tables

| model | studies | repeats | T | 95% CI (20 domains) | 95% CI (studies) | F | F 95% CI (domains) | penalty, quoted copy | penalty, own turn | reading |
|---|---|---|---|---|---|---|---|---|---|---|
| Haiku | 60 | 2 | +5.26 | [+2.02, +8.43] | [+2.55, +7.87] | +4.15 | [+0.86, +7.46] | 73.0 | 67.7 | **undetermined** |
| Opus | 30 | 1 | +5.03 | [+3.80, +6.14] | [+3.87, +6.17] | +4.00 | [+3.17, +4.81] | 83.8 | 78.8 | turn role |
| Sonnet | 30 | 1 | +0.70 | [−0.91, +2.21] | [−0.93, +2.23] | +1.10 | [0.00, +2.07] | 88.6 | 87.9 | reported only |

|  | Haiku | Opus | Sonnet |
|---|---|---|---|
| sg-b4's T on the same studies (cross-run) | +6.82 | +3.97 | +1.33 |
| own-turn penalty, this run − sg-b3's | +0.82 | −0.90 | +0.53 |
|   95% CI (domains) | [−0.62, +2.42] | [−2.11, +0.21] | [−0.79, +1.79] |
| quoted penalty, this run − sg-b4's | −0.74 | +0.17 | −0.10 |
| clean text, quoted − own (points) | +1.11 | +1.03 | −0.40 |
| same-run blunting G (fresh − own; Haiku only) | +11.53 | — | — |
|   95% CI (domains) | [+8.73, +14.42] | — | — |
| T as a share of the same-run G | 0.46 | — | — |
| reading on the study bootstrap | undetermined | turn role | — |
| fragile, one study dropped | no | no | — |
| fragile, one domain dropped | no | no | — |
| ties (T = 0) | 1 | 1 | — |
| median T | +5.00 | +4.50 | — |
| 10% trimmed mean T | +5.34 | +5.08 | — |

| Haiku's two repeats | value |
|---|---|
| T, first repeat only | +4.85 |
| T, second repeat only | +5.67 |
| share of grades identical across repeats | 0.55 |
| SD of (second − first), points | 4.54 |

|  | Haiku | Opus | Sonnet | total |
|---|---|---|---|---|
| test run | $0.054 | $0.399 | $0.190 | **$0.642** |

- T = (clean − flawed) in the quoted copy − (clean − flawed) in the own reply, per study, each cell the mean of its repeats; F = own-reply flawed − quoted flawed. Penalties are clean − flawed, in points of 100.
- **The bars:** Haiku 6.3 (scored), Opus 3.0 (reported). **Verdict** (§5): Haiku reads undetermined → **mixed**. Score 0 against engine odds 0.55.

Raw data: `results/sg-b6-grade-calls.json` (committed `3164fff`, before this analysis). The analysis is `results/sg-b6-analysis.json`, regenerated by `python3 experiments/sg_b6_samerun.py analyse` with no calls. The tables above are printed by `sg_b6_samerun.tables()`.
