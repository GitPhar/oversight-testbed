# Independent audit, round 3: summary

2026-11-05, 05:00–06:20 America/Denver. Auditor: claude-fable-5-1, a stronger model than the claude-opus-5-5 that did the work, the design reviews and audit rounds 1 and 2. That is the round's own experiment: does a stronger auditor change the verdicts? Scope: every scored bet in `ledger/bets.jsonl` at the start of the round (20) plus the one pass-unreplicated unscored result (ng-p3-5c): 21 bets, one file each in `ledger/audits/round-3/`. Standard: `operators/auditor.md`. Each bet was worked in a stripped clone at its results commit, its headline number re-derived from the archived data with code written for this round (scratch paths are named in each file), its pre-registered rule compared word for word with what was reported, and every claim in the current results file checked against the data. No paid API call, no hardware, no local model. Cuts were applied to the results files under one DEVIATIONS row per program (entangled-mind D60, other-minds D16, nature-graded D40, settled-science D49).

## In plain English

**Every headline number in the record reproduces.** Twenty-one headline statistics, re-derived with independent code, match the archive to the printed precision or better. The arithmetic of this project is sound, as rounds 1 and 2 also found.

**One verdict is reversed: ss-b6, pass → undetermined.** The bet asked whether round 2's bettor knows anything beyond "which version flatters the paper". Its pre-registered rule was met by a bound of −0.003. But in the null world matched to the data, where the bettor knows only what the flattery rater knows, that rule is passed about 53% of the time (round 2 had found 58% and left the label standing). A test that passes half the time when its hypothesis is false does not decide the bet. The ledger's own precedent, om-p2-4, is the same case: a rule met in letter with no power to tell its outcomes apart. ss-b6 is now unscored with both outcomes as sensitivity rows.

**One label changes without a score change: om-p2-5, null → mixed.** The map's event passed at five times its bar; the fail is a design-review conjunct that fires when the effect is larger, not smaller. The miss stays a miss (the odds were for the full rule).

**Nineteen stand, all with cuts** (two with none: om-p2-1, om-p2-3b, om-p2-6, om-p2-6r had no new wording to cut; the rest had one to five sentences). The cuts are the same families rounds 1 and 2 found: non-detections written as findings ("not privileged", "gives no advantage"), mechanism words, and subsets or robustness facts the files knew and did not say.

**A stronger auditor changed little at the level of verdicts and a lot at the level of what the verdicts mean.** The reversal rate is 1 of 21 (5%), against 0 of 39 in round 1 and 3 of 13 in round 2. What the stronger model added was not new arithmetic but inference: which passes could not have failed, which misses could not have passed, and how the ledger counts them. That is where the three biggest holes are.

## Verdicts

| bet | program | round 1 | round 2 | round 3 | after audit | outcome | cuts | most serious finding |
|---|---|---|---|---|---|---|---|---|
| em-gm1 | 1 | stands w/ caveats | — | stands with cuts | null | 0 | 4 | all-298 interval excludes 0 narrowly (28 of 298 single drops put it at or above 0); sign is mostly the 26 disagreement items; paper's "not privileged" headings cut |
| em-gm2 | 1 | stands w/ caveats | mixed (dm4) | stands with cuts | pass | 1 | 5 | "redaction gives a larger effect" not established (8.0 [−0.8, +17.7]); R 1.91 [0.93, 4.70] holds under every seed, drop and correction |
| em-gm3b | 1 | stands | pass-unrep. (Opus) | stands with cuts | pass | 1 | 2 | round 2's one-bit artefact does not transfer to Haiku (graded one-credence model wins by 12.6 per claim); by-format table from an under-converged fit |
| em-gm4 | 1 | stands | — | stands with cuts | mixed | 0 | 1 | EIG's above-chance rate is entirely overlap with the confirmatory target; at chance on disjoint menus |
| em-gm5 | 1 | stands w/ caveats | untestable → mixed (DP2) | stands with cuts | mixed | 0 | 4 | the ledger scores DP2, whose data exist only on the unmerged `probes` branch; the main file still said "queued" |
| om-p2-1 | 2 | — | stands | stands | null | 0 | 0 | none left; bar 0.90 below the same-wording retest ceiling 0.955 |
| om-p2-2 | 2 | — | stands | stands with cuts | null | 0 | 1 | "even on the lenient test" overstated; the pooled test was not lenient |
| om-p2-3b | 2 | — | stands | stands | null | 0 | 0 | none; the strongest miss of the six |
| om-p2-5 | 2 | — | stands | stands with cuts, **label null → mixed** | mixed | 0 | 1 | map event passed at 5× the bar; the fail is conjunct 5b, which fires on more effect |
| om-p2-6 | 2 | — | stands | stands | null | 0 | 0 | none; position is a disclosed bundle |
| om-p2-6r | 2 | — | stands | stands | null | 0 | 0 | none new; round 2's P13 float-boundary cut verified |
| ng-p3-1 | 3 | — | stands | stands with cuts | null | 0 | 3 | the pass bar sat 94 SE away and could not be met on this circuit; the D8 re-run was never audited |
| ng-p3-5 | 3 | — | stands | stands with cuts | null | 0 | 2 | the map row had already ruled the event out before 42% was staked; ρ_ref not archived |
| ng-p3-15 | 3 | — | stands | stands with cuts | null | 0 | 2 | real forecast, informative miss; the one replicated signal (chip above prediction, 8/8 arms) had nothing pre-registered |
| ng-p3-5c | 3 | — | stands | stands with cuts | pass-unrep. | — | 3 | on h088 the bootstrap null comes from a model the counts reject (deviance 63 on 11 df) |
| ss-b1 | 4 | — | stands | stands with cuts | pass-unrep. | 1 | 1 | one run scored three times in the ledger |
| ss-b2 | 4 | — | stands | stands with cuts | pass-unrep. | 1 | 1 | robust to the writers' selection (break-even 88% headline-right); same run as ss-b1 |
| ss-b3 | 4 | — | stands (one field) | stands with cuts | pass-unrep. | 1 | 1 | field-cluster interval includes 0 (−0.156, +0.038); recognised items carry the gap (0.024 vs 0.129) |
| ss-b5 | 4 | — | stands | stands with cuts | pass-unrep. | 1 | 1 | a sentence-reading task; margin on 21 down-word items, 9 removals flip |
| ss-b6 | 4 | — | stands (fragile) | **reversed** | undetermined | — (was 1) | 4 | the rule passes 53% of the time in the null world matched to the data |
| ss-b7 | 4 | — | stands (easy) | stands with cuts | pass-unrep. | 1 | 1 | a coin rater passes both legs; shuffled ratings give the same leg 2 |

Reversal rate: round 1, 0 of 39 (2 undetermined); round 2, 3 of 13 (23%); round 3, 1 of 21 (5%), plus one label change with no score change. The stronger auditor reversed less than round 2 did, because round 2 had already taken the arithmetic holes; what was left to reverse was inference, and only ss-b6 crossed the ledger's own line for it.

## Brier before and after

| state | scored bets | hits | engine Brier |
|---|---|---|---|
| at the start of round 3 (committed ledger, 2b90988) | 20 | 8 | 0.249 |
| after ss-b6 → undetermined (this round's only score change) | 19 | 7 | 0.240 |
| ledger as it stands after this round, including two misses other sessions scored meanwhile (ng-p3-16 at 0.05, sg-b1 at 0.24) | 21 | 7 | 0.220 |

Sensitivity (round-3 computation, `scratchpad/p4/rederive.py`): ss-b6 counted as a miss, 0.234 on 20; one bet per program-4 run (ss-b1 and ss-b5 only), 0.205 on 16; without program 4 at all, 0.177 on 14 with 2 hits.

## The three most serious holes in the whole record

1. **Six of the engine's eight hits were two runs of one model, and the ledger scored them as six bets.** ss-b1, ss-b2 and ss-b3 are one bettor run on one item set against three bars. ss-b5, ss-b6 and ss-b7 are one set of 92 bettor ratings against three comparators, and the two comparator bets (ss-b6, ss-b7) test the rater prompts, not the bettor: ss-b7 is passed by a coin rater, and shuffling the striking rater's ratings leaves its leg 2 unchanged. Round 2 found "the test was easy" and left the hit in place. The engine's headline, "0.249, about a coin", rests on this; without program 4 the record is 0.177 on 14 bets with 2 hits, and with one bet per run it is 0.205. The fix is a ledger rule, not a cut: secondary bets on one run should share one row's weight or be labelled as a cluster in brier.md.

2. **Rules met in letter by tests that could not decide them, in both directions.** ss-b6 (reversed) passed at a 53% false-pass rate. ng-p3-1's pass bar sat 94 standard errors from anything this circuit could produce, and ng-p3-5's event had been ruled out by the map row before the 42% was staked; both are scored as misses at 0.0049 and 0.1764, which is calibration the design bought, not the world. em-gm5's priced event (the probe holds within its noise) was nearly unreachable by construction. The pattern (round 1's "nulls written as findings", round 2's "non-detection rules called passes", now "rules that cannot fail or cannot pass") is logged as P12 but is still reaching the ledger: design-review check D11 ("both outcomes possible") was added on 2026-11-04 and did not catch ss-b6, because the review simulated the null world at the wrong noise.

3. **The record is not fully reproducible from this repository, and the shared checkout keeps corrupting it.** em-gm5 is scored on DP2, whose pre-registration, data and results exist only on the unmerged `probes` branch of the old entangled-mind checkout; `git log --all` here has no such commit, and the main results file said "queued" until this round. ng-p3-5's fitted-family log-likelihoods cannot be recomputed because ρ_ref is not archived. ng-p3-1's D8 re-run was never audited and the "corrected simulator" hold was never formally lifted. And during this round the ss-b6 ledger edit was overwritten once by another session's write of `bets.jsonl` and nearly swept into another session's path commit; a scored row briefly lacked a field and crashed `brier.py` for every session. Several sessions writing one index is the record's weakest link, as CONTEXT.md §2 already says.

## What the stronger auditor added, and did not

- Added: the null-world false-pass rate for ss-b6 with independent code (53%), the reweighting that clears ss-b2 of the selection worry, the field-cluster interval on ss-b3, the coin-rater and shuffle checks on ss-b7, the one-bit test that clears Haiku's gm3b, the 28-of-298 fragility of gm1's sign, the per-subset decomposition of gm2's effect, the retest-ceiling-versus-bar check on all six program-2 misses (none was a cheap miss), the could-it-have-passed check on program 3 (two of three misses could not), and the h088 misfit in ng-p3-5c.
- Did not add: any arithmetic error. Rounds 1 and 2, by the weaker model, had found all of those.
- The same-family caveat is weaker this round (different model, same vendor) and not gone. No non-Anthropic auditor has read any of this record.

## What the owning sessions should do first

1. Ledger: decide how secondary bets on one run count (hole 1); until then, brier.md should say that 6 of 8 hits are two runs.
2. Program 1: merge or archive the `probes` branch so DP2 is in this repository; otherwise re-score em-gm5 on DP1.
3. Program 3: audit the D8 re-run and lift or keep the hold with a row; archive ρ_ref.
4. Design review D11: simulate the null world at the disagreement the data would show, not at call noise, before any comparator bet.
5. Program 4: the flattery rival is open again; the next test needs a rater with less stable disagreement from the bettor (averaged prompts, about $0.91) or a different-family rater.

## How this round was done, and its limits

- Four forks of this session (same model, full context) audited programs 1 (two forks), 2 and 3; the main session audited program 4 and wrote this summary. Each fork re-derived its headlines with its own code under `python3 -I` in a stripped clone at the results commit.
- The main session re-verified: all six program-4 headlines, the ss-b6 null world (53% against round 2's 58% and the design review's 8% at call noise), the ss-b7 coin rater, and the Brier figures above.
- Not recomputed: the beacon pulses (rounds 1–2 re-fetched them), the probe projections (no local model), any simulator that needs a backend. em-gm5's DP2 could not be reproduced from this checkout at all.
- Cost: $0 in API calls, 0 QPU s.
