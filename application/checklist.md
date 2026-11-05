# Application checklist: Anthropic Residency, closes 2026-11-22

Current with the ledger as of the end of 2026-11-05 (`main` at `078e0bc`: `ledger/brier.md` <!--n:brier-->0.160<!--/n--> on <!--n:scored-->44<!--/n--> scored bets one per run, <!--n:brier_all-->0.182<!--/n--> on <!--n:scored_all-->50<!--/n--> every row; Sean's odds scored on <!--n:human_n-->12<!--/n--> bets at <!--n:human_brier-->0.386<!--/n-->; <!--n:human_lines-->35<!--/n--> odds lines; the numbers in these markers are filled by `python3 site/numbers.py` and stay current; `paper/day-four.md` is the day's account). Sources: the residency page (alignment.anthropic.com/2026/anthropic-residency) and the US Greenhouse posting (job-boards.greenhouse.io/anthropic/jobs/5438311008), both fetched 2026-11-04; Anthropic's candidate AI guidance (anthropic.com/candidate-ai-guidance); `CONTEXT.md` §0, §2, §3 and §9; `TASKS.md`.

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
- [ ] **S5. Record the walkthrough.** Use `walkthrough-script.md`: about 1,700 spoken words, eleven to twelve minutes, with two paragraphs marked as cuttable to land under ten. It covers one kill (the 3 November chip question: four tries, closed on 5 November under your steer st-19), one steer (st-16, the chip budget and the lever handed over, now labelled helped), program 4's audited passes with the flattery-rule reversal and the one-bet-per-run rule you set, and the human column as it stands (behind the engine). Record your screen with the files and commits the script names. Host it as an unlisted link (YouTube or Loom). A session puts the link in the READMEs and the site (E2). The script's ledger totals are filled by `site/numbers.py`; read it rendered (E1 keeps the rest current).
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
    - [ ] What research would you most like to work on, and why? `research-interest.md` is a Claude draft (about 460 words, every term explained in its sentence, ledger numbers filled by `site/numbers.py`) with a source table and the panel review's Part 5 as its wording guide. The guidance's first-draft rule applies to it as it does to the essay: your own first draft, checked against the file's numbers and wording; trim to 400.
    - [ ] Mentor areas of interest: Model Psychology and Model Internals, the two areas the research-interest answer names. Mentors whose work our results touch: Jack Lindsey (introspection), Samuel Marks (truth probes), Belinda Li (what models represent).
    - [ ] Residency length: `research-proposal.md` is sized for three months; six weeks covers its H1 and H2 only.
    - [ ] earliest start date; deadlines or timeline considerations
    - [ ] Additional information / cover letter: can link `research-proposal.md`
    - [ ] phone, country, address you will work from, how you heard

---

## E — Engine work

- [ ] **E1. Keep the walkthrough current** (TASKS 11). Brought current at the end of 2026-11-05 (`078e0bc`): the ledger totals in Parts 3 and 4 and the table are `site/numbers.py` placeholders; Part 2 carries st-16's label (helped) and the steer count (helped 18 of 28); Part 3 carries rule 15 in Sean's words; Part 4 carries the human column (placeholders; sg-b4 the hit on which his 0.65 beat the engine's 0.18). Next: when P3-9 (his 0.90 against the engine's 0.80 under rule 14) or P3-17 (his 0.30 against 0.55) scores, or the `p1-wave3` and `p2-wave3` branches are folded (om-p2-15 fail at his 0.70), the human-column row of the table changes; the placeholders in the prose change on their own. Change nothing stronger than the audit allows.
- [ ] **E2. Walkthrough link** (TASKS 8). After S5, add the unlisted link to `README.md`, `programs/entangled-mind/README.md` and the site's front page.
- [x] **E3. ng-p3-15 run 2 and audit** (TASKS 4). Done: run 2 agreed with run 1 (fail; audited, stands). ng-p3-16 followed (fail, 7.0 QPU s, audited `60eae19`, plant pl-013 clean), and the 3 November question was closed with a diagnosis (`programs/nature-graded/map/program-3-map.md`, "After P3-16"; st-19). 69 of 420 QPU s used.
- [x] **E4. Program 4, round 2** (TASKS 2). Done: ss-b4 withdrawn before data (`9b3d222`); ss-b5 pass (Brier 0.070, 93% right; audited, stands); ss-b6 (beat the "which version flatters the paper" rater, 93% against 90%) first a weak pass, then reversed to undetermined by audit round 3 (`60940b1`); ss-b7 pass (the rater was near a coin, so the test was easy). All on one bettor model; $4.76 of the $5.00 cap spent; ss-f1/ss-f2 need a budget ruling. The non-Claude item-writer (ss-f5) is still the cheapest overturning test and is still unrun.
- [x] **E5. Bring `research-proposal.md` current** (TASKS 8). Done 2026-11-05 by the review session: Brier 0.220 on 21 after the merge, programs 2–5, the empty human column, the probe wording.
- [x] **E6. Bring `proposal.md` current.** Done 2026-11-05 by the review session: overclaims replaced with what replicated, numbers to the ledger, replications marked landed, jargon glossed. `proposal.md` is still where the title will come from (S4).
- [x] **E7. `paper/the-engine.md`** (TASKS 10). Done 2026-11-05 morning on branch `front-page` (§6.10, §6.11) and again at the end of the day on branch `papers-day4` (the day-four revision, `c42128e`): the novelty check's papers in related work (§2.8), rules 13 to 15 and the steer-valuation method as instruments (§3.11 to §3.15), H1 to H5 against the day's counts (§4.8: H1 and H2 at their minimum n, H3 to H5 untestable), the ledger and the human column (§6.12), four limitations, and a status paragraph in the abstract. Every ledger number in the new sections is a `site/numbers.py` placeholder, and the file is on that script's document list, so `reproduce.py` and CI fail on a stale one. The abstract's bullets and §6.5 to §6.11 keep their dated numbers and say so.
- [ ] **E8. Notable-work links and notes** (TASKS 8). Decision under rule 11, vetoable from the cockpit: (1) the site; (2) `programs/entangled-mind/paper/record.md`; (3) `programs/entangled-mind/paper/no-credence-to-read.md`; (4) `ledger/audits/` with `SUMMARY-1.md` and `SUMMARY-2.md`; (5) `ledger/audits/ss-b1.md` and its results file; (6) the walkthrough video (after S5). Draft one line each saying what Sean did and what Claude did, from the steers and commit trailers, in a file in this folder.
- [x] **E9. Check the residency quote.** Done 2026-11-05: the live page reads "the ability to frame a research agenda and judge what is worth doing". `CONTEXT.md` and `proposal.md` now paraphrase it and say so.
- [ ] **E10. OSF registration** (waiting on S1; TASKS "Waiting on Sean"). Once the account exists, register entangled-mind's frozen pre-registrations (`afe1c1b` onwards, as listed in its `DEVIATIONS.md`), this repo's `paper/the-engine.md` §4 (H1–H5, frozen in `7b6bbb8`), and every bet's pre-registration commit in `ledger/bets.jsonl`. Put the OSF link in both READMEs.
- [ ] **E11. Record the ticket** (waiting on S2). Put the ticket number in `CONTEXT.md` §3, rule 3, and against each request id in the refusal files.
- [ ] **E12. Refine the essay** (waiting on S3; TASKS "Waiting on Sean"). Numbers and wording only, against `why-anthropic-outline.md`'s facts and its keep-out list. The voice stays Sean's.
- [ ] **E13. Rename** (waiting on S4). Rename the repository and every link to it, including the Pages URL in `README.md`, the site and this checklist. Do it before submission, or not until after the decision.
- [ ] **E14. `CONTEXT.md` §4 and §8** (TASKS 1, the nightly updater). The nightly updater (23:33) left no commit on 4 November (the Mac crashed at 23:44); CONTEXT.md was rewritten by hand at 05:40 on 5 November. Its §4 still says 0.220 on 21 and 6 plants, and §8 lists steers to st-18; the ledger now says <!--n:brier-->0.160<!--/n--> on <!--n:scored-->44<!--/n--> and <!--n:plants_caught-->21<!--/n--> plants caught, and `ledger/steers.jsonl` runs to st-28. `paper/day-four.md` has the day. Fix the cloud routine, then let it catch up.
- [ ] **E15. Reproduction check before submitting** (TASKS 6). Run `python3 reproduce.py` at the root; it should print ALL LEDGER TABLES AND SITE DATA REPRODUCED. Run `experiments/reproduce.py` in `programs/entangled-mind/`; it should print ALL TABLES REPRODUCED. Confirm the site loads every page.
- [ ] **E16. Papers final** (TASKS deliverable 3). *No Credence to Read*, scoped to what replicated, and *The Entangled Mind*, the short negative result. Both get figures and a safety-framed abstract.
- [ ] **E17. Engine first analysis** (TASKS 10; frozen in `paper/the-engine.md` §4 for 2026-11-21). Run it then and report each H at the n it reached, on both analysis sets (one bet per run as primary, every row as the sensitivity; `the-engine.md` §3.13 says why both). H1 needs 20 scored bets: <!--n:scored-->44<!--/n--> now with <!--n:hits-->11<!--/n--> hits, reached. H2 needs 10 planted faults: <!--n:plants_planted-->21<!--/n-->, all caught, reached. H3 needs 20 bets with both sets of odds: <!--n:human_n-->12<!--/n--> now. H4 has no within-seed control scout; H5 is two engine-sourced bets short (`the-engine.md` §4.8). H3 to H5 will be untestable, and that is the honest result.

- [ ] **E18. This folder on main** (TASKS 11). The engine session in the main checkout merges each application branch into `main` and pushes (`CONTEXT.md` §2). There is no human step. If a merge is refused, the branch stays unmerged and the session's report says so.
- [ ] **E19. `paper/what-the-human-adds.md` to seven bets.** The page was written when four scored bets carried Sean's odds (engine 0.057, Sean 0.513 on four); the ledger now has seven (`paper/day-four.md` §7: engine 0.140, Sean <!--n:human_brier-->0.386<!--/n-->, combined 0.213). A writing session updates its "four-bet odds column" section and keeps the rest; the steer count (helped 18 of 28) is unchanged until the next monthly scoring.

## Done

- [x] **Day four, application folder to the ledger at `078e0bc`** (2026-11-05, branch `papers-day4`): `research-interest.md` rewritten at bachelor's reading level with every term explained in its sentence and the panel review's Part 5 as its guide; the walkthrough's Parts 2 to 4 and table brought to the day's ledger (st-16 helped, rule 15, the seven-bet human column); this checklist; the three files added to `site/numbers.py`'s document list so their ledger totals cannot drift. `why-anthropic-outline.md` untouched, by design (S3 is Sean's).
- [x] **The audit log in this repo.** `ledger/audits/` holds round 1's links (`em-*.md`, `SUMMARY-1.md`), round 2 (`SUMMARY-2.md`) and every audit since; 31 of 33 bets audited (`73a413b` and later).
- [x] **How em-gm5 is scored.** DP2 re-ran the probe's test step on fresh seeds. The audit verified it, with the verdict mixed (`ledger/audits/probe-dissociation-dp2.md`). It stays scored 0; the Brier is unchanged.
- [x] **This update** (TASKS 8): walkthrough script on ng-p3-15, st-16 and program 4's audited passes; research-interest answer naming Model Psychology and Model Internals; Why Anthropic outline refreshed; this checklist.
- [x] **Front page to the ledger and the novelty check** (2026-11-05 morning, branch `front-page`): `README.md` and `paper/plain-words.md` say in their first screen what the engine is, what it found, and which findings are known, partly new or new (per `paper/novelty.md`), each with the models it was shown on; the self-grading result is a footnote to Self-Correction Bench and Self-Attribution Bias; program 7's first wave is three misses in plain words; `paper/the-engine.md` §6.10–6.11; this checklist and the walkthrough script.

## Dates

| date | what |
|---|---|
| now | E14 (the cloud routines); E19; E1 when P3-9, P3-17 or the wave branches land |
| now → 11-15 | S1, S2, S6's references asked; E4–E9 |
| by 11-18 | S3 drafted and S5 recorded; E2, E12 |
| 11-21 | E17 engine first analysis; E15 reproduction check |
| **11-22** | **applications close**; S6 submitted by the morning, not at midnight |

## Files in this folder

| file | what | status |
|---|---|---|
| `research-interest.md` | answer of about 460 words naming Model Psychology and Model Internals, every term explained, ledger numbers as placeholders, plus its source table and the panel review's Part 5 as the wording guide | Claude draft, current to `078e0bc`; S6 |
| `research-proposal.md` | one-page proposal (TL;DR, H1–H5 table, plan, outcomes, risks, resources, mentor fit) | numbers current to the morning of 2026-11-05 (0.220 on 21); not brought to the day's end, and not on `site/numbers.py`'s list |
| `why-anthropic-outline.md` | beats and facts for Sean's own essay | outline only, by design; S3 |
| `walkthrough-script.md` | ten-minute script: the 3 November chip question closed (four tries), the st-16 steer (helped) and the steer count, program 4's audited passes, the flattery-rule reversal and rule 15, the engine's score as placeholders, the human column with seven scored bets | ready to record, current to `078e0bc`; E1 keeps it current |
| `checklist.md` | this file | — |
| `../paper/review-anthropic.md` | a panel-style review of the whole submission, with twelve ranked changes and ten interview questions | written 2026-11-05 |
| `../paper/novelty.md` | has this project found anything not already in print? Twelve findings checked against the literature: most known, three partly new, one new and unreplicated (ss-b10c), none new and replicated; three replications re-ranked | written 2026-11-05, brought to the day's end on `papers-day4` |
| `../paper/day-four.md` | the plain account of 5 November: the three rules, the ledger inbox, the steers scored, the seven bets with Sean's odds, the chip's pass, every bet that settled or stopped | written 2026-11-05 evening |
