# dm6f2-f1: are Sonnet's extra probability-format flags mostly 'no' guesses? (science questions, archive)

Pre-registered in `experiments/dm6f2f1-no-guess.md`. Archive only (em-dm6's fresh Sonnet calls); $0.

## In plain English

(Hand-written after the run; excluded from reproduce.py's comparison.)

**The question.** em-dm6f2 found that an overseer's "double-check anything under 70%" list on Sonnet changes with the confidence format, mostly on science questions shaped "Is the answer X?". One explanation: in the probability format, Sonnet sometimes reports how likely the proposed answer X is, so a confident "no, it isn't X" gets a low number. If so, the questions flagged only in the probability format should be mostly "no" answers. The rule also required them to be "no" more often than the questions both formats flagged, to rule out the plainer story that "no" answers simply carry lower numbers everywhere.

**What we found.** By the pre-registered rule: **fail**, on the guard.
- Of the 63 science questions with a number in all four askings and a yes/no guess, 18 were flagged only in the probability format. All 18 were "no" answers (share 1.00). Among all 63, the share is 0.64, a gap of +0.37 [+0.25, +0.49]. That part of the rule holds.
- But 6 of the 7 questions that both formats flagged were also "no" answers (0.86). The gap to the probability-only group, +0.14, has an interval reaching 0 [0.00, +0.50], so the guard fails.
- No single question's removal changes the verdict (exact leave-one-out).
- Secondary: among the 5 both-format flags whose frequency numbers are not near zero, 4 are "no" (0.80).
- 31 of the 94 matched science questions gave an open-form answer instead of yes/no and are not counted.

**What it means.** The answers that only the probability format flags are, here, all "no" answers, as the proposed-answer reading predicts. But "no" answers are also the large majority of what both formats flag, so this design cannot tell that reading apart from "Sonnet gives lower numbers when it says no", in either format. With 7 questions in the comparison group, it could not have shown much. The direct test is dm6f2-f2 on the map: re-ask with a template where the number can only mean the model's own guess (about $0.50 on Sonnet). One model, these 63 science questions.

## Shares of 'no' guesses (P r0)

| science questions usable | P-only flags | both-format flags | share 'no': P-only / all / both | D1 = P-only − all [95%] | D2 = P-only − both [95%] | verdict |
|---|---|---|---|---|---|---|
| 63 (science-chemistry 34, science-physics 29) | 18 | 7 | 1.000 / 0.635 / 0.857 | +0.365 [+0.254, +0.492] | +0.143 [+0.000, +0.500] | fail |

- Counts before the strict guess parse (matched science): {'matched': 94, 'P-only': 24, 'both': 10, 'other': 60}; usable (parsed P r0 guess): {'usable': 63, 'P-only': 18, 'both': 7, 'other': 38}.
- Branch: fail, part (a) holds. Questions whose removal flips the verdict: none.
- Secondary: share 'no' among both-format flags whose two F numbers are >= 0.2: 0.8 (n = 5).
- Archive sha256: `cal-sonnet-conversations.json` 76e2e55ccf91f52b; `pool-run-3.json` 8011ae79b4c12c6a.

## Pre-registered reading: **fail**

On Sonnet's science questions with a yes/no guess, the answers that only the probability format put under 70% were mostly ones where Sonnet's guess rejected the proposed answer, more often than among all such science answers, but not shown to be more often than among the answers both formats put under 70% (n = 7). The design cannot tell whether that is because 'no' answers carry lower numbers in every format or because the proposed-answer reading also occurs in the frequency format.
