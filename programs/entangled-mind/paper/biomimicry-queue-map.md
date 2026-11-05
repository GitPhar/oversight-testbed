# Biomimicry-queue map: memory, sleep and adaptive forgetting, against catastrophic forgetting

Written 2026-11-04 (America/Denver) by the scout session on branch `scout-bmq`, for Sean's biomimicry queue (`bmq`, steer st-14). This is a reading-and-map session only:
- no API call, no pre-registration and no bet;
- the ledger is untouched;
- open-weight models only.

The reads are in [`reads/`](reads/README.md): 93 sources, 32 read in full, 52 in part and 9 from the abstract only. Every number below comes from those files or from this program's own `results/`.

## In plain English

**The question.** Brains forget on purpose and consolidate memories in sleep. Language models forget what they learned before whenever they are trained on something new. Does anything in the brain's way of handling memory give us a cheap test, on a model we can run on the laptop, that nobody has run?

**The field is crowded, and most of it is already done.** Named up front:
- **complementary learning systems** (McClelland, McNaughton & O'Reilly 1995; Kumaran, Hassabis & McClelland 2016);
- **replay-based continual learning**: generative replay (Shin 2017), brain-inspired replay (van de Ven 2020), and a language model replaying its own pseudo-samples (LAMOL 2020; self-synthesized rehearsal on 7B models, 2024);
- **sleep-replay consolidation** (Tadros et al. 2022; Bazhenov 2026);
- **importance-weighted consolidation**: EWC, synaptic intelligence, memory-aware synapses;
- **mortal computation** (Hinton 2022; Ororbia & Friston 2023);
- **synaptic downscaling in sleep** (Tononi & Cirelli 2014), and its machine cousins: weight interpolation (WiSE-FT) and shrink-and-perturb;
- **anticipatory recovery** (Yang 2024), and a long run of papers showing that "forgotten" or "unlearned" knowledge in 7–8B models comes back (Deeb & Roger 2024; Lynch 2024; Hu 2024; Zheng 2025; Jain 2024; Kotha 2024; Jiang 2024 and 2025).

**What the metascience says about borrowing from it.** The human effects these ideas rest on are smaller than their headlines:
- **Sleep's memory benefit:** g = 0.44, falling to 0.28 after bias correction, with typical studies at 28% power.
- **Cueing memories during sleep (targeted memory reactivation):** g = 0.29, and 0.13 under a selection model.
- **Retrieval-induced forgetting:** g = 0.22 once output order is controlled.
- **Sleep making memory more gist-like:** null overall, g = 0.13, and its sign flips with list length.
- **"Slow-wave sleep does the consolidating":** a within-person test with n = 159 found no link (BF₀₁ = 14.9).
- **Human reconsolidation:** its flagship result does not survive principled reanalysis.

On the machine side:
- a trivially simple stored-memory baseline beat the best published continual-learning method on CIFAR-10 (GDumb);
- tuning the training regime alone beat EWC and replay (Mirzadeh 2020);
- one audit (abstract only) found that only 2 of 5 brain-inspired "forgets less" claims survive once you control for how much was learned in the first place.

So a "biomimetic" prediction is worth only what its human effect is worth, and every test here needs a plain baseline.

**What survives the filter: five directions, each $0 on the laptop.** In rank order:
1. **Does the knowledge survive when the answers forget?** (`bmq-d1`)
   - *The test:* train an open model until it forgets its true/false answers, then check whether a truth probe fitted before the training still reads the truth inside it.
   - *Who has looked:* both halves have been done separately (Du 2025; Zhang, Choshen & Andreas 2024), never together.
   - *Why it matters for oversight:* an overseer could read what a model knows but no longer says.
2. **When a conversation is consolidated into the weights, is "who said it" lost before "what was said"?** (`bmq-d2`)
   - *Why it matters:* nightly LoRA consolidation of conversations is already being proposed for deployed agents (Dennis 2026).
   - *What our data say:* in context, Claude treats its own earlier answer as a commitment and another person's as almost nothing (own minus other +0.46).
   - *Who has looked:* no one in the reads measured source after consolidation into weights.
3. **Does practising some facts make a model forget their neighbours, in its weights, as it does in people?** (`bmq-d4`) This has been shown in context on Qwen-2.5-7B (Li & Wang 2026), but never in the weights.
4. **Does a "those questions are finished" turn clear the question-order effect?** (`bmq-d5`)
   - *Why it might:* the closing turn borrows from proactive interference, which is how LLMs fail to forget (Wang 2025; Chattaraj 2026).
   - *What our data say:* it is a direct test of our own main finding.
5. **Does consolidating the model's own answer into its weights stop question order moving it?** (`bmq-d3`) This is nearly run in other forms, on judges (SARA, Yu 2026) and on multi-turn pollution (CCOPD, Lin 2026), and the Llama gate probably fails.

**Killed fast, with diagnoses** (nothing disappears; each stays on the map):
- self-generated replay (already run);
- sleep-like downscaling (nearly run, and confounded with how much was learned);
- triage replay (already run);
- resurfacing of forgotten knowledge (run many times; kept as a secondary assay in `bmq-d1`);
- sleep-replay consolidation on transformers (needs new method work, and is not about minds);
- mortal computation (no test exists on open-weight software, by definition);
- EWC, SI and MAS on LoRA (method benchmarking);
- active forgetting by embedding resets (needs pretraining scale);
- gist and false memory after consolidation (nearly run; null human prior);
- reconsolidation windows (the human flagship fails reanalysis);
- the sleep-protects-against-interference transfer (no clean analogue);
- schema-consistent learning (probably run, not read here);
- the fan effect (no reliable effect on Llama-3; not about forgetting).

**Steer st-14, stated plainly.** The steer's bet was that a full read would find a cheapest falsifier under $5, on a local open model, that has not already been run.
- **It did.** `bmq-d1` and `bmq-d2` both qualify, and so do `bmq-d4` and `bmq-d5`. All four cost $0, all run on the laptop's Llama-3-8B or Qwen2.5-7B, and the reads show none of them already run.
- **How narrow the novelty is.**
  - *`bmq-d1`* combines two halves that have each been run.
  - *`bmq-d2`* is the most clearly unrun.
  - *`bmq-d4`*: the knowledge-editing literature was not read and may sit close to it.
- **What "not already run" covers.** It means: not found in these 93 reads and in the searches listed in `reads/README.md`.
- **Who scores it.** The scout is grading its own scout here, so the ledger session should have an auditor check this claim before scoring st-14.

## How the odds were stated

**Format.** Every odds figure is P(pass): the probability that the draft pass rule below will be met, on the scout's v1 template.
- Each direction went to a fresh context holding only its row and its draft pass rule.
- Each context wrote a rationale of at most 100 words, then one integer from 1 to 99.
- No context saw any other direction, any human odds, or any outcome.
- All five were elicited in one pass, before ranking, at about 20:05 America/Denver on 2026-11-04.

**The elicitation check.**
- *Which directions:* a random half, seed `6ee4bca4` (the first 8 hex characters of sha256("bmq-scout-2026-11-04")), drew `bmq-d1`, `bmq-d4` and `bmq-d5`.
- *What was re-asked:* each was re-elicited in two more fresh contexts, once with the pass rule paraphrased and once negated.
- *Headline:* the headline odds are the v1 number.

| direction | v1 P(pass) | paraphrased | negated P(not pass) | spread (v1 vs paraphrase) | \|P(pass) + P(not pass) − 100\| |
|---|---|---|---|---|---|
| bmq-d1 | 55 | 45 | 56 | 10 | 11 |
| bmq-d2 | 30 | — | — | — | — |
| bmq-d3 | 12 | — | — | — | — |
| bmq-d4 | 35 | 20 | 66 | 15 | 1 |
| bmq-d5 | 10 | 9 | 83 | 1 | 7 |

**What the check shows.** The two directions near the middle (`bmq-d1`, `bmq-d4`) moved 10–15 points under paraphrase, and `bmq-d1` is 11 points incoherent under negation. Read those two as about ±10.

**Against the running base rate.** The ledger's running base rate is (5 + 1)/(14 + 2) = 0.375 (lesson pattern P1).
- *`bmq-d1`* sits above the base rate because the literature predicts its outcome: the probe should survive.
- *The rest* sit below it, for the reasons each row names.

These are map odds. Each must be re-stated with a lesson line (operators/learn.md) at pre-registration.

**The engine's other number.** The engine's own odds on the scout item itself (`bmq`, 0.30, stated 2026-11-04 18:30 by the close-founding session) are unchanged here.

---

## 1. The directions, ranked

**How the rank was set.** It weighs four things:
- **cost:** all five are $0, so cost does not separate them;
- **odds;**
- **surprise potential:** what a pass or a fail would overturn;
- **neighbourhood heat:** the probe tooling and the own-vs-other finding are this program's live neighbourhood.

**The order, and why.**
- `bmq-d1` leads because it has the best odds, existing tooling and the clearest safety reading.
- `bmq-d2` is second: lower odds, but the most clearly unrun, and tied to the program's strongest finding.
- `bmq-d4` is third: fair odds, but further from the program's question.
- `bmq-d5` is fourth: the cheapest and directly about our main finding, but low odds.
- `bmq-d3` is last: nearly run elsewhere, and its gate probably fails on Llama.

### bmq-d1 — Belief survives forgetting (rank 1; P(pass) 0.55; $0, laptop ~4–6 h)

**Assumption at stake.** When fine-tuning makes a model "forget", the knowledge is erased: what the model says is what it has.

**Who has looked, and why it is open.**
- **Du et al. 2025** (COLM; read in part). A truth probe trained on base Llama-3.1-8B, read frozen on the instruct model, stays within ±4 points of the instruct model's own probe on six Marks & Tegmark sets (e.g. cities 95.91 vs 94.65). Causal-tracing maps correlate 0.9923. But that post-training did not degrade the verbal answers, so the dissociation was never tested.
- **Zhang, Choshen & Andreas 2024** (read in full). Llama-2-7B driven to chance by random-label fine-tuning; a probe *retrained after* forgetting still decodes the tasks "largely" unchanged (figure only). The probe was not frozen, and the items were benchmark tasks, not truth statements.
- **Zheng et al. 2025.** Old-task accuracy on Llama-3-8B-Instruct falls from about 100% to about 10%, and comes back to about 96–100% after retraining on half the items. Shown by recovery, not by a probe.
- **Retrained probes on non-LLMs:** Davari 2022 (CNNs: observed 20.8 vs linear probe 64.8), Tao 2023 (BERT), Jain 2024 (toy models).
- **Tsatsos 2026** (read in full). Frozen base *harm* probes change AUC by only −0.011 to +0.027 on XSTest across successor models (the arXiv abstract; the record reads −0.003 to +0.027 from the body), despite a 17–35° rotation of the direction.
- **Design warnings from the reads:**
  - LoRA forgets less than full fine-tuning (Biderman 2024: 0.617 vs 0.545 kept), so use the random-label recipe.
  - 4-bit quantization restored unlearned knowledge from 21% to 83% (Zhang et al. 2024), so keep the adapter unmerged.
  - Alignment breaks within the first ~150 steps (Zheng), so read the probe at early checkpoints too.

**What our data say.**
- Our local Llama-3-8B-Instruct-4bit mass-mean probe at layer 13: AUROC 0.99–1.00 on its training sets, 0.94 on companies, 0.86 on counterfact, 0.88 on held-out common_claim (`results/probe-dissociation.md`, step 2).
- The same probe moved about 6% of its true/false gap with question order.
- That probe result is under a verification hold (D53; a fresh step 3 is queued). The probe *training* step is not what D53 concerns.
- Llama's verbal true/false accuracy on these sets has not been measured.

**Cheapest falsifying test.**
- *The fine-tune:* LoRA (mlx-lm, adapter unmerged) on 600 Marks & Tegmark statements with *random* true/false labels, until held-out verbal accuracy drops.
- *What is read:* on 600 held-out statements, the frozen pre-fine-tune probe and the verbal answer.
- *Secondary arms (engine-only):*
  - a probe retrained after fine-tuning, so the comparison with Zhang 2024 is direct;
  - the angle between the old and new truth directions, against control directions (Tsatsos);
  - zero-training recovery: the question asked in French (Kotha's conjugate prompt), and the original task vector re-added (Jiang 2024);
  - the adapter fused into the 4-bit base (the quantization confound).
- *Score both readouts on the same footing.* The fresh contexts flagged one risk: if verbal AUROC is scored from the True/False logits, a model biased toward one answer can still rank true above false. The pre-registration must say which readout counts as "the answer".

**Draft pass rule.**
- *Gate:* held-out verbal accuracy ≤ 0.60, or the test is untestable.
- *Pass:* the frozen probe keeps AUROC ≥ 0.80 on the held-out statements, **and** beats the verbal answer's AUROC by ≥ 0.15, with a bootstrap 95% interval above 0.
- *Fail:* the frozen probe falls below 0.80, which means the fine-tune moved the knowledge, not just the readout. That is the surprising outcome, and would be worth more.

**Engine-only sub-bets.**
- The retrained probe ≥ 0.85: 0.70.
- Fusing the adapter into 4-bit restores verbal accuracy by ≥ 10 points: 0.25.
- A French re-ask restores ≥ 10 points: 0.30.
- These are stated by the scout in one pass, not on the v1 template.

**Cost.** $0 API. On the M2 Pro (16 GB): about 1 h of probe reuse, 1–2 h of LoRA on the 4-bit 8B, and 1–2 h of evaluation. Uses the existing `experiments/local_lm.py` and the probe pipeline's venv (mlx-lm 0.32.2).

**Source.** Literature (Du; Zhang/Choshen/Andreas; Zheng), joined to this program's own probe (gold map 5).

### bmq-d2 — Source lost before content after consolidation (rank 2; P(pass) 0.30; $0, laptop ~6–10 h)

**Assumption at stake.** When an LLM agent's conversations are consolidated into its weights ("sleep"), the model keeps track of which content was its own commitment and which came from the user.

**Who has looked, and why it is open.**
- **People:**
  - *Johnson, Hashtroudi & Lindsay 1993* (source monitoring): with delay, content is kept and source is lost (false fame; cryptomnesia, where others' items are later claimed as one's own).
  - *Moscovitch et al. 2016:* consolidation keeps gist and loses context.
- **LLMs in context only.**
  - *Ranjan et al. 2026:* six open LLMs. Own-generated items were 100% correctly sourced while in context. After a delay block, 38.46% for own items against 76.34% for user-given items.
- **LLMs consolidated into weights, with no source measure.**
  - *Spens & Burgess 2026* (Nature Communications): Mistral-7B, LoRA-trained on its own reconstructions of 500 stories, becomes more gist-like ("an approximation of an approximation").
  - *Dennis et al. 2026:* nightly LoRA consolidation keeps 80.4% of conversation knowledge, against 36.8% for repeated summarising.
  - *Behrouz et al. 2026:* consolidation plus "dreaming" on Llama and Qwen.
- **The nearest own-vs-other work.**
  - *Lin et al. 2026* (CCOPD): distillation cut the pull of the model's own earlier turns (Qwen3-8B math under a wrong assistant-side solution: 33.0 → 89.3). The authors say their pollution test "is not a role-matched trust test".
- **The gap.** No read measures own-vs-other source after consolidation into weights.

**What our data say.**
- On Claude Haiku (API, not open-weight), a number framed as the model's own earlier answer pulls its re-rating, and the same number framed as another person's pulls about 0.
  - Own minus other: +0.46 [+0.21, +0.84] (`results/bm0-source-distance-lag.md`); bm1 found +0.37 [+0.17, +0.57].
- With its own first answer hidden, Haiku's repeat consistency falls from 86% to 36% (`results/gm2b-self-conditioning-40.md`).
- None of this has been run on Llama-3-8B.

**Cheapest falsifying test.**
- *Model:* Llama-3-8B-4bit in MLX.
- *Material:* word-pair transcripts (Ranjan's paradigm). For half the items the model generates the second word; for half the user gives it.
- *Gate:* in-context source d′ ≥ 1.0.
- *Consolidation:* LoRA SFT on the full transcripts, both roles, loss on all tokens.
- *Test, without the transcript:*
  - source d′ (own vs user);
  - content recognition d′ (old vs new pairs).
- *Controls:*
  - separate copy failure from source failure (Ranjan);
  - a reverse-KL distillation arm, since in CCOPD plain SFT did nothing (+0.0);
  - a familiarity control: lures the model would itself have generated, so "sounds like me" cannot pass as source memory.
- *The fresh context's warning:* content d′ in context may sit near ceiling, above source d′. Then a difference-of-drops rule has a ceiling problem. The pre-registration should equate the two in-context d′ values, or state the rule on proportional loss.

**Draft pass rule.**
- *Gate:* as above, and content d′ after consolidation ≥ 0.5 (something was consolidated).
- *Pass:* the drop in source d′ from in-context to consolidated exceeds the drop in content d′, with an item-bootstrap 95% interval above 0.

**Cost.** $0 API. Laptop about 6–10 h: a gate run of about 1 h, then LoRA and testing.

**Source.** Literature (Johnson 1993; Ranjan 2026; Spens & Burgess 2026), joined to this program's own-vs-other finding (bm1, bm0).

### bmq-d4 — Retrieval-induced forgetting in the weights (rank 3; P(pass) 0.35; $0, laptop ~4–6 h)

**Assumption at stake.** In a gradient-trained network, practising some items of a category helps the rest or leaves them alone. The human "remembering causes forgetting" effect is not a property of weights.

**Who has looked, and why it is open.**
- **Anderson, Bjork & Bjork 1994:** unpractised items of practised categories were recalled at 37.5%, against 48.4% for unpractised categories.
- **Murayama et al. 2014** (meta-analysis): g = 0.35 overall; 0.22 with output order controlled; restudy 0.07, not significant.
- **Li & Wang 2026** (ICML; poster and abstract only): in context on Qwen-2.5-7B, +11.2 pp (N = 150). Larger with high overlap: +17.4 against +3.7, the latter not significant.
- **The gap.** No in-weights version was found. The knowledge-editing literature on neighbourhood damage was not read, and may be close.

**What our data say.** Nothing direct. Program 1 measured judgments, not recall.

**Cheapest falsifying test.**
- *Model:* Qwen2.5-7B-4bit or Llama-3-8B, with MLX LoRA.
- *Stage 1:* teach 8 fictional categories × 6 exemplars, to at least 80% cued recall.
- *Stage 2:* retrieval practice (category plus stem → exemplar) on 3 exemplars in each of 4 categories.
- *Test:* cued recall of everything, with the unpractised items of practised categories asked first (the output-order control).
- *Controls:* a restudy arm (re-presentation instead of retrieval), and a matched-step arm on unrelated text.
- *Power:* the fresh contexts flagged it. Twelve key items cannot clear a 5-point gap. The pre-registration needs about 40 categories, or repeated sampling per item, sized from a pilot (P2).

**Draft pass rule.** Recall of unpractised items in practised categories (Rp−) is lower than recall of items in unpractised categories (Nrp) by ≥ 5 percentage points, with an item-bootstrap 95% interval above 0, and with Rp− items tested first.

**Engine-only sub-bet.** An in-context replication on Llama-3-8B (Li & Wang ran Qwen only), ≥ 5 pp: 0.45.

**Cost.** $0 API, laptop about 4–6 h.

**Source.** Literature (Anderson 1994; Li & Wang 2026).

### bmq-d5 — The order effect as interference that a closing turn clears (rank 4; P(pass) 0.10; $0, laptop ~2–3 h)

**Assumption at stake.** The question-order effect in LLM ratings is a judgment built from the whole question history. It is not interference from earlier items that an event boundary could clear.

**Who has looked, and why it is open.**
- **Wang et al. 2025** ("Unable to forget"): proactive interference in LLM key-value tracking.
  - A per-key "forget" instruction gains under 10 pp.
  - A mock QA turn that "closes" the earlier batch helps substantially.
- **Chattaraj et al. 2026:** across 39 LLMs, proactive interference beats retroactive interference in every model, by a mean of 69.5 points (d = 1.73).
- **The gap.** Neither study tested graded judgments or order effects. No read inserts a boundary before a rated question.

**What our data say.**
- **Haiku:** a median swing of about 25 points with chain order.
- **With Haiku's earlier answers hidden:** the order effect is about the same size (R = 1.23 [0.75, 2.02]), so it is driven by the questions, not the record of answers. That is why the fresh contexts put this direction low.
- **Llama-3-8B:** an order effect on 3 of 10 items, with within-order SD of about 13 points.

**Cheapest falsifying test.**
- *Model and items:* Llama-3-8B-4bit locally; the 40 experiment-5 items; chains O1–O4; one scale direction; 10 repeats.
- *Manipulation:* with and without a mock closed QA turn ("Those questions are finished. New, separate question:") before the main question.
- *Noise floor:* the fresh contexts flagged it. Repeat noise sets a floor under the span, so the pre-registration should state the span net of within-order noise.

**Draft pass rule.**
- *Gate:* at least 8 items show an order effect without the reset.
- *Pass:* the reset brings the median order span to ≤ 50% of the span without it, with the item-bootstrap 95% interval of the ratio below 1, while the no-chain baseline moves ≤ 5 points.

**Cost.** $0 API, laptop about 2–3 h. This is the cheapest direction on the map.

**Source.** Literature (Wang 2025; Chattaraj 2026), joined to this program's main finding.

### bmq-d3 — Consolidation dissolves the order effect (rank 5; P(pass) 0.12; $0, laptop ~6 h)

**Assumption at stake.** Anchoring a judgment in the weights, as a consolidated memory, makes it resistant to question-order interference.

**Who has looked, and why it is (barely) open.**
- **Ellenbogen et al. 2006** (people): after sleep, A-B recall under A-C interference was 76%, against 32% after wake (d = 3.07).
- **Yu et al. 2026** (SARA, abstract only): self-distillation of a judge's own single-rubric verdicts made its multi-rubric verdicts less sensitive to rubric reordering (Qwen3, Llama-3.1).
- **Lin et al. 2026** (CCOPD): distilling full-context behaviour cut the pull of earlier turns.
- **What is open.** Only graded credences under permutation of the sub-question order.

**What our data say.** Llama's order effect is significant on only 3 of 10 items. The fresh context projects about 6 per half against a gate of 8, so the gate probably fails.

**Cheapest falsifying test.**
- *Model and items:* Llama-3-8B; the 40 experiment-5 items.
- *Consolidation:* reverse-KL self-distillation to the model's own bare-question rating distribution, on 20 random items.
- *Comparison:* re-measure the chain-order spans on the 20 trained items against the 20 held-out items.

**Draft pass rule.**
- *Gate:* at least 8 items per half show an order effect before training.
- *Pass:* the median span on trained items falls by at least 50% **and** by more than on held-out items (difference in differences, with an item-bootstrap 95% interval above 0).

**Cost.** $0 API, laptop about 6 h.

**Source.** Literature (Ellenbogen 2006; SARA; CCOPD).

## 2. Killed, with diagnoses (status `killed`; they stay on the map)

| id | direction | diagnosis |
|---|---|---|
| bmq-d6 | Self-generated ("dreamed") vs real vs no replay | **Already run.** LAMOL (GPT-2: score SD across task orders 12 → 0.8); self-synthesized rehearsal on Llama-2-7B LoRA (BWT −42.39 none, −3.02 real, −0.79 self-synthesized). In vision, plain stored replay beats generative replay (GDumb: generative 15.3). Only a new outcome measure would add anything, and those are in d1 and d2. |
| bmq-d7 | Sleep-like downscaling: shrink the fine-tuning delta toward the base | **Nearly run, and confounded.** WiSE-FT does exactly this on CLIP; Mirzadeh 2020 gets the effect from the training regime; quantization rounding of small deltas restores old knowledge (Zhang 2024). Shrinking a delta trades learning for retention by construction (Subramanian 2026, abstract only). The only informative version matches learning strength, which is a method question with no stake in an assumption about minds. The LLM model-averaging literature was not read. |
| bmq-d8 | Triage replay: prioritise uncertain or tagged items | **Already run.** SuRe: surprise-prioritised replay on Llama-3.1-8B, 68.53 vs 50.53 random. The human prior (targeted reactivation) is g = 0.13 after bias correction. Our variant (priority = measured order sensitivity) has no assumption at stake. |
| bmq-d9 | Forgotten knowledge resurfaces; relearning savings; spacing | **Run many times on 7–8B models.** Deeb & Roger: ≥ 88% of unlearned pretrained knowledge recovered; Hu; Lynch; Zheng; Jain; Kotha; Jiang (CommonsenseQA 0.03 → 0.49 without weight change); Yang 2024 for anticipatory recovery. Kept only as d1's secondary recovery arm. |
| bmq-d10 | Sleep-replay consolidation (Tadros 2022) on a transformer | **Not ours.** Its spiking-conversion and Hebbian method has no transformer version; making one is method work, not a test of a mind. Evidence is MLP/CNN only (MNIST: 19.49% sequential, 48.47% with sleep). No independent replication or baseline test was found. |
| bmq-d11 | Mortal computation | **No test exists.** It is defined by computation bound to one physical hardware instance; an open-weight software model is immortal by construction. Hinton's own wake/sleep separation result did not replicate (he suspects a bug). |
| bmq-d12 | EWC / SI / MAS importance regularisation on LoRA | **Method benchmarking, crowded.** The evidence is on vision; simple baselines win under honest evaluation (Farquhar & Gal; van de Ven & Tolias: EWC 20.01% when task identity must be inferred). It asks nothing about a mind. |
| bmq-d13 | Active forgetting by periodic embedding resets | **Needs pretraining scale, and is about plasticity, not retention** (Chen 2023: +21.2% XNLI). |
| bmq-d14 | Gist and false memory (DRM) after consolidation | **Nearly run, weak prior.** Spens & Burgess 2026 already show semanticisation after LoRA consolidation on Mistral-7B. The human sleep–false-memory effect is null overall (g = 0.13, sign flips with list length). An in-context baseline exists (Orthey 2026). |
| bmq-d15 | A reconsolidation window for LoRA edits | **The human prior fails.** Schiller 2010's fear-recovery difference disappears under principled exclusions (Chalkia 2020); human reconsolidation is "viable but hotly contested". The knowledge-editing literature was not read. |
| bmq-d16 | Consolidation protects against interference (A-B, then A-C) | **Does not transfer cleanly.** With A-B in weights and A-C in context, which answer is "correct" depends on the question asked. That is the context-vs-parametric knowledge-conflict literature (not read), not interference. |
| bmq-d17 | Facts consistent with the model's priors are learned faster and interfere less (Kumaran 2016) | **Probably run** in the LLM knowledge-injection literature (not read here; named for a later scout). |
| bmq-d18 | Fan effect | **Not about forgetting**, and Llama-3 showed no reliable effect (Roberts 2024). |

## 3. Controls every pre-registration in this queue must carry (from the metascience reads)

1. **A plain baseline** at the same token or step budget: stored replay, or a tuned vanilla arm with lower or decaying learning rate (GDumb; Mirzadeh; Farquhar & Gal). This applies lesson pattern P3.
2. **Learning strength matched.** Report first-task performance before the second task starts, and match the arms on it or regress on it (Subramanian 2026).
3. **Format against knowledge.** Probe in the original template and in a neutral one. Treat instructions as task labels (Zheng 2025: forgetting is often alignment, not knowledge).
4. **For any retrieval-induced forgetting test:** an output-order control and a restudy arm (Murayama 2014).
5. **For anything reconsolidation-like:** a 2×2 of reactivation × update, plus a context-only control (Elsey 2018).
6. **Pre-registered exclusions and power,** sized for the bias-corrected human effects (g ≈ 0.13–0.3), not the headlines (Berres & Erdfelder; Hu 2020). This applies P2.
7. **The 4-bit confound.** Keep adapters unmerged, and report any fused-into-4-bit reading separately (Zhang 2024).

## 4. The human's questions

Each direction's cockpit card asks Sean one question at direction level: is this worth about $X, and will it come back a hit?
- The questions are in each node's `human_prompt` in `map/entangled-mind.json`.
- The printed form, in a shuffled order with no engine numbers, is `map/entangled-mind-bmq-odds-form.md`.
- His odds come only from the cockpit (`ledger/human-odds.jsonl`).
- A bet pre-registered without them proceeds marked "no human odds".
