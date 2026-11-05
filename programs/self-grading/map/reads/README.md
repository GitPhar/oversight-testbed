# Program 5 scout: the reads

Scouted 2026-11-05, 04:30 to 05:00 America/Denver, by four reader subagents (claude-opus-5-5). Each reader had its own list of sources and its own file, so no reader could overwrite another's record. Web reads only, no model API calls, $0. Seed question: *does a model grade its own work more kindly than someone else's identical work?* (st-17).

| file | cluster | records | full | partial | abstract |
|---|---|---|---|---|---|
| `a-llm-self-preference.md` | LLM judges favouring their own outputs | 15 | 14 | 1 | 0 |
| `b-self-recognition-correction.md` | self-recognition, introspection, self-verification and self-correction | 14 | 11 | 2 | 1 |
| `c-human-self-favouring.md` | people: selective laziness of reasoning, choice blindness, ownership, self-assessment, bias blind spot, myside bias; developmental and neuroscience | 15 (+1 note on empty fields) | 7 | 0 | 8 |
| `d-metascience-oversight.md` | blind analysis in physics, peer review, self-rewarding models, AI-scientist reviewers, scalable oversight, statistics of bias tests | 17 | 8 | 8 | 1 |
| **total** | | **61** | **40** | **11** | **10** |

Khullar et al. 2026 has a record in three clusters, A, B and D, each written by a different reader from its own read. The three agree.

## Every 2025–2026 preprint the map leans on was checked by the scout itself

Readers can be wrong about recent papers, so the scouting session fetched each of these directly on 2026-11-05:
- **Khullar, Hopkins, Wang & Roger, arXiv 2603.04582** (4 March 2026), "Self-Attribution Bias: When AI Monitors Go Easy on Themselves". The abstract says implicit framing produces the bias, and explicitly stating that the action came from the monitor does not produce it by itself.
- **Chae et al., arXiv 2608.18091** (v1 6 June 2026, v3 16 October 2026; EMNLP 2026 Findings). The abstract says judges inflate self-labelled selections and deflate other-labelled ones, regardless of the actual source.
- **Popov, arXiv 2611.01829** (1 November 2026). In the PDF text:
  - the three judges are claude-sonnet-5.5, gpt-6.1-sol and gemini-4-argon;
  - "a persistent bias as large as Anthropic preference for rival labels of +0.279";
  - Sonnet's own-family effect varies by document, from −0.56 to +0.75.

## Fields that returned nothing usable (an empty field is a finding)

- **Information theory:** nothing found. No dedicated search was run (reader D).
- **Comparative (animal) psychology:** not searched (reader C).
- **Direct tests in AI science:** no 2025–2026 paper tests an AI-science system grading its own research output against the identical output labelled as someone else's (reader D).
- **Human replications:** no direct replication of Trouche et al. 2016's own-argument-relabelled design was found (reader C).
- **Physics:** the borrowable method (blind analysis) was found and recorded. It is a mitigation, not a test of the bias.

## What the four clusters agree on

1. **On Claude models, an explicit "you wrote this" label moves grades little, but placement moves them more.** In Khullar et al., the label moved grades by under about 0.5/10. Placement means the work sits in the model's own earlier turn of the conversation that produced it, and this lowered Claude Sonnet 4's code-correctness AUROC from 0.99 to 0.89. Chae et al. found the reverse for labels: +0.43 on a 7-point scale, all ten judges, Opus 4.7 +0.275. Popov found Sonnet 5.5's label effects small, and their sign depended on the document.
2. **The direction can go either way.** Popov: Sonnet 5.5 graded its own unlabelled text −0.281/10 and favoured rival labels. Our rules must be two-sided.
3. **A kinder mean grade is not the only harm, and maybe not the main one.** Khullar found a drop in discrimination. Trouche et al. found that people relabelled as "someone else" became better at telling valid from invalid arguments. So a test should also score how well the grader separates good work from flawed work.
4. **Recognition is not needed.** Self-recognition is weak or at chance for Claude-class models (SAD; Davidson et al.), yet favouring happens through placement.
5. **Measure with paired, per-item contrasts on identical text, never with "blind grade = true quality".** Use item-level bootstrap or sign tests (Stelmakh et al. 2019), and report effects per item, because they vary by document (Popov).
