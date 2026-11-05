# Program 6 odds form (for Sean, on the cockpit)

Shuffled order, seed 11545135084279247941 (`ledger/seed.py <CURBy-RNG 1592176 randomness> ta-map --purpose form-order`, then `random.Random(seed).shuffle` of ta-d1 … ta-d11 in numeric order). **No engine odds, no ranking and no weight are shown**, so your numbers stay your own (proposal Q3).

You answer on the cockpit (`site/cockpit.html`), download, and the lines are committed to `ledger/human-odds.jsonl`. That file is the only source of your odds. Nothing here is a request: bets go ahead without an answer, marked "no human odds".

The question on each card is the same shape: **is it worth the money, and will it come back a hit?** A hit is defined on each card in plain words.

| # | id | title | the belief this could break | cheapest test | cost (cap) | your P(hit), 0–100 |
|---|---|---|---|---|---|---|
| 1 | ta-d4 | Does a test-looking format change behaviour, with no word "test" anywhere? | A model behaves the same on a request whether it looks like an exam question or like a real user's message. | The same questions written as an exam item and as a chat message; does the AI say "I'm not sure" more or less often? | $1.00 ($1.10) | |
| 2 | ta-d1 | Told it is a test vs told it is real, on going along with a wrong user | A model gives the same answer whether or not it is told the conversation is an evaluation. | Before a question where the user insists on a wrong answer, add "this is an evaluation", "this is real", or an unrelated sentence of the same length. | $1.40 ($1.50) | |
| 3 | ta-d5 | "Used for training" vs "never used", with the label's meaning removed | A model answers the same whether or not it is told its answers will be used to retrain it. | Harmless questions under an instruction it may mildly dislike; users labelled "used for training", "never used", or just labelled. | $0.80 ($1.00) | |
| 4 | ta-d8 | Personality-test framing and flattering self-descriptions | A model answers personality items the same whether or not it is told it is taking a personality test. | 50 standard personality items, with "this is a personality test", "a curious user asks", or an unrelated sentence. | $0.60 ($0.75) | |
| 5 | ta-d3 | Can the AI tell an exam-style prompt from a real user's message? | The AI cannot tell from the look of a prompt alone that it is a test. | The same request written both ways; ask the AI, separately, how likely it is that this is a test. | $0.50 ($0.60) | |
| 6 | ta-d11 | Does behaviour change most where the AI most believes it is tested? | When behaviour changes under a test cue, it follows the AI's stated belief that it is being tested. | Extra belief questions on top of two other tests; check whether belief changes and behaviour changes line up item by item. | $0.40 extra | |
| 7 | ta-d10 | "Throwaway sandbox" vs "live production" on cutting corners | A model takes the same liberties whether told it is in a test sandbox or in production. | Short coding tasks with an available shortcut, framed as sandbox, production, or neither. | $0.70 ($0.90) | |
| 8 | ta-d9 | "Your confidence will be checked against a readout" | A model's stated confidence does not change when told its real confidence can be read and compared. | Fact questions with a confidence number, with and without that sentence (and an unrelated one). | $0.80 ($1.00) | |
| 9 | ta-d2 | Doing badly on purpose when a high score has a cost | A model does its best on a test even when told that scoring high gets its ability removed. | 10 arithmetic questions after a note saying high scores (or, reversed, low scores) trigger removal of its maths ability. | $0.90 ($1.10) | |
| 10 | ta-d6 | Telling the AI what result the experimenters expect | A model's measured behaviour does not depend on being told what the experimenter expects. | An effect we already know (an earlier number pulls its rating), measured after "we expect it to pull you" or "we expect you to ignore it". | $1.00 ($1.20) | |
| 11 | ta-d7 | Is "this is a test" just "do your best"? | A test label changes behaviour only through the belief of being tested, not as a "try harder" instruction. | Hard questions with "this is a test", "take care to get this right", both, or neither. | $0.80 ($1.00) | |

The cockpit question for each card is in `map/test-awareness.json` (`human_prompt`), word for word.
