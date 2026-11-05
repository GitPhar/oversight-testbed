// The kill log: every closed direction with its diagnosis. Nothing disappears.
import { header, esc, inline, parseDate, fmtDate, markSVG, SITE } from "./common.js";
import { loadKills } from "./data.js";

header();
const main = document.getElementById("main");

function commitLink(program, hash) {
  const p = SITE.programs[program];
  if (!hash) return "";
  return p ? `<a href="${p.commit}${esc(hash)}"><code>${esc(hash)}</code></a>` : `<code>${esc(hash)}</code>`;
}
function resultLink(program, file) {
  const p = SITE.programs[program];
  if (!file || !p) return "";
  return `<a href="${p.blob}${esc(file)}">${esc(file.split("/").pop())}</a>`;
}

(async () => {
  const kills = await loadKills();
  kills.sort((a, b) => (parseDate(b.date)?.getTime() || 0) - (parseDate(a.date)?.getTime() || 0));
  const n = kills.length;
  const hasDiag = (k) => String(k.diagnosis || "").trim().length > 0;
  const diagN = kills.filter(hasDiag).length;
  const dayOf = (k) => { const d = parseDate(k.date); return d ? `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}` : ""; };
  const latest = dayOf(kills[0] || {});
  const latestN = kills.filter((k) => dayOf(k) === latest).length;
  const latestDiag = kills.filter((k) => dayOf(k) === latest && hasDiag(k)).length;
  main.innerHTML = `<h1>Kill log</h1>
    <p class="how">A direction is killed when its pre-registered test says no, or when a scout drops it before any test (too costly, already settled, or nothing at stake). It is not deleted: it stays on the map, marked with a cross, and it is listed here with the reason it died. Newest first.</p>
    ${n ? `<p class="lede" style="margin-bottom:32px">${n} directions closed so far; ${diagN === n ? "every one" : diagN} with a diagnosis${diagN === n ? "" : `, ${n - diagN} still without one`}.${latest ? ` ${latestN} closed on ${esc(fmtDate(parseDate(latest), false))}, the latest day${latestDiag === latestN ? ", all with a diagnosis" : `, ${latestDiag} with a diagnosis`}.` : ""}</p>` : ""}
    <ol class="kills" id="list"></ol>`;
  const list = document.getElementById("list");
  if (!n) { list.outerHTML = `<div class="empty">Nothing has been killed yet.</div>`; return; }
  let curDay = null;
  list.innerHTML = kills.map((k) => {
    const day = dayOf(k);
    const head = day !== curDay ? (() => { curDay = day; const m = kills.filter((x) => dayOf(x) === day).length;
      return `<li class="k-day"><h2>${day ? esc(fmtDate(parseDate(day), false)) : "Undated"}</h2><span class="muted">${m} closed</span></li>`; })() : "";
    const d = parseDate(k.date);
    const b = k.bet;
    const meta = [];
    if (b) meta.push(`ledger bet <code>${esc(b.id)}</code>`);
    if (k.prereg) meta.push(`pre-registered in ${commitLink(k.program, k.prereg)}`);
    if (b?.resultFile) meta.push(`result: ${resultLink(k.program, b.resultFile)}`);
    if (b?.verdictPrereg) meta.push(`the rule's own reading: “${inline(b.verdictPrereg)}”`);
    const audit = !b ? "" : b.audit
      ? `<a href="data/ledger/${esc(b.audit.replace(/^ledger\//, ""))}">audited</a>` : "not yet audited";
    const kind = b?.failureKind ? ` <span class="k-kind">kind: ${esc(b.failureKind)}</span>` : "";
    const diagText = k.diagnosis ? inline(String(k.diagnosis).replace(/\s*Kind (world|design|execution|artefact)\.\s*$/i, "")) : "";
    return head + `<li class="kill">
      <div class="k-top">${markSVG("killed", 14)}<span>${[d ? esc(fmtDate(d)) : "", audit].filter(Boolean).join(" · ")}</span><span class="k-prog">${esc(k.programTitle || k.program)}</span></div>
      <h3>${esc(k.title)}</h3>
      <p class="diag">${diagText ? diagText + kind : `<span class='muted'>No diagnosis in the ledger yet${b && !b.audit ? " (its audit has not run)" : ""}.</span>`}</p>
      ${k.evidence && k.evidence !== k.diagnosis ? `<p class="ev">${inline(k.evidence)}</p>` : ""}
      ${meta.length ? `<details><summary>Evidence</summary>${meta.map((x) => `<p>${x}</p>`).join("")}</details>` : ""}
    </li>`;
  }).join("");
})();
