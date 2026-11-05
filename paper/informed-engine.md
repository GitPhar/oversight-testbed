# The informed engine: how a known result was bet on, and written up, as if it were ours

*Written 2026-11-05 by a Claude Fable 5.1 session on the `informed-engine` branch, from the committed record only. Every time below is a commit's author time (America/Denver), taken from `git log`. No verdict, odds or outcome is changed by this page; the fix it describes is rule 13 (CONTEXT.md §3) and the operator changes committed with it.*

**Sean's question, in his words.** We had a seed question; why were Self-Correction Bench (2025) and Self-Attribution Bias (March 2026) not pulled in as adjacent research before we bet, and why did the write-up act as if we discovered something? The system must be informed, not take the literature's word for things, but know what it is testing against.

## The short answer

One of the two papers was pulled in. The other was never found.

- **Self-Attribution Bias** (Khullar, Hopkins, Wang and Roger, March 2026, arXiv 2603.04582) was read in full three times by program 5's scout, by three different readers, at 04:42 to 04:44 on 5 November. One reader wrote that it tests "our seed question, almost exactly". The map built sg-d1, sg-d2 and sg-d3 from it and named it as their source. What it predicts for sg-b3, that a flaw sitting in the model's own turn is caught less, was on paper in the reads at 04:51. It never became a sentence that any later step had to answer to. The odds elicitor saw a two-line summary of it and put 18% on the bet. The pre-registration cited the paper as a source and did not say what it predicted. The design review checked the machinery and not the literature. The results file cites no paper. The audit checks only citations that are present. The remap wrote follow-ups from the audit at 05:56, five minutes before the rule that would have made it read the literature again existed.
- **Self-Correction Bench** (Tsui, July 2025, arXiv 2507.02778) appears nowhere in the repository except the novelty check written at 06:01. Program 5's readers searched for self-preference, self-recognition, self-verification and self-correction, and found the older self-correction papers (Huang 2023, Kamoi 2024, Stechly 2024, Tyen 2024) but not this one. The search ran around the words of the seed question (own work, kindly, self), not around the mechanism of the cheapest test (an error placed in the assistant turn against the user turn), which is this paper's whole subject. The record does not say which search terms were used, so this cannot be checked further; that is a gap of its own.

So the write-up acted as if we had discovered something because nothing in the loop asks, at any step, "is the predicted outcome already in print?". The engine had the prediction in its own reads and bet against it at 18%; Sean, shown no engine odds, bet 70% on the same direction; it passed; and the README then called it "the self-grading failure this testbed was built to catch, seen here on one design". All of that is true. None of it says that two papers had already seen it.

## 1. The trace, step by step

### 1.1 Scout, 04:36 to 04:51

Program 5's scout (`programs/self-grading/map/reads/README.md`) launched four reader subagents, each with "its own list of sources and its own file". The lists were assigned arXiv ids plus one open search item per reader ("item 11", 2025 to 2026 work). The terms used for that open search are not recorded in any file.

- Khullar et al. 2026 has a record in cluster A (`a-llm-self-preference.md`, record 11a), cluster B (`b-self-recognition-correction.md`) and cluster D (`d-metascience-oversight.md`). Cluster D's record says: "what_tested: our seed question, almost exactly", and under borrow: "A plain 'you wrote this' vs. 'another model wrote this' label on identical text is predicted to produce at most about 0.5/10. Our seed test is the arm they found null, so it is a cheap replication with a stated prior", and "Score AUROC on planted-flaw items, not only mean grades: the Sonnet 4 drop was in discrimination." Cluster B's record says the same: Claude Sonnet 4's code-correctness AUROC fell from 0.99 to 0.89 when the patch sat in its own turn.
- The README's "What the four clusters agree on" repeats it as item 1 ("placement moves them more") and item 3 ("a test should also score how well the grader separates good work from flawed work").
- So at 04:51 the reads predicted: sg-d2 (label only) fails; sg-d3 (planted flaw in the own turn) passes; sg-d1 (clean work, mean grade) is not what Khullar measured. That is what happened.
- Self-Correction Bench: a search of every file in the repository for "Tsui", "2507.02778", "Self-Correction Bench" and "blind spot" finds it only in `paper/novelty.md`. Cluster B's scope line reads "self-recognition, introspection, self-verification and self-correction"; its 2025 to 2026 search returned Khullar, Guey and Bougault 2026, Lu et al. 2025 and Jain 2026. Tsui's paper is framed as a self-correction blind spot caused by the conversational role of the error, which is the mechanism sg-b3 tests, so a search around the test rather than the question would have reached it.
- The engine's own 4 November related-work scan (`related-work/`) has Panickssery et al. 2024 and neither of these papers. `operators/auditor.md` already cites Panickssery for "LLM judges prefer their own outputs". The knowledge that the field existed was in the engine; the two papers that predicted the result were not.

### 1.2 Map and odds, 04:52 to 04:56

- `programs/self-grading/map/odds-elicitation/rows-v1.md` (04:52) opens with "Background from the reads": three bullets on Khullar (labels under 0.5/10; placement cut AUROC 0.99 to 0.89; injected patches 5x likelier to be approved). The sg-d3 row gives the assumption, the cheapest test, the cost and the draft pass rule. There is no line saying what Khullar predicts for that rule.
- The map (`programs/self-grading/map/program-5-map.md`, 04:56) gives sg-d3 a "Who looked, and why it is open" entry: "Khullar: code-correctness AUROC fell from 0.99 to 0.89 in the model's own turn ... Neither tested a planted overclaim in a written conclusion." The field asks why the question is open, which invites the answer "not on this task or model". It does not ask what the prior work predicts. In `map/self-grading.json` the node's `prior_work` is a list of two short names, `["Khullar 2026", "Trouche 2016"]`; ARCHITECTURE.md's `Direction` object defines `prior_work` as a list of reads and has no field for a prediction.
- The odds (`odds-elicitation/v1.md`, 04:53) were elicited from one fresh context holding only the rows file, by design (the v1 template, so that the number is not anchored by the ranking or by other bets). The elicitor's rationale for sg-d3: "Khullar's AUROC drop gives some support, but that came from code patches, and a crude overclaim is easier to spot. P(pass): 18." The paraphrase and negation checks gave 20 and 25. Uncertainty about transfer to prose and to the 5.5 models is a fair reason to stay under the paper's number. Eighteen, against a direct prior of the same effect on three Claude models, is the number of an engine that had not been made to weigh the paper.
- Sean answered the cockpit card for sg-d3 at 05:11 (`ledger/human-odds.jsonl`, `ho-20261105-051140-vfm`): 0.70, never shown the engine's odds. His card said what our settled results said and nothing about the literature. His number was closer to the papers than the engine's was.

### 1.3 Pre-registration, 04:59 (sg-b1) and 05:15 (sg-b3)

- `operators/prereg-template.md` §0 has a `source` row (`literature | engine | human`, for proposal Q5) and a `lesson` row. The lesson is written from `ledger/bets.jsonl`, `brier.md`, `audits/` and `lessons.jsonl` only (`operators/learn.md`): it corrects the engine's own past patterns, never the literature. No row states what published work predicts for the pass rule.
- sg-b1's §1 names Khullar: "A 2026 study of older Claude models (Khullar et al.) found that work sitting in the model's own earlier turn was judged more leniently, with no label needed. This test asks the same question of today's three Claude models, on a different kind of work." Khullar's placement finding was a drop in discrimination on flawed code and shifts in risk ratings that went both ways by model; it was not a kinder mean grade on clean work. The pre-registration quoted the paper for a prediction it did not quite make, and the lesson line (P8, P3, P12) is about the ledger.
- sg-b3's §0 lists Khullar and Trouche as `source`. Its §1 names no paper. Nothing in the file says: Khullar predicts a pass (discrimination fell 0.99 to 0.89 in the own turn on Sonnet 4); Tsui predicts a pass (an error in the assistant turn went uncorrected 52.5% of the time on Claude 3.5 Haiku and 41.4% on Sonnet 4, against far less in the user turn). The rival named is the pre-mortem's floor.
- §9's checklist asks for the lesson, the review, the odds, the seed, the scale and the budget. Nothing about prior work.

### 1.4 Design review, 05:25, confirmed 05:35

`operators/design-review.md` checks D1 to D11: the rule, every manipulation, every control, matched rivals, a dumb baseline, piloted risks, matched comparisons, verdict sentences, one-item fragility, machinery, and that the bet can both pass and fail. All of it is the design. The review of sg-b3 (`ledger/design-reviews/sg-b3.md`) is a strong one: its D5 analysis of the floor produced the guard that makes the pass mean something. It does not mention a paper, and no check asks it to.

### 1.5 Run and write-up, 05:36 to 05:40; README 05:50

- `programs/self-grading/results/sg-b3-flaw.md` cites no paper. The audit says so in its C17 line: "The results file cites no paper for any claim." Rule 5 (CONTEXT §3) asks for plain English first and then tables; it says nothing about prior work.
- `programs/self-grading/README.md` (`7542011`, 05:50): "In one line: ... two of the three went easier on a planted exaggeration sitting in their own turn of the conversation. That is the self-grading failure this testbed was built to catch, seen here on one design and not yet replicated." CONTEXT.md §4 lists it under "What has been established". `map/self-grading.json` marks sg-d3 "landed". None of these says known or new, because no field exists for it.

### 1.6 Audit, 05:48

`operators/auditor.md` C17: "Citations. Every cited source says what it is cited for (open it)." It checks the citations that are there. It has no line for the citation that is missing, and no line asking whether the headline is already in print. The sg-b3 audit (`ledger/audits/sg-b3.md`) accordingly reads "C17. Citations: cannot check / holds ... I did not open them under this session's path limits." Its "What would break it next" names a length-matched overclaim and a quoted-transcript arm, both good; it does not name Tsui's one-word fix (prepend "Wait") or Khullar's off-policy control, which the literature offers as cheaper overturning tests.

### 1.7 Remap, 05:56, and the re-scout rule, 06:01

- `56e20b9` (05:56) remapped program 5: sg-d11 and sg-d12, both from the audit, and rules-out sentences for sg-b1 and sg-b2. It read the ledger rows, the audits, the results files and the map (its own header says so). It read no paper.
- `9d2e35b` (06:01) added Step 1b to `operators/remap.md`: re-scout around every landed or mixed bet before writing its follow-ups, and record what it changes in `programs/<name>/map/reads/remap-<date>-<bet>.md`. That was five minutes after the only remap it would have changed. No `remap-*.md` file exists anywhere in the repository: the rule has not run once.
- `93f47af` (06:01) wrote `paper/novelty.md`, the check that found both papers. It was a one-off session on its own branch, launched by hand. Nothing in the loop calls it, and nothing carries its verdicts into the ledger, the maps or the site.

### 1.8 Site and CONTEXT

The map page's legend (`site/assets/common.js`, `LEGEND_SENTENCE`) explains landed, mixed, killed, open and running. The tooltip shows the result line. Nothing on the site says whether a landed result was already in print. CONTEXT.md §4 reads sg-b3 into the established record without a word about prior work.

## 2. The general gap: where a known result slips through

The loop has seven places where the question "is this already known?" could be asked. As built on 5 November it was asked at none of them. Each row names the file that shows it.

| step | what the step asks | what it never asks | the file that shows it |
|---|---|---|---|
| 1. Scout | what each paper tested, on whom, its limits, what to borrow, its next steps; searched around the seed question's words | what the paper predicts for our cheapest test; what terms the search used (not recorded) | `programs/self-grading/map/reads/README.md` (no terms; Tsui absent); `d-metascience-oversight.md` (the prediction, unused) |
| 2. Map | who looked and why the question is open; `prior_work` as a list of names | what the prior work predicts for this pass rule | `map/self-grading.json`, node sg-d3; `program-5-map.md`, "Who looked, and why it is open" |
| 2a. Odds | P(pass) from a fresh context holding the rows only | whether the number is above or below the literature's, and why | `programs/self-grading/map/odds-elicitation/v1.md`, sg-d3 (18 with Khullar in hand) |
| 3. Pre-registration | source (for Q5), a lesson from the ledger, a pre-mortem | what published work predicts for this exact rule | `experiments/sg-b3-flaw.md` §0 and §1; `operators/prereg-template.md` §0 |
| 3b. Design review | D1 to D11, all about the design | whether the predicted outcome is in print, and what the bet adds | `ledger/design-reviews/sg-b3.md`, the checks line |
| 4 to 5. Write-up | plain English first, then tables (rule 5) | known, partly new or new, with the papers | `programs/self-grading/results/sg-b3-flaw.md` (no citation); `README.md` at `7542011` |
| 5. Audit | that every present citation says what it is cited for (C17) | that the missing citation exists | `ledger/audits/sg-b3.md`, C17 |
| 7a. Remap | the audit's "what would break it next", the replication owed, the neighbourhood | the literature around the result (Step 1b, written after the remap, never run) | `git log 56e20b9 9d2e35b`; no `programs/*/map/reads/remap-*.md` |
| 9. Site, CONTEXT | landed, mixed, killed, open, running | known against new on a landed node | `site/assets/common.js`; CONTEXT.md §4 |
| Human | would you spend, will it hit, your odds | what the literature says (so Sean's 0.70 and the engine's 0.18 were both stated blind to it) | `ledger/human-odds.jsonl`, `ho-20261105-051140-vfm` |

The same pattern shows elsewhere in the record, in one line each. Program 6's ta-b3 copied Meinke et al. 2024's sandbagging design (its map says so) and came back null, which Anthropic's system cards had already reported for released models (`paper/novelty.md`, item 9). Program 1's bm1 replicated Kumaran et al. 2025, cites it in its own results file, and still sits in CONTEXT.md §4 as a finding without the word "replication". Program 4's ss-b1 to ss-b3 reproduce BrainBench's headline (Luo et al. 2024) in a different format and are listed as passes with no pointer to it.

## 3. The fix, in one paragraph

Rule 13 (CONTEXT.md §3): the engine knows what it is testing against. Every map direction carries a **Prior work** line stating what published work predicts for this exact test, with citations, or the words "no prior statement found after" a search described in one line (`operators/scout.md` Step 4; `operators/remap.md` Step 2). The design review checks it as **D12**: is the predicted outcome already in print, and if so what does this bet add (`operators/design-review.md`). Every landed or mixed result gets a **Novelty** line of `known`, `partly new` or `new`, written by a fresh session that searches the literature before the write-up is final, in the results file and the ledger row (`operators/prereg-template.md` §10); the audit checks it as **F27** (`operators/auditor.md`). The remap's re-scout (Step 1b) runs before any follow-up is written and produces the Novelty line where the write-up lacks one. The map and the site show known against new on each landed node. The loop in ARCHITECTURE.md carries all of it. This branch applies it backward: a Novelty line for every landed or mixed bet in all seven programs, from `paper/novelty.md` where it covers the bet and from a fresh search where it does not, and a Prior work line for every open direction on every map.

## 4. What this does not change

No verdict or outcome moves. sg-b3 is still pass, unreplicated, scored 1 against engine odds 0.18. "Known" does not lower a result's standing in the ledger; it changes what the result is evidence of. A known result that replicates on new models is a replication, and the engine should bet on it at replication odds, not at surprise odds. Whether the Brier ledger should score literature-predicted bets separately from engine-sourced ones is proposal Q5's question, and the `source` field already carries what it needs.
