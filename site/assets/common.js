// Shared by every page: the header, data loading, the status vocabulary, markdown.
// No build step. Data live under data/ at deploy time (see site/assemble.sh).

export const SITE = {
  title: "Oversight testbed",            // placeholder until the title is chosen (CONTEXT.md §0)
  titleNote: "working title",
  engineRepo: "https://github.com/GitPhar/oversight-testbed",
  operator: "Sean Pharris",              // the human whose odds and steers the cockpit records
  // Every program lives inside the engine repo as programs/<name>/, with its history imported (git subtree),
  // so commit hashes in the ledger resolve in the engine repo. Program 1's standalone repo is its historical record.
  // Any programs/<name> gets the same four links, so a new program's result files link correctly the day it
  // lands in the ledger (program 5's did not: it was missing from a hand-kept list).
  programs: new Proxy({}, { get: (_, name) => typeof name !== "string" ? undefined : ({
    commit: "https://github.com/GitPhar/oversight-testbed/commit/",
    blob: `https://github.com/GitPhar/oversight-testbed/blob/main/programs/${name}/`,
    raw: `https://raw.githubusercontent.com/GitPhar/oversight-testbed/main/programs/${name}/`,
    home: `https://github.com/GitPhar/oversight-testbed/tree/main/programs/${name}`,
  }) }),
  history: { "entangled-mind": "https://github.com/GitPhar/entangled-mind" },   // left untouched; history to 795dadb
};

export const DATA = "data/";

// Names for programs whose map is not deployed with the site (their map file lives only under programs/<name>/map/).
const PROGRAM_NAMES = { "entangled-mind": "Program 1: The Entangled Mind", "other-minds": "Program 2: Other Minds",
  "nature-graded": "Program 3: Nature-Graded", "settled-science": "Program 4: Settled Science",
  "self-grading": "Program 5: Self-Grading", "test-awareness": "Program 6: Test Awareness",
  "said-vs-did": "Program 7: Said vs Did" };
export function programTitle(id, programs = []) {
  return programs.find((p) => p.id === id)?.title || PROGRAM_NAMES[id] || id;
}

const PAGES = [
  ["index.html", "Home"],
  ["map.html", "Map"],
  ["replay.html", "Replay"],
  ["cockpit.html", "Cockpit"],
  ["human.html", "The human hand"],
  ["calibration.html", "Calibration"],
  ["instruments.html", "Instruments"],
  ["kills.html", "Kill log"],
  ["record.html", "Record"],
  ["papers.html", "Papers"],
];

// The site's root, from this module's own address (assets/common.js), so a link never depends on the page's URL:
// "…/index.html/" or "…/kills" would otherwise send every relative nav link to a 404.
export const ROOT = new URL("../", import.meta.url).href;
export const page = (h) => ROOT + h;

export function header() {
  const here = location.pathname.split("/").filter(Boolean).pop() || "index.html";
  const cur = here === "paper.html" ? "papers.html" : here;
  const el = document.createElement("header");
  el.className = "top";
  el.innerHTML = `<div class="top-inner">
    <a class="brand" href="${page("index.html")}">${esc(SITE.title)}<small>${esc(SITE.titleNote)}</small></a>
    <nav class="nav" aria-label="Site">${PAGES.map(([h, t]) =>
      `<a href="${page(h)}"${h === cur || h === cur + ".html" ? ' aria-current="page"' : ""}>${t}</a>`).join("")}</nav>
  </div>`;
  document.body.prepend(el);
  const f = document.createElement("footer");
  f.innerHTML = `Every number on this site is read from the repositories' own files. Nothing is typed in by hand. ·
    <a href="${SITE.engineRepo}">engine repository</a> ·
    <a href="${SITE.engineRepo}/tree/main/programs">programs</a> ·
    <a href="${SITE.history["entangled-mind"]}">program 1's original repository (historical record)</a>`;
  document.body.append(f);
}

// ---------- fetching ----------
export async function getText(url) {
  try {
    const r = await fetch(url, { cache: "no-cache" });
    if (!r.ok) return null;
    return await r.text();
  } catch { return null; }
}
export async function getJSON(url) {
  const t = await getText(url);
  if (t == null) return null;
  try { return JSON.parse(t); } catch { return null; }
}
export async function getJSONL(url) {
  const t = await getText(url);
  if (t == null) return null;
  const out = [];
  for (const line of t.split("\n")) {
    const s = line.trim();
    if (!s || s.startsWith("//")) continue;
    try { out.push(JSON.parse(s)); } catch { /* skip a bad line rather than lose the file */ }
  }
  return out;
}
// The deploy writes data/manifest.json listing the files it copied (Pages cannot list folders).
let _manifest;
export async function manifest() {
  if (_manifest === undefined) _manifest = (await getJSON(DATA + "manifest.json")) || {};
  return _manifest;
}

// ---------- the status vocabulary ----------
// Every status has a colour, a shape and a word. Colour is never the only channel.
export const STATUS = {
  hit:     { word: "Landed",      color: "var(--hit)",   hex: "#5cc98a" },
  killed:  { word: "Killed",      color: "var(--kill)",  hex: "#e47272" },
  mixed:   { word: "Mixed",       color: "var(--mixed)", hex: "#a99cf0" },
  running: { word: "Running",     color: "var(--run)",   hex: "#6aaee8" },
  open:    { word: "Open",        color: "var(--open)",  hex: "#737983" },
};

// What the words mean, in one plain sentence (the map's legend; Sean's walk, 2026-11-04).
export const LEGEND_SENTENCE = "<b>Landed</b> means its pre-registered test passed; <b>mixed</b> means it was tried but not settled " +
  "(a partial result, a test that could not decide, or one withdrawn); <b>killed</b> means a test said no, or it was dropped " +
  "with a stated reason before any test; <b>open</b> means nothing has tried it yet, and <b>running</b> means a test is under way now.";

const SYN = {
  hit: ["hit", "pass", "passed", "positive", "confirmed", "landed", "supported", "found", "true", "yes", "win"],
  killed: ["killed", "kill", "closed", "dead", "null", "fail", "failed", "falsified", "negative", "miss", "classical",
           "tie", "refuted", "no", "false"],
  mixed: ["mixed", "partial", "partly", "split", "untestable", "undetermined", "inconclusive", "withdrawn"],   // unsettled: the direction is not dead
  running: ["running", "bet", "preregistered", "pre-registered", "registered", "queued", "in_progress", "active"],
  open: ["open", "candidate", "proposed", "idea", "pending", ""],
};
export function normStatus(v) {
  if (v === true || v === 1) return "hit";
  if (v === false || v === 0) return "killed";
  const s = String(v ?? "").trim().toLowerCase();
  for (const [k, list] of Object.entries(SYN)) if (list.includes(s)) return k;
  return "open";
}

// Draws the status's mark as inline SVG. Same shapes as the map.
export function markSVG(status, size = 16) {
  const c = STATUS[status]?.hex || STATUS.open.hex;
  const h = size / 2, r = size / 2 - 2;
  const wrap = (inner) => `<svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" aria-hidden="true">${inner}</svg>`;
  switch (status) {
    case "hit": return wrap(`<circle cx="${h}" cy="${h}" r="${r}" fill="${c}"/>`);
    case "killed": {
      const a = h - r * 0.75, b = h + r * 0.75;
      return wrap(`<path d="M${a} ${a}L${b} ${b}M${b} ${a}L${a} ${b}" stroke="${c}" stroke-width="2.6" stroke-linecap="round"/>`);
    }
    case "mixed": return wrap(`<circle cx="${h}" cy="${h}" r="${r - 0.5}" fill="none" stroke="${c}" stroke-width="2"/><path d="M${h} ${h - r + 0.5}A${r - 0.5} ${r - 0.5} 0 0 1 ${h} ${h + r - 0.5}Z" fill="${c}"/>`);
    case "running": return wrap(`<circle cx="${h}" cy="${h}" r="${r - 1}" fill="none" stroke="${c}" stroke-width="2.4"/><circle cx="${h}" cy="${h}" r="${r * 0.35}" fill="${c}"/>`);
    default: return wrap(`<circle cx="${h}" cy="${h}" r="${r - 1}" fill="none" stroke="${c}" stroke-width="1.6" stroke-dasharray="2 2.2"/>`);
  }
}
export function chip(status) {
  return `<span class="chip">${markSVG(status, 15)}${STATUS[status]?.word || status}</span>`;
}

// ---------- normalising ledger rows (tolerant of field-name drift) ----------
export function num(v) {
  if (v === null || v === undefined || v === "" || v === "—" || v === "-") return null;
  let n = typeof v === "number" ? v : parseFloat(String(v).replace(/[^\d.\-]/g, ""));
  if (!isFinite(n)) return null;
  if (n > 1 && n <= 100) n = n / 100;    // tolerate percentages
  return n;
}
const pick = (o, ...keys) => { for (const k of keys) if (o[k] !== undefined && o[k] !== null && o[k] !== "") return o[k]; return undefined; };

export function normBet(o) {
  const verdictRaw = pick(o, "verdict", "outcome", "status", "result_class");
  // A bet pre-registered but not yet resolved is running, not open.
  const status = (verdictRaw == null || String(verdictRaw).toLowerCase() === "open") && o.prereg_commit && !o.result_commit
    ? "running" : normStatus(verdictRaw);
  return {
    raw: o,
    id: String(pick(o, "id", "bet_id", "bet", "key") ?? ""),
    program: pick(o, "program", "repo") || "",
    direction: pick(o, "direction", "direction_id", "map_id") ?? "",
    title: pick(o, "title", "question", "name", "direction") || "(untitled bet)",
    engine: num(pick(o, "engine_odds", "engine_p", "p_engine", "odds_engine", "engine")),
    human: num(pick(o, "human_odds", "human_p", "p_human", "odds_human", "human")),
    verdictRaw: verdictRaw ?? "",
    status,
    date: pick(o, "date", "resolved", "verdict_date", "landed", "opened") || "",
    result: pick(o, "result", "result_summary", "summary") || "",
    // A failed bet's reason is written as failure_reason by the auditor's scoring (operators/premortem.md).
    diagnosis: pick(o, "diagnosis", "why", "kill_reason", "failure_reason") || "",
    failureKind: pick(o, "failure_kind") || "",
    prereg: pick(o, "prereg_commit", "prereg", "preregistration") || "",
    source: pick(o, "source") || "",
    cost: pick(o, "cost", "budget") || (o.cost_usd != null ? "$" + Number(o.cost_usd).toFixed(2) : ""),
    engineFirst: num(pick(o, "engine_odds_first")),
    oddsEvent: pick(o, "odds_event") || "",
    opened: pick(o, "prereg_time", "opened") || "",
    landed: pick(o, "result_time", "date", "resolved") || "",
    resultFile: pick(o, "result_file") || "",
    resultCommit: pick(o, "result_commit") || "",
    verdictPrereg: pick(o, "verdict_prereg") || "",
    scored: o.scored,
    scoringNote: pick(o, "scoring_note") || "",
    replicationOf: pick(o, "replication_of") || "",
    audit: pick(o, "audit_path") || "",
    auditStatus: pick(o, "audit_status") || "",
    verdictAfterAudit: pick(o, "verdict_after_audit") || "",
    referee: refereeOf(o),
  };
}

// What decided a bet's outcome. Three referees: another model, the quantum chip, the published record.
export const REFEREE = {
  model:  { word: "Model-graded",  short: "model",  hex: "#3987e5", shape: "circle",   what: "another language model's behaviour decided it" },
  chip:   { word: "Chip-graded",   short: "chip",   hex: "#c98500", shape: "square",   what: "the ibm_fez quantum chip decided it" },
  record: { word: "Record-graded", short: "record", hex: "#d55181", shape: "triangle", what: "the published literature decided it" },
};
export function refereeOf(o) {
  const r = String(o.referee || "").toLowerCase();
  if (["nature", "chip", "hardware", "qpu"].includes(r)) return "chip";
  if (["published-record", "record", "literature", "published"].includes(r)) return "record";
  if (["mathematics", "math", "maths", "proof"].includes(r)) return "maths";
  if (r) return "model";
  return o.program === "nature-graded" ? "chip" : o.program === "settled-science" ? "record" : "model";
}
// The mark for a referee, as SVG markup centred on (x, y). Shape and colour both carry identity.
export function refMark(ref, x, y, r = 7, ring = "#191c20") {
  const R = REFEREE[ref] || REFEREE.model, c = R.hex;
  if (R.shape === "square") return `<rect x="${x - r * 0.9}" y="${y - r * 0.9}" width="${r * 1.8}" height="${r * 1.8}" rx="2" fill="${c}" stroke="${ring}" stroke-width="2"/>`;
  if (R.shape === "triangle") { const h = r * 1.15; return `<path d="M${x} ${y - h}L${x + h} ${y + h * 0.8}L${x - h} ${y + h * 0.8}Z" fill="${c}" stroke="${ring}" stroke-width="2" stroke-linejoin="round"/>`; }
  return `<circle cx="${x}" cy="${y}" r="${r}" fill="${c}" stroke="${ring}" stroke-width="2"/>`;
}
export function refKey(ref, size = 16) {
  const h = size / 2;
  return `<svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" aria-hidden="true">${refMark(ref, h, h + (REFEREE[ref]?.shape === "triangle" ? 1 : 0), h - 2.5, "transparent")}</svg>`;
}
// 1 = hit, 0 = miss, null = not scorable (open, running, mixed)
export function outcomeOf(b) {
  if (b.raw?.scored === false) return null;   // the ledger says this bet is not scored; respect it
  const o = b.raw?.outcome;
  if (o === 1 || o === "1" || o === true) return 1;
  if (o === 0 || o === "0" || o === false) return 0;
  if (b.status === "hit") return 1;
  if (b.status === "killed") return 0;
  return null;
}

// ---------- time ----------
export function parseDate(s) {
  if (!s) return null;
  const m = String(s).match(/(\d{4})-(\d{2})-(\d{2})(?:[T ](\d{2}):(\d{2}))?/);
  if (!m) return null;
  return new Date(+m[1], +m[2] - 1, +m[3], +(m[4] || 0), +(m[5] || 0)); // already America/Denver local in the data
}
const MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
const WD = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
export function fmtDate(d, withTime = true) {
  if (!d) return "";
  const t = `${String(d.getHours()).padStart(2, "0")}:${String(d.getMinutes()).padStart(2, "0")}`;
  return `${WD[d.getDay()]} ${MON[d.getMonth()]} ${d.getDate()}${withTime ? ", " + t : ""}`;
}

// ---------- markdown ----------
export function esc(s) {
  return String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}
// Inline markdown only (bold, italic, code, links) for short strings inside cards.
export function inline(md) {
  if (window.marked) return window.marked.parseInline(String(md ?? ""));
  return esc(md);
}
// Wrap every table in a scroll container so wide tables never push the page sideways.
export function wrapTables(root) {
  root.querySelectorAll("table").forEach((t) => {
    if (t.parentElement.classList.contains("tablewrap")) return;
    const w = document.createElement("div");
    w.className = "tablewrap";
    t.replaceWith(w);
    w.append(t);
  });
}
export function slug(s) {
  return String(s).toLowerCase().replace(/<[^>]+>/g, "").replace(/[^\w\s-]/g, "").trim().replace(/\s+/g, "-").slice(0, 80);
}
