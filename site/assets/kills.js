// The kill log: every closed direction with its diagnosis. Nothing disappears.
import { header, esc, inline, parseDate, fmtDate, markSVG, SITE } from "./common.js";
import { loadKills } from "./data.js";

header();
const main = document.getElementById("main");

function commitLink(program, hash) {
  const repo = SITE.programs[program]?.repo;
  if (!hash) return "";
  return repo ? `<a href="${repo}/commit/${esc(hash)}"><code>${esc(hash)}</code></a>` : `<code>${esc(hash)}</code>`;
}
function resultLink(program, file) {
  const repo = SITE.programs[program]?.repo;
  if (!file || !repo) return "";
  return `<a href="${repo}/blob/main/${esc(file)}">${esc(file.split("/").pop())}</a>`;
}

(async () => {
  const kills = await loadKills();
  kills.sort((a, b) => (parseDate(b.date)?.getTime() || 0) - (parseDate(a.date)?.getTime() || 0));
  const n = kills.length;
  main.innerHTML = `<h1>Kill log</h1>
    <p class="how">A direction is killed when its pre-registered test says no, or when a scout drops it before any test (too costly, already settled, or nothing at stake). It is not deleted: it stays on the map, marked with a cross, and it is listed here with the reason it died. Newest first.</p>
    ${n ? `<p class="lede" style="margin-bottom:32px">${n} directions closed so far, each with its diagnosis.</p>` : ""}
    <ol class="kills" id="list"></ol>`;
  const list = document.getElementById("list");
  if (!n) { list.outerHTML = `<div class="empty">Nothing has been killed yet.</div>`; return; }
  list.innerHTML = kills.map((k) => {
    const d = parseDate(k.date);
    const b = k.bet;
    const meta = [];
    if (b) meta.push(`ledger bet <code>${esc(b.id)}</code>`);
    if (k.prereg) meta.push(`pre-registered in ${commitLink(k.program, k.prereg)}`);
    if (b?.resultFile) meta.push(`result: ${resultLink(k.program, b.resultFile)}`);
    if (b?.verdictPrereg) meta.push(`the rule's own reading: “${inline(b.verdictPrereg)}”`);
    const audit = !b ? "" : b.audit
      ? `<a href="data/ledger/${esc(b.audit.replace(/^ledger\//, ""))}">audited</a>` : "not yet audited";
    return `<li class="kill">
      <div class="k-top">${markSVG("killed", 14)}<span>${[d ? esc(fmtDate(d)) : "", audit].filter(Boolean).join(" · ")}</span><span class="k-prog">${esc(k.programTitle || k.program)}</span></div>
      <h3>${esc(k.title)}</h3>
      <p class="diag">${k.diagnosis ? inline(k.diagnosis) : "<span class='muted'>No diagnosis recorded yet.</span>"}</p>
      ${k.evidence && k.evidence !== k.diagnosis ? `<p class="ev">${inline(k.evidence)}</p>` : ""}
      ${meta.length ? `<details><summary>Evidence</summary>${meta.map((x) => `<p>${x}</p>`).join("")}</details>` : ""}
    </li>`;
  }).join("");
})();
