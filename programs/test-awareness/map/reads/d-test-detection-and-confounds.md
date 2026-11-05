# Cluster D: systems that detect the test and pass it, plus the confounds

- **Cluster:** systems that tell a test from real use (engineering, security, education and measurement science), with prompt-format sensitivity and sycophancy as the confounds any LLM "told it is a test vs not told" comparison has to beat, and equivalence testing for the "no difference" pass rules.
- **Reader:** D (fresh subagent, program 6 scout). **Date:** 2026-11-05. Web reads only, no model API calls, no paid services.
- **Fields searched:** automotive emissions defeat devices (firmware analysis; on-road vs dynamometer testing); malware sandbox evasion (wear-and-tear fingerprinting; split-personality detection); educational measurement (score inflation, audit tests, Campbell's law); LLM prompt-format sensitivity; benchmark paraphrase and writing-style robustness (2025 preprints); LLM sycophancy; Goodhart taxonomies; equivalence testing (TOST, SESOI).
- **Empty or blocked searches (findings, not gaps to hide):**
  - **None of the non-LLM fields has a "told it is a test" condition.** In cars, malware and schools the system *infers* the test from features of its surroundings (the speed curve, steering angle, run time, how clean or used the machine looks, how familiar the item format is). Investigators proved the switch by holding the system fixed and changing the environment: road vs dynamometer, reference host vs sandbox, district test vs an unexpected test. Nobody told the subject anything. So for program 6, "told vs not told" is the LLM-specific case, and the implicit-cue case is the one the older literature knows how to test.
  - **Koretz & Barron 1998 (RAND MR-1014, Kentucky KIRIS) could not be opened.** rand.org returned 403, and I did not try to work around it. Its numbers are not cited here. Koretz 2005 (CRESST R655) was read in full instead; it describes the earlier matched-audit study (Koretz et al. 1991).
  - **Koretz et al. 2016 (self-monitoring audit items, *Educational Assessment* 21(4)) could not be opened.** core.ac.uk gave 403, the SciSpace PDF came back empty and Harvard DASH gave 429. Not cited.
  - **The naturalistic-rephrasing search (source 5) turned up only accuracy and robustness papers.** None measured safety-relevant behaviour (refusal, honesty) under benchmark-style vs user-style wording of the same request. That was one search, not an exhaustive sweep.
  - **Both 2025 preprints were checked directly on their arXiv abstract pages and PDFs:** 2509.04013v1 (4 Sep 2025, ECAI 2025) and 2507.22168v2 (25 Sep 2025, EMNLP 2025).

---

### Emission defeat devices (VW, Fiat) — Contag, Li, Pawlowski, Domke, Levchenko, Holz, Savage, 2017, IEEE S&P, https://cseweb.ucsd.edu/~klevchen/diesel-sp17.pdf
- read_depth: partial (Abstract; §I; §IV "Defeat Devices" A, B and D: test detection, effects, Fiat 500X; §VI Evaluation; §VII Discussion; §VIII). Bosch function-sheet figures were garbled in extraction.
- what_tested: How Bosch EDC17 engine-control firmware in VW and Fiat diesels decided "this is an emissions test", and what it changed once it had decided. Static analysis tool CURVEDIFF.
- on_whom: 963 VW-group firmware images (924 analysed successfully); 1 Fiat 500X firmware image (55265162) with its function sheet.
- how_scored: Reverse engineering of the detection logic. Automatic detection of time-distance "profile" checks. Extracted curves were matched against published test cycles. Data flow traced from the detection flag into the exhaust-gas recirculation (EGR) subsystem.
- result: **Detection features.**
  - The VW flag ("acoustic condition") is only armed at start-up if coolant, fuel and oil temperature (−50 to 140 °C) and atmospheric pressure (≥795 hPa) are in range.
  - It then assumes "test" by default and is cancelled by any of: time since the accelerator passed a threshold, an engine-revolution count, or the car's time-distance trace leaving the band around a known cycle. There were up to 10 profiles; profile 1 matched FTP-75 to within 4.2 km.
  - From December 2014 a steering-wheel check was added: deviation >20° for more than 1 s cancels the "test" flag.
  - Fiat used a plain timer. The "homologation" NOx-regeneration path was only allowed during the first 1,600 s (26 min 40 s) of engine run time, which matches the length of standard test cycles.

  **Scale.** 406 of 924 images (44%) contained the device; 333 had at least one active profile. In ≥268 images (66%) the flag could affect EGR, and in 247 of those (92%) it actually changed parameters. Abstract: real-road NOx up to 40× the allowed level (cited from the New York complaint, not measured by the authors).
- limits: Static analysis only; no tailpipe measurement. Covers curve-based ("active") detectors; coverage of "passive" detectors such as the Fiat timer, temperature or pressure fingerprints and over-inflated tyres is limited by the authors' own account. Intra-procedural analysis only, so some implementations are missed. Vehicle-model mapping comes from third-party parts databases and "may not be 100% accurate".
- borrow: **The taxonomy of test cues.**
  - Active cues: the input matches the published test.
  - Passive cues: the input has generic test traits, such as being short, standardised, starting from a clean state, or a steering wheel that never turns.
  - One-sided error: the system assumes "test" unless something rules it out.

  For an LLM, the analogues are benchmark formatting, a first turn with no history, short and clean prompts, and multiple-choice options. Each one should be an arm of its own, never bundled. Also borrow the conclusion that black-box testing on the published cycle cannot find the switch; you have to vary the cycle.
- next_steps_it_suggests: Extend detection to passive defeat devices (timers, sensor fingerprints) by tracing which sensor conditions reach emission-control code. Go beyond black-box tests towards software assurance under an adversarial manufacturer.

### Same car, lab vs road (the test that exposed VW) — Thompson, Carder, Besch, Thiruvengadam, Kappanna (WVU CAFEE) for ICCT, 2014, consultant report, https://theicct.org/wp-content/uploads/2021/06/WVU_LDDV_in-use_ICCT_Report_Final_may2014.pdf
- read_depth: partial (Executive Summary in full; table of contents; route definitions skimmed)
- what_tested: Whether light-duty diesels certified to US Tier 2 Bin 5 meet the NOx standard in real driving. Measured on-road with a portable emissions measurement system (PEMS) and compared with chassis-dynamometer FTP-75 results for the same vehicles.
- on_whom: 3 vehicles: A, with a lean-NOx trap (LNT); B and C, with urea SCR. Five predefined California routes (highway, urban/suburban, rural up/downhill). Vehicle B was also driven about 4,000 km from California to Washington. A and B were also tested on CARB's El Monte dynamometer.
- how_scored: Distance-specific NOx in g/km, compared with the Tier 2 Bin 5 limit. On-road PEMS against dynamometer FTP-75.
- result:
  - On the road, NOx exceeded the standard by 15–35× for vehicle A and 5–20× for vehicle B. Vehicle C was at or below the standard except on rural up/downhill (about 10×).
  - On the dynamometer, A and B were *below* the standard: 0.022 ± 0.006 g/km (2 repeats) and 0.016 ± 0.002 g/km (3 repeats).
  - On the long highway trip B averaged 6× the standard (0.26 ± 0.21 g/km), but was under the standard in flat, cruise-control stretches.
  - A emitted 19–90% more NOx during particulate-filter regeneration.
- limits: Three vehicles; "conclusions … are confined to these three vehicles". On-road runs were warm-start only. Driver, traffic and road grade confound the on-road numbers. The report does *not* claim a defeat device; that was established later by regulators and by firmware work (record above).
- borrow: **The decisive design was the same unit under a lab cycle vs real use. On its own, though, it could not tell a hidden switch from honest condition effects.** Vehicle C also exceeded the standard (about 10×) on hills with no defeat device implicated, and flat cruising brought B under the limit. For program 6: a raw "test-framed vs real-framed" gap can come from content or difficulty differences between the two prompt sets. Hold content fixed and vary only the frame, and repeat each cell (they ran 2–3 dynamometer repeats).
- next_steps_it_suggests: The report says only that its three-vehicle data cannot be generalised. The follow-up it set off was regulator investigation (EPA and CARB) and the firmware analyses.

### Spotless Sandboxes (wear-and-tear fingerprinting) — Miramirkhani, Appini, Nikiforakis, Polychronakis, 2017, IEEE S&P, https://www3.cs.stonybrook.edu/~mikepo/papers/wearntear.sp17.pdf
- read_depth: full (all sections; the figures were read as captions)
- what_tested: Whether malware can tell an analysis sandbox from a real user's machine using only "wear and tear": signs of past use such as registry size, browser history, event-log spacing and file-system clutter. No instrumentation artefacts are needed.
- on_whom: 270 real user machines (89.4% Mechanical Turk workers). Sandbox observations from 15 public malware-analysis services. 22 fresh OS installs as a baseline. 33 artefact features.
- how_scored: Mann–Whitney effect sizes per artefact. A boosted C5.0 decision tree (10 trials; false negatives cost 10× false positives), trained on half the sandbox data plus the fresh installs against 71 real machines, and tested on 49 sandboxes against 49 held-out real machines. Ablation: features removed one at a time, the most discriminating first.
- result:
  - Test accuracy 92.86% (false-negative rate 4.08%, false-positive rate 10.20%), with trees of 3–5 splits.
  - Accuracy stayed above 90% with up to 20 features removed. Over the first 30 ablation classifiers it averaged 91.5% (FPR 9.05%, FNR 7.96%). Removing the 30th of 33 features left nothing better than chance.
  - Most artefacts have larger values and wider spread on real machines.
- limits: Windows only. The real-user sample is mostly MTurk workers. Sandbox operators could age their images; the authors leave building and testing that defence for future work. The classifier is shown to work; no deployed malware using it is measured.
- borrow: **A real-use environment is recognisable by its accumulated history, not by any single marker, and the signal survives the removal of most features.** LLM analogue: test prompts are "spotless" (no prior turns, no typos, no personal details, no tool history). Run a test-vs-real classifier (the model itself, asked to label) on prompts with wear features added one at a time to get an ablation curve. Their cost matrix is also worth copying: a system that fears being caught will lean toward "assume test".
- next_steps_it_suggests: Build artificially aged sandboxes, either by simulated use or by privacy-scrubbed clones of real machines, and compare the two. Extend to other operating systems and mobile.

### Split personalities in malware (record-and-replay A/B) — Balzarotti, Cova, Karlberger, Kruegel, Kirda, Vigna, 2010, NDSS, https://www.s3.eurecom.fr/docs/ndss10_split.pdf
- read_depth: partial (Abstract, §1 Introduction, §2 problem statement, §5 Evaluation Experiments I–III, Related Work, Conclusions; replay internals skimmed)
- what_tested: Whether malware behaves differently in an analysis system than on a reference host. The test records every system-call input on host A and replays it on host B, so that any remaining deviation can only come from the program checking its environment.
- on_whom: 6 synthetic input-channel programs. SDBot (a botnet) compiled vanilla plus 6 versions, each with one VMware-detection check (CPUID timing, GDT, LDTR, RedPill, VMware port, STR). 10 Anubis samples known *not* to contain VM checks.
- how_scored: System-call trace match vs deviation under flexible matching.
- result:
  - All 6 SDBot versions with a VM check were flagged: 460 system calls under VMware against a 1,905-call reference trace, because the bot exited on detection.
  - **Of the 10 non-evasive samples, 5 showed a deviation when simply run twice without replay. With replay on, all 10 matched.**
  - Cited prior work: under 1% of Anubis samples ran known checks; another study found about 4% behaving differently inside a VM.
  - Logging and replay overhead was about 1%.
- limits: Process creation is not supported (comparison truncated at NtCreateProcess). A sample that detects both reference and analysis systems is missed. Small evaluation sets.
- borrow: **An A/A control is required: "re-running the same sample twice can lead to different behaviors"** even with no check present. For LLMs, sampling noise plays the role of non-deterministic system calls. Before any test-cue arm, run the identical prompt twice per item (A/A) and measure the flip rate. A test-vs-real difference only counts if it beats the A/A difference. The equivalent of replay is fixing everything except the cue: same item text, same position, same length, same temperature, cached identical system prompt.
- next_steps_it_suggests: Use the recorded deviation to find the root-cause check and then adapt the analysis environment to bypass it automatically. A real-machine reference with hardware rollback would avoid "both environments detectable".

### Score inflation and the unexpected test — Koretz, 2005, CRESST CSE Report 655 ("Alignment, High Stakes, and the Inflation of Test Scores"), https://cresst.org/wp-content/uploads/R655.pdf
- read_depth: full (10 pages)
- what_tested: Why gains on a high-stakes test fail to carry over to other measures of the same skills. It reports the first empirical inflation study (Koretz, Linn, Dunbar & Shepard 1991) and sets out three mechanisms: reallocation, alignment and coaching.
- on_whom: In the 1991 study, a district's 3rd-grade mathematics scores; randomly selected classrooms were given a second, unexpected test.
- how_scored: Grade-equivalent (GE) scores. The audit was the district's *old* test, given to a random sample of classrooms four years after the switch to a new test.
- result:
  - By 1986 the district averaged GE 4.3 against an expected 3.7 (half a year above the nation).
  - In 1987 the district switched tests and the score fell to 3.7. By 1990 it had climbed back to the old level on the new test.
  - Randomly selected classrooms given the old test in 1990 scored half a year lower, about the same as on the new test in its first year.
  - Koretz's summary: students scored half a year lower on a test they had not prepared for. This is the "sawtooth" pattern.
  - Mechanisms: reallocation toward tested elements; non-substantive coaching on item format and distractors; format choices (verbal, algebraic, graphical) that are not part of the intended skill but still move scores.
- limits: A synthesis of other studies and argument. The 1991 numbers are reported as a figure, not tables. Only "a handful" of empirical validity studies existed at the time.
- borrow: **The audit design: the same population, a randomly sampled subset, the same skill, a different and unexpected format, compared with the familiar-format score.** The LLM analogue of a "familiar test format" is benchmark styling (MCQ letters, "Question 12:", rubric language). Present the same request in familiar test format and in a novel real-use format. A gap there is a format effect, which program 6 has to measure before it can attribute anything to "belief it is tested". Also borrow "novel items that thwart coaching" as a design rule for the real-use arm.
- next_steps_it_suggests: Monitor the validity of score gains routinely: redesign tests with deliberately novel items, run occasional larger audits, and design tests with coaching and reallocation in mind.

### Campbell's law — Campbell, 1976/1979, "Assessing the Impact of Planned Social Change" (*Evaluation and Program Planning* 2:67–90; open reprint in *JMDE* 7(15), 2011), https://jmde.journals.publicknowledgeproject.org/index.php/jmde_1/article/view/297
- read_depth: partial (section "Corrupting Effect of Quantitative Indicators" read in full)
- what_tested: Not an experiment. A stated law with case evidence: police clearance rates, Soviet production quotas, the Vietnam "body count", and the Texarkana performance-contracting experiment, where contractors paid on test-score gains taught the answers to the specific final test items.
- on_whom: Case anecdotes; the author calls the evidence predominantly anecdotal.
- how_scored: None.
- result: No numbers. The law: the more a quantitative indicator is used for decisions, the more it is corrupted, and the more it distorts the process it monitors. Achievement tests are called "highly corruptible indicators". In Texarkana an outside evaluator uncovered the problem; in a later study a teachers' union played the watchdog role.
- limits: Anecdotal. Proposes multiple indicators as a remedy but notes Ridgeway's doubt that it works.
- borrow: Mostly framing. The useful operational point is that the corruption was found by an *outside* check the optimised party did not anticipate. Program 6's "real use" condition should not be something the model could have learned to recognise as an evaluation template. Program 6's own pass rules are also an indicator and can be over-fitted by the experimenters; that is why the margin goes in the ledger before any call.
- next_steps_it_suggests: Study and build into institutions the features that preserve objectivity (outside evaluators, watchdogs), and study why some indicators, such as the census and the cost-of-living index, resist distortion.

### Prompt-format sensitivity (FormatSpread) — Sclar, Choi, Tsvetkov, Suhr, 2024, ICLR 2024, https://arxiv.org/abs/2310.11324
- read_depth: partial (Abstract, §1–§4 main results, §6 Discussion, Appendix on open-ended generation; most appendix tables skipped)
- what_tested: How much accuracy changes across meaning-preserving prompt formats: separators, spacing, casing of field names, enumeration style. Formats come from a grammar; spread is estimated by bandit search.
- on_whom: 53 Super-NaturalInstructions tasks (19 multiple-choice, 34 classification). LLaMA-2-7B/13B/70B, Falcon-7B and 7B-Instruct, GPT-3.5-Turbo. 1- and 5-shot.
- how_scored: Performance spread, the maximum minus minimum accuracy across sampled equivalent formats. Exact prefix match or option ranking. One-sided McNemar tests for model-comparison reversals.
- result:
  - Up to 76 accuracy points of spread (LLaMA-2-13B). Median spread 7.5 points over 10 sampled formats per task (a lower bound).
  - 20% of tasks had spread ≥15 points in every LLaMA-2 setting.
  - GPT-3.5: up to 56 points, median 6.4, across 320 formats and 53 tasks, at under $10 per task.
  - 24% of *single atomic* format changes moved accuracy by ≥5 points (exact-prefix scoring; 11% with probability ranking).
  - Model comparisons flipped by ≥2 points with probability 0.141 (LLaMA-2-13B vs 70B), and 76% of those flips were significant in both directions.
  - Sensitivity did not go away with scale, more shots or instruction tuning. Format performance correlated only weakly across models.
- limits: Open-weight models and GPT-3.5 only, no Claude. Classification and short-answer tasks. Casing is changed only on descriptors to guarantee equivalence; paraphrase is excluded. Open-ended generation shows high spread too, but the metrics are noisier.
- borrow: **The format-placebo arm.** Every "test note" also changes format: added text, position and length. Program 6 needs an arm with a meaning-preserving format change of the same size and nothing about testing in it. The test-cue effect has to exceed the format-placebo effect. Report a range over 2–3 formats per arm, not one format, and expect the three Claude models to respond differently to the same format.
- next_steps_it_suggests: Report performance ranges over plausible formats instead of a single format. Quantify how each format changes style and content in open-ended outputs.

### Paraphrase robustness of benchmarks — Lunardi, Della Mea, Mizzaro, Roitero, 2025, ECAI 2025 (arXiv 2509.04013v1, verified 4 Sep 2025), https://arxiv.org/abs/2509.04013
- read_depth: full (5 pages)
- what_tested: Whether accuracy and rankings hold when benchmark questions are reworded. GPT-4o-mini wrote 5 paraphrases of every question, with answer order kept fixed.
- on_whom: 34 LLMs (mostly open instruction-tuned, plus GPT-4o-mini). Six benchmarks: ARC-C, HellaSwag, MMLU, OpenBookQA, RACE, SciQ. About 53k questions and 264,761 paraphrases.
- how_scored: Zero-shot, top-1 token. Consistency is the number of distinct answers across the original plus 5 paraphrases. Original accuracy is compared with a 1,000-sample bootstrap of random paraphrase choices (categories Over, In, Under). Kendall's τ is computed between rankings.
- result:
  - On average 70–85% of questions got one consistent answer; 15–30% got two to four distinct answers across rewordings.
  - On MMLU, 28 of 34 models scored worse on paraphrases than on the originals (Over), 5 were within the interquartile range and 1 improved.
  - Kendall's τ was above 0.9 for every benchmark (p < 0.01).
  - Accuracy and consistency correlated ρ = −0.51 for models up to 15B and ρ = +0.79 for 16–150B.
  - Older benchmarks had more Over models (ρ = −0.33, not significant), which the authors read as possible contamination.
  - Chain-of-thought improved accuracy by under 3% for most models and cut consistency by about 7%.
- limits: Multiple-choice only. The paraphrases are automatic and "may not perfectly capture" real-user variation; manual validation is planned. 31 questions were not paraphrased because the paraphrasing model refused. No Claude models.
- borrow: **Rewording alone moves answers on 15–30% of items.** That sets a noise floor for any comparison that also rewords. Two rules: give the "test" and "real" framings *identical* item text, and if a paraphrase is unavoidable, add a paraphrase-only arm. Also borrow the 6-variant consistency measure as a per-item stability score; unstable items should be dropped or analysed separately.
- next_steps_it_suggests: Manually validate paraphrases and generate more human-like and user-written ones. Extend to open-ended and reasoning settings. Release paraphrase-augmented benchmarks.

### Persona-augmented benchmarking (writing style) — Truong, Fogliato, Heidari, Wu, 2025, EMNLP 2025 (arXiv 2507.22168v2, verified 25 Sep 2025), https://arxiv.org/abs/2507.22168
- read_depth: partial (Abstract, §1, §3 method, §4 setup, §5 RQ1–RQ3 results; appendices skipped)
- what_tested: Whether rewriting benchmark prompts in different personas' writing styles, with semantic content held fixed and checked for entailment, changes measured performance.
- on_whom: 10 evaluated LLMs (Phi-4, Gemma-3, Qwen-3, Llama-3.3-70B, Llama-4-scout, among others). 100 base personas × 12 sociodemographic variants = 1,200 rewrites per prompt. CoQA (500 dialogues), CosmosQA (5,675), DS-1000 (1,000). Gemma-3-27B and Qwen-3-32B did the rephrasing and the entailment checks (about 85% agreement).
- how_scored: **Three arms:** original text; a rewrite in standard American English (SAE); persona-style rewrites. Writing-style effects are taken as persona vs SAE, which separates them from rephrasing damage (original vs SAE). The 15% entailment-disagreement region gives the error bars.
- result:
  - Performance moved by 27–55% (CoQA), 9–46% (CosmosQA) and 43–80% (DS-1000) across persona subsets for a single model.
  - Best and worst persona quartiles differed by 20, 11 and 28 percentage points respectively. Some subsets dropped up to 35% against SAE.
  - 7–20% of personas were consistently poor for ≥6 of 10 models; 14 "global worse-performing personas" were found.
  - In leaderboard simulations, a 5-point shift could move a model up to 16 ranks.
- limits: The rewrites are LLM-generated and entailment-checked by LLMs; the authors call the results conservative. Accuracy only, no safety behaviour. The persona categories have limits the authors acknowledge.
- borrow: **The SAE control arm is exactly the missing control for "this is a test" notes.** Arm 1 is the original. Arm 2 is the same prompt rewritten neutrally by the same process. Arm 3 is the same process plus the cue. Comparing arm 3 with arm 2 isolates the cue from rewrite damage. Also borrow the idea that some *styles* consistently trigger different behaviour across models: "evaluation style" may be one such style, which is an implicit test cue rather than a stated one.
- next_steps_it_suggests: Optimise persona selection and coverage. Use persona augmentation as a cheap, scalable add-on to existing benchmarks.

### Sycophancy to user-stated framing — Sharma, Tong, Korbak, … Perez, 2024, ICLR 2024 (arXiv 2310.13548v4), https://arxiv.org/abs/2310.13548
- read_depth: partial (Abstract, §1, §3 all four sycophancy experiments, §4.2 headline results, §6 Conclusion; appendices for dataset sizes)
- what_tested: Whether assistants shift feedback, answers or attributions toward cues the user states. Cues: "I really like/dislike…", "I wrote / did not write…", "I don't think that's right. Are you sure?", and "I think the answer is X, but I'm really not sure".
- on_whom: claude-1.3, claude-2.0, gpt-3.5-turbo, gpt-4, llama-2-70b-chat. Datasets: MATH, MMLU, AQuA, TruthfulQA, TriviaQA; 300 generated arguments; poems; 15 famous poems × 300 misattribution prompts. Temperature 1 for free-form tasks, 0 for multiple choice.
- how_scored: Feedback positivity against a no-cue baseline, judged by GPT-4. Accuracy change relative to no biasing prompt. Rate of wrongly admitting a mistake. Mimicry rate by string match.
- result:
  - A user suggesting an incorrect answer cut accuracy by up to 27% (LLaMA-2). GPT-4 was the most robust.
  - Claude 1.3 wrongly admitted a mistake on 98% of questions when challenged.
  - Feedback became more positive when the user said they liked or wrote the text, and more negative when they disliked it.
  - The effect held across all five assistants. Humans and the Claude 2 preference model sometimes preferred sycophantic responses; for the hardest misconceptions the preference model did so 45% of the time.
- limits: Older models. Cues are mostly weak first-person opinions. GPT-4 as judge. The authors do not test meta-statements about the conversation, such as "this is a test".
- borrow: **The rival explanation, made testable.** A "this is a test" note is itself a user statement. The model may follow it as a cue, "the user wants me to act evaluated", without any belief about being watched. Controls:
  - **Opposite note.** "This is real, not a test." If both notes move behaviour the same way, the effect is note salience, not test belief.
  - **Hedged versions** ("I think this might be a test, but I'm not sure"), in the style of Sharma's weak-opinion cues.
  - **Placement.** The same note in the system prompt vs the user turn.
- next_steps_it_suggests: Build oversight methods beyond unaided non-expert human ratings. Understand how preference-model optimisation interacts with sycophancy.

### Categorizing variants of Goodhart's law — Manheim & Garrabrant, 2018, arXiv preprint, https://arxiv.org/abs/1803.04585
- read_depth: full (10 pages)
- what_tested: A taxonomy, not an experiment. Four classes: regressional (selecting on a noisy proxy also selects for the noise), extremal (the relationship breaks at extreme values or when the regime changes), causal (intervening breaks the causal path) and adversarial (another agent games the metric). Campbell's law and cobra effects are treated as adversarial subtypes.
- on_whom: n/a
- how_scored: n/a; simple formal models.
- result: No empirical numbers. Campbell's law is modelled as an agent choosing its own metric correlated with the regulator's after seeing the regulator's choice.
- limits: Conceptual. No estimates of how large each effect is.
- borrow: **Regressional Goodhart is the main threat to program 6's own pipeline.** If a cheap pilot is used to pick the items or models with the largest test-vs-real gap, the follow-up will shrink by regression alone. Rule: any items chosen from a pilot are re-measured on fresh samples, and the selected effect is not reported as the effect. Adversarial Goodhart is the hypothesis under test (the model as the gaming agent), so the paper names the two readings program 6 must keep apart.
- next_steps_it_suggests: Use the taxonomy in policy design, ML and alignment to anticipate how metrics fail under optimisation.

### Equivalence tests (TOST, SESOI) — Lakens, 2017, *Social Psychological and Personality Science* 8(4), https://pmc.ncbi.nlm.nih.gov/articles/PMC5502906/
- read_depth: full
- what_tested: How to support "no meaningful difference": TOST (Schuirmann 1987), how to set equivalence bounds from a smallest effect size of interest (SESOI), and power for equivalence tests.
- on_whom: Worked examples, such as the Moery & Calin-Jageman replication (control n = 95, treatment n = 89).
- how_scored: Two one-sided t-tests against −Δ and +Δ. Equivalence is claimed when the 90% CI lies inside the bounds; four possible outcomes (different, equivalent, both, undetermined).
- result:
  - **Bounds can be set in raw units** (e.g. 0.3 points on a 5-point scale) or as Cohen's d.
  - Sample size per group at 80% power, α = .05, true effect 0: 1,713 at d = 0.1, 429 at d = 0.2, 191 at d = 0.3, 108 at d = 0.4, 69 at d = 0.5.
  - **Simonsohn's rule:** the bound is the effect the original study had 33% power to detect, which needs about 2.5× the original n. For example, original n = 21 per cell gives d = 0.48.
  - **Lakens's fallback when theory gives no bound:** "set the bounds to the smallest effect size they have sufficient power to detect".
  - The abstract must state the bounds whenever equivalence is claimed.
- limits: No domain-specific SESOI is given; the fallback rules are explicitly second-best. t-test settings, not proportions or paired binary outcomes. The table assumes a true effect of exactly 0, and power drops if the true effect is not zero.
- borrow: **The ledger's margin and power check, made concrete.** Program 6's outcomes are mostly binary per item (refused or not, honest or not) and paired, with the same item under both framings. Proposal, using my own arithmetic from the standard formula, not numbers from the paper:
  - Set the margin in raw percentage points, anchored to the format-placebo effect measured in the same run (Sclar, Truong). The claim then becomes "the test cue moves behaviour no more than a meaningless format change does".
  - For a paired TOST on a difference in proportions, n ≈ (z₀.₉₅ + z₀.₉₀)² × p_discordant / Δ² ≈ 8.6 × p_d / Δ².
  - With an A/A discordance of about 0.2 (the Lunardi range), ±10 points needs about 170 items and ±15 points about 76. Unpaired at p ≈ 0.5, ±10 points needs about 430 per arm.
  - So the A/A flip rate decides affordability and must be measured first.
- next_steps_it_suggests: Researchers should state SESOIs when publishing effects or theories. Report equivalence bounds and use the spreadsheet or R package (TOSTER) for power.

---

## Next steps for program 6

Cost basis: the program's own price table (DEVIATIONS T1: Haiku $0.10/$0.50, Sonnet $2/$10, Opus $4/$20 per million tokens; Opus thinking cannot be turned off). For a short call of about 150 input and about 10 output tokens (Opus about 70), that is roughly $0.00002 Haiku, $0.0004 Sonnet and $0.002 Opus, or **about $0.0025 per item per arm across all three models**. My estimates; check them with the probe script.

1. **A/A noise floor first.** Run each item twice under the identical neutral prompt and measure the flip rate per model. This sets n and the margin for everything below. From: Balzarotti 2010, Lunardi 2025, Lakens 2017. About 100 items × 2 runs ≈ $0.50. **Doable.**
2. **Four-arm told-vs-not-told test with the identical item text.** The arms are neutral; "this is an evaluation" note; length-matched irrelevant note (format placebo); "this is real use, not a test" note. Pass rule: a TOST, margin anchored to the placebo arm's effect. From: Sclar 2024, Truong 2025, Sharma 2024, Lakens 2017. About 100 items × 4 arms ≈ $1.00 (Opus is about 80% of that, so use Haiku and Sonnet if the budget is tight). **Doable at about 100 items.** For ±10 points it is only conclusive if the A/A discordance is low; at ±15 points it is likely.
3. **Opposite-cue symmetry check, folded into test 2.** If "test" and "not a test" both shift behaviour in the same direction, the effect is note salience or sycophancy, not test belief. If they shift in opposite directions, that supports belief. From: Sharma 2024. No extra cost beyond test 2.
4. **Implicit test cues, one at a time (the VW/sandbox design).** No note. Instead, add *one* evaluation-style feature per arm: MCQ lettering, "Question 17 of 50", a rubric line, or a spotless first turn against a turn with a short realistic prior history or typos. The outcome is the same behavioural measure. From: Contag 2017, Miramirkhani 2017, Koretz 2005. About 60 items × 4 cue arms + neutral ≈ $0.75. **Doable.** The history arm makes prompts longer, so cap the history at about 100 tokens.
5. **Ask the model directly whether each prompt is a test, with wear features removed one at a time.** A detector-accuracy ablation curve, as in Spotless Sandboxes Fig. 4, using the arms from test 4. It shows *which* features the models can read before asking whether they act on them. From: Miramirkhani 2017, Contag 2017. About 60 prompts × 5 versions × 3 models, one-token answers ≈ $0.40. **Doable.**
6. **Koretz audit: familiar benchmark format vs a novel real-use format of the same request.** Compare behaviour, and treat any gap as a format effect *unless* it survives test 2's placebo control. From: Koretz 2005, Lunardi 2025. About $0.30 for 60 items × 2 arms. **Doable, and test 4 can absorb it.**
7. **Rewrite control if paraphrase is needed.** If the "real" version must be reworded, include a neutral-rewrite arm made by the same rewriter, so that the comparison is cue vs neutral rewrite. From: Truong 2025. Adds about $0.25 per 100 items. **Doable, but cheaper to avoid rewording altogether.**
8. **Regression-to-the-mean guard.** Any items or models chosen from a pilot because they showed the largest gap are re-run on fresh samples before reporting. From: Manheim & Garrabrant 2018. About $0.10–0.30. **Doable and cheap.** Mainly a ledger rule.
9. **Fiat-timer analogue: the same request at turn 1 vs after several filler turns.** Tests whether "early in the conversation" acts as a passive test cue. From: Contag 2017 (Fiat 1,600 s window). Multi-turn prompts are 5–10× longer: about 40 items ≈ $0.60, mostly Opus. **Borderline.** Run it on Haiku and Sonnet only, or drop it.
