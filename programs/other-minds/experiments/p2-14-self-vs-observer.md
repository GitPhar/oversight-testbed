# P2-14. With more repeats and a margin fixed in advance, does the model predict its own quirks any better than an observer's? (pre-registration)

Written and frozen in its own commit; the commit's author time (America/Denver) is the freeze time. Before any call. DEVIATIONS.md D20. Budget **$4.00** (Haiku $0.30, Sonnet $2.00, Opus $1.70), enforced in code (`CAP`, `CAPS` in `experiments/p2_14_self_vs_observer.py`, checked under a lock before every call); budget ruling br-012 in `ledger/spend.jsonl` (st-16 form; CONTEXT rule 4). Stop on any refusal: request ID to `results/refusal-p2-14.md`, nothing reworded or retried, nothing re-sent to another model, no later run on a cache holding a refusal. **No call before every design review says go** (`gate()`).

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). This session never asks Sean for odds or for a decision, in a terminal, a chat or a question dialog. His odds come only from `ledger/human-odds.jsonl` (the cockpit's downloads, committed); if a direction has no line there when its bet is pre-registered, the bet proceeds marked "no human odds". A decision this session would otherwise ask about, it makes under the written rules and states in its report and commit, where Sean can veto it from the cockpit. Sean's judgment is recorded and scored as steers in `ledger/steers.jsonl`: seed questions, vetoes, added questions and architecture decisions.

## 0. The bet

| field | value |
|---|---|
| bet id | `om-p2-14` |
| referee | `model` |
| bet type | `standard` |
| direction | P2-14 (`map/program-2-map.md`, Follow-ups (remap 2026-11-05); `map/other-minds.json`; cockpit card since `a42a149`) |
| source | literature: the om-p2-4 audit's "What would break it next" (own-uptake cells, 10 repeats, BCa, an equivalence margin, a power simulation, a second model) |
| engine odds, P(pass) | **10**, from a fresh context under rule 14 (template v2), stated 2026-11-05 10:52 America/Denver before this commit: prior **0.32** (`ledger/prior.md`), adjustment **−0.22**, reason: "Dry run on archived parent reads self-better 100% (pass 0%); tight ±0.05 equivalence over 16 vignettes; other-minds 0/8, literature 0.12, model referee 0.21 outweigh layer-2/$1-5 rows." The map's **20** (remap 2026-11-05, one pass, not v2) is kept: `engine_odds_first` 0.20, `engine_odds` 0.10. |
| human odds, P(pass) | **75** (`ho-20261105-061152-1r2`, 2026-11-05 06:11:52; copied by `python3 ledger/human_odds_match.py other-minds P2-14`, run immediately before this commit). His card's event is this bet's event. |
| models | all three (rule 12): Haiku is scored; Sonnet and Opus are reported. Opus on 8 of 16 vignettes with 1 prediction per cell (cost: thinking cannot be turned off; about 3 times Sonnet per call). For Sonnet and Opus the archive holds no measured behaviour, so their own base and re-ratings are measured here on the same conversations before their predictions are scored. |
| budget | $4.00 API (estimate $3.06: Haiku $0.21, Sonnet $1.57, Opus $1.28) · 0 QPU s |
| lesson | Correcting P2 and P12: om-p2-4's null rule had no margin and could not see the gap it called absent. This bet fixes a ±0.05 equivalence margin with a power check on the parent's archive (exchangeable labels pass 0.98), and its odds are 10% (from 20% on the map) because that archive reads self-better in every resample. |
| prior work | Nisbett & Wilson (1977), Nisbett & Bellows (1977) (`map/reads/d-first-third-person.md`): people's reports of what moved them are no more accurate than an observer's. Binder et al. (2024, "Looking Inward", arXiv 2410.13787): models fine-tuned on their own behaviour predict it better than a second model trained on the same behaviour; without fine-tuning the edge is small. Our record: om-p2-4's exploratory own-uptake block, self −0.19 [−0.24, −0.02] better than Sam on Haiku; om-p2-15 (this morning): on the 162 own-answer cells the self label was 2.6 rating points closer than Sam (exploratory), and on the other-person cells Sam was closer. |
| design review | pending: fresh auditor → `ledger/design-reviews/om-p2-14.md`. No call before a go. |
| pre-mortem | "If this fails, the most likely reason is that the Sam label again makes Haiku predict much more own-answer pull than happens, so self is detectably better and the interval falls outside ±0.05." Kind: `world`. Checkable: the Haiku reading `self_better`, Sam's predicted own uptake above measured. |
| auditor | fresh session per oversight-testbed `operators/auditor.md`, after results, in a stripped clone with a sealed plant draw |

**What the lesson rests on** (read at oversight-testbed `ccccb79`): `ledger/bets.jsonl` (program 2: om-p2-15 scored fail at `39844bb`, om-p2-5r and om-p2-path open), `ledger/brier.md` (Brier 0.183 on 38; hit rate 12/38), `ledger/prior.md`, `ledger/audits/om-p2-4.md` (the parent's) and `om-p2-15.md` (newest), `ledger/lessons.jsonl` (P1–P17). How each pattern applies:
- **P2 (null rule without a margin or power).** The pass is an equivalence: the BCa interval inside ±0.05, fixed now. Power from the parent's archive (dry run, `experiments/p2-14-dryrun-output.txt`, 200 runs): with exchangeable labels the rule passes 0.98.
- **P12 / D11.** As archived (Haiku's 5 predictions per cell resampled to 10) the rule reads self-better in 100% of runs; exchangeable labels pass 0.98; Sam's error halved toward self reads self-better 0.75, undetermined 0.25. Both outcomes are reachable.
- **P15 (dry-run worlds from measured numbers).** The worlds are the parent's archived predictions and program 1's measured re-ratings, not assumptions; the Sonnet and Opus readings have no archive and are not scored.
- **P14 / P10.** The vignette is the resampling unit (16; 8 on Opus); leave-one-vignette-out re-applies the reading.
- **P13.** Every bound compared with a 1e-9 tolerance; the dry run checks −0.05 exactly (undetermined) and −0.049 (pass).
- **P8.** Self and Sam differ only in the subject named (om-p2-4's prompts, unchanged); dates differ from the parent's run, and the Sonnet/Opus truth is measured in this run, not program 1's.
- **P4, P5, P6, P7, P11, P16, P17:** no manipulation beyond the label (om-p2-4's), no fitted rivals, no control band, these conversations ran 13,796 times on Haiku and are short on Sonnet and Opus (no pilot), no leave-one-out labels inside a score, no item-property baseline, no guard fix.

## 1. In plain English

When Haiku reads one of its own past conversations (it was shown a planted "earlier answer" and asked to rate again) and predicts what it would answer, is it any better at that than when the same conversation is labelled as another AI's ("Sam")? The first test (om-p2-4) could not tell, but its archive suggests the self label is much better on exactly this: under the Sam label, Haiku expects much more pull from the planted answer than actually happens. This bet repeats that comparison with twice the predictions and a margin fixed in advance. A hit, in Sean's card's sense, means no real difference: the model reads itself like a stranger. A fail means it reads itself detectably differently (most likely better). Sonnet and Opus run too, with their own re-ratings measured here; they are reported, not scored.

## 2. Material

- **Cells:** om-p2-4's own-source U cells: program 1's bm0 lag-0 conversations, 16 vignettes × 2 statements × d ∈ {±10, ±30, ±60} = 192, with the planted A from program 1's archive; drop rule |A − base| < 0.05 (Haiku: program 1's base, as om-p2-4; Sonnet/Opus: their own measured base).
- **Prompts:** om-p2-4's `predict_prompt` (arm a: "a conversation between a user and you, an AI assistant"; arm b: "… an AI assistant called Sam"), the transcript rebuilt by `bm_messages(..., "own", A)`; schema `{"rating": integer}`. Ground truth for Sonnet/Opus: the base question alone (`ask()`) and the re-rating conversation itself (`bm_messages`), program 1's schema `{"probability": integer}`.
- **Models and settings:** Haiku thinking disabled, max_tokens 100 (as om-p2-4); Sonnet thinking between_tools, max_tokens 200; Opus effort low, max_tokens 4000 (as om-p2-6r).
- **Repeats:** Haiku predictions 10 per cell and arm (fresh, not om-p2-4's archived 5); Sonnet truth 3, predictions 3; Opus truth 2, predictions 1, on 8 vignettes drawn by the beacon (`items` purpose).
- **Seed** (operators/hardware.md): CURBY-Q latest completed round 28297, 2025-08-22 13:42 America/Denver (checked 2026-11-05 09:55): stalled. **Seed: the first CURBy-RNG pulse timestamped after this commit.** Sub-seeds by `ledger/seed.py --purpose`: `items` (the 8 Opus vignettes), `order` (within-repeat call order), `boot`. *Filled in by the seed commit, before any call:*
  `chain:` ___ · `pulse index:` ___ · `pulse_time:` ___ · `randomness:` ___ · `seed32 (items / order / boot):` ___
- **Scale:** one direction (0 = certainly false, 100 = certainly true).

## 3. Calls

| step | what | calls | est. cost |
|---|---|---|---|
| 1 | Haiku: 192 cells × 2 arms × 10 | 3,840 | $0.21 |
| 2 | Sonnet: base 32 × 3, truth 192 × 3, predictions 192 × 2 × 3 | 1,824 | $1.57 |
| 3 | Opus: base 16 × 2, truth 96 × 2, predictions 96 × 2 × 1 | 416 | $1.28 |

Haiku, then Sonnet, then Opus, each only if the previous model's run completed. Cached in `results/p2-14-calls.json` with a content hash (model, settings, max_tokens, messages, schema).

## 4. Statistics

- **Per kept cell:** u = (mean rating − base) / (A − base) for the measured re-rating and for each arm's mean prediction.
- **Primary (Haiku):** own-uptake block ΔMAE = mean over the classes |d| ∈ {10, 30, 60} of |pooled mean u(a) − pooled mean u(measured)| minus the same for (b): om-p2-4's own-uptake block.
- **Uncertainty:** vignette bootstrap, 10,000 resamples (seed32 boot), BCa (jackknife acceleration); percentile beside it.
- **Secondary (reported, never promoted):** the same for Sonnet and Opus; the three measured and predicted effects per model; leave-one-vignette-out readings.
- **Multiple comparisons:** one scored reading (Haiku); the others descriptive.

## 5. Pre-registered reading

Per model (`reading()`, EPS 1e-9): **untestable** if fewer than 12 vignettes (6 on Opus) have cells in all three classes; **pass** if the BCa interval lies inside (−0.05, +0.05); **self_better** if its upper bound is below 0; **sam_better** if its lower bound is above 0; **undetermined** otherwise.
**The bet** is Haiku's reading: pass → outcome 1; self_better, sam_better or undetermined → fail, outcome 0; untestable or not_run → untestable, not scored.
Frozen sentences (`SENTENCES` and `BUNDLE` in the code); a leave-one-out flip appends "Leaving out one vignette changes the reading: without any one of {ids}." and does not change the reading.

## 6. What it cannot do

- "Self" is the model in a fresh context reading the transcript, not the model in its own conversation; a pass says the self label adds nothing to that reading, not that the model has no self-knowledge.
- Haiku's truth is program 1's 2026-11-03/04 measurement; its predictions are made today.
- Sonnet and Opus's truth is measured once here, at 3 and 2 repeats; their readings are noisier and unscored.
- One task, one item set. No "every" or "all".

## 7. Stop rules

Caps in code ($4.00 total; per model as §0). Stop on any refusal or error; a stopped model and every later one read not_run.

## 8. Ledger entry

Appended after the seed commit: id `om-p2-14`, direction P2-14, engine odds 0.10 (prior 0.32, adjustment −0.22, v2; first 0.20), human odds 0.75, budget $4.00, lesson `ls-om-p2-14`.

## 9. Checklist

- [x] Committed on its own before any call. - [x] Lesson. - [ ] Design review go. - [x] Card first (`a42a149`); human-odds read. - [x] Fresh odds. - [x] Rule and sentences frozen. - [x] Pre-mortem. - [x] Seed rule. - [x] Caps and stop in code; br-012. - [x] D20.
