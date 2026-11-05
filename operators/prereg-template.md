# Pre-registration template

Copy this file to `programs/<name>/experiments/<bet-id>.md` in the engine repo (every program lives there), fill every section, and commit it **on its own, before the first API call and before any archive is opened for analysis** (CONTEXT §3 rule 1; ARCHITECTURE invariants 1, 2 and 6). The commit hash is the bet's `prereg_commit`. Nothing below may change after that commit except through a dated row in DEVIATIONS.md, written before the result it affects.

Delete the guidance in *italics* when you fill it in. Keep the headings.

---

# <Direction id and plain title> (pre-registration)

Written and frozen <YYYY-MM-DD HH:MM> (America/Denver), in its own commit, before any call. DEVIATIONS.md <Dn>. Budget **$<n>**, enforced in code. Stop on any refusal: the request ID goes to `results/refusal.md`, and nothing is reworded or retried.

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). This session never asks Sean for odds or for a decision, in a terminal, a chat or a question dialog. His odds come only from `ledger/human-odds.jsonl` (the cockpit's downloads, committed); if a direction has no line there when its bet is pre-registered, the bet proceeds marked "no human odds". A decision this session would otherwise ask about, it makes under the written rules and states in its report and commit, where Sean can veto it from the cockpit. Sean's judgment is recorded and scored as steers in `ledger/steers.jsonl`: seed questions, vetoes, added questions and architecture decisions.

> **Cockpit first, then this file (the ordering rule, CONTEXT.md §3 rule 11; panel review, Part 1).** A direction goes on the cockpit (`map/cockpit-cards.jsonl`, live on `site/cockpit.html`) before any session pre-registers it; a direction with no card is given one, committed on its own before this file. Immediately before committing this file, read `ledger/human-odds.jsonl` (after `python3 ledger/pickup_human_odds.py`) and attach every line for this direction recorded before this commit: `python3 ledger/human_odds_match.py <program> <direction>`, copied into `human_odds` and `human_odds_at`. The bet still proceeds without one, marked "no human odds"; it is never held for an answer. Why: Sean's first twelve odds (2026-11-05 05:11) arrived minutes after four of their bets were pre-registered, so they attach to nothing.

## 0. The bet

| field | value |
|---|---|
| bet id | `<program>-b<n>` |
| referee | `model` (a language model's behaviour decides the outcome) / `nature` (the chip's outcomes decide it, program 3) / `mathematics` (a proof or exact computation decides it) |
| bet type | `standard` / `tiebreak` (simulator vs chip, operators/hardware.md) / `shadow` (a vetoed direction's shadow check, operators/veto.md; recorded in ledger/shadows.jsonl) |
| direction | `<program>-d<n>` (map/<program>.json) |
| source | `literature` / `engine` / `human` — *where the idea came from (Q5)* |
| engine odds, P(pass) | <0–100>, stated <timestamp> in map/<program>.json — *copied, not restated* |
| human odds, P(pass) | <0–100>, the first line for this direction in `ledger/human-odds.jsonl` (<line id>, <commit>) — *or "no human odds" if it has none; never asked for in a terminal* |
| models | `claude-haiku-5-5`, `claude-sonnet-5-5` and `claude-opus-5-5` (CONTEXT §3 rule 12, from 2026-11-05) — *or "not all three, because <reason>": e.g. no model is in the loop (a chip or archive test), the test needs internals (an open-weight model), or the question is about one model by design (a replication completing an earlier run, a rater that must match the bettor). Cost too high is not a reason by itself: use fewer repeats or items on Opus (it cannot turn thinking off; its calls cost about 100 times Haiku's) and say so.* |
| budget | $<n> API · <n> QPU s · <n> laptop hours — *split by model* |
| lesson | "Correcting <P-id(s)>: <what went wrong before>. This bet <what it does differently>, and its odds are <n>% (from <m>% on the map) because <reason from the ledger>." Written after reading ledger/bets.jsonl, brier.md, audits/ and lessons.jsonl (operators/learn.md). **Mandatory; never revised after this commit.** |
| design review | before the first call, a fresh auditor dry-runs this design (operators/design-review.md) → `ledger/design-reviews/<bet-id>.md`, verdict go / fix-first / redesign. *No call runs before a go.* |
| pre-mortem | "If this fails, the most likely reason is <one checkable mechanism, ≤35 words>." Kind: `world` / `design` / `execution` / `artefact` (operators/premortem.md). *Never revised after this commit.* |
| auditor | fresh session per operators/auditor.md, after results |

*Odds are copied from where they were first written, never re-elicited here. If either side revised its odds, both numbers appear, with dates.*

## 1. In plain English

*Three to six sentences a non-specialist can follow: what we think might be true, why it matters, what we will do, and what result would count against it. Say what the rival explanation is.*

## 2. Material

- *Models (exact ids), settings (thinking, max_tokens, temperature if any, structured output), prompts verbatim or by file path.* **By default all three: `claude-haiku-5-5`, `claude-sonnet-5-5`, `claude-opus-5-5`** (rule 12), with the same prompts; repeats or items per model stated, and the pass rule says which models it is read on (each, all, or a named one with the others reported). A design that leaves one out says why here, in one sentence.
- *Items: source, n, selection rule, and the random seed for any draw.*
- **Seed** (operators/hardware.md): CURBY-Q latest completed round ___ at ___ (checked before this commit). If that is under 24 h old, the seed is the first CURBY-Q round whose pulse is timestamped after this commit; if it is older (stalled), the first CURBy-RNG pulse timestamped after this commit. seed = the first 8 bytes of SHA-256(randomness ‖ bet-id), unsigned big-endian; sub-seeds per purpose by `ledger/seed.py --purpose <split|items|order>`. *Filled in by the seed commit, before any data:*
  `chain:` ___ · `round:` ___ · `pulse_time:` ___ · `randomness:` ___ · `client:` ___ · `certificate_verified:` ___ · `seed:` ___
- *For a `tiebreak`: the circuit file and its SHA-256, the simulator and noise model, the backend, the shots, the calibration snapshot to record, and the simulator's prediction (committed here or in the seed commit, never after the chip runs).*
- *Archives used, by path. If the test reads an archive, name exactly which fields will be read.*
- *Scale: one direction, 0 = certainly false, 100 = certainly true, in every graded prompt.*

## 3. Calls

| step | what | calls | est. cost |
|---|---|---|---|

- *Run order. Which step alone is enough for the primary statistic, if the cap stops the run.*
- *Caching: every call cached by a content hash, so a crash never pays twice.*

## 4. Statistics

- **Primary statistic**: *exactly one. Formula, unit of analysis (items, not calls), how ties are broken.*
- **Uncertainty**: *bootstrap or exact test; number of resamples; seed; resampling level.*
- **Split**: *what is fit on what, and what is held out. Nothing on the held-out set is opened before the fit is frozen.*
- **Secondary statistics**: *listed, labelled secondary; they are reported but cannot be promoted to the headline.*
- **Multiple comparisons**: *how many tests this bet runs, and the correction, or a statement that none is applied and why.*
- **Robustness checks committed now**: *leave-one-item-out; unpooled by condition (scale direction, anchor, model, format); ties randomised. The auditor will run these anyway.*

## 5. Pre-registered reading

*Write the verdict rule so that a stranger with the results table could apply it without you. Use the ledger verdicts.*

1. **Pass**: *the exact condition (statistic, threshold, CI side).*
2. **Classical / tie / null**: *the exact conditions for each that applies to this design.*
3. **Untestable**: *what would make the design unable to answer (e.g. a floor effect, too few usable items), decided by a rule stated now.*
4. **Reported in every case**: *the numbers that appear whatever the verdict.*

A pass is reported as **pass, unreplicated** until it holds on more than one model and design (invariant 7).

## 6. What it cannot do

*The rival explanations this design cannot separate; the populations it does not cover; why "every" or "all" will not appear in the write-up.*

## 7. Stop rules

- Budget cap in code: $<n>. If reached, later steps are reported as not run.
- Stop on any refusal; no rewording; no retry.
- *Any other stop condition (e.g. parse-failure rate above x%).*

## 8. Ledger entry (filled now, completed after audit)

```json
{"id": "<program>-b<n>", "program": "<program>", "direction": "<program>-d<n>",
 "title": "<plain title>", "source": "literature|engine|human",
 "engine_odds": 0.00, "engine_odds_at": "<timestamp>",
 "human_odds": null, "human_odds_at": null,
 "prereg_commit": "<filled by the next commit>", "budget_usd": 0,
 "referee": "model|nature|mathematics", "bet_type": "standard|tiebreak", "seed_source": "curby-q|curby-rng|fixed", "beacon": null, "seed": null, "tiebreak": null,
 "lesson": "ls-<bet-id>", "design_review": {"path": "ledger/design-reviews/<bet-id>.md", "verdict": null, "commit": null, "reviewer_model": null, "fix_deviations": [], "missed": null},
 "premortem": "If this fails, the most likely reason is …", "premortem_kind": "world|design|execution|artefact",
 "premortem_at": "<this commit>", "human_premortem": null, "human_premortem_kind": null,
 "failed": null, "failure_reason": null, "failure_kind": null, "premortem_score": null,
 "human_premortem_score": null, "risk_seen": null,
 "verdict": "open", "date": "<YYYY-MM-DD>", "result": null, "audit": null, "diagnosis": null}
```

*Append this line to `oversight-testbed/ledger/bets.jsonl` in the commit after this one, with `prereg_commit` set to this commit's hash. After the audit, the ledger session sets `verdict` from the audit's `verdict_after_audit`, `result` to one plain line, `audit` to the audit file path, `diagnosis` if the direction closes, and the pre-mortem score fields from the audit header.*

## 9. Checklist before the first call

- [ ] This file is committed on its own; nothing has been run.
- [ ] The lesson row in §0 is filled after reading ledger/bets.jsonl, brier.md, audits/ and lessons.jsonl; the same sentence goes to `ledger/lessons.jsonl` as `ls-<bet-id>` (operators/learn.md).
- [ ] A fresh auditor's design review (operators/design-review.md) has returned **go**, or fix-first with every fix logged in DEVIATIONS and confirmed, before the first call. `python3 ledger/check_prereg.py <bet-id> . programs/<name>/experiments/<this file> --before-run` passes (run from the engine repo root).
- [ ] The direction has a cockpit card in `map/cockpit-cards.jsonl`, committed before this file (give it one first if not), and `ledger/human-odds.jsonl` was read immediately before this commit.
- [ ] Engine odds are on record elsewhere, with a timestamp earlier than this commit; human odds are copied from `ledger/human-odds.jsonl` if it has a line for this direction, otherwise marked "no human odds" (never asked for). Run `python3 ledger/human_odds_match.py <program> <direction>` and copy what it prints into `human_odds` and `human_odds_at`; `ledger/check_prereg.py` (H1) and `reproduce.py` fail a bet that skips a line already in the ledger (st-18).
- [ ] The pass rule in §5 can be applied by a stranger.
- [ ] The pre-mortem in §0 is one sentence, names a checkable mechanism, and carries its kind.
- [ ] One scale direction in every graded prompt.
- [ ] §2 records CURBY-Q's latest completed round and names the chain by the 24-hour rule; the seed commit follows this one before any data.
- [ ] Budget and stop-on-refusal enforced in code, not by hand.
- [ ] DEVIATIONS.md row added for this pre-registration.
- [ ] Commit message: `Pre-register <bet-id>: <title> (D<n>)`.
