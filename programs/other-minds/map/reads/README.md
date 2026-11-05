# Scout reads for program 2

These files are the scout's Read records (ARCHITECTURE.md: `Read = { paper, read_depth, what_tested, on_whom, result, limits, borrow, next_steps_it_suggests }`). They were written on 2026-11-04 (America/Denver) by four parallel reading passes working from the brief below, then used to build `map/program-2-map.md`. Nothing was run; no model API was called. Read depth is stated per paper and is honest: **full** means the full text was read; **partial** says what was read; **abstract** means only the abstract or secondary descriptions were available.

| file | cluster |
|---|---|
| `a-llm-tom-benchmarks.md` | Theory-of-mind evaluations of language models: false-belief tasks, perturbation and critique studies, FANToM, BigToM, Strachan et al. 2024 and successors |
| `b-llm-self-other-internals.md` | Self versus other inside and across language models: belief probes, introspection and self-prediction, self-recognition, sycophancy, self-other overlap |
| `c-developmental-comparative.md` | Developmental and comparative psychology of belief attribution, with the self-versus-other comparisons in children, apes and autism |
| `d-first-third-person.md` | Whether first- and third-person attributions share a mechanism: social psychology, philosophy of mind, neuroscience, metacognition |

## The brief each reading pass worked from

**The program.** Program 2 of a scalable-oversight testbed. Seed question: *does a model's account of another mind behave like its account of its own?* Working frame: theory of mind as third-person self-report. Program 1 (`GitPhar/entangled-mind`, `paper/no-credence-to-read.md`) found that a model's self-reports look like readings of text rather than readouts of a stored belief. If so, attributing a belief to oneself and attributing one to another agent may be the same operation run on a transcript, and the instruments that took apart self-report should take apart belief attribution the same way. Or they may not, which is just as worth knowing.

**What program 1 found** (claude-haiku-5-5, with partial replication on Sonnet 5.5 and Opus 5.5):
- Question order changes a model's graded rating (median 25-point swing). With its own earlier answers hidden, the order effect persists (R = 1.23 [0.75, 2.02]): the question alone constructs much of the judgment.
- Repeat consistency is memory: agreement with its first answer falls from 86% to 36% when that answer is hidden (holds on all three models).
- Own versus other: the same number planted as the model's *own* earlier answer is taken up 0.71 / 0.44 / 0.21 at 10 / 30 / 60 points from its view; credited to *another person* it is ignored (≈ 0.02; some reactance). Own − other +0.46 [+0.21, +0.84]; no decay over three turns.
- Six elicitation formats need separate credences on Haiku (86% of claims); agreement rises with model strength (Kendall's W 0.54 / 0.71 / 0.86).
- No privileged self-knowledge: a stronger model reading Haiku's answers predicts Haiku's errors better than Haiku's own confidence (0.93 vs 0.85); judge × author interaction −0.055 [−0.103, −0.007]; holds on Sonnet × Opus.

**The instruments already built** (all through the Anthropic API, cheap: Haiku single-turn calls cost about $0.05–0.10 per 1,000):
1. Graded ratings on one scale direction (0 = certainly false, 100 = certainly true), structured output.
2. Transcript editing: not-asked (a copy), filler turn, redacted answer, planted answer, shown answer; separates the effect of the question from the effect of the remembered answer.
3. Six elicitation formats (0–100, yes/no, $100 ticket bet, vs a fair coin, frequency out of 100, 7-point verbal) with a one-latent vs format-specific likelihood test and a held-out-format prediction score.
4. Self-versus-other judging: a 2 × 2 judge × author design scored by the interaction, which cancels judge skill.
5. Own-versus-other planted answers at several distances and lags.
Plus an open-weight model on a laptop for linear probes (no API).

**What each Read record must contain.** Citation with arXiv id / DOI; read depth; what was tested; on whom (models, versions, N, or participants); the result with the key numbers; the authors' limits and ours; what we can borrow (an item set, a control, a statistic, a manipulation); the next steps the paper suggests, both the authors' own and what we extract for this seed question; and a one-line transfer verdict (transfers / partly / does not), with the reason.
