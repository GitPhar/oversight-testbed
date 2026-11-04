import { DATA, header, getText, esc, inline, manifest } from "./common.js";
import { loadBets, loadMaps, loadKills, joinBets, loadHumanOdds, joinHumanOdds } from "./data.js";
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
  const waiting = dirs.filter((d) => (d.status === "open" || d.status === "running") && !d.raw.moved_to);
  if (waiting.length) {
    const need = waiting.filter((d) => d.human == null).length;
    set("n-cock", `${plural(waiting.length, "open question")} · ${need} waiting for the human's odds`);
  }
  // the chip's budget, from the program that uses it as referee
  const q = maps.map((p) => p.raw?.qpu).find(Boolean);
  if (q && q.used_s != null && q.hard_stop_s != null) {
    set("qpu", `Chip time used so far: ${q.used_s} of ${q.hard_stop_s} seconds allowed for the whole project.`);
  }
  const withOdds = bets.filter((b) => b.engine != null);
  if (bets.length) set("n-cal", `${plural(bets.length, "bet")} in the ledger · ${withOdds.length} with odds stated`);
  if (kills.length) set("n-kill", `${plural(kills.length, "direction")} closed with a diagnosis`);
  const papers = m.papers ? listFromManifest(m).filter((it) => !it.href).length : 0;
  if (papers) set("n-pap", `${plural(papers, "document")}`);
})();
