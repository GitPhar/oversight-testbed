# Your odds, before the data: Sean's biomimicry queue (`bmq`)

Made by the scout session on branch `scout-bmq`, 2026-11-04, from `programs/entangled-mind/paper/biomimicry-queue-map.md`. The questions are in a shuffled order: seed `6ee4bca4` (first 8 hex of sha256("bmq-scout-2026-11-04")), `random.Random(int(seed, 16) + 1).shuffle`. **No engine numbers and no ranking are shown here.**

**You are never asked these in a terminal.** Each question is on its direction's card in the cockpit (`site/cockpit.html`). Answer there if you want to, download, and the lines are committed to `ledger/human-odds.jsonl`. A direction with no line when its bet is pre-registered goes ahead, marked "no human odds". Skip any you have no feel for: a blank is recorded as "no odds", not as 50.

A guide, if it helps: 5 = I'd be amazed. 25 = I doubt it. 50 = coin flip. 75 = I expect it. 95 = I'd be amazed if not.

---

**Q1 (bmq-d2).** Is it worth most of a day of laptop time (free) to find out whether a model that has its conversations trained into its memory keeps what was said but loses track of who said it, itself or the user? Will it come back a hit (here, a hit means it loses who-said-it faster than what-was-said)?

- What it tests: Weight-based memory for LLM agents (consolidating conversations into LoRA weights) keeps the model's record of which content was its own commitment and which came from the user.
- The cheapest test: Llama-3-8B-4bit: word-pair transcripts, half model-generated, half user-given; gate on in-context source d'; LoRA SFT on the full transcripts; then, without the transcript, source d' and content recognition d'.
- Cost: $0 API; laptop ~6-10 h

Your odds (0–100): ____ Why (one line): ____

---

**Q2 (bmq-d1).** Is it worth a few hours of laptop time (free) to find out whether, when training makes a model forget its true-or-false answers, the knowledge is still readable inside it? Will it come back a hit (here, a hit means the knowledge is still readable inside even though the model's answers have gone wrong)?

- What it tests: When fine-tuning makes a model forget, the knowledge is erased: what the model says is what it has.
- The cheapest test: Random-label LoRA (adapter unmerged) on 600 Marks & Tegmark statements; on 600 held-out statements read the frozen pre-fine-tune probe and the verbal answer.
- Cost: $0 API; laptop ~4-6 h (MLX LoRA on Llama-3-8B-4bit)

Your odds (0–100): ____ Why (one line): ____

---

**Q3 (bmq-d5).** Is it worth a couple of hours of laptop time (free) to find out whether telling the model 'those questions are finished, here is a new one' stops the earlier questions from moving its answer? Will it come back a hit (here, a hit means it cuts the effect of question order at least in half)?

- What it tests: The question-order effect is a judgment built from the whole question history, not interference from earlier items that an event boundary could clear.
- The cheapest test: Llama-3-8B-4bit, 40 experiment-5 items, chains O1-O4, one scale, 10 repeats, with vs without a mock closed QA turn before the main question.
- Cost: $0 API; laptop ~2-3 h

Your odds (0–100): ____ Why (one line): ____

---

**Q4 (bmq-d3).** Is it worth most of a day of laptop time (free) to find out whether training a model's own answer into its memory stops the order of earlier questions from moving that answer? Will it come back a hit (here, a hit means order moves the trained answers at most half as much as before, and less than the untrained ones)?

- What it tests: Question-order effects in LLM ratings are built at ask time from context; anchoring the judgment in the weights makes it resistant.
- The cheapest test: Llama-3-8B, 40 experiment-5 items: reverse-KL self-distillation of the bare-question rating on 20 random items; re-measure chain-order spans on trained vs held-out items.
- Cost: $0 API; laptop ~6 h

Your odds (0–100): ____ Why (one line): ____

---

**Q5 (bmq-d4).** Is it worth a few hours of laptop time (free) to find out whether drilling a model on some facts makes it forget related facts it wasn't drilled on, the way it happens to people? Will it come back a hit (here, a hit means the related, undrilled facts are recalled clearly worse)?

- What it tests: In gradient-trained networks, practising some items of a category helps or is neutral for the rest; the human 'remembering causes forgetting' effect is not a property of weights.
- The cheapest test: LoRA stage 1 teaches 8 fictional categories x 6 exemplars to >= 80% cued recall; stage 2 retrieval practice on 3 exemplars in 4 categories; then cued recall of all, unpractised items of practised categories first. Size categories from a pilot.
- Cost: $0 API; laptop ~4-6 h

Your odds (0–100): ____ Why (one line): ____

---

## What you knew when you answered

- [ ] I had **not** seen the engine's odds for these directions.
- [ ] I had seen the engine's odds for some or all of them. Which: ________
- [ ] I had read the map entries.
- [ ] I had seen pilot data or a related result. Which: ________

## Optional, one line each

- **Which direction would you cut first, and why?** ______________
- **Is there a direction you'd add?** ______________
- **For any question: "If it fails, the most likely reason is …"** ______________

## Engine-only sub-bets (scored with engine odds only)

| parent | sub-bet | marked |
|---|---|---|
| bmq-d1 | a probe retrained after the fine-tune reaches AUROC >= 0.85 | engine-only, correlated |
| bmq-d1 | fusing the adapter into the 4-bit base restores verbal accuracy by >= 10 points | engine-only, correlated |
| bmq-d1 | asking in French restores verbal accuracy by >= 10 points | engine-only, correlated |
| bmq-d2 | the in-context gate (source d' >= 1.0) passes on Llama-3-8B | engine-only, correlated |
| bmq-d3 | the gate (>= 8 items per half with an order effect) passes on Llama-3-8B | engine-only, correlated |
| bmq-d4 | the in-context version replicates on Llama-3-8B (>= 5 pp) | engine-only, correlated |
| bmq-d1, bmq-d4, bmq-d5 | the paraphrase and negation re-elicitations (seed `6ee4bca4`) | engine-only |

---

**Recorded:** ________ (America/Denver) · **Commit:** ________
