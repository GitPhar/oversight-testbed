import { DATA, header, getText, getJSON, esc, inline, manifest } from "./common.js";
import { loadBets, loadMaps, loadKills, joinBets, loadHumanOdds, joinHumanOdds, nextToAsk } from "./data.js";
import { listFromManifest } from "./papers-common.js";

header();

// The sentence and the commitments are read from the engine's own README and proposal when the deploy copied them,
// so the front page cannot drift from the repository. The HTML holds the same text as a fallback.
(async () => {
  const [readme, proposal] = await Promise.all([getText(DATA + "engine/README.md"), getText(DATA + "engine/proposal.md")]);
  if (proposal) {
    const m = proposal.match(/##\s*One sentence\s*\n+([^\n]+)/i);
    if (m) document.getElementById("sentence").textContent = m[1].trim();
  }
  if (readme) {
    const sec = readme.split(/\n##\s+/).find((s) => /^the five commitments/i.test(s));
    if (sec) {
      const items = [...sec.matchAll(/^\d+\.\s+\*\*(.+?)\*\*\s*(.*)$/gm)];
      if (items.length) {
        document.getElementById("commitments").innerHTML = items
          .map(([, head, body]) => `<li><strong>${esc(head)}</strong><span>${inline(body)}</span></li>`).join("");
      }
    }
  }
})();

(async () => {
  const [bets, maps, kills, m, odds] = await Promise.all([loadBets(), loadMaps(), loadKills(), manifest(), loadHumanOdds()]);
  joinHumanOdds(joinBets(maps, bets), odds);
  const dirs = maps.flatMap((p) => p.directions);
  const set = (id, t) => { if (t) document.getElementById(id).textContent = t; };
  const plural = (n, w) => `${n} ${w}${n === 1 ? "" : "s"}`;
  if (dirs.length) {
    const open = dirs.filter((d) => (d.status === "open" || d.status === "running") && !d.raw.moved_to).length;
    set("n-map", `${plural(maps.length, "program")} · ${plural(dirs.length, "path")} · ${open} still open`);
  }
  // The cockpit's own rule (data.js nextToAsk): open directions with no bet, not yet answered in the ledger.
  const answered = new Set(odds.map((e) => `${e.program}|${e.direction}`));
  const ask = nextToAsk(maps, answered, Infinity).length;
  if (ask) set("n-cock", `${plural(ask, "question")} not yet answered · the cockpit shows the next ${Math.min(12, ask)}`);
  // Chip seconds: the per-job usage log (the same file the instruments page adds up); the hard stop from program 3's map.
  const q = maps.map((p) => p.raw?.qpu).find(Boolean);
  const jobs = await getJSON(DATA + "programs/entangled-mind/results/ibm-usage.json");
  const used = Array.isArray(jobs) ? jobs.reduce((a, j) => a + (Number(j.quantum_seconds) || 0), 0) : q?.used_s;
  if (used != null && q?.hard_stop_s != null) {
    set("qpu", `Chip time used so far: ${used} of ${q.hard_stop_s} seconds allowed for the whole project.`);
  }
  const withOdds = bets.filter((b) => b.engine != null);
  if (bets.length) set("n-cal", `${plural(bets.length, "bet")} in the ledger · ${withOdds.length} with odds stated`);
  if (kills.length) set("n-kill", `${plural(kills.length, "direction")} closed with a diagnosis`);
  const papers = m.papers ? listFromManifest(m).filter((it) => !it.href).length : 0;
  if (papers) set("n-pap", `${plural(papers, "document")}`);
})();

// What we have found so far: one sentence per finding, with the models it was shown on, read from the
// "What we have found so far" section of paper/plain-words.md. A ledger number in that file is a placeholder,
// <!--n:key-->value<!--/n-->; its value here is taken from data/numbers.json (site/numbers.py, run by the deploy on
// this deploy's ledger), never from the value last written into the file, so the list cannot show a stale score.
// If the section is missing, the block stays hidden.
const fillNumbers = (md, nums) => md.replace(/<!--n:([a-z0-9_]+)-->([\s\S]*?)<!--\/n-->/g, (m, k, old) => (nums && k in nums ? String(nums[k]) : old));
(async () => {
  const [md, nums] = await Promise.all([getText(DATA + "engine/paper/plain-words.md"), getJSON(DATA + "numbers.json")]);
  if (nums) {
    let all = true;
    document.querySelectorAll("#score [data-n]").forEach((e) => { const v = nums[e.dataset.n]; if (v == null) all = false; else e.textContent = String(v); });
    if (all) { document.getElementById("score").hidden = false; document.getElementById("score-src").hidden = false; }
  }
  const sec = md && md.split(/\n##\s+/).find((x) => /^what we have found so far/i.test(x));
  if (!sec) return;
  const items = [...fillNumbers(sec, nums).matchAll(/^-\s+(.+?)\s*\(Shown on:\s*(.+?)\)\s*$/gm)];
  if (!items.length) return;
  document.getElementById("findings").innerHTML = items.map(([, said, on]) =>
    `<li><span class="f-said">${inline(said)}</span><span class="f-on">Shown on: ${esc(on)}</span></li>`).join("");
  document.getElementById("found").hidden = false;
})();
