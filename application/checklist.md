# Application checklist: Anthropic Residency, closes 2026-11-22

Current with the ledger as of 2026-11-05 morning (main at `b2c0121`: `ledger/brier.md` 0.217 on 26 scored bets at `dafca10`, `ledger/human-odds.jsonl` 26 lines at `9a75cc2`; the front-page rewrite of README, plain-words and the-engine on branch `front-page`). Sources: the residency page (alignment.anthropic.com/2026/anthropic-residency) and the US Greenhouse posting (job-boards.greenhouse.io/anthropic/jobs/5438311008), both fetched 2026-11-04; Anthropic's candidate AI guidance (anthropic.com/candidate-ai-guidance); `CONTEXT.md` §0, §2, §3 and §9; `TASKS.md`.

Two kinds of item:
- **S: Sean only.** Nobody else can do these. There are six: the five chores plus the form itself.
- **E: engine work.** A session does it, under the rules in `CONTEXT.md` §3. Each carries the `TASKS.md` open item it belongs to, or says that none is open yet. Decisions these items need are made by the session under rule 11 and stated in its commit, where Sean can veto them from the cockpit.

Tick each box when it's done.

---

## S — Sean only

- [ ] **S1. OSF account.** Create a free account at osf.io. That is the whole chore. A session then registers the pre-registration files so their timestamps do not rest on git alone (E10).
- [ ] **S2. Support ticket for the refusals.** File one ticket with Anthropic support covering the three refused requests on file. Each stopped its run, and none was reworded or retried (`CONTEXT.md` §3, rule 3):

  | request id | category | where | record |
  |---|---|---|---|
  | `req_011Cgh7v49vVQNR6AgY3EDui` | `reasoning_extraction` | program 1, claim extractor, Sonnet as base, SimpleQA item `h101` (D20) | `programs/entangled-mind/results/refusal-sonnet-replication.md` |
  | `req_011CghAdzJQ9nFBMocCLUMhf` | `reasoning_extraction` | program 1, claim extractor, Sonnet as base, SimpleQA item `t368` (D25) | `programs/entangled-mind/results/refusal-sonnet-replication-2.md` |
  | `req_011Cgih9NjqNtezArQLWd12p` | `general_harms` | program 2, om-p2-3, SimpleToM job `ms\|gen8_sev3`, after 26 calls | `programs/other-minds/results/refusal-p2-3.md` |

  The question for support: is the claim-extractor design (claims taken only from the model's visible explanation) acceptable, and is the SimpleToM story set usable? Program 1's day-one extractor refusal (`results/refusal-attempt-2.md`) has no request id on file, so it cannot go on the ticket. Once the ticket exists, a session records its number (E11).
- [ ] **S3. The essay, "Why Anthropic?"** It is required, and the form says 200–400 words is typical. `why-anthropic-outline.md` has the beats and the facts, but no sentences, by design. The guidance says to write the first draft yourself and then use Claude to refine it. A session refines it once a draft is in the folder (E12).
- [ ] **S4. The title.** See `CONTEXT.md` §0. It comes from `proposal.md` when that reads right to you. Timing matters: GitHub redirects a renamed repository but not its Pages site, so a rename after submitting would break https://gitphar.github.io/oversight-testbed/ on the form. A session does the rename and fixes every link the day a title is chosen (E13).
- [ ] **S5. Record the walkthrough.** Use `walkthrough-script.md`: about 1,600 spoken words, eleven to twelve minutes, with two paragraphs marked as cuttable to land under ten. It covers one kill (the 3 November chip question: four tries, closed on 5 November under your steer st-19), one steer (st-16, the chip budget and the lever handed over) and program 4's audited passes with the flattery-rule reversal. Record your screen with the files and commits the script names. Host it as an unlisted link (YouTube or Loom). A session puts the link in the READMEs and the site (E2). The script is current to the ledger at `dafca10` (E1 keeps it so).
- [ ] **S6. The form itself.** Submit on the US or the UK posting, not both. Everything on it is yours to enter:
  - **Required fields:**
    - [ ] first name, last name, email
    - [ ] open to working in person 25% of the time? (San Francisco preferred; remote possible, especially for shorter placements)
    - [ ] AI Policy for Application: read the guidance, then select "Yes"
    - [ ] Why Anthropic? (S3)
    - [ ] visa sponsorship now; visa sponsorship in future
    - [ ] open to relocation?
    - [ ] interviewed at Anthropic before?
    - [ ] Agreement to Arbitrate: read the agreement first
    - [ ] References: 2–3 people, one per line, each with name, current role and how you worked together. They are contacted only in later rounds. People who saw your four years as a technical lead in AI pipeline development fit best.
    - [ ] voluntary self-identification (marked required, but voluntary; it does not affect hiring)
  - **Optional fields worth filling:**
    - [ ] Resume/CV or LinkedIn (one of the two; pdf, doc, docx, txt or rtf)
    - [ ] website: https://gitphar.github.io/oversight-testbed/
    - [ ] Links to notable work, each with a short note on your involvement. The links and draft notes are E8.
    - [ ] What research would you most like to work on, and why? `research-interest.md` is a Claude draft (384 words) with a source table. The guidance's first-draft rule applies to it as it does to the essay: your own first draft, checked against the file's numbers and wording.
    - [ ] Mentor areas of interest: Model Psychology and Model Internals, the two areas the research-interest answer names. Mentors whose work our results touch: Jack Lindsey (introspection), Samuel Marks (truth probes), Belinda Li (what models represent).
    - [ ] Residency length: `research-proposal.md` is sized for three months; six weeks covers its H1 and H2 only.
    - [ ] earliest start date; deadlines or timeline considerations
    - [ ] Additional information / cover letter: can link `research-proposal.md`
    - [ ] phone, country, address you will work from, how you heard

---

## E — Engine work

- [ ] **E1. Keep the walkthrough current** (TASKS 8). Brought current 2026-11-05 morning: ng-p3-15's run 2 and audit, ng-p3-16 (fail, audited) and the chip question closed (st-19); program 4's round 2 (ss-b5 pass, ss-b6 reversed to undetermined by audit round 3, ss-b7 pass); the engine at 0.217 on 26; Sean's 26 odds and the bets carrying them. Next: when om-p2-7 is scored (its audit `399df63` let the fail stand; the ledger row is open) or ta-b1r2 is audited, update Part 4's human-column paragraph and the table. Change nothing stronger than the audit allows.
- [ ] **E2. Walkthrough link** (TASKS 8). After S5, add the unlisted link to `README.md`, `programs/entangled-mind/README.md` and the site's front page.
- [x] **E3. ng-p3-15 run 2 and audit** (TASKS 4). Done: run 2 agreed with run 1 (fail; audited, stands). ng-p3-16 followed (fail, 7.0 QPU s, audited `60eae19`, plant pl-013 clean), and the 3 November question was closed with a diagnosis (`programs/nature-graded/map/program-3-map.md`, "After P3-16"; st-19). 69 of 420 QPU s used.
- [x] **E4. Program 4, round 2** (TASKS 2). Done: ss-b4 withdrawn before data (`9b3d222`); ss-b5 pass (Brier 0.070, 93% right; audited, stands); ss-b6 (beat the "which version flatters the paper" rater, 93% against 90%) first a weak pass, then reversed to undetermined by audit round 3 (`60940b1`); ss-b7 pass (the rater was near a coin, so the test was easy). All on one bettor model; $4.76 of the $5.00 cap spent; ss-f1/ss-f2 need a budget ruling. The non-Claude item-writer (ss-f5) is still the cheapest overturning test and is still unrun.
- [x] **E5. Bring `research-proposal.md` current** (TASKS 8). Done 2026-11-05 by the review session: Brier 0.220 on 21 after the merge, programs 2–5, the empty human column, the probe wording.
- [x] **E6. Bring `proposal.md` current.** Done 2026-11-05 by the review session: overclaims replaced with what replicated, numbers to the ledger, replications marked landed, jargon glossed. `proposal.md` is still where the title will come from (S4).
- [x] **E7. `paper/the-engine.md`** (TASKS 7). Done 2026-11-05 morning on branch `front-page`: §6.10 (programs 5 to 7's first wave, ng-p3-16 and the chip question closed, audit round 3, the ledger at 0.217 on 26 with the by-referee split 0.198 on 17 / 0.047 on 4 / 0.417 on 5) and §6.11 (Sean's 26 odds beside the engine's). The abstract and §6.5–6.9 keep their 4 November numbers as a dated record and say so; a full re-draft of the abstract is still open.
- [ ] **E8. Notable-work links and notes** (TASKS 8). Decision under rule 11, vetoable from the cockpit: (1) the site; (2) `programs/entangled-mind/paper/record.md`; (3) `programs/entangled-mind/paper/no-credence-to-read.md`; (4) `ledger/audits/` with `SUMMARY-1.md` and `SUMMARY-2.md`; (5) `ledger/audits/ss-b1.md` and its results file; (6) the walkthrough video (after S5). Draft one line each saying what Sean did and what Claude did, from the steers and commit trailers, in a file in this folder.
- [x] **E9. Check the residency quote.** Done 2026-11-05: the live page reads "the ability to frame a research agenda and judge what is worth doing". `CONTEXT.md` and `proposal.md` now paraphrase it and say so.
- [ ] **E10. OSF registration** (waiting on S1; TASKS "Waiting on Sean"). Once the account exists, register entangled-mind's frozen pre-registrations (`afe1c1b` onwards, as listed in its `DEVIATIONS.md`), this repo's `paper/the-engine.md` §4 (H1–H5, frozen in `7b6bbb8`), and every bet's pre-registration commit in `ledger/bets.jsonl`. Put the OSF link in both READMEs.
- [ ] **E11. Record the ticket** (waiting on S2). Put the ticket number in `CONTEXT.md` §3, rule 3, and against each request id in the refusal files.
- [ ] **E12. Refine the essay** (waiting on S3; TASKS "Waiting on Sean"). Numbers and wording only, against `why-anthropic-outline.md`'s facts and its keep-out list. The voice stays Sean's.
- [ ] **E13. Rename** (waiting on S4). Rename the repository and every link to it, including the Pages URL in `README.md`, the site and this checklist. Do it before submission, or not until after the decision.
- [ ] **E14. `CONTEXT.md` §4 and §8** (TASKS 1, the nightly updater). The nightly updater (23:33) left no commit on 4 November (the Mac crashed at 23:44); CONTEXT.md was rewritten by hand at 05:40 on 5 November. Its §4 still says 0.220 on 21 and 6 plants; the ledger now says 0.217 on 26 (`dafca10`) and nine plants caught (`ledger/plants.jsonl`). Fix the cloud routine, then let it catch up.
- [ ] **E15. Reproduction check before submitting** (TASKS 6). Run `python3 reproduce.py` at the root; it should print ALL LEDGER TABLES AND SITE DATA REPRODUCED. Run `experiments/reproduce.py` in `programs/entangled-mind/`; it should print ALL TABLES REPRODUCED. Confirm the site loads every page.
- [ ] **E16. Papers final** (TASKS deliverable 3). *No Credence to Read*, scoped to what replicated, and *The Entangled Mind*, the short negative result. Both get figures and a safety-framed abstract.
- [ ] **E17. Engine first analysis** (TASKS 7; frozen in `paper/the-engine.md` §4 for 2026-11-21). Run it then and report each H at the n it reached. H1 needs 20 scored bets (26 now, with 8 hits and 18 misses; reached 5 November). H2's catch rate needs 10 plants (8 in `scores.md`, a ninth revealed caught in `plants.jsonl`). H3 needs 20 bets with both sets of odds (3 ledger rows carry Sean's odds now, one withdrawn, plus ng-p3-17's pre-registration; 0 scored; 26 of his odds are recorded, 22 of them before any bet on their direction existed). Most will be untestable, and that is the honest result.

- [ ] **E18. This folder on main** (TASKS 8). The engine session in the main checkout merges each application branch into `main` and pushes (`CONTEXT.md` §2). There is no human step. If a merge is refused, the branch stays unmerged and the session's report says so.

## Done

- [x] **The audit log in this repo.** `ledger/audits/` holds round 1's links (`em-*.md`, `SUMMARY-1.md`), round 2 (`SUMMARY-2.md`) and every audit since; 31 of 33 bets audited (`73a413b` and later).
- [x] **How em-gm5 is scored.** DP2 re-ran the probe's test step on fresh seeds. The audit verified it, with the verdict mixed (`ledger/audits/probe-dissociation-dp2.md`). It stays scored 0; the Brier is unchanged.
- [x] **This update** (TASKS 8): walkthrough script on ng-p3-15, st-16 and program 4's audited passes; research-interest answer naming Model Psychology and Model Internals; Why Anthropic outline refreshed; this checklist.
- [x] **Front page to the ledger and the novelty check** (2026-11-05 morning, branch `front-page`): `README.md` and `paper/plain-words.md` say in their first screen what the engine is, what it found, and which findings are known, partly new or new (per `paper/novelty.md`), each with the models it was shown on; the self-grading result is a footnote to Self-Correction Bench and Self-Attribution Bias; program 7's first wave is three misses in plain words; `paper/the-engine.md` §6.10–6.11; this checklist and the walkthrough script.

## Dates

| date | what |
|---|---|
| now | E14 (the cloud routines); the om-p2-7 audit, then E1 |
| now → 11-15 | S1, S2, S6's references asked; E4–E9 |
| by 11-18 | S3 drafted and S5 recorded; E2, E12 |
| 11-21 | E17 engine first analysis; E15 reproduction check |
| **11-22** | **applications close**; S6 submitted by the morning, not at midnight |

## Files in this folder

| file | what | status |
|---|---|---|
| `research-interest.md` | 384-word answer naming Model Psychology and Model Internals, plus its source table | Claude draft; S6 |
| `research-proposal.md` | one-page proposal (TL;DR, H1–H5 table, plan, outcomes, risks, resources, mentor fit) | numbers current to 2026-11-05 |
| `why-anthropic-outline.md` | beats and facts for Sean's own essay | outline only, by design; S3 |
| `walkthrough-script.md` | ten-minute script: the 3 November chip question closed (four tries), the st-16 steer, program 4's audited passes and the flattery-rule reversal, the engine at 0.217 on 26, the human column | ready to record, current to `dafca10`; E1 keeps it current |
| `checklist.md` | this file | — |
| `../paper/review-anthropic.md` | a panel-style review of the whole submission, with twelve ranked changes and ten interview questions | written 2026-11-05 |
| `../paper/novelty.md` | has this project found anything not already in print? Ten findings checked against the literature: most known, three partly new, none new and replicated | written 2026-11-05 |
