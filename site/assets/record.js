// The record as a timeline, parsed from entangled-mind's paper/record.md.
// Dated paragraphs and table rows become events; whatever follows the last table is shown as written.
import { header, esc, inline, slug, wrapTables } from "./common.js";
import { loadPaper, linkCommits } from "./papers-common.js";

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

(async () => {
  const { text, repo } = await loadPaper("record");
  if (!text) {
    main.innerHTML = `<h1>The record</h1><div class="empty">Could not load <code>paper/record.md</code> from the entangled-mind repository.</div>`;
    return;
  }
  const rec = parseRecord(text);
  const days = [...new Set(rec.events.map((e) => e.date).filter(Boolean))];

  main.innerHTML = `<h1>The record</h1>
    <p class="how">Program 1, test by test, in the order the tests ran. Each card shows the question asked, what came back, and what we concluded. Open “Details” on a card to see the commits that pre-registered and ran it. All times are America/Denver.</p>
    <p class="lede">${rec.events.length} entries over ${days.length} days.</p>
    <nav class="daynav" aria-label="Days">${days.map((d) => `<a class="btn" href="#d-${d}">${esc(dayTitle(d))}</a>`).join("")}<a class="btn" href="#standing">Where it stands</a></nav>
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
