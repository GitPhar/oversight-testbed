// The record as a timeline, parsed from entangled-mind's paper/record.md.
// Dated paragraphs and table rows become events; whatever follows the last table is shown as written.
import { header, esc, inline, slug, wrapTables, markSVG, STATUS, SITE, parseDate, fmtDate, programTitle, REFEREE, refKey } from "./common.js";
import { loadPaper, linkCommits } from "./papers-common.js";
import { loadBets, loadMaps } from "./data.js";

header();
const main = document.getElementById("main");
const MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
const DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
function dayTitle(iso) {
  const [y, m, d] = iso.split("-").map(Number);
  const dt = new Date(y, m - 1, d);
  return `${DAYS[dt.getDay()]}, ${MONTHS[m - 1]} ${d}`;
}

function parseRecord(md) {
  const lines = md.split("\n");
  const title = (lines.find((l) => /^#\s/.test(l)) || "# The record").replace(/^#\s+/, "");
  const intro = [];
  const events = [];
  const trailing = [];
  let date = null, seenEvent = false, seenTable = false, inTrailing = false;
  const cells = (row) => row.trim().replace(/^\||\|$/g, "").split("|").map((c) => c.trim());

  for (let i = 0; i < lines.length; i++) {
    const L = lines[i];
    if (/^#\s/.test(L)) continue;
    const rem = L.match(/remaining entries are from (\d{4}-\d{2}-\d{2})/i);
    if (rem && !inTrailing) { date = rem[1]; continue; }

    const dated = L.match(/^\*\*(\d{4}-\d{2}-\d{2})(?:\s+(\d{1,2}:\d{2}))?:?\s*(.*?)\*\*\s*(.*)$/);
    if (dated && !inTrailing) {
      date = dated[1];
      const ev = { date, time: dated[2] || "", q: dated[3].replace(/[.:]\s*$/, ""), result: dated[4], bullets: [], milestone: true };
      while (lines[i + 1] && /^\s*[-*]\s/.test(lines[i + 1])) ev.bullets.push(lines[++i].replace(/^\s*[-*]\s+/, ""));
      events.push(ev);
      seenEvent = true;
      continue;
    }
    if (L.trim().startsWith("|") && lines[i + 1] && /^\s*\|[\s:|-]+\|\s*$/.test(lines[i + 1]) && !inTrailing) {
      const head = cells(L).map((h) => h.toLowerCase());
      i += 2;
      while (i < lines.length && lines[i].trim().startsWith("|")) {
        const r = Object.fromEntries(head.map((h, j) => [h, cells(lines[i])[j] || ""]));
        events.push({ date, time: r.time || "", q: r.question || r.test || "", result: r.result || "", diagnosis: r.diagnosis || "",
          prereg: r["pre-registered"] || "", test: r["test (commit)"] || r.test || "", redirect: r.redirect || "", bullets: [] });
        i++;
      }
      i--;
      seenTable = true;
      continue;
    }
    if (!seenEvent) { intro.push(L); continue; }
    // A bold paragraph that is not dated, after the tables, starts the closing notes.
    if (seenTable && /^\*\*[^*\d]/.test(L)) inTrailing = true;
    if (inTrailing) trailing.push(L);
  }
  return { title, intro: intro.join("\n"), events, trailing: trailing.join("\n") };
}

const dash = (s) => !s || /^[—–-]$/.test(s.trim());

// ---------- programs 2 onward, from the ledger ----------
// Program 1 has its own hand-kept record (paper/record.md). The later programs' record is their ledger rows:
// each bet in the order it landed, with the verdict as the audit left it (verdict_after_audit) when there is one.
const VERDICT_WORDS = {
  "pass-unreplicated": "passed its pre-registered rule once, on one model and one item set; not yet repeated",
  pass: "passed its pre-registered rule", fail: "failed its pre-registered rule", running: "pre-registered; no result yet", untestable: "its rule could not be applied",
  undetermined: "neither a pass nor a fail is established", mixed: "partly passed", open: "pre-registered; no result yet",
};
function ledgerCards(bets, maps) {
  // A bet still running has no landing time; it is placed by its pre-registration and drawn last.
  const when = (b) => b.status === "running" ? (b.raw?.prereg_time || b.opened) : (b.raw?.result_time || b.landed || b.opened);
  const later = bets.filter((b) => b.program && b.program !== "entangled-mind" && b.prereg && b.raw?.verdict !== "withdrawn")
    .sort((a, b) => (a.status === "running") - (b.status === "running") || String(when(a)).localeCompare(String(when(b))));
  if (!later.length) return "";
  const link = (b, file) => `<a href="${SITE.programs[b.program]?.blob || ""}${esc(file)}">${esc(file.split("/").pop())}</a>`;
  const commit = (h) => h ? `<a href="${SITE.engineRepo}/commit/${esc(h)}"><code>${esc(h)}</code></a>` : "";
  const pnum = (id) => +(programTitle(id, maps).match(/\d+/)?.[0] || 99);
  const progs = [...new Set(later.map((b) => b.program))].sort((a, b) => pnum(a) - pnum(b));
  const p4 = later.filter((b) => b.program === "settled-science" && b.status === "hit");
  const p4u = p4.filter((b) => /unreplicated/i.test(b.verdictAfterAudit)).length;
  const days = [...new Set(later.map((b) => String(when(b) || "").slice(0, 10)).filter(Boolean))];
  let html = `<section id="ledger" class="ledger-record"><h2>${progs.length === 1 ? esc(programTitle(progs[0], maps)) : `Programs ${progs.map((id) => programTitle(id, maps).match(/\d+/)?.[0]).filter(Boolean).join(", ")}`}, from the ledger</h2>
    <p class="how">Every bet these programs placed, in the order it landed, read from <code>ledger/bets.jsonl</code>. The verdict is the one the audit left standing, in the audit's own words.</p>
    ${p4.length ? `<p class="lede">${esc(programTitle("settled-science", maps).replace(/:.*/, ""))}'s first results: ${p4.length} pass${p4.length === 1 ? "" : "es"}${p4u ? `, ${p4u === p4.length ? "all" : p4u} audited as <b class="scope">pass-unreplicated</b>` : ""}.${later.some((b) => b.program !== "settled-science" && b.status === "hit") ? "" : " No other program after program 1 has a pass in the ledger."}${p4u ? " Each has held once, on one model and one item set." : ""}</p>` : ""}
    <ol class="timeline">`;
  let cur = null;
  for (const b of later) {
    const day = String(when(b) || "").slice(0, 10);
    if (day !== cur) { cur = day; html += `<li class="day"><h2>${esc(dayTitle(day))}</h2><p>${later.filter((x) => String(when(x) || "").slice(0, 10) === day).length} bets</p></li>`; }
    // The ledger writes a failed rule as "null"; on the page it is a fail. Every other verdict is shown as written.
    const v0 = b.verdictAfterAudit || b.verdictRaw || "";
    const v = b.status === "running" ? "running" : String(v0).toLowerCase() === "null" ? "fail" : v0;
    const vword = VERDICT_WORDS[v.toLowerCase()] || VERDICT_WORDS[String(b.verdictRaw).toLowerCase()] || "";
    const t = parseDate(when(b));
    const auditCounts = (String(b.auditStatus).match(/\d+ claims[^;)]*/) || [])[0] || "";
    const auditNote = (String(b.scoringNote).match(/The audit notes (.*)$/) || [])[1] || "";
    const ref = REFEREE[b.referee];
    const det = [
      ["Pre-registered", commit(b.prereg)], ["Result", b.resultFile ? link(b, b.resultFile) : ""], ["Result commit", commit(b.resultCommit)],
      ["The rule's own reading", b.verdictPrereg ? inline(b.verdictPrereg) : ""],
    ].filter(([, x]) => x);
    html += `<li class="ev-item${b.status === "hit" ? " milestone" : ""}"><div class="ev-card">
      <div class="ev-time">${t ? esc(b.status === "running" ? `pre-registered ${fmtDate(t)}` : fmtDate(t)) : ""} · ${esc(programTitle(b.program, maps))}${ref ? ` · ${refKey(b.referee, 13)} ${esc(ref.word.toLowerCase())}` : ""}</div>
      <div class="ev-q">${esc(b.title)}</div>
      <p class="ev-verdict">${markSVG(b.status, 14)} <b class="scope">${esc(v || STATUS[b.status]?.word || "")}</b>${vword ? ` <span class="muted">· ${esc(vword)}</span>` : ""}</p>
      ${b.result ? `<p class="ev-r">${inline(b.result)}</p>` : ""}
      ${b.status === "killed" && b.diagnosis ? `<p class="ev-r" style="margin-top:8px;color:var(--text-2)"><b style="color:var(--text)">Why it failed:</b> ${inline(b.diagnosis.replace(/\s*Kind (world|design|execution|artefact)\.\s*$/i, ""))}</p>` : ""}
      <p class="ev-audit">${b.audit ? `<a href="data/ledger/${esc(b.audit.replace(/^ledger\//, ""))}">Audited</a>${auditCounts ? `: ${esc(auditCounts)}` : ""}.${auditNote ? ` The audit notes ${inline(auditNote)}` : ""}` : `<span class="muted">Not yet audited.</span>`}</p>
      ${det.length ? `<details><summary>Details</summary><dl>${det.map(([k, x]) => `<dt>${k}</dt><dd>${x}</dd>`).join("")}</dl></details>` : ""}
    </div></li>`;
  }
  return { html: html + `</ol></section>`, days, label: progs.length === 1 ? programTitle(progs[0], maps).replace(/:.*/, "") : "Programs 2 onward" };
}

(async () => {
  const [{ text, repo }, bets, maps] = await Promise.all([loadPaper("record"), loadBets(), loadMaps()]);
  const L = ledgerCards(bets, maps);
  if (!text) {
    main.innerHTML = `<h1>The record</h1><div class="empty">Could not load <code>paper/record.md</code> from the entangled-mind repository.</div>${L ? L.html : ""}`;
    return;
  }
  const rec = parseRecord(text);
  const days = [...new Set(rec.events.map((e) => e.date).filter(Boolean))];

  main.innerHTML = `<h1>The record</h1>
    <p class="how">Each test in the order it ran. The newer programs come first, read from the ledger; then program 1, test by test, from its own record. Each card shows the question asked, what came back, and what was concluded. Open “Details” to see the commits that pre-registered and ran it. All times are America/Denver.</p>
    <nav class="daynav" aria-label="Sections">${L ? `<a class="btn" href="#ledger">${esc(L.label)}</a>` : ""}<a class="btn" href="#p1">Program 1</a>${days.map((d) => `<a class="btn" href="#d-${d}">${esc(dayTitle(d))}</a>`).join("")}<a class="btn" href="#standing">Where it stands</a></nav>
    ${L ? L.html : ""}
    <h2 id="p1" class="rec-p1">${esc(programTitle("entangled-mind", maps))}</h2>
    <p class="lede">${rec.events.length} entries over ${days.length} days.</p>
    <ol class="timeline" id="tl"></ol>
    <section class="prose" id="standing"></section>
    <p class="muted small" style="margin-top:32px">Parsed from <a href="${repo}/blob/main/paper/record.md">paper/record.md</a>. If this page and that file disagree, the file is right.</p>`;

  let html = "", curDay = null;
  for (const e of rec.events) {
    if (e.date !== curDay) {
      curDay = e.date;
      const n = rec.events.filter((x) => x.date === curDay).length;
      html += `<li class="day" id="d-${curDay}"><h2>${esc(dayTitle(curDay))}</h2><p>${n} ${n === 1 ? "entry" : "entries"}</p></li>`;
    }
    const det = [
      ["Pre-registered", e.prereg], ["Test", e.test], ["Led to", e.redirect],
    ].filter(([, v]) => !dash(v));
    html += `<li class="ev-item${e.milestone ? " milestone" : ""}"><div class="ev-card">
      ${e.time ? `<div class="ev-time">${esc(e.time)}</div>` : ""}
      <div class="ev-q">${inline(e.q.charAt(0).toUpperCase() + e.q.slice(1))}</div>
      ${e.result ? `<p class="ev-r">${inline(e.result)}</p>` : ""}
      ${!dash(e.diagnosis) && e.diagnosis ? `<p class="ev-r" style="margin-top:8px;color:var(--text-2)"><b style="color:var(--text)">What it meant:</b> ${inline(e.diagnosis)}</p>` : ""}
      ${e.bullets.length ? `<ul>${e.bullets.map((b) => `<li>${inline(b)}</li>`).join("")}</ul>` : ""}
      ${det.length ? `<details><summary>Details</summary><dl>${det.map(([k, v]) => `<dt>${k}</dt><dd>${inline(v)}</dd>`).join("")}</dl></details>` : ""}
    </div></li>`;
  }
  const tl = document.getElementById("tl");
  tl.innerHTML = html;
  const st = document.getElementById("standing");
  st.innerHTML = rec.trailing.trim() ? `<h2>Where it stands</h2>` + window.marked.parse(rec.trailing) : "";
  wrapTables(st);
  linkCommits(main, repo);
})();
