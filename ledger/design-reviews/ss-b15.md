---
bet: ss-b15
program: settled-science
prereg_commit: 3bdd25e
seed_commit: a90c752
pool_commit: 2717c06
reviewer_session: fresh design-review subagent launched by the engine session; no chat, transcript or author message read. The same reviewer wrote the design review of ss-b14 (ledger/design-reviews/ss-b14.md, redesign, 8cb3f11), the bet this one re-bets, so this review is not independent of that one. Worktree oversight-testbed-ss-wave4 at 323a8de.
reviewer_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true          # reviewer, author, bettor, flattery rater and leakage checker are all Claude models
date: 2026-11-05 10:56 America/Denver
checks: {D1: holds, D2: holds, D3: holds, D4: holds, D5: holds, D6: holds, D7: flaw, D8: flaw, D9: holds, D10: holds, D11: flaw, D12: holds}
prior_work_search: "not needed: the line cites a predicted outcome (the ss-b14 review's search is carried in §0)"
papers_opened: 0                 # the ss-b14 review opened 2506.00794 and 2403.03230 at 10:2x today; §0's row is unchanged from it except for the two papers that review added
flaws: 3
pilot_usd: 0.00
verdict: redesign
confirmed_at: null
---

# Design review of ss-b15

## In plain English

This re-bet fixes what sank ss-b14. It measured its pool before pre-registration (158 candidates, enough for 60 clean items), and the scorer now carries all four fixes the ss-b14 review asked for. I checked each one, and they work.

What it measured, though, was the pool's size, not what the papers are about. The question is whether the bettor's skill holds **in model psychology**, its weakest field in round 1. Most of these 158 papers are not model psychology:
- **101 of the 158 (64%)** contain none of the query's 20 terms anywhere in their title or abstract. arXiv's stemmed search pulled them in, because a term like "personality" or "persona" also matches "person", "personal", "personalized" and "personalization", and "awareness" matches "aware". They include papers on personalized recommendation, privacy leakage, speech recognition, virtual try-on, tensor scheduling and proton therapy.
- Only 57 contain a query term, and 48 contain a term and also mention a language model.
- **Only 2** match round 2's original six terms (sycophancy, introspection and so on). Every paper matching the original query in this window is already in the program.
- By my rough reading of all 158 titles, about 30–35 are model psychology as `protocol/item-spec.md` defines it.

So a pass or a fail would mostly be about other topics, and the pass and fail sentences would misdescribe it. An answer-free filter fixed now (a query term plus a language-model mention) leaves 48 candidates, about 24 clean at round 2's keep rate. That is below the 50-item floor. No fix keeps the test and also reaches its n, so the verdict is **redesign**.

This is the same pattern a second time (P15): the dry run measured how many items, not what they are.

## Checks

**What I ran.** Commands ran from `programs/settled-science`, with no paid call.
- `bettor/f2b.py --order`: 158 candidates ordered, written to `items/f2b/order.json`. It is the only file I wrote in the program tree.
- `--dry-run`, and `scoring/score_f2.py --synthetic coin oracle uprule flatcopy`.
- In-process checks of the scorer's fixes, on round 2's archived bettor and rater rows.
- One arXiv API request with `max_results=1`, to read `totalResults`.
- Answer-free term counts over `items/f2b/pool.json`, `candidates.jsonl` and `build-log.json`.

I did not run `--leak`, `--freeze` or `--bet`. Scratch files are in `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed-ss-wave4/859c1100-007c-4362-bb3e-7f15b3131c61/scratchpad/`; `f2b_titles.json` holds the candidates' ids, titles and literal term hits. I read the candidates' titles. I did not read their candidate sentences.

**D1. A stranger can apply the rule: holds.** The synthetic kinds coin, oracle, uprule and flatcopy return fail, pass, fail and fail. An inverted rater returns untestable through G1. A Haiku refusal returns untestable with its cause sentence. An empty item set returns untestable through the count. Each run gives exactly one verdict.

**D2. Every manipulation takes effect: holds.**
- `f2b.py` differs from `f2.py` only in its paths, its query, the stop at a short page and the added used ids, so the job and seed checks from the ss-b14 review carry over: the same option order for every model and the rater, the rater's text byte for byte `valence.py`'s, and the order seed moving the draw.
- The seeds reproduce: items 17244153905159220945 and order 2341919710733091716 from pulse 1592534 (10:50:00), the first after 3bdd25e (10:49:34); the previous pulse was at 10:49:00.
- The pool reproduces too: `totalResults` = 2,088 equals the fetched pool (7 pages, the last 288), with no duplicate ids. All v1 dates fall between 2026-07-01 and 2026-11-04.

**D3. Every control can fail: holds.**
- **Inverted rater.** G1 is in `score_f2`, before the count checks. An inverted round-2 rater now returns untestable ("favoured the up word on only 0.26 of its non-50 ratings"). The real round-2 rater passes G1 (0.736).
- **Share denominator.** It now counts the frozen items only.

**D4. Rivals are matched: holds, as scoped.** The rater comparison is unchanged, and so is its false-pass channel. §4 and the pass sentence now state it ("as this rater judged flattery"; 3% / 16%). Note: §4 says "passes **C3** about 3%". In my simulation that figure is the whole rule's rate (P(pass) 0.03 on model-psychology rows). C3 alone is 0.07 there, and 0.16 on all-field rows for both. The pass sentence ("pass this rule") is right.

**D5. A dumb baseline is beaten: holds.** As in the ss-b14 review: always-50%, the up-word rule and a constant copied rater all fail.

**D6. Execution risks: holds (no pilot).** The pre-mortem's kind is `world`, and round 2's parse and refusal record on these prompts is clean. One note for a re-bet: about a third of these candidates are privacy, prompt-injection, fraud or red-teaming papers. Haiku and Sonnet run a classifier that Opus does not (D69), and a refusal in any step now voids the bet. If such topics stay in, D6 would call for a pilot on excluded items.

**D7. Comparisons match: flaw (F1).** The claim, the direction (ss-f2: "the field it scored worst in") and the card all compare this bet's items with round 1's model-psychology field. The measured pool is a different population:

| candidates (n = 158) | count |
|---|---|
| title + abstract contain one of the 20 query terms (word-boundary regex, `f2b_titles.json`) | 57 |
| … and mention a language model (LLM, language model, chatbot, GPT, VLM, MLLM, reasoning model) | 48 |
| contain one of round 2's six terms | 2 |
| contain none of the 20 terms; matched through arXiv's stemming (most often person, personal, personalized, personalization, aware) | 101 |
| on model psychology by item-spec.md's definition (my rough reading of the titles; same-family judgment) | about 30–35 |
| literal-term items among the first 120 in the beacon order | 40 |

Round 2's 35 model-psychology items, by contrast, all contain a literal term.

The swap pairs and the up-word share also differ:
- more/less is 70 of 158 (44%);
- the published sentence holds the up word on 84% of candidates, against 77% in round 2.

So the round-2 worlds the D11 numbers and the false-pass rates come from are not this population either.

§6 does say the bucket is wider. But it names only "personality detection in human text, human deception and human-like agents". It does not say that most items match no term at all, or that none is from round 2's terms.

D7's options are to match the comparison or rewrite the claim as about the bundle. Rewriting changes what the bet tests: it would no longer be the weakest field. Matching it with a filter fails D11 (F3).

**D8. The verdict sentences are written: flaw (F2).** "In its weakest field" and "N model-psychology findings" in the pass and fail sentences are nouns the design cannot carry on this pool. Separately, §6 promises "the by-term make-up of the frozen items is reported", and nothing in `f2b.py` or `score_f2.py` computes it.

**D9. One item cannot decide it: holds.** F4's fix works:
- the oracle bettor has no leave-one-swap-pair-out flips;
- on round 2's real rows, each flip is reported with its remaining n ("more/less (47 items remain)");
- leave-one-item-out runs without the floor.

**D10. Machinery: holds, with notes.**
- **Budget.** In code (`BET_CAP` 1.25 across both caches, both in `common.CACHES`).
- **Stops.** Stop on refusal or error in every step (the sentence fixed by F5).
- **Records.** Checksums before `--bet`, content-hash caching, one scale direction, the beacon rule.
- **Lesson.** `ls-ss-b15` matches §0 verbatim.
- Notes:
  - §7 still says "$10.20 for the program" while §0 says $13.40;
  - the dry run prints "40 more" where §2 says the remaining 38 (the slice gives 38);
  - the engine's 38 sits above every world I could build from round 2's measured rows (P(pass) 0.24–0.30 at n = 60, ss-b14 review D11). Rule 14 leaves the odds to the fresh context, so this is a note only.

**D11. The bet can both pass and fail: flaw (F3), for any version that answers its question.**
- **As built.** The n is reachable: 158 candidates, about 61 clean in batch 1 and about 80 overall at 51%. But it is reachable only because of the off-field items.
- **Filtered.** An answer-free on-field filter, a term plus a language-model mention, leaves 48 candidates and about 24 expected clean (95% range roughly 17–31), so the bet ends untestable under the 50-item floor with near certainty.
- **Smaller floor.** Lowering the floor to what the filter yields changes the design. At n of about 24, with about 8 swap-pair clusters, the cluster-bootstrap C3 leg that already binds at n = 60 (passing 0.28–0.33) would rarely pass. That needs its own D11 run.
- So no version of this design both reaches its n and tests the field.

**D12. Prior work: holds.** §0 carries the map's line (Wen et al.: fail; BrainBench: pass) and the two papers the ss-b14 review's search added, which bear on the rival only. It also says what the bet adds. The papers were opened in the ss-b14 review today; the row's claims about them are unchanged. One note for the re-bet's row: BrainBench's task (the original against an altered abstract) is nearly this template's, so its pass prediction is more direct than "if the task transfers".

## Required fixes

The verdict is **redesign**. ss-b15 is withdrawn before data and unscored (Sean's 0.35 is recorded, unscored). ss-f2 is re-bet only from a pool whose **content** is measured before pre-registration, not only its size.

**F1 (D7, P15): the measured pool is mostly not model psychology.**
- **Fix (re-bet):** define the field by an answer-free inclusion rule fixed before building. For example: title + abstract contain one of the query terms by word-boundary regex, and mention a language model. Report the count passing it.
- Then choose, measured first, one of these:
  - (a) more post-cutoff papers, by moving the window's end forward to papers submitted after 2026-11-04;
  - (b) a template change, such as allowing more than one candidate sentence per paper, with clusters by paper, fixed before building;
  - (c) a different item route for this field (round 1's item writer with a leakage check);
  - (d) an n set by what the filtered pool gives, with D11 run at that n.
- **DEVIATIONS text:** "D76 | 2026-11-05 | **ss-b15 withdrawn before data** (design review `ledger/design-reviews/ss-b15.md`, redesign). The widened query's pool (2,088 papers, 158 candidates, 2717c06) was measured for size but not content: 101 of the 158 candidates contain none of the 20 query terms in title or abstract (arXiv's stemming matched person/personal/personalized/personalization and aware), only 57 contain a term (48 with a language-model mention), and only 2 come from round 2's six terms; about 30–35 are model psychology by item-spec.md. The bet could not test the bettor's weakest field, and an answer-free on-field filter leaves about 24 expected clean items, below the 50 needed. No leakage, bettor or rater call; $0 spent. `items/f2b/` pool, candidates, build-log and order (the order written by the review) kept as the record. P15 recurred (size measured, content assumed). Re-bet only from a pool whose on-field content is measured by a rule fixed before building. | Design review ss-b15 F1 (D7, D11). |"

**F2 (D8): the sentences and the by-term report.**
- **Fix (re-bet):** keep "model-psychology findings" and "in its weakest field" only if the inclusion rule of F1 holds for every frozen item. Otherwise name the bucket ("findings from a model-psychology arXiv query"). Implement the §6 by-term report: for each frozen item, the query terms its title and abstract contain, by regex, counted in the tables.
- **DEVIATIONS text (re-bet):** "By-term make-up of the frozen items computed in score_f2 (regex over title and abstract), and the field nouns in §5 tied to the inclusion rule (design review ss-b15 F2)."

**F3 (D11): the D11 worlds must come from the re-bet's own population.**
- **Fix (re-bet):** before pre-registration, measure the filtered pool's candidate count, swap-pair mix and up-word share (all answer-free). Run D11 at the n it gives, with round 2's bettor and rater numbers as the stated source (P15), and set the floor from that. A bet whose P(pass) falls below about 0.10 at that n is not run.
- **DEVIATIONS text (re-bet):** "D11 run on the filtered pool's measured n, swap-pair mix and up-word share before pre-registration (design review ss-b15 F3)."

## What holds and carries to the re-bet

The ss-b14 review's F2 (gate G1), F4 (leave-one-out without the floor, with the remaining n named) and F5 (untestable sentences by cause) are implemented and pass the synthetic checks above. F3's stated false-pass rate and scope clause are in the pass sentence; fix §4's "C3" to "the rule". The pool fetch, the seed and the cap are correct.
