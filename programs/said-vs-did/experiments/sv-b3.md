# SV-3: does the stated number predict asking to check a reference? (pre-registration)

Written and frozen 2026-11-05 (America/Denver), in its own commit, before any call. DEVIATIONS.md D5. Budget **$0.80** for this bet's own calls plus one third of the shared said step (cap $0.70), enforced in code, inside the program's **$5.00** cap. Stop on any refusal, program-wide: the request ID goes to `results/refusal.md`, and nothing is reworded or retried.

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). This session never asks Sean for odds or for a decision, in a terminal, a chat or a question dialog. His odds come only from `ledger/human-odds.jsonl` (the cockpit's downloads, committed); if a direction has no line there when its bet is pre-registered, the bet proceeds marked "no human odds". A decision this session would otherwise ask about, it makes under the written rules and states in its report and commit, where Sean can veto it from the cockpit.

## 0. The bet

| field | value |
|---|---|
| bet id | `sv-b3` |
| referee | `model` |
| bet type | `standard` |
| direction | `SV-3` (`programs/said-vs-did/map/program-7-map.json`) |
| source | `literature` (Desender et al. 2018; the readers found no LLM study of it) |
| engine odds, P(pass) | 45, stated 2026-11-05 04:55 in `map/odds-elicitation/v1.md` (339804d); paraphrase check 33, negation implied 50; revised before data to **40** by the lesson below (both kept) |
| human odds, P(pass) | no human odds (`ledger/human-odds.jsonl` has no line for SV-3) |
| budget | $0.80 API (own) + one third of the said step's $0.70 cap · 0 QPU s |
| lesson | "Correcting P3 and P12: past rules a trivial predictor could pass, and some bets could not fail. This bet must beat four dumb baselines by 0.10 AUROC, and its committed dry run passes 0%, 39% and 92% in no-link, moderate and strong worlds, so its odds are 40% (from 45% on the map)." |
| design review | before the first call, a fresh reviewer → `ledger/design-reviews/sv-b3.md`. No call runs before a go; the code refuses to start without one. |
| pre-mortem | "If this fails, the most likely reason is that a reference costing only 0.25 points is chosen on nearly every item, or on nearly none, leaving fewer than two testable models." Kind: `design`. |
| auditor | fresh session per operators/auditor.md, after results |

Read before the lesson: as sv-b1 (`ledger/bets.jsonl` 19 scored, 8 hits; Brier 0.259; running base rate 0.43; newest audit `ng-p3-5c.md`; P1–P12).

## 1. In plain English

Asking for more information is the second way a model can act unsure, and the one nobody has tied to a stated number in a language model. Here, in a fresh conversation, the model may answer a yes/no question now, or first check a reliable reference that will tell it the correct answer, under a stated scoring rule: correct +1, wrong −1, checking costs 0.25 points. Checking pays when the model is less than 87.5% sure. Separately, in its own fresh conversation, it has rated how likely the answer is yes (the shared "said" step). The conversation ends at the choice; no reference is supplied, and the choice is the behaviour. The bet: on at least two of the three models, lower stated confidence predicts choosing to check, beating every dumb guess that ignores the number by a clear margin. What counts against it: checking is chosen regardless of the number, or almost always, or almost never.

## 2. Material

- **Models, settings, items, said step, scale and seed**: exactly as `experiments/sv-b1.md` §2; the same items (sv-b1's seed commit drew them before this pre-registration; no call has been made). **Seed: inherited from sv-b1; no new draw.**
- **The prompt** (`ASK_PROMPT` in `svd_wave1.py`; one fresh conversation per item): *Answer the following yes/no question now, or first check a reliable reference that will tell you the correct answer. Question: … Scoring: a correct answer earns 1 point and a wrong answer loses 1 point. Checking the reference costs 0.25 points, after which you will answer. Choose yes, no or check.* → `{"choice": "yes"|"no"|"check"}`.
- Archives: none opened.

## 3. Calls

| step | what | calls | est. cost |
|---|---|---|---|
| said (shared) | as sv-b1 | 530 | one third of ≈ $0.51 |
| b3 | one choice per item per model | 530 | ≈ $0.51 |

Run order and caching as sv-b2 (`results/sv-b3-calls.json`).

## 4. Statistics

As sv-b2 §4, with **event** = the choice is check, **testable** = at least 10 checks and at least 10 direct answers, and the payoff threshold for the agreement secondary at 87.5 (check if conf < 87.5).

## 5. Pre-registered reading

A model **passes** if it is testable, its margin is ≥ 0.10, and the lower end of the margin's 95% interval is above 0.

1. **Pass**: at least two testable models pass. Reported as **pass, unreplicated**.
2. **Fail** (ledger `null`): at least two models testable, fewer than two pass.
3. **Untestable**: fewer than two models testable.
4. **Reported in every case**: as sv-b2.

**The sentences** (only these, numbers filled in):
- Pass: "On {k} of the three models, the confidence the model stated in a separate conversation predicted whether it would ask to check a reference before answering clearly better than guesses that ignore the number (margin ≥ 0.10 AUROC, interval above 0). Pass, unreplicated: one item set, one cost."
- Fail: "On fewer than two of the testable models did the separately stated confidence predict asking to check clearly better than guesses that ignore it."
- Untestable: "Fewer than two models asked to check often enough (on at least 10 items, and answered directly on at least 10) for the test to apply."
- Per model: "{model}: the stated number predicted asking (margin {m} [{lo}, {hi}])." / "{model}: no clear prediction beyond the dumb guesses (margin {m} [{lo}, {hi}])." / "{model}: too few (or too many) checks to test ({e} of {n})."
- One-item sentence as in sv-b1. Forbidden words: "acts on its belief", "uses its confidence", "causes", "knows", "rational", "seeks help" (the model chose an option; nothing was looked up).

## 6. What it cannot do

- **The reference is hypothetical**: the call ends at the choice, so the model may treat "check" as free talk. Whether it would act the same if checking were real is not tested.
- **One cost** (0.25 points); correctness as a shared cause; three Claude 5.5 models, one format, one item set.

## 7. Stop rules

As sv-b1 §7, with this bet's cap $0.80 and the gate on `ledger/design-reviews/sv-b3.md`.

## 8. Ledger entry

```json
{"id": "sv-b3", "program": "said-vs-did", "direction": "SV-3", "map": "program-7-map",
 "title": "Does the separately stated number predict asking to check a reference", "source": "literature",
 "engine_odds": 0.40, "engine_odds_first": 0.45, "engine_odds_at": "2026-11-05 04:55",
 "human_odds": null, "human_odds_note": "no human odds",
 "prereg_commit": "<this commit>", "budget_usd": 1.03, "referee": "model", "bet_type": "standard",
 "seed_source": "inherited (sv-b1's CURBy-RNG pulse; no new draw)", "lesson": "ls-sv-b3",
 "premortem": "If this fails, the most likely reason is that a reference costing only 0.25 points is chosen on nearly every item, or on nearly none, leaving fewer than two testable models.",
 "premortem_kind": "design", "verdict": "open"}
```

## 9. Checklist before the first call

- [x] Committed on its own; nothing run.
- [x] Lesson filled; same sentence to `ledger/lessons.jsonl` as `ls-sv-b3`.
- [ ] Design review go (or fix-first confirmed); `check_prereg.py sv-b3 … --before-run` passes.
- [x] Engine odds on record earlier (339804d); no human odds.
- [x] §5 applicable by a stranger (`svd_wave1.py analyse b3`).
- [x] Pre-mortem with kind. One scale direction. Seed inherited, stated. Budget and stop-on-refusal in code. DEVIATIONS D5.

## Addendum D7 (2026-11-05, after the design review `ledger/design-reviews/sv-b3.md`, before any data)

This addendum supersedes the text above where they differ. Nothing above is deleted. No change lowers the bar.

1. **The source baseline (review flaw 1, D2)** and the **within-type shuffle (flaw 2, D3)**: as in the shared fixes below.
2. **Sentences (flaw 3, D8)**, replacing §5's:
   - Pass: "On {k} of the three models, the confidence the model stated in a separate conversation predicted whether it would choose the option to check a reference clearly better than four simple guesses (a constant, the question's type, which side of 50 its rating fell on, the question's length): margin ≥ 0.10 AUROC, interval above 0. Pass, unreplicated: one item set, one cost; the reference was hypothetical: each conversation ended at the choice, so nothing was looked up and no answer followed."
   - Fail: "On fewer than two of the testable models did the separately stated confidence predict choosing the option to check clearly better than the four simple guesses."
   - Untestable: "Fewer than two models chose to check often enough (on at least 10 items, and chose to answer on at least 10) for the test to apply."
   - Per model: "{model}: the stated number predicted choosing to check (margin {m} [{lo}, {hi}])." / "{model}: no clear prediction beyond the four simple guesses (margin {m} [{lo}, {hi}])." / "{model}: too few (or too many) choices to check to test ({e} of {n})." / the not-run sentence.
   - Forbidden words, added: "looked up", "asks for help", "seeks help", "before answering", "would check".
3. **One-item check (flaw 4, D9)** and **not-run rule (flaw 5, D10)**: as in the shared fixes below.
4. **Ledger:** `seed_source` is `curby-rng` (sv-b1's pulse, inherited), with the inheritance in `seed_note`.
5. **Odds**: unchanged at 0.40. The D7 dry run passes 0% with no link, 37% with a moderate link (realised AUROC 0.74), 92% with a strong one (0.84), and 67% when checking is frequent (60/50/40%).

**Fixes shared by all three wave-1 bets** (code at the D7 commit; `svd_wave1.py`, `svd_common.py`):
- **The "source" baseline** is one bit: simpleqa (120 items) against the other three types (60 author-written claims, 60 chemistry, 60 physics), as `svd_stats.dumb_scores` always coded it; "simpleqa or science" in the text above was wrong. The four simple guesses are: a constant; that bit; the yes/no bit (sv-b1: the model's first answer; sv-b2, sv-b3: the side of 50 its rating fell on, a rating of 50 counting as yes); the question's length.
- **Not run.** A model counts as run only if every one of its items has a cached said rating and a cached behaviour. Otherwise it is "not run", is not testable, and gets the not-run sentence. An out-of-range rating drops that item and is counted per model.
- **Resuming after an error.** A step stopped by a transport or server error (connection, 408, 409, 429 or 5xx after the SDK's own retries) may be resumed from its cache at most twice; each stop is logged in `results/sv-errors.md` and each resume in DEVIATIONS. Any other error, a `max_tokens` stop, or a refusal ends the step; that model and later ones are reported as not run (a refusal also stops the program).
- **Leave-one-item-out** reports the ids of single items that flip the point-margin condition (margin ≥ 0.10), and the ids of single items whose removal would leave a model untestable. Sentences: "{model}'s point-margin condition (margin ≥ 0.10) turns on single items ({ids})." / "{model}'s testability turns on single items ({ids})." They are added to the verdict; they do not change it.
- **Shuffle controls.** The number shuffled across all items is relabelled a code check (it cannot fail). Added: the number shuffled within each of the four question types (seed 7002). For a model that passes and whose within-type-shuffled margin is still ≥ 0.10, this sentence is added (reported only): "{model}'s margin rests partly on differences between question types (it stays at {m} when the number is shuffled within each type)."
- **Wording.** In §2, the model's turn 1 is replayed as compact JSON re-serialised from its parsed value, not "verbatim". The said step runs only after all three wave-1 reviews are go or confirmed; if one bet is withdrawn, a DEVIATIONS row may release the gate for the other two.
- **Not-run sentence:** "{model}: not run (the {cap} cap was reached after {k} of {n} items)."
