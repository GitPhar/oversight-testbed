// The cockpit: at most 20 cards, the next layer of directions, posted before any session pre-registers them.
// Per card: what we would test (one plain question), would you spend about $X on it, will it come back a hit, what our
// own settled results say so far (one sentence), your odds if you want. One "Save my answers" button writes human-odds.jsonl in the ledger's format (ledger/README.md): every
// line already committed, plus the new ones. The next session picks the file up from ~/Downloads with
// ledger/pickup_human_odds.py and commits it. The engine's odds are never shown here (CONTEXT.md §3 rule 11).
//
// Which cards: map/cockpit-cards.jsonl, written ahead of the pre-registrations (CONTEXT.md §3 rule 11, the ordering
// rule): for every program, the two cheapest not-yet-bet follow-ups its remap wrote. A card drops off once its
// direction has a bet in ledger/bets.jsonl (too late to attach) or an answer in ledger/human-odds.jsonl.
// The page reads no map file, so no engine odds reach the browser.
import { header, esc, SITE, DATA, getText, getJSONL } from "./common.js";
import { loadBets } from "./data.js";

header();

const MAX = 20;
const KEY = "cockpit.v2";
const el = (id) => document.getElementById(id);

// ---------- local store: answers survive a reload until they are saved and committed ----------
let local = { answers: {}, lines: [] };
try { const s = JSON.parse(localStorage.getItem(KEY) || "null"); if (s) local = { ...local, ...s }; } catch { /* storage blocked */ }
const store = () => { try { localStorage.setItem(KEY, JSON.stringify(local)); } catch { /* one visit only */ } };

function denverNow() {
  const parts = Object.fromEntries(new Intl.DateTimeFormat("en-CA", {
    timeZone: "America/Denver", year: "numeric", month: "2-digit", day: "2-digit",
    hour: "2-digit", minute: "2-digit", second: "2-digit", hourCycle: "h23", timeZoneName: "longOffset",
  }).formatToParts(new Date()).map((p) => [p.type, p.value]));
  const off = (parts.timeZoneName || "").replace("GMT", "") || "-07:00";
  const date = `${parts.year}-${parts.month}-${parts.day}`, time = `${parts.hour}:${parts.minute}`;
  return { date, time, iso: `${date}T${time}:${parts.second}${off}`, stamp: `${parts.year}${parts.month}${parts.day}-${parts.hour}${parts.minute}${parts.second}` };
}

// ---------- choosing the cards ----------
function choose(rows, answered, betOn) {
  return rows.filter((r) => r.program && r.direction && !answered.has(`${r.program}|${r.direction}`) && !betOn.has(`${r.program}|${r.direction}`))
    .slice(0, MAX)
    .map((r) => ({ key: `${r.program}|${r.direction}`, program: r.program, programTitle: r.program_title || r.program, id: r.direction,
      layer: r.layer || "", test: r.question, hit: r.hit_means || null, ours: r.our_results || null,
      spend: { ask: r.spend_ask || "Its cost is not estimated yet. Would you run it anyway?", phrase: r.spend_asked || null }, event: r.event || null }));
}

// ---------- drawing ----------
const yesNo = (c, name, val) => `<div class="yn" role="radiogroup" aria-label="${name === "spend" ? "Would you spend it" : "Will it come back a hit"}">
  ${[[true, "Yes"], [false, "No"]].map(([v, w]) => `<button type="button" class="btn yn-b" role="radio" data-key="${esc(c.key)}" data-q="${name}" data-v="${v}" aria-checked="${val === v}">${w}</button>`).join("")}
</div>`;
function cardHTML(c, i) {
  const a = local.answers[c.key] || {};
  const prog = c.programTitle.replace(/^Program\s*(\d+):\s*/i, "Program $1 · ");
  return `<article class="qcard${a.spend != null || a.hit != null || a.odds != null ? " answered" : ""}" data-key="${esc(c.key)}">
    <div class="q-top"><span class="q-n">${i + 1}</span><span>${esc(prog)}</span><span class="muted">· ${/^remap/.test(c.layer) ? "a follow-up from its remap" : "next on its map"}</span></div>
    <h3 class="q-test">${esc(c.test)}</h3>
    ${c.ours ? `<p class="q-ours"><b>What our own results say so far:</b> ${esc(c.ours)}</p>` : ""}
    <div class="q-row"><p class="q-ask">${esc(c.spend.ask)}</p>${yesNo(c, "spend", a.spend)}</div>
    <div class="q-row"><p class="q-ask">Will it come back a hit?${c.hit ? `<span class="q-hit">A hit means: ${esc(c.hit)}</span>` : ""}</p>${yesNo(c, "hit", a.hit)}</div>
    <div class="q-row q-odds"><label for="o-${i}">Your odds it comes back a hit, if you want</label>
      <span><input id="o-${i}" type="number" inputmode="numeric" min="0" max="100" step="1" placeholder="0–100" data-key="${esc(c.key)}" value="${a.odds ?? ""}"> %</span></div>
  </article>`;
}

let cards = [], committedText = "", committedIds = new Set();
function anyAnswer(a) { return a && (a.spend != null || a.hit != null || a.odds != null); }
function unsaved() {
  return cards.filter((c) => { const a = local.answers[c.key]; return anyAnswer(a) && a.changed && a.changed !== a.saved; });
}
function renderSave() {
  const n = unsaved().length, pending = local.lines.filter((l) => !committedIds.has(l.id)).length;
  el("save").disabled = n === 0 && pending === 0;
  el("save").textContent = n ? `Save my answers (${n})` : "Save my answers";
  el("savestate").textContent = n ? "" : pending
    ? `${pending} saved answer${pending === 1 ? " is" : "s are"} waiting for the next session to add ${pending === 1 ? "it" : "them"} to the ledger. Saving again rewrites the same file.`
    : "";
}

// ---------- saving: the whole file, in the ledger's format ----------
function lineFor(c, a) {
  const t = denverNow();
  const pct = a.odds == null ? null : a.odds;
  return {
    id: `ho-${t.stamp}-${Math.random().toString(36).slice(2, 5)}`, program: c.program, direction: c.id, bet: null,
    question: c.test, event: c.event, human_odds: pct == null ? null : pct / 100, odds_pct: pct,
    worth_spend: a.spend ?? null, spend_asked: c.spend.phrase, expects_hit: a.hit ?? null, hit_means: c.hit,
    because: null, saw_engine_odds: false, saw_engine_odds_note: "not seen: the cockpit never shows the engine's odds",
    human: SITE.operator, recorded: t.iso, date: t.date, time: t.time, recorded_via: "site/cockpit.html",
  };
}
function save() {
  for (const c of unsaved()) {
    const a = local.answers[c.key];
    local.lines.push(lineFor(c, a));
    a.saved = a.changed;
  }
  store();
  const fresh = local.lines.filter((l) => !committedIds.has(l.id));
  const body = (committedText.trim() ? committedText.trim() + "\n" : "") + fresh.map((l) => JSON.stringify(l)).join("\n") + (fresh.length ? "\n" : "");
  const a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([body], { type: "application/x-ndjson" }));
  a.download = "human-odds.jsonl";
  document.body.append(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(a.href), 4000);
  renderSave();
  el("savestate").textContent = `Saved human-odds.jsonl with ${fresh.length} new answer${fresh.length === 1 ? "" : "s"}. The next session picks it up.`;
  document.querySelectorAll(".qcard").forEach((n) => n.classList.toggle("saved", !!local.answers[n.dataset.key]?.saved));
}

// ---------- input ----------
function touch(key, patch) {
  const a = local.answers[key] || {};
  Object.assign(a, patch, { changed: new Date().toISOString() });
  local.answers[key] = a;
  store();
  document.querySelector(`.qcard[data-key="${CSS.escape(key)}"]`)?.classList.toggle("answered", anyAnswer(a));
  renderSave();
}
document.addEventListener("click", (e) => {
  const b = e.target.closest(".yn-b");
  if (b) {
    const key = b.dataset.key, q = b.dataset.q, v = b.dataset.v === "true";
    const cur = local.answers[key]?.[q];
    touch(key, { [q]: cur === v ? null : v });            // a second press clears it
    b.parentElement.querySelectorAll(".yn-b").forEach((x) => x.setAttribute("aria-checked", String(local.answers[key][q] === (x.dataset.v === "true"))));
    return;
  }
  if (e.target.id === "save") save();
});
document.addEventListener("input", (e) => {
  if (e.target.type !== "number" || !e.target.dataset.key) return;
  const s = e.target.value.trim(), n = Math.round(Number(s));
  const ok = s !== "" && Number.isFinite(n) && n >= 0 && n <= 100;
  e.target.setAttribute("aria-invalid", String(s !== "" && !ok));
  touch(e.target.dataset.key, { odds: ok ? n : null });
});

// ---------- load ----------
(async () => {
  const [bets, text, rows] = await Promise.all([loadBets(), getText(DATA + "ledger/human-odds.jsonl"), getJSONL(DATA + "map/cockpit-cards.jsonl")]);
  committedText = text || "";
  const committed = committedText.split("\n").map((l) => { try { return JSON.parse(l); } catch { return null; } }).filter(Boolean);
  committedIds = new Set(committed.map((l) => l.id));
  // what is in the ledger leaves this browser
  local.lines = local.lines.filter((l) => !committedIds.has(l.id));
  const answered = new Set(committed.map((l) => `${l.program}|${l.direction}`));
  for (const k of Object.keys(local.answers)) if (answered.has(k)) delete local.answers[k];
  store();
  const betOn = new Set(bets.filter((b) => b.program && b.direction).map((b) => `${b.program}|${b.direction}`));
  cards = choose(rows || [], answered, betOn);
  el("cards").innerHTML = cards.length ? cards.map(cardHTML).join("")
    : `<div class="empty">Nothing on the maps is waiting for an answer right now.</div>`;
  if (answered.size) el("intro").insertAdjacentHTML("beforeend", ` <span class="muted">${answered.size} question${answered.size === 1 ? " you answered is" : "s you answered are"} already in the ledger, so ${answered.size === 1 ? "it is" : "they are"} not shown again.</span>`);
  renderSave();
})();
