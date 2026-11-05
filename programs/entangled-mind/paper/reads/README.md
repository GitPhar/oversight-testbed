# Reads: Sean's biomimicry queue (`bmq`, steer st-14)

Scouted 2026-11-04, 18:45–20:10 America/Denver, by the scout session on branch `scout-bmq`. The question: memory, sleep and adaptive forgetting, against catastrophic forgetting, open-weight models only. The map built from these reads is [`../biomimicry-queue-map.md`](../biomimicry-queue-map.md).

## In plain English

**93 sources, one file each.**
- **By depth:** 32 were read in full, 52 in part (each file names the sections it read), and 9 from the abstract only. Abstract-only files carry no numbers that are not in the abstract.
- **By field:** neuroscience 13, cognitive psychology 14, machine learning 53, metascience 12, and one theory paper filed as "other" (mortal computation).
- **How each file is laid out:** what was tested, on whom, how it was scored, the result (numbers from the text read), the limits, what we could borrow, the paper's own next steps, whether it already ran one of our candidate tests (T1–T8, below), and whether it transfers to a local open model.

**How the reading was done.**
- Six readers worked in parallel, one per field slice: neuroscience (A), cognitive psychology (B), continual-learning classics (C), what forgetting is inside LLMs (D), replay and sleep in LLMs (E), and metascience (F).
- They used web reads only: no model API, no paid service.
- The scout then fetched the arXiv or PMC page of every 2025–2026 preprint the map relies on, and found each real, with matching title, authors and gist: Du 2025, Zhang/Choshen/Andreas 2024, Lin 2026 (CCOPD), Behrouz 2026, Lee 2026, Spens & Burgess 2026, Dennis 2026, Ranjan 2026, Tsatsos 2026, Li & Wang 2026 (ICML listing), and Yu 2026 (SARA).
- One reader record was killed as not credible: `imanov-2026-mechanistic-forgetting`. It claims hidden-state access to API-only models and its numbers are inconsistent.

**Two records were overwritten in the shared folder.**
- `tadros-2022-sleep-replay-consolidation.md`: reader A's version was replaced by reader C's.
- `zheng-2025-spurious-forgetting.md`: reader D's version was replaced by reader F's.

Each source keeps one record, and the surviving one is a partial read. Reader D's report gave the same arXiv id (2501.13453) and the same headline, which the surviving file also states.

**Substitutes.** Where a classic had no open copy, the reader used an open paper by the same authors or the same school, and the file says so:
- French 1999 for McCloskey & Cohen 1989 and Ratcliff 1990;
- Lewis, Knoblich & Poe 2018 for Lewis & Durrant 2011;
- Lee, Nader & Schiller 2017 for Nader 2000;
- Moscovitch et al. 2016 for Winocur & Moscovitch 2011;
- O'Leary et al. 2024 for Ryan & Frankland 2022.

## The candidate tests each read was checked against

| id | test | verdict across all reads |
|---|---|---|
| T1 | A truth probe trained before a forgetting fine-tune, read frozen after it, while the verbal answers degrade | **Not run as a whole.** The frozen-probe half is Du 2025, but its fine-tune did not degrade the answers. The forgetting half is Zhang/Choshen/Andreas 2024, but its probe was retrained after forgetting. Retrained-probe cases on non-LLMs: Davari, Tao, Jain. → `bmq-d1` |
| T2 | Consolidating in-context content into weights, then measuring order sensitivity and own-vs-other source | **Order half nearly run:** SARA (Yu 2026, abstract only) and CCOPD (Lin 2026). **Retention half run:** Dennis 2026, Behrouz 2026, Spens & Burgess 2026. **Source half not found.** → `bmq-d2`, `bmq-d3` |
| T3 | Self-generated vs real vs no replay | **Run:** LAMOL; SSR on 7B with LoRA; vision networks. → killed (`bmq-d6`) |
| T4 | Sleep-like downscaling of fine-tuning deltas | **Nearly run:** WiSE-FT (CLIP), Mirzadeh 2020, and quantization rounding (Zhang 2024). Confounded with how much was learned (Subramanian 2026, abstract). → killed (`bmq-d7`) |
| T5 | Retrieval-induced forgetting in LLMs | **Run in context** on Qwen-2.5-7B (Li & Wang 2026). **In weights: not found.** → `bmq-d4` |
| T6 | Spacing, anticipatory recovery, relearning savings | **Run:** Yang 2024 (anticipatory recovery); savings in Deeb & Roger 2024 and Jain 2024. → folded into `bmq-d9` (killed as a direction) |
| T7 | Selective ("triage") replay | **Run:** SuRe (surprise-prioritised replay, Llama-3.1-8B). → killed (`bmq-d8`) |
| T8 | Forgotten knowledge resurfacing | **Run, many times on 7–8B models:** Deeb & Roger, Hu, Lynch, Zheng, Jain, Kotha, Jiang, and Zhang (quantization). → killed (`bmq-d9`); kept as a secondary assay in `bmq-d1` |

## Searches that returned nothing (an empty search is a finding)

**Probes and forgetting**
- A truth probe trained before a forgetting fine-tune and read after it, on any LLM (D).

**Consolidation and source**
- Source amnesia, or source monitoring, after fine-tuning or context distillation (B, E).
- Context distillation combined with order sensitivity of graded judgments (E).
- Fine-tuning on a model's own answers, measured for order effects (E).

**Sleep and downscaling**
- Sleep-replay consolidation (Tadros et al.) applied to any transformer or LLM (C). There is also no independent replication or baseline test of it (F).
- Shrinking fine-tuned LLM deltas toward the base model, framed as sleep (C).
- A head-to-head of EWC plus LoRA on Llama (C).

**Human paradigms on LLMs**
- A forgetting curve over time in context; spontaneous recovery of A-B after A-C fine-tuning; the testing effect in fine-tuning (B).

**Human replication**
- A multi-lab or registered-report replication of retrieval-induced forgetting (F).

**Open full texts, none found:**
- McCloskey & Cohen 1989, Ratcliff 1990, Storm 2011, Nørby 2015, Lewis & Durrant 2011;
- Richards & Frankland 2017, Ryan & Frankland 2022, Klinzing et al. 2019, Winocur & Moscovitch 2011;
- Cordi & Rasch 2021 (Current Opinion), Li & Wang 2026, Subramanian 2026, Robins 1995.

## Not read, and possibly close (named so a later scout can check)

- **Knowledge-editing literature.** Neighbourhood damage after an edit is close to in-weights retrieval-induced forgetting (`bmq-d4`).
- **Knowledge-conflict literature** (context against parametric memory). Bears on the killed `bmq-d16`.
- **LLM model-averaging work.** Weight interpolation between base and fine-tuned models, against forgetting; bears on the killed `bmq-d7`.
- **Leads named by readers:**
  - arXiv 2407.08582 (a universal truthfulness hyperplane);
  - Wu et al. 2022 (layer-wise probing in continual learning);
  - Patil et al. 2023 (deleted facts extracted from hidden states);
  - Xiang et al. 2024 (EWC with LoRA);
  - EVAF (arXiv 2606.29916, a valence × surprise write gate).

## Index

### Neuroscience (13)

| record | source | depth | transfers |
|---|---|---|---|
| [`davis-2017-biology-of-forgetting`](davis-2017-biology-of-forgetting.md) | The biology of forgetting, a perspective — Davis & Zhong, 2017, Neuron 95(3):490-503 | full | partly |
| [`klinzing-2019-systems-consolidation-sleep`](klinzing-2019-systems-consolidation-sleep.md) | Mechanisms of systems memory consolidation during sleep — Klinzing, Niethard & Born, 2019, Nature Neuroscience 22:1598-1610 | abstract | partly |
| [`kumaran-2016-cls-updated`](kumaran-2016-cls-updated.md) | Complementary learning systems theory updated — Kumaran, Hassabis & McClelland, 2016, Trends in Cognitive Sciences 20(7):512-534 | partial | yes |
| [`lee-2017-reconsolidation-updating`](lee-2017-reconsolidation-updating.md) | Reconsolidation updating (substitute for Nader, Schafe & LeDoux 2000) — Lee, Nader & Schiller, 2017, Trends in Cognitive Sciences 21(7):531-545 | full | partly |
| [`lewis-2018-replay-creativity`](lewis-2018-replay-creativity.md) | iOtA/BiOtA: overlapping replay builds schemas (substitute for Lewis & Durrant 2011) — Lewis, Knoblich & Poe, 2018, Trends in Cognitive Sciences 22(6):491-503 | full | partly |
| [`mcclelland-1995-cls`](mcclelland-1995-cls.md) | Why there are complementary learning systems — McClelland, McNaughton & O'Reilly, 1995, Psychological Review 102(3):419-457 | partial | yes |
| [`moscovitch-2016-memory-transformation`](moscovitch-2016-memory-transformation.md) | Episodic memory and beyond: hippocampus and neocortex in transformation (substitute for Winocur & Moscovitch 2011) — Moscovitch, Cabeza, Winocur & Nadel, 2016, Annual Review of Psychology 67:105-134 | partial | partly |
| [`oleary-2024-natural-forgetting-engram`](oleary-2024-natural-forgetting-engram.md) | Natural forgetting reversibly modulates engram expression (substitute for Ryan & Frankland 2022) — O'Leary, Bruckner, Autore & Ryan, 2024, eLife 12:RP92860 | partial | partly |
| [`richards-2017-persistence-transience`](richards-2017-persistence-transience.md) | The persistence and transience of memory — Richards & Frankland, 2017, Neuron 94(6):1071-1084 | abstract | partly |
| [`spens-2024-generative-consolidation`](spens-2024-generative-consolidation.md) | A generative model of memory construction and consolidation — Spens & Burgess, 2024, Nature Human Behaviour 8:526-543 | partial | partly |
| [`spens-2026-compressive-rag-consolidation`](spens-2026-compressive-rag-consolidation.md) | Hippocampo-neocortical interaction as compressive retrieval-augmented generation — Spens & Burgess, 2026, Nature Communications (doi 10.1038/s41467-026-74357-6) | partial | yes |
| [`stickgold-2013-memory-triage`](stickgold-2013-memory-triage.md) | Sleep-dependent memory triage — Stickgold & Walker, 2013, Nature Neuroscience 16(2):139-145 | full | partly |
| [`tononi-2014-shy-price-of-plasticity`](tononi-2014-shy-price-of-plasticity.md) | Sleep and the price of plasticity (SHY) — Tononi & Cirelli, 2014, Neuron 81(1):12-34 | partial | partly |

### Cognitive psychology (people, and human memory paradigms run on LLMs) (14)

| record | source | depth | transfers |
|---|---|---|---|
| [`anderson-1991-reflections-environment`](anderson-1991-reflections-environment.md) | Reflections of the environment in memory (rational analysis of forgetting) — John R. Anderson & Lael J. Schooler, 1991, Psychological Science 2(6) | partial | partly |
| [`anderson-1994-retrieval-induced-forgetting`](anderson-1994-retrieval-induced-forgetting.md) | Remembering can cause forgetting (retrieval-induced forgetting) — Michael C. Anderson, Robert A. Bjork & Elizabeth L. Bjork, 1994, JEP: Learning, Memory, and Cognition 20(5) | partial | yes |
| [`bjork-1992-new-theory-of-disuse`](bjork-1992-new-theory-of-disuse.md) | A new theory of disuse and an old theory of stimulus fluctuation — Robert A. Bjork & Elizabeth L. Bjork, 1992, in Healy, Kosslyn & Shiffrin (eds), From Learning Processes to Cognitive Processes, vol 2, pp 35-67, Erlbaum | partial | partly |
| [`cao-2025-memory-effects-llm`](cao-2025-memory-effects-llm.md) | Analyzing memory effects in large language models through the lens of cognitive psychology — Zhaoyang Cao, Lael Schooler & Reza Zafarani, 2025, arXiv 2509.17138 (v3, q-bio.NC) | partial | partly |
| [`chattaraj-2026-pi-ri-llm`](chattaraj-2026-pi-ri-llm.md) | LLMs remember first, forget last: dual-process interference — Sourav Chattaraj & Kanak Raj, 2026, arXiv 2603.00270 (v3; comments say it appears in Springer LNNS, NPIR volume) | full | yes |
| [`ellenbogen-2006-sleep-interference`](ellenbogen-2006-sleep-interference.md) | Interfering with theories of sleep and memory: sleep protects declarative memory from associative interference — Jeffrey M. Ellenbogen, Justin C. Hulbert, Robert Stickgold, David F. Dinges & Sharon L. Thompson-Schill, 2006, Current Biology 16(13) | full | yes |
| [`french-1999-catastrophic-forgetting`](french-1999-catastrophic-forgetting.md) | Catastrophic forgetting in connectionist networks (review) — Robert M. French, 1999, Trends in Cognitive Sciences 3(4) | full | partly |
| [`johnson-1993-source-monitoring`](johnson-1993-source-monitoring.md) | Source monitoring (review and framework) — Marcia K. Johnson, Shahin Hashtroudi & D. Stephen Lindsay, 1993, Psychological Bulletin 114(1) | partial | yes |
| [`orthey-2026-drm-false-memory-llm`](orthey-2026-drm-false-memory-llm.md) | False memories in LLMs: gist-based recognition despite verbatim context — Robin Orthey, Guillaume Pelat & Yuri Nakao (Fujitsu Research), 2026, Proceedings of LUHME 2026 (ACL Anthology 2026.luhme-1.7), pp 89-97 | full | yes |
| [`payne-2009-sleep-false-memory`](payne-2009-sleep-false-memory.md) | The role of sleep in false memory formation — Jessica D. Payne, Daniel L. Schacter, Ruth E. Propper, Li-Wen Huang, Erin J. Wamsley, Matthew A. Tucker, Matthew P. Walker & Robert Stickgold, 2009, Neurobiology of Learning and Memory 92(3) | full | yes |
| [`ranjan-2026-reality-monitoring-llm`](ranjan-2026-reality-monitoring-llm.md) | Reality monitoring in LLMs — Ranjan, Sokratous & Odegaard, 2026, arXiv preprint (not peer reviewed) | partial | partly |
| [`roberts-2024-fan-effect-llm`](roberts-2024-fan-effect-llm.md) | Large language model recall uncertainty is modulated by the fan effect — Jesse Roberts, Kyle Moore, Thao Pham, Oseremhen Ewaleifoh & Doug Fisher, 2024, CoNLL 2024 (arXiv 2407.06349) | full | no |
| [`storm-2011-benefit-of-forgetting`](storm-2011-benefit-of-forgetting.md) | The benefit of forgetting in thinking and remembering — Benjamin C. Storm, 2011, Current Directions in Psychological Science 20(5) | abstract | no |
| [`wang-2025-proactive-interference-llm`](wang-2025-proactive-interference-llm.md) | Unable to forget: proactive interference reveals working-memory limits in LLMs beyond context length — Chupei Wang & Jiaqiu Vince Sun, 2025, arXiv 2506.08184 (v3; ICML 2025 Long-Context Foundation Models workshop) | partial | yes |

### Machine learning (53)

| record | source | depth | transfers |
|---|---|---|---|
| [`aljundi-2018-memory-aware-synapses`](aljundi-2018-memory-aware-synapses.md) | Memory Aware Synapses (MAS) — Aljundi, Babiloni, Elhoseiny, Rohrbach & Tuytelaars, 2018, ECCV (read as arXiv 1711.09601v4) | full | partly |
| [`ash-2020-warm-starting`](ash-2020-warm-starting.md) | On warm-starting neural network training (shrink-and-perturb) — Ash & Adams, 2020, NeurIPS | full | partly |
| [`bazhenov-2026-not-just-after-one`](bazhenov-2026-not-just-after-one.md) | Not Just After One: sleep-inspired replay after sequential tasks — A. Bazhenov, Delanois & Krishnan, 2026, arXiv preprint 2606.08447v1 | full | partly |
| [`behrouz-2026-language-models-need-sleep`](behrouz-2026-language-models-need-sleep.md) | Language Models Need Sleep: learning to self-modify and consolidate memories — Behrouz, Hashemi, Javanmard & Mirrokni, 2026, arXiv preprint 2606.03979v2 (OpenReview version since Sept 2025, per the paper) | partial | partly |
| [`biderman-2024-lora-forgets-less`](biderman-2024-lora-forgets-less.md) | LoRA learns less and forgets less — Biderman, Portes, Gonzalez Ortiz, et al., 2024, arXiv preprint 2405.09673 (venue not confirmed in fetched text) | partial | partly |
| [`chen-2023-active-forgetting`](chen-2023-active-forgetting.md) | Active forgetting for language plasticity — Chen, Marchisio, Raileanu, Adelani, Stenetorp, Riedel & Artetxe, 2023, NeurIPS 2023 | partial | no |
| [`davari-2022-representation-forgetting`](davari-2022-representation-forgetting.md) | Probing representation forgetting in supervised and supervised contrastive learning — Davari, Asadi, Mudur, Aljundi, Belilovsky, 2022, CVPR 2022 | full | partly |
| [`deeb-2024-unlearning-weights`](deeb-2024-unlearning-weights.md) | Do unlearning methods remove information from language model weights? — Deeb, Roger, 2024, arXiv preprint 2410.08827 (v3, Feb 2025) | full | yes |
| [`dennis-2026-nightly-lora-consolidation`](dennis-2026-nightly-lora-consolidation.md) | Weight-based consolidation vs cascading compaction — Dennis, Shabahang, Guo & Patil, 2026, arXiv preprint | full | yes |
| [`dohare-2024-loss-of-plasticity`](dohare-2024-loss-of-plasticity.md) | Loss of plasticity in deep continual learning — Dohare, Hernandez-Garcia, Lan, Rahman, Mahmood & Sutton, 2024, Nature | partial | partly |
| [`du-2025-post-training-reshapes`](du-2025-post-training-reshapes.md) | How post-training reshapes LLMs: knowledge, truthfulness, refusal, confidence — Du, Li, Cai, Saraipour, Zhang, Lakkaraju, Sun, Zhang, 2025, arXiv preprint 2504.02904 (v3) | partial | yes |
| [`hazard-2025-sure-surprise-replay`](hazard-2025-sure-surprise-replay.md) | SuRe: surprise-driven prioritised replay — Hazard, Fountas, Benfeghoul, Oomerjee, Wang & Bou-Ammar, 2025, arXiv preprint | partial | yes |
| [`hinton-2022-forward-forward-mortal`](hinton-2022-forward-forward-mortal.md) | Forward-Forward algorithm, "Mortal computation" and "Sleep" sections — Hinton, 2022, arXiv preprint 2212.13345v1 | partial | no |
| [`hu-2024-relearning-attacks`](hu-2024-relearning-attacks.md) | Unlearning or obfuscating? Jogging the memory of unlearned LLMs via benign relearning — Hu, Fu, Wu, Smith, 2024, arXiv preprint 2406.13356 (v4, Mar 2025) | partial | yes |
| [`huang-2024-ssr`](huang-2024-ssr.md) | Self-Synthesized Rehearsal (SSR) — Huang, Cui, Wang, Yang, Liao, Song, Yao & Su, 2024, ACL 2024 | partial | partly |
| [`ibrahim-2024-continual-pretraining`](ibrahim-2024-continual-pretraining.md) | Simple and scalable continual pre-training — Ibrahim, Thérien, Gupta, Richter, Anthony, Lesort, Belilovsky & Rish, 2024, TMLR (06/2024) | partial | partly |
| [`imanov-2026-mechanistic-forgetting`](imanov-2026-mechanistic-forgetting.md) | Mechanistic analysis of catastrophic forgetting in LLMs during continual fine-tuning — Imanov, 2026, arXiv preprint 2601.18699 (v1) | full | no |
| [`jain-2024-finetuning-wrapper`](jain-2024-finetuning-wrapper.md) | Mechanistically analyzing fine-tuning on procedurally defined tasks (fine-tuning as a wrapper) — Jain, Kirk, Lubana, Dick, Tanaka, Grefenstette, Rocktäschel, Krueger, 2024, ICLR 2024 (venue per brief; not confirmed in fetched text) | partial | partly |
| [`jiang-2024-instruction-vector`](jiang-2024-instruction-vector.md) | Interpretable catastrophic forgetting of LLM fine-tuning via instruction vector — Jiang, Li, Jiang, Xue, Zhou, Song, Lian, Wei, 2024, arXiv preprint 2406.12227 (v1) | full | yes |
| [`jiang-2025-function-vectors-forgetting`](jiang-2025-function-vectors-forgetting.md) | Function vectors for characterizing and mitigating catastrophic forgetting in continual instruction tuning — Jiang, Jiang, Li, Xue, Zhou, Song, Lian, Wei, 2025, ICLR 2025 (per proceedings listing in search; arXiv 2502.11019) | partial | yes |
| [`kirkpatrick-2017-ewc`](kirkpatrick-2017-ewc.md) | EWC (elastic weight consolidation) — Kirkpatrick, Pascanu, Rabinowitz, Veness, Desjardins, Rusu, Milan, Quan, Ramalho, Grabska-Barwinska, Hassabis, Clopath, Kumaran & Hadsell, 2017, PNAS (read as arXiv 1612.00796v2) | full | partly |
| [`kissane-2024-sae-transfer`](kissane-2024-sae-transfer.md) | SAEs (usually) transfer between base and chat models — Kissane, Krzyzanowski, Conmy, Nanda, 2024, LessWrong / Alignment Forum interim report (18 July 2024) | full | partly |
| [`kotha-2024-implicit-inference`](kotha-2024-implicit-inference.md) | Understanding catastrophic forgetting via implicit inference (conjugate prompting) — Kotha, Springer, Raghunathan, 2024, ICLR 2024 (venue per brief; not confirmed in fetched text) | partial | yes |
| [`lee-2026-language-models-need-sleep`](lee-2026-language-models-need-sleep.md) | Do language models need sleep? Offline recurrence — Lee, McLeish, Goldstein & Fanti, 2026, arXiv preprint (v3) | partial | no |
| [`li-2017-learning-without-forgetting`](li-2017-learning-without-forgetting.md) | Learning without Forgetting (LwF) — Li & Hoiem, 2017, IEEE TPAMI (read as arXiv 1606.09282v3; first version ECCV 2016) | full | partly |
| [`li-2026-rif-in-llms`](li-2026-rif-in-llms.md) | Retrieval-induced forgetting in LLMs: a reproducible failure mode and a verified fix — Shuzhen Li & Mengdi Wang, 2026, ICML 2026 workshop (Failure Modes in Agentic AI), poster | abstract | yes |
| [`li-2026-rif-llm-poster`](li-2026-rif-llm-poster.md) | Retrieval-induced forgetting in LLMs (poster read) — Shuzhen Li & Mengdi Wang, 2026, ICML 2026 Workshop on Failure Modes in Agentic AI (FAGEN), poster | partial | yes |
| [`lin-2025-sleep-time-compute`](lin-2025-sleep-time-compute.md) | Sleep-time compute — Lin, Snell, Wang, Packer, Wooders, Stoica & Gonzalez, 2025, arXiv preprint | abstract | no |
| [`lin-2026-canonical-context-distillation`](lin-2026-canonical-context-distillation.md) | Canonical-Context On-Policy Distillation (CCOPD) — Z. Lin, Liu, Quan, Zhang, Shi, Xu, Li, Luo & Zhu, 2026, arXiv preprint (v2, Oct 2026) | partial | yes |
| [`lopezpaz-2017-gem`](lopezpaz-2017-gem.md) | Gradient Episodic Memory (GEM) — Lopez-Paz & Ranzato, 2017, NeurIPS (read as arXiv 1706.08840v6) | full | partly |
| [`luo-2023-forgetting-empirical`](luo-2023-forgetting-empirical.md) | Empirical study of catastrophic forgetting in LLM continual fine-tuning — Luo, Yang, Meng, Li, Zhou, Zhang, 2023, arXiv preprint (2308.08747) | full | partly |
| [`lynch-2024-eight-methods-unlearning`](lynch-2024-eight-methods-unlearning.md) | Eight methods to evaluate robust unlearning in LLMs — Lynch, Guo, Ewart, Casper, Hadfield-Menell, 2024, arXiv preprint 2402.16835 | full | yes |
| [`mirzadeh-2020-training-regimes`](mirzadeh-2020-training-regimes.md) | Understanding the role of training regimes in continual learning — Seyed Iman Mirzadeh, Mehrdad Farajtabar, Razvan Pascanu, Hassan Ghasemzadeh, 2020, arXiv 2006.06958 (NeurIPS 2020) | full | partly |
| [`parisi-2019-continual-lifelong-learning-review`](parisi-2019-continual-lifelong-learning-review.md) | Continual lifelong learning with neural networks: a review — Parisi, Kemker, Part, Kanan & Wermter, 2019, Neural Networks (read as arXiv 1802.07569v4) | partial | partly |
| [`robins-1995-pseudorehearsal`](robins-1995-pseudorehearsal.md) | Catastrophic forgetting, rehearsal and pseudorehearsal — Robins, 1995, Connection Science (DOI 10.1080/09540099550039318) | abstract | partly |
| [`scialom-2022-continual-t0`](scialom-2022-continual-t0.md) | Continual-T0 — Scialom, Chakrabarty & Muresan, 2022, EMNLP 2022 (per arXiv v4; venue not checked on the publisher page) | partial | partly |
| [`shin-2017-deep-generative-replay`](shin-2017-deep-generative-replay.md) | Deep Generative Replay (DGR) — Shin, Lee, Kim & Kim, 2017, NeurIPS (read as arXiv 1705.08690v3) | full | partly |
| [`snell-2022-context-distillation`](snell-2022-context-distillation.md) | Learning by distilling context — Snell, Klein & Zhong, 2022, arXiv preprint | partial | yes |
| [`sun-2020-lamol`](sun-2020-lamol.md) | LAMOL — Sun, Ho & Lee, 2020, ICLR 2020 | full | partly |
| [`tadros-2022-sleep-replay-consolidation`](tadros-2022-sleep-replay-consolidation.md) | Sleep Replay Consolidation (SRC) — Tadros, Krishnan, Ramyaa & Bazhenov, 2022, Nature Communications 13:7742 | partial | partly |
| [`tao-2023-bert-probing-forgetting`](tao-2023-bert-probing-forgetting.md) | Can BERT refrain from forgetting on sequential tasks? A probing study — Tao, Feng, Zhao, 2023, ICLR 2023 | partial | partly |
| [`tsatsos-2026-probe-transfer-distilled`](tsatsos-2026-probe-transfer-distilled.md) | Linear probes transfer from base to distilled language models despite rotation — Tsatsos, 2026, arXiv preprint 2610.35586 (v1, 26 Oct 2026) | full | yes |
| [`vandeven-2019-three-scenarios`](vandeven-2019-three-scenarios.md) | Three scenarios for continual learning — Gido M. van de Ven & Andreas S. Tolias, 2019, arXiv 1904.07734 (NeurIPS 2018 Continual Learning workshop) | full | partly |
| [`vandeven-2020-brain-inspired-replay`](vandeven-2020-brain-inspired-replay.md) | Brain-inspired replay (BI-R) — van de Ven, Siegelmann & Tolias, 2020, Nature Communications 11 | partial | partly |
| [`wang-2026-context-returns-nca`](wang-2026-context-returns-nca.md) | When context returns: context-induced degradation after distillation (NCA) — X. Wang, Chen, Li, Y. Chen & Huang, 2026, arXiv preprint (v2, Aug 2026) | partial | yes |
| [`wortsman-2022-wise-ft`](wortsman-2022-wise-ft.md) | Robust fine-tuning of zero-shot models (WiSE-FT) — Wortsman, Ilharco, Kim, Li, Kornblith, Roelofs, Gontijo-Lopes, Hajishirzi, Farhadi, Namkoong & Schmidt, 2022, CVPR (read as arXiv 2109.01903v3) | partial | yes |
| [`yang-2024-anticipatory-recovery`](yang-2024-anticipatory-recovery.md) | Reawakening knowledge: anticipatory recovery — Yang, Jones, Mozer & Ren, 2024, NeurIPS 2024 | partial | yes |
| [`yu-2026-rubric-interference-sara`](yu-2026-rubric-interference-sara.md) | Rubric interference in LLM judges (SARA) — Yu, Zhang, Mou, Zhang, Ye & Zhang, 2026, arXiv preprint | abstract | partly |
| [`zenke-2017-synaptic-intelligence`](zenke-2017-synaptic-intelligence.md) | Synaptic Intelligence (SI) — Zenke, Poole & Ganguli, 2017, ICML (read as arXiv 1703.04200v3) | full | partly |
| [`zhang-2024-unforgettable-generalization`](zhang-2024-unforgettable-generalization.md) | Unforgettable generalization in language models — Zhang, Choshen, Andreas, 2024, arXiv preprint 2409.02228 | full | yes |
| [`zhang-2024-unlearning-quantization`](zhang-2024-unlearning-quantization.md) | Catastrophic failure of LLM unlearning via quantization — Zhang, Wang, Li, Wu, Tang, Liu, He, Yin, Wang, 2024, arXiv preprint 2410.16454 (v3, Mar 2025) | partial | yes |
| [`zheng-2025-spurious-forgetting`](zheng-2025-spurious-forgetting.md) | Spurious forgetting in continual learning of language models — Junhao Zheng, Xidi Cai, Shengjie Qiu, Qianli Ma, 2025, ICLR 2025 | partial | yes |
| [`zweiger-2025-seal`](zweiger-2025-seal.md) | Self-Adapting Language Models (SEAL) — Zweiger, Pari, Guo, Akyürek, Kim & Agrawal, 2025, arXiv preprint (v2, Sep 2025) | partial | partly |

### Metascience (replication and evaluation) (12)

| record | source | depth | transfers |
|---|---|---|---|
| [`berres-2021-sleep-benefit-meta`](berres-2021-sleep-benefit-meta.md) | Sleep benefit in episodic memory, meta-analysis — Sabrina Berres & Edgar Erdfelder, 2021, Psychological Bulletin 147(12) | partial | partly |
| [`chalkia-2020-schiller-verification`](chalkia-2020-schiller-verification.md) | Reconsolidation-update verification report (Schiller et al. 2010) — Anastasia Chalkia, Lukas Van Oudenhove, Tom Beckers, 2020, Cortex 129 | partial | partly |
| [`cordi-2021-no-sws-correlation`](cordi-2021-no-sws-correlation.md) | No within-person SWS-memory correlation — Maren Jasmin Cordi & Björn Rasch, 2021, Sleep 44(8) zsab034 | partial | partly |
| [`cordi-2021-robust-sleep-benefits`](cordi-2021-robust-sleep-benefits.md) | How robust are sleep-mediated memory benefits? — Maren Jasmin Cordi & Björn Rasch, 2021, Current Opinion in Neurobiology 67:1-7 | abstract | partly |
| [`elsey-2018-human-reconsolidation-review`](elsey-2018-human-reconsolidation-review.md) | Human memory reconsolidation: framework and critical review — Jacob W. B. Elsey, Vanessa A. Van Ast, Merel Kindt, 2018, Psychological Bulletin 144(8) | partial | partly |
| [`farquhar-2018-robust-cl-evaluation`](farquhar-2018-robust-cl-evaluation.md) | Towards robust evaluations of continual learning — Sebastian Farquhar & Yarin Gal, 2018 (v3 2019), arXiv 1805.09733 (ICML 2018 workshop version) | full | partly |
| [`hu-2020-tmr-meta`](hu-2020-tmr-meta.md) | Targeted memory reactivation meta-analysis — Xiaoqing Hu, Larry Y. Cheng, Man Hin Chiu, Ken A. Paller, 2020, Psychological Bulletin 146(3) | partial | partly |
| [`murayama-2014-rif-meta`](murayama-2014-rif-meta.md) | Retrieval-induced forgetting meta-analysis — Kou Murayama, Toshiya Miyatsu, Dorothy Buchli, Benjamin C. Storm, 2014, Psychological Bulletin 140(5) | partial | partly |
| [`newbury-2019-sleep-false-memory-meta`](newbury-2019-sleep-false-memory-meta.md) | Sleep and veridical/false memory (DRM) meta-analysis — Chloe R. Newbury & Padraic Monaghan, 2019, Psychonomic Bulletin & Review 26(2) | partial | partly |
| [`prabhu-2020-gdumb`](prabhu-2020-gdumb.md) | GDumb: a simple approach that questions our progress in continual learning — Ameya Prabhu, Philip H. S. Torr, Puneet K. Dokania, 2020, ECCV 2020 | partial | partly |
| [`shi-2024-cl-llm-survey`](shi-2024-cl-llm-survey.md) | Continual learning of large language models: a comprehensive survey — Haizhou Shi, Zihao Xu, Hengyi Wang, Weiyi Qin, Wenyuan Wang, Yibin Wang, Zifeng Wang, Sayna Ebrahimi, Hao Wang, 2024, arXiv 2404.16789 (v3, Nov 2024; ACM Computing Surveys) | partial | partly |
| [`subramanian-2026-bwt-audit`](subramanian-2026-bwt-audit.md) | Auditing backward transfer against learning strength: a reanalysis of biologically plausible continual learning — Saanvi S. Subramanian, 2026, NeurIPS 2026 workshop (AI for Meta-Science), poster | abstract | yes |

### Other (1)

| record | source | depth | transfers |
|---|---|---|---|
| [`ororbia-2023-mortal-computation`](ororbia-2023-mortal-computation.md) | Mortal computation: a foundation for biomimetic intelligence — Ororbia & Friston, 2023, arXiv preprint 2311.09589 | partial | no |
