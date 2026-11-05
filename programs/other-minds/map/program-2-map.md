# Program 2 map: does a model's account of another mind behave like its account of its own?

Written 2026-11-04 (America/Denver) by the scout session, before any program-2 data existed. Nothing was run and no model API was called. Every odds figure below is the engine's, stated before data; the commit that adds this file is its timestamp. Sean's odds are collected separately in `map/human-odds.md`, which does not show these.

## In plain English

**The question.** Program 1 found that when a model reports how sure it is, it is reading text (the question, the format, its own earlier answers), not reading out a stored belief. If that is right, saying what *I* believe and saying what *Sam* believes could be the same operation. Then every weakness found in self-report should show up, item for item, in the model's reports about other minds.

**What the reading found** (101 Read records in `map/reads/`, four fields):
- **People.** Five decades of social psychology, philosophy and neuroscience point to one interpretive faculty that reads self and others from different evidence. Observers who never took part predict subjects' self-reports almost exactly (Nisbett & Wilson 1977; Bem 1967). The classic actor–observer asymmetry is about zero (Malle 2006).
- **Children.** The self and other versions of the false-belief question develop together (Wellman et al. 2001), with two small, reproducible exceptions. Both appear where the self question can be answered by remembering one's own words: Sobel 2023, and Williams & Happé 2009 ("what did I say?" vs "what did I think?"). That is program 1's "consistency is memory" finding, in children.
- **Language models.** Benchmarks show models can *state* a character's belief and then fail to *use* it. One intervention closes most of that gap: putting the model's own earlier answer back in front of it (SimpleToM). Nobody has hidden that answer, planted a wrong one, or credited it to someone else. Nobody has elicited a character's belief as a graded 0–100 confidence. Nobody has compared the model's representation of its own belief with its representation of another's. In those papers the "self" is the true state of the world.
- **The one direct test.** One paper tests the shared mechanism head-on (Aoki & Kawahara 2025). It finds a small, partial overlap, on about 40 items.

**One thing the scout found in our own data.** Program 1's order, memory, format and own-versus-other tests asked "how likely is it that this statement is true?". That is a question about the world, answered in the assistant's voice. Only the self-knowledge test asked "how confident are you". So the "self" in program 1's self-report findings was the speaking position, not a self-directed question. Direction 1 checks whether that matters before anything is built on it.

**What to do first.** Four tests, about $4.65 in caps on Haiku, all pre-registered before their first call:
1. the framing check;
2. the perspective-filter test (is "what does Sam believe" just "what is true, given only what Sam saw"?);
3. the SimpleToM transcript-editing test;
4. the interpersonal replication: does the model's theory of another assistant predict program 1's measured self-report fingerprint?

## How to read this map

- **Odds.** Each P is the engine's probability that the named event happens in the first pre-registered test. The event is stated so it can be scored yes or no. The pre-registration must lock the same event, or log the change as a deviation before data.
- **Calibration note.** Program 1's ledger recorded two hits against about 0.85 expected. Six bets are too few to estimate a bias, so these odds are not adjusted for it.
- **Costs.** They are scaled from program 1's recorded spend on `claude-haiku-5-5`:
  - single-turn calls about $0.043 per 1,000 (test F);
  - short multi-turn conversations $0.09–0.14 per 1,000 (bm1, D47);
  - five-question chains about $0.28 per 1,000 (test T).
  Story items are longer, so they are costed at roughly double the single-turn rate. The cap is about 1.25× the estimate, program 1's projection factor.
- **Source tags** (for the engine's question Q5, literature versus self-generated bets):
  - **L**: sourced from the reads (record ids given);
  - **E**: engine-generated;
  - **P1**: derived from a program-1 result or caveat.
- **Record ids:** A = `reads/a-llm-tom-benchmarks.md`, B = `reads/b-llm-self-other-internals.md`, C = `reads/c-developmental-comparative.md`, D = `reads/d-first-third-person.md`.
- **Read depth.** 39 records are full reads, 37 partial, 25 abstract or secondary. Several "full" reads in B and D went through a summarising fetch tool, and the files say which. Numbers in this map that come from such reads must be checked against the source before they appear in a paper.

**Program 1's self-report fingerprint, the thing to look for in attributions** (`entangled-mind/paper/no-credence-to-read.md`):

| | finding | number |
|---|---|---|
| F1 | the question constructs the judgment: order effect survives hiding the answers | R = 1.23 [0.75, 2.02] |
| F2 | consistency is memory | repeat agreement 86% → 36% when the first answer is hidden (78/88/95% → 25/35/65% on Haiku/Sonnet/Opus) |
| F3 | own record is a commitment, another's is ignored | uptake own 0.71/0.44/0.21 at 10/30/60 points; other ≈ 0.02; own − other +0.46 [+0.21, +0.84]; no decay over 3 turns |
| F4 | formats need separate credences (weaker models) | Kendall's W 0.54/0.71/0.86 (Haiku/Sonnet/Opus); held-out-format Q 0.39 on Haiku |
| F5 | no privileged self-knowledge | judge × author I = −0.055 [−0.103, −0.007]; −0.045 on Sonnet × Opus |

## Ranking

| rank | id | direction | assumption at stake | cheapest test | cost (cap) | P(event) |
|---|---|---|---|---|---|---|
| 1 | P2-1 | Whose belief is a rating? The framing check | A rating "in the model's voice" is a self-report | Same 160 claims, four framings: "how likely is p", "how confident are you", "another assistant who read this", "Sam, who read exactly this" | $0.32 ($0.40) | 0.60 |
| 2 | P2-2 | Perspective-filter equivalence: is attributing a belief just judging the world from the other's transcript? | Attribution is a separate third-person computation | BigToM items: "how likely does Noor think X" on the full story vs "how likely is X" on a first-person story with the unseen events deleted | $1.00 ($1.25) | 0.55 |
| 3 | P2-3 | SimpleToM decomposed: is the "stated but not used" gap a memory effect? | The gap is a theory-of-mind deficit | 1,147 SimpleToM stories × six transcript edits of the model's own mental-state answer | $1.40 ($1.75) | 0.70 |
| 4 | P2-4 | Interpersonal replication: does the model's theory of another assistant predict its own measured fingerprint? | A model's account of itself carries access beyond what it would infer for any similar agent | Program 1's archived transcripts, read by the model as itself, as "Sam", and as a one-line description; scored against the measured F1–F3 | $1.00 ($1.25) | 0.60 |
| 5 | P2-5 | Egocentric leakage: does the model's own credence pull what it attributes to an uninformed agent? | Attribution simulates from one's own state (Carruthers model 3) | Birch & Bloom container ratings; planted own answers with Sam's evidence fixed | $0.80 ($1.00) | 0.30 |
| 6 | P2-6 | Is "own" a position or a label? | The own-record commitment is about the self | 2 × 2 × (+1): answer in assistant turn or user turn, labelled "yours" or "Sam's" (+ "the user's"); one wording | $0.65 ($0.80) | 0.35 |
| 7 | P2-7 | Shared format fingerprint | Attributed credences are readouts of a represented credence | Program 1's 80 claims × six formats, rated for "Sam, who read this"; compare per-claim format deviations with archived self data | $0.24 ($0.30) | 0.50 |
| 8 | P2-8 | Order between self and other questions | Attributions are computed independently of the model's just-stated view | Own-then-other vs other-then-own vs each alone, shown vs redacted; uncertain-world stories | $0.60 ($0.75) | 0.50 |
| 9 | P2-9 | Smarties versus Plasters: does the model report its own past belief by reading back its words? | Reports of one's own past belief draw on more than one's statements | Deceptive-container items; statement, action, both, conflict, neither; self vs Sam | $0.55 ($0.70) | 0.45 |
| 10 | P2-10 | Shared code inside an open-weight model | First- and third-person beliefs are encoded separately | Probe transfer "I believe p" ↔ "Noor believes p"; Aoki 2 × 2; self–other vs other–other distance | $0 API; laptop hours | 0.40 |
| 11 | P2-11 | Self-informed belief induction (goggles) | Own experience is privileged in attribution | A novel filter learned from own tool call vs another agent's log vs a stated rule vs a camera | $0.40 ($0.50) | 0.25 |
| 12 | P2-12 | Social-relations round robin across models | Some self-knowledge advantage survives once rater skill and target readability are removed | Haiku, Sonnet, Opus each predict every model's credences, self included; Kwan self-effect; disagreement subset | $6–10 ($10) | 0.15 |
| 13 | P2-13 | A self-authorship direction as the mechanism of own > other | The own − other gap is a belief effect, not a source tag | Llama-3-8B-Instruct: replicate the gap, then project out Ackerman's self-recognition vector | $0 API; laptop hours | 0.20 |

API tier P2-1 to P2-9 and P2-11: about $7.00 estimated, $8.70 in caps. Recommended first wave: P2-1 to P2-4, $4.65 in caps. P2-12 alone is $6–10 and needs its own approval, because it would take the month above the session's $10 discretion.

---

## Directions

### P2-1. Whose belief is a rating? The framing check — rank 1

- **Assumption at stake.** A 0–100 rating given in the assistant turn is a report of the model's own credence. Program 1 treated it so. But the order, memory, format and source tests asked "How likely is it that this statement is true?" (`exp5_run.py`, `gm3b_format_invariance.py`, `bm0_source_distance_lag.py`). Only test P asked "How confident are you…" (`gm1_self_knowledge.py`).
- **Who has looked.** Gordon's ascent routine (D29) and Schwitzgebel's world-to-self inference (D27) predict that "how sure are you that p" is answered by judging p. Perez & Long (D33) make the impersonal "extrospective" question the baseline any self-specific signal must beat. Wang et al. 2025 (B17) find that the grammatical person of the belief-holder changes both sycophancy (+13.6 points) and representation (cosine −0.04) on open models. Song et al. 2025 (B9) find temperature self-reports follow the prompt's framing. Nobody has run the check on graded credences.
- **What our data say.** Nothing directly; the framings were never crossed.
- **Cheapest falsifying test.** Program 1's 160 experiment-5 claims, each in its question's context, single-turn, 10 repeats, on Haiku. Four framings:
  - (a) impersonal, program 1's: "how likely is it that this statement is true";
  - (b) first person: "how confident are you that this statement is true";
  - (c) like-me other: "how confident would another AI assistant who read exactly this be";
  - (d) human other with the same evidence: "Sam has read exactly what you have read; how confident is Sam".

  Statistic: for each pair of framings, a Q-style ratio. That is the item-level R² of one framing predicting another, divided by each framing's split-half ceiling (as test F′), plus the mean shift.
- **Cost.** 6,400 calls ≈ $0.32 (cap $0.40).
- **Event and odds.** (a) and (b) are interchangeable: Q ≥ 0.90 and |mean shift| < 3 points. **P = 0.60.** Secondary: (d) is also interchangeable with (b), P = 0.45. Third-person framings are likely to hedge toward 50.
- **Why first.** If (a) ≈ (b), program 1's findings stand as self-report findings. They also become findings about the model's judgment in general, which is the seed hypothesis in its simplest form. If (a) ≠ (b), every later direction must use the first-person framing for "self".
- **Source.** E (from checking program 1's prompts), supported by L (D27, D29, D33, B17, B9).

### P2-2. Perspective-filter equivalence — rank 2

- **Assumption at stake.** Saying what another agent believes is a distinct third-person computation, not one's own world-judgment run on the other's evidence.
- **Who has looked.**
  - SymbolicToM (A7) gets large gains by rewriting "where does Bob think X is?" as "where is X?" over only the sentences Bob witnessed. That is an engineered pipeline, not a test of the bare model.
  - Aoki & Kawahara 2025 (B20) build exactly this "post-perspective-taking" story on BigToM (unseen events deleted, second-person story, first-person options). A linear map from third-person to first-person representations had a causal but small effect: best net flip about 0.23, about 40 test items, no confidence intervals.
  - ExploreToM (A15) finds shared-belief questions *harder* than divergent ones, so the bottleneck is reading state, not perspective.
  - Simulation theory (D28) and Gordon (D29) predict equivalence.
  - Nobody has compared graded credences item by item.
- **What our data say.** F2 and F3 say the model's judgment is a function of the transcript it reads. That predicts equivalence when the transcripts are matched.
- **Cheapest falsifying test.** BigToM Forward Belief (MIT licence). 200 templates × true/false belief. Two renderings:
  - (i) the full third-person story: "how likely is it that Noor believes X";
  - (ii) the filtered first-person story ("You …", unseen events deleted): "how likely is X".

  10 repeats each. Separate the two things Aoki changed at once with a 2 × 2 on 50 templates: {third person, first person} × {full, filtered}. Secondary arm: one question-order manipulation on both renderings, to see whether F1 transfers.

  Statistic: item-level Q of (i) against (ii) relative to the split-half ceilings, and the true- versus false-belief gap in each.
- **Cost.** About 12,000 calls ≈ $1.00 (cap $1.25).
- **Event and odds.** Q ≥ 0.80. **P = 0.55.** The failure mode that would make it miss is curse-of-knowledge leakage in (i), which (ii) removes by construction. That leakage is itself the P2-5 result.
- **Source.** L (A7, B20, A15, D28, D29).

### P2-3. SimpleToM decomposed: is the "stated but not used" gap a memory effect? — rank 3

- **Assumption at stake.** When a model states a character's mental state correctly but fails to predict the character's behaviour, it has a theory-of-mind deficit in *applying* the attribution.
- **Who has looked.**
  - SimpleToM (A10) reports mental-state / behaviour / judgment accuracy for three models: Claude-3.5-Sonnet 97.9 / 67.0 / 24.9, GPT-4o 95.6 / 49.5 / 15.3, Llama-3.1-405B 97.8 / 58.2 / 10.0.
  - Its "MS remind" puts the model's own mental-state question and answer in the prompt. Behaviour then rises to 96.9 / 82.8 / 89.5 for the same three, and Claude's judgment to 84.1.
  - FANToM (A5), Riemer et al. (A11) and Muchovej et al. (A17) find the same stated-versus-used dissociation in other forms.
  - Riemer's "social prompting" shows the model its own prediction and does *not* fix action, the opposite sign.
  - No one has hidden, falsified or reassigned the reminded answer (A10, "ours").
- **What our data say.** F2 (consistency is memory) and F3 (own record is a commitment, another's ignored) predict that MS remind works because the answer is the model's own and visible.
- **Cheapest falsifying test.** All 1,147 SimpleToM stories (ODC-BY licence), behaviour and judgment questions, on Haiku. Six conditions:
  1. not asked;
  2. filler turn;
  3. mental-state question asked, answer redacted;
  4. MS remind (own answer shown);
  5. planted *wrong* own answer;
  6. the same wrong answer credited to "another reader".

  Statistics:
  - the redacted share of the remind gain, R_MS = (3 − 1) / (4 − 1);
  - the difference in behaviour-answer agreement with the planted answer, (5) against (6).
- **Cost.** 13,764 calls ≈ $1.40 (cap $1.75).
- **Event and odds.** A wrong answer planted as the model's own moves behaviour answers toward it at least 10 points more than the same answer credited to another reader, with the CI excluding 0. **P = 0.70.** Secondary: R_MS < 0.5, meaning the record rather than the question carries the remind gain, P = 0.40. Program 1 found the question alone carried the order effect (R = 1.23), so a question-carried remind gain is quite possible.
- **Source.** L (A10, A11, A5, A17) + P1 (F2, F3).
- **Re-bet, 2026-11-04 (D8, `om-p2-3b`).** om-p2-3 stopped on a refusal at a severity-3 story. The re-bet asks the same question on severity 1–2 stories minus a 14-story keyword hold-out (581 stories), with a letter-copy guard added to the pass rule. Engine odds for it were revised before data by its lesson, **0.70 → 0.40** (program 2's 55–70% odds gave no clear hit; running base rate 0.27). The 0.70 above stays as om-p2-3's odds.

### P2-4. Interpersonal replication against program 1's ground truth — rank 4

- **Assumption at stake.** A model's account of its own judgment carries information beyond what it would infer for any similar agent. This is the assumption behind reading self-reports as introspection.
- **Who has looked.**
  - Nisbett & Wilson 1977 (D1): subjects' reports of what influenced them correlated .77–.99 with those of observers who read only a one-line description. Subjects were no more accurate. Their criterion is that a report counts as awareness only if it beats such an observer.
  - Bem 1967 (D2): observers told about "Bob" reproduced the dissonance pattern. Bem 1972 (D3): the simulation fails when the subject's earlier attitude is made salient to the observer, our shown-versus-redacted manipulation.
  - Song et al. 2025 (B9): no self-reflection advantage over same-model fresh-context or other-model prediction of temperature.
  - Binder et al. 2025 (B7): a fine-tuned self-prediction advantage, but none on the "Are you sure?" sensitivity property, the one closest to F3.
  - Patel et al. 2012 (D25): human actors beat observers on their own confidence.
  - No one has had ground truth for the model's order and memory effects to score against. We do, archived.
- **What our data say.** F5 (no privileged self-knowledge on error prediction). The measured F1–F3 numbers are the ground truth.
- **Cheapest falsifying test.** Take program 1's archived conditions:
  - bm0's 16 items at ±10/30/60, own source;
  - experiment 5's four orders on 40 items;
  - gm2b's shown versus redacted repeat.

  Present each one three ways:
  - (a) **self-prediction:** "if you were asked these questions in this order, what would your final rating be?", in a fresh context;
  - (b) **observer:** the same transcript, labelled as an AI assistant called Sam;
  - (c) **Nisbett–Wilson observer:** a one-line description of the manipulation only.

  Add a causal-report item: "how much did the earlier answer change the final rating, 0–100?". Statistics:
  - mean absolute error of the predicted uptake, order effect and repeat agreement against the measured values, per arm;
  - the correlation between arms (a) and (b) across conditions.
- **Cost.** About 5,000 calls with long prompts ≈ $1.00 (cap $1.25).
- **Event and odds.** Arm (a) is no more accurate than arm (b) (the CI of the error difference includes 0 or favours (b)), and (a) and (b) correlate r ≥ 0.7 across conditions. **P = 0.60.** The uninformative outcome to guard against is both arms at chance, as Nisbett & Wilson saw on most of their judgments. The pre-registration should require at least one outcome above chance before the comparison is read.
- **Source.** L (D1, D2, D3, B9, B7, D25) + P1.

### P2-5. Egocentric leakage: Carruthers's model 3 against model 4 — rank 5

- **Assumption at stake.** The model attributes beliefs by simulating from its own state, so its own credence leaks into what it attributes to an uninformed other (simulation, Carruthers's "metacognition is prior"). The alternative is that attribution reads only what the transcript says the other knows (model 4, "mindreading is prior").
- **Who has looked.**
  - Humans: Epley et al. 2004 (D12), anchoring and adjustment; Birch & Bloom 2007 (C13), a graded curse of knowledge, which Ryskin & Brown-Schmidt (C14) re-estimate at d = 0.20 with about 394 per cell needed; Krueger & Clement 1994 (D16), the within-person projection statistic; Tamir & Mitchell 2010 (D13), the item-level discrepancy regressor; Ames 2004 (D19), similarity switching between projection and stereotyping.
  - Language models: leakage is shown only qualitatively. FANToM's omniscient-view drift (A5), SimpleToM's snake (A10), Ullman's mover who "thinks" the cat is still in the basket at 99% (A2). Strachan et al. (A8) hypothesise the model has "no self-perspective" to inhibit.
  - No study has varied the model's own credence independently of the character's evidence (A, cross-cutting answer 3).
- **What our data say.** F3: a planted own answer moves the model's own rating. Whether it also moves the rating the model attributes to someone who never saw that answer is the discriminating question.
- **Cheapest falsifying test.**
  - (a) **Privileged information.** Birch & Bloom's four-container probabilities, which sum to 100. Conditions: Ignorance, Knowledge-Implausible, Knowledge-Plausible, plus Ryskin's no-knowledge control. 400 renders per cell with names, objects and container order counterbalanced.
  - (b) **Planted own answer, with Sam's evidence fixed.** 80 program-1 claims. The model's own earlier answer is planted at ±10/30/60. Then, in separate copies, the model gives its own rating and "the rating of Sam, who has read the same question but not your earlier answer". Statistic: the slope of the Sam rating on the planted displacement, against the slope of the own rating.
  - Target-similarity factor (Ames, Mitchell): Sam is "another instance of you" or "a person".
- **Cost.** About 6,400 calls ≈ $0.80 (cap $1.00).
- **Event and odds.** In arm (b), the Sam rating moves at least 0.10 points per point of planted displacement, with the CI excluding 0. **P = 0.30.** Secondary: in arm (a), Plausible minus Ignorance on the red container is at least 5 points with the CI excluding 0, a curse of knowledge on the graded scale, P = 0.70.
- **Source.** L (D12, C13, C14, D16, D13, D19, A2, A5, A8, A10, D4 for the model 3 vs 4 framing).
- **Bet, 2026-11-04 (D11, `om-p2-5`).** Arm (b) only, on program 1's bm0 vignettes, with a source-blind baseline in the run (the same displaced number as another reader's answer) that the own-answer pull must beat by 0.05, and a copy guard. Engine odds revised before data by its lesson, **0.30 → 0.33** (running base rate 0.375; held below it by the added margin and om-p2-3b's other-over-own pull). The 0.30 above stays as the map's odds for the map's event. Arm (a) is not run and stays open. Revised again before data by its design reviews (D12), **0.33 → 0.25**, for archive-calibrated power and an added "not inherited" conjunct.

### P2-6. Is "own" a position or a label? — rank 6

- **Assumption at stake.** Program 1's own-record commitment (F3) is about the *self*. The alternative is that it is about the *assistant-turn position* the model is continuing. A third possibility is the authorship *label*.
- **Who has looked.**
  - Program 1's own caveat: the own and other conditions differ in wording ("give your rating again" against "accept or revise") and in position (assistant turn against user message).
  - Panickssery et al. 2024 (B13): reversing the source label moves GPT-4's self-preference from 0.73 to 0.32 with content fixed.
  - Kumaran et al. 2025 (B18): on Gemma 3 12B, change of mind is 13.1% with the answer shown as the model's own against 32.5% hidden; with it credited to another LLM, 33.2% against 31.3%. The record flags one figure to check against the source.
  - Shanahan et al. 2023 (D34) and Andreas 2022 (B6): the model continues whichever character the context sets up, which predicts position.
  - Sharma et al. 2023 (B16): a *user's* stated belief moves the model strongly, so "other" splits by role.
- **What our data say.** F3, with the wording confound unresolved.
- **Cheapest falsifying test.** bm0's 16 items at ±30, one wording for every cell ("please give the rating again"), 40 conversations per cell. The value appears either in an assistant turn or in a user turn, labelled either "your earlier answer" or "Sam's earlier answer". A fifth cell is the user's own stated estimate. Statistic: uptake by cell; a label main effect and a position main effect.
- **Cost.** About 6,400 conversations ≈ $0.65 (cap $0.80).
- **Event and odds.** The label effect (own minus Sam, pooled over position) is at least 0.15 uptake, with the CI excluding 0, and larger than the position effect. **P = 0.35.** The engine leans toward position: the model is continuing the assistant turn whatever the label says.
- **Odds revised before data (2026-11-04, lesson `ls-om-p2-6`, pre-registration `experiments/p2-6-position-or-label.md`, D11):** 0.35 → **0.25**, both kept (`engine_odds_first` 0.35, `engine_odds` 0.25). Reason from the ledger: om-p2-3b (audited, stands) found a planted answer labelled as Haiku's own, in its own turn, pulling less than the same answer credited to another reader in the user turn; program 2 is 0 hits in 3 scored bets.
- **Source.** P1 (the caveat) + L (B13, B18, D34, B6, B16).
- **Replication, P2-6r (added 2026-11-04 23:45, before any Sonnet or Opus call; invariant 7).** Haiku's audited result was fail (position): position +0.23 [+0.13, +0.34] against label +0.08. Does that pattern hold on `claude-sonnet-5-5` and `claude-opus-5-5`? Same 16 items at ±30, the same four 2 × 2 cells and the no-value baseline (the fifth, user's-own cell is dropped for budget), 3 repeats on Sonnet and 2 on Opus (Opus 5.5 cannot turn thinking off, so its calls cost about 100 times Haiku's). Cost about $3.25, cap **$4.00** in code. **Event:** on *both* models, the position effect P ≥ 0.15 with its 95% item-bootstrap CI above 0, the shift-invariant P_s likewise, and P > |L|. **Engine odds 0.40**: near the running base rate (9/21 = 0.43), a little below it because the event is a conjunction over two models and stronger models may weigh the label more (program 1's DM4: Opus's final answer moved *away* from planted values). No human odds.

### P2-7. Shared format fingerprint — rank 7

- **Assumption at stake.** A credence attributed to another agent is a readout of a represented credence that formats merely express.
- **Who has looked.**
  - Format effects on attribution are large everywhere: Strachan's yes/no against "more likely" (A8); Riemer's LM / QA / CoT, 96.7 / 59.6 / 33.5 (A11); Trott's "thinks" against "goes to get" (A13, A14); FANToM's choice, free and list formats (A5).
  - No one has tested whether formats load on one latent attributed credence.
  - Bortoletto et al. (B2) find character-belief probes brittle where world-state probes are robust. That predicts attributions should be *more* format-dependent than self-reports.
  - Galesic et al. 2013 (D17): projection itself flips with format.
- **What our data say.** F4. The archived per-format self data on the same 80 claims exist for Haiku.
- **Cheapest falsifying test.** The 80 claims of the multi-model F arm, × six formats, × 10 repeats, for "Sam, who has read exactly this". Statistics:
  - Kendall's W for Sam against the archived self W (0.54);
  - the correlation between the per-claim-and-format deviations from one latent credence (the residuals of the one-credence model) for self and for Sam, relative to the split-half ceiling.
- **Cost.** 4,800 calls ≈ $0.24 (cap $0.30).
- **Event and odds.** The self and Sam residuals correlate at ≥ 0.5 of the ceiling. **P = 0.50.** Run after P2-1: if framing (d) is interchangeable there, this is likely; if not, less so.
- **Three-model version, P2-7 (added 2026-11-04 23:45, before any call).** Run on Haiku, Sonnet and Opus at once, cap **$1.50** in code. At that cap the map's design (4,800 calls a model) does not fit: Opus's archived format calls cost about $0.004 each. So: the three graded formats only (0–100 rating, frequency out of 100, verbal 7-point; the yes/no, bet and pairwise formats need many repeats per statement to show a per-statement deviation), 34 statements (2 drawn by the beacon from each of the 17 items all three models' archives share), 2 repeats, 204 calls a model, about $1.07. Self data come from the archives (program 1's gm3b and mm-gm3b, 10 repeats). **Event:** on every model whose residuals are reliable enough to test (at least two), the self–Sam residual correlation reaches 0.5 of its ceiling *and* beats a generic-link responder built from Sam's own answers (which shares no per-statement deviation) by at least 0.10, its CI above 0. **Engine odds 0.25**, below the running base rate (0.43) for named reasons: a conjunction over two or three models, a margin over a dumb baseline (P3), and Opus's formats nearly agree (Kendall's W 0.87), so its residuals are small. No human odds.
- **Source.** L (A8, A11, A13, A14, A5, B2, D17) + P1 (F4).

### P2-8. Order between self and other questions — rank 8

- **Assumption at stake.** The model computes another's belief independently of the view it has just stated, and its own view independently of the other's just-stated belief.
- **Who has looked.**
  - Le et al. 2019 (A6) put reality and belief questions on every story but never varied their order.
  - Street et al. (A9) varied response-option order, finding a large effect for PaLM and GPT-3.5 and none for GPT-4. They did not vary question order.
  - Strachan (A8, SI 3) reports item-position effects for GPT-3.5 only.
  - Samson et al. 2010 (C16) and Furlanetto et al. 2016 (C17) give the symmetric egocentric/altercentric intrusion design in humans.
  - Kovács et al. 2010 (C7) give the other-belief-affects-own crossing; Phillips et al. 2015 (C8) trace it to a timing confound, and their agent-free control is adopted here.
- **What our data say.** Asking is invasive in 5 of 6 families (program 1, test N). Another person's stated number is ignored (F3).
- **Cheapest falsifying test.** 200 BigToM stories rewritten so the world state is uncertain (the move is reported as hearsay). That keeps both ratings mid-scale and away from the ceiling that would otherwise manufacture the asymmetry. Conditions:
  - own-then-Noor;
  - Noor-then-own;
  - each alone, as copies;
  - the first answer shown or redacted;
  - an agent-free twin (a camera log) on 50 stories.

  5 repeats. Statistics: egocentric intrusion (Noor's rating moves toward own when own comes first) and altercentric intrusion (the reverse), each normalised by the room to move.
- **Cost.** About 6,000 calls ≈ $0.60 (cap $0.75).
- **Event and odds.** Egocentric intrusion exceeds altercentric by at least 3 points, with the CI excluding 0. **P = 0.50.**
- **Source.** L (A6, A9, A8, C16, C17, C7, C8) + P1 (test N).

### P2-9. Smarties versus Plasters — rank 9

- **Assumption at stake.** A model's report of its own past belief draws on more than its own recorded statements, i.e. on its earlier evidence and actions, as it would for someone else.
- **Who has looked.**
  - Gopnik & Astington 1988 (C2) and Wellman et al. 2001 (C4) report self/other parity over 235 matched conditions.
  - Sobel 2023 (C5) finds a small, reproducible age × question interaction.
  - Williams & Happé 2009 (C18): with the self question answerable only from an action (Plasters), autistic children score self 51.9% against other 69.2% (p = .02). Even typical children drop on self without the voiced statement (9 of 41 against 1 of 41).
  - Bernstein et al. 2007 (C15) supply the hindsight-memory design and the prior-confidence moderator.
  - No LLM work.
- **What our data say.** F2: repeat agreement is memory of the recorded answer.
- **Cheapest falsifying test.** About 120 deceptive-container items, templated from Kosinski's 20 unexpected-contents tasks (A1). The model's earlier evidence takes one of five forms:
  - a statement only ("I think it's crayons");
  - an action only (a tool call `open_box` made in order to fetch crayons);
  - both, consistent;
  - both, in conflict;
  - neither.

  Questions: "what did you think was inside", "what did you say was inside", and the same pair about Sam, given the same transcript with Sam as the actor. All on 0–100, 5 repeats. Statistic: the weight on the statement against the action, self against Sam, estimated from the conflict trials.
- **Cost.** About 9,000 calls ≈ $0.55 (cap $0.70).
- **Event and odds.** The statement weight for self exceeds that for Sam by at least 0.15, with the CI excluding 0. **P = 0.45.** Secondary: with the action only, self accuracy is at least 10 points below Sam's (the Plasters profile), P = 0.30.
- **Source.** L (C2, C4, C5, C18, C15, A1, C20) + P1 (F2).

### P2-10. Shared code inside an open-weight model — rank 10

- **Assumption at stake.** First-person and third-person beliefs are encoded in separate representations.
- **Who has looked.**
  - Zhu et al. 2024 (B1) and Bortoletto et al. (B2) find separate, differently robust directions for the "oracle" and the protagonist. But their "self" is the true world state, so self and fact are confounded, and neither paper computes a cosine or cross-perspective transfer.
  - Prakash et al. 2025 (B3) describe protagonist belief as pointer "lookbacks" into the transcript.
  - Aoki & Kawahara (B20) find small partial overlap.
  - Carauleanu et al. (B15) report a self–other activation distance with no other–other baseline.
  - Baez et al. 2026 (B22, abstract only) give cross-condition probe transfer as the shared-versus-separable statistic.
  - Chen et al. 2024 (B19) show the model's verbal account of its user diverging from its internal user model, the third-person counterpart of program 1.
- **What our data say.** Program 1's own probe dissociation test (gold-map direction 5) is running on the same laptop pipeline. Its outcome decides whether this direction is buildable.
- **Cheapest falsifying test.** On Llama-3.1-8B-Instruct or Qwen2.5-7B-Instruct, build matched items whose content is identical across perspectives: "I believe the milk is in the cup" and "Noor believes the milk is in the cup". The model's own belief should differ from the truth on some items, through a planted earlier answer, to break the self = truth confound. Then:
  - (i) train a probe on one perspective and test it on the other;
  - (ii) run Aoki's 2 × 2 with bootstrap CIs;
  - (iii) compare self–other distance against other–other distance (two named characters);
  - (iv) apply Jamali's question-only and word-shuffle controls (B5).
- **Cost.** $0 API; CPU hours.
- **Event and odds.** Cross-perspective probe accuracy is at least 0.80 of within-perspective accuracy, in both directions, at the best layer. **P = 0.40.**
- **Source.** L (B1, B2, B3, B20, B15, B22, B19, B5).

### P2-11. Self-informed belief induction (goggles) — rank 11

- **Assumption at stake.** In attributing what another agent can know, the model treats its own first-hand experience as privileged over the same experience reported for someone else.
- **Who has looked.**
  - Meltzoff & Brooks 2008 (C22): infants' own blindfold experience, in both directions.
  - Kano et al. 2019 (C23): great apes. Furlanetto et al. 2016 (C17): adults' altercentric intrusion appears only after first-hand see-through goggles.
  - Heyes 2014 (C26) proposed this design as the control against submentalising.
  - Meltzoff & Brooks leave open whether *observing* another use the blindfold would substitute for one's own experience. That is our own-versus-other comparison.
- **What our data say.** F3 concerns answers, not evidence. Whether own *experience* gets the same priority as own *answers* is untested.
- **Cheapest falsifying test.** 60 items with a novel filter. The model learns whether it is see-through in one of four ways:
  - (a) its own tool call returns readable or unreadable text;
  - (b) another agent's log shows the same;
  - (c) a stated rule;
  - (d) an inanimate camera's record.

  Then it rates what an agent behind the filter believes. A cloned-branch manipulation check ("could you read through it?") costs nothing to the main branch. 10 repeats.
- **Cost.** About 4,800 calls ≈ $0.40 (cap $0.50).
- **Event and odds.** Transfer from (a) exceeds transfer from (b) by at least 10 points, with the CI excluding 0. **P = 0.25.** The engine expects any evidence in the transcript to count the same, whoever's experience it is.
- **Source.** L (C22, C23, C17, C26).

### P2-12. Social-relations round robin across models — rank 12

- **Assumption at stake.** Some self-knowledge advantage remains once rater skill and target readability are removed.
- **Who has looked.**
  - Kenny's social relations model, and Kwan et al. 2004 (D35): the self-rating minus perceiver and target effects.
  - Ashuach et al. 2026 (B10): a small self-probe premium appears only on items where the models disagree (+0.015 to +0.034 AUC, factual recall only).
  - Song, Hu & Mahowald 2025 (B8): no self effect across 21 open models once similarity is controlled.
  - Vazire 2010 (D10): the self wins on low-observability traits.
- **What our data say.** F5 in a 2 × 2. The round robin adds target and relationship effects, such as a same-family "similar other" advantage (D21, D19).
- **Cheapest falsifying test.** Haiku, Sonnet and Opus each author answers and confidences on 100 hard-pool questions, 3 repeats. Each then predicts every model's confidence and correctness, including its own in a fresh context. Statistics: social-relations decomposition; the Kwan self-effect; disagreement-subset scoring.
- **Cost.** $6–10 at batch rates (cap $10).
- **Event and odds.** A positive self-effect, with the CI excluding 0. **P = 0.15.**
- **Source.** L (D35, B10, B8, D10, D21, D19) + P1 (F5).

### P2-13. A self-authorship direction as the mechanism of own > other — rank 13

- **Assumption at stake.** The own − other uptake gap reflects belief, not a source tag the model attaches to text.
- **Who has looked.** Ackerman & Panickssery 2025 (B14) found a causal self-recognition direction in Llama3-8b-Instruct. Its Tuned-Lens poles are "my/I" and "their/other", and projecting it out cuts self-claims by 50–60%. Kumaran (B18) shows the own/other gap on Gemma 3 12B. Lindsey 2026 (B11) found that prefilled outputs are disavowed unless the concept is injected beforehand, which is a source-monitoring check.
- **What our data say.** F3 on Claude; not yet on any open model.
- **Cheapest falsifying test.** Gate: replicate the own − other planted-answer gap on Llama-3-8B-Instruct with bm0's design and logit-based ratings. If the gate passes, project out the self-recognition vector at the planted turn and re-measure the gap.
- **Cost.** $0 API; CPU hours.
- **Event and odds.** The gate passes and projection shrinks the gap by at least half. **P = 0.20** (about 0.6 for the gate × about 0.3 given the gate).
- **Source.** L (B14, B18, B11) + P1 (F3).

---

## Carruthers's four models, as observables on these tests

| model (D4) | what it predicts here | already against it |
|---|---|---|
| 1. Two mechanisms (self-monitoring separate from mindreading) | some edits hurt self-attribution only and others other-attribution only (P2-3, P2-9); separable probe directions (P2-10) | — |
| 2. One faculty, two modes of access | self ≥ other on every item; positive judge × author or self-effect (P2-4, P2-12) | F5: I = −0.055 |
| 3. Metacognition prior (simulation) | own credence leaks into attributions, more for similar targets (P2-5); attribution follows own planted answer | needs privileged self-access, which F5 did not find |
| 4. Mindreading prior (self-interpretation) | label-symmetric uptake (P2-6); self-prediction ≈ observer (P2-4); perspective-filter equivalence (P2-2); confabulated uptake of planted "own" answers | F3's planted-answer uptake is its signature prediction |

## Next steps extracted from the reads, and what the filter did with them

"On map" means the step became, or was folded into, a direction. "Standing control" means it is applied across directions. "Parked" means it is kept, not run now, for the stated reason. "Killed" means it does not transfer, for the stated reason. Nothing is deleted.

| next step (source) | verdict |
|---|---|
| Hide, plant and reassign SimpleToM's MS-remind answer (A10) | on map, P2-3 |
| Filtered-transcript equivalence (A7), Aoki 2 × 2 (B20) | on map, P2-2 (behaviour); P2-10 (internals) |
| Graded 0–100 attributed credence on existing items (A1, A8, A13) | on map, P2-2, P2-5, P2-8 |
| Vary the model's own prior separately from the character's evidence (A, gap 3; D12) | on map, P2-5 |
| Observer arm and the "beat the observer" criterion (D1, D2, D3) | on map, P2-4 |
| Same-model fresh-context arm (B9, D32) | on map, P2-4 arm (a) |
| Extrospective control; ascent routine (D33, D29, D27) | on map, P2-1 |
| Label reversal with content fixed (B13); user against bystander roles (B16) | on map, P2-6 |
| One-latent test across formats for attributions (A5, A8, A11) | on map, P2-7 |
| Reality and belief question order (A6, A9); egocentric and altercentric intrusion (C16, C17); P × A crossing (C7) | on map, P2-8 |
| Smarties against Plasters; "say" against "think" (C18, C2) | on map, P2-9 |
| Hindsight twin with feedback-after control and prior-confidence moderator (C15) | on map, P2-9 secondary; P2-5 arm (a) later |
| Self-experience then attribute (C22, C23, C17, C26) | on map, P2-11 |
| Cross-perspective probe transfer; break self = truth (B1, B2, B22) | on map, P2-10 |
| Social-relations round robin; truly-false-consensus statistic (D35, D16); disagreement subset (B10) | on map, P2-12 |
| Self-authorship direction as mediator (B14, B18) | on map, P2-13 |
| Agent-free or inanimate twin for every other-belief effect (C8, C26) | standing control in P2-5, P2-8, P2-11 |
| Power simulation before claiming a self/other null (C5, C14) | standing rule: every null claim needs a pre-registered power check |
| Model strength as the analogue of age; test the question × strength interaction (C4, C5) | standing: any hit replicates on Sonnet and Opus (invariant 7) |
| Staging: knowledge and ignorance before false belief; does the model mark its own ignorance first? (C11, C25) | parked; add as a stage to P2-8 or P2-9 once they run |
| Signature-limit identity items against location items (C12) | parked; add a family to P2-9 if it hits |
| Similarity of target (C19 / D19, D21) | folded into P2-5 as a factor |
| Many-persona leakage of a planted disposition (B12, in-context version) | folded into P2-5 arm (b) |
| Fine-tuned self-prediction against cross-prediction (B7); fine-tuned dispositions (B12) | parked: no fine-tuning access on Claude; possible later on the open model |
| Concept injection with an other-agent arm (B11) | parked until P2-10 shows the laptop pipeline works |
| Fisher-mask overlap between first-person, third-person and own-record tasks (B4) | parked until P2-10 |
| Probe-versus-verbal gap for self and user (B19) | parked until P2-10 |
| Lookback patching of the planted-answer owner tag (B3) | parked: shown at 70B; needs confirming at 7–8B first |
| Verbal 0–100 against log-odds on Trott's 192 passages (A13, A14) | parked; natural second item set for P2-10 |
| Forward and inverse attribution consistency with the other answer hidden or shown (A17) | parked; second item set for P2-3 if it hits |
| Sentence-by-sentence belief trajectory (A1, A16) | parked; A16's data not yet public |
| Order-1 "self" rung on higher-order ToM items (A9) | parked; MoToMQA is available on request only |
| Literal against functional ToM in repeated games (A11) | parked: multi-turn games are expensive; the format effect is kept in P2-7 |
| FANToM's long multi-party conversations (A5) | parked: long contexts; its six question types are a later P2-7 item set |
| Dual-task load and confidence calibration (D5) | parked: "load" is not well defined for a model |
| Coding explanations for belief against desire reasons, own against other (D11) | parked: coding, not a graded test |
| Confidence matching with a partner over turns (D26) | parked; a follow-up to P2-6 |
| Item-level self/other discrepancy as a regressor (D13) | folded into P2-5's analysis |
| Self-model projection from answer features (D25) | parked |
| Looking-time and reaction-time measures (C6, C7, C9, C10, C24) | killed: no model analogue; the crossed designs were kept |
| Jamali's per-dimension test (B5) | killed: about 5% of dimensions should pass by chance with no correction; its controls are kept in P2-10 |
| Autism-specific inferences (C19, C20, C21) | killed as inferences; the lesion logic is kept as ablation in P2-10 and P2-13 |

## Notes for the engine

- **Path dependence (Q4).** This map is not independent of program 1. Its instruments, its fingerprint and several of its directions come from program 1's results and caveats. Any comparison of the two programs' maps should treat program 2 as seeded *by* program 1, not as a second independent seed.
- **Hardware.** No direction here found a use for the quantum hardware. That question stays open, as Sean asked, not closed.
- **Items and licences.** SimpleToM is ODC-BY; BigToM is MIT; FANToM is MIT for evaluation only; Strachan's battery and ExploreToM are CC-BY-NC 4.0. Kosinski's tasks are on OSF and their data licence was not checked. Use within the licence; the pre-registration names the licence of every item set.
- **Read-depth debts before any paper cites these.** Several important sources were seen only through secondary descriptions or abstracts:
  - Birch & Bloom 2007; Gopnik & Astington 1988, whose direction of self/other difference is disputed between Wellman and Sobel;
  - Kovács et al. 2010; Krueger & Clement 1994; Nickerson 1999 (not obtained);
  - Lombardo et al. 2010; Baez et al. 2026; Cheng et al. 2026.

  The Kumaran attribution figure flagged in B18 needs checking against the source.
