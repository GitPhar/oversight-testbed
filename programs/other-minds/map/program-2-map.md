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
- **Odds revised before data (2026-11-05, lesson `ls-om-p2-6r`, pre-registration `experiments/p2-6r-replication.md`, D14):** 0.40 → **0.25**, both kept (`engine_odds_first` 0.40, `engine_odds` 0.25). Reason from the archive: in program 1's DM4 a planted earlier answer pulled the next rating 0.46 (Sonnet) and 0.15 (Opus) as much as on Haiku, and the dry run passes about 0% if uptake halves.

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
- **Odds revised before data (2026-11-05, lesson `ls-om-p2-7`, pre-registration `experiments/p2-7-format-fingerprint.md`, D15):** 0.25 → **0.20**, both kept. Reason: in the dry run Opus held in 2 of 60 runs where Sam is hedged toward 50, and P2-1 found Haiku's Sam framing shared only 0.67 of its reproducible item variation with "how confident are you". Sean's cockpit odds for P2-7 (70%, for the map's original event) arrived 2026-11-05 05:11 and are copied into the bet. Revised again before data by the design review (D15a), **0.20 → 0.15**: a flat Sam now fails instead of dropping out, and on the beacon draw Opus holds 0 of 60 hedged-Sam dry runs.
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

## Follow-ups (remap 2026-11-05)

Written 2026-11-05 04:45 America/Denver by the remap session (`operators/remap.md`), from every settled result in `ledger/bets.jsonl` and its audit, before any data for these directions. Nothing was run, pre-registered or called. Each follow-up's odds are the engine's P(pass) for the draft event, stated in one pass in id order before ranking, not in fresh v1 contexts: the betting session re-elicits under v1 before pre-registration (`operators/learn.md`). API follow-ups are costed on `claude-haiku-5-5`, `claude-sonnet-5-5` and `claude-opus-5-5` (CONTEXT.md §3 rule 12) unless the row says why not. Sean's question for each is on its cockpit card; `map/remap-2026-11-05-odds-form.md` lists them shuffled, without these odds.

### In plain English

Nothing in program 2 landed: six scored bets, six misses, and one untestable (a refusal). Only P2-4 came back undetermined, which the remap counts as mixed. Its two follow-ups are the auditor's larger re-run with a margin fixed in advance (P2-14, about $3.50 on the three models) and a free check that its predictions beat a guess of 'no effect' (P2-15). Three of the misses turned up effects running the other way from the bet (own answer pulled less than another reader's; Sam followed the planted answer more than the model did; the turn mattered more than the label). They stay killed. Two of them get an optional lead from their audit's cheapest test (P2-16, P2-17), labelled post hoc. Program 2 did not stop for lack of directions: P2-7 to P2-13 are still open and untried, and P2-6r is mapped above.

### Follow-ups

| id | grows from | direction | models | cost | engine P(pass) |
|---|---|---|---|---|---|
| P2-14 | P2-4, bet `om-p2-4` | Does the model predict its own quirks any better than an observer's, with enough repeats and a margin fixed in advance? | Haiku, Sonnet, Opus | about $3.50 (Haiku $0.15; Sonnet about $1.80; Opus about $1.50) | 20 |
| P2-15 | P2-4, bet `om-p2-4` | Do the model's predictions of its own quirks beat a predictor that expects no quirk at all? | archive: Haiku | $0 (archive) | 55 |
| P2-16 | P2-6, bet `om-p2-6` | Lead (post hoc): is 'position over label' about the turn, or about the message structure around the value? *(lead, post hoc)* | Haiku, Sonnet, Opus | about $3.70 (Haiku $0.25; Sonnet about $0.80; Opus about $2.60) | 40 |
| P2-17 | P2-5, bet `om-p2-5` | Lead (post hoc): is 'Sam follows the planted answer more than the model does' just the wording of the self question? *(lead, post hoc)* | Haiku, Sonnet, Opus | about $3.50 | 45 |

Test, event and the reason for each number:

- **P2-14.** *Test:* om-p2-4's arms (a) self and (b) observer on the 192 own-source uptake cells only; Haiku 10 repeats, Sonnet 3, Opus 1 on half the cells; own-uptake block difference in error with BCa intervals and a +/-0.05 equivalence margin. *Event:* On Haiku, the BCa 95% interval of the own-uptake difference in error (self minus observer) lies inside +/-0.05: the model reads itself like a stranger. Sonnet and Opus reported. *Odds 20:* The audit's cheapest overturning test (om-p2-4 audit). The first run's point estimate was self error about half the observer's (0.054 against 0.097, a difference of -0.043), so an interval inside +/-0.05 needs the estimate to shrink toward 0. Program 2 is 0 hits in 6 scored bets. Well below the running base rate 8/19 = 0.42 (ledger/brier.md).
- **P2-15.** *Test:* Archive only: om-p2-4's committed predictions; compare self-prediction error with an always-no-uptake predictor, BCa interval. *Event:* On Haiku, self-prediction error on the uptake cells is below the always-no-uptake predictor's, BCa 95% upper bound of the difference below 0. *Odds 55:* The audit showed the gate and r bar were met by a know-nothing predictor, which is a warning; but self error (0.054) is small, and the measured uptake (0.21-0.71 on own cells) is far from zero, so a no-uptake guess should do badly there. Above the running base rate 8/19 = 0.42 (ledger/brier.md).
- **P2-16.** *Test:* om-p2-6's 16 items at +/-30 with the message structure matched in both positions, plus a cell quoting the value as the assistant's earlier output; Haiku 20 repeats, Sonnet 3, Opus 2. *Event:* On Haiku, with the message structure matched, the position effect falls below 0.10 (from +0.23), 95% item-bootstrap upper bound below 0.15. *Odds 40:* The audit of om-p2-6 names this as the cheapest test that could overturn 'position over label'. Message structure is a live rival: the user-position value sat inside the request turn. But the assistant-turn role marker may carry the pull by itself. Near the running base rate 8/19 = 0.42 (ledger/brier.md); program 2's 0 of 6 argues lower.
- **P2-17.** *Test:* om-p2-5's design with the self question reworded to match Sam's, plus a recall question ('what rating did you give earlier?'); Haiku 20 repeats, Sonnet 3, Opus 2. *Event:* On Haiku, with matched wording, the Sam-minus-own uptake gap falls below 0.05 (from +0.14), 95% item-bootstrap upper bound below 0.10. *Odds 45:* The om-p2-5 audit names this rival and its test. Wording effects are large in this family (om-p2-1: framing moved 18 of 160 claims by over 30 points), which favours it. But the gap came mostly from upward plants, which wording alone may not explain. Near the running base rate 8/19 = 0.42 (ledger/brier.md).

### Killed or untestable: what each rules out

| direction | bet(s) | rules out |
|---|---|---|
| P2-1 | `om-p2-1` | Rules out, on Haiku and program 1's 160 claims, that 'how likely is this true' and 'how confident are you' are interchangeable: they share about 77% of reproducible item variation, below the 90% bar. |
| P2-2 | `om-p2-2` | Rules out, on Haiku and BigToM stories, that attributing Noor's belief is just judging the world from her filtered evidence: the two share about half the item variance, almost none within condition. |
| P2-3 | `om-p2-3`, `om-p2-3b` | Rules out, on Haiku and 581 lower-severity SimpleToM stories, that the 'stated but not used' gap is memory of the model's own answer: a planted own answer pulled less than another reader's (om-p2-3 itself was untestable: a refusal). |
| P2-5 | `om-p2-5` | Rules out, on Haiku and program 1's 16 vignettes, that a planted own answer reaches Sam's rating only through the model's own revised view: Sam's rating followed it more (+0.14). |
| P2-6 | `om-p2-6` | Rules out, on Haiku and program 1's 16 items at +/-30, that the 'yours' label carries the own-answer pull: the label added +0.08, the assistant-turn position +0.23. |
| P2-15 | `om-p2-15` | Rules out, on Haiku and om-p2-4's 324 archived uptake cells, that its self-predictions beat a no-effect guess cell by cell (+0.33 rating points, [−3.08, +4.07]); they beat it on own-answer cells and lose on another person's number (audit `ledger/audits/om-p2-15.md`). |
| P2-5r | `om-p2-5r` | Rules out, on Sonnet 5.5 and Opus 5.5 and program 1's 16 vignettes at 2 repeats, that the rating attributed to Sam moves further toward the model's planted answer than its own re-rating, in either direction (both read none; audit `ledger/audits/om-p2-5r.md`). |
| P2-14 | `om-p2-14` | Rules out, on Haiku and program 1's 16 vignettes at 10 predictions per cell, that the 'you' and 'Sam' labels predict its own-answer pull equally well (within ±0.05): the self label was more accurate by 0.185 [−0.282, −0.087], because the Sam label predicts about 6 points more pull than happens; Sonnet and Opus undetermined (audit `ledger/audits/om-p2-14.md`; Novelty partly new). |
| P2-path | `om-p2-path`, `om-p2-path2` | Rules out nothing about path dependence: both bets were withdrawn before any tag (D19a, D21b). By a fresh origin coding, 11 of the engine's 17 recorded traps were already in program 1's pre-gate work, so program 2's failures cannot be tied to program 1's traps rather than to the generic ones every program shares; a test needs an origin-specific pattern list or two seeds run in parallel. |

## Prior work lines (rule 13, added 2026-11-05)

Written in the backward pass of 2026-11-05 (`paper/informed-engine.md`) by a fresh claude-fable-5-1 subagent that read this program's reads and opened every paper it cites that the reads do not already quote with numbers; the search behind each line is in `map/other-minds.json` (`prior_work_search`, `prior_work_sources`). Each line says what the nearest published work predicts for the direction's draft pass rule, on which models, and what the bet would add, or that no prior statement was found after a named search. From here on every new direction gets its line from the scout or the remap (`operators/scout.md` Step 4; `operators/remap.md` Step 2), and the design review checks it (D12).

| id | prior work predicts | Prior work |
|---|---|---|
| P2-1 | mixed | Philosophy (Gordon 1986; Schwitzgebel 2008; no data) predicts pass: confidence in p is read off a judgment of p. LLM work predicts fail: Kim and Kang 2026 (arXiv 2605.27752, five open LLMs) find instruction wording the main driver of stated-confidence shifts; Suzgun et al. 2024 (arXiv 2410.21195; GPT-4, Claude 3, Llama 3) score first-person belief items 54.4% against 80.7% third-person. Settled om-p2-1: fail, Q 0.77 on Haiku. |
| P2-2 | fail | Predicts fail, partial overlap. Aoki and Kawahara 2025 (IJCNLP-AACL SRW; Llama-3.1-70B, Qwen2.5-72B): mapping third-person onto filtered first-person representations flips at most 0.23 net on about 40 items. Wilf et al. 2023 (arXiv 2311.10227; Llama-2, GPT-3.5, GPT-4): filtering to what the character knows raises false-belief accuracy 3 to 62 points, so the two readings differ wherever filtering helps. Settled om-p2-2: fail, Q 0.50 on Haiku. |
| P2-3 | pass | Predicts pass. Kumaran et al. 2025 (arXiv 2507.03120, Gemma 3 12B): change of mind 13.1% with its own answer shown against 32.5% hidden; the same answer credited to another LLM gives 33.2% against 31.3%, no effect. SimpleToM (Gu et al. 2024, arXiv 2410.13648): showing the model its own mental-state answer lifts GPT-4o behaviour accuracy 49.5 to 82.8. Settled om-p2-3b: fail, reversed; the other-credited answer pulled more (Δ −0.053) on Haiku. |
| P2-4 | pass | Predicts pass. Nisbett and Wilson 1977 (DOI 10.1037/0033-295X.84.3.231): observers given one-line descriptions matched subjects' reports at .77 to .99 and were no less accurate. Blandfort and Pawar 2026 (arXiv 2609.09899): self-report predicts own behaviour at r +0.04; other models' self-answers predict a target at least as well. Xiao et al. 2025 (arXiv 2509.24988): self-correctness prediction no better than an unrelated LLM. om-p2-4: undetermined (self 0.054, Sam 0.097). |
| P2-5 | pass | Predicts pass. Choi, Hong and Kim 2024 (arXiv 2407.12007; GPT-4, Claude 3 Opus, Llama 2 70B, Mixtral): an option inserted as the model's own choice shifts its estimate of peers choosing it by 0 to 40.5 points (Claude 3: 0 to 25.5), below Ross et al. 1977's 17 to 21.5. No self re-rating or third-party arm. om-p2-5: Sam moved 0.50, map's event met, frozen rule failed (Sam exceeded own, +0.14). |
| P2-6 | mixed | Mixed. Khullar et al. 2026 (arXiv 2603.04582; Claude 3.5 Haiku, Sonnet 4, Opus 4.1 among ten): explicit authorship labels move scores under 0.5 of 10, while the artefact's transcript position cuts monitor AUROC 0.99 to 0.92, predicting fail. Panickssery et al. 2024 (arXiv 2404.13076): reversing the source label moves GPT-4 self-preference 0.73 to 0.32, predicting pass. Settled om-p2-6: fail, position +0.23, label +0.08 (Haiku); neither on Sonnet or Opus. |
| P2-7 | fail | No published test of a shared format fingerprint. Nearest work leans fail: Bortoletto et al. 2025 (arXiv 2406.17513; Pythia, Llama-2) find character-belief probes brittle under prompt changes where world-state probes hold near 95%, so attributions should carry their own format quirks; Riemer et al. 2025 (arXiv 2412.19726, Mixtral): one prediction scores 96.7, 59.6 or 33.5 by format. Settled om-p2-7: fail, 0.21, −0.10, 0.24 of ceiling on Haiku, Sonnet, Opus. |
| P2-8 | pass | No LLM paper varies self and other question order. Nearest work predicts pass: Furlanetto et al. 2016 (JEP:HPP 42, 158; 17 adults) find egocentric interference (614 against 748 ms) larger than altercentric (579 against 621 ms); Choi, Hong and Kim 2024 (arXiv 2407.12007): a planted own choice shifts four LLMs' estimates of others by up to 40 points, while program 1 found another's stated number ignored (uptake about 0.02). |
| P2-9 | pass | No LLM test of own past belief against an action. Children predict pass: Williams and Happé 2009 (DOI 10.1007/s10803-009-0695-6): with the belief shown only by an action, autistic children score self 51.9% against other 69.2% (p = .02); 9 of 41 typical children pass the voiced self question but fail the acted one. Suzgun et al. 2024 (arXiv 2410.21195; GPT-4, Claude 3, Llama 3): first-person false beliefs 54.4%, third-person 80.7%. |
| P2-10 | fail | Predicts fail, partial overlap. Aoki and Kawahara 2025 (IJCNLP-AACL SRW; Llama-3.1-70B, Qwen2.5-72B): a linear map from third-person to first-person belief representations flips at most 0.23 net, 'relatively small compared to the ideal value of 1', about 40 items. Zhu et al. 2024 (arXiv 2402.18496, Mistral-7B) and Bortoletto et al. 2025 (arXiv 2406.17513) put oracle and protagonist beliefs in different heads, but 'self' there is the world state; no transfer computed. |
| P2-11 | unknown | No prior statement found for LLMs after searching arXiv and the web for first-hand versus observed experience in belief attribution. Human and ape work predicts that own experience transfers: Meltzoff and Brooks 2008 (DOI 10.1037/a0012888, 168 infants; trick blindfold raised gaze following 0.33 to 1.04) and Kano et al. 2019 (DOI 10.1073/pnas.1910095116, 47 apes). Meltzoff and Brooks leave untested whether observing another's experience substitutes, which is this direction's comparison. |
| P2-12 | fail | Predicts fail. Song, Hu and Mahowald 2025 (arXiv 2503.07513, 21 open models): no self effect once model similarity is controlled; seed variants show none (p > .25). Ashuach et al. 2026 (arXiv 2604.12373; Llama-3.1-8B, Qwen2.5-7B, Gemma-2-9B): a self-probe premium only on disagreement items, +0.015 to +0.034 AUC, factual recall only. Blandfort and Pawar 2026 (arXiv 2609.09899): other models' self-answers predict a target at least as well. No round-robin decomposition published. |
| P2-13 | mixed | Mixed. Gate likely: Kumaran et al. 2025 (arXiv 2507.03120, Gemma 3 12B) find the own-answer effect vanishes when credited to another LLM. Mediation unlikely: Ackerman and Panickssery 2025 (arXiv 2410.02064, Llama3-8b-Instruct) show projecting out the self-recognition vector cuts authorship claims 50 to 60%, but Khullar et al. 2026 (arXiv 2603.04582) and Tsui 2025 (arXiv 2507.02778) locate the own-output bias in transcript position and a conversational-role direction, not an authorship tag. |
| P2-path | pass | Predicts pass, by analogy only. Trehan and Chopra 2026 (arXiv 2601.03315): six failure modes recur across four autonomous ML research attempts on different topics. Fei et al. 2026 (arXiv 2608.14905): 45 failure patterns recur across all 8 harness-model combinations on 100 tasks in 7 domains, blamed on the model, not the scaffold. Neither runs one engine from two seed questions or classifies blind; no published number for the expected share. |
| P2-14 | pass | Predicts pass. Blandfort and Pawar 2026 (arXiv 2609.09899): self-report predicts own behaviour at r +0.04; other models' answers predict a target at least as well. Binder et al. 2025 (arXiv 2410.13787): no self-advantage on the 'Are you sure?' property, Llama 70B self 74.5% against GPT-4o 76.5%. Xiao et al. 2025 (arXiv 2509.24988): self-correctness prediction no better than an unrelated LLM. om-p2-4 ran the other way (self 0.054, Sam 0.097; undetermined). |
| P2-15 | unknown | No prior statement found for this comparison after searching arXiv for LLM self-prediction scored against a no-effect baseline. Nearest: Blandfort and Pawar 2026 (arXiv 2609.09899) find showing the exact items lifts self-prediction to r +0.24, barely above a generic AI-agent question (+0.28); Kumaran et al. 2025 (arXiv 2507.03120) put own-answer uptake in print, so a transcript reader need not predict none. om-p2-4's archive: self arm 0.71/0.42/0.22 against measured 0.71/0.44/0.21. |
| P2-16 | fail | Predicts fail. Tsui 2025 (arXiv 2507.02778; 14 open models, Claude 3.5 Haiku 52.5%, Claude Sonnet 4 41.4% blind spot): content and context identical, only the chat-template role header differs, and a conversational-role direction steers correction monotonically, though role and turn position were not separated. Khullar et al. 2026 (arXiv 2603.04582): a prefilled previous assistant turn cuts monitor AUROC 0.99 to 0.92, labels inert. om-p2-6r: no position effect on Sonnet, Opus. |
| P2-17 | unknown | No prior statement found on a Sam-minus-own gap after searching arXiv for false consensus and self re-rating in LLMs. Choi, Hong and Kim 2024 (arXiv 2407.12007) measure the pull on others (0 to 40.5 points, four LLMs) but never re-elicit the model's own answer. Kim and Kang 2026 (arXiv 2605.27752): instruction wording drives stated-confidence shifts, which favours the wording rival. om-p2-5: gap +0.14, from upward plants only. |

## Known or new (rule 13)

Every landed or mixed bet of this program carries a Novelty line in its results file and ledger row (`novelty`, `novelty_line`): 2 partly new. A known result keeps its verdict and score; the word says what it is evidence of.

| bet | direction | ledger verdict | novelty | the line |
|---|---|---|---|---|
| om-p2-4 | P2-4 | undetermined | **partly new** | Binder et al. 2024 (arXiv 2410.13787) report that a finetuned model predicts its own behaviour better than a second model trained on the same facts, while Song, Hu and Mahowald 2025 (arXiv 2503.07513) and Blandfort and Pawar 2026 (NeurIPS 2026 AI4GOOD workshop) find no self-specific advantage by prompting; our prompt-only "you" versus "Sam" contrast on anchoring effects is undetermined, leaning self. That models misreport what moved their answers is in print (Turpin et al. 2023, arXiv 2305.04388; Chen et al. 2025, arXiv 2505.05410), but no paper states that reported anchor influence runs opposite to measured uptake, the same under self and other labels. Search: WebSearch for "LLM self-prediction vs other-model prediction introspection", "self-report anchoring influence LLM", "Nisbett Wilson 1977"; arXiv abstract pages for each lead. |
| om-p2-5 | P2-5 | mixed | **partly new** | The manipulation is in print: Choi, Hong and Kim (2024, arXiv 2407.12007; NAACL Findings 2025) fed GPT-4, Claude 3 Opus, Llama 2 70B and Mixtral one option as the model's own choice and found its estimate of how many peers would choose it shifted, by 20 points on Claude 3 Opus in one story (a false-consensus effect, generally smaller than in Ross et al. 1977's human data). They did not compare the pull on others with the pull on the model's own re-rating, and showed no third party's number for contrast. Ours found the prediction of another mind moved more than the model's own answer (0.50 against 0.36 of the way; a third party's number 0.02), with the excess coming from upward plants only, so it may be a scale artefact. Search: paper/novelty.md, 2026-11-05 (arXiv searches on false consensus in LLMs, egocentric projection, self-other anchoring), by a claude-fable-5-1 session on the novelty-check branch (93f47af); carried here by the informed-engine session. |

## Follow-ups (remap 2026-11-05c)

*Written 2026-11-05 by a fresh remap session (claude-opus-5-5) that ran none of program 2's bets; re-scouts by a fresh reader subagent; odds by fresh blind contexts (rule 14).*

**What came back.** No new program 2 result landed; two mixed nodes had only one not-yet-run follow-up each. P2-4 (om-p2-4, undetermined): Haiku's predictions of its own uptake had about half the error of its predictions for "Sam", but the test could not see an advantage that small; P2-15 then found its self-predictions scattered about twice too far on another person's number. P2-5 (om-p2-5, mixed): on Haiku a planted own answer pulled the rating it gave for Sam more than its own re-rating, which did not replicate on Sonnet and Opus with Haiku's anchors (om-p2-5r). Both Novelty lines stay partly new and were corrected (om-p2-5's is now Haiku only, with Lee and Morewedge 2021's noise account named as a rival). Three bets get rules-out sentences below (om-p2-7, om-p2-path and om-p2-path2, and om-p2-6r on its new node P2-6r).

**What the follow-ups would show.** P2-18: whether the scatter that sank P2-15 recurs on a fresh Haiku run with a base arm (about $0.07). P2-19: whether "Sam moves more than self" appears on Sonnet once the planted answers are built from Sonnet's own usual ratings (archived in om-p2-6r), the om-p2-5r audit's anchors test (about $1.80; Opus reported on 8 vignettes).

**One Prior work line corrected.** P2-17's line said Kim and Kang 2026 (arXiv 2605.27752) show that instruction wording drives stated-confidence shifts. The re-scout read the main text: it varies how token confidence is read, not how the confidence question is worded. The clause is dropped; the old line is kept on the node in `citation_corrections`.

**Budget.** Program 2 has spent $9.84 in November. br-020 (on branch p2-14, not yet on main) raised November's limit to $13.75 for om-p2-14 alone. P2-18 fits only under a new ruling and only if om-p2-14 comes in near its estimate; P2-19 fits December's $10. This remap approves none.

### What the re-scouts change

- **om-p2-4** (Novelty: partly new; corrected; `programs/other-minds/map/reads/remap-2026-11-05c-om-p2-4.md`). The re-scout drops nothing and adds one candidate: a fresh Haiku re-run of the self arm on the 162 other-person cells plus a base arm (about $0.07; om-p2-15's audit, no node yet). Nothing in print predicts its pass rule. P2-14 is re-priced in prose only. Blandfort and Pawar (now a full arXiv read) predict no self-specific gain, but Mayne et al. show a small prompt-only self advantage in explanations. So a "self better" outcome on P2-14 would partly replicate Mayne et al., not overturn the literature. The causal-report inversion stays partly new; Mehta 2025 is the nearest prior work.
- **om-p2-5** (Novelty: partly new; corrected; `programs/other-minds/map/reads/remap-2026-11-05c-om-p2-5.md`). Adds one candidate: the om-p2-5r audit's anchors test, om-p2-5r's design on Sonnet with planted values built from Sonnet's own base ratings (om-p2-6r's archive, $0), plus a reduced Opus arm, about $1.80. Names two rivals the map lacked: stronger models take up any number less (Huang et al. 2025), and a vaguer judgment of a stranger takes up any relevant number more (Lee and Morewedge 2021). A range-width secondary (about $0.02) tests the second. Kim and Kang 2026 do not support P2-17's Prior work line; that clause should go. P2-17 otherwise unchanged.

### Follow-ups

| id | parent (bet, novelty) | follow-up | models | cost | engine odds (prior + adjustment) | prior work predicts | card |
|---|---|---|---|---|---|---|---|
| P2-18 | P2-4 (om-p2-4, partly new) | Were Haiku's scattered guesses about another person's number a one-off? A fresh self-prediction run with a base arm | haiku | about $0.065 | 0.10 (0.25 -0.15) | unknown | yes |
| P2-19 | P2-5 (om-p2-5, partly new) | Does 'Sam moves more than self' appear on Sonnet once the planted answers are built from Sonnet's own usual ratings? | sonnet, opus | about $1.80 | 0.11 (0.25 -0.14) | fail | yes |

Each row's Prior work line, pass rule, cost arithmetic and cap note are on its node in `map/other-minds.json`; the odds record is in `programs/other-minds/map/odds-elicitation/v2-remap-2026-11-05c.md`.

### Rules out (killed or withdrawn bets that had no sentence)

| node | bet(s) | rules out |
|---|---|---|
| P2-7 | P2-7 | Rules out, on Haiku, Sonnet and Opus 5.5 with 34 statements in three formats, that the format pattern in ratings given for 'Sam' matches the model's own archived pattern at half the ceiling or more (+0.21, -0.10, +0.24; om-p2-7). |
| P2-path | om-p2-path, om-p2-path2 | Rules out nothing about path dependence between programs; 11 of the 17 recorded traps were already in program 1's early work, so program 2's failures cannot be tied to program 1 (om-p2-path, om-p2-path2). Needs an origin-specific pattern list. |
| P2-6r | om-p2-6r | Rules out, on Sonnet and Opus 5.5 with P2-6's 16 items at +/-30, that an earlier number's place in the assistant turn pulls the re-rating by 0.15 or more beyond its label: +0.05 and +0.02 (om-p2-6r). |
