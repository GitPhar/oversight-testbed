// The record as a timeline, parsed from entangled-mind's paper/record.md.
// Dated paragraphs and table rows become events; whatever follows the last table is shown as written.
import { header, esc, inline, slug, wrapTables, markSVG, STATUS, SITE, parseDate, fmtDate, programTitle, REFEREE, refKey, DATA, getJSON } from "./common.js";
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
const hasClock = (s) => /\d{1,2}:\d{2}/.test(String(s || ""));
function ledgerCards(bets, maps, commitTimes = {}) {
  // A bet still running has no landing time; it is placed by its pre-registration and drawn last.
  // A row whose result_time has no clock (or is missing) takes the time of its result commit, read from git by
  // the deploy (data/commit-times.json); failing that it shows the date alone, never a made-up 00:00.
  const when = (b) => {
    const r = b.raw || {};
    if (b.status === "running") return r.prereg_time || b.opened;
    if (hasClock(r.result_time)) return r.result_time;
    return String(commitTimes[r.result_commit] || r.result_time || b.landed || b.opened || "").replace("T", " ");   // one format, so the order sorts right
  };
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
    ${summary(later, progs, maps)}
    <div id="ledger-tl">`;
  // Two blocks, each labelled, so the day headers do not repeat without a reason (panel review, Part 3): bets with a
  // result, by the day it landed, then bets still open, by the day they were pre-registered.
  const settled = later.filter((b) => b.status !== "running"), open = later.filter((b) => b.status === "running");
  const block = (list, tag, title, how) => {
    if (!list.length) return;
    const scored = list.filter((b) => b.raw?.scored === true).length;
    html += `<h3 class="rec-block" id="ledger-${tag}">${title} <span class="muted rec-n">${list.length} bet${list.length === 1 ? "" : "s"}${tag === "settled" ? `, ${scored} scored` : ""}</span></h3>
      <p class="how rec-how">${how}</p><ol class="timeline">`;
    let cur = null;
    for (const b of list) {
      const day = `${tag}-${String(when(b) || "").slice(0, 10)}`;
      if (day !== cur) { cur = day; html += `<li class="day" data-day="${esc(day)}"><h2>${esc(dayTitle(day.slice(tag.length + 1)))}</h2><p class="daycount">${list.filter((x) => `${tag}-${String(when(x) || "").slice(0, 10)}` === day).length} bets</p></li>`; }
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
      html += `<li class="ev-item${b.status === "hit" ? " milestone" : ""}" data-p="${esc(b.program)}" data-day="${esc(day)}"><div class="ev-card">
        <div class="ev-time">${t ? esc(b.status === "running" ? `pre-registered ${fmtDate(t)}` : fmtDate(t, hasClock(when(b)))) : ""} · ${esc(programTitle(b.program, maps))}${ref ? ` · ${refKey(b.referee, 13)} ${esc(ref.word.toLowerCase())}` : ""}</div>
        <div class="ev-q">${esc(b.title)}</div>
        <p class="ev-verdict">${markSVG(b.status, 14)} <b class="scope">${esc(v || STATUS[b.status]?.word || "")}</b>${vword ? ` <span class="muted">· ${esc(vword)}</span>` : ""}</p>
        ${b.result ? `<p class="ev-r">${inline(b.result)}</p>` : ""}
        ${b.status === "killed" && b.diagnosis ? `<p class="ev-r" style="margin-top:8px;color:var(--text-2)"><b style="color:var(--text)">Why it failed:</b> ${inline(b.diagnosis.replace(/\s*Kind (world|design|execution|artefact)\.\s*$/i, ""))}</p>` : ""}
        <p class="ev-audit">${b.audit ? `<a href="data/ledger/${esc(b.audit.replace(/^ledger\//, ""))}">Audited</a>${auditCounts ? `: ${esc(auditCounts)}` : ""}.${auditNote ? ` The audit notes ${inline(auditNote)}` : ""}` : `<span class="muted">Not yet audited.</span>`}</p>
        ${det.length ? `<details><summary>Details</summary><dl>${det.map(([k, x]) => `<dt>${k}</dt><dd>${x}</dd>`).join("")}</dl></details>` : ""}
      </div></li>`;
    }
    html += `</ol>`;
  };
  block(settled, "settled", "Settled: the result is in",
    "Each bet with a verdict, by the day its result landed. <b>Scored</b> ones count in the engine's score; the rest (untestable, undetermined, a second bet on a run already scored, or no odds stated) are shown with the same card and say why.");
  block(open, "open", "Open: pre-registered, no result yet",
    "Each bet whose test is written down and committed but has not come back, by the day it was pre-registered.");
  return { html: html + `</div></section>`, days, open: open.length, label: progs.length === 1 ? programTitle(progs[0], maps).replace(/:.*/, "") : `Programs ${progs.map((id) => programTitle(id, maps).match(/\d+/)?.[0]).filter(Boolean).join(", ")}` };
}

// One row per program after program 1, counted from the ledger, and a button that shows only that program's cards.
function summary(later, progs, maps) {
  const c = (id, st) => later.filter((b) => b.program === id && (st ? b.status === st : true)).length;
  const rows = progs.map((id) => `<tr><td><button class="btn rf" type="button" data-p="${esc(id)}" aria-pressed="false">${esc(programTitle(id, maps)).replace(/^Program\s+/, '<span class="rs-long">Program </span>')}</button></td>
    <td class="num">${c(id)}</td><td class="num">${c(id, "hit")}</td><td class="num">${c(id, "killed")}</td><td class="num">${c(id, "mixed")}</td><td class="num">${c(id, "running")}</td></tr>`).join("");
  return `<div class="tablewrap rec-sum"><table><thead><tr><th>Program <span class="muted rs-long" style="font-weight:400">(tap to show only its bets)</span></th><th class="num">bets</th><th class="num">landed</th><th class="num">killed</th><th class="num">mixed</th><th class="num"><span class="rs-long">no result yet</span><span class="rs-short">open</span></th></tr></thead><tbody>${rows}</tbody></table></div>
    <p class="rf-all"><button class="btn rf" type="button" data-p="" aria-pressed="true">All programs</button> <span class="muted small" id="rf-state"></span></p>`;
}
function wireFilter() {
  const tl = document.getElementById("ledger-tl");
  if (!tl) return;
  const btns = [...document.querySelectorAll(".rf")];
  const apply = (p) => {
    btns.forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.p === p)));
    let shown = 0;
    tl.querySelectorAll(".ev-item").forEach((li) => { const on = !p || li.dataset.p === p; li.hidden = !on; if (on) shown++; });
    tl.querySelectorAll(".day").forEach((d) => {
      const n = [...tl.querySelectorAll(`.ev-item[data-day="${d.dataset.day}"]`)].filter((li) => !li.hidden).length;
      d.hidden = !n;
      d.querySelector(".daycount").textContent = `${n} bet${n === 1 ? "" : "s"}`;
    });
    // A block (settled, open) with no card left for this program hides its label too.
    tl.querySelectorAll(".rec-block").forEach((h) => {
      const ol = h.nextElementSibling?.nextElementSibling;
      const any = ol ? [...ol.querySelectorAll(".ev-item")].some((li) => !li.hidden) : true;
      h.hidden = !any; if (h.nextElementSibling) h.nextElementSibling.hidden = !any;
    });
    document.getElementById("rf-state").textContent = p ? `Showing ${shown} bet${shown === 1 ? "" : "s"} from one program.` : "";
  };
  btns.forEach((b) => b.addEventListener("click", () => apply(b.dataset.p)));
}

(async () => {
  const [{ text, repo }, bets, maps, ct] = await Promise.all([loadPaper("record"), loadBets(), loadMaps(), getJSON(DATA + "commit-times.json")]);
  const L = ledgerCards(bets, maps, ct || {});
  if (!text) {
    main.innerHTML = `<h1>The record</h1><div class="empty">Could not load <code>paper/record.md</code> from the entangled-mind repository.</div>${L ? L.html : ""}`;
    wireFilter();
    return;
  }
  const rec = parseRecord(text);
  const days = [...new Set(rec.events.map((e) => e.date).filter(Boolean))];

  main.innerHTML = `<h1>The record</h1>
    <p class="how">Each test in the order it ran. The newer programs come first, read from the ledger; then program 1, test by test, from its own record. Each card shows the question asked, what came back, and what was concluded. Open “Details” to see the commits that pre-registered and ran it. All times are America/Denver.</p>
    <nav class="daynav" aria-label="Sections">${L ? `<a class="btn" href="#ledger-settled">${esc(L.label)}: settled</a>${L.open ? `<a class="btn" href="#ledger-open">${esc(L.label)}: open</a>` : ""}` : ""}<a class="btn" href="#p1">Program 1</a>${days.map((d) => `<a class="btn" href="#d-${d}">${esc(dayTitle(d))}</a>`).join("")}<a class="btn" href="#standing">Where it stands</a></nav>
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
  wireFilter();
  const st = document.getElementById("standing");
  st.innerHTML = rec.trailing.trim() ? `<h2>Where it stands</h2>` + window.marked.parse(rec.trailing) : "";
  wrapTables(st);
  linkCommits(main, repo);
})();
