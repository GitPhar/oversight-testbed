# Site walk, 2026-11-05 (before changes)

Live site at https://gitphar.github.io/oversight-testbed, screenshotted at 1366×900 and 390×844 (phone) with Playwright before any change on branch `site-night`, which was first fast-forwarded to main (`24c3ea2`). Sean's walk of 4 November evening named six fixes; this records what the live site showed for each.

**Legend.** The map's key reads "Bet landed · Running · Mixed or unsettled · Killed · Open not yet bet on". Landed is yellow (`--hit: #f2c14e`), the same gold the site uses for the human's hand, the buttons and the current-page underline. No sentence says what any of the five words means. A stranger has to open "How to read it", and even that does not define mixed.

**Kill log 404.** From the desktop, every page's nav link to `kills.html` returned 200, and a crawl of 48 same-site links found none broken. Two things fail. (1) On a phone the nav is one row that scrolls sideways with its scrollbar hidden. It shows "Home Map Cockpit Calibration Instruments" and cuts off there, so Kill log, Record and Papers cannot be seen. (2) The Kill log page, and the home and instruments pages through it, request `data/ledger/kills.jsonl`, which does not exist. Each load logs a 404 in the browser. The nav links are also relative to the page's URL, so any address with a trailing slash (`…/index.html/`) breaks every link, and GitHub's own 404 page offers no way back.

**Program 4 on the map.** The tabs are Program 1, 2 and 3. Program 4 has a map (`programs/settled-science/map/settled-science.json`, 8 directions), and the ledger has 7 of its bets with 6 passes, but `map/` has no `settled-science.json`, so the site never draws it.

**Cockpit.** At 10,692 px on the desktop and 27,219 px on a phone, it has a "Next to run" strip, a human column listing every bet, a path-dependence counter, and 28 open-question cards. Each card has a heading of up to four lines in research language ("checking whether a qubit's quick repeated measurements 'remember' one another, which one fringe theory of reality predicts…"), two background bullets, a cost pill, an engine-only fold, an odds box with a five-point scale, and reveal, veto and add-question buttons. Then come a separate add-a-question form and a two-file export with shell commands. Nothing says which few questions matter now.

**Home.** It has the description, three panels, the diagram, tiles and the five commitments. Nowhere does it say what the project has found. `paper/plain-words.md` (on main since `24c3ea2`) has the findings, but only on the Papers page.

**Instruments.** The gauges are dense and sourced. Nothing says what changed since yesterday. The day-by-day panel shows "Thu Nov 5 today: placed 0, settled 0, killed 0", but a reader has to work out the rest by comparing gauges with memory.
