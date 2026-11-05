---
bet: probe-dissociation DP2 (step 3 on fresh seeds)
program: entangled-mind (gold map direction 5), branch probes
prereg_commit: d7de8a2 (2026-11-04 14:34:35)
results_commit: 3fa5832 (14:59:06)
auditor_session: audit2 lead auditor (branch audit2)
auditor_model: claude-opus-5-5
author_model: claude-opus-5-5 (commit trailers)
same_model_family: true
date: 2026-11-04 15:25 America/Denver
claims_checked: 18
holes_found: 2
overclaims_cut: 3
reproduced: true
verdict_claimed: mixed
verdict_after_audit: mixed
verdict_stands: true
canary: unknown
false_alarms: 0
failed: true
failure_reason: with three gate items, "not with the rating" is set by one non-tracking item (h191), and fresh seeds cannot test the near-deterministic probe side
failure_kind: design
premortem_score: null        # pre-registration predates operators/premortem.md (e287cb3, 14:41); it has no pre-mortem
risk_seen: null
---

# Audit of DP2: the probe study's step 3 on fresh seeds

`verdict_claimed: mixed` stands for the frozen reading **DP1 VERIFIED**. The label underneath is PROBE MOVES, BUT NOT WITH THE RATING: a positive half and an undetermined half.

## In plain English

DP2 does what it set out to do, and its write-up says almost exactly what the data show. Every number checked reproduces:
- The authors' `analyse` on a clean copy of `3fa5832` regenerates `results/probe-dissociation-run-2.json` byte for byte.
- My own code reproduces the replay share (22 of 500 sequences, 4.4%; M alone 156 of 500, 31.2%).
- It reproduces the gate items' rating order means and per-item r (+0.86, +0.98, −0.16).
- It reproduces the probe's correlation with DP1 (at least 0.994 on every item), and confirms that the no-chain and told-cue probe readings are identical to DP1's.
- It reproduces the descriptive noise comparison (median within-order SD 12.1 against 13.0; lower in 26 of 40 cells).

The run started 4 s after its freeze, while this auditor was watching the process table.

So the replay hole found in round 1 is closed **on the rating side**. The rating's order effect replicates on independent samples, and the frozen rule returns DP1's label.

What "verified" verifies is narrow, and the file says so:
- The probe side is near-deterministic and not independently tested.
- "Not with the rating" is again set by h191.
- With three gate items, the rule could return "not with" from a single non-tracking item. A replication of this label is therefore weak evidence that probe and rating are independent.

Three sentences go slightly further than the data:
1. The non-gate r is called "the strongest evidence so far", but its interval reaches +0.06.
2. "7 of 10 items" leads, where under Holm it is 5.
3. The DP1 file on main still says "unverified … queued". That needs updating when `probes` merges.

## The case that this result is false

"DP1 VERIFIED" means the frozen label recurred. But the label's two halves were never in much doubt from the seed change alone.

**"Probe moves" is close to a replay.** The probe reading depends on the fixed question sequence and readout sentence, not on the sampled sub-ratings: its order means correlate with DP1's at 0.994–1.000, and its B0 and told-cue readings are identical to DP1's. So fresh seeds could not have overturned it. p_P = 0.0001 again is the same measurement taken twice.

**"Not with the rating" is near-guaranteed by the design.** With three items resampled from ten, r's interval spans roughly the range of the per-item r's. Any one non-tracking item puts the lower bound below 0. h191 did that twice. The informative quantities point the other way:
- items fixed, r = [+0.18, +0.52];
- without h191, r = +0.82 [+0.67, +0.99], BELIEF MOVES;
- layers 11 and 15 read BELIEF MOVES.

On this reading, the replicated label could reflect h191's peculiarity, not a dissociation. The only new evidence for "not with" is the seven non-gate items: r = −0.23 [−0.55, +0.06], a secondary whose interval includes 0. And half the cross-item variation there is on items whose rating effects pass only uncorrected.

**What the checks found.** All of this is true, and **all of it is in the results file**: "Limits", "What is still not settled", sections D–G. The case does not make the reported reading false. It makes "DP1 VERIFIED" a statement that the label replicated, which is how the file uses it. The remaining overreach is three sentences.

## Claims checked

| # | claim (`results/probe-dissociation-run-2.md` on `3fa5832`) | check | outcome |
|---|---|---|---|
| 1 | frozen in `d7de8a2` before any fresh conversation | commit 14:34:35; runner process start 14:34:39 (`ps -o lstart`, observed live); run file created 14:36:30 | holds |
| 2 | 0 of 700 seeds shared | `seed_for` namespaces | holds (by construction; `seedcheck` output not archived) |
| 3 | replay share 4.4% (22 of 500), M alone 31.2% | own code | holds: 22/500; M 156/500 |
| 4 | chance rate 3.8% (M 29.6%) | prereg §4 | taken as stated (computed before the freeze; not recomputed) |
| 5 | 12 DP1 conversations regenerated identically | DEVIATIONS DP2 note | cannot check (needs the local model) |
| 6 | Q 2.82 [1.40, 5.35], r +0.36 [−0.20, +0.98], p_V = p_P = 0.0001 | authors' `analyse` on a clean copy | holds (JSON byte-identical) |
| 7 | reading DP1 VERIFIED | §4 precedence: V4 passes, label equals DP1's | holds |
| 8 | gate items' order means and per-item r +0.86, +0.98, −0.16 | own code | holds |
| 9 | fresh gate 7 of 10 uncorrected, 5 under Holm | authors' output | holds |
| 10 | Q_sep 0.44 [0.23, 0.83], Q_b0 0.49 [−0.01, 2.53] | JSON | holds |
| 11 | r without h191 +0.82 [+0.67, +0.99]; items-fixed [+0.18, +0.52] | JSON | holds |
| 12 | layer 15 r +0.43 [+0.002, +0.82] → BELIEF MOVES | JSON | holds; the file rightly calls it "a coin's edge" |
| 13 | probe order means correlate with DP1 at ≥ 0.994 | own code | holds: min 0.9943 |
| 14 | B0 and told-cue probe readings identical to DP1 | own code | holds |
| 15 | median within-order SD 12.1 vs 13.0, lower in 26/40 | own code | holds; the Mann–Whitney "1 of 40" is not recomputed |
| 16 | "The winner's curse the audit expected did not appear" | spans 30.7/23.4/38.4 vs 29.5/20.0/24.7 | holds |
| 17 | "This is the strongest evidence so far for 'not with the rating' outside two items" | non-gate r −0.23 [−0.55, +0.06] | **overclaim (minor)**: a secondary interval including 0 |
| 18 | "21 minutes" | 14:34:39 → last write before 14:59 | consistent |

## Checklist

**A.** A1: holds (claims row 1). A2: holds; DP1's `compute()` and rule are imported unchanged, and the output rename is disclosed. A3 and A4: hold. The analysis was checked on DP1's archive before freezing, which looked only at DP1's already-public data.

**B.**
- **B5 ties.** Not material; permutation p at its floor (0.0001) for both p_V and p_P.
- **B6 pooling.** Primary on G only, as frozen; all-10 and non-gate are secondaries.
- **B7 few items.** **Hole, carried over and disclosed.** h191 decides "not with" on both draws (claims row 11). Stated in the file.
- **B8 circularity.** Closed on the rating side by the fresh seeds. The gate items were still *chosen* on DP1's gate data, but the effect was re-measured on new samples.
- **B9 units.** Disclosed (row 10).
- **B10 uncertainty.** Item bootstrap as frozen.
- **B11 multiple comparisons.** Seven secondaries, uncorrected, presented as secondaries. The "7 of 10" headline puts the uncorrected count first (cut 2).
- **B12 leakage.** Not applicable.

**C.**
- **C13 scope.** Holds ("Nothing here bears on Claude's internals").
- **C14 rank drift.** One sentence (row 17).
- **C15 mechanism.** "The probe's order effect is a property of the question sequence" is supported by rows 13–14 as stated, since only the samples changed. It could also be a property of the fixed readout sentence, which the file names under Limits. Holds.
- **C16 plain English vs tables.** Holds, apart from cuts 1–2.
- **C17 citations.** None new.
- **C18 negatives stated plainly.** Holds ("It does not mean the two were shown to be independent").

**D.**
- **D19 budget.** $0 API, local. Holds.
- **D20 refusals.** Not applicable.
- **D21 one scale direction.** Holds.
- **D22 replication.** The rating half replicated on independent samples. The probe half is the same measurement twice. "Pass, unreplicated" applies to the probe half until a reworded readout or new sub-question wording is run.

**Hole (process, minor).** The DP2 DEVIATIONS row is dated "2026-11-04 (America/Denver)" with no time. The commit time (14:34:35) is the only timestamp.

## The pre-mortem, scored

The pre-registration has no pre-mortem: it was frozen before `operators/premortem.md` entered the standard (`e287cb3`, 14:41). So `premortem_score: null`. The auditor's own one-line failure account is in the front matter (`failure_reason`, `failure_kind`).

**E23–E24.** Not applicable: no beacon seed, and not a tiebreak bet.

## Required cuts

1. `results/probe-dissociation-run-2.md`, "What this changes", third bullet: "This is the strongest evidence so far for \"not with the rating\" outside two items. It is secondary, and its interval reaches +0.06." → "Its point estimate is negative, but the interval includes 0 (it reaches +0.06), so tracking on these items is not detected rather than ruled out. It is secondary."
2. `results/probe-dissociation-run-2.md`, plain English, first bullet of "What holds up": "7 of 10 items show an order effect (5 under Holm)" → "5 of 10 items show an order effect under Holm (7 uncorrected)".
3. On merging `probes`: `results/probe-dissociation.md` banner, `README.md:31`, `paper/morning-brief.md:122` and `paper/gold-map.md:270`. "Unverified (D53) … a fresh step 3 … is queued" → "Verified on fresh ratings by DP2 (`3fa5832`): the label replicates; the probe side is a near-replay by construction, and \"not with the rating\" is again set by one item (h191)."

## What would break it next

**$0, local.** Reword the readout sentence and the four sub-question prompts (one fixed paraphrase each, written before any run) and re-run the gate items plus h261 and h058, which pass Holm on fresh data. That makes five items, so r is no longer set by one item of three. The probe half becomes testable: if the probe's order pattern survives a paraphrase, it is about content; if not, it was about the fixed text.
