---
bet: om-p2-3
program: other-minds (program 2)
prereg_commit: 6f17538 (2026-11-04 15:07:51); seed commit 46378b0 (15:08:41)
results_commit: 5141ca7 (15:42); wording fix f46f8e3 (15:42:28)
auditor_session: audit2 lead auditor (branch audit2, entangled-mind)
auditor_model: claude-opus-5-5
author_model: claude-opus-5-5 (commit trailers)
same_model_family: true
date: 2026-11-04 15:45 America/Denver
claims_checked: 12
holes_found: 2
overclaims_cut: 2
reproduced: true
verdict_claimed: untestable
verdict_after_audit: untestable
verdict_stands: true
canary: unknown
false_alarms: 0
failed: true
failure_reason: the API refused the 22nd step-1 call (story gen8_sev3, explosives), and stop-on-refusal ended the run with 0 of the 300 required stories in the planted conditions
failure_kind: execution
premortem_score: named
risk_seen: null
---

# Audit of om-p2-3: SimpleToM decomposed (stopped on a refusal)

## In plain English

The verdict, **untestable**, stands. It is the pre-registered rule 3: fewer than 300 stories had both planted conditions answered, and the actual count was 0.

The run stopped correctly at the first refusal:
- 26 answers are archived, with 26 unique request IDs, all decoded to 15:40:39–15:40:41.
- That is after the seed commit, so after the pre-registration.
- Spend was $0.0010 of the $1.75 cap.
- Nothing was reworded or retried.

The beacon seed recomputes exactly from the archived pulse. The pulse is the first round after the pre-registration commit.

Two small points:
- Five of the 26 archived answers were sent after the refused request. They were calls already in flight in the 8-worker pool, and they were kept. "No new call started" is consistent with that but cannot be verified to the millisecond, and the file should say so.
- The design accepted a known, likely failure. 552 of 1,147 stories are severity 3 (bombs, poison), program 1 had already hit two refusals, and the pre-mortem itself named this exact mechanism. No refusal pilot was run before freezing. At $0.001 the cost is trivial; the lesson is for the next design.

## The case that this result is false

"Untestable" could be false in two ways.

**The run might have continued past the refusal.** Five cached answers come from stories after the refused one in run order (indices 22–26 against 21). Their request IDs are timestamped 29–556 ms after the refused request's. If those calls were *started* after the refusal was known, the stop rule ("no later call of the wave") was broken. The rule-faithful archive would then have 21 answers, and the write-up's "No new call started" would be false.

**The refusal might have been avoidable within the rules.** The prereg's item order interleaves severities by scenario, so a severity-3 story came third. A run ordered by severity, or one that pre-registered severity 1–2 first, would have produced a testable subset before reaching any severity-3 story. On that view "untestable" reflects an ordering choice, not the question.

## Claims checked

| # | claim (`results/p2-3-simpletom.md` at f46f8e3) | check | outcome |
|---|---|---|---|
| 1 | "Pre-registered … commit `6f17538`. Seed commit `46378b0` … Both came before any call." | request-ID decode (`audits/tools/ridtime.py`): 26 IDs, 15:40:39–15:40:41; prereg 15:07:51, seed 15:08:41 | holds |
| 2 | "Stopped on a refusal after 26 calls" | `p2-3-calls.json`: 26 entries, 26 unique IDs, all step 1 (`ms|`) | holds (the first version said "About 30"; corrected in f46f8e3) |
| 3 | "$0.001 of the $1.75 cap" | sum of cached costs | holds: $0.00101 |
| 4 | refused request `req_011Cgih9NjqNtezArQLWd12p`, category `general_harms` | `results/refusal-p2-3.md`; decodes to 15:40:41 | holds |
| 5 | the refused story is `gen8_sev3` | `data/p2-3-items.json` order: index 21 | holds |
| 6 | "No new call started" after the refusal | per-call ID times relative to the refused request: indices 22–26 at +29, +204, +216, +349, +556 ms | **cannot check exactly**: ID times mark receipt of each request, not the arrival of the refusal response. The pattern fits 5 calls already in flight in the 8-worker pool (`om_common.Caller.run`, `workers=8`; the stop event is set only when the refusal returns). The file should state that 5 in-flight calls completed and were kept |
| 7 | "nothing was reworded, retried, skipped or replaced" | cache keys: one per story; no key for gen8_sev3; no duplicate IDs | holds |
| 8 | "Stories with both planted conditions answered: 0 of 1,147 (rule: 300). **Verdict: untestable.**" | `6f17538` §5 rule 3 | holds |
| 9 | seed: CURBy-RNG pulse 1591352, `seed32_boot` 2809903762 | `ledger/seed.py <randomness> om-p2-3 --purpose boot` | holds: 17468122858864229010 / 2809903762 |
| 10 | pulse after the prereg commit, first such round | archived `data/p2-3-seed.json`: pulse 15:08:00.202, previous 15:07:00.190, commit 15:07:51 | holds on the archive; `certificate_verified: false`, and the chain itself is **not checkable** offline (no network allowed) |
| 11 | "The pre-mortem named this" | prereg §0 | holds (scored below) |
| 12 | "The interpersonal result (P2-4) already speaks to part of the same question." | P2-4 is a separate bet, unaudited when this was written | **overclaim (minor)**: an unaudited result is cited as a substitute |

## Checklist

**A.**
- **A1.** Holds (claims row 1).
- **A2.** Holds. The stop rule, cap and rule 3 are applied as written.
- **A3–A4.** Not applicable; no statistic was computed.

**B.** No statistic was computed (B5–B12 not applicable). The 26 step-1 answers are archived but carry no inference.

**C.**
- **C13–C16.** The plain English matches the table, except rows 6 and 12.
- **C17.** SimpleToM (Gu et al. 2024, ODC-BY licence): not opened offline (**cannot check**).
- **C18.** Negatives stated plainly: holds ("The test says nothing either way").

**D.**
- **D19.** Budget enforced in code (`Caller.run` checks `spent() >= cap` under a lock before each call). Holds.
- **D20.** Stop-on-refusal obeyed. Holds, with row 6's caveat.
- **D21.** Not reached.
- **D22.** Not applicable.

**E.**
- **E23 seed.** Holds on the archive (rows 9–10). Whether 1591352 is the first round on its chain after 15:07:51 rests on the archived `previous_index` and times, and the certificate is unverified. **Cannot check** live (network forbidden in this audit).
- **E24.** Not a tiebreak bet.

**Holes.**
1. **The record is silent on in-flight calls.** The stop rule says "no later call of the wave". Five later-wave calls completed and were archived, plausibly in flight. The write-up says "No new call started" without mentioning them.
2. **A foreseen execution failure was accepted without a pilot.** That cost a bet slot, not money. Because the pre-mortem named it, this is a design-review point, not a fault in the run.

**Process note.** The results file was edited one minute after the result commit (f46f8e3, "About 30" → "26"). That is a correction toward the archive, with no DEVIATIONS row. It is harmless, but the standard asks for corrections to be logged.

## The pre-mortem, scored

**Auditor's failure reason, and its order.** The refusal at the 22nd step-1 story (a severity-3 explosives story) ended the run before any planted condition (kind `execution`). Honesty about order: the results file quotes the pre-mortem in its plain-English section. So the auditor saw it before writing this line, and the blind-order rule could not be kept.

**Pre-mortem (prereg §0, `6f17538`):** "If this fails, the most likely reason is a refusal on one of the 552 severity-3 stories (bombs, poison, contaminated food), which stops the run before the planted conditions are complete for 300 stories." Kind: `execution`.

**Score: `named`.** The same mechanism occurred: a refusal on a severity-3 story stopped the run before 300 stories were complete.

## Required cuts

- `results/p2-3-simpletom.md` ("What the rules did"): "No new call started, and nothing was reworded, retried, skipped or replaced." → "No new call started after the refusal reached the runner. Five calls already in flight (stories 22–26 in run order) completed and are kept. Nothing was reworded, retried, skipped or replaced."
- `results/p2-3-simpletom.md` (last option): "The interpersonal result (P2-4) already speaks to part of the same question." → "P2-4 (separately pre-registered and audited) bears on a related question."

## What would break it next

Nothing can break "untestable"; it is a rule outcome. Two cheap steps for the question itself:
1. **About $0.01:** a refusal pilot, pre-registered, on 50 random severity-3 stories, step 1 only, to measure the refusal rate before any new design.
2. **About $1:** a new pre-registered bet on severity 1–2 only (595 stories), as the result file suggests. It is a different item set, so a new bet, with its own pre-mortem.
