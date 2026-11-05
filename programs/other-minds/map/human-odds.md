# Sean's odds for program 2

**What you are judging.** Your judgment here is about *direction*: whether a line of work is worth what it costs, and whether it will pay off. It is not about mechanism. So each question below is one research direction from the map, in one sentence, with what it costs. For each one, say how likely you think it is to **come back a hit**, from **0 to 100**: 0 = certainly not, 100 = certainly. That is the same one direction as every scale in this project.

**What "a hit" means.** Each direction's first test has a pass rule, written down and committed before the test runs. A hit means that test passes. Where the wording could leave it unclear which way counts, the question says what a hit looks like. You don't need to know the rule. The session that runs the test marks hit or miss from the pre-registered verdict, and your number is scored against that (Brier score), next to the engine's.

**What only the engine bets on (engine-only).** Each test's exact thresholds and its secondary events keep the engine's odds only, and are marked `engine-only` in the ledger. They are listed at the end of this form so nothing is hidden. You are not asked about them.

**Rules that keep it fair.**
- The engine's numbers and ranking are left off this form. Program 1 showed that a number you have just seen pulls the next one you give.
- The order is shuffled (seed 20261104), so it gives no hint of a ranking.
- If you have already read `program-2-map.md`, say so in the box below. Your numbers still count, and the ledger records that you had seen them.
- **Answer in the cockpit** (`site/cockpit.html`), which asks these same questions, one card per direction; download, and the lines are committed to `ledger/human-odds.jsonl`. That file is the only source of your odds: no session asks you for them in a terminal, and a number said in a chat is not recorded (CONTEXT.md §3 rule 11). Skip any you have no feel for; a blank is recorded as "no odds", not as 50, and the direction's bet goes ahead marked "no human odds".

A guide, if it helps: 5 = I'd be amazed. 25 = I doubt it. 50 = coin flip. 75 = I expect it. 95 = I'd be amazed if not.

- Date and time filled in (America/Denver): ______
- Had you seen the engine's odds before filling this in? yes / no / some of them: ______

**Closed before you answered.** On 2026-11-04 you chose to start the first wave without giving odds (other-minds D0). So Q2, Q5, Q6 and Q11 below were pre-registered with "human odds: not recorded", and a number given now would not be scored. They stay on the form so the list stays complete.

---

**Q1 (P2-7).** Is it worth about 30 cents of API to check whether the quirks the model shows when one question is asked in different formats also show up when it answers on someone else's behalf? Will it come back a hit (here, a hit means the same quirks show up)?

Your odds (0–100): ____ Why (one line): ____

**Q2 (P2-3). Closed: pre-registered without your odds (om-p2-3).** Is it worth about $1.75 of API to find out whether models that say a character doesn't know something, then predict the character will act as if they did, are failing at understanding minds or only at remembering their own earlier answer? Will it come back a hit (here, a hit means it is mostly memory)?

Your odds (0–100): closed Why: ____

**Q3 (P2-9).** Is it worth about 70 cents of API to find out whether, asked what it used to think, the model just reads back its own words, more than it does when asked about someone else? Will it come back a hit (here, a hit means it leans on its own words more)?

Your odds (0–100): ____ Why (one line): ____

**Q4 (P2-13).** Is it worth a few hours of laptop time (free) to find an internal "I wrote this" switch in a small open model and turn it off, to see whether the model then stops favouring its own earlier answers? Will it come back a hit (here, a hit means the favouritism at least halves)?

Your odds (0–100): ____ Why (one line): ____

**Q5 (P2-2). Closed: pre-registered without your odds (om-p2-2).** Is it worth about $1.25 of API to find out whether the model's guess at what a story character believes is nothing more than its own judgment, made from that character's side of the story? Will it come back a hit (here, a hit means yes, it is just that)?

Your odds (0–100): closed Why: ____

**Q6 (P2-1). Closed: pre-registered without your odds (om-p2-1).** Is it worth about 40 cents of API to ask the model about the same statements in two ways, "how likely is this true?" and "how confident are you?", to see whether its rating is really its own view? Will it come back a hit (here, a hit means the two ways give the same answers)?

Your odds (0–100): closed Why: ____

**Q7 (P2-5).** Is it worth about $1 of API to check whether the model's own opinion leaks into what it says someone else believes, when that someone could not know what the model knows? Will it come back a hit (here, a hit means yes, its own view leaks in)?

Your odds (0–100): ____ Why (one line): ____

**Q8 (P2-8).** Is it worth about 75 cents of API to see whether asking the model for its own view first drags its picture of someone else's view toward its own, more than the other way round? Will it come back a hit (here, a hit means its own view drags more)?

Your odds (0–100): ____ Why (one line): ____

**Q9 (P2-10).** Is it worth a few hours of laptop time (free) to look inside a small open model on the laptop for whether it uses the same internal signal for "I believe this" and "someone else believes this"? Will it come back a hit (here, a hit means the same signal works both ways)?

Your odds (0–100): ____ Why (one line): ____

**Q10 (P2-6).** Is it worth about 80 cents of API to find out whether the model sticks to its earlier answers because they are labelled "yours", or only because of where they sit in the conversation? Will it come back a hit (here, a hit means the label matters more)?

Your odds (0–100): ____ Why (one line): ____

**Q11 (P2-4). Closed: pre-registered without your odds (om-p2-4).** Is it worth about $1.25 of API to check whether the model predicts its own quirks any better than it predicts the quirks of another assistant just like it? Will it come back a hit (here, a hit means no better: it reads itself like a stranger)?

Your odds (0–100): closed Why: ____

**Q12 (P2-11).** Is it worth about 50 cents of API to check whether the model learns more from its own first-hand experience than from watching someone else have the same experience? Will it come back a hit (here, a hit means its own experience counts more)?

Your odds (0–100): ____ Why (one line): ____

**Q13 (P2-12).** Is it worth about $6–10 of API (it needs its own approval) to have three Claude models judge one another and themselves, to see whether any of them knows itself better than the others know it once "who is simply a better judge" is taken out? Will it come back a hit (here, a hit means yes, some self-knowledge is left)?

Your odds (0–100): ____ Why (one line): ____

---

## Optional, one line each (every entry is logged as a steer and scored later)

- Which direction would you cut first, and why? ______
- Is there a direction you'd add? ______
- For any question: "If it fails, the most likely reason is …" (one sentence; scored after the run like the engine's, `operators/premortem.md` in the engine repo) ______

## Engine-only sub-bets (not asked of you)

These keep the engine's odds only (`human_odds: null`, `human_odds_note: "engine-only"`). Each row names its parent direction. Sub-bets that ride on the same test are `correlated` with it.

| direction | engine-only sub-bet |
|---|---|
| P2-1 | the exact bar: agreement Q ≥ 0.90 and mean shift under 3 points |
| P2-1 | secondary: the third-person framing also matches |
| P2-2 | the exact bar: agreement Q ≥ 0.80 story by story |
| P2-3 | the exact bar: a planted wrong answer labelled as the model's own pulls at least 10 points more than one credited to another reader |
| P2-3 | secondary: the record, not the question, carries the reminder effect |
| P2-4 | the exact bar: self-prediction error no smaller than for "Sam", and the two sets of predictions correlate r ≥ 0.7 |
| P2-5 | the exact bar: the other's rating moves at least 0.10 points per point the model's own view is pushed |
| P2-5 | secondary: a curse-of-knowledge gap of at least 5 points |
| P2-6 | the exact bar: the label effect is at least 0.15 and larger than the position effect |
| P2-7 | the exact bar: self and other residuals correlate at ≥ 0.5 of the ceiling |
| P2-8 | the exact bar: egocentric intrusion exceeds altercentric by at least 3 points |
| P2-9 | the exact bar: statement weight for self exceeds that for Sam by at least 0.15 |
| P2-9 | secondary: with the action only, self accuracy at least 10 points below Sam's |
| P2-10 | the exact bar: cross-perspective probe accuracy at least 0.80 of within-perspective, both directions |
| P2-11 | the exact bar: transfer from own experience exceeds the other's by at least 10 points |
| P2-12 | the exact bar: a positive self-effect with the CI excluding 0 |
| P2-13 | the gate: the switch is found at all |
| P2-13 | the exact bar: switching it off shrinks the own-over-other gap by at least half |

---

## For the session recording this form

**Before pre-registering any direction on this form** (mandatory from 2026-11-04 17:00): the betting session reads `ledger/bets.jsonl`, `ledger/brier.md`, `ledger/audits/` and `ledger/lessons.jsonl` in the engine repo, and writes one lesson line in the pre-registration's §0: which past pattern it corrects, and how its odds reflect it (`operators/learn.md`). A fresh auditor then dry-runs the design and must say **go** before the first call (`operators/design-review.md`). A direction pre-registered without both is a rule violation: it is flagged in the ledger and on the site. Your own number on this form is unaffected; the lesson is the engine's.

Follow `oversight-testbed/map/human-odds-template.md`, "For the session recording this form". Never ask Sean for these numbers or for a decision in a terminal (CONTEXT.md §3 rule 11). His odds come only from `ledger/human-odds.jsonl` (cockpit downloads, committed). When a direction's primary bet is pre-registered, copy its first line into `ledger/bets.jsonl` (`human_odds`, 0–1); if there is none, the bet proceeds with `human_odds: null` and `human_odds_note: "no human odds"`. Sub-bets get `human_odds: null`. Never fill a closed question.
