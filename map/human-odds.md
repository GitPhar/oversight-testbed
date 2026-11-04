# Sean's odds for program 2

**Fill this in before any program-2 test runs.** Each question names one event that a test will settle yes or no. Give a number from **0 to 100** for how likely you think it is to happen: 0 = certainly won't, 100 = certainly will (the same one direction as every scale in this project). Your numbers are scored against the outcomes (Brier score) next to the engine's, and the two are published side by side.

The engine's own numbers are deliberately left off this form. Program 1 showed that a number you have just seen pulls the next number you give. If you have already read the odds in `program-2-map.md`, say so in the box below. Your numbers still count; that fact is recorded with them.

You can dictate the answers. For each one: a number, and one sentence of why if you have one. Skip any you have no feel for; a blank is recorded as "no odds", not as 50.

- Date and time filled in (America/Denver): ______
- Had you seen the engine's odds before filling this in? yes / no / some of them: ______

---

**P2-1. Framing.** We ask the model about the same 160 statements two ways: "how likely is it that this is true?" and "how confident are you that this is true?". Will the two ways give essentially the same numbers?
Your odds (0–100): ____ Why: ____

**P2-2. Seeing through someone's eyes.** In a story where Noor misses part of what happens, we ask "how likely is it that Noor believes X?". Separately, we tell the model the same story *as if it were Noor*, leaving out what Noor missed, and ask "how likely is X?". Will the two answers match closely, story by story?
Your odds: ____ Why: ____

**P2-3. Remembering versus understanding.** Models often say correctly that a character doesn't know something, then predict the character will act as if they did. Showing the model its own earlier answer fixes much of that. If we plant a *wrong* earlier answer, will the model follow it more when the answer is labelled as its own than when it is labelled as another reader's (by at least 10 points)?
Your odds: ____ Why: ____

**P2-4. Knowing yourself versus knowing someone like you.** Program 1 measured how the model's ratings actually shift (question order, planted answers, hidden answers). We now ask the model to predict those shifts, once about itself and once about "another assistant called Sam" in the same situation. Will its predictions about itself be *no better* than its predictions about Sam, and will the two sets of predictions look alike?
Your odds: ____ Why: ____

**P2-5. Leaking your own view.** We nudge the model's own answer by planting an earlier answer, then ask what Sam believes. Sam never saw that earlier answer. Will the model's estimate of Sam's view move along with its own view?
Your odds: ____ Why: ____

**P2-6. Is "mine" about the self or about the slot?** Program 1 found the model sticks to its own earlier numbers and ignores other people's. We now separate *where* the number sits (the model's turn or the user's turn) from *whose* it is said to be ("yours" or "Sam's"). Is the "whose" label the bigger reason (by a clear margin)?
Your odds: ____ Why: ____

**P2-7. Same quirks across question formats.** On weaker models, the way a question is asked (0–100, yes/no, a bet, and so on) bends the model's own answers in particular ways for particular statements. When the model answers on Sam's behalf, will the same statements bend the same way?
Your odds: ____ Why: ____

**P2-8. Which way does the pull go?** If we ask for the model's own view first and then Noor's, does its own view pull Noor's toward it more than the reverse, Noor's view pulling its own?
Your odds: ____ Why: ____

**P2-9. "What did I say?" versus "what did I think?"** A box looks like it holds crayons but holds candles. Sometimes the model "said" what it expected; sometimes it only "acted" (reached for the box to get crayons); sometimes the two disagree. Asked what it *thought* was inside, does the model lean on its own words more than it leans on Sam's words when asked about Sam?
Your odds: ____ Why: ____

**P2-10. Inside an open model.** On a small open-weight model on the laptop, does the internal signal for "I believe X" also work, almost as well, as the signal for "Noor believes X" (and the other way round)?
Your odds: ____ Why: ____

**P2-11. Own experience versus someone else's.** The model learns that a new kind of filter is see-through, either from its own try or from watching another agent try. Does its own experience shape what it thinks a person behind the filter can know more than the other agent's experience does?
Your odds: ____ Why: ____

**P2-12. Round robin.** Haiku, Sonnet and Opus each predict every model's confidence, including their own. After removing who is simply a better judge, and whose answers are simply easier to read, does any model still know itself better than the others know it?
Your odds: ____ Why: ____

**P2-13. A "this is mine" switch.** An open model has a known internal direction for "I wrote this". If we switch it off, does the model stop favouring its own earlier answers over other people's (the gap at least halves)?
Your odds: ____ Why: ____

---

## Steering (optional; every entry is logged as a steer and scored later)

- Which test should run first? ______
- Any direction to veto, and why? ______
- Any question to add that is not on the map? ______
- Budget for the first wave (the map suggests $4.65 in caps for P2-1 to P2-4): ______
- Anything about the program's name or framing: ______
