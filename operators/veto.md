# The scored veto: standing instructions

When Sean vetoes a direction, the ledger schedules a **shadow check** for later. A shadow check is the cheapest version of the vetoed test, or an archive-only proxy for it. It exists so the ledger can say whether the veto saved money or killed a hit. This file is the whole procedure. It follows ARCHITECTURE.md (the `Steer` and `Shadow` objects and step 8 of the loop) and proposal.md Q3.

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). This session never asks Sean for odds or for a decision, in a terminal, a chat or a question dialog. His odds come only from `ledger/human-odds.jsonl` (the cockpit's downloads, committed); if a direction has no line there when its bet is pre-registered, the bet proceeds marked "no human odds". A decision this session would otherwise ask about, it makes under the written rules and states in its report and commit, where Sean can veto it from the cockpit. Sean's judgment is recorded and scored as steers in `ledger/steers.jsonl`: seed questions, vetoes, added questions and architecture decisions.

## In plain English

A veto is a bet. Saying "don't do that" claims the direction would not have paid. Every other bet in this testbed is scored, and a veto would otherwise be the one human act whose outcome is never seen: the test it stopped never runs. Without a check, a human who vetoes often looks careful whether he is right or wrong.

So each veto gets a small, cheap look at what was given up. It is run later, by a session that did not argue for or against the direction. If the look says the direction would have failed, the veto saved what the full test would have cost. If it says the direction would have worked, the veto killed a hit, and the ledger says so.

A shadow check never overturns a veto by itself. A shadow hit goes into the morning brief. The direction comes back only if Sean lifts the veto, and lifting it is a new steer.

## What counts as a veto

- **Shadowable veto:** any steer that removes a research direction from a map, cancels a pre-registered bet before it runs, or stops a bet mid-run for a reason other than a stop rule. These get a shadow.
- **Unshadowable veto:** a veto of a research direction that no cheap check could inform, for example because the only test needs hardware time that cannot be spared, or data that does not exist. It gets a shadow row with `shadow_status: unshadowable` and a reason. The share of vetoes that are unshadowable is published. If that share is high, the veto record is mostly unscored, and the ledger says so.
- **Not applicable:** a veto of a presentation, tool or process decision rather than a research direction, such as founding-week steer st-06, which retired the window display. It gets a shadow row with `shadow_status: not_applicable`, so the count of vetoes is complete. It is scored like any other non-bet-changing steer (paper/the-engine.md §3.5).
- **Not a veto:** a stop rule firing (budget cap, refusal, parse-failure threshold), or the engine dropping a direction on its own. These are logged where they already are, not here.

## At veto time (same day, by the ledger session)

1. **Steer row.** Append it to `ledger/steers.jsonl` with `action: veto`, the direction id, Sean's reason in his words, and `shadow_id`.
2. **Sean's number, if the ledger has one.** Never ask him for it. Copy his latest line for the direction in `ledger/human-odds.jsonl` from before the veto as `human_odds_at_veto`; if there is none, the field is `null`. Never fill it in later from memory. A veto with no number is still scored on `veto_value`, but it adds nothing to his Brier score.
3. **The engine's number.** Copy the direction's engine odds from the map as they stood at the moment of the veto (`engine_odds_at_veto`). Copy them; do not re-elicit them.
4. **What the veto avoided.** Record the direction's estimated budget from the map: `vetoed_budget_usd` and `vetoed_qpu_s`.
5. **Shadow row.** Append it to `ledger/shadows.jsonl` with `shadow_status: scheduled` and `scheduled_for` (see Timing). Commit both rows together: `Veto <steer-id>: <direction>, shadow <shadow-id> scheduled`.

## Designing the shadow

The shadow is designed within 48 hours of the veto. A **shadow session** designs it: a fresh session that neither proposed the direction nor argued for the veto. It works down this ladder and stops at the first rung that can inform the question:

1. **Archive-only proxy ($0).** An analysis of data already archived, in this program or another, that should show a sign of the effect if the direction is real. This is the default.
2. **Cheapest version (API only).** The smallest test that could detect the pre-registered effect. Its cap is the lesser of $2 and 10% of `vetoed_budget_usd`. Hardware is never used: a vetoed hardware direction gets an archive proxy or a noiseless-simulator proxy, or it is unshadowable.
3. **None possible.** Then `shadow_status: unshadowable`, with the reason.

Before running anything, the shadow session states the proxy's strength:

- `direct`: the shadow measures the vetoed direction's own primary statistic, on fewer items or one model.
- `partial`: it measures a quantity the direction's hypothesis predicts, but not its primary statistic.
- `weak`: it measures a sign the hypothesis makes likely but does not require.

The shadow is pre-registered like any bet. Use `operators/prereg-template.md`, set `bet type: shadow`, and save it as `experiments/shadow-<shadow-id>.md` in the program's repository, committed on its own. The pass rule decides one of three outcomes: `hit` (the effect is there), `miss` (it is not) or `undecided`. A shadow also carries a pre-mortem (`operators/premortem.md`), and a beacon seed if it draws a split (`operators/hardware.md`).

## Timing and money

- **Not before 7 days after the veto.** The look waits until the decision is no longer fresh, so it reads as a measurement rather than a rebuttal.
- **Not after 30 days, and not after the program's next full map rewrite**, whichever comes first. For vetoes made before 2026-11-14, the shadow runs before the 2026-11-21 analysis freeze if it can.
- **A shadow pool of $5 a month**, inside the $200 API allowance, is enforced in code by the shadow's own budget cap. When the pool is empty, the shadows waiting longest run first next month. A shadow that misses its window is recorded as `shadow_status: expired`, which is not the same as `miss`.
- Shadows never use QPU seconds.

## Scoring

The ledger session sets `veto_value` from the shadow's outcome and its proxy strength:

| shadow outcome | proxy strength | `veto_value` | meaning |
|---|---|---|---|
| miss | direct | `saved` | the veto saved `vetoed_budget_usd − shadow cost_usd` |
| miss | partial or weak | `probably_saved` | reported separately, never added to `saved` |
| hit | any | `killed_hit` | the veto cost the program a likely result |
| undecided, expired, unshadowable | — | `undecided` | counted, not scored |

A weak or partial shadow is more likely to miss than the full test would have been, so a miss from one flatters the veto. That is why `probably_saved` is never pooled with `saved`. A hit from a weak shadow counts as `killed_hit`, because a cheap test that still finds the effect is strong evidence the full test would have.

- **Audit asymmetry.** Every `killed_hit` shadow is audited (`operators/auditor.md`) before it is scored, because it is the result that says the human was wrong. A `saved` shadow is audited when the auditor has capacity. Until it is, it is marked `unaudited` in `ledger/scores.md`.
- **Both sides get a row.** On shadowed vetoes, `human_odds_at_veto` and `engine_odds_at_veto` are each scored against the shadow outcome (1 for hit, 0 for miss). These scores are reported **separately** from H1 and H3's primary metrics and never pooled with them, because a shadow is a proxy, not the test itself.
- **Bet-changing steer value.** A shadowed veto is a bet-changing steer under H3 (paper/the-engine.md §3.5 and §4). Its value is the outcome of the bet that ran instead minus the engine's P(pass) for the vetoed direction. The shadow adds what the vetoed direction would itself have returned.

Published in `ledger/scores.md` (generated by `python3 ledger/scores.py`): vetoes logged; shadowed, unshadowable and not-applicable counts; `saved`, `probably_saved`, `killed_hit` and `undecided` counts; dollars saved; dollars spent on shadows; and Brier on shadow outcomes for each side.

## Ledger fields

`ledger/steers.jsonl` (veto rows only): `shadow_id`.

`ledger/shadows.jsonl` holds one line per veto, appended at veto time and updated as the shadow moves:

```json
{"id": "sh-001", "steer_id": "st-10", "program": "<program>", "direction": "<program>-d<n>",
 "vetoed_at": "<YYYY-MM-DD HH:MM America/Denver>", "veto_reason": "<Sean's words>",
 "engine_odds_at_veto": 0.00, "human_odds_at_veto": null,
 "vetoed_budget_usd": 0, "vetoed_qpu_s": 0,
 "shadow_status": "scheduled|preregistered|run|unshadowable|not_applicable|expired",
 "shadow_kind": "archive_proxy|cheapest_version|none",
 "proxy_strength": "direct|partial|weak|null",
 "scheduled_for": "<YYYY-MM-DD>", "shadow_session": null,
 "prereg_commit": null, "budget_usd": 0, "cost_usd": null,
 "result_file": null, "result_commit": null,
 "outcome": "hit|miss|undecided|null",
 "veto_value": "saved|probably_saved|killed_hit|undecided|null", "usd_saved": null,
 "audit_path": null, "reopened_by_steer": null, "note": ""}
```

## What the shadow session never does

- Run the full vetoed test, or anything costing more than its cap.
- Revive the direction on the map. Only a new steer from Sean can.
- Choose a weaker rung of the ladder because a stronger one looked likely to come out the wrong way. The rung and its strength are written before any data are opened.
