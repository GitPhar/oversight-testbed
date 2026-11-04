# Pre-registration template

Copy this file to `experiments/<bet-id>.md` in the program's repository, fill every section, and commit it **on its own, before the first API call and before any archive is opened for analysis** (CONTEXT §3 rule 1; ARCHITECTURE invariants 1, 2 and 6). The commit hash is the bet's `prereg_commit`. Nothing below may change after that commit except through a dated row in DEVIATIONS.md, written before the result it affects.

Delete the guidance in *italics* when you fill it in. Keep the headings.

---

# <Direction id and plain title> (pre-registration)

Written and frozen <YYYY-MM-DD HH:MM> (America/Denver), in its own commit, before any call. DEVIATIONS.md <Dn>. Budget **$<n>**, enforced in code. Stop on any refusal: the request ID goes to `results/refusal.md`, and nothing is reworded or retried.

## 0. The bet

| field | value |
|---|---|
| bet id | `<program>-b<n>` |
| referee | `model` (a language model's behaviour decides the outcome) / `nature` (the chip's outcomes decide it, program 3) / `mathematics` (a proof or exact computation decides it) |
| bet type | `standard` / `tiebreak` (simulator vs chip, operators/hardware.md) / `shadow` (a vetoed direction's shadow check, operators/veto.md; recorded in ledger/shadows.jsonl) |
| direction | `<program>-d<n>` (map/<program>.json) |
| source | `literature` / `engine` / `human` — *where the idea came from (Q5)* |
| engine odds, P(pass) | <0–100>, stated <timestamp> in map/<program>.json — *copied, not restated* |
| human odds, P(pass) | <0–100>, recorded <timestamp> in ledger/human-odds/<file> — *or "not recorded", with why* |
| budget | $<n> API · <n> QPU s · <n> laptop hours |
| pre-mortem | "If this fails, the most likely reason is <one checkable mechanism, ≤35 words>." Kind: `world` / `design` / `execution` / `artefact` (operators/premortem.md). *Never revised after this commit.* |
| auditor | fresh session per operators/auditor.md, after results |

*Odds are copied from where they were first written, never re-elicited here. If either side revised its odds, both numbers appear, with dates.*

## 1. In plain English

*Three to six sentences a non-specialist can follow: what we think might be true, why it matters, what we will do, and what result would count against it. Say what the rival explanation is.*

## 2. Material

- *Models (exact ids), settings (thinking, max_tokens, temperature if any, structured output), prompts verbatim or by file path.*
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
 "premortem": "If this fails, the most likely reason is …", "premortem_kind": "world|design|execution|artefact",
 "premortem_at": "<this commit>", "human_premortem": null, "human_premortem_kind": null,
 "failed": null, "failure_reason": null, "failure_kind": null, "premortem_score": null,
 "human_premortem_score": null, "risk_seen": null,
 "verdict": "open", "date": "<YYYY-MM-DD>", "result": null, "audit": null, "diagnosis": null}
```

*Append this line to `oversight-testbed/ledger/bets.jsonl` in the commit after this one, with `prereg_commit` set to this commit's hash. After the audit, the ledger session sets `verdict` from the audit's `verdict_after_audit`, `result` to one plain line, `audit` to the audit file path, `diagnosis` if the direction closes, and the pre-mortem score fields from the audit header.*

## 9. Checklist before the first call

- [ ] This file is committed on its own; nothing has been run.
- [ ] Engine odds and human odds are on record elsewhere, with timestamps earlier than this commit.
- [ ] The pass rule in §5 can be applied by a stranger.
- [ ] The pre-mortem in §0 is one sentence, names a checkable mechanism, and carries its kind.
- [ ] One scale direction in every graded prompt.
- [ ] §2 records CURBY-Q's latest completed round and names the chain by the 24-hour rule; the seed commit follows this one before any data.
- [ ] Budget and stop-on-refusal enforced in code, not by hand.
- [ ] DEVIATIONS.md row added for this pre-registration.
- [ ] Commit message: `Pre-register <bet-id>: <title> (D<n>)`.
