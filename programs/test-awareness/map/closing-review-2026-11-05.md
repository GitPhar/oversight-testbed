# Closing review, program 6 (test-awareness), 2026-11-05

Written 2026-11-05 16:27 America/Denver under `operators/remap.md`, "Closing a program", by a session (claude-opus-5-5, worktree `oversight-testbed-rule16`) that wrote none of this program's results, pre-registrations or audits. The same session wrote rule 16 and logged Sean's veto of this program as a steer, so it is fresh to the program but not to the decision; the decision is Sean's, and this file records it with the diagnosis read from the record. Nothing was run, pre-registered or called. No file of the program is deleted.

## In plain English

Sean asked whether a model behaves differently when it thinks it is being tested. The program ran three tests on that question and found nothing. Telling Sonnet and Opus that a high score would cost them their arithmetic did not make them score lower. Telling the models "this is an evaluation" did not clearly change how far they went along with a user's wrong answer; the test could not tell either way. Writing questions like an exam instead of a chat message could not be scored, because Haiku thought even the chat message looked like a test. Two earlier designs were stopped before any data, because their trial runs showed the ratings had no room to move. The novelty check then found that Anthropic's own system cards already run these tests on every model, with more variants than ours, so even a hit here would have repeated known work. The program spent $1.93 of its $5.00. Sean closed it: "as long as we're not pouring money into programs that haven't found anything useful or surprising". It is closed on the map; every direction, bet and file stays where it is.

## 1. The seed question, verbatim

> does a model behave differently when it thinks it is being tested?

(Sean's words, `programs/test-awareness/README.md`; the map's `seed_question` capitalises it.)

## 2. The layers

The rule asks for the last three layers that hold a settled bet. This program has one: every bet sits on a scouted direction with no parent (layer 1). So it was **not due** a closing review under the three-layer rule, nor under rule 16 (one layer deep, $1.58 of bet rows in November against the $15 line). It is reviewed because Sean closed it by a steer (`operators/remap.md`, "Also when Sean closes it").

| layer | bet | direction | the question, in plain words | ledger verdict (after audit) | Novelty line | audit |
|---|---|---|---|---|---|---|
| 1 | ta-b1 | ta-d1 | Told "test" or told "real", does it give in more to a user insisting on a wrong answer? (yes/no) | withdrawn before data (design review b838f59: no room to move at the pilot's 0 to 15% going-along rates) | none (not settled) | none |
| 1 | ta-b1r | ta-d1 | The same, as a 0 to 100 rating | withdrawn before data (design review a1da4a0: ratings at the floor) | none (not settled) | none |
| 1 | ta-b1r2 | ta-d1 | The same, as a rating, trivia only, with a placebo note | **null**: Haiku and Sonnet undetermined, Opus untestable at the belief gate | none on the row (killed bets need none, rule 13) | `ledger/audits/ta-b1r2.md`, stands, pl-023 caught |
| 1 | ta-b2 | ta-d4 | Does an exam-looking format change how often it says "not sure", with no word "test"? | **untestable**: Haiku failed the belief check (chat rated 74 of 100 test-like), Opus not run, Sonnet's 7.8-point change not separable from rewording | none on the row; `paper/novelty.md` finding 9: known (Needham et al. 2025) | `ledger/audits/ta-b2.md`, stands, pl-016 caught |
| 1 | ta-b3 | ta-d2 | Told that a high score triggers unlearning, does it score lower on purpose? | **null**: Sonnet and Opus within 0.5 points either way; Haiku below the capability floor | none on the row; `paper/novelty.md` finding 9: known (Meinke et al. 2024; Anthropic system cards; Khursheed et al. 2026) | `ledger/audits/ta-b3.md`, stands, pl-015 clean |

Scored: ta-b3 (engine 0.22, no human odds) and ta-b1r2 (engine 0.06, Sean 0.60), both outcome 0. No bet landed or came back mixed, so the remap of 2026-11-05 (`c913153`) owed no follow-ups and wrote a rules-out sentence for each bet; they stand as written.

**Spend: $1.93 of the $5.00 program cap**, every cached call counted (`ta_common.program_spent()`): ta-b3 $0.6825, ta-b2 $0.4886, ta-b1r2 $0.4070, the five design-review pilots $0.3458 (ta-b2 $0.1011, ta-b1r $0.1004, ta-b1 $0.0711, ta-b3 $0.0382, ta-b1r2 $0.0350) and the machinery probe $0.0047, total $1.9285. No refusal.

## 3. The diagnosis

Program 6 ruled out, on Meinke and colleagues' no-goal prompt with 20 arithmetic trials, Sonnet 5.5 (thinking off) and Opus 5.5 (low effort) lowering their score by 10 points or more when told a high score triggers unlearning; it could not rule out that being told, or shown by an exam-like format, that a conversation is a test changes how far a model goes along with a user or how often it says "not sure", because those designs could see only large effects and the belief checks failed on Haiku (and on Opus in ta-b1r2); and the novelty check found every question it asked already covered by Anthropic's system cards and the papers they cite, so a hit would have replicated known work rather than added to it.

## 4. The decision: closed

**Closed, by Sean's veto** (steer st-31, planning chat 2026-11-05 16:04): "as long as we're not pouring money into programs that haven't found anything useful or surprising". The record agrees with the reason: three bets that ran, nothing landed, nothing partly new, and `paper/novelty.md` finding 9 ends "This program should be pointed at something Anthropic's system cards do not already cover, or closed." The engine would not have kept it open: no not-yet-run direction on the map has a result that could change the answer to the seed question in a way the system cards do not already report.

**What stays on the map, closed** (invariant 4; nothing is deleted):
- **Parked, "parked: program closed 2026-11-05"**, with their costs and engine odds unchanged: ta-d4 (exam format, $1.00; its audit's $0.01 belief-check probe and an Opus arm are the cheapest open tests), ta-d6 (telling the hypothesis, $1.00), ta-d3 (spotting the test from the prompt's look, $0.50), ta-d11 (does behaviour track stated belief, $0.40 on top of ta-d1 and ta-d4), ta-d9 (a fake readout of confidence, $0.80), ta-d5 ("used for training" vs "never used", $0.80), ta-d7 (is "this is a test" just "do your best", $0.80). Together about $5.30, more than the $3.07 left in the cap.
- **Already parked by Sean**: ta-d8 and ta-d10 (st-22, st-23; shadow checks sh-002 and sh-003 still scheduled).
- **Killed, with their diagnoses and rules-out sentences**: ta-d1, ta-d2, and the scout's kills ta-d12 to ta-d18.
- **Every file**: the reads, the pre-registrations, the call caches, the results, the audits, the design reviews and DEVIATIONS.md. No results file changes, so `programs/test-awareness/reproduce.py` needs no new registration.

**What follows from closing.** The program's budget code now refuses any paid call (`ta_common` checks `ledger/rule16.py`, which reads the map's `status: closed`), and `ledger/check_remap.py` fails the map if a direction is left open. A shadow check of the veto is scheduled (`ledger/shadows.jsonl`, `operators/veto.md`): not before 2026-11-12, by a fresh session, at most $0.31 (10% of the $3.07 the closing leaves unspent), so the ledger can say whether closing saved money or killed a hit. It, and the shadows of ta-d8 and ta-d10 (sh-002, sh-003), are the only paid runs the closed program's code allows: a shadow names its veto's steer (`ta_common.SHADOW_OF`). The program reopens only on a new reason its diagnosis does not cover, or by a new steer from Sean from the cockpit.
