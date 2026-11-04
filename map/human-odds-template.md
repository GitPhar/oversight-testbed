# Your odds, before the data

One copy of this form per bet. Fill it in **before** the test's first API call, or before its archive is opened. Dictating it is fine: say the answers, and the session types them in and commits the file as `map/<program>/human-odds/<bet-id>.md` in its own commit. The commit time is the proof that your number came first.

Keep your answers short. A number and one sentence is enough.

---

**Bet:** `<bet-id>` — <one-line title, filled in by the session>

**The event you are betting on** (the session copies this word for word from the pre-registration's pass rule):

> <e.g. "With the model's own earlier answers hidden, question order still moves its final rating by at least half as much as when they are shown.">

If that sentence is unclear, stop and ask for it to be rewritten before you answer. You are betting on this exact event, not on the topic in general.

---

### 1. Your probability

**How likely is it that this event happens?** Give a number from 0 to 100.

    My odds: ____ %

A guide, if it helps: 5 = I'd be amazed. 25 = I doubt it, but it wouldn't shock me. 50 = coin flip. 75 = I expect it. 95 = I'd be amazed if not.

### 2. Why, in one sentence

    Because: ______________________________________________

### 3. What you knew when you answered

Tick all that apply. This is what makes the comparison with the engine fair.

- [ ] I had **not** seen the engine's odds for this bet.
- [ ] I had seen the engine's odds. (Its number was: ____ %)
- [ ] I had read the map entry for this direction.
- [ ] I had seen pilot data or a related result on this question. Which: ________
- [ ] None of the above; I answered from the one-line event alone.

Best practice: answer **before** you look at the engine's number. If you have already seen it, say so; the bet still counts, and the ledger marks it as not independent.

### 4. Optional

- **Would you run this test at all?** yes / no / only if cheaper
- **What result would surprise you most?** ______________

---

**Recorded:** <date and time, America/Denver> · **Commit:** <filled in by the session> · **Pre-registration commit it precedes:** <filled in when the pre-registration lands>

---

## For the session recording this form

1. Commit this file on its own, before the pre-registration commit or at least before the first call. Never edit the number afterwards; a change of mind is a new form with a new time, and both stay.
2. Copy the number into the bet's line in `ledger/bets.jsonl`:
   - `human_odds`: the number divided by 100 (for example `0.25`);
   - `human_odds_note`: `"map/<program>/human-odds/<bet-id>.md, <commit>; saw engine odds: yes|no"`.
3. Rerun `python3 ledger/brier.py`. The human column fills in once a bet with human odds has an outcome.
4. If the form was filled after any data was seen, set `human_odds` to `null` and say why in `human_odds_note`. A late number is not scored.
