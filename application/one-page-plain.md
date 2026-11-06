# One page, plain words

Sean Pharris · 2026-11-04, numbers brought current 2026-11-05 · long version: `paper/plain-words.md`.

**What it is.** An AI (Claude) runs small research projects and writes down its odds before each test. A separate Claude session tries to break every result, and a public record scores the odds against what happened. Sean steers. Can either be trusted to choose research?

**What the programs found.**
- *Can quantum maths tell when a model is wrong?* No: a tie with ordinary maths on two Claude models, Haiku and Sonnet.
- *Does a model hold a fixed belief its confidence reports?* On Haiku, mostly not: question order moves its rating by about 25 points out of 100. Hide its earlier answer and it repeats it far less, on all three models. On Opus, six ways of asking largely agree, so the "no fixed belief" part does not carry over.
- *Does a model reason about other minds like its own?* No test passed (six on Haiku; one repeat on Sonnet and Opus also failed).
- *Can a quantum chip grade the odds?* A 3 November surprise never came back in four tries and is not explained; four scored tests, all fails.
- *Can Claude tell which way new published findings came out?* Yes, 76% right, in five passes (a sixth was reversed to undecided). Not yet repeated; the questions were written by the same model family, and a "which version flatters the paper?" shortcut comes close on harder items.
- Three more programs opened on 5 November: does a model grade its own work kindly (first test: no, on three models); does it act differently when it thinks it is tested; does its stated confidence predict what it does.

**The AI's score.** <!--n:brier-->0.170<!--/n--> on <!--n:scored-->48<!--/n--> tests counted one per run (<!--n:brier_all-->0.189<!--/n--> on <!--n:scored_all-->54<!--/n--> counting every scored row), where a coin scores <!--n:coin-->0.250<!--/n--> and guessing the pass rate scores <!--n:hit_rate_ref-->0.188<!--/n-->. Too few tests to say its odds separate passes from misses, and they shift when reworded.

**The checks.** Every number held up, but 38 of 39 early write-ups overstated. Across the record <!--n:audited-->62<!--/n--> of <!--n:bets_total-->90<!--/n--> bets are checked and <!--n:reversals-->4<!--/n--> verdicts were reversed. The checks caught real set-up errors and caught <!--n:plants_caught-->25<!--/n--> of <!--n:plants_planted-->25<!--/n--> mistakes planted to test them. Every checker so far is a Claude model.

**Strong:** rules written before data, plain failures, cheap (about $<!--n:api_usd-->108<!--/n--> of API and <!--n:chip_s-->117<!--/n--> chip seconds), fully rebuildable.
**Weak:** too few tests to judge anything, human odds on only <!--n:human_n-->14<!--/n--> scored bets, and nearly everything done by Claude.

**Before 22 November:** Sean's odds on 20 bets entered before each is registered, more scored tests and planted mistakes, one non-Claude check, the essay and the walkthrough.
