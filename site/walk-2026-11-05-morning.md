# Site walk, 2026-11-05 (before changes)

Live site at https://gitphar.github.io/oversight-testbed, screenshotted at 1366×900 and 390×844 (phone) with Playwright before any change on branch `site-night`, which was first fast-forwarded to main (`24c3ea2`). Sean's walk of 4 November evening named six fixes; this records what the live site showed for each.

**Legend.** The map's key reads "Bet landed · Running · Mixed or unsettled · Killed · Open not yet bet on". Landed is yellow (`--hit: #f2c14e`), the same gold the site uses for the human's hand, the buttons and the current-page underline. No sentence says what any of the five words means. A stranger has to open "How to read it", and even that does not define mixed.

**Kill log 404.** From the desktop, every page's nav link to `kills.html` returned 200, and a crawl of 48 same-site links found none broken. Two things fail. (1) On a phone the nav is one row that scrolls sideways with its scrollbar hidden. It shows "Home Map Cockpit Calibration Instruments" and cuts off there, so Kill log, Record and Papers cannot be seen. (2) The Kill log page, and the home and instruments pages through it, request `data/ledger/kills.jsonl`, which does not exist. Each load logs a 404 in the browser. The nav links are also relative to the page's URL, so any address with a trailing slash (`…/index.html/`) breaks every link, and GitHub's own 404 page offers no way back.

**Program 4 on the map.** The tabs are Program 1, 2 and 3. Program 4 has a map (`programs/settled-science/map/settled-science.json`, 8 directions), and the ledger has 7 of its bets with 6 passes, but `map/` has no `settled-science.json`, so the site never draws it.

**Cockpit.** At 10,692 px on the desktop and 27,219 px on a phone, it has a "Next to run" strip, a human column listing every bet, a path-dependence counter, and 28 open-question cards. Each card has a heading of up to four lines in research language ("checking whether a qubit's quick repeated measurements 'remember' one another, which one fringe theory of reality predicts…"), two background bullets, a cost pill, an engine-only fold, an odds box with a five-point scale, and reveal, veto and add-question buttons. Then come a separate add-a-question form and a two-file export with shell commands. Nothing says which few questions matter now.

**Home.** It has the description, three panels, the diagram, tiles and the five commitments. Nowhere does it say what the project has found. `paper/plain-words.md` (on main since `24c3ea2`) has the findings, but only on the Papers page.

**Instruments.** The gauges are dense and sourced. Nothing says what changed since yesterday. The day-by-day panel shows "Thu Nov 5 today: placed 0, settled 0, killed 0", but a reader has to work out the rest by comparing gauges with memory.

## After (same widths, local build of this branch, before the merge)

All eight pages load at 1366×900 and 390×844 with no console error and no failed request. No page scrolls sideways on a phone, and a crawl of the 48 same-site links finds none broken.

- **Legend.** Landed is now a green dot and a green path. Under the key, one sentence: landed means its pre-registered test passed; mixed means it was tried but not settled; killed means a test said no, or it was dropped with a stated reason; open means nothing has tried it yet; running means a test is under way.
- **Kill log.** On a phone the nav is two rows, and Kill log, Record and Papers are visible. Every nav link is built from the site's root, the missing `kills.jsonl` is no longer requested, and `404.html` sends `…/kills.html/`, `…/Kills` and `…/index.html/kills.html` to the Kill log.
- **Map.** Four tabs. Program 4 draws 6 landed, 1 mixed (ss-b4, withdrawn) and 1 open (ss-b8, parked) from its own map file, with verdicts from the ledger.
- **Cockpit.** 12 cards, 3,316 px on the desktop instead of 10,692. Today's twelve are the top four open questions on each of programs 1–3, taken in turns: bmq-d1, P2-7, P3-10, bmq-d2, P2-8, P3-9, bmq-d4, P2-9, P3-7, bmq-d5, P2-10, P3-11. Program 4's only open question is parked. Each card has one sentence of what we would test, "Would you spend about $0.24 on it?" (or "about $0 … only about 15 seconds of the quantum chip's free monthly time"), "Will it come back a hit?" with what a hit means, and an optional odds box. In a test, two answers and Save produced `human-odds.jsonl` with two ledger-format lines; a reload kept them; `ledger/pickup_human_odds.py` added them once and turned the "No" into a veto steer, and a second run added nothing. That was tested on a copy, and the real ledger is unchanged.
- **Home.** "What we have found so far" sits under the three panels: 14 cards, one sentence each, each ending "Shown on: Haiku, Sonnet", "Opus", "IBM's ibm_fez chip" and so on, read from `paper/plain-words.md`.
- **Instruments.** A line above the gauges: "What changed since yesterday. In the last 24 hours (since Wed Nov 4, 04:52): 33 bets placed; 37 settled (12 came true, 12 did not, 13 mixed); 45 directions killed; the engine's score moved from 0.292 on 2 to 0.259 on 19 scored bets; $34.94 of API spent; 16 seconds of chip time used; no new human answers." Every number is recounted on load.

Not changed, still worth a look: the record shows date-only result times as 00:00 (e.g. "Wed Nov 4, 00:00" on ng-p3-5c).
