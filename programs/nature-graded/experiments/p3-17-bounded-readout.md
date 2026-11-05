# P3-17: is P3-5c's blur-type term still needed when readout error may be up to three times each job's calibration value? (pre-registration)

Written and frozen 2026-11-05 (America/Denver; the commit's author time is the record), in its own commit, before any archived tomography count is opened by this bet. DEVIATIONS.md D41. Budget **$0 · 0 QPU s · ≤ 3 laptop hours**; no network, no model, no chip. Stop rules in §7.

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). This session never asks Sean for odds or for a decision, in a terminal, a chat or a question dialog. His odds come only from `ledger/human-odds.jsonl` (the cockpit's downloads, committed); if a direction has no line there when its bet is pre-registered, the bet proceeds marked "no human odds". A decision this session would otherwise ask about, it makes under the written rules and states in its report and commit, where Sean can veto it from the cockpit.

> **Cockpit first, then this file.** P3-17's card is in `map/cockpit-cards.jsonl` (remap 2026-11-05, `a394a25` and before). `ledger/human-odds.jsonl` was read immediately before this commit, after `python3 ledger/pickup_human_odds.py` (`9a75cc2`, 06:16): it holds Sean's line for P3-17.

## 0. The bet

| field | value |
|---|---|
| bet id | `ng-p3-17` |
| referee | `nature` (the chip's archived counts decide it; no model in the loop) |
| bet type | `standard` |
| direction | `P3-17` (`programs/nature-graded/map/program-3-map.json`, remap 2026-11-05) |
| source | `literature` (audit ng-p3-5c, round 2, "What would break it next"; round 3 the same) |
| engine odds, P(pass) | **60** after the lesson. Map (remap one pass, 2026-11-05 04:45): 70. v1 re-elicitation in a fresh context that saw only the direction's row and this file's pass rule (2026-11-05 about 06:30, before this commit): 72. |
| human odds, P(pass) | **30**, `ho-20261105-061152-9fe` (cockpit, saved 2026-11-05 06:11:52; committed `9a75cc2`). His card's event says "readout knobs bounded at 3x each job's calibration error"; this file's event (§5) reads that as readout *error* up to 3× the calibration value, and reports his card's other reading (each knob up to ±3× the value) as a secondary (D41). |
| odds disclosure | The session that set the after-lesson odds (60) had read Sean's line (30) before doing so; the v1 number (72) came from a fresh context that never saw it. Both are kept. |
| models | not all three, because no model is in the loop: an archive of chip counts is refitted (rule 12 does not apply). |
| budget | $0 API · 0 QPU s · ≤ 3 laptop hours (11 worker processes) |
| lesson | Correcting P5, P12: P3-5c's blur term never had to beat readout drift, its matched rival on tomography counts. This bet gives each model four readout knobs (error up to 3x each job's calibration value) and checks pre-run worlds that pass and fail; its odds are 60% (from 70% on the map) because these bounds are looser than the map's. |
| design review | before the run, a fresh subagent dry-runs this design (`operators/design-review.md`) → `ledger/design-reviews/ng-p3-17.md`; `--run` refuses without go (or a confirmed fix-first). |
| pre-mortem | If this fails, the most likely reason is that on h221 or h268 the knobs hit their upper bounds and absorb enough blur to push LR below its null's 99th percentile. Kind: `world`. |
| auditor | fresh session per `operators/auditor.md`, after results, with a sealed plant draw first (`operators/plant.md`) |

**Read before betting (operators/learn.md).** `ledger/bets.jsonl`, `ledger/brier.md`, `ledger/audits/` and `ledger/lessons.jsonl` at `9a75cc2`: 24 scored bets, 8 hits, Brier 0.223, running base rate (8 + 1)/(24 + 2) = 0.35; nature-graded 0 hits in 4 scored; newest audit file `ledger/audits/sv-b3.md` (author's reply, `20ad07e`); for this direction `ledger/audits/ng-p3-5c.md` and `ledger/audits/round-3/ng-p3-5c.md`. Patterns: P5 (unmatched rivals: the readout rival was never in P3-5c's model) and P12 (a bet must be able to pass and fail: `--recovery` builds one world of each kind before the run). P1 moves the odds toward the base rate: 70 → 60.

## 1. In plain English

P3-5c refitted program 1's saved chip data (three entangled qubit pairs, one job, 3 November) and found that a model of the chip's errors needs a "blur-type" part on every pair. Its auditor noticed a rival: if the chip misread its own results a little more often than its calibration said, that extra misreading would look like blur in these counts. With misreading allowed up to 5%, the blur part was no longer needed on two of the three pairs, but the misreading needed was several times what IBM reports. This test asks the fair version of that question: if each qubit is allowed to misread anywhere from not at all up to **three times** as often as the same job's own calibration measured, is the blur part still needed on all three pairs? If yes, readout drift of a believable size cannot stand in for it. If no, the archive cannot tell blur from misreading on those pairs, and P3-5c's "blur on every pair" does not stand on the archive alone. Either way, these are terms in a fitted model, not identified physical mechanisms.

## 2. Material

- **Archive.** `programs/entangled-mind/results/witness-run-1.json`, job `dbl6e1d8mdtc73d5gesg` (ibm_fez, 2026-11-03): per pair, `hardware_counts[0:9]` (the nine tomography settings, 4,000 shots each, read only by `--run` after every gate) and `hardware.assignment_matrix` (the in-job readout calibration, 4,000 shots per prepared basis state). Archived circuits in `programs/entangled-mind/window/data/hardware/` (reference states only).
- **Reference state ρ_ref.** P3-5c's (`p3_5c_fits.reference_state`, T1/T2 loaded and asserted, D8 fix), unchanged.
- **Models.** P3-5c's primary set (D19): coh (7 knobs), inc9 (9), full16 (16), each with four readout knobs added (cohR 11, inc9R 13, full16R 20). Readout knob per measured qubit q and prepared value b: A′ = (R_j ⊗ R_i) A with R_q = [[1 − e0_q, e1_q], [e0_q, 1 − e1_q]].
- **Bounds (primary).** r_q,b = qubit q's misread rate for prepared value b in the job's calibration, from A (the mean of the two calibration columns with that prepared value; 8,000 shots). e ∈ [−r, +2r], so the readout error ranges from about 0 to about 3r. The bounds are computed by the code from A; this session has not computed them for the archive.
- **Secondary bounds (point fits, reported, never a test):** "knob" |e| ≤ 3r (the card's other reading); "3 SE" |e| ≤ 3 × the binomial SE of r (the remap's draft test text); "wide" e ∈ [−0.02, 0.05] (audit round 2).
- **Code.** `experiments/p3_17_bounded.py` (this commit). `--check` (synthetic only) printed: knobs at their upper bound move a 1%/2% calibration rate to 2.9%/5.9% and at their lower bound to 0.03%/0.06%; the cohR fit recovers synthetic readout-only knobs (0.018, 0.040, 0.019, 0.040 for true 0.02, 0.04, 0.02, 0.04); `verdict()` returns exactly one verdict on each synthetic table.
- **Disclosed, not blind.** The archive was analysed by P3-5 and P3-5c and by their auditors; round 2's auditor ran a wide-bound readout refit (blur LR 8.9 on h221, 7.6 on h268, 38.9 on h088). This session has also seen, before this commit, the calibration rates for h221 and part of h088 in another session's **uncommitted** file `data/p3-17-bounds.json` (and its uncommitted `experiments/p3_17_readout.py`, a different, unscored design with 3-SE bounds). Neither file is used, changed or committed by this bet. This session has opened no tomography counts. The bet is scored, as the map planned, with all of this stated before data; the odds above include it.
- **Seed** (`operators/hardware.md`). CURBY-Q latest completed round 28297, result pulse 2025-08-22 13:42 America/Denver (checked 2026-11-05 06:23): stalled. Seed: the first CURBy-RNG pulse timestamped after this commit; seed = the first 8 bytes of SHA-256(randomness ‖ ng-p3-17), unsigned big-endian; sub-seed by `ledger/seed.py --purpose boot` (bootstrap SeedSequence and fit starts). The `--recovery` worlds use the fixed root seed 20261105 (synthetic only). *Filled in by the seed commit, before any data:* `chain:` ___ · `pulse index:` ___ · `pulse_time:` ___ · `randomness:` ___ · `client:` ___ · `certificate_verified:` ___ · `seed:` ___
- **Scale:** no graded scale (no model).

## 3. Calls

| step | what | calls | est. cost |
|---|---|---|---|
| 1 | `--recovery`: two worlds per pair (below), synthetic counts only | none | about 15 min laptop |
| 2 | design review (fresh subagent) | none | $0 |
| 3 | `--run`: per pair, cohR / inc9R / full16R point fits (11 starts each plus warm starts), bootstrap of LR_b (B = 100, extended to 1,000 if p ≤ 0.05), secondaries | none | about 45 min laptop |

`--run` refuses unless: the seed file exists; the design review says go (or fix-first confirmed); every file it reads or executes (`USES` in the code: the code, the seed, P3-5c's results JSON, the archive, this file, the review, `check_prereg.py`) is committed and unchanged; `ledger/check_prereg.py ng-p3-17 … --before-run` passes; and no results file exists. The run is never repeated.

**Pre-run worlds (`--recovery`, P12 / D11).** Per pair, 8 synthetic draws of 4,000 shots × 9 settings each:
- **W_blur:** truth = P3-5c's published fitted full16 state through the archived A (blur really there, readout as calibrated). Should come out "still needed".
- **W_readout:** truth = P3-5c's published fitted coh state (no blur) through A′ at the primary knobs' upper bound (readout error at 3× the calibration value). Should come out "not needed".

Each draw's LR_b is classified against the 99th percentile of one B = 100 null fitted on that world's first draw. P(pass | W_blur) and P(fail | W_readout) are reported (products over pairs). If P(pass | W_blur) < 0.10 or P(fail | W_readout) < 0.10, the design cannot both pass and fail at this n; the design review then decides (redesign or fix), before any run.

## 4. Statistics

- **Primary statistic**, per pair: LR_b = 2 (logL_full16R − logL_cohR). Null: parametric bootstrap from the fitted cohR (its state and its readout knobs), 4,000 shots × 9 settings per draw, each draw refitted with cohR and full16R (2 random starts plus warm starts from the observed optima). B = 100, extended to 1,000 if p ≤ 0.05. p = (1 + #{null ≥ LR_b})/(B + 1). Blur "still needed" on a pair iff p < 0.01 (strictly; at B = 100 the floor is 0.0099). Unit of analysis: the pair; nothing is pooled across pairs.
- **Split:** none; the archive is the whole data set.
- **Dumb baselines** (P3), scored beside the engine's and Sean's odds in the result: (a) *carry-over*, "readout knobs change nothing, so P3-5c's blur on 3 of 3 stands": P(pass) = 0.95; (b) the running base rate, 0.35. In the design, the dumbest world that must not pass is W_readout (readout drift within the bounds and no blur), checked by `--recovery`.
- **Secondary statistics** (reported, never promoted): the point LR for rotation given blur and readout, 2 (logL_full16R − logL_inc9R); LR_b scaled by the full16R overdispersion max(1, deviance/7) against the same null's 99th percentile (round 3's misfit point); goodness of fit (deviance on 27 − 20 = 7 df); the fitted knob values and which sit at a bound; the per-setting shares of LR_b and the top setting; point LR_b under the three secondary bounds, compared with the primary null's 99th percentile (not tests); P3-5c's LR beside each.
- **Multiple comparisons:** three primary tests, one per pair; the rule needs all three, so no correction is applied (a correction would make "still needed" harder and the pass easier to miss, not easier to get). Reported against α = 0.01 and against Bonferroni 0.0033.
- **Robustness committed now (P10):** the rule is an all-three rule, so one pair decides a fail; the result names the pair or pairs that did, with their p, LR_b and null 99th percentile. The top-setting share of each LR_b is reported; if one setting carries more than half of a "still needed" LR_b, the sentence for that pair adds "This rests mostly on setting <S>."

## 5. Pre-registered reading

The rule (`verdict()` in the code), on the per-pair p's:

1. **Pass:** blur still needed (p < 0.01) on all three pairs.
2. **Fail:** on at least one pair, p ≥ 0.01.
3. **Untestable:** any pair's fits do not return a finite log-likelihood, or its bootstrap does not complete B = 100 (or 1,000) draws.

Sentences, used verbatim (`verdict()`):
- Per pair, still needed: "On pair <P>, the blur-type term is still needed even when each qubit's readout error may be up to three times its calibration value in that job: extra readout error that large cannot stand in for it."
- Per pair, not needed: "On pair <P>, the blur-type term is no longer needed once each qubit's readout error may be up to three times its calibration value in that job: readout error that large can stand in for it, so on this pair the archive cannot tell blur from misreading."
- Pass: "Overall: on all three archived pairs (one job, 3 November), P3-5c's blur-type term survives readout error up to three times the job's own calibration value. These are terms in a fitted model, not identified physical mechanisms, and readout drift larger than three times the calibration value is not excluded."
- Fail: "Overall: on <n> of 3 archived pairs (<pairs>), readout error within three times the job's calibration value can stand in for P3-5c's blur-type term, so P3-5c's 'blur on every pair' does not stand on the archive alone. This does not show the chip was misreading; it shows the archive cannot tell the two apart on those pairs."
- Untestable: "The refit could not be completed on <pairs>, so this test cannot say whether readout error within three times the calibration value can stand in for the blur-type term."

Reported in every case: per pair LR_b, p, B, null 99th percentile and maximum; the bounds and fitted knobs; the secondaries in §4; the two dumb baselines; P3-5c's blur LR beside each. A pass is reported as **pass, unreplicated** (one job, one archive; P3-18 is the fresh-job test).

## 6. What it cannot do

It cannot say the chip's errors *are* blur or *are* misreading: both are terms in a fitted model. It treats the calibration matrix's shape as known up to these four knobs (correlated readout errors and readout drift during the job are outside them). It does not exclude readout drift larger than 3× the calibration value. h088's full model already misfits on this archive (deviance 63.3 on 11 df in P3-5c), so its nulls are drawn from a model the counts may reject; the overdispersion-scaled secondary says how much that matters. It is one job on one afternoon; "every pair" or "the chip" will not appear in the write-up.

## 7. Stop rules

- No network, no model, no chip: the code makes no call. Budget $0 by construction; laptop time is not capped in code (≤ 3 h stated).
- `--run` refuses on any gate in §3 and runs once.
- If the bootstrap or a fit raises, the run stops; the result is untestable on that pair by §5.3, and nothing is re-run without a DEVIATIONS row written before the re-run.

## 8. Ledger entry (filled now, completed after audit)

```json
{"id": "ng-p3-17", "program": "nature-graded", "direction": "P3-17",
 "title": "Is P3-5c's blur-type term still needed when readout error may be up to 3x each job's calibration value?",
 "source": "literature", "engine_odds": 0.60, "engine_odds_first": 0.70, "engine_odds_v1": 0.72,
 "human_odds": 0.30, "human_odds_at": "ho-20261105-061152-9fe",
 "prereg_commit": "<this commit>", "budget_usd": 0, "qpu_s_budget": 0,
 "referee": "nature", "bet_type": "standard", "seed_source": "curby-rng", "beacon": null, "seed": null, "tiebreak": null,
 "lesson": "ls-ng-p3-17", "design_review": {"path": "ledger/design-reviews/ng-p3-17.md", "verdict": null},
 "premortem_kind": "world", "verdict": "open", "date": "2026-11-05"}
```

## 9. Checklist before the run

- [x] This file is committed on its own; no archived tomography count has been opened by this bet.
- [x] Lesson row filled after reading the ledger at `9a75cc2`; the same sentence goes to `ledger/lessons.jsonl` as `ls-ng-p3-17`.
- [ ] Design review go (or fix-first confirmed); `python3 ledger/check_prereg.py ng-p3-17 . programs/nature-graded/experiments/p3-17-bounded-readout.md --before-run` passes (the code runs it).
- [x] Cockpit card exists; `ledger/human-odds.jsonl` read immediately before this commit; `human_odds_match.py nature-graded P3-17` printed 0.3, `ho-20261105-061152-9fe`.
- [x] Pass rule applicable by a stranger (`verdict()`; checked on synthetic tables).
- [x] Pre-mortem one sentence, checkable, with its kind.
- [x] CURBY-Q stalled; seed commit follows this one before any data.
- [x] No spend possible; refusals n/a (no model).
- [x] DEVIATIONS.md D41.
