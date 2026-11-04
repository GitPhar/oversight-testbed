// The map: paths fan out from a seed question and collapse as bets land.
// Built from data/map/*.json joined with data/ledger/bets.jsonl. Plain SVG, no library.
import { header, esc, inline, STATUS, markSVG, chip, parseDate, fmtDate } from "./common.js";
import { loadBets, loadMaps, joinBets } from "./data.js";

header();

const R = 7;                 // node radius
const LINE_H = 21;           // label line height
const FONT = 16;
let WRAP = 30;            // shrinks when the map would not fit             // characters per label line
const MAX_LINES = 2;
const COL_GAP = 70;          // horizontal room for the curves between columns
const SIB_GAP = 10;
const PAD = { l: 28, r: 40, t: 30, b: 30 };

const KEY_TEXT = {
  hit: "",
  running: "",
  mixed: "",
  killed: "hover for why",
  open: "not yet bet on",
};

const el = (id) => document.getElementById(id);
const SVGNS = "http://www.w3.org/2000/svg";
let programs = [], current = null, times = [], tIndex = 0, pinned = null, playTimer = null;

// ---------- text measuring ----------
const ctx = document.createElement("canvas").getContext("2d");
function measure(s, bold) {
  ctx.font = `${bold ? 700 : 400} ${FONT}px "Plain Digits", "Atkinson Hyperlegible", system-ui, sans-serif`;
  return ctx.measureText(s).width;
}
function wrap(text) {
  const words = String(text).split(/\s+/).filter(Boolean);
  const lines = [];
  let cur = "";
  for (const w of words) {
    if (!cur) cur = w;
    else if ((cur + " " + w).length <= WRAP) cur += " " + w;
    else { lines.push(cur); cur = w; }
  }
  if (cur) lines.push(cur);
  if (lines.length > MAX_LINES) {
    const kept = lines.slice(0, MAX_LINES);
    kept[MAX_LINES - 1] = kept[MAX_LINES - 1].replace(/[\s,;:.]*$/, "") + "…";
    return kept;
  }
  return lines;
}

// ---------- tree ----------
function buildTree(p) {
  const root = { id: "__seed", title: "Seed question", status: "seed", children: [], depth: 0, isRoot: true,
    opened: p.seedDate };
  const byId = new Map(p.directions.map((d) => [d.id, { ...d, children: [] }]));
  for (const n of byId.values()) {
    const par = n.parent != null && byId.has(String(n.parent)) ? byId.get(String(n.parent)) : root;
    par.children.push(n);
    n.parentNode = par;
  }
  // depth (guard against cycles in hand-edited data)
  const seen = new Set();
  (function setDepth(n, d) {
    if (seen.has(n)) return;
    seen.add(n);
    n.depth = d;
    n.children.forEach((c) => setDepth(c, d + 1));
  })(root, 0);
  for (const n of byId.values()) if (!seen.has(n)) { n.depth = 1; root.children.push(n); n.parentNode = root; }
  // Siblings sorted by where they ended up, so the bright paths bundle together and the faint ones fan out below.
  const rank = { hit: 0, running: 1, mixed: 2, killed: 3, open: 4 };
  (function sortKids(n) { n.children.sort((a, b) => (rank[a.status] ?? 5) - (rank[b.status] ?? 5)); n.children.forEach(sortKids); })(root);
  return root;
}

function layout(root) {
  const all = [];
  (function walk(n) { all.push(n); n.children.forEach(walk); })(root);
  for (const n of all) {
    n.lines = n.isRoot ? ["Seed question"] : wrap(n.label || n.title);
    n.bold = n.isRoot || n.status === "hit";
    n.labelW = Math.max(...n.lines.map((l) => measure(l, n.bold)));
    n.labelH = n.lines.length * LINE_H;
  }
  // columns
  const maxDepth = Math.max(...all.map((n) => n.depth));
  const colX = [PAD.l + R];
  for (let d = 0; d < maxDepth; d++) {
    const w = Math.max(...all.filter((n) => n.depth === d).map((n) => R + 12 + n.labelW + 10));
    colX.push(colX[d] + w + COL_GAP);
  }
  for (const n of all) n.x = colX[n.depth];
  // rows: each subtree takes the height of its children or of its own label, whichever is taller
  function place(n, top) {
    const own = Math.max(n.labelH, 2 * R) + SIB_GAP;
    if (!n.children.length) { n.y = top + own / 2; return own; }
    const kids = n.children.map((c) => ({ c, h: subtreeH(c) }));
    const sum = kids.reduce((a, k) => a + k.h, 0);
    let y = top + Math.max(0, (own - sum) / 2);
    for (const k of kids) { place(k.c, y); y += k.h; }
    n.y = (n.children[0].y + n.children[n.children.length - 1].y) / 2;
    return Math.max(sum, own);
  }
  const memo = new Map();
  function subtreeH(n) {
    if (memo.has(n)) return memo.get(n);
    const own = Math.max(n.labelH, 2 * R) + SIB_GAP;
    const h = n.children.length ? Math.max(n.children.reduce((a, c) => a + subtreeH(c), 0), own) : own;
    memo.set(n, h);
    return h;
  }
  const H = place(root, PAD.t);
  const W = Math.max(...all.map((n) => n.x + R + 12 + n.labelW)) + PAD.r;
  return { all, W, H: H + PAD.t + PAD.b };
}

// ---------- state at a moment ----------
function stateAt(n, t) {
  if (n.isRoot) return "seed";
  if (t == null) return n.status;
  const o = parseDate(n.opened), r = parseDate(n.resolved);
  if (o && t < o) return "hidden";
  if (r && t >= r) return n.status;
  if (r) return "open";              // held open until its bet landed
  return n.status;                   // still open or running today
}

// ---------- drawing ----------
const EDGE = {
  hit: { w: 3, c: "#f2c14e", o: 1, dash: null },
  running: { w: 2.5, c: "#6aaee8", o: 0.95, dash: null },
  mixed: { w: 2.5, c: "#a99cf0", o: 0.9, dash: null },
  killed: { w: 2, c: "#e47272", o: 0.55, dash: null },
  open: { w: 1.6, c: "#8a9099", o: 0.5, dash: "1 6" },
};
const TEXT = { seed: "#ffffff", hit: "#ffffff", running: "#ece9e2", mixed: "#ece9e2", killed: "#a9a59c", open: "#8d8a82" };

function s(tag, attrs, parent) {
  const e = document.createElementNS(SVGNS, tag);
  for (const [k, v] of Object.entries(attrs)) if (v != null) e.setAttribute(k, v);
  if (parent) parent.append(e);
  return e;
}

function drawMark(g, status, x, y) {
  const c = STATUS[status]?.hex;
  switch (status) {
    case "seed":
      s("circle", { cx: x, cy: y, r: R + 3, fill: "#ece9e2" }, g); break;
    case "hit":
      s("circle", { cx: x, cy: y, r: R + 1, fill: c, stroke: "#191c20", "stroke-width": 2 }, g); break;
    case "killed": {
      const a = R * 0.95;
      s("circle", { cx: x, cy: y, r: R + 2, fill: "#191c20" }, g);
      s("path", { d: `M${x - a} ${y - a}L${x + a} ${y + a}M${x + a} ${y - a}L${x - a} ${y + a}`, stroke: c, "stroke-width": 3, "stroke-linecap": "round" }, g);
      break;
    }
    case "mixed":
      s("circle", { cx: x, cy: y, r: R, fill: "#191c20", stroke: c, "stroke-width": 2.2 }, g);
      s("path", { d: `M${x} ${y - R}A${R} ${R} 0 0 1 ${x} ${y + R}Z`, fill: c }, g);
      break;
    case "running":
      s("circle", { cx: x, cy: y, r: R, fill: "#191c20", stroke: c, "stroke-width": 2.6 }, g);
      s("circle", { cx: x, cy: y, r: 2.6, fill: c }, g);
      break;
    default:
      s("circle", { cx: x, cy: y, r: R - 1, fill: "#191c20", stroke: "#8a9099", "stroke-width": 1.6, "stroke-dasharray": "2 2.4" }, g);
  }
}

function draw() {
  const box = el("mapbox");
  box.innerHTML = "";
  if (!current) return;
  const root = buildTree(current);
  const avail = box.clientWidth;
  let L;
  for (const w of [30, 26, 22, 19]) {        // narrower labels before scrolling sideways
    WRAP = w;
    L = layout(root);
    if (L.W * 0.86 <= avail) break;
  }
  const { all, W, H } = L;
  const t = times.length ? times[tIndex] : null;
  const isLatest = !times.length || tIndex === times.length - 1;
  for (const n of all) {
    n.view = stateAt(n, isLatest ? null : t);
    if (n.view !== "hidden" && n.parentNode && n.parentNode.view === "hidden") n.view = "hidden";
  }

  const svg = s("svg", { width: W, height: H, viewBox: `0 0 ${W} ${H}`, role: "img",
    "aria-label": `Map of ${current.title}: ${all.length - 1} directions` });
  const edges = s("g", {}, svg);
  const nodes = s("g", {}, svg);

  // draw faint edges first so bright ones sit on top
  const order = { open: 0, killed: 1, mixed: 2, running: 3, hit: 4 };
  const visible = all.filter((n) => !n.isRoot && n.view !== "hidden").sort((a, b) => order[a.view] - order[b.view]);
  for (const n of visible) {
    const p = n.parentNode;
    const st = EDGE[n.view] || EDGE.open;
    const x1 = p.x + R + 12 + p.labelW + 8, y1 = p.y;
    const x2 = n.x - R - 5, y2 = n.y;
    const dx = Math.max(24, (x2 - x1) * 0.55);
    s("path", { d: `M${x1} ${y1}C${x1 + dx} ${y1} ${x2 - dx} ${y2} ${x2} ${y2}`, fill: "none",
      stroke: st.c, "stroke-width": st.w, "stroke-opacity": st.o, "stroke-dasharray": st.dash, "stroke-linecap": "round" }, edges);
  }

  for (const n of all) {
    if (n.view === "hidden") continue;
    const g = s("g", { class: "node", tabindex: 0, role: "button",
      "aria-label": n.isRoot ? `Seed question: ${current.seed}` : `${STATUS[n.view]?.word}: ${n.title}` }, nodes);
    g.__node = n;
    const top = n.y - n.labelH / 2;
    s("rect", { x: n.x - R - 6, y: Math.min(top, n.y - R) - 4, width: R * 2 + 18 + n.labelW, height: Math.max(n.labelH, 2 * R) + 8, fill: "transparent" }, g);
    s("circle", { class: "halo", cx: n.x, cy: n.y, r: R + 6, fill: "none", stroke: "transparent" }, g);
    drawMark(g, n.view, n.x, n.y);
    const tx = s("text", { x: n.x + R + 12, y: top + LINE_H * 0.74, fill: TEXT[n.view] || TEXT.open,
      "font-size": FONT, "font-weight": n.bold && n.view === n.status ? 700 : 400 }, g);
    n.lines.forEach((l, i) => { const ts = s("tspan", { x: n.x + R + 12, dy: i ? LINE_H : 0 }, tx); ts.textContent = l; });
  }
  box.append(svg);
  // Shrink slightly to fit rather than scroll, but never so far that labels drop below ~14px.
  box.classList.toggle("scrolls", W * 0.86 > avail);
  if (W > avail && avail / W >= 0.86) { svg.setAttribute("width", avail); svg.setAttribute("height", H * avail / W); }
  wireTips(svg);
  renderTimeLabel(all);
}

// ---------- tooltip ----------
let tip;
function tipHTML(n) {
  if (n.isRoot) {
    return `<div class="t-status">Seed question</div><div class="t-title">${esc(current.seed)}</div>` +
      (current.seedDate ? `<div class="t-meta">Opened ${esc(fmtDate(parseDate(current.seedDate)))}</div>` : "");
  }
  const v = n.view;
  const meta = [];
  if (n.engine != null) meta.push(`Engine's odds before data: <b>${Math.round(n.engine * 100)}%</b>`);
  meta.push(`Human's odds before data: <b>${n.human != null ? Math.round(n.human * 100) + "%" : "not recorded"}</b>`);
  if (n.cost) meta.push(`Cost: ${esc(n.cost)}`);
  if (n.resolved && v !== "open") meta.push(`Landed ${esc(fmtDate(parseDate(n.resolved)))}`);
  else if (n.opened) meta.push(`Opened ${esc(fmtDate(parseDate(n.opened)))}`);
  if (n.bet?.prereg) meta.push(`Pre-registered in <code>${esc(n.bet.prereg)}</code>`);
  let body = "";
  if (v === "killed") body += `<div class="t-diag"><b>Why it died.</b> ${n.diagnosis ? inline(n.diagnosis) : "No diagnosis recorded yet."}</div>`;
  if (n.result && v !== "open") body += `<div style="margin-top:8px">${inline(n.result)}</div>`;
  if (v === "open" && n.status !== "open") body += `<div style="margin-top:8px" class="muted">Not yet bet on at this point in the replay.</div>`;
  return `<div class="t-status">${markSVG(v, 14)}${STATUS[v]?.word || v}</div>
    <div class="t-title">${esc(n.title)}</div>${body}<div class="t-meta">${meta.join("<br>")}</div>`;
}
function showTip(g) {
  if (!tip) { tip = document.createElement("div"); tip.className = "tip"; tip.style.position = "fixed"; document.body.append(tip); }
  tip.innerHTML = tipHTML(g.__node);
  tip.hidden = false;
  const r = g.querySelector(".halo").getBoundingClientRect();
  const tw = Math.min(352, window.innerWidth - 24);
  tip.style.maxWidth = tw + "px";
  const th = tip.offsetHeight;
  let x = r.right + 10, y = r.top - 6;
  if (x + tw > window.innerWidth - 12) x = Math.max(12, r.left - tw - 10);
  if (x < 12) { x = 12; y = r.bottom + 10; }
  if (y + th > window.innerHeight - 12) y = Math.max(70, window.innerHeight - th - 12);
  tip.style.left = x + "px";
  tip.style.top = y + "px";
  document.querySelectorAll(".node.active").forEach((a) => a.classList.remove("active"));
  g.classList.add("active");
}
function hideTip() {
  if (tip) tip.hidden = true;
  document.querySelectorAll(".node.active").forEach((a) => a.classList.remove("active"));
  pinned = null;
}
function wireTips(svg) {
  svg.querySelectorAll(".node").forEach((g) => {
    g.addEventListener("mouseenter", () => { if (!pinned) showTip(g); });
    g.addEventListener("mouseleave", () => { if (!pinned) hideTip(); });
    g.addEventListener("focus", () => showTip(g));
    g.addEventListener("blur", () => { if (!pinned) hideTip(); });
    g.addEventListener("click", (e) => { e.stopPropagation(); if (pinned === g) hideTip(); else { pinned = g; showTip(g); } });
    g.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); pinned = g; showTip(g); } });
  });
}
document.addEventListener("click", () => hideTip());
document.addEventListener("keydown", (e) => { if (e.key === "Escape") hideTip(); });
el("mapbox").addEventListener("scroll", () => hideTip(), { passive: true });
window.addEventListener("scroll", () => { if (!pinned) hideTip(); }, { passive: true });

// ---------- time ----------
function buildTimes(p) {
  const set = new Set();
  const add = (v) => { const d = parseDate(v); if (d) set.add(d.getTime()); };
  add(p.seedDate);
  p.directions.forEach((d) => { add(d.opened); add(d.resolved); });
  return [...set].sort((a, b) => a - b).map((x) => new Date(x));
}
function renderTimeLabel(all) {
  if (!times.length) return;
  const counts = { hit: 0, killed: 0, open: 0, running: 0, mixed: 0 };
  all.forEach((n) => { if (counts[n.view] != null) counts[n.view]++; });
  const latest = tIndex === times.length - 1;
  const parts = [[counts.hit, "landed"], [counts.mixed, "mixed"], [counts.killed, "killed"], [counts.running, "running"], [counts.open, "open"]]
    .filter(([n]) => n).map(([n, w]) => `${n} ${w}`);
  el("whenout").innerHTML = `<b>${latest ? "Now" : esc(fmtDate(times[tIndex]))}</b> · ${parts.join(" · ")}`;
}
function stopPlay() { clearInterval(playTimer); playTimer = null; el("play").textContent = "▶ Replay"; }
el("when").addEventListener("input", (e) => { stopPlay(); tIndex = +e.target.value; hideTip(); draw(); });
el("play").addEventListener("click", () => {
  if (playTimer) return stopPlay();
  tIndex = 0; el("when").value = 0; draw();
  el("play").textContent = "❚❚ Pause";
  playTimer = setInterval(() => {
    if (tIndex >= times.length - 1) return stopPlay();
    tIndex++; el("when").value = tIndex; draw();
  }, 650);
});

// ---------- list view (the same tree, as an indented list; the default on phones) ----------
function renderList() {
  const root = buildTree(current);
  const rows = [];
  (function walk(n) {
    if (!n.isRoot) {
      const depth = Math.min(n.depth - 1, 4);
      const odds = [n.engine != null ? `engine ${Math.round(n.engine * 100)}%` : null, n.human != null ? `human ${Math.round(n.human * 100)}%` : null].filter(Boolean);
      const note = n.status === "killed" ? `<b>Why it died:</b> ${inline(n.diagnosis || "no diagnosis recorded yet")}` : n.status !== "open" && n.result ? inline(n.result) : "";
      rows.push(`<li class="${n.status}" style="margin-left:${depth * 18}px">${markSVG(n.status, 16)}
        <span class="t">${esc(n.title)}</span>${note ? `<span class="d">${note}</span>` : ""}
        <span class="o">${STATUS[n.status].word}${odds.length ? " · odds before data: " + odds.join(", ") : ""}</span></li>`);
    }
    n.children.forEach(walk);
  })(root);
  el("listview").innerHTML = `<ol class="mlist">${rows.join("")}</ol>`;
}
function setList(show) {
  el("listview").hidden = !show;
  el("listbtn").setAttribute("aria-expanded", String(show));
  el("listbtn").textContent = show ? "Hide the list" : "Show as a list";
}
el("listbtn").addEventListener("click", () => setList(el("listview").hidden));
// On a phone the list comes first and the drawing follows it.
if (window.matchMedia("(max-width: 700px)").matches) {
  setList(true);
  const lv = el("listview"), btn = el("listbtn").parentElement;
  el("mapbox").before(btn, lv);
}

// ---------- program switching ----------
function select(id) {
  stopPlay(); hideTip();
  current = programs.find((p) => p.id === id) || programs[0];
  document.querySelectorAll("#tabs button").forEach((b) => b.setAttribute("aria-selected", String(b.dataset.id === current.id)));
  el("seed").textContent = current.seed || "(no seed question recorded)";
  times = buildTimes(current);
  tIndex = Math.max(0, times.length - 1);
  const tb = el("timebar");
  tb.hidden = el("timenote").hidden = times.length < 3;
  el("when").max = Math.max(0, times.length - 1);
  el("when").value = tIndex;
  renderList();
  draw();
  history.replaceState(null, "", "#" + encodeURIComponent(current.id));
}

el("key").innerHTML = ["hit", "running", "mixed", "killed", "open"]
  .map((k) => `<span>${markSVG(k, 18)}<b>${STATUS[k].word}</b>&nbsp;<span class="muted">${KEY_TEXT[k]}</span></span>`).join("");

let lastW = window.innerWidth;
window.addEventListener("resize", () => { if (current && Math.abs(window.innerWidth - lastW) > 40) { lastW = window.innerWidth; hideTip(); draw(); } });

(async () => {
  const [bets, maps] = await Promise.all([loadBets(), loadMaps()]);
  programs = joinBets(maps, bets);
  if (!programs.length) {
    el("mapbox").innerHTML = `<div class="empty" style="margin:24px">No map files yet. The map is drawn from <code>map/&lt;program&gt;.json</code> in the engine repository; it will appear here once the first one is committed.</div>`;
    el("seed").textContent = "";
    return;
  }
  el("tabs").innerHTML = programs.map((p) => `<button role="tab" type="button" data-id="${esc(p.id)}">${esc(p.title)}</button>`).join("");
  el("tabs").hidden = programs.length < 2;
  el("tabs").querySelectorAll("button").forEach((b) => b.addEventListener("click", () => select(b.dataset.id)));
  await document.fonts.ready;
  select(decodeURIComponent(location.hash.slice(1)) || programs[0].id);
})();
