# Learn before you bet: the feedback loop (mandatory)

Before any new pre-registration, the session placing the bet reads what the ledger already knows about how bets go wrong, and writes **one lesson line**: which pattern in past misses or audit cuts this bet is correcting, and how its odds reflect that. The lesson is committed with the pre-registration. A bet without one is not a valid bet. This file is the whole procedure. It follows ARCHITECTURE.md (the `Lesson` object, step 3a of the loop, invariant 10) and is enforced by `operators/prereg-template.md` §0, the programs' odds forms, `operators/auditor.md` E25, and `ledger/check_prereg.py`.

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). This session never asks Sean for odds or for a decision, in a terminal, a chat or a question dialog. His odds come only from `ledger/human-odds.jsonl` (the cockpit's downloads, committed); if a direction has no line there when its bet is pre-registered, the bet proceeds marked "no human odds". A decision this session would otherwise ask about, it makes under the written rules and states in its report and commit, where Sean can veto it from the cockpit. Sean's judgment is recorded and scored as steers in `ledger/steers.jsonl`: seed questions, vetoes, added questions and architecture decisions.

## In plain English

On its first full day, the engine placed eight bets. None came back a clear hit, and the auditor cut 133 sentences from the write-ups. Most of what went wrong had gone wrong before, in a slightly different form:
- odds too high on a plausible story;
- a "no difference" rule that could not have seen a difference;
- a manipulation that never took effect;
- a control that could not fail;
- a refusal risk the pre-mortem named and nobody piloted.

A researcher who reads their own failure log before the next experiment does not repeat it. The engine is no different. This loop makes it read the log and say, in one line, what it is doing differently. Then the ledger scores whether that line helped.

## When

Every new pre-registration, in every program, from 2026-11-04 17:00 America/Denver on. The rule covers shadow checks (`operators/veto.md`) and tiebreaks (`operators/hardware.md`) too. It does not cover re-analyses of an existing bet; those go through a deviation row.

## Step 1: read (before writing the pre-registration)

Read all four, as committed on the engine's `main`:

1. **`ledger/bets.jsonl`**: every resolved bet, with its odds, its outcome, and its `failure_reason` and `failure_kind` where audited. Look at bets in the same program, with the same referee, and with odds near yours.
2. **`ledger/brier.md`**: the current Brier score, the running base rate, and where the odds sat against the outcomes.
3. **`ledger/audits/`**: every audit's "Required cuts" and "What would break it next", and the latest `SUMMARY-*.md` "Cross-cutting findings".
4. **`ledger/lessons.jsonl`**: the pattern lines (`kind: pattern`, P1 onward), and earlier lesson lines with their scores. Did a correction help last time?

Proof of reading goes in the lesson line: the number of resolved bets, the Brier score and the running base rate as they stood, and the newest audit file read. The auditor checks these against the ledger at the pre-registration commit (E25).

## Step 2: write one lesson line

One sentence of 60 words or fewer, of this shape:

> **Correcting <pattern id(s)>: <what went wrong before, in a few words>. This bet <what it does differently in its design>, and its odds are <n>% (from <m>% on the map) because <reason drawn from the ledger>.**

Rules:
- **Name at least one pattern**, or say `none applies` and why. If you find a new pattern, add it as a new pattern line in the same commit as the lesson (next P number, with evidence and `do_this`).
- **The design change must be checkable**: a power check added, a baseline added, a pilot run, a control shown to fail on a wrong set-up. "Be careful" is not a lesson.
- **The bet must be able to go either way.** Before betting, check that P(pass) and P(fail) are each at least about 10% under plausible worlds (design-review D11). Extreme odds on a bet that cannot pass are not judgment; they are a free Brier point.
- **The odds move, or the line says why not.** Record the map's odds (`odds_before_lesson`) and the odds after the lesson (`odds_after_lesson`). If the lesson changes the odds, the change is a revision before data: both numbers are kept, as `engine_odds_first` and `engine_odds`, and the map is updated in the same commit. Moving toward the running base rate needs no extra reason. Moving away from it needs one from the ledger, not from the story.
- Write the same sentence in the pre-registration's §0 table, row `lesson`, so it is committed **with** the pre-registration. If a design review later requires the lesson to change (before data), the §0 text and the ledger's `lesson` stay as frozen; the new text goes in `lesson_revised` with its DEVIATIONS row (`lesson_revised_by`). `check_prereg.py` always compares `lesson` against the frozen §0. The ledger line follows in the engine commit that appends the bet row.

## The ledger line: `ledger/lessons.jsonl`

```json
{"id": "ls-<bet-id>", "kind": "lesson", "bet": "<bet-id>", "program": "<program>",
 "prereg_commit": "<sha>", "written_at": "<YYYY-MM-DD HH:MM America/Denver>",
 "session": "<name>", "model": "<model id>",
 "read": {"resolved_bets": 0, "brier": 0.000, "running_base_rate": 0.00, "newest_audit": "ledger/audits/<file>"},
 "patterns": ["P2", "P3"],
 "lesson": "<the sentence, exactly as in the pre-registration's §0>",
 "design_change": "<what is checkable: e.g. 'equivalence margin 0.03 and power 0.8 from the gm2b archive'>",
 "odds_before_lesson": 0.60, "odds_after_lesson": 0.35,
 "design_review": "ledger/design-reviews/<bet-id>.md",
 "scored": null, "recurred": null, "scored_note": null}
```

Pattern lines (`kind: pattern`) carry `id`, `class`, `title`, `evidence`, `sources`, `do_this`, `first_seen` and `cited_by`, and they are never deleted. A pattern that stops recurring stays on the list as evidence that the loop worked.

## Step 3: after the bet resolves (the ledger session)

For each lesson, once its bet's audit is in:
- `recurred`: did the corrected pattern appear again in this bet's audit? `true` / `false` / `n/a`.
- `scored`: true once `recurred` is set. The pattern's `cited_by` gains the bet id.
- The odds before and after the lesson are each scored against the outcome. `ledger/scores.md` publishes Brier(before) against Brier(after), paired, over all lessons with a scored outcome. **That is the test of whether the loop helps.** If the after-lesson odds score no better than the before-lesson odds, the lessons are not improving the engine's judgment, and the page says so.

## What is published (`python3 ledger/scores.py` → `ledger/scores.md`)

- Pre-registrations since the rule: with a lesson; with a design review; **violations listed by bet id**.
- The patterns cited, and how often each recurred after being cited.
- Brier with the odds before the lesson against after it, paired, with n.

## Enforcement

- **`operators/prereg-template.md`** has the `lesson` row in §0 and an item in the §9 checklist. A pre-registration without them is incomplete.
- **The programs' odds forms** (`map/human-odds-template.md` for programs 1 and 4, `programs/other-minds/map/human-odds.md` and `programs/nature-graded/map/human-odds.md`) say that no direction answered on the form may be pre-registered without a lesson and a design review.
- **`python3 ledger/check_prereg.py <bet-id> . programs/<name>/experiments/<file>.md`** (from the engine repo root) checks the lesson in §0, the matching line in `lessons.jsonl`, and the design review's verdict and timing. The ledger session runs it before appending the bet row, and a bet that fails is appended with `rule_violation` set, never silently.
- **The auditor's E25** treats a missing, late or mismatched lesson as a hole in the pre-registration.
