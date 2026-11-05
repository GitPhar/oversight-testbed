// The map: paths fan out from a seed question and collapse as bets land.
// Built from data/map/*.json joined with data/ledger/bets.jsonl and human-odds.jsonl. Plain SVG, no library.
// The drawing always opens fitted to the screen, with the replay bar inside the same frame, so the replay
// can be watched without scrolling. Scroll or pinch zooms, drag pans, Fit goes back.
import { header, esc, inline, STATUS, LEGEND_SENTENCE, markSVG, parseDate, fmtDate } from "./common.js";
import { loadBets, loadMaps, joinBets, loadHumanOdds, joinHumanOdds, engineOddsVisible } from "./data.js";

header();

const R = 7;                 // node radius
const LINE_H = 19;           // label line height
const FONT = 15;
const MAX_LINES = 2;
const COL_GAP = 46;          // horizontal room for the curves between columns
const SIB_GAP = 6;
const PAD = { l: 20, r: 24, t: 18, b: 18 };
const WRAPS = [64, 44, 34, 26];   // characters per label line; the layout that fits the frame best wins


const el = (id) => document.getElementById(id);
const SVGNS = "http://www.w3.org/2000/svg";
let programs = [], current = null, times = [], tIndex = 0, pinned = null, playTimer = null;
let L = null;                // current layout {all, W, H}
let view = null, fitted = true;
let suppressClick = false;

// ---------- text measuring ----------
const ctx = document.createElement("canvas").getContext("2d");
function measure(s, bold) {
  ctx.font = `${bold ? 700 : 400} ${FONT}px "Plain Digits", "Atkinson Hyperlegible", system-ui, sans-serif`;
  return ctx.measureText(s).width;
}
function wrap(text, width) {
  const words = String(text).split(/\s+/).filter(Boolean);
  const lines = [];
  let cur = "";
  for (const w of words) {
    if (!cur) cur = w;
    else if ((cur + " " + w).length <= width) cur += " " + w;
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
  const root = { id: "__seed", title: "Seed question", status: "seed", children: [], depth: 0, isRoot: true, opened: p.seedDate };
  const byId = new Map(p.directions.map((d) => [d.id, { ...d, children: [] }]));
  for (const n of byId.values()) {
    const par = n.parent != null && byId.has(String(n.parent)) ? byId.get(String(n.parent)) : root;
    par.children.push(n);
    n.parentNode = par;
  }
  const seen = new Set();   // depth, guarding against cycles in hand-edited data
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

function layout(root, width) {
  const all = [];
  (function walk(n) { all.push(n); n.children.forEach(walk); })(root);
  for (const n of all) {
    n.lines = n.isRoot ? ["Seed question"] : wrap(n.label || n.title, width);
    n.bold = n.isRoot || n.status === "hit";
    n.labelW = Math.max(...n.lines.map((l) => measure(l, n.bold)));
    n.labelH = n.lines.length * LINE_H;
  }
  const maxDepth = Math.max(...all.map((n) => n.depth));
  const colX = [PAD.l + R];
  for (let d = 0; d < maxDepth; d++) {
    const w = Math.max(...all.filter((n) => n.depth === d).map((n) => R + 10 + n.labelW + 8));
    colX.push(colX[d] + w + COL_GAP);
  }
  for (const n of all) n.x = colX[n.depth];
  const memo = new Map();
  const ownH = (n) => Math.max(n.labelH, 2 * R) + SIB_GAP;
  function subtreeH(n) {
    if (memo.has(n)) return memo.get(n);
    const h = n.children.length ? Math.max(n.children.reduce((a, c) => a + subtreeH(c), 0), ownH(n)) : ownH(n);
    memo.set(n, h);
    return h;
  }
  function place(n, top) {
    if (!n.children.length) { n.y = top + ownH(n) / 2; return; }
    const sum = n.children.reduce((a, c) => a + subtreeH(c), 0);
    let y = top + Math.max(0, (ownH(n) - sum) / 2);
    for (const c of n.children) { place(c, y); y += subtreeH(c); }
    n.y = (n.children[0].y + n.children[n.children.length - 1].y) / 2;
  }
  place(root, PAD.t);
  const H = subtreeH(root) + PAD.t + PAD.b;
  const W = Math.max(...all.map((n) => n.x + R + 10 + n.labelW)) + PAD.r;
  return { all, W, H };
}

// Picks the label width whose layout is drawn largest when fitted to the frame.
function bestLayout() {
  const box = el("mapbox");
  const bw = box.clientWidth, bh = box.clientHeight;
  let best = null;
  for (const w of WRAPS) {
    const root = buildTree(current);
    const lay = layout(root, w);
    lay.scale = Math.min(bw / lay.W, bh / lay.H);
    if (!best || lay.scale > best.scale + 0.01) best = lay;
  }
  return best;
}

// ---------- the view (a viewBox with the frame's aspect ratio, so screen and drawing map linearly) ----------
function boxSize() { const b = el("mapbox"); return { w: b.clientWidth, h: b.clientHeight }; }
function fitView() {
  const { w, h } = boxSize();
  const s = Math.min(w / L.W, h / L.H);
  const vw = w / s, vh = h / s;
  return { x: (L.W - vw) / 2, y: (L.H - vh) / 2, w: vw, h: vh };
}
function applyView() {
  const svg = el("mapbox").querySelector("svg");
  if (!svg || !view) return;
  svg.setAttribute("viewBox", `${view.x} ${view.y} ${view.w} ${view.h}`);
  const { w } = boxSize();
  const scale = w / view.w;                 // screen pixels per drawing unit
  el("zfit").setAttribute("aria-pressed", String(fitted));
  el("zin").disabled = scale >= 2.5;
  el("zout").disabled = fitted || view.w >= fitView().w * 1.001;
}
function zoomAt(factor, cx, cy) {
  const box = el("mapbox").getBoundingClientRect();
  const { w } = boxSize();
  const fit = fitView();
  const minW = w / 2.5, maxW = fit.w;       // between 2.5× and the whole map
  const nw = Math.min(maxW, Math.max(minW, view.w / factor));
  const f = nw / view.w;
  const px = (cx - box.left) / box.width, py = (cy - box.top) / box.height;
  const sx = view.x + px * view.w, sy = view.y + py * view.h;
  view = { x: sx - px * nw, y: sy - py * view.h * f, w: nw, h: view.h * f };
  fitted = Math.abs(nw - maxW) < 0.5;
  if (fitted) view = fit;
  clampView();
  applyView();
  hideTip();
}
function panBy(dxPx, dyPx) {
  const { w } = boxSize();
  const k = view.w / w;
  view = { ...view, x: view.x - dxPx * k, y: view.y - dyPx * k };
  fitted = false;
  clampView();
  applyView();
}
// Keeps at least a third of the frame on the drawing.
function clampView() {
  const mx = view.w * 0.66, my = view.h * 0.66;
  view.x = Math.min(Math.max(view.x, -mx), L.W - view.w + mx);
  view.y = Math.min(Math.max(view.y, -my), L.H - view.h + my);
}
function centreZoom(f) { const r = el("mapbox").getBoundingClientRect(); zoomAt(f, r.left + r.width / 2, r.top + r.height / 2); }

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
  hit: { w: 3, c: STATUS.hit.hex, o: 1, dash: null },
  running: { w: 2.5, c: "#6aaee8", o: 0.95, dash: null },
  mixed: { w: 2.5, c: "#a99cf0", o: 0.9, dash: null },
  killed: { w: 2, c: "#e47272", o: 0.55, dash: null },
  open: { w: 1.6, c: "#8a9099", o: 0.55, dash: "1 6" },
};
const TEXT = { seed: "#ffffff", hit: "#ffffff", running: "#ece9e2", mixed: "#ece9e2", killed: "#a9a59c", open: "#9b988f" };

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

// Lays the program out again (on a program switch or a resize) and refits.
function relayout() {
  if (!current) return;
  sizeFrame();
  L = bestLayout();
  view = fitView();
  fitted = true;
  paint();
}

function paint() {
  const box = el("mapbox");
  box.innerHTML = "";
  if (!current || !L) return;
  const { all, W, H } = L;
  const t = times.length ? times[tIndex] : null;
  const isLatest = !times.length || tIndex === times.length - 1;
  for (const n of all) {
    n.view = stateAt(n, isLatest ? null : t);
    if (n.view !== "hidden" && n.parentNode && n.parentNode.view === "hidden") n.view = "hidden";
    // what changed at this step of the replay, ringed so the eye finds it
    n.fresh = !isLatest && t && n.view !== "hidden" &&
      [n.opened, n.resolved].some((v) => { const d = parseDate(v); return d && d.getTime() === t.getTime(); });
  }

  const svg = s("svg", { width: "100%", height: "100%", preserveAspectRatio: "none", role: "img",
    "aria-label": `Map of ${current.title}: ${all.length - 1} directions` });
  const edges = s("g", {}, svg);
  const nodes = s("g", {}, svg);

  const order = { open: 0, killed: 1, mixed: 2, running: 3, hit: 4 };
  const visible = all.filter((n) => !n.isRoot && n.view !== "hidden").sort((a, b) => order[a.view] - order[b.view]);
  for (const n of visible) {
    const p = n.parentNode;
    const st = EDGE[n.view] || EDGE.open;
    const x1 = p.x + R + 10 + p.labelW + 6, y1 = p.y;
    const x2 = n.x - R - 5, y2 = n.y;
    const dx = Math.max(20, (x2 - x1) * 0.55);
    s("path", { d: `M${x1} ${y1}C${x1 + dx} ${y1} ${x2 - dx} ${y2} ${x2} ${y2}`, fill: "none",
      stroke: st.c, "stroke-width": st.w, "stroke-opacity": st.o, "stroke-dasharray": st.dash, "stroke-linecap": "round" }, edges);
  }

  for (const n of all) {
    if (n.view === "hidden") continue;
    const g = s("g", { class: "node" + (n.fresh ? " fresh" : ""), tabindex: 0, role: "button",
      "aria-label": n.isRoot ? `Seed question: ${current.seed}` : `${STATUS[n.view]?.word}: ${n.title}` }, nodes);
    g.__node = n;
    const top = n.y - n.labelH / 2;
    s("rect", { x: n.x - R - 6, y: Math.min(top, n.y - R) - 3, width: R * 2 + 16 + n.labelW, height: Math.max(n.labelH, 2 * R) + 6, fill: "transparent" }, g);
    if (n.fresh) s("circle", { class: "ring", cx: n.x, cy: n.y, r: R + 7, fill: "none", stroke: "#ffffff", "stroke-width": 2 }, g);
    s("circle", { class: "halo", cx: n.x, cy: n.y, r: R + 6, fill: "none", stroke: "transparent" }, g);
    drawMark(g, n.view, n.x, n.y);
    const tx = s("text", { x: n.x + R + 10, y: top + LINE_H * 0.74, fill: TEXT[n.view] || TEXT.open,
      "font-size": FONT, "font-weight": n.bold && n.view === n.status ? 700 : 400 }, g);
    n.lines.forEach((l, i) => { const ts = s("tspan", { x: n.x + R + 10, dy: i ? LINE_H : 0 }, tx); ts.textContent = l; });
  }
  box.append(svg);
  applyView();
  wireTips(svg);
  renderTimeLabel(all);
}

// The frame takes the rest of the window, so the drawing and the replay bar are both on screen.
function sizeFrame() {
  const f = el("mapframe");
  const top = f.getBoundingClientRect().top + window.scrollY;
  const phone = window.innerWidth <= 700;
  const h = Math.round(window.innerHeight - top - (phone ? 10 : 16));
  f.style.height = Math.max(phone ? 380 : 420, h) + "px";
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
  if (n.engine != null) {
    meta.push(engineOddsVisible(n)
      ? `Engine's odds before data: <b>${Math.round(n.engine * 100)}%</b>`
      : `Engine's odds: <b>hidden</b> until the human's are in (the cockpit)`);
  }
  meta.push(`Human's odds before data: <b>${n.human != null ? Math.round(n.human * 100) + "%" : "not recorded"}</b>`);
  if (n.cost && !(v === "open" && n.status === "open")) meta.push(`Cost: ${esc(n.cost)}`);
  if (n.resolved && v !== "open") meta.push(`Landed ${esc(fmtDate(parseDate(n.resolved)))}`);
  else if (n.opened) meta.push(`Opened ${esc(fmtDate(parseDate(n.opened)))}`);
  if (n.bet?.prereg) meta.push(`Pre-registered in <code>${esc(n.bet.prereg)}</code>`);
  if (n.raw?.moved_to) meta.push(`Carried into ${esc(n.raw.moved_to)}`);
  let body = "";
  if (v === "killed") body += `<div class="t-diag"><b>Why it died.</b> ${n.diagnosis ? inline(n.diagnosis) : "No diagnosis recorded yet."}</div>`;
  if (n.result && v !== "open") body += `<div style="margin-top:8px">${inline(n.result)}</div>`;
  if (v === "open" && n.status !== "open") body += `<div style="margin-top:8px" class="muted">Not yet bet on at this point in the replay.</div>`;
  if (v === "open" && n.status === "open" && n.raw?.question) body += `<div style="margin-top:6px">${esc(n.raw.question)}</div>`;
  if (v === "open" && n.status === "open") {
    const test = n.raw?.cheapest_test || n.test || "";
    body += `<div class="t-test"><b>Cheapest test:</b> ${test ? esc(test) : "not designed yet"}</div>` +
      `<div class="t-test"><b>Cost:</b> ${n.cost ? esc(n.cost) : "not estimated yet"}</div>`;
  }
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
    g.addEventListener("mouseenter", () => { if (!pinned && !drag) showTip(g); });
    g.addEventListener("mouseleave", () => { if (!pinned) hideTip(); });
    g.addEventListener("focus", () => showTip(g));
    g.addEventListener("blur", () => { if (!pinned) hideTip(); });
    g.addEventListener("click", (e) => {
      e.stopPropagation();
      if (suppressClick) return;
      if (pinned === g) hideTip(); else { pinned = g; showTip(g); }
    });
    g.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); pinned = g; showTip(g); } });
  });
}
document.addEventListener("click", () => hideTip());
document.addEventListener("keydown", (e) => { if (e.key === "Escape") hideTip(); });
window.addEventListener("scroll", () => { if (!pinned) hideTip(); }, { passive: true });

// ---------- zoom and pan ----------
const box = el("mapbox");
box.addEventListener("wheel", (e) => {
  if (!view) return;
  e.preventDefault();
  const k = e.ctrlKey ? 0.012 : 0.0022;    // a trackpad pinch arrives as ctrl+wheel with small deltas
  zoomAt(Math.exp(-e.deltaY * k), e.clientX, e.clientY);
}, { passive: false });

const pts = new Map();
let drag = null;
box.addEventListener("pointerdown", (e) => {
  if (!view || (e.pointerType === "mouse" && e.button !== 0)) return;
  pts.set(e.pointerId, { x: e.clientX, y: e.clientY });
  drag = { moved: 0, dist: pinchDist() };
  suppressClick = false;
});
window.addEventListener("pointermove", (e) => {
  if (!drag || !pts.has(e.pointerId)) return;
  const prev = pts.get(e.pointerId);
  const dx = e.clientX - prev.x, dy = e.clientY - prev.y;
  pts.set(e.pointerId, { x: e.clientX, y: e.clientY });
  if (pts.size >= 2) {
    const d = pinchDist(), [a, b] = [...pts.values()];
    if (drag.dist) zoomAt(d / drag.dist, (a.x + b.x) / 2, (a.y + b.y) / 2);
    drag.dist = d;
    drag.moved += 10;
  } else {
    drag.moved += Math.abs(dx) + Math.abs(dy);
    if (drag.moved > 4) { panBy(dx, dy); box.classList.add("dragging"); hideTip(); }
  }
});
function endPointer(e) {
  if (!pts.has(e.pointerId)) return;
  pts.delete(e.pointerId);
  if (pts.size === 0 && drag) {
    suppressClick = drag.moved > 4;
    setTimeout(() => { suppressClick = false; }, 0);
    drag = null;
    box.classList.remove("dragging");
  } else if (drag) drag.dist = pinchDist();
}
window.addEventListener("pointerup", endPointer);
window.addEventListener("pointercancel", endPointer);
function pinchDist() {
  if (pts.size < 2) return 0;
  const [a, b] = [...pts.values()];
  return Math.hypot(a.x - b.x, a.y - b.y);
}
box.addEventListener("keydown", (e) => {
  if (!view || e.target !== box) return;
  const step = 60;
  const keys = { "+": () => centreZoom(1.25), "=": () => centreZoom(1.25), "-": () => centreZoom(0.8), "0": () => { view = fitView(); fitted = true; applyView(); },
    ArrowLeft: () => panBy(step, 0), ArrowRight: () => panBy(-step, 0), ArrowUp: () => panBy(0, step), ArrowDown: () => panBy(0, -step) };
  if (keys[e.key]) { e.preventDefault(); keys[e.key](); }
});
el("zin").addEventListener("click", (e) => { e.stopPropagation(); centreZoom(1.4); });
el("zout").addEventListener("click", (e) => { e.stopPropagation(); centreZoom(1 / 1.4); });
el("zfit").addEventListener("click", (e) => { e.stopPropagation(); hideTip(); view = fitView(); fitted = true; applyView(); });

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
el("when").addEventListener("input", (e) => { stopPlay(); tIndex = +e.target.value; hideTip(); paint(); });
el("play").addEventListener("click", (e) => {
  e.stopPropagation();
  if (playTimer) return stopPlay();
  hideTip();
  if (tIndex >= times.length - 1) { tIndex = 0; el("when").value = 0; paint(); }
  el("play").textContent = "❚❚ Pause";
  playTimer = setInterval(() => {
    if (tIndex >= times.length - 1) return stopPlay();
    tIndex++; el("when").value = tIndex; paint();
  }, 700);
});

// ---------- list view (the same tree, as an indented list; shown under the drawing on phones) ----------
function renderList() {
  const root = buildTree(current);
  const rows = [];
  (function walk(n) {
    if (!n.isRoot) {
      const depth = Math.min(n.depth - 1, 4);
      const odds = [n.engine != null && engineOddsVisible(n) ? `engine ${Math.round(n.engine * 100)}%` : null,
        n.human != null ? `human ${Math.round(n.human * 100)}%` : null].filter(Boolean);
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
if (window.matchMedia("(max-width: 700px)").matches) setList(true);

// "Program 2: Other Minds" -> the name hides on phones, the number stays
function tabLabel(t) {
  const m = String(t).match(/^(Program\s*\d+)(:\s*.*)$/i);
  return m ? `<span>${esc(m[1])}</span><span class="pt">${esc(m[2])}</span>` : esc(t);
}

// ---------- program switching ----------
function select(id) {
  stopPlay(); hideTip();
  current = programs.find((p) => p.id === id) || programs[0];
  document.querySelectorAll("#tabs button").forEach((b) => b.setAttribute("aria-selected", String(b.dataset.id === current.id)));
  el("seed").textContent = current.seed || "(no seed question recorded)";
  el("seed").title = current.seed || "";
  times = buildTimes(current);
  tIndex = Math.max(0, times.length - 1);
  el("timebar").hidden = times.length < 3;
  el("noreplay").hidden = times.length >= 3;
  el("when").max = Math.max(0, times.length - 1);
  el("when").value = tIndex;
  renderList();
  relayout();
  history.replaceState(null, "", "#" + encodeURIComponent(current.id));
}

el("key").innerHTML = ["hit", "running", "mixed", "killed", "open"]
  .map((k) => `<span>${markSVG(k, 16)}<b>${STATUS[k].word}</b></span>`).join("");
el("legendline").innerHTML = LEGEND_SENTENCE;

let lastW = window.innerWidth, lastH = window.innerHeight;
window.addEventListener("resize", () => {
  if (!current) return;
  if (Math.abs(window.innerWidth - lastW) > 30 || Math.abs(window.innerHeight - lastH) > 80) {
    lastW = window.innerWidth; lastH = window.innerHeight; hideTip(); relayout();
  }
});

(async () => {
  const [bets, maps, odds] = await Promise.all([loadBets(), loadMaps(), loadHumanOdds()]);
  programs = joinHumanOdds(joinBets(maps, bets), odds);
  if (!programs.length) {
    el("mapbox").innerHTML = `<div class="empty" style="margin:24px">No map files yet. The map is drawn from <code>map/&lt;program&gt;.json</code> in the engine repository; it will appear here once the first one is committed.</div>`;
    el("seed").textContent = "";
    return;
  }
  el("tabs").innerHTML = programs.map((p) => `<button role="tab" type="button" data-id="${esc(p.id)}" title="${esc(p.title)}">${tabLabel(p.title)}</button>`).join("");
  el("tabs").hidden = programs.length < 2;
  el("tabs").querySelectorAll("button").forEach((b) => b.addEventListener("click", () => select(b.dataset.id)));
  await document.fonts.ready;
  select(decodeURIComponent(location.hash.slice(1)) || programs[0].id);
})();
