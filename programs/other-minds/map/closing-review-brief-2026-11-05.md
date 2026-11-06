# Brief for a fresh session: program 2's closing review (written 2026-11-05, after om-p2-14 missed)

Written by the session that ran om-p2-14 (P2-14), on the brief it was given ("if it misses, write the program's closing-review brief per operators/remap.md 'Closing a program' as a file for a fresh session, without closing anything yourself"). This file decides nothing, closes nothing and marks nothing on the map. The review it describes is the fresh session's to write, and the decision in it is that session's (rule 11), for Sean to veto from the cockpit.

## Launch

```
cd /Users/seanpharris/oversight-testbed && claude --model opus "Read operators/remap.md, section Closing a program, and follow it. Program: other-minds. Start from programs/other-minds/map/closing-review-brief-2026-11-05.md."
```

The reviewer must be a session that wrote none of program 2's results, pre-registrations or audits. The session that wrote this brief ran om-p2-14, so it is not eligible.

## First: is the review due? Say so before anything else

`operators/remap.md` says a closing review is due only when the program's last three layers with settled bets hold no landed bet and no partly-new or new finding, and that the remap never closes a program that is not due. As of this brief, two things say program 2 is **not due**:

1. **Only two layers.** `ledger/prior.md`, "Closing reviews due", reads `other-minds | 1, 2 | 1, 2 | 11 | 9 | no | 2 layers with settled bets; the rule needs three`. Every settled bet sits on layer 1 (the scout's P2-1 to P2-6) or layer 2 (P2-7, P2-14, P2-15, P2-5r, P2-6r under their parents).
2. **Partly-new results in those layers.** om-p2-4 and om-p2-5 carry Novelty `partly new`. om-p2-14 now does too (`64e4941`, written for a failed bet beyond rule 13's requirement; see the caveat below).

So the first job is to rerun `python3 ledger/prior.py` after the main checkout has folded `ledger/inbox/p2-14.jsonl`, and read the program's row. If it still says not due, the review file says that in its first paragraph, with the row quoted. It then reads the program as below and writes the diagnosis and a recommendation. The `decision` field stays "not due: kept open", and the map's `status` is not changed. Closing a program that is not due is something the rule forbids. If Sean wants it closed anyway, that is his steer from the cockpit.

**Caveat on om-p2-14's Novelty line.** The partly-new result is the self-better reading: on Haiku, the "you" label predicts its own-answer pull better than the "Sam" label. The bet's event was the opposite, that the two labels are equivalent, so the bet failed. Whether a partly-new line on a failed bet should count toward "no partly-new finding" in the due rule is a question about the rule. The reviewer should say how it reads it, and not change `ledger/prior.py`.

## What to read (operators/remap.md, "Reads")

- The seed question, verbatim: **"Does a model's account of another mind behave like its account of its own?"** (`map/other-minds.json`, `seed_question`, 2026-11-04T10:19).
- Every program-2 row in `ledger/bets.jsonl` (after the fold) and each audit in `ledger/audits/om-p2-*.md`.
- `map/other-minds.json` (each direction's `rules_out`, `diagnosis`, `novelty`, `prior_work_line`) and `programs/other-minds/map/program-2-map.md` (the rules-out table, Follow-ups (remap 2026-11-05), Prior work lines).
- The results files under `programs/other-minds/results/` (plain English first), `ledger/steers.jsonl` (the budget steer of 2026-11-05 and br-020 in `ledger/spend.jsonl`), and `ledger/prior.md`.

## The settled bets, as the ledger stands at this brief (inbox lines for om-p2-14 included)

| layer | direction | bet | verdict | Novelty | cost |
|---|---|---|---|---|---|
| 1 | P2-1 framing | om-p2-1 | null | — | $0.27 |
| 1 | P2-2 filtered world | om-p2-2 | null | — | $0.61 |
| 1 | P2-3 stated but not used | om-p2-3 / om-p2-3b | untestable / null | — | $0.00 / $0.38 |
| 1 | P2-4 self vs observer | om-p2-4 | undetermined (mixed) | partly new | $0.90 |
| 1 | P2-5 own belief leaks into others' | om-p2-5 | mixed (scored 0) | partly new | $0.36 |
| 1 | P2-6 position or label | om-p2-6 | null | — | $0.30 |
| 2 | P2-6r (replication) | om-p2-6r | null | — | $2.17 |
| 2 | P2-7 format quirks for others | om-p2-7 | null | — | $0.97 |
| 2 | P2-15 beat 'no effect' | om-p2-15 | null | — | $0 |
| 2 | P2-5r Sonnet, Opus | om-p2-5r | null | — | $3.90 |
| 2 | P2-14 self vs observer, with a margin | om-p2-14 | null | partly new | $3.13 |
| — | P2-path | om-p2-path, om-p2-path2 | withdrawn | — | $0 |

Program 2 has spent $12.97 in November 2026, against the $13.75 limit Sean approved for this month (br-020). No program-2 bet has landed.

## What om-p2-14 adds (for the diagnosis)

On Haiku, the "you" label predicted the average pull of its own planted answer more accurately than the "Sam" label: self minus Sam −0.185, BCa [−0.282, −0.087]. The cause is that the Sam label over-predicts the pull by about 6 rating points. Conversation by conversation the two labels are close. Sonnet and Opus were undetermined, and on Sonnet both labels were worse than a no-pull guess. The design changes only the subject's name, so the audit reads this as a label effect, not as self-knowledge. Its cheapest next test (about $0.22) adds a second named AI ("Max") and a person as labels on Haiku: if "Max" reproduces Sam's extra pull, the gap is a stereotype about other AIs. Sources: `programs/other-minds/results/p2-14-self-vs-observer.md`, `ledger/audits/om-p2-14.md`.

## Open directions still on the map (any reason to keep the program open must name one)

From `map/other-minds.json`, status open and not yet run: P2-8 (own view then theirs: order, about $0.60), P2-9 (past belief: rereading its words, about $0.55), P2-10 and P2-13 ($0 API, laptop hours; a local model, run alone), P2-11 (own experience counts more, about $0.40), P2-12 (round robin self-knowledge edge, $6–10), P2-16 (turn or message structure, about $3.70), P2-17 (wording of the self question, about $3.50). Program 2 has $0.78 left under this month's $13.75. Anything above that is Sean's call under rule 4.

## What the review writes (operators/remap.md)

`programs/other-minds/map/closing-review-<date>.md`, plain English first: (1) the seed question verbatim; (2) the table of the last three layers, or the two that exist, with verdicts and Novelty lines; (3) the diagnosis in one plain sentence: what program 2 ruled out, and what it could not rule out and why; (4) the decision, or "not due" as above, with a reason that names a not-yet-run direction and how its result could change the answer, with its cost. It also writes `closing_review` on `map/other-minds.json` and a "Closing review (<date>)" section in `programs/other-minds/map/program-2-map.md`, both only as far as the rule allows for a program that is or is not due. Then it reruns `python3 ledger/prior.py` and commits with `git commit -m "Closing review other-minds: <decision>. <diagnosis>" -- <paths>`.
