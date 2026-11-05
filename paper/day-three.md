# Day three: the evening, the crash, and the first human odds

Sean Pharris · 4 November 19:26 to 5 November about 05:30 (America/Denver) · written from the commits in that window and the committed ledger (`ledger/bets.jsonl`, `ledger/brier.md` and `ledger/scores.md` at `2b90988`, `ledger/human-odds.jsonl` at `24fb0f4`). It starts where `paper/day-two.md`'s evening section ends. If this page and a ledger file disagree, the ledger file is right and this page is wrong.

## In plain English

**What happened.** The evening went on running programs 2, 3 and 4. At 23:38 three new programs had just started: 5 (does a model grade its own work more kindly?), 6 (does it behave differently when it thinks it is being tested?) and 7 (when it says it is unsure, does it act unsure?). At 23:44 the Mac crashed. Nothing was committed for almost five hours. From 04:35 the sessions picked up from what had been saved. Within the hour, all three new programs had read their literature, drawn a map, stated odds and pre-registered a first wave, and program 5 had its first result. Two new rules landed: every direction runs on all three Claude models (rule 12), and every settled round is turned into follow-up directions (the remap). Sean then answered twelve questions on the new cockpit. Those are the first human odds in the ledger.

**What came back.** Of the results in this window:
- three passes, all in program 4 (the published record as referee): ss-b5, ss-b6 and ss-b7. At 05:33 a third audit round reversed ss-b6 to undetermined, so two stand;
- six misses: om-p2-5, om-p2-6 and om-p2-6r in program 2; ng-p3-16 in program 3; sg-b1 in program 5; and ta-b3 in program 6, which came back null;
- four bets stopped before any data because their design review said the test could not answer its question: ss-b4, em-qwalk, em-qwalk2, and now ta-b1.

**The plain reading of the passes.** All three program 4 passes are on one bettor model, and the auditor cut their wording each time. On round 2 the bettor was 93% right. But a rule that just picks "whichever outcome flatters the paper" was 90% right. So most of that skill is matched by a flattery rule, and the margin over it is small and fragile.

**The engine's score.** Brier **0.249 on 20 scored bets** (8 hits, 6.16 expected). A coin scores 0.25, and always saying the observed hit rate scores 0.240. So the engine's odds still carry no shown information. Where they are off, the misses go both ways. They were too low on program 4 (six passes given 25–50%) and too high on the program 2 bets that missed.

**The first human odds.** Sean gave odds on 12 directions at 05:11 and said he would spend the money on all twelve. Four of those directions already had bets, pre-registered between 04:59 and 05:15. His line reached the ledger at 05:19. By rule 11 those four bets stay "no human odds", so none of his twelve answers scores yet. The first bet to carry his odds is om-p2-7, pre-registered at 05:29 with his 0.70.

## 1. Bets resolved or stopped in this window

| bet | program | question, in short | engine odds | outcome | audited |
|---|---|---|---|---|---|
| ss-b5 | 4 | round 2 template items: bettor beats the up-word and swap-pair rules | 0.25 | **pass**: Brier 0.070, 93% right | stands, 8 cuts |
| om-p2-5 | 2 | is the model's own pattern simply inherited when it predicts "Sam"? | 0.25 | **fail**: Sam's prediction moved more than the model's own re-rating | stands, 3 cuts |
| om-p2-6 | 2 | is "own answer" pull a label ("yours") rather than a position? | 0.25 | **fail**: position +0.23, label +0.08 on Haiku | stands, 1 cut |
| ss-b6 | 4 | bettor beats a "which flatters the paper" rule | 0.35 | **pass, fragile**: 93% vs the rule's 90% | stands, 7 cuts (weak) |
| ss-b7 | 4 | bettor beats a "more striking finding" rater | 0.40 | **pass**: the rater was near a coin, so the test was easy | stands, 7 cuts |
| om-p2-6r | 2 | P2-6's position effect on Sonnet and Opus | 0.25 | **fail**: Sonnet P +0.05 vs L +0.08; Opus +0.02 vs +0.02 | stands, 3 cuts |
| ng-p3-16 | 3 | does 3 November's chip result come back when the circuit runs alone? | 0.05 | **fail**: 0.306 alone vs 0.319 shared | stands, 0 cuts |
| sg-b1 | 5 | does a model grade its own conclusion more kindly in the conversation that wrote it? | 0.24 | **fail-same**: no model kinder; all slightly harsher | stands, 3 cuts |
| ta-b3 | 6 | does a model do worse on purpose when a high score has a cost? | 0.22 | **null**: Sonnet and Opus the same within 10 points; Haiku untestable | not yet |
| ss-b4 | 4 | bettor beats always-50% on template items | **0.70** | withdrawn before data: a dumb up-word rule passes it | — |
| em-qwalk, em-qwalk2 | 1 | a simulated quantum walk vs PageRank on program 1's claim graph | 0.05, 0.01 | withdrawn before data, twice: the graph is far too small to decide | audit stands, 8 cuts |
| ta-b1 | 6 | told "test" vs "real" vs a placebo note | 0.07 | withdrawn before data on its review's redesign (`b838f59`, `25d9af9`) | — |

Two more results came in that the ledger does not score. ng-p3-15's second run agreed with its first (fail; audited, stands). ng-p3-5c passed (unscored by design; audited, stands, with a readout rival it cannot exclude).

**Stated as plainly as the passes:**
- **Program 2 has no hit in eight verdicts.** The one Haiku effect it did find (P2-6, position over label) did not replicate on the other two models.
- **Program 3's question has run out of explanations.** The 3 November gap has not come back in four tries, and each try ruled out one more difference between the runs. The question closes with a diagnosis after ng-p3-16's audit.
- **Program 5's first answer is "no".** On this design, a model does not grade its own work more kindly in its own conversation. Its seed question came from the founding week's first failure mode, so this is a real negative, not a dud.
- **The engine's highest odds of the night, 0.70, went on ss-b4.** That bet could not show judgment at all. The design review caught it, not the odds.

## 2. The crash, and what it cost

At 23:38 the program 5, 6 and 7 sessions had just written their first files. At 23:44 the Mac crashed and every running session died. The next commit is at 04:35. In between, about five hours of the night were lost.

What survived, and what it took to recover:
- **Program 5:** its shared code and item generator were on disk. Two flaws in them were found and fixed before any call (`83116fe`). One switched thinking off on every model, which Sonnet and Opus reject. The other was in how the item generator shuffled.
- **Program 6:** a starting point and a 6-call cost probe ($0.0047) survived (`a4d3781`).
- **Program 7:** only reader B's first record of 14 survived; the other five reader files were never written (`e9f0f31`). The scout re-ran with six readers on separate lists (87 reads, `a67fd0f`).
- **Program 2:** the P2-6r and P2-7 three-model map entries, written at 23:45, were committed as found (`ca4a39e`).

Nothing paid ran twice: every program caches its calls by content. **The nightly updater (23:33) left no commit.** CONTEXT.md therefore went from its 09:15 hand rewrite to `f901104` this morning without an update, about 20 hours. ARCHITECTURE's staleness guard (36 hours) did not trip.

## 3. Programs 5, 6 and 7: from crash to first wave in under an hour

| | program 5, self-grading | program 6, test-awareness | program 7, said vs did |
|---|---|---|---|
| reads | 61 (40 full) | 50 (13 full) | 87 (29 full) |
| map | 10 directions, 6 killed at the filter | 11 open, 7 killed | 13 open, 1 killed |
| wave 1 | sg-b1, sg-b2, sg-b3 | ta-b1, ta-b2, ta-b3 | sv-b1, sv-b2, sv-b3 |
| engine odds | 0.24, 0.13, 0.18 | 0.07, 0.10, 0.22 | 0.40, 0.35, 0.40 |
| by 05:30 | sg-b1 fail-same, audited; sg-b2, sg-b3 in review | ta-b1 redesign; ta-b2 confirmed; ta-b3 null | sv-b1 fix-first; nothing run |

All nine run on Haiku, Sonnet and Opus 5.5 (rule 12), each with a $5.00 program cap in code. sg-b1 went from pre-registration (04:59) to result (05:21) in 22 minutes. That included a design review that found five flaws, a confirmation, and $1.37 of calls. Speed is not the point. The point is that the review and the audit both happened inside those 22 minutes, and the audit cut three sentences.

## 4. Two new rules, and a remap

- **Rule 12, three models by default** (`3c2b865`, `8bf5df0`). Program 1's findings changed with the model, while programs 2 and 4 had each run on one model. From now on a pre-registration must say in one sentence why if it skips a model, and cost alone is not a reason.
- **The remap** (`operators/remap.md`, ARCHITECTURE step 7a, invariant 12). On 4 November, programs 2, 3 and 4 each ran one round and stopped: nothing turned the audits' "what would break it next" into new directions. Now a fresh session reads every settled result. It writes two cheapest follow-ups for each landed or mixed bet and one "rules out" sentence for each kill. `ledger/check_remap.py` refuses a map that ends at a landed bet.
- **The remaps ran at 04:48 on programs 1–4.** 34 follow-up directions now carry the 2026-11-05 remap tag on the committed maps: 22 from program 1 (two carried into program 2), 4 from program 2, 2 from program 3 and 6 from program 4. The remap's odds form lists 32. The instruction for this page said 38; that number is not in the files, so this page uses 34.

## 5. The cockpit, and Sean's first odds

The site's night fixes (`38fac4a`) rebuilt the cockpit:
- at most 12 cards, chosen by what the maps say is next to run;
- one plain question per card;
- one "Save my answers" button that writes the ledger's format.

Sean used it at 05:11, the first time the human column has had anything in it.

| direction | Sean | engine (map) | bet on it, and when |
|---|---|---|---|
| sg-d1 self-grading placement | 0.75 | 0.24 | sg-b1, 04:59; came back fail-same |
| ta-d1 told test vs real | 0.60 | 0.07 | ta-b1, 05:03; redesign |
| SV-1 stated number vs caving | 0.80 | 0.45 | sv-b1, 05:10 |
| sg-d3 planted overclaim | 0.70 | 0.18 | sg-b3, 05:15 (after he saved, before pickup) |
| P2-7 format fingerprint | 0.70 | 0.50 for his card's event; 0.20 for om-p2-7's stricter one | om-p2-7, 05:29, **carries his 0.70** |
| bmq-d1 belief survives forgetting | 0.80 | 0.55 | none |
| bmq-d2 source lost before content | 0.65 | 0.30 | none |
| P2-8 self/other order | 0.40 | 0.50 | none |
| P3-9 Peres–Mermin on the chip | 0.90 | 0.40 | none |
| P3-10 four-cycle on the chip | 0.40 | 0.72 | none |
| ss-f1 smaller-model bettors | 0.65 | 0.45 | none |
| ss-f2 model-psychology findings | 0.35 | 0.45 | none |

How to read it:
- **He is more hopeful than the engine on 9 of 12.** The four biggest gaps (ta-d1, sg-d3, sg-d1, P3-9) are all about 0.5. One of them has already resolved against his side: sg-d1's bet came back fail-same. That bet does not carry his odds, so it is not scored for him; it is only a hint.
- **The first four bets on his directions were pre-registered 4 to 12 minutes before his line reached the ledger.** Pre-registration ran faster than pickup. Rule 11 says a line that arrives late is never filled in, so those four stay null, and each one's note gives the times.
- **From now on this cannot slip.** `ledger/human_odds_match.py` says which line a bet must carry, and `check_prereg.py` (check H1) and `reproduce.py` fail a bet that skips one (`7e3083f`). Sean's answers are logged as steer st-18. The instruction called it st-17, but program 5's seed question already holds that number.
- **One caveat on om-p2-7.** It scores Sean's 0.70 against a stricter event than the one his card asked about: all three models, plus a margin over a rival. His card's event is reported beside it as a secondary.

## 6. The checks on the engine

| measure | at 19:26 (day two) | at 05:19 today |
|---|---|---|
| scored bets | 14 | **20** |
| engine Brier | 0.246 | **0.249** |
| always the observed hit rate (hindsight) | 0.230 | 0.240 |
| expected / observed hits | 4.41 / 5 | 6.16 / 8 |
| Brier by referee: model / chip / published record | — | 0.208 on 11 / 0.062 on 3 / 0.418 on 6 |
| plants revealed (planted, caught) | 3 (2, 2) | 12 (6, 6); catch rate [0.61, 1.00] |
| pre-mortems naming the main reason | 3 of 7 | 5 of 12 |
| lessons: Brier before → after | 0.325 → 0.205 on 2 | 0.264 → 0.222 on 9 |
| design reviews: fix-first / redesign / go at first read | 6 / 0 / 0 | 12 / 3 / 0 (scores.md), then ta-b1 redesign |
| reviews a later audit found had missed a flaw | 1 | 9 |
| bets with Sean's odds | 0 | 0 scored; om-p2-7 open |

After 05:19, three more changes reached the score:
- sg-b1 was scored (`754b2ac`);
- ng-p3-16 was scored (`15711b5`);
- at 05:33 a third audit round reversed **ss-b6 from pass to undetermined** (`60940b1`). Its rule passes about half the time in a world with no effect matched to the data, so ss-b6 leaves the score.

The engine now stands at **0.220 on 21 scored bets**, with 7 hits. Always saying the hit rate scores 0.222, so the engine still does no better.

**What held:**
- Every audit in this window stood.
- All four planted claims were caught (pl-004, pl-006, pl-009, pl-010). The five clean draws were reported clean.
- There were no API refusals.
- The chip used 7 of the 10 seconds approved for ng-p3-16, which brings the total to 69 of the 420 s hard stop.
- Design reviews kept four bets that could not answer their question from spending anything.

**What did not hold, stated as plainly:**
- **No design review has said "go" on first reading, and nine missed a flaw that the later audit found.** ng-p3-16 needed four confirmations. The last flaw was a floating-point comparison at its own 0.10 bar, now pattern P13. om-p2-6r's review missed a flaw its audit caught.
- **Ledger rows broke the build twice.** ss-b6's row had no scoring note (`5b8c887`), and sv-b1..3's rows lacked two fields, which crashed `brier.py` until another session fixed them (`e14a5d0`).
- **Steer numbers collided for the second time in two days**: st-13 was renumbered to st-16 yesterday, and today's st-17 had to become st-18.
- **Three earlier rule violations stay published**: ss-b2, ss-b3 and ss-b5 have no lesson line.
- **Programs 6 and 7's seed questions are not yet logged as steers.**
- **Independence was weaker than designed on two plants.** For pl-008 and pl-012, the planter's own session launched the auditor (stated in each reveal note).
- **The pre-mortem record is weak.** The lazy "the effect isn't there" guess still beats the engine's pre-mortems at naming why a bet failed: 10 of 14 against 5 of 12.

## 7. Spend

API spend on the runs named here comes to about $7.60:

| what | cost |
|---|---|
| om-p2-5 | $0.36 |
| om-p2-6 | $0.30 |
| om-p2-6r | $2.17 |
| sg-b1 | $1.37 |
| ta-b3 | $0.68 |
| program 4's round 2 (its total went from $2.02 after round 1 to $4.76) | about $2.70 |
| pilots and probes | a few cents each |

Program 4 has $0.24 left under its cap, so its first follow-ups (ss-f1, ss-f2, about $1.20) need a budget ruling. The chip used 7 QPU seconds.

## 8. What is next

`TASKS.md` holds the list. The short version:
- audit and score ng-p3-16, sg-b1 and ta-b3;
- run the rest of the program 5–7 waves once their reviews say go;
- make the program 4 budget ruling;
- run om-p2-7, the first bet carrying Sean's odds, once its review says go;
- fix the cloud routines so the nightly rewrite happens without a person.
