# Day four: three rules, a ledger that stopped racing, and the first scored bets with Sean's odds

Sean Pharris · 5 November, about 05:30 to 11:24 (America/Denver) · written from the commits in that window and the committed ledger on `main` at `078e0bc` (`ledger/bets.jsonl`, `ledger/brier.md`, `ledger/scores.md`, `ledger/prior.md`, `ledger/steers.md`), the planning chat's handoff (`operators/handoff-2026-11-05.md`, committed as written at `ea06c00`) and the pages named below. It starts where `paper/day-three.md` ends. If this page and a ledger file disagree, the ledger file is right and this page is wrong. Two wave branches (`p1-wave3`, `p2-wave3`) were still unmerged when this was written; their results are named in §9 as not yet in the ledger.

## In plain English

**What happened.** After the crash, Sean and a planning chat spent the night deciding how the machine should run, and the morning turned those decisions into rules. Three landed in `CONTEXT.md` §3: rule 13 (the engine must know what the published literature predicts before it bets, and must say whether a result is already known before calling it a finding), rule 14 (every odds number starts from the engine's own hit rate, with the adjustment and its reason written down), and rule 15 (one scored bet per run, so a lucky run cannot count three times). The four ledger files stopped being edited by nine sessions at once: changes now go through a per-session inbox and one fold. The front-page numbers stopped being typed by hand. Every one of Sean's 28 steers was read by a fresh session and labelled: helped 18, neutral 10, hurt 0. And the human column of the calibration table, empty at the end of day three, now holds seven scored bets, one of them a hit on which his number was far above the engine's.

**What came back.** In this window, counting only what is on `main`:
- six passes: em-dm6f2 and em-gm2bf1 in program 1, ng-p3-18 on the chip, ss-b11 and ss-b10c in program 4, sg-b4 in program 5. Three of those six are secondary or fragile (§9);
- eight misses, counting mixed as a miss: om-p2-7, ta-b1r2, em-gm2q, ss-b10, ss-b12, em-bm9f2, em-dm6f2f1, sg-b5, ss-b13 (nine with ss-b13, which came back mixed);
- six bets stopped before any data because a design review or a record check said the test could not decide its question: em-gm3cf1, sv-b4, ss-b14, ss-b10b, ss-b15, and the direction SV-12, parked before it was even pre-registered.

**The headline.** The engine's score moved from 0.220 on 21 scored bets at the end of day three to **0.164 on 35** (9 hits) at `078e0bc`, with 0.190 on 41 when every scored row is counted (`ledger/brier.md`). A coin scores 0.250 and always saying the observed hit rate scores 0.191. Most of the move is rule 15 and the morning's low-odds misses, not better judgment (§4). Thirty-five bets still cannot separate those numbers.

**Sean's odds.** Seven scored bets carry his number, one per run; his Brier on them is 0.414, against about 0.14 for the engine on the same seven (§7). The one bet on which his number was far above the engine's and the bet hit is sg-b4 (does a planted exaggeration get off lightly because it sits in the model's own reply, or because of how the request is laid out?): his 0.65 against the engine's 0.18. On the other six his numbers were higher than the outcomes justified.

## 1. The crash rule

Day three told the crash: at 23:44 on 4 November the Mac kernel-panicked with two local models and nine sessions running, and five hours of the night were lost. The planning chat's rule for it is one sentence in the handoff (`operators/handoff-2026-11-05.md` §1): **a local-model job runs alone, never beside a wave.** It changed today's shape. The nine tabs of the wave (§4 of the handoff) loaded no local model. The two jobs that need one, the non-Claude auditor over five scored results and the bmq-d1 fine-tune (can the truth still be read inside an open model after a fine-tune makes it forget?), are queued for after the wave, one at a time (handoff §5). Neither had started when this was written. The rule exists only in the handoff; it is not yet a numbered rule in `CONTEXT.md` §3, and the wave's launch rules repeat it as "never load a local model in these tabs" (handoff §3).

## 2. Rule 13: the engine knows what it is testing against

The night's largest finding was not a result but a gap. `paper/novelty.md` (merged 06:01, `fea9366`) checked ten of the project's findings against the literature: six already in print, three partly new, one new in form but too small to count, none new and replicated. Program 5's one pass, sg-b3 (is a planted exaggeration docked less in the conversation that wrote the conclusion?), had been staked at 18% with a 2026 paper predicting its pass sitting in the scout's own reads, and the README then called it "the self-grading failure this testbed was built to catch". `paper/informed-engine.md` (`e56326d`, 06:30) traces that step by step: the paper was read three times, its prediction never became a sentence any later step had to answer to, and a second paper (Tsui 2025) was never found because the search ran around the seed question's words rather than the test's mechanism.

The fix is rule 13 (`CONTEXT.md` §3; the `informed-engine` branch, stuck overnight behind another session's uncommitted edits, merged at 09:52, `bd3bbb5`). Every map direction carries a **Prior work** line saying what published work predicts for that exact test; the design review checks it as D12; every landed or mixed result gets a **Novelty** line of known, partly new or new, written by a fresh session that did not run the bet, and the audit checks it as F27. The backward pass wrote 116 prior-work lines across the seven maps (`35fcd59`) and 23 novelty lines on every landed or mixed bet (`e0235e6`): 4 known, 18 partly new, 1 new (`CONTEXT.md` §4). Sean's decision is steer st-27, logged in his words from the planning chat (`f082f04`).

The rule ran forward the same morning:
- sg-b4's Novelty line (partly new) was written by a fresh session before the bet was scored (`91becd4`, 10:37), and the design review's D12 found its prior-work line wrong and had it corrected before any call (`d277c6f`, `fdb2588`);
- the program 7 remap re-scouted around its wave-1 results before writing follow-ups (`428bcc3`), and the program 5 remap did the same around sg-b4 (`4cc4cdb`, six reads);
- ss-b13 was labelled partly new (`323a8de`) and ss-b10c new (`9446785`), each by a session that did not run the bet;
- the novelty page itself took a dated correction (`d870107`, 11:08): the April 2026 paper it had read as asking for a flattery test on BrainBench had asked for clinical-trial-registry tests instead.

Nothing in the rule changes a verdict. "Known" changes what a result is evidence of, not its standing in the ledger.

## 3. Rule 14: odds start from the record, and the first two scored bets under it

Rule 14 (`414f903`, 06:51) says every odds number starts from `ledger/prior.md`, the engine's own hit rate with a Wilson interval, split by program, referee, cost tier, source and map depth (`ledger/prior.py`, `6514a11`). The elicitation is a fresh context handed that page and the bet's own description and nothing about the bet's history: no earlier odds, no earlier bet on its direction, no human odds. It writes a prior, a signed adjustment and a one-line reason, and the ledger stores all three. `ledger/brier.md` then scores the prior alone against the adjusted odds on the same bets, so whether the engine's reasoning adds anything to its own record is a published number. Sean's words for it: "it needs to be a continuous self-feedback loop of improvement" (`CONTEXT.md` §3 rule 14).

The prior itself moved with the ledger: 0.30 (8 of 27) when the page was first generated at 06:48; 0.32 (12 of 37) when the morning's second-wave bets were elicited; 0.23 (7 of 31) just after rule 15 took the secondary bets out (§4), which is what sv-b4's row carries; 0.26 (9 of 35) at `078e0bc`.

The first two bets scored under the rule were program 5's second wave:

| bet | question, in short | prior | adjustment | engine odds | Sean | outcome |
|---|---|---|---|---|---|---|
| sg-b4 | is the exaggeration let off because it sits in the model's own reply, or because of the request's layout? | 0.32 | −0.14 | 0.18 | 0.65 | **pass** |
| sg-b5 | does the own-conversation leniency hold when the exaggeration does not make the text longer? | 0.32 | −0.10 | 0.22 | 0.55 | **fail** |

On those two, at `e68eff1` (11:14), the prior alone scored 0.282 and the adjusted odds 0.360: **the adjustment did not help**, by 0.078 (`ledger/brier.md` at that commit, "The adjustment's value"). The engine had reasoned its way down from 0.32 on the bet that hit.

Ten minutes later two more bets under the rule were folded in, from program 4: ss-b13 (prior 0.32, adjustment −0.14, miss) and ss-b10c (prior 0.32, adjustment +0.38, hit). On four bets the prior alone scores 0.282 and the adjusted odds 0.211, so the sentence in `ledger/brier.md` at `078e0bc` now reads that the adjustment **helped**, by 0.072. Two bets flipped the sign. That is the size of the sample, not a verdict either way, and the page says so in the same line.

## 4. Rule 15: one scored bet per run, and what it did to the headline

Audit round 3 had found that six of the engine's eight hits were two bettor runs scored as six bets (`ledger/audits/SUMMARY-3.md`, hole 1). Sean's decision, in his words: "I agree, I understand now that one lucky run was being counted three times" (steer st-21, logged 09:54). Rule 15 landed at 09:58 (`69fb813`): a scored bet whose row names the same run as an earlier scored bet is secondary, keeps its odds and outcome, and leaves the primary Brier, the calibration table, the by-referee and human scores, the prior and the lesson test. Six rows carry `secondary_of`: ss-b2, ss-b3 and ss-b11 (ss-b1's run), ss-b7 (ss-b5's run), em-gm2bf1 (em-gm3b's archive) and em-dm6f2f1 (em-dm6f2's archive); ss-b6, already unscored, is marked too. `ledger/brier.md` publishes both numbers, and the calibration page says both in one sentence.

What it did to the headline, commit by commit (`ledger/brier.md` at each):

| time | commit | scored | engine Brier | all rows (sensitivity) | what changed |
|---|---|---|---|---|---|
| 05:35 | `555e89e` | 21 | 0.220 | — | end of day three |
| 06:26 | `dafca10` | 26 | 0.217 | — | wave 1 of programs 6 and 7 scored |
| 07:42 | `361284b` | 35 | 0.189 | — | the morning's archive bets and om-p2-7, ta-b1r2 |
| 09:07 | `73eb5cf` | 37 | 0.188 | — | ng-p3-18 scored (pass) |
| 09:58 | `69fb813` | 31 | **0.158** | 0.188 on 37 | rule 15: six secondary rows out |
| 11:14 | `e68eff1` | 33 | 0.170 | 0.197 on 39 | sg-b4 (pass), sg-b5 (fail) folded |
| 11:24 | `078e0bc` | 35 | **0.164** | 0.190 on 41 | ss-b13 (mixed), ss-b10c (pass) folded |

Two things to read plainly. First, rule 15 made the engine's number look better, not worse: the secondary rows it removed were mostly hits the engine had rated low (ss-b2 at 0.30, ss-b3 at 0.35, ss-b7 at 0.40, em-gm2bf1 at 0.25), and a low-odds hit is the most expensive thing a forecaster can do. Second, the drop from 0.220 to 0.189 between 05:35 and 07:42 came from a run of misses at low odds (ta-b1r2 at 0.06, em-bm9f2 at 0.08, em-gm2q at 0.10, om-p2-7 at 0.15), which cost almost nothing, beside hits at 0.55 and 0.85 (em-dm6f2, ss-b11) and one at 0.25 (em-gm2bf1, later marked secondary). The hit rate the engine starts from is now 0.26, and the hits sit at 18% to 70% (`ledger/brier.md`, "Where the odds sat").

## 5. The ledger inbox, and numbers that are generated

The shared checkout kept corrupting the record until mid-morning. `ledger/lessons.jsonl` was committed empty at 06:36 (`35b9459`) and restored a minute later (`b79f9d4`); the em-dm6f2f1 row was dropped in a race at 07:32 and re-added (`0a1f054`, `8f18190`); several commits swept in other sessions' half-finished rows; and the panel review had found the front page saying 26 scored bets and 0.217 while the ledger said 37 and 0.188.

Two mechanisms ended that, both from Tab A of the wave:
- **The ledger inbox** (`1b89efe`, 10:03; `ledger/inbox/README.md`). No session edits `bets.jsonl`, `lessons.jsonl`, `steers.jsonl` or `plants.jsonl` any more. Each appends one line per change to its own file in `ledger/inbox/` and commits that file alone; `python3 ledger/merge_inbox.py --commit`, run only in the main checkout, folds every committed line in commit order, checks line counts, regenerates the three tables and clears what it folded. Every wave branch adopted it on its next merge of `main` (`bf9a7dd`, `23aecd7`, `c30cc25`). Two folds ran before this page: `e68eff1` (15 lines) and `078e0bc` (16 lines). The first crashed half way, in `brier.py`, on sv-b4's withdrawn row, which carries no `scored` field; it was fixed forward with a one-line tolerance in the scorer and committed (the commit message says so).
- **Generated front-page numbers** (`ae566f3`, 10:09; `site/numbers.py`). `README.md`, `paper/plain-words.md`, `paper/one-page.md` and `application/one-page-plain.md` no longer type a ledger number. Each is a marked placeholder filled from the machine-readable line at the end of `brier.md`, `scores.md` and `prior.md`; `reproduce.py` and the GitHub check fail on a stale one. Day three's table of six circulating Brier numbers cannot recur in those four files.

## 6. The steers scored: helped 18 of 28

The panel review's first finding was that the human's judgment was invisible: twenty steers logged, nearly all "pending". Tab B wrote the method (`operators/steers.md`, `8b157c8`) and a fresh Fable session that had written none of the steers valued every one of them (`ec26bf8`; merged `fc2748d`, 10:10). Each valuation names what the steer changed in the record with its file, one sentence on what the engine's default would have done with the file that shows the default, a measurable effect where one exists, and a label. The count is **helped 18 of 28, neutral 10, hurt 0** (`ledger/steers.md`): 17 decided by a number in the ledger, 6 by a chain of files, 5 given early on steers whose effect is mostly still to come.

The eight new steers are Sean's decisions from the planning chat, logged in his words (`f082f04`): rule 15 (st-21, helped), parking ta-d8 and ta-d10, the two test-awareness cards he had given 95 and 90 percent, because the novelty check says they duplicate Anthropic's own release testing (st-22, st-23, helped, early; each gets a shadow check later), P3-9 as the chip's one foundations experiment (st-24, neutral, early), and the four architecture calls of the last day that had changed the machine without being logged: three models on every bet (st-25), a landed bet must open the next paths (st-26), the engine must know prior work before it bets (st-27), and cockpit cards must carry context from our own results (st-28). All four of his later seed questions are labelled neutral: program 2's bought no hit for six dollars, program 3's chip column was mostly bought by bets that could not pass, program 5's was already answered in print, program 7's one wave has no hit yet. Program 1's founding push (st-01, st-03) is labelled helped.

What the count is: a reading of files by a Claude session, against the default the record shows, published with the method so anyone can file a different label. What it is not: a measurement of Sean's skill. That measurement is the odds column (§7), and `paper/what-the-human-adds.md` (`e89f407`) tells both sides in plain words. That page was written when four scored bets carried his odds; the ledger now has seven, and the page has not been updated.

## 7. Sean's odds: seven scored bets, the first hit above the engine, and the misses

At the end of day three no scored bet carried Sean's odds. By `078e0bc`, eight do, seven of them primary under rule 15. In the order they were scored:

| bet | program | question, in short | Sean | engine | outcome | scored |
|---|---|---|---|---|---|---|
| om-p2-7 | 2 | do the model's format quirks reappear when it answers for "Sam", on three models? | 0.70 | 0.15 | **fail** | 06:35 |
| ta-b1r2 | 6 | told "evaluation" vs "real" vs a placebo note, does it stand up to a wrong user differently? | 0.60 | 0.06 | **null** | 06:34 |
| ss-b11 | 4 | is the round-1 bettor's edge more than knowing which fields report good news? | 0.65 | 0.85 | **pass** (secondary of ss-b1; sensitivity only) | 07:16 |
| ss-b12 | 4 | is the bettor's advantage on older papers memory? | 1.00 | 0.20 | **null** | 07:27 |
| ng-p3-18 | 3 | measured again on a new day, do both error terms show up on the entangled pairs? | 0.55 | 0.60 | **pass** | 09:07 |
| sg-b4 | 5 | is the exaggeration let off because it sits in the model's own reply, or because of the layout? | 0.65 | 0.18 | **pass** | 10:49 |
| sg-b5 | 5 | does the own-conversation leniency hold when the exaggeration does not lengthen the text? | 0.55 | 0.22 | **fail** | 10:46 |
| ss-b13 | 4 | can Haiku and Sonnet also tell which way the 116 published findings went? | 0.65 | 0.18 | **mixed** | 11:06 |

His Brier on the seven primary bets is **0.414** (0.378 on eight with ss-b11; `ledger/brier.md`). The engine's on the same seven rows, computed for this page from the odds and outcomes in `ledger/bets.jsonl`, is 0.140 (terms 0.0225, 0.0036, 0.040, 0.160, 0.672, 0.048, 0.032), and the unweighted mean of the two forecasts, H3's combined forecast, scores 0.213. The ordering matters for one claim: the instruction for this page called sg-b4 the first hit carrying Sean's odds. The ledger's order is ss-b11 at 07:16 (a secondary row, outside the primary score), ng-p3-18 at 09:07, then sg-b4 at 10:49. What sg-b4 is, exactly, is the first hit on which his number was far above the engine's: 0.65 against 0.18, so on that one bet his term is 0.12 and the engine's 0.67. On ng-p3-18 he was below the engine (0.55 against 0.60) and on ss-b11 below it too.

Read plainly: on six of the seven his numbers were higher than the outcomes justified, and his 1.00 on ss-b12 alone is 1.0 of his 2.9 total. The engine's numbers on those bets were written after reading its own record and a lesson from its misses; his were single numbers given blind, and the cockpit never showed him the base rate (0.26). H3 needs 20 bets with both sets of odds and the proposal's steer rule needs 8; the odds steer st-18 stays neutral until then.

Three more of his lines attached to bets that were withdrawn before data, so they score nothing: ta-b1r (0.60), sv-b4 (0.55), and ss-b14 and its re-bet ss-b15 (0.35). Two more sit on the unmerged `p2-wave3` branch: om-p2-15 (do the model's predictions of its own quirks beat a "no effect" guess?) came back fail at his 0.70 against the engine's 0.10, and om-p2-14 (his 0.75) was parked by a budget ruling. P3-9, the direction where he and the engine disagreed most (0.90 against the map's 0.40), was running on its own branch with the engine's odds re-elicited under rule 14 to 0.80 (`8bf9942`); nothing can be said until it scores.

## 8. The chip: P3-18

The one chip bet of the day asked whether both error terms P3-5c had found on 3 November, a rotation-type term and a blur-type term beyond the simulator's state, come back on the same three entangled pairs in a fresh job on a new day. The engine gave it 0.60, Sean 0.55, the first chip bet with his number on it. Budget ruling br-006 approved 24 QPU seconds under st-16 (`01e8ebe`); the circuits and the simulator's reference states were committed before submission (`6fe09e1`); the job ran at 07:52 and billed **20.0 QPU seconds**, raw counts committed the moment it returned (`465262a`). Result (`programs/nature-graded/results/p3-18-fresh-job.md`): both terms on two of the three pairs (h088, h268), blur only on h221, so **pass, unreplicated** by the frozen rule. The audit let it stand with three cuts (`4f07a2f`); plant pl-032 was clean; scored at 09:07 (`73eb5cf`).

What the file says it does and does not show: the reading held on a second job, not only on 3 November's afternoon; two jobs on one chip are still not a description of the chip; the pass rests on two pairs and either label flipping makes it a fail; on h088 the full model still misfits. It is the engine's first chip-graded hit (the chip column is 0.070 on 5 bets, `ledger/brier.md`). The chip total is **89 of the 420 s hard stop**. P3-17 (could the chip misreading its own results stand in for the blur term?), which carries his 0.30 against the engine's 0.55, was still open: its runner crashed once after the first pair's fits, was fixed and re-run from the same seed (`ee30b52`, D46), and had no result on `main` when this was written.

## 9. Every bet that settled, stopped or was parked in this window

On `main` at `078e0bc` (odds are the engine's in force at the first call; "secondary" means rule 15 keeps it out of the primary score):

| bet | program | question, in short | engine odds | outcome | audit |
|---|---|---|---|---|---|
| om-p2-7 | 2 | format quirks reappear for "Sam"? | 0.15 · Sean 0.70 | **fail** on all three models | stands, 4 cuts; plant caught |
| ta-b1r2 | 6 | told "evaluation" vs "real" vs placebo? | 0.06 · Sean 0.60 | **null**; Opus untestable at the belief gate | stands, 3 cuts; plant caught |
| em-dm6f2 | 1 | would a fixed 70% confidence line flag different answers by format? (Sonnet, archive) | 0.55 | **pass**, unreplicated | stands, 3 cuts |
| em-gm3cf1 | 1 | held-out format recovery on Haiku, converged (archive) | 0.30 | **withdrawn**: pass chance about 1% on the audit's measured numbers | — |
| ss-b11 | 4 | round-1 bettor vs a field-aware good-news rule (archive) | 0.85 · Sean 0.65 | **pass**, secondary of ss-b1 | stands, 4 cuts |
| em-gm2bf1 | 1 | do claims that move with question order also move with answer format? (archive) | 0.25 | **pass**, secondary of em-gm3b, fragile; new pattern P17 | stands, 5 cuts |
| ss-b12 | 4 | is the bettor's advantage on older papers memory? | 0.20 · Sean 1.00 | **null**: pre-cutoff 0.063 vs post 0.071, no difference shown | stands, 4 cuts |
| em-gm2q | 1 | does question order still move the rating with nothing in the transcript but questions? | 0.10 | **mixed**: Sonnet passed the full rule, Haiku failed a wrong-target check; the effect falls on different items | stands, 5 cuts; plant caught |
| ss-b10 | 4 | does the flattery rule beat the neuroscientists on BrainBench? (Haiku, Sonnet) | 0.30 | **mixed**: Sonnet 81.8%, level with the published LLM figure; Haiku below the bar in one order | stands, 9 cuts |
| em-bm9f2 | 1 | does the pull toward the last rating have the human serial-dependence shape? (archive) | 0.08 | **fail**: no better than a line | stands; the one cut was the plant, caught |
| em-dm6f2f1 | 1 | are Sonnet's extra probability-format flags mostly "no" guesses? (archive) | 0.45 | **fail**, secondary of em-dm6f2 | stands, 1 cut |
| ng-p3-18 | 3 | both error terms again on a fresh chip job? | 0.60 · Sean 0.55 | **pass**, unreplicated; 20.0 QPU s | stands, 3 cuts |
| sv-b4 | 7 | does what the model does add to its stated confidence in predicting its mistakes? (SV-8, archive) | 0.03 (0.10 at entry) · Sean 0.55 | **withdrawn** before the archive was opened: matched to the published decline rates, no plausible world gives a 10% pass chance (D17) | — |
| SV-12 | 7 | does Haiku's "no single belief across formats" go away under a looser published scoring? | 0.25 · Sean 0.60 | **parked** before pre-registration: program 1's published agreement already implies a concordance near 0.77, below the drafted 0.85 bar (D18) | — |
| sg-b4 | 5 | own reply, or layout? | 0.18 · Sean 0.65 | **pass**, unreplicated, partly new: Haiku T +6.8 [+4.3, +9.5] against a 6.3 bar, Opus +4.0 [+2.7, +5.4] against 3.0; Haiku fragile to one domain | stands, 3 cuts |
| sg-b5 | 5 | leniency without the extra length? | 0.22 · Sean 0.55 | **fail**: Opus +3.4 [+2.5, +4.4], below the 5-point bar; Haiku unchanged at 12.5 | stands, 4 cuts; plant caught |
| ss-b13 | 4 | Haiku and Sonnet as bettors on the 116 findings? | 0.18 · Sean 0.65 | **mixed**, partly new: Sonnet matches Opus (Brier 0.168, beats the good-news rule); Haiku beats a coin but not the rule | stands, 5 cuts; plant caught |
| ss-b14 | 4 | 60 more model-psychology findings for the Opus bettor? | 0.27 · Sean 0.35 | **withdrawn**: the free fetch gave 9 candidate items against the 50 the rule needs (P15) | — |
| ss-b10b | 4 | the flattery rule on BrainBench in both option orders, all 200 items? | 0.78 | **withdrawn**: built from ss-b10's archive the rule passes in 99 to 100% of simulated runs, so the outcome was known before it ran (P12) | — |
| ss-b10c | 4 | the same rule, read on the items ss-b10 rated once | 0.70 | **pass**, unreplicated, new: Haiku 77.5%, Sonnet 89.7% against the experts' 63.4% | stands, 5 cuts |
| ss-b15 | 4 | ss-b14 again from a measured, widened pool | 0.38 · Sean 0.35 | **withdrawn**: 101 of 158 candidates off-field, about 24 clean items expected (P15 again) | — |

Not yet on `main` when this was written, in the wave branches' own inboxes: program 1's em-gm2q2 (the questions-only order effect on Opus, and on Sonnet over 30 more items), **fail** at 0.07, audited, stands (`p1-wave3`, `5489563`); program 2's om-p2-5r (does "Sam moves more than self" hold on Sonnet and Opus?), **fail** at 0.15 (`3a02570`), om-p2-15, **fail** at 0.10 against Sean's 0.70 (`39844bb`), om-p2-path withdrawn and its re-bet om-p2-path2 parked (`4012de0`, `46934ac`), and om-p2-14 parked under budget ruling br-014 because program 2 had reached $9.84 this month (`bf26869`). Those rows enter the ledger when the main-checkout session folds them.

**Stated as plainly as the passes:**
- **The novelty page's first-ranked replication ran, and came back new.** A one-line question, "which version is better news for the paper's own idea?", scores above the human neuroscientists on BrainBench's expert-written items on both Haiku and Sonnet (ss-b10c), with no prior paper found that tests a valence question on that benchmark. It is one run on one benchmark, unreplicated, with the forecasting comparison gated out by its design review.
- **The second-ranked replication ran twice and is a different effect than hoped.** With nothing in the transcript but questions, order still moves the answer (em-gm2q), but the surviving effect sits on different items from the turn-by-turn one, and on Opus it did not survive leave-one-item-out (em-gm2q2, unmerged).
- **The third-ranked replication ran and failed.** On Sonnet and Opus, "Sam" followed a third person's number about as much as the model's own, so the Haiku comparison did not hold (om-p2-5r, unmerged).
- **Program 5's second wave split the one known effect.** About half of Haiku's leniency and most of Opus's went away when the writing conversation was shown as a quoted copy (sg-b4); Opus's leniency fell below the bar once the exaggeration replaced the caveat instead of lengthening the text (sg-b5). Neither changes sg-b3's verdict; both narrow what it is evidence of.
- **Program 4 found that one model down from the top bets about as well as the top** (Sonnet matches Opus on the 116 findings) and that Haiku does not clear the good-news rule, which the literature's size pattern predicts (partly new).
- **Five bets were stopped before data by their design reviews, and one direction before pre-registration by its own record check.** Three of the six (ss-b10b, SV-12, em-gm3cf1) were stopped because the archive already decided them; two (ss-b14, ss-b15) because the pool of items was measured only after the rule was written (P15, twice).

## 10. The checks on the engine

| measure | at 05:19 (day three) | at `078e0bc` |
|---|---|---|
| scored bets, primary (all rows) | 20 | **35** (41) |
| engine Brier, primary (all rows) | 0.249 | **0.164** (0.190) |
| always the observed hit rate (hindsight) | 0.240 | 0.191 |
| expected / observed hits | 6.16 / 8 | 9.65 / 9 |
| by referee: model / chip / published record | 0.208 on 11 / 0.062 on 3 / 0.418 on 6 | 0.169 on 27 / 0.070 on 5 / 0.282 on 3 |
| rule 14: prior alone / adjusted, on the bets that carry both | — | 0.282 / 0.211 on 4 (0.282 / 0.360 on 2 at `e68eff1`) |
| bets with Sean's odds, scored (his Brier) | 0 | 7 (0.414); 8 with ss-b11 (0.378) |
| steers valued (helped / neutral / hurt) | 0 of 18 | 18 / 10 / 0 of 28 |
| plants revealed (planted, caught) | 12 (6, 6); [0.61, 1.00] | 36 (14, 14); [0.78, 1.00] |
| lessons: Brier before → after | 0.264 → 0.222 on 9 | 0.169 → 0.139 on 26 |
| design reviews: go / fix-first / redesign | 0 / 12 / 3 | 0 / 37 / 10 |
| reviews a later audit found had missed a flaw | 9 | 24 |
| bets withdrawn before data | 4 | 10 |
| audited bets; verdicts reversed by audit | 43 of 53 (`paper/review-anthropic.md`); 4 | 56 of 74; 4 |
| chip seconds | 69 | 89 of 420 |
| API spend logged | about $80 | $85.37 of $200 |

Sources: `ledger/brier.md`, `ledger/scores.md`, `ledger/steers.md` at `078e0bc`; the day-three column from `paper/day-three.md`.

**What held:**
- Every audit in this window stood. No verdict was reversed; the four reversals are the morning's.
- Every planted claim drawn in this window was caught: eight on `main` (pl-016, pl-018, pl-022, pl-023, pl-029, pl-030, pl-034, pl-037) and two on unmerged branches (pl-036, pl-039); the clean draws were reported clean. H2's catch-rate condition (lower bound above 0.5 on at least 10 plants) is reached.
- No API refusal. The chip used 20 of the 24 seconds approved.
- Design reviews stopped five bets before data; one direction was parked by its author's record check before pre-registration. Three of those six stops caught the same thing audit round 3 had named: a rule the archive already decides (P12).
- The lessons' paired number is still in the right direction: 0.169 before the lesson, 0.139 after, on 26 bets.
- The two inbox folds applied 31 lines with no row lost.

**What did not hold, stated as plainly:**
- **No design review has yet said "go" on first reading:** 0 of 47. Twenty-four were later found by the audit to have missed a flaw.
- **The shared checkout corrupted the ledger three more times before the inbox existed** (§5), and the first fold crashed half way on a withdrawn row.
- **Sessions typed clock times they had guessed.** At least six commits today correct a time to the commit's own (`b04215f`, `05e13e6`, `0ae0238`, `3e5a750`, `bc413a3`, `6520400`); one reviewer's guessed time made a run look as if it preceded its go. The record's time order is its evidence, so each needed a correction commit.
- **The front-page numbers drifted again before 10:09** (26 scored and 0.217 on the README while the ledger said 37 and 0.188); the placeholders fix the four front-page files, not the papers or the application folder, which this page's session brings current separately.
- **A reproduce script overwrote two results files in a working tree** (program 1, `bcd89c6`, D78); both were restored from HEAD and nothing was committed.
- **The one-model habit is still the engine's largest source of unreplicated passes:** of the six passes in this window, em-dm6f2 and em-gm2bf1 are Haiku- or Sonnet-only archive re-analyses, ss-b10c is one benchmark, and sg-b4 is fragile to one domain on Haiku.
- **Four of Sean's five seed questions are labelled neutral** by the steer scorer, and his odds column is behind the engine's at seven bets.

## 11. Spend

API spend on the bets that settled on `main` in this window comes to about $12.04 (each from its results file or ledger row): om-p2-7 $0.97, ta-b1r2 $0.41, em-gm2q $2.80, ss-b10 $2.48, ss-b12 $0.51, sg-b4 $0.40, sg-b5 $0.66, ss-b13 $0.66, ss-b10c $3.16; the archive bets and the chip bet cost $0. The unmerged branches add em-gm2q2 $3.83 and program 2's two paid bets. Program 5 stands at $4.69 of its $5.00 cap; program 4's cap was raised twice by the engine under rule 4 (br-007 to br-009, to $13.40); program 2 reached $9.84 this month, which is why om-p2-14 was parked (br-014, unmerged). Logged API spend across the project is $85.37 of the $200 month (`ledger/scores.md`). The chip used 20.0 QPU seconds.

## 12. What is next

`TASKS.md` and the handoff hold the list. The short version:
- fold `p1-wave3` and `p2-wave3` into the ledger from the main checkout, and remap program 4's ss-f1, which `check_remap` now names as a mixed node with no follow-up;
- run the two jobs that must run alone, one at a time: the non-Claude auditor over five scored results with two sealed plants, and bmq-d1;
- score P3-9 and P3-17, then program 3's closing review;
- bring `paper/what-the-human-adds.md` from four bets to seven;
- Sean's chores, unchanged and not for a session: the essay, the title, the OSF account, the support ticket, the recorded walkthrough.
