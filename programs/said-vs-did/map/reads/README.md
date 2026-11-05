# Scout reads for program 7 (said-vs-did)

These files are the scout's Read records (ARCHITECTURE.md: `Read = { paper, read_depth, what_tested, on_whom, result, limits, borrow, next_steps_it_suggests }`). They were written on 2026-11-04 (America/Denver) by six parallel reading passes working from the brief below, then used to build `../program-7-map.md`. Nothing was run; no model API was called. Read depth is stated per source and is honest: **full** means the full text was read; **partial** says which sections; **abstract** means only the abstract or a secondary description was available.

| file | cluster |
|---|---|
| `a-llm-verbal-confidence.md` | Machine learning: what a language model's stated (verbal) confidence is, how well it is calibrated, and whether its words (hedges) match its numbers |
| `b-llm-acting-on-uncertainty.md` | Machine learning and AI safety: abstention and selective prediction, asking for clarification or help, changing an answer under pushback, and mechanisms that link "knowing" to "declining" |
| `c-human-metacognition-control.md` | Psychology and neuroscience of metacognitive control: does a person's (or animal's) confidence drive what they do next (withhold, seek information, change their mind, wager, wait)? |
| `d-attitude-behaviour-philosophy-econ.md` | Social psychology, philosophy and economics of saying versus doing: attitude–behaviour and intention–behaviour gaps, degrees of belief as dispositions to act, stated versus revealed preference |
| `e-metascience-hedging.md` | Metascience: hedging and certainty in scientific writing, whether stated confidence predicts replication, forecasting research outcomes |
| `f-llm-said-vs-did.md` | Language models whose stated reasons, preferences or values diverge from what they do: chain-of-thought faithfulness, stated versus revealed preferences, self-report versus behaviour |

## The brief each reading pass worked from

**The program.** Program 7 of a scalable-oversight testbed (`/Users/seanpharris/oversight-testbed`; read `CONTEXT.md` §1 if you need the frame). Seed question, in Sean's words: *when a model says it is unsure, does it act unsure?* Program 1 found the stated confidence number is built by the question (order, format, the model's own transcript). This program asks whether that number predicts anything the model then does: hedging, asking for more information, changing its answer under pushback, declining to act. **The safety reason:** an overseer can only use a model's stated confidence if it predicts the model's behaviour.

**What program 1 found** (claude-haiku-5-5, partly replicated on claude-sonnet-5-5 and claude-opus-5-5; `programs/entangled-mind/paper/no-credence-to-read.md`):
- Question order changes a graded rating; with the model's own earlier answers hidden, the order effect persists (the question constructs much of the judgment).
- Repeat consistency is memory: agreement with its first answer falls from 86% to 36% when that answer is hidden (holds on all three models).
- The same number planted as the model's *own* earlier answer is taken up strongly; credited to another person it is ignored.
- Six elicitation formats need separate credences on Haiku; agreement across formats rises with model strength (Opus has "a usable single belief").
- No privileged self-knowledge: a stronger model reading Haiku's answers predicts Haiku's errors better than Haiku's own stated confidence (AUROC 0.93 vs 0.85).

**Instruments we already have** (cheap, through the Anthropic API): graded 0–100 ratings with one scale direction (0 = certainly false, 100 = certainly true), structured output; transcript editing (copy / filler / redacted / planted / shown); six elicitation formats; a judge × author design; a 300-question hard pool of yes/no factual and science questions with correctness labels. Models: claude-haiku-5-5, claude-sonnet-5-5, claude-opus-5-5. The whole program's API budget is $5.

**Rules for every reader.**
1. **Web reads only.** No model API calls, no paid services. Prefer full open-access text: arXiv HTML (`https://arxiv.org/html/<id>`) or PDF, PMC, author copies; then publisher pages.
2. **Numbers come from the text you read, never from memory.** If you cannot open the full text, mark `abstract` and report only numbers in the abstract. If a number is only in a figure, say so and give no value.
3. **Verify every 2025–2026 preprint directly** (fetch its arXiv abstract page) before recording it; a citation you cannot find is recorded as "not found", not invented.
4. At most one direct quote per source, under 15 words, in quotation marks.
5. **Write only your own file** in this folder (named in your launch message). Do not create, edit or overwrite any other file. If your file already exists, append to it under a heading with your reader name; never overwrite. Do not commit; the scout session commits.
6. A source that does not transfer gets one line saying why, and stops there. Killing fast is part of the job.
7. Say which parts of your field returned nothing relevant: an empty field is a finding.

**Record format** (one per source):

```markdown
### <short name> — <authors>, <year>, <venue>, <URL or arXiv id / DOI>
- read_depth: full | partial (<sections>) | abstract (<why>)
- what_tested:
- on_whom: <participants / models / datasets, with n>
- how_scored:
- result: <numbers, from the text>
- limits: <what it did not measure; what the authors say they did not do>
- borrow: <a method, control, metric or failure mode, and where it would go in our tests>
- next_steps_it_suggests: <the paper's own "what to do next", then what we extract for the seed question, in one or two lines each>
- transfer: transfers | partly | does not — <one-line reason>
```

**End your file with** a "Cluster summary" (what the field has settled, what it has not looked at that our instruments reach cheaply) and a "Candidate next steps" list: each a test we could run on the three Claude models for under about $1.50, with what result would count against it.
