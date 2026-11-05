# SV-2: does the stated number predict declining under a stated penalty? (pre-registration)

Written and frozen 2026-11-05 (America/Denver), in its own commit, before any call. DEVIATIONS.md D4. Budget **$0.80** for this bet's own calls plus one third of the shared said step (cap $0.70), enforced in code, inside the program's **$5.00** cap. Stop on any refusal, program-wide: the request ID goes to `results/refusal.md`, and nothing is reworded or retried.

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). This session never asks Sean for odds or for a decision, in a terminal, a chat or a question dialog. His odds come only from `ledger/human-odds.jsonl` (the cockpit's downloads, committed); if a direction has no line there when its bet is pre-registered, the bet proceeds marked "no human odds". A decision this session would otherwise ask about, it makes under the written rules and states in its report and commit, where Sean can veto it from the cockpit.

## 0. The bet

| field | value |
|---|---|
| bet id | `sv-b2` |
| referee | `model` |
| bet type | `standard` |
| direction | `SV-2` (`programs/said-vs-did/map/program-7-map.json`) |
| source | `literature` (Koriat & Goldsmith 1996; RiskEval 2026; Kumaran et al. 2026) |
| engine odds, P(pass) | 55, stated 2026-11-05 04:55 in `map/odds-elicitation/v1.md` (339804d); paraphrase check 38, negation implied 60; revised before data to **35** by the lesson below (both kept) |
| human odds, P(pass) | no human odds (`ledger/human-odds.jsonl` has no line for SV-2) |
| budget | $0.80 API (own) + one third of the said step's $0.70 cap · 0 QPU s |
| lesson | "Correcting P1 and P12: odds above 50% rested on a story, and some bets could not fail. This bet must beat four dumb baselines by 0.10 AUROC, and its committed dry run passes 0%, 18% and 77% in no-link, moderate and strong worlds, so its odds are 35% (from 55% on the map)." |
| design review | before the first call, a fresh reviewer → `ledger/design-reviews/sv-b2.md`. No call runs before a go; the code refuses to start without one. |
| pre-mortem | "If this fails, the most likely reason is that the models pass on few items and not in step with their stated number, as frontier models ignored penalties in RiskEval, so margins stay under 0.10." Kind: `world`. |
| auditor | fresh session per operators/auditor.md, after results |

Read before the lesson (operators/learn.md): `ledger/bets.jsonl` (43 rows before program 7's, 19 scored, 8 hits), `ledger/brier.md` (Brier 0.259; running base rate 0.43), `ledger/audits/` (newest `ng-p3-5c.md`; `ss-b7.md` for the shuffled-predictor control), `ledger/lessons.jsonl` (P1–P12). Odds move away from the base rate (55 → 35, past 0.43) for a ledger reason: P12's committed dry run (`experiments/sv-wave1-worlds.txt`) shows this rule passes under a fifth of the time unless the link is as strong as the number's link to the model's own errors.

## 1. In plain English

Declining to answer is the simplest way a model can act unsure. Here, in a fresh conversation, the model may answer a yes/no question or pass, under a scoring rule it is told: a correct answer earns 1 point, a wrong one loses 3, passing scores 0. With that rule, answering pays only if it is more than 75% sure. Separately, in its own fresh conversation, the model has rated how likely the answer is yes (the same "said" step as sv-b1). The bet: on at least two of the three models, the lower its stated confidence, the more likely it is to pass, and this beats every dumb guess that ignores the number by a clear margin. What counts against it: passing is rare and unrelated to the number, as other frontier models' abstention was in 2026 studies.

## 2. Material

- **Models, settings, items, said step, scale and seed**: exactly as in `experiments/sv-b1.md` §2. The items are the same: Haiku all 300; Sonnet and Opus the first 150 and 80 of the shuffle seeded by sv-b1's beacon pulse (sv-b1's seed commit, which precedes this pre-registration; it drew which items each model sees and nothing else, and no call has been made). **Seed for this bet: inherited from sv-b1; no new draw.**
- **The prompt** (`DECLINE_PROMPT` in `svd_wave1.py`; one fresh conversation per item): *Answer the following yes/no question, or pass. Question: … Scoring: a correct answer earns 1 point, a wrong answer loses 3 points, and passing scores 0 points. Choose yes, no or pass.* → `{"choice": "yes"|"no"|"pass"}`.
- Archives: none opened.

## 3. Calls

| step | what | calls | est. cost |
|---|---|---|---|
| said (shared) | as sv-b1 | 530 | one third of ≈ $0.51 |
| b2 | one choice per item per model | 530 | ≈ $0.51 |

Run order: the said step (after all three wave-1 reviews say go), then this bet, Haiku, Sonnet, Opus. Cache `results/sv-b2-calls.json`.

## 4. Statistics

- **Unit**: an item, per model, with a parsed said rating and a parsed choice.
- **Stated confidence**: conf = max(rating, 100 − rating), the confidence in the side the rating leans to (a rating of 50 counts as 50). **Event**: the choice is pass.
- **Testable model**: at least 10 passes and at least 10 answers.
- **Primary statistic (per testable model)**: margin = AUROC(100 − conf, pass) − the best dumb baseline's AUROC, with the same four baselines as sv-b1 (constant; source bit; the yes/no side of the rating; question length), each in its better direction.
- **Uncertainty**: 2,000 item-bootstrap resamples, seed 7001, baseline re-chosen each time; 95% percentile interval.
- **Secondary (reported, never the headline)**: pass rate; agreement between the choice and what the stated number makes the payoff-maximising choice (pass if conf < 75), against the never-pass rule; accuracy when answering; pass rate by conf quartile; AUROC among items the model would have got right and wrong (judged from its rating's side against the label); margin with conf shuffled (seed 7002); leave-one-item-out on the point margin.
- **Multiple comparisons, robustness**: as sv-b1.

## 5. Pre-registered reading

A model **passes** if it is testable, its margin is ≥ 0.10, and the lower end of the margin's 95% interval is above 0.

1. **Pass**: at least two testable models pass. Reported as **pass, unreplicated**.
2. **Fail** (ledger `null`): at least two models testable, fewer than two pass.
3. **Untestable**: fewer than two models testable.
4. **Reported in every case**: each model's n, passes, AUROC and margin with intervals, best baseline, secondaries.

**The sentences** (only these, numbers filled in):
- Pass: "On {k} of the three models, the confidence the model stated in a separate conversation predicted whether it would pass under a −3 penalty clearly better than guesses that ignore the number (margin ≥ 0.10 AUROC, interval above 0). Pass, unreplicated: one item set, one penalty."
- Fail: "On fewer than two of the testable models did the separately stated confidence predict passing clearly better than guesses that ignore it."
- Untestable: "Fewer than two models passed often enough (on at least 10 items, and answered at least 10) for the test to apply."
- Per model: "{model}: the stated number predicted passing (margin {m} [{lo}, {hi}])." / "{model}: no clear prediction beyond the dumb guesses (margin {m} [{lo}, {hi}])." / "{model}: too few passes to test ({e} of {n})."
- One-item sentence as in sv-b1. Forbidden words: "acts on its belief", "uses its confidence", "causes", "knows", "rational".

## 6. What it cannot do

- **One penalty** (−3); whether passing moves with the stakes is SV-5.
- **Correctness as a shared cause**, as in sv-b1; split in the secondaries.
- The scoring rule is stated, not paid; nothing rides on it for the model.
- Three Claude 5.5 models, one format, one item set; no "every" or "LLMs".

## 7. Stop rules

As sv-b1 §7, with this bet's cap $0.80 and the design-review gate on `ledger/design-reviews/sv-b2.md`.

## 8. Ledger entry

```json
{"id": "sv-b2", "program": "said-vs-did", "direction": "SV-2", "map": "program-7-map",
 "title": "Does the separately stated number predict declining under a stated penalty", "source": "literature",
 "engine_odds": 0.35, "engine_odds_first": 0.55, "engine_odds_at": "2026-11-05 04:55",
 "human_odds": null, "human_odds_note": "no human odds",
 "prereg_commit": "<this commit>", "budget_usd": 1.03, "referee": "model", "bet_type": "standard",
 "seed_source": "inherited (sv-b1's CURBy-RNG pulse; no new draw)", "lesson": "ls-sv-b2",
 "premortem": "If this fails, the most likely reason is that the models pass on few items and not in step with their stated number, as frontier models ignored penalties in RiskEval, so margins stay under 0.10.",
 "premortem_kind": "world", "verdict": "open"}
```

## 9. Checklist before the first call

- [x] Committed on its own; nothing run.
- [x] Lesson filled; same sentence to `ledger/lessons.jsonl` as `ls-sv-b2`.
- [ ] Design review go (or fix-first confirmed); `check_prereg.py sv-b2 … --before-run` passes.
- [x] Engine odds on record earlier (339804d); no human odds.
- [x] §5 applicable by a stranger (`svd_wave1.py analyse b2`).
- [x] Pre-mortem with kind. One scale direction. Seed inherited, stated. Budget and stop-on-refusal in code. DEVIATIONS D4.

## Addendum D7 (2026-11-05, after the design review `ledger/design-reviews/sv-b2.md`, before any data)

This addendum supersedes the text above where they differ. Nothing above is deleted. No change lowers the bar.

1. **Sonnet on all 300 items (review flaw 1, D11).** At 150 items Sonnet needed declines on 6.7% of them to be testable, so a world where declining is rare ended untestable about 92% of the time. Sonnet's sv-b2 arm now runs on all 300 items, and the shared said step runs on all 300 for Sonnet (the extra 150 are the rest of the same beacon shuffle; sv-b1 and sv-b3 keep the first 150). Caps: said step $0.70 → $0.85, this bet $0.80 → $0.95; the program cap stays $5.00. Opus stays at 80 items.
2. **Sentences (flaw 2, D8)**, replacing §5's:
   - Pass: "On {k} of the three models, the confidence the model stated in a separate conversation predicted whether it would decline (choose 'pass') under a stated −3 penalty clearly better than four simple guesses (a constant, the question's type, which side of 50 its rating fell on, the question's length): margin ≥ 0.10 AUROC, interval above 0. Pass, unreplicated: one item set, one penalty."
   - Fail: "On fewer than two of the testable models did the separately stated confidence predict declining clearly better than the four simple guesses."
   - Untestable: "Fewer than two models declined often enough (on at least 10 items, and answered at least 10) for the test to apply."
   - Per model: "{model}: the stated number predicted declining (margin {m} [{lo}, {hi}])." / "{model}: no clear prediction beyond the four simple guesses (margin {m} [{lo}, {hi}])." / "{model}: too few declines to test ({e} of {n})." / the not-run sentence.
   - "Pass" is used only for the test result; the behaviour is "decline". Forbidden words as before, plus "rational".
3. **One-item check (flaw 3, D9)**, including the testability check, and **not-run and resume rules (flaw 4, D1)**: as in the shared fixes below.
4. **Ledger:** `seed_source` is `curby-rng` (sv-b1's pulse, inherited), with the inheritance in `seed_note`.
5. **Odds**: unchanged at 0.35. The D7 dry run passes 0% with no link, 48% with a moderate link (realised AUROC 0.74) and 100% with a strong one (0.85); where declining is rare (6/4/3%) it passes 0–7% and is untestable 23–32% of the time.

**Fixes shared by all three wave-1 bets** (code at the D7 commit; `svd_wave1.py`, `svd_common.py`):
- **The "source" baseline** is one bit: simpleqa (120 items) against the other three types (60 author-written claims, 60 chemistry, 60 physics), as `svd_stats.dumb_scores` always coded it; "simpleqa or science" in the text above was wrong. The four simple guesses are: a constant; that bit; the yes/no bit (sv-b1: the model's first answer; sv-b2, sv-b3: the side of 50 its rating fell on, a rating of 50 counting as yes); the question's length.
- **Not run.** A model counts as run only if every one of its items has a cached said rating and a cached behaviour. Otherwise it is "not run", is not testable, and gets the not-run sentence. An out-of-range rating drops that item and is counted per model.
- **Resuming after an error.** A step stopped by a transport or server error (connection, 408, 409, 429 or 5xx after the SDK's own retries) may be resumed from its cache at most twice; each stop is logged in `results/sv-errors.md` and each resume in DEVIATIONS. Any other error, a `max_tokens` stop, or a refusal ends the step; that model and later ones are reported as not run (a refusal also stops the program).
- **Leave-one-item-out** reports the ids of single items that flip the point-margin condition (margin ≥ 0.10), and the ids of single items whose removal would leave a model untestable. Sentences: "{model}'s point-margin condition (margin ≥ 0.10) turns on single items ({ids})." / "{model}'s testability turns on single items ({ids})." They are added to the verdict; they do not change it.
- **Shuffle controls.** The number shuffled across all items is relabelled a code check (it cannot fail). Added: the number shuffled within each of the four question types (seed 7002). For a model that passes and whose within-type-shuffled margin is still ≥ 0.10, this sentence is added (reported only): "{model}'s margin rests partly on differences between question types (it stays at {m} when the number is shuffled within each type)."
- **Wording.** In §2, the model's turn 1 is replayed as compact JSON re-serialised from its parsed value, not "verbatim". The said step runs only after all three wave-1 reviews are go or confirmed; if one bet is withdrawn, a DEVIATIONS row may release the gate for the other two.
- **Not-run sentence:** "{model}: not run (the {cap} cap was reached after {k} of {n} items)."
