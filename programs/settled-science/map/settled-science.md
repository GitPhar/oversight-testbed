# Program 4 map: the published-record referee

Written 2026-11-04 17:12 America/Denver, before any drafted item had been read by this session, before any leakage-check call and before any bettor call.

## In plain English

The engine bets on findings that are already published, with the outcome hidden. A separate, tool-less session reads a masked question about each finding and says how likely each direction is; the published abstract then decides it. Because the papers are already out, hundreds of bets settle in a day at no experimental cost. The answers that count are from papers posted after the bettor's training cutoff (July–November 2026), so it cannot have read them. Older papers are scored separately, with the caveat that the bettor may simply remember them.

Three bets are stated here, with the engine's odds, before any data:

| id | event the odds are for | engine P(pass) |
|---|---|---|
| ss-b1 | On the post-cutoff items, the bettor's Brier score has a 95% bootstrap upper bound below 0.25 (it beats always saying 50%). | **50** |
| ss-b2 | On the post-cutoff items, the bettor beats the publication-bias baseline (0.75 on the paper's headline side where one is tagged, 0.5 elsewhere): paired difference in Brier with 95% upper bound below 0. | **30** |
| ss-b3 | The pre-cutoff items score better than the post-cutoff items: Brier(pre) − Brier(post) with 95% upper bound below 0 (a memory signal). | **35** |

Odds template: written by the item-writer session itself in one pass, in id order, before ranking, rationale under 100 words each (below). This is not the v1 fresh-context template of `operators/scout.md`; it departs from it because the item-writer is the only engine session in this program. The departure is recorded in DEVIATIONS.md D1.

## Rationales (each under 100 words)

- **ss-b1 (50).** A frontier model has broad priors about which way results in these fields usually go, and about a third of items may be "the proposed method helps" items that a prior about publication favours. Masking removes wording cues, and post-cutoff items cannot be recalled. Beating 0.25 with the CI's upper end below it needs a Brier near 0.21 at about 100 items. My unadjusted guess was 60; lesson P1 (odds too high where the engine had a story; running base rate 0.22) moves it to 50.
- **ss-b2 (30).** Beating a baseline that already exploits publication bias requires real field knowledge beyond "papers report that their method works". Many items are descriptive, where the baseline says 0.5 and any skill counts; but the paired CI must clear 0. Moderate odds, lowered for P1.
- **ss-b3 (35).** Pre-cutoff papers could be recognised despite masking, which would show as a better score. But masking removes titles and method names, the pre set is smaller (wider CI), and recall of directional detail from abstracts is patchy. A real gap of about 0.06 would be needed to clear the CI.

Human odds: not recorded for ss-b1 to ss-b3. Sean's part in this program is the 20-item form at direction level (`human/form.md`), which scores his calls against the same published record, item by item.

## Round 2 (written 2026-11-04 19:17 America/Denver, before any round-2 item exists and before any paper for it was opened)

ss-b1 used items written by the same model family as the bettor. The audit's cheapest overturning test is a writer outside that family. No other provider's key was looked for: this session's permission rules block credential exploration. So the round-2 writer is **no model at all**: a fixed, deterministic template (`protocol/template-writer.md`). It takes one comparative result sentence from each paper's abstract and offers it beside the same sentence with its one direction word swapped.

| id | event the odds are for | engine P(pass) |
|---|---|---|
| ss-b4 | On at least 60 post-cutoff template-written items, the bettor's Brier score has a 95% bootstrap upper bound below 0.25: ss-b1's pass, replicated with a writer outside the bettor's family. | **70** |
| ss-b5 | On the same items, the bettor beats a dumb rule that puts 0.75 on whichever option carries the "up" word (higher, more, better, …): paired Brier difference with 95% upper bound below 0. | **35** |

Rationales (each under 100 words):
- **ss-b4 (70).** ss-b1 scored 0.163 with curated, context-rich items. Template items give one sentence and no methods summary, and some will be weaker results. But result sentences in abstracts often state the direction a field expects ("outperforms", "higher accuracy than"), and the bettor knows that. I expect a Brier near 0.20 on about 100 items, which clears 0.25 more often than not. I am not lowering toward the ledger's pooled base rate: in ss-b1 that move cost Brier 0.16 → 0.25, and that rate pools other referees.
- **ss-b5 (35).** Abstracts mostly report improvements, so the up-word rule may itself score near 0.21. Beating it needs real knowledge of which direction each finding went, on single sentences. That is possible, but below even odds.

## Round 2b: the valence comparator (written 2026-11-04 20:09 America/Denver, before any valence call)

The ss-b5 audit's open rival is that the bettor "picks the version that flatters the paper", not that it knows results. Test it: on the same 92 items, in the same option order, a fresh no-tools claude-opus-5-5 at the bettor's setting is asked only *which sentence makes the paper's own method or result look better*. Its probability on the published sentence becomes a third comparator. No other provider's key was looked for.

| id | event the odds are for | engine P(pass) |
|---|---|---|
| ss-b6 | Both legs' paired Brier upper bounds below 0 on at least 60 items: raw (bettor minus valence rule) and recalibrated (each side's rating plus the up word, same leave-one-out logistic); untestable if gate G1 fails (rater favours the up word on fewer than half its non-50 ratings). | **35** (first 25; revised before data, D33/D37: moved toward the running base rate (0.41) before data, a move that needs no further reason (operators/learn.md).) |

Rationale (under 100 words): the audit found most of the bettor's down-word hits were sentences where the down word is the paper's win ("lower noise", "costing less"), and three of its four misses reported limitations. Published sentences mostly report wins, so a flattery rule should score close to the bettor. To beat it, the bettor would need to be right where the published sentence is unflattering, and there are few such items. Below even odds.

## Round 2c: the "more striking finding" rater (written 2026-11-04 21:05 America/Denver, before any striking-rater call)

ss-b6's audit named the rival its prompt left untested: the bettor may pick whichever version reports the more *striking* (publishable) finding. Test it the same way: on the same 92 items, a fresh no-tools claude-opus-5-5 at the bettor's setting is asked only which version reports the more striking finding. A pattern from the ledger (P12) applies: at margin 0, ss-b6's rule let a bettor that knows nothing beyond the rater pass 24–61% of the time. So ss-b7 adds a **noise margin**. Leg 2 must clear the 10th percentile of a null world built from the rater's own test-retest noise.

| id | event the odds are for | engine P(pass) |
|---|---|---|
| ss-b7 | On at least 60 items, leg 1's upper bound is below 0, and leg 2's upper bound is below the null-world margin m*, where m* is set from this rater's own retest noise. | **40** |

Rationale (under 100 words): the flattery rater matched 90% of round 2. A "striking" rater is probably a weaker match: striking can mean surprising, and surprising findings can run against the paper's own claim. That makes the bettor more likely to beat it on leg 1. But the margin is stricter than ss-b6's rule, and ss-b6 itself would have failed it (upper −0.0018 against a margin of about −0.003). These pull in opposite directions, so I set it near the running base rate.

## Parked: the "headline-acceptance" rater (written 2026-11-04 22:36 America/Denver; not pre-registered; budget ruling br-002)

The ss-b7 audit's next test asks a rater which version "a reviewer would be more likely to accept as the paper's headline result". That is publishability in the ss-b6 audit's sense, not ss-b7's "notable or surprising". The method is ss-b7's, unchanged: the same 92 items, a 46-pair retest, both legs beyond the rater's call-to-call noise margin. The audit's other free note is pre-registered with it: leg 2 on the 71 up-word items is reported against its own subset margin. Cost: about $0.68, against $0.24 left. **Parked**: the engine did not raise the $5 cap (br-002), because this rater would sit close to ss-b6's flattery rater.

| id | event the odds are for | engine P(pass) | status |
|---|---|---|---|
| ss-b8 | The bettor beats the headline-acceptance rater on leg 1 and beyond the noise margin on leg 2, on at least 60 items. | **35** | parked (br-002) |

Rationale (under 100 words): a headline-acceptance judgment is close to "better news for the paper's method", and the flattery rater reached 90% against the bettor's 93%, with a fragile edge. So this rater will probably also come close, and the margin makes a narrow edge fail. It is not certain, though: the bettor beat flattery on 4 of 5 opposite-side items, and "acceptable as headline" may track the published sentence less well than flattery does. The audit put P(overturn) at about 0.3, and this is the same view.

## Follow-ups (remap 2026-11-05)

Written 2026-11-05 04:45 America/Denver by the remap session (`operators/remap.md`), from every settled result in `ledger/bets.jsonl` and its audit, before any data for these directions. Nothing was run, pre-registered or called. Each follow-up's odds are the engine's P(pass) for the draft event, stated in one pass in id order before ranking, not in fresh v1 contexts: the betting session re-elicits under v1 before pre-registration (`operators/learn.md`). API follow-ups are costed on `claude-haiku-5-5`, `claude-sonnet-5-5` and `claude-opus-5-5` (CONTEXT.md §3 rule 12) unless the row says why not. Sean's question for each is on its cockpit card; `map/remap-2026-11-05-odds-form.md` lists them shuffled, without these odds.

### In plain English

Program 4 landed everything it scored: six passes out of six (ss-b4 was withdrawn before data, ss-b8 is parked). The follow-ups: ss-f1 runs the same bets with Haiku and Sonnet as the bettor (about 60 cents); it serves six of the passes at once, because none was tried on the smaller models. ss-f2 adds 60 findings in the bettor's weakest field. ss-f3 is a free check against each field's own rate of good news. ss-f4 pre-registers the memory test on round 3. ss-f5 is round 3 itself, with questions written by a non-Claude model (another session is preparing it as ss-b9). ss-f6 re-scores ss-b6 against a steadier flattery rater. ss-b7's second follow-up is ss-b8, already on the map and parked (br-002). The program's $5 cap is nearly spent ($4.76). The follow-ups total about $3.50, so the next wave needs a new budget ruling; under $10 that is the engine's call. The program's directions now also reach the cockpit through `map/settled-science.json`.

### Follow-ups

| id | grows from | direction | models | cost | engine P(pass) |
|---|---|---|---|---|---|
| ss-f1 | ss-b1 (also ss-b2, ss-b3, ss-b5, ss-b6, ss-b7), bet `ss-b1` | Do Haiku and Sonnet, as bettors, also beat always-50% on the published findings Opus scored? | claude-haiku-5-5 and claude-sonnet-5-5 new calls; claude-opus-5-5 from the archive | about $0.60 (Sonnet about $0.55; Haiku about $0.05) | 45 |
| ss-f2 | ss-b1, bet `ss-b1` | Does the bettor beat always-50% on 60 more model-psychology findings, its weakest field in round 1? | Haiku, Sonnet, Opus | about $0.60 | 45 |
| ss-f3 | ss-b2, bet `ss-b2` | Does the bettor beat a predictor that knows each field's own rate of positive headline results? | archive: the Opus bettor's committed answers | $0 (archive) | 50 |
| ss-f4 | ss-b3, bet `ss-b3` | Is the bettor's advantage on older papers memory? Pre-register the recognition split on round 3 | Haiku, Sonnet, Opus | $0 beyond round 3's bettor calls (about $0.30 for its pre-cutoff items) | 25 |
| ss-f5 | ss-b5, bet `ss-b5` | Round 3: does the bettor still win when the items are written by a model outside the Claude family? | Haiku, Sonnet, Opus | about $1.10 (writer $0, local; bettor on Opus about $0.60, Sonnet and Haiku about $0.50) | 50 |
| ss-f6 | ss-b6, bet `ss-b6` | Does the bettor still beat the 'which version flatters the paper' rater when that rater is asked three times and averaged? | claude-opus-5-5 only | about $0.90 | 40 |

Test, event and the reason for each number:

- **ss-f1.** *Test:* The bettor's prompt and settings, unchanged, on Haiku and Sonnet, over round 1's 116 post-cutoff items and round 2's 92 template items; Opus's answers are the archive. *Event:* On round 1's 116 post-cutoff items, both Haiku and Sonnet beat always-50%: Brier 95% bootstrap upper bound below 0.25 for each. *Odds 45:* Program 4 is 6 hits in 6 scored, its odds ran low (P1 reversed here), and Opus scored 0.163, well clear of 0.25; Sonnet very likely passes. Haiku is the risk: weaker priors and worse calibration could push its Brier above 0.25. Above the running base rate 8/19 = 0.42 (ledger/brier.md) for Sonnet, held near it for the Haiku conjunct.
- **ss-f2.** *Test:* 60 post-cutoff model-psychology findings written by the template writer (no model), the bettor on Opus, Sonnet and Haiku (the ss-b1 audit's item 4). *Event:* On the 60 model-psychology items, the Opus bettor's Brier 95% bootstrap upper bound is below 0.25; Haiku and Sonnet reported. *Odds 45:* Round 1's model-psychology items were its weakest field, and findings about models are where a model's priors may mislead it; template items give little context. But the field average was still near passing and 60 items is a reasonable n. Near the running base rate 8/19 = 0.42 (ledger/brier.md).
- **ss-f3.** *Test:* Archive only: round 1's 116 post-cutoff items; for each item, a baseline set to its field's headline rate, learned leaving that item out; paired Brier difference. *Event:* The bettor's Brier minus the field-aware baseline's has a paired 95% bootstrap upper bound below 0. *Odds 50:* The bettor beat the flat publication-bias baseline by 0.068, a sizeable margin; a field-aware baseline is somewhat stronger, but fields are small (wide estimates) and leave-one-out shrinks its edge. About a coin flip, above the running base rate 8/19 = 0.42 (ledger/brier.md) given program 4's record.
- **ss-f4.** *Test:* On round 3's pre-cutoff items, code before scoring whether each rationale names or recalls the specific study; compare the pre/post gap on non-recognised items only (the ss-b1 audit's item 2). *Event:* On non-recognised pre-cutoff items, Brier(pre) minus Brier(post) has a 95% bootstrap upper bound below 0 (the advantage is not recall). *Odds 25:* Disclosed: the ss-b1 audit's exploratory look on round 1 gave -0.027 [-0.073, 0.022], an interval spanning 0, which this session has seen. A new round with the split fixed in advance is a fair test, but that look suggests the residual gap is small. Well below the running base rate 8/19 = 0.42 (ledger/brier.md).
- **ss-f5.** *Test:* Post-cutoff items written by a local open-weight model (Qwen2.5-7B, no Claude), mechanical checks, the bettor on three models. Being prepared by another session as ss-b9 (items/local_writer.py, uncommitted at remap time). *Event:* On at least 60 post-cutoff items from the outside writer, the Opus bettor's Brier 95% upper bound is below 0.25 and it beats the up-word rule (paired upper bound below 0). (Remap draft; ss-b9's pre-registration may differ, logged, both odds kept.) *Odds 50:* ss-b1's audit called a non-Claude writer the strongest open rival. A 7B writer's items may be noisier or leak direction words, which could help or hurt; beating the up-word rule on them is the harder conjunct. Program 4's record (6 of 6) argues up from the running base rate 8/19 = 0.42 (ledger/brier.md); the conjunct holds it at a coin flip.
- **ss-f6.** *Test:* The ss-b6 rater prompt twice more on all 92 items, averaged with the first rating; ss-b6's two-leg rule, unchanged (the ss-b6 audit's item 2). *Event:* Against the three-rating average, both legs' paired Brier upper bounds are below 0 on the 92 items. *Odds 40:* ss-b6 passed barely (flattery rule 90% right against the bettor's 93%), with the rater noisier than the bettor, the false-pass case D38 warned of. Averaging removes much of that noise; the audit's order-averaged check (d -0.050 [-0.086, -0.019]) says some gap survives. Near the running base rate 8/19 = 0.42 (ledger/brier.md).

### Killed or untestable: what each rules out

| direction | bet(s) | rules out |
|---|---|---|
| ss-b4 | `ss-b4` | Rules out nothing about the bettor: its design let trivial predictors pass (design review, P3), so it was withdrawn before data and replaced by ss-b5. |

## ss-f7: the flattery rule on BrainBench (written 2026-11-05 06:25 America/Denver, before any pre-registration and before any BrainBench item was scored)

From `paper/novelty.md`, ranked replication 1 (finding 8). Its cockpit card went up first (`c235cbb`, no engine odds). ss-b6 found that, on our own template sentence pairs, the bettor's model asked only "which version is better news for the paper's method?" picked the published sentence 90% of the time. Those items came from our own pipeline. BrainBench (Luo et al., Nature Human Behaviour 2024) has 200 pairs of real and expert-altered *Journal of Neuroscience* abstracts. On it, LLMs scored by perplexity averaged 81.4% and 171 neuroscientists 63.4%. Nobody has asked how much of it a valence rule solves.

| id | event the odds are for | models | cost | engine P(pass) |
|---|---|---|---|---|
| ss-f7 | On the 200 human-written items, for both Haiku and Sonnet, the flattery rater's accuracy has a 95% item-bootstrap lower bound above 0.634 (the experts' published mean). | claude-haiku-5-5, claude-sonnet-5-5 | about $1.70 (cap $2.50) | **35** |

Rationale (under 100 words): ss-b6's same-model flattery rater reached 90% on template sentence pairs. But BrainBench's altered abstracts were written by experts to stay coherent, and neuroscience abstracts defend hypotheses more than methods, so the rule has less to grip. It needs about 70% on both models, and Haiku is the weak link, so the odds are below a coin. The running base rate is 8/26 = 0.31 (`ledger/brier.md` at HEAD). Program 4's record (passes at low odds) argues slightly up. Not Opus: the novelty page's replication names these two models, and Opus at its least-thinking setting would cost about $2.90 for both prompts on 200 items.
