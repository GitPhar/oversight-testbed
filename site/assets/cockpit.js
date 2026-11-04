// The cockpit: where the human steers. One card per open or running question across every program.
// Odds are entered before the engine's number is shown; vetoes need a reason; new questions are steers.
// No backend: entries live in this browser (localStorage, best effort) until downloaded as JSON lines and
// appended to ledger/human-odds.jsonl and ledger/steers.jsonl by hand. Once committed, the ledger is the truth
// and the local copy of that entry is dropped.
import { header, esc, inline, markSVG, STATUS, SITE, fmtDate, parseDate } from "./common.js";
import { loadBets, loadMaps, joinBets, loadSteers, loadHumanOdds } from "./data.js";

header();

const KEY = "cockpit.v1";
const el = (id) => document.getElementById(id);
const HUMAN = SITE.operator;

// ---------- local store (best effort: private windows and blocked storage still work for one visit) ----------
let local = { odds: [], steers: [], revealed: {}, exported: {} };
try { const s = JSON.parse(localStorage.getItem(KEY) || "null"); if (s) local = { ...local, ...s }; } catch { /* storage blocked */ }
let storageOK = true;
function save() {
  try { localStorage.setItem(KEY, JSON.stringify(local)); storageOK = true; } catch { storageOK = false; }
}

// ---------- time, in America/Denver ----------
function denverNow() {
  const d = new Date();
  const parts = Object.fromEntries(new Intl.DateTimeFormat("en-CA", {
    timeZone: "America/Denver", year: "numeric", month: "2-digit", day: "2-digit",
    hour: "2-digit", minute: "2-digit", second: "2-digit", hourCycle: "h23", timeZoneName: "longOffset",
  }).formatToParts(d).map((p) => [p.type, p.value]));
  const off = (parts.timeZoneName || "").replace("GMT", "") || "-07:00";
  const date = `${parts.year}-${parts.month}-${parts.day}`, time = `${parts.hour}:${parts.minute}`;
  return { date, time, iso: `${date}T${time}:${parts.second}${off}`, stamp: `${parts.year}${parts.month}${parts.day}-${parts.hour}${parts.minute}${parts.second}` };
}
const rand = () => Math.random().toString(36).slice(2, 5);
const showTime = (iso) => { const d = parseDate(iso); return d ? fmtDate(d) : iso; };

// ---------- the cards ----------
let cards = [], committedOdds = [], committedSteers = [], filter = { program: "all", needOdds: false };

// A fixed shuffle within each program, so the engine's ranking does not nudge the human.
function hash(s) { let h = 2166136261; for (const c of s) { h ^= c.charCodeAt(0); h = Math.imul(h, 16777619); } return h >>> 0; }
const progNum = (p) => { const m = String(p.title).match(/program\s*(\d+)/i); return m ? +m[1] : 99; };

function buildCards(programs, bets) {
  const out = [];
  const onMap = new Set();
  for (const p of programs) {
    for (const d of p.directions) {
      if (d.bet) onMap.add(d.bet.id);
      if (d.status !== "open" && d.status !== "running") continue;
      if (d.raw.moved_to) continue;               // shown in the program it was carried into
      const r = d.raw;
      out.push({
        key: `${p.id}|${d.id}`, program: p.id, programTitle: p.title, programNum: progNum(p), id: d.id, status: d.status,
        question: r.question || d.title, known: r.known || [], test: r.cheapest_test || d.test || "",
        cost: d.cost || "", event: r.odds_event || d.bet?.oddsEvent || "", engine: d.engine,
        title: d.title, betId: d.bet?.id || null,
      });
    }
  }
  // a running bet that no map node points at still gets a card
  for (const b of bets) {
    if (b.status !== "running" || onMap.has(b.id)) continue;
    const p = programs.find((x) => x.id === b.program);
    out.push({ key: `${b.program}|${b.direction || b.id}`, program: b.program, programTitle: p?.title || b.program, programNum: p ? progNum(p) : 99,
      id: String(b.direction || b.id), status: "running", question: b.title, known: [], test: b.raw.test || "", cost: b.cost,
      event: b.oddsEvent, engine: b.engine, title: b.title, betId: b.id });
  }
  return out.sort((a, b) => a.programNum - b.programNum || hash(a.key + "cockpit") - hash(b.key + "cockpit"));
}

// Everything the human has said about a card, committed first, then local.
function oddsFor(c) {
  const all = [...committedOdds.map((e) => ({ ...e, committed: true })), ...local.odds]
    .filter((e) => `${e.program}|${e.direction}` === c.key);
  return all.sort((a, b) => String(a.recorded).localeCompare(String(b.recorded)));
}
function steersFor(c) {
  return [...committedSteers.map((e) => ({ ...e, committed: true })), ...local.steers]
    .filter((e) => e.program === c.program && String(e.direction) === c.id);
}

function cardHTML(c) {
  const odds = oddsFor(c);
  const first = odds[0], last = odds[odds.length - 1];
  const steers = steersFor(c);
  const veto = steers.find((s) => s.action === "veto");
  const revealed = !!local.revealed[c.key];
  const canReveal = odds.length > 0;
  const progShort = c.programTitle.replace(/^Program\s*(\d+):\s*/i, "Program $1 · ");
  const known = c.known.length ? `<ul class="known">${c.known.slice(0, 2).map((k) => `<li>${esc(k)}</li>`).join("")}</ul>` : "";
  const test = c.test ? `<p class="test"><b>Cheapest test:</b> ${esc(c.test)}${c.cost ? ` <span class="costpill">${esc(c.cost)}</span>` : ""}</p>`
    : c.cost ? `<p class="test"><b>Cost:</b> <span class="costpill">${esc(c.cost)}</span></p>` : "";
  const event = c.event
    ? `<details class="event"><summary>The exact event you're betting on</summary><p style="margin:6px 0 0">${inline(c.event)}</p></details>`
    : `<p class="event">No exact pass rule yet. Your number is for the question as written.</p>`;

  let oddsBlock;
  if (last && !c._changing) {
    const changed = odds.length > 1 ? ` <span class="muted">(first said ${Math.round(first.odds_pct)}%)</span>` : "";
    oddsBlock = `<div class="oddsrow">
      <span class="recorded">Your odds: <b>${Math.round(last.odds_pct)}%</b>${changed} · ${esc(showTime(last.recorded))}${last.committed ? " · in the ledger" : ""}${last.saw_engine_odds ? " · after seeing the engine's" : ""}</span>
      <button class="btn" type="button" data-act="change">Change my mind</button>
    </div>`;
  } else {
    oddsBlock = `<div class="oddsrow">
      <label class="big" for="o-${esc(c.key)}">Your odds it comes true</label>
      <input type="number" inputmode="numeric" min="0" max="100" step="1" id="o-${esc(c.key)}" data-role="odds" placeholder="0–100" aria-describedby="g-${esc(c.key)}">
      <span class="pct">%</span>
      <button class="btn primary" type="button" data-act="record" disabled>Record my odds</button>
      <span class="muted small" id="g-${esc(c.key)}" style="flex-basis:100%">5 = I'd be amazed · 25 = I doubt it · 50 = coin flip · 75 = I expect it · 95 = amazed if not</span>
      <span class="later" data-role="later" hidden>
        <input class="because" type="text" data-role="because" placeholder="Because… (one sentence, optional)" aria-label="Why, in one sentence">
        ${revealed ? "" : `<label class="seen"><input type="checkbox" data-role="seen"> I had already seen the engine's number somewhere</label>`}
      </span>
      ${c._changing ? `<button class="btn" type="button" data-act="cancel-change">Cancel</button>` : ""}
    </div>`;
  }

  let reveal = "";
  if (revealed) {
    reveal = c.engine != null
      ? `<div class="reveal">Engine's odds, stated before data: <b>${Math.round(c.engine * 100)}%</b>${last ? ` · yours: <b>${Math.round(last.odds_pct)}%</b>` : ""}</div>`
      : `<div class="reveal">The engine gave no odds for this one.</div>`;
  }

  const mine = steers.filter((s) => s.action !== "veto").map((s) =>
    `<li>Question added: ${esc(s.reason)} <span class="muted">· ${s.committed ? "in the ledger" : local.exported[s.id] ? "downloaded" : "not downloaded yet"}</span>${!s.committed && !local.exported[s.id] ? ` <button class="btn" type="button" data-act="undo" data-id="${esc(s.id)}" style="font-size:13px;padding:0 10px">Undo</button>` : ""}</li>`).join("");
  const vetoLine = veto ? `<p class="vetonote"><b>Vetoed</b> · ${esc(veto.reason)} <span class="muted">· ${veto.committed ? "in the ledger" : local.exported[veto.id] ? "downloaded" : "not downloaded yet"}</span>${!veto.committed && !local.exported[veto.id] ? ` <button class="btn" type="button" data-act="undo" data-id="${esc(veto.id)}" style="font-size:13px;padding:0 10px">Undo</button>` : ""}</p>` : "";

  return `<article class="card${veto ? " vetoed" : last ? " done" : ""}" data-key="${esc(c.key)}">
    <div class="c-top">${markSVG(c.status, 14)} ${STATUS[c.status].word} · ${esc(c.id)}<span class="prog">${esc(progShort)}</span></div>
    <h3>${esc(c.question)}</h3>
    ${known}${test}${event}
    ${oddsBlock}
    ${reveal}
    <div class="actions">
      ${revealed ? "" : `<button class="btn" type="button" data-act="reveal" ${canReveal ? "" : `disabled title="Record your own odds first"`}>Reveal the engine's odds</button>`}
      ${veto ? "" : `<button class="btn danger" type="button" data-act="veto-open" aria-expanded="false">Veto…</button>`}
      <button class="btn" type="button" data-act="q-open" aria-expanded="false">Add a question…</button>
      ${canReveal || revealed ? "" : `<span class="muted small">The engine's number unlocks after yours.</span>`}
    </div>
    <div class="panelbox" data-panel="veto" hidden>
      <label class="lbl">Why veto this direction? (required; this is what gets scored later)</label>
      <textarea data-role="veto-reason" placeholder="e.g. Too close to what program 1 already showed; not worth the money."></textarea>
      <div class="actions"><button class="btn danger" type="button" data-act="veto" disabled>Veto it</button><button class="btn" type="button" data-act="veto-close">Cancel</button></div>
    </div>
    <div class="panelbox" data-panel="q" hidden>
      <label class="lbl">A question that grows from this one</label>
      <textarea data-role="q-text" placeholder="Your question, in your own words"></textarea>
      <div class="actions"><button class="btn primary" type="button" data-act="q-add" disabled>Add the question</button><button class="btn" type="button" data-act="q-close">Cancel</button></div>
    </div>
    ${vetoLine}${mine ? `<ul class="mine">${mine}</ul>` : ""}
  </article>`;
}

function visibleCards() {
  return cards.filter((c) => (filter.program === "all" || c.program === filter.program) && (!filter.needOdds || !oddsFor(c).length));
}

function render() {
  const list = visibleCards();
  el("cards").innerHTML = list.length ? list.map(cardHTML).join("") :
    `<div class="empty">${cards.length ? "Nothing here needs your odds. Untick the box to see every card." : "No open questions in the maps."}</div>`;
  renderFilters();
  renderBar();
  renderExport();
}
function rerenderCard(key) {
  const c = cards.find((x) => x.key === key);
  const old = document.querySelector(`.card[data-key="${CSS.escape(key)}"]`);
  if (!c || !old) return render();
  old.outerHTML = cardHTML(c);
  renderFilters(); renderBar(); renderExport();
}

function renderFilters() {
  const progs = [...new Map(cards.map((c) => [c.program, c])).values()];
  const need = (p) => cards.filter((c) => (p === "all" || c.program === p) && !oddsFor(c).length).length;
  const count = (p) => cards.filter((c) => p === "all" || c.program === p).length;
  el("filters").innerHTML =
    [`<button class="btn" type="button" data-prog="all" aria-pressed="${filter.program === "all"}">All · ${count("all")}</button>`,
      ...progs.map((c) => `<button class="btn" type="button" data-prog="${esc(c.program)}" aria-pressed="${filter.program === c.program}" title="${esc(c.programTitle)}">Program ${c.programNum} · ${count(c.program)}</button>`)].join("") +
    `<label><input type="checkbox" id="needodds" ${filter.needOdds ? "checked" : ""}> Only the ones still waiting for my odds (${need(filter.program)})</label>`;
}

// ---------- the pending lines, and their export ----------
const pendingOdds = () => local.odds.filter((e) => !local.exported[e.id]);
const pendingSteers = () => local.steers.filter((e) => !local.exported[e.id]);
const clean = (e) => { const { committed, ...rest } = e; return rest; };
const lines = (arr) => arr.map((e) => JSON.stringify(clean(e))).join("\n") + (arr.length ? "\n" : "");

function renderBar() {
  const o = pendingOdds().length, sv = pendingSteers().filter((s) => s.action === "veto").length, sq = pendingSteers().filter((s) => s.action !== "veto").length;
  const waiting = cards.filter((c) => !oddsFor(c).length).length;
  const any = o + sv + sq;
  el("bar").innerHTML = `<span class="count"><b>${waiting}</b> of ${cards.length} still need your odds${any ? ` · not downloaded yet: <b>${o}</b> odds, <b>${sv}</b> veto${sv === 1 ? "" : "es"}, <b>${sq}</b> question${sq === 1 ? "" : "s"}` : ""}${storageOK ? "" : ` · <span style="color:var(--kill)">this browser is not saving; download before you leave</span>`}</span>
    ${o ? `<button class="btn primary" type="button" data-dl="odds">Download odds (${o})</button>` : ""}
    ${sv + sq ? `<button class="btn primary" type="button" data-dl="steers">Download steers (${sv + sq})</button>` : ""}
    ${any ? "" : `<a class="small" href="#export">How saving works</a>`}`;
}

let lastFiles = {};
function renderExport() {
  const o = pendingOdds(), s = pendingSteers();
  const exportedWaiting = [...local.odds, ...local.steers].filter((e) => local.exported[e.id]).length;
  const fo = lastFiles.odds || "human-odds-<time>.jsonl", fs = lastFiles.steers || "steers-<time>.jsonl";
  el("export").innerHTML = `<h2>Saving what you entered</h2>
    <p class="muted small" style="margin:0 0 8px">Two downloads, one per ledger file. Each holds only the lines that are new. Then, in the engine repository:</p>
    <pre>cat ~/Downloads/${esc(fo)} &gt;&gt; ledger/human-odds.jsonl
cat ~/Downloads/${esc(fs)} &gt;&gt; ledger/steers.jsonl
git add ledger &amp;&amp; git commit -m "Cockpit: odds and steers"</pre>
    <p class="muted small" style="margin:0">Your number is final once it is in the ledger. A change of mind is a new line with a new time, and both stay. When the site next deploys, committed entries show as "in the ledger" and leave this browser's list.${exportedWaiting ? ` ${exportedWaiting} downloaded entr${exportedWaiting === 1 ? "y is" : "ies are"} waiting to show up in the ledger.` : ""}</p>
    <div class="actions">
      <button class="btn" type="button" data-copy="odds" ${o.length ? "" : "disabled"}>Copy the odds lines</button>
      <button class="btn" type="button" data-copy="steers" ${s.length ? "" : "disabled"}>Copy the steer lines</button>
    </div>`;
}

function toast(msg) {
  document.querySelectorAll(".toast").forEach((x) => x.remove());
  const t = document.createElement("div");
  t.className = "toast"; t.textContent = msg; t.setAttribute("role", "status");
  document.body.append(t);
  setTimeout(() => t.remove(), 2600);
}

function download(kind) {
  const arr = kind === "odds" ? pendingOdds() : pendingSteers();
  if (!arr.length) return;
  const name = `${kind === "odds" ? "human-odds" : "steers"}-${denverNow().stamp}.jsonl`;
  const blob = new Blob([lines(arr)], { type: "application/x-ndjson" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob); a.download = name;
  document.body.append(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(a.href), 4000);
  for (const e of arr) local.exported[e.id] = true;
  lastFiles[kind] = name;
  save();
  render();
  toast(`Saved ${name}. Append it to the ledger, then commit.`);
}
async function copy(kind) {
  const arr = kind === "odds" ? pendingOdds() : pendingSteers();
  try { await navigator.clipboard.writeText(lines(arr)); toast("Copied. These lines still count as not downloaded."); }
  catch { toast("This browser would not copy. Use the download button."); }
}

// ---------- actions ----------
function addSteer(c, action, text) {
  const t = denverNow();
  const s = {
    id: `st-${t.stamp}-${rand()}`, date: t.date, time: t.time, human: HUMAN, program: c.program,
    action, direction: c.id, reason: text,
    outcome: null, outcome_later: null, evidence: [], value: "pending", value_judgment: null, counterfactual: null,
    value_judged_by: null, scored: false, recorded: t.iso, recorded_via: "site/cockpit.html",
  };
  if (action === "veto") s.direction_title = c.title;
  if (action === "add_question") s.grows_from = c.id ? c.title : null;
  local.steers.push(s);
  save();
}

document.addEventListener("input", (e) => {
  const card = e.target.closest(".card");
  if (card) {
    const role = e.target.dataset.role;
    if (role === "odds") {
      const v = e.target.value.trim(), n = Number(v);
      const ok = v !== "" && Number.isFinite(n) && n >= 0 && n <= 100;
      card.querySelector('[data-act="record"]').disabled = !ok;
      if (ok) card.querySelector('[data-role="later"]').hidden = false;
    }
    if (role === "veto-reason") card.querySelector('[data-act="veto"]').disabled = e.target.value.trim().length < 3;
    if (role === "q-text") card.querySelector('[data-act="q-add"]').disabled = e.target.value.trim().length < 5;
  }
  if (e.target.id === "newq") el("newqbtn").disabled = e.target.value.trim().length < 5;
});
document.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && e.target.dataset?.role === "odds") {
    const b = e.target.closest(".card").querySelector('[data-act="record"]');
    if (!b.disabled) b.click();
  }
});
document.addEventListener("change", (e) => {
  if (e.target.id === "needodds") { filter.needOdds = e.target.checked; render(); }
});

document.addEventListener("click", (e) => {
  const dl = e.target.closest("[data-dl]"); if (dl) return download(dl.dataset.dl);
  const cp = e.target.closest("[data-copy]"); if (cp) return copy(cp.dataset.copy);
  const pf = e.target.closest("[data-prog]"); if (pf) { filter.program = pf.dataset.prog; return render(); }
  const btn = e.target.closest("[data-act]");
  if (!btn) return;
  const card = btn.closest(".card");
  const c = card && cards.find((x) => x.key === card.dataset.key);
  if (!c) return;
  const panel = (name, open) => {
    const p = card.querySelector(`[data-panel="${name}"]`);
    p.hidden = !open;
    const opener = card.querySelector(`[data-act="${name}-open"]`);
    if (opener) opener.setAttribute("aria-expanded", String(open));
    if (open) p.querySelector("textarea").focus();
  };
  switch (btn.dataset.act) {
    case "record": {
      const n = Math.round(Number(card.querySelector('[data-role="odds"]').value));
      const because = card.querySelector('[data-role="because"]').value.trim();
      const seenBox = card.querySelector('[data-role="seen"]');
      const revealed = !!local.revealed[c.key];
      const t = denverNow();
      local.odds.push({
        id: `ho-${t.stamp}-${rand()}`, program: c.program, direction: c.id, bet: c.betId,
        question: c.question, event: c.event || null,
        human_odds: n / 100, odds_pct: n, because: because || null,
        saw_engine_odds: revealed || !!seenBox?.checked,
        saw_engine_odds_note: revealed ? "revealed in the cockpit before this entry" : seenBox?.checked ? "the human said they had already seen it elsewhere" : "not seen: the cockpit hides it until this entry is recorded",
        human: HUMAN, recorded: t.iso, date: t.date, time: t.time, recorded_via: "site/cockpit.html",
      });
      c._changing = false;
      save();
      rerenderCard(c.key);
      document.querySelector(`.card[data-key="${CSS.escape(c.key)}"] [data-act="reveal"]`)?.focus();
      break;
    }
    case "change": c._changing = true; rerenderCard(c.key); document.querySelector(`.card[data-key="${CSS.escape(c.key)}"] [data-role="odds"]`)?.focus(); break;
    case "cancel-change": c._changing = false; rerenderCard(c.key); break;
    case "reveal":
      if (!oddsFor(c).length) return;
      local.revealed[c.key] = true; save(); rerenderCard(c.key); break;
    case "veto-open": panel("q", false); panel("veto", true); break;
    case "veto-close": panel("veto", false); break;
    case "q-open": panel("veto", false); panel("q", true); break;
    case "q-close": panel("q", false); break;
    case "veto": {
      const r = card.querySelector('[data-role="veto-reason"]').value.trim();
      if (r.length < 3) return;
      addSteer(c, "veto", r); rerenderCard(c.key); toast("Veto logged. Download the steers to make it count."); break;
    }
    case "q-add": {
      const q = card.querySelector('[data-role="q-text"]').value.trim();
      if (q.length < 5) return;
      addSteer(c, "add_question", q); rerenderCard(c.key); toast("Question logged."); break;
    }
    case "undo":
      local.steers = local.steers.filter((s) => s.id !== btn.dataset.id || local.exported[s.id]);
      save(); rerenderCard(c.key); break;
  }
});

el("newqbtn").addEventListener("click", () => {
  const q = el("newq").value.trim();
  const p = el("newprog").value;
  if (q.length < 5) return;
  addSteer({ program: p, id: null, title: null }, "add_question", q);
  el("newq").value = ""; el("newqbtn").disabled = true;
  render();
  toast("Question logged. Download the steers to make it count.");
});

// ---------- load ----------
(async () => {
  const [bets, maps, steers, odds] = await Promise.all([loadBets(), loadMaps(), loadSteers(), loadHumanOdds()]);
  const programs = joinBets(maps, bets);
  committedOdds = odds;
  committedSteers = steers.filter((s) => s.direction != null && (s.action === "veto" || s.action === "add_question"));
  // what is already in the ledger leaves the browser's list
  const inLedger = new Set([...odds, ...steers].map((e) => e.id));
  const before = local.odds.length + local.steers.length;
  local.odds = local.odds.filter((e) => !inLedger.has(e.id));
  local.steers = local.steers.filter((e) => !inLedger.has(e.id));
  if (local.odds.length + local.steers.length !== before) save();
  cards = buildCards(programs, bets);
  el("newprog").innerHTML = programs.map((p) => `<option value="${esc(p.id)}">${esc(p.title)}</option>`).join("");
  render();
  if (location.hash) document.querySelector(`.card[data-key="${CSS.escape(decodeURIComponent(location.hash.slice(1)))}"]`)?.scrollIntoView();
})();

window.addEventListener("beforeunload", (e) => {
  if (!storageOK && (pendingOdds().length || pendingSteers().length)) { e.preventDefault(); e.returnValue = ""; }
});
