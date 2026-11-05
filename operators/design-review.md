# Design review: a fresh auditor dry-runs every pre-registration before its first call (mandatory)

After a pre-registration is committed and before its first API call, chip submission or archive read, a **fresh auditor session** tries to break the *design*. It reads the frozen pre-registration and the code, and dry-runs the code without paid calls. It ends with one verdict: **go**, **fix first** or **redesign**. No call runs before a **go**. This file is the whole procedure. It follows ARCHITECTURE.md (the `DesignReview` object, step 3b of the loop, invariant 10) and is enforced by `operators/prereg-template.md` §0, `operators/auditor.md` E26 and `ledger/check_prereg.py`.

## In plain English

The audit after a result asks "is this true?". By then the money is spent and the chance is gone. Two of today's misses were broken before they ran, in ways a careful reader of the code could have caught for free:
- **ng-p3-1:** the simulator never loaded the error rates the test was about, and one of its variations never applied the error it was meant to add. The run tested a different model from the one described.
- **ng-p3-5:** one of the two rival explanations was built so that it could not win on the data it was given.

Two more were weak in ways a dry run shows at once:
- om-p2-4 could not have detected the difference its rule said was absent;
- om-p2-3 hit a refusal risk its own pre-mortem had named.

The design review is the cheap version of the audit, run while the design can still change.

## Who and how

- **A fresh session.** It is not the session that wrote the pre-registration, and it has not seen the chat. It follows `operators/auditor.md`'s independence rules. Where possible it is a different model family; when it is not, the header says so.
- **What it reads:** the pre-registration at its commit, the analysis and run code, the map entry, the lesson line (`operators/learn.md`), and the archives the test will use.
- **What it may run:** the code with every paid call stubbed or replayed from cache, the chip replaced by its simulator, and synthetic data built to have a known answer. It may make **no paid calls**, with one exception: a pilot of at most $0.10, on items excluded from the test, when the pre-mortem names an execution risk (check D6). Pilot results are not test data.
- **Launch** (one local tab, in a fresh worktree of the engine repo at the pre-registration commit; programs are under `programs/<name>/`):
  ```
  cd /Users/seanpharris/oversight-testbed && git worktree add ../oversight-testbed-review-<bet-id> <prereg-commit> && cd ../oversight-testbed-review-<bet-id> && claude --model opus "Read /Users/seanpharris/oversight-testbed/operators/design-review.md and follow it. Bet: <bet-id>. Pre-registration: programs/<name>/experiments/<file>.md at <prereg-commit>. Write the review to /Users/seanpharris/oversight-testbed/ledger/design-reviews/<bet-id>.md."
  ```
  The engine session may instead launch the reviewer as a fresh subagent with a brief that names the files; either way the reviewer has not seen the work.

## The checks

Each gets one of: *holds*, *flaw* (with evidence and the fix), or *cannot check* (with the reason).

**D1. The rule can be applied by a stranger.** Hand the §5 reading to yourself as a stranger, run it on a synthetic results table for each possible verdict, and check that it returns exactly one verdict each time.

**D2. Every manipulation takes effect** (pattern P4). For each knob the design turns (a noise term, a calibration, a framing, a planted number, a label), run the code at two settings and check that the output moves. Print the parameters the run will actually use and compare them with the pre-registration's text. *ng-p3-1 would have failed this: T1/T2 unchanged after the overwrite, and identical counts at ZZ 0, 0.1 and 1.0 rad.*

**D3. Every control can fail** (P6). For each control or reproduction band, name a wrong set-up it must reject, run it, and check that it is rejected. *ng-p3-1's band was passed by a noiseless simulator.*

**D4. Rivals are matched** (P5). Where two families or models compete, check on synthetic data that each can reproduce the other's best case, and that neither wins by construction (parameter counts, constraints, purity, scale).

**D5. A dumb baseline is beaten, and the design can see the effect** (P2, P3).
- Name the dumbest predictor that could pass: constant, one-bit, label-only, noiseless, no-uptake. Check, on the archive or synthetic data, that the rule is not passed by it.
- For a "no difference" rule, check that it has an equivalence margin and a power calculation, with the minimum detectable effect below the margin.
- A rule without these is a **redesign**.

**D6. Foreseeable execution risks are piloted** (P7). If the pre-mortem is of kind `execution`, or the items include content likely to be refused, pilot at most $0.10 on excluded items, or check that a filter rule is written. Check parse rates, token caps and refusal categories on the pilot.

**D7. Comparisons match** (P8). List every difference between the conditions the claim compares: circuit, barrier, shot layout, wording, schema, turn position, model, date. If more than the named factor differs, it is a **fix first**: either match them, or rewrite the claim as about the bundle.

**D8. The verdict sentences are written** (P9). §5 has the plain-English sentence for each possible verdict, using only nouns the design can carry.

**D9. One item cannot decide it** (P10). The leave-one-item-out check is pre-registered, and so is what happens if one item flips the label.

**D10. Machinery.** Budget enforced in code; stop-on-refusal in code; one scale direction (0 = false, 100 = true); caching by content hash; the beacon seed rule (`operators/hardware.md`); and the lesson line present and matching (`operators/learn.md`).

## Verdict and what follows

- **go:** no flaw. The run may start.
- **fix first:** flaws that can be fixed without changing what is being tested. The author fixes each one under a dated DEVIATIONS row, written before any data and naming this review, and the reviewer confirms the fix in a short addendum to the review file. A fix may tighten the design but never lower the bar. Odds may be revised before data (both numbers kept).
- **redesign:** the test cannot answer its question as built (for example, a null rule with no power). The bet is withdrawn before data, recorded in `ledger/bets.jsonl` with `verdict: withdrawn`, and re-bet as a new pre-registration with a new lesson. A withdrawn bet is not scored, but it is counted and published: a high withdrawal rate says the engine designs badly.

## Output: `ledger/design-reviews/<bet-id>.md`

```markdown
---
bet: <bet-id>
program: <program>
prereg_commit: <sha>
reviewer_session: <name>
reviewer_model: <model id>
author_model: <model id>
same_model_family: true|false
date: <YYYY-MM-DD HH:MM America/Denver>
checks: {D1: holds, D2: flaw, ...}
flaws: <int>
pilot_usd: 0.00
verdict: go|fix-first|redesign
confirmed_at: <date, when a fix-first is confirmed; else null>
---

# Design review of <bet-id>

## In plain English
<three to five sentences: would this test have answered its question as built, and what had to change>

## Checks
<D1–D10, each with evidence and the commands run>

## Required fixes
<each flaw, with the exact fix and the DEVIATIONS row it needs>
```

Commit it to `oversight-testbed` on its own: `Design review <bet-id>: go | fix-first (<n>) | redesign`.

## Scored later

When the bet's post-result audit is in, the ledger session records whether the audit found a flaw the design review should have caught under D1–D10 (`design_review_missed: [...]`). `ledger/scores.md` publishes the share of reviews ending go, fix-first and redesign, the flaws per review, and the misses per review. That last number is the design review's own catch rate, and it can also be tested with plants (`operators/plant.md`): a planted design flaw goes in a copy of a pre-registration.

## Ledger fields: `ledger/bets.jsonl`

`"design_review": {"path": "ledger/design-reviews/<bet-id>.md", "verdict": "go|fix-first|redesign", "commit": "<sha>", "reviewer_model": "<id>", "fix_deviations": ["D<n>"], "missed": null}`. Bets pre-registered before 2026-11-04 17:00 have `design_review: null` with a `design_review_note`.
