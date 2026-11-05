// The replay: the whole project on one timeline, every program at once.
// Each bet appears in its program's row at its pre-registration time, open, and turns green (landed), red (killed)
// or grey (mixed or unsettled) at its result time. The human's steers appear as gold marks with their sentence.
// The engine's Brier score ticks in the corner as scored bets settle. Everything is read from files:
// ledger/bets.jsonl, ledger/steers.jsonl, ledger/human-odds.jsonl, map/*.json (seed dates, and program 1's
// first-day tests from before the ledger), and data/commit-times.json (git commit times, written by assemble.sh).
import { header, esc, inline, parseDate, fmtDate, programTitle, DATA, getJSON, STATUS } from "./common.js";
import { loadBets, loadMaps, loadSteers, loadHumanOdds, joinBets } from "./data.js";

header();

const el = (id) => document.getElementById(id);
const SVGNS = "http://www.w3.org/2000/svg";
const COL = { open: "#ece9e2", hit: STATUS.hit.hex, killed: STATUS.killed.hex, mixed: "#9aa0a8", gold: "#f2c14e", seed: "#ece9e2" };
const WORD = { open: "Pre-registered, no result yet", hit: "Landed", killed: "Killed", mixed: "Mixed or unsettled" };
const ACTION = {
  choose_seed: "chose a seed question", set_rule: "set a rule", add_question: "added a question", veto: "vetoed a direction",
  architecture: "decided how the system works", budget: "set a budget", set_frame: "set the frame",
  human_odds: "gave odds of his own, before seeing the engine's",
};
const MIN = 60e3, HOUR = 60 * MIN;
const CAP = 20 * MIN;          // a quiet stretch longer than this is squeezed (and marked)
const EVP = 11 * MIN;          // each moment something happened gets this much extra room, so busy hours spread out
const DURATION = 36e3;         // one full play, not counting the pauses on steers
const HOLD = 1600;             // pause on each steer so its sentence can be read

// ---------- time ----------
// The ledger's times are America/Denver wall-clock; "now" is read in the same zone, whatever the viewer's zone.
function denverNow() {
  const p = Object.fromEntries(new Intl.DateTimeFormat("en-US", { timeZone: "America/Denver", year: "numeric", month: "2-digit",
    day: "2-digit", hour: "2-digit", minute: "2-digit", hourCycle: "h23" }).formatToParts(new Date()).map((x) => [x.type, x.value]));
  return new Date(+p.year, +p.month - 1, +p.day, +p.hour, +p.minute);
}
const hasClock = (s) => /\d{1,2}:\d{2}/.test(String(s || ""));

// A steer's time as the ledger wrote it: "16:55", "~07:00", "before 14:13", "evening", or nothing.
// Words are placed at a stated hour and the card says so; nothing is invented beyond that.
function steerTime(s) {
  if (hasClock(s.recorded)) return { t: parseDate(s.recorded), approx: false, said: s.time || "" };
  const day = parseDate(s.date);
  if (!day) return null;
  const raw = String(s.time ?? "").trim(), low = raw.toLowerCase();
  const m = low.match(/(\d{1,2}):(\d{2})/);
  let h = 12, mi = 0, approx = true;
  if (m) { h = +m[1]; mi = +m[2]; approx = /~|before|after|about/.test(low); if (/before/.test(low)) mi -= 1; }
  else if (/morning/.test(low)) h = 8;
  else if (/afternoon/.test(low)) h = 15;
  else if (/evening/.test(low)) h = 19;
  else if (/night/.test(low)) { h = 22; mi = 30; }
  return { t: new Date(day.getFullYear(), day.getMonth(), day.getDate(), h, mi), approx, said: raw || "no time recorded" };
}

// ---------- state ----------
let lanes = [], items = [], steers = [], events = [], scoredAll = [], oddsLines = [];
let axis = null, L = null, pos = 1, playing = false, holdUntil = 0, lastTs = 0, lastFeedN = -1, lastSteerId = null;
let commitTimes = {};
const ct = (h) => (h && commitTimes[h] ? parseDate(commitTimes[h]) : null);

function betItem(b) {
  const r = b.raw;
  const start = hasClock(r.prereg_time) ? parseDate(r.prereg_time) : ct(r.prereg_commit) || parseDate(r.prereg_time);
  if (!start) return null;
  const final = b.status === "running" || b.status === "open" ? "open" : b.status;
  let end = null, endHow = "";
  if (final !== "open") {
    if (hasClock(r.result_time)) { end = parseDate(r.result_time); endHow = "its result time"; }
    else if (ct(r.result_commit)) { end = ct(r.result_commit); endHow = "the time of its result commit"; }
    else if (r.verdict === "withdrawn" && ct(r.design_review?.commit)) { end = ct(r.design_review.commit); endHow = "the time of the design review that withdrew it"; }
    else if (ct(r.audit_commit)) { end = ct(r.audit_commit); endHow = "the time of its audit commit"; }
    else { end = start; endHow = "unknown: no landing time recorded, so it is shown settling when it was placed"; }
    if (end < start) end = start;
  }
  const oc = r.outcome === 1 || r.outcome === 0 ? r.outcome : null;
  const scored = r.scored === true && !r.secondary_of && b.engine != null && oc != null;   // rule 15: one scored bet per run
  return { kind: "bet", id: b.id, program: b.program, title: b.title, start, end, endHow, final, b,
    scored, engine: b.engine, human: b.human, outcome: oc };
}

function build(bets, maps, steerRows, odds) {
  joinBets(maps, bets);
  lanes = maps.map((p) => ({ id: p.id, title: p.title, seed: parseDate(p.seedDate), seedQ: p.seed, items: [] }));
  const lane = (id) => lanes.find((l) => l.id === id) || (lanes.push({ id, title: programTitle(id, maps), seed: null, items: [] }), lanes[lanes.length - 1]);
  items = bets.map(betItem).filter(Boolean);
  // Program 1's first day ran before the ledger began; its tests are on its map with their own times.
  const firstLedger = Math.min(...items.map((i) => +i.start));
  for (const p of maps) for (const d of p.directions) {
    if (d.bet || !["hit", "killed", "mixed"].includes(d.status)) continue;
    const o = parseDate(d.opened), e = parseDate(d.resolved);
    if (!o || !e || !(e > o) || +e > firstLedger) continue;
    items.push({ kind: "record", id: `${p.id}:${d.id}`, program: p.id, title: d.title, start: o, end: e, final: d.status,
      endHow: "its time on the program's map", result: d.result, diagnosis: d.diagnosis, scored: false });
  }
  for (const it of items) lane(it.program).items.push(it);
  const n = (l) => +(String(l.title).match(/program\s*(\d+)/i)?.[1] || 99);
  lanes.sort((a, b) => n(a) - n(b));

  // Steers, and the human's odds (one gold mark per save; a steer row for the same save carries it).
  oddsLines = odds.map((o) => ({ ...o, t: parseDate(o.recorded) })).filter((o) => o.t);
  steers = steerRows.map((s) => { const st = steerTime(s); return st && { kind: "steer", id: s.id, s, ...st, text: s.words || s.reason || "" }; })
    .filter(Boolean);
  const batches = new Map();
  for (const o of oddsLines) { const k = +o.t; if (!batches.has(k)) batches.set(k, []); batches.get(k).push(o); }
  for (const [k, lines] of batches) {
    const own = steers.find((s) => s.s.action === "human_odds" && +s.t === k);
    if (own) own.lines = lines;
    else steers.push({ kind: "steer", id: `odds-${k}`, s: { action: "human_odds" }, t: new Date(k), approx: false, said: "",
      text: `Odds on ${lines.length} direction${lines.length === 1 ? "" : "s"}, saved from the cockpit.`, lines });
  }
  steers.sort((a, b) => a.t - b.t || String(a.id).localeCompare(String(b.id), undefined, { numeric: true }));
  scoredAll = items.filter((i) => i.scored).sort((a, b) => a.end - b.end);

  // The feed: every moment, in order.
  events = [];
  for (const l of lanes) if (l.seed) events.push({ t: l.seed, type: "seed", lane: l });
  for (const it of items) {
    events.push({ t: it.start, type: "placed", it });
    if (it.end) events.push({ t: it.end, type: "settled", it });
  }
  for (const s of steers) events.push({ t: s.t, type: "steer", s });
  const pr = { seed: 0, steer: 1, placed: 2, settled: 3 };
  events.sort((a, b) => a.t - b.t || pr[a.type] - pr[b.type]);
}

// ---------- the time axis: real time, with long quiet stretches squeezed and marked ----------
function buildAxis() {
  const now = denverNow();
  const pts = [...events.map((e) => +e.t), ...items.filter((i) => i.final === "open").map(() => +now)];
  const t0 = Math.min(...pts) - 30 * MIN;
  const tEnd = Math.max(+now, Math.max(...pts) + 10 * MIN);
  const ts = [...new Set([t0, ...pts, tEnd])].sort((a, b) => a - b);
  const segs = [];
  let d = 0;
  for (let i = 0; i < ts.length - 1; i++) {
    const a = ts[i], b = ts[i + 1], gap = b - a;
    const len = gap <= CAP ? gap : CAP * (1 + 0.28 * Math.log2(gap / CAP));
    // the room before each moment (EVP) is a flat step: time inside it maps to the moment itself
    segs.push({ t0: a, t1: a, d0: d, d1: d + EVP, squeezed: false });
    d += EVP;
    segs.push({ t0: a, t1: b, d0: d, d1: d + len, squeezed: gap > 2 * HOUR });
    d += len;
  }
  return { segs, D: d, t0, tEnd, now };
}
function dOf(t) {
  const x = +t, s = axis.segs;
  if (x <= axis.t0) return 0;
  if (x >= axis.tEnd) return axis.D;
  let lo = 0, hi = s.length - 1;
  while (lo < hi) { const m = (lo + hi) >> 1; if (s[m].t1 < x) lo = m + 1; else hi = m; }
  const g = s[lo];
  return g.t1 === g.t0 ? g.d0 : g.d0 + ((x - g.t0) / (g.t1 - g.t0)) * (g.d1 - g.d0);
}
function tOf(d) {
  const s = axis.segs;
  if (d <= 0) return new Date(axis.t0);
  if (d >= axis.D) return new Date(axis.tEnd);
  let lo = 0, hi = s.length - 1;
  while (lo < hi) { const m = (lo + hi) >> 1; if (s[m].d1 < d) lo = m + 1; else hi = m; }
  const g = s[lo];
  return new Date(g.d1 === g.d0 ? g.t0 : g.t0 + ((d - g.d0) / (g.d1 - g.d0)) * (g.t1 - g.t0));
}

// ---------- layout ----------
function sv(tag, attrs, parent) {
  const e = document.createElementNS(SVGNS, tag);
  for (const [k, v] of Object.entries(attrs)) if (v != null) e.setAttribute(k, v);
  if (parent) parent.append(e);
  return e;
}
function layout() {
  const box = el("draw");
  const W = Math.max(300, box.clientWidth);
  const phone = W < 700;
  const r = phone ? 4.2 : 5.2;
  const left = phone ? 10 : 150, right = phone ? 12 : 18;
  const x = (t) => left + (dOf(t) / axis.D) * (W - left - right);
  const rowH = 2 * r + 2.2, AX = phone ? 30 : 30, labelH = phone ? 16 : 0, lanePad = phone ? 5 : 4.5;
  const stack = (list, x0, x1) => {
    const rows = [];
    for (const it of [...list].sort((a, b) => x0(a) - x0(b))) {
      let k = rows.findIndex((end) => end + 2 <= x0(it) - r);
      if (k < 0) { k = rows.length; rows.push(0); }
      rows[k] = Math.max(x0(it) + r, x1(it));
      it.row = k;
    }
    return Math.max(1, rows.length);
  };
  let y = AX;
  const rowsS = stack(steers, (s) => x(s.t), (s) => x(s.t) + r);
  const minH = phone ? rowH : 31;   // room for a two-line label on a desktop
  const laneH = (n) => Math.max(n * rowH, minH);
  const steerLane = { y0: y + labelH + lanePad, rows: rowsS };
  y += labelH + laneH(rowsS) + 2 * lanePad;
  for (const l of lanes) {
    const n = stack(l.items, (i) => x(i.start), (i) => x(i.end || axis.now));
    l.y0 = y + labelH + lanePad; l.rows = n;
    y += labelH + laneH(n) + 2 * lanePad;
  }
  L = { W, H: y + 6, phone, r, left, right, x, rowH, AX, labelH, lanePad, steerLane, laneH };
}

// ---------- drawing ----------
function markInner(state, r, small) {
  const R = small ? r * 0.78 : r, c = COL[state];
  switch (state) {
    case "hit": return `<circle r="${R + 0.6}" fill="${c}" stroke="#191c20" stroke-width="1.6"/>`;
    case "killed": { const a = R * 0.9; return `<circle r="${R + 1}" fill="#191c20"/><path d="M${-a} ${-a}L${a} ${a}M${a} ${-a}L${-a} ${a}" stroke="${c}" stroke-width="2.6" stroke-linecap="round"/>`; }
    case "mixed": return `<circle r="${R}" fill="#191c20" stroke="${c}" stroke-width="2"/><path d="M0 ${-R}A${R} ${R} 0 0 1 0 ${R}Z" fill="${c}"/>`;
    case "open": return `<circle r="${R - 0.4}" fill="#191c20" stroke="${c}" stroke-width="2"/>`;
    case "gold": { const a = R + 1.4; return `<path d="M0 ${-a}L${a} 0L0 ${a}L${-a} 0Z" fill="${c}" stroke="#191c20" stroke-width="1.4"/>`; }
    default: return "";
  }
}
function draw() {
  layout();
  const { W, H, phone, r, left, x, rowH, AX, labelH, lanePad, steerLane } = L;
  const box = el("draw");
  box.innerHTML = "";
  const svg = sv("svg", { width: W, height: H, viewBox: `0 0 ${W} ${H}`, role: "img",
    "aria-label": `Timeline of ${items.length} tests in ${lanes.length} programs and ${steers.length} human steers` });
  const g0 = sv("g", {}, svg);

  // days and squeezed stretches
  const d0 = new Date(axis.t0);
  for (let day = new Date(d0.getFullYear(), d0.getMonth(), d0.getDate() + 1); +day < axis.tEnd; day = new Date(day.getFullYear(), day.getMonth(), day.getDate() + 1)) {
    const xx = x(day);
    sv("line", { x1: xx, x2: xx, y1: AX - 10, y2: H, stroke: "#3a414a", "stroke-width": 1 }, g0);
    const near = W - xx < (phone ? 64 : 84);   // keep the last day's label inside the frame
    const tx = sv("text", { x: near ? xx - 4 : xx + 4, y: phone ? 12 : 14, fill: "#bcb8ae", "font-size": phone ? 11 : 13, "font-weight": 700,
      "text-anchor": near ? "end" : "start" }, g0);
    tx.textContent = fmtDate(day, false);
  }
  const first = sv("text", { x: phone ? left : left, y: phone ? 12 : 14, fill: "#8d8a82", "font-size": phone ? 11 : 13 }, g0);
  first.textContent = fmtDate(new Date(axis.t0), false);
  // keep the first label clear of the first midnight's label
  const firstMid = new Date(d0.getFullYear(), d0.getMonth(), d0.getDate() + 1);
  if (x(firstMid) - left < (phone ? 70 : 90)) first.remove();
  for (const s of axis.segs) if (s.squeezed) {
    const xa = left + (s.d0 / axis.D) * (W - left - L.right), xb = left + (s.d1 / axis.D) * (W - left - L.right);
    const xm = (xa + xb) / 2, yy = AX - 6;
    sv("rect", { x: xa, y: AX - 2, width: Math.max(1, xb - xa), height: H - AX, fill: "#ffffff", "fill-opacity": 0.025 }, g0);
    sv("path", { d: `M${xm - 5} ${yy + 4}l3 -8M${xm + 1} ${yy + 4}l3 -8`, stroke: "#8d8a82", "stroke-width": 1.4 }, g0);
    if (xb - xa > (phone ? 34 : 46)) {
      const t = sv("text", { x: xm, y: yy + 16, fill: "#8d8a82", "font-size": phone ? 10 : 11.5, "text-anchor": "middle" }, g0);
      t.textContent = `${Math.round((s.t1 - s.t0) / HOUR)} h quiet`;
    }
  }

  // lanes
  const laneBox = (label, sub, y0, rows, colour, id) => {
    const top = y0 - labelH - lanePad;
    sv("line", { x1: 0, x2: W, y1: top, y2: top, stroke: "#2c3138", "stroke-width": 1 }, g0);
    const tx = sv("text", { x: phone ? 10 : 12, y: phone ? top + 13 : y0 + rowH / 2 + 1 - (sub ? 8 : -4), fill: colour,
      "font-size": phone ? 12 : 14.5, "font-weight": 700, "data-lane": id }, g0);
    tx.textContent = label;
    if (sub) {
      const ts = sv("tspan", phone ? { dx: 6, fill: "#8d8a82", "font-weight": 400 } : { x: 12, dy: 18, fill: "#8d8a82", "font-weight": 400, "font-size": 13.5 }, tx);
      ts.textContent = sub;
    }
    return { top, tx };
  };
  laneBox(phone ? "Sean, the human" : "Sean", phone ? "" : "the human's steers", steerLane.y0, steerLane.rows, COL.gold, "sean");
  for (const l of lanes) {
    const m = String(l.title).match(/^Program\s*(\d+):\s*(.*)$/i);
    const label = m ? (phone ? `${m[1]} · ${m[2]}` : `Program ${m[1]}`) : l.title;
    const sub = m && !phone ? m[2] : "";
    const sub2 = sub.length > 19 ? sub.slice(0, 18).replace(/\s+\S*$/, "") + "…" : sub;
    l.labelEl = laneBox(label, sub2, l.y0, l.rows, "#ece9e2", l.id).tx;
    if (l.seed) {
      // the seed sits just left of any first marks that opened with it, so it is not hidden under them
      const xs = x(l.seed), crowd = l.items.some((i) => Math.abs(x(i.start) - xs) < 2 * r && i.row === 0);
      l.seedEl = sv("circle", { cx: crowd ? xs - 2 * r - 1 : xs, cy: l.y0 + rowH / 2, r: r * 0.6, fill: COL.seed }, g0);
    }
  }

  // marks
  const gTails = sv("g", {}, svg), gMarks = sv("g", {}, svg);
  for (const l of lanes) for (const it of l.items) {
    it.cy = l.y0 + it.row * rowH + rowH / 2;
    it.x0 = x(it.start);
    it.tail = sv("line", { x1: it.x0, x2: it.x0, y1: it.cy, y2: it.cy, stroke: "#bcb8ae", "stroke-width": phone ? 1.4 : 1.8, "stroke-opacity": 0.55, "stroke-linecap": "round" }, gTails);
    it.g = sv("g", { transform: `translate(${it.x0} ${it.cy})`, class: "rp-m", tabindex: 0, role: "button" }, gMarks);
    it.g.__it = it;
    it.cur = null;
  }
  for (const s of steers) {
    s.cy = steerLane.y0 + s.row * rowH + rowH / 2;
    s.g = sv("g", { transform: `translate(${x(s.t)} ${s.cy})`, class: "rp-m", tabindex: 0, role: "button" }, gMarks);
    s.g.innerHTML = markInner("gold", r);
    s.g.__it = s;
  }
  L.head = sv("line", { x1: 0, x2: 0, y1: AX - 12, y2: H, stroke: "#ffffff", "stroke-width": 1.6, "stroke-opacity": 0.9 }, svg);
  L.shade = sv("rect", { x: 0, y: AX - 2, width: 0, height: H - AX, fill: "#121417", "fill-opacity": 0.35, "pointer-events": "none" }, svg);
  box.append(svg);
  wireTips(svg);
  lastFeedN = -1; lastSteerId = null;
  paint();
}

// ---------- one moment ----------
const brier = (list, k) => list.length ? list.reduce((a, i) => a + (i[k] - i.outcome) ** 2, 0) / list.length : null;
function paint() {
  const t = tOf(pos * axis.D), tt = +t;
  const atNow = pos >= 0.9995;
  const { r, x } = L;
  const counts = { placed: 0, hit: 0, killed: 0, mixed: 0, open: 0, record: 0 };
  for (const l of lanes) {
    const started = !l.seed || +l.seed <= tt;
    l.labelEl.setAttribute("fill-opacity", started ? 1 : 0.4);
    if (l.seedEl) l.seedEl.setAttribute("visibility", started ? "visible" : "hidden");
    for (const it of l.items) {
      const state = tt < +it.start ? "hidden" : it.end && tt >= +it.end ? it.final : "open";
      if (state !== "hidden" && it.kind === "bet") { counts.placed++; counts[state]++; }
      if (state !== "hidden" && it.kind === "record") counts.record++;
      if (state !== it.cur) {
        it.g.innerHTML = state === "hidden" ? "" : markInner(state, r, it.kind === "record");
        it.g.setAttribute("aria-label", state === "hidden" ? "" : `${WORD[state]}: ${it.title}`);
        if (playing && it.cur != null && state !== "hidden") { it.g.classList.remove("fresh"); it.g.getBoundingClientRect(); it.g.classList.add("fresh"); }
        it.cur = state;
      }
      if (state === "hidden") it.tail.setAttribute("visibility", "hidden");
      else {
        const xe = x(new Date(Math.min(tt, +(it.end || axis.now))));
        it.tail.setAttribute("visibility", "visible");
        it.tail.setAttribute("x2", Math.max(it.x0, xe));
        it.tail.setAttribute("stroke", state === "open" ? "#bcb8ae" : COL[state]);
      }
    }
  }
  for (const s of steers) s.g.setAttribute("visibility", +s.t <= tt ? "visible" : "hidden");
  const xh = x(t);
  L.head.setAttribute("x1", xh); L.head.setAttribute("x2", xh);
  L.head.setAttribute("visibility", atNow ? "hidden" : "visible");
  L.shade.setAttribute("x", xh); L.shade.setAttribute("width", Math.max(0, L.W - xh));

  // clock, counts, score
  el("clock").textContent = atNow ? `Now · ${fmtDate(axis.now)}` : fmtDate(t);
  el("counts").textContent = counts.placed
    ? ` ${counts.placed} bet${counts.placed === 1 ? "" : "s"} placed · ${counts.hit} landed · ${counts.killed} killed · ${counts.mixed} mixed · ${counts.open} waiting for a result`
    : counts.record ? ` no ledger bets yet; ${counts.record} of program 1's first tests, from its own record` : " nothing placed yet";
  const sc = scoredAll.filter((i) => +i.end <= tt);
  const eb = brier(sc, "engine");
  const hs = sc.filter((i) => i.human != null), hb = brier(hs, "human");
  const given = oddsLines.filter((o) => +o.t <= tt).length;
  el("score").innerHTML = `<div class="rp-sc"><span class="rp-sl">Engine's score</span><b class="rp-sv">${eb == null ? "—" : eb.toFixed(3)}</b>
      <span class="rp-sn">${sc.length ? `on ${sc.length} scored bet${sc.length === 1 ? "" : "s"}; a coin scores 0.250, lower is better` : "no scored bet has settled yet"}</span></div>
    <div class="rp-sc rp-human"><span class="rp-sl">Sean's score</span><b class="rp-sv">${hb == null ? "—" : hb.toFixed(3)}</b>
      <span class="rp-sn">${hs.length ? `on ${hs.length} scored bet${hs.length === 1 ? "" : "s"}` : given ? `${given} odds given; none has settled yet` : "no odds given yet"}</span></div>`;
  el("when").value = Math.round(pos * 1000);

  // the latest steer, in gold, inside the frame
  const last = [...steers].reverse().find((s) => +s.t <= tt);
  if ((last?.id || null) !== lastSteerId) {
    lastSteerId = last?.id || null;
    el("steer").innerHTML = last ? steerLine(last) : `<span class="muted">No steer yet. Sean's first comes at ${esc(fmtDate(steers[0]?.t))}.</span>`;
    el("steer").classList.toggle("lit", !!last && playing);
  }

  // feed
  const past = events.filter((e) => +e.t <= tt);
  if (past.length !== lastFeedN) {
    lastFeedN = past.length;
    el("feed").innerHTML = past.slice(-10).reverse().map(feedItem).join("") ||
      `<li class="muted">Nothing yet. The first event is at ${esc(fmtDate(events[0]?.t))}.</li>`;
  }
}

function when(s) {
  return `${esc(fmtDate(s.t))}${s.approx ? ` <span class="muted">(the ledger says “${esc(s.said)}”)</span>` : ""}`;
}
function steerLine(s, withLines) {
  const lines = s.lines && withLines ? ` <span class="rp-odds">${s.lines.map((o) => `${esc(o.direction)} ${Math.round(o.human_odds * 100)}%`).join(" · ")}</span>` : "";
  return `<span class="rp-who">${markInnerSvg("gold")} Sean · ${when(s)} · ${esc(ACTION[s.s.action] || s.s.action || "steered")}</span>
    <span class="rp-said">${inline(s.text)}</span>${lines}`;
}
function markInnerSvg(state, small) {
  return `<svg width="16" height="16" viewBox="-8 -8 16 16" aria-hidden="true">${markInner(state, 5.6, small)}</svg>`;
}
function feedItem(e) {
  if (e.type === "steer") return `<li class="rp-f gold">${steerLine(e.s, true)}</li>`;
  if (e.type === "seed") return `<li class="rp-f"><span class="rp-ft">${esc(fmtDate(e.t))} · ${esc(e.lane.title)} opened</span>
    <span class="rp-fx">Seed question: ${esc(e.lane.seedQ || "")}</span></li>`;
  const it = e.it, prog = esc(programTitle(it.program, lanes.map((l) => ({ id: l.id, title: l.title }))));
  const tag = it.kind === "record" ? " · from program 1's record, before the ledger began" : "";
  if (e.type === "placed") return `<li class="rp-f"><span class="rp-ft">${markInnerSvg("open", it.kind === "record")} ${esc(fmtDate(e.t))} · ${prog} · pre-registered${tag}</span>
    <span class="rp-fx">${esc(it.title)}</span></li>`;
  const res = it.kind === "bet" ? it.b.result : it.result;
  const short = res ? String(res).replace(/\s+/g, " ") : "";
  return `<li class="rp-f"><span class="rp-ft">${markInnerSvg(it.final, it.kind === "record")} ${esc(fmtDate(e.t))} · ${prog} · <b style="color:${COL[it.final]}">${esc(WORD[it.final])}</b>${tag}</span>
    <span class="rp-fx">${esc(it.title)}</span>${short ? `<span class="rp-fr">${inline(short.length > 260 ? short.slice(0, 257).replace(/\s+\S*$/, "") + " …" : short)}</span>` : ""}</li>`;
}

// ---------- tooltips ----------
let tip, pinned = null;
function tipHTML(it) {
  if (it.kind === "steer") return `<div class="t-status" style="color:${COL.gold}">The human's steer</div><div class="t-title">${esc(ACTION[it.s.action] || it.s.action)}</div>
    <div>${inline(it.text)}</div><div class="t-meta">${when(it)}${it.s.value ? `<br>Judged so far: <b>${esc(it.s.value)}</b>` : ""}</div>`;
  const state = it.cur === "hidden" || !it.cur ? it.final : it.cur;
  const meta = [`Pre-registered ${esc(fmtDate(it.start))}`];
  if (it.end && state !== "open") meta.push(`Result ${esc(fmtDate(it.end))}${/result time/.test(it.endHow) ? "" : ` <span class="muted">(${esc(it.endHow)})</span>`}`);
  if (state === "open") meta.push("No result yet at this point");
  if (it.kind === "bet" && state !== "open" && it.engine != null) meta.push(`Engine's odds before data: <b>${Math.round(it.engine * 100)}%</b>${it.scored ? "" : " (not scored)"}`);
  if (it.kind === "bet") meta.push(`Sean's odds: <b>${it.human != null ? Math.round(it.human * 100) + "%" : "none on this bet"}</b>`);
  if (it.kind === "record") meta.push("From program 1's record, before the ledger began; no odds were stated");
  const res = it.kind === "bet" ? it.b.result : it.result;
  const short = res && state !== "open" ? String(res) : "";
  return `<div class="t-status">${markInnerSvg(state, it.kind === "record")} ${esc(WORD[state])}</div>
    <div class="t-title">${esc(it.title)}</div><div class="muted" style="font-size:14px">${esc(programTitle(it.program, lanes.map((l) => ({ id: l.id, title: l.title }))))}${it.kind === "bet" ? ` · ${esc(it.id)}` : ""}</div>
    ${short ? `<div style="margin-top:6px">${inline(short.length > 420 ? short.slice(0, 417).replace(/\s+\S*$/, "") + " …" : short)}</div>` : ""}
    <div class="t-meta">${meta.join("<br>")}</div>`;
}
function showTip(g) {
  if (!tip) { tip = document.createElement("div"); tip.className = "tip"; tip.style.position = "fixed"; document.body.append(tip); }
  tip.innerHTML = tipHTML(g.__it);
  tip.hidden = false;
  const r = g.getBoundingClientRect();
  const tw = Math.min(352, window.innerWidth - 24);
  tip.style.maxWidth = tw + "px";
  const th = tip.offsetHeight;
  let x = r.right + 10, y = r.top - 8;
  if (x + tw > window.innerWidth - 12) x = Math.max(12, r.left - tw - 10);
  if (x < 12 || window.innerWidth < 640) { x = 12; y = r.bottom + 10; }
  if (y + th > window.innerHeight - 12) y = Math.max(12, r.top - th - 10);
  tip.style.left = x + "px"; tip.style.top = y + "px";
}
function hideTip() { if (tip) tip.hidden = true; pinned = null; }
function wireTips(svg) {
  svg.querySelectorAll(".rp-m").forEach((g) => {
    g.addEventListener("mouseenter", () => { if (!pinned && (g.__it.kind === "steer" || g.__it.cur !== "hidden")) showTip(g); });
    g.addEventListener("mouseleave", () => { if (!pinned) hideTip(); });
    g.addEventListener("focus", () => showTip(g));
    g.addEventListener("blur", () => { if (!pinned) hideTip(); });
    g.addEventListener("click", (e) => { e.stopPropagation(); if (pinned === g) hideTip(); else { pinned = g; showTip(g); } });
  });
}
document.addEventListener("click", () => hideTip());
document.addEventListener("keydown", (e) => { if (e.key === "Escape") hideTip(); });
window.addEventListener("scroll", () => { if (!pinned) hideTip(); }, { passive: true });

// ---------- play ----------
function setPlaying(on) {
  playing = on;
  el("play").textContent = on ? "❚❚ Pause" : "▶ Play";
  el("play").setAttribute("aria-pressed", String(on));
  if (on) { lastTs = performance.now(); requestAnimationFrame(tick); }
  el("steer").classList.toggle("lit", on && !!lastSteerId);
}
function tick(ts) {
  if (!playing) return;
  const dt = Math.min(100, ts - lastTs); lastTs = ts;
  if (ts < holdUntil) { requestAnimationFrame(tick); return; }
  const before = +tOf(pos * axis.D);
  pos = Math.min(1, pos + dt / DURATION);
  const after = +tOf(pos * axis.D);
  const crossed = steers.find((s) => +s.t > before && +s.t <= after);
  if (crossed) { pos = dOf(crossed.t) / axis.D; holdUntil = ts + HOLD; }
  paint();
  if (pos >= 1) return setPlaying(false);
  requestAnimationFrame(tick);
}
el("play").addEventListener("click", (e) => {
  e.stopPropagation(); hideTip();
  if (playing) return setPlaying(false);
  if (pos >= 0.999) { pos = 0; holdUntil = 0; paint(); }
  setPlaying(true);
});
el("when").addEventListener("input", (e) => { setPlaying(false); hideTip(); pos = +e.target.value / 1000; paint(); });
el("now").addEventListener("click", (e) => { e.stopPropagation(); setPlaying(false); hideTip(); pos = 1; paint(); });

let lastW = 0;
window.addEventListener("resize", () => {
  const w = el("draw").clientWidth;
  if (axis && Math.abs(w - lastW) > 24) { lastW = w; hideTip(); draw(); }
});

// ---------- go ----------
(async () => {
  const [bets, maps, steerRows, odds, times] = await Promise.all([loadBets(), loadMaps(), loadSteers(), loadHumanOdds(), getJSON(DATA + "commit-times.json")]);
  commitTimes = times || {};
  build(bets, maps, steerRows, odds);
  if (!items.length && !steers.length) { el("draw").innerHTML = `<div class="empty" style="margin:16px">The ledger is empty, so there is nothing to replay yet.</div>`; return; }
  axis = buildAxis();
  el("key").innerHTML = [["open", "Pre-registered, waiting for its result"], ["hit", "Landed"], ["killed", "Killed"], ["mixed", "Mixed or unsettled"]]
    .map(([k, w]) => `<span>${markInnerSvg(k)}<b>${w}</b></span>`).join("") +
    `<span>${markInnerSvg("gold")}<b style="color:${COL.gold}">Sean's steer</b></span>` +
    `<span><svg width="16" height="16" viewBox="-8 -8 16 16" aria-hidden="true"><circle r="3.4" fill="${COL.seed}"/></svg><b>Program opened</b></span>`;
  const noClock = items.filter((i) => i.kind === "bet" && i.endHow && !/result time/.test(i.endHow)).length;
  const rec = items.filter((i) => i.kind === "record").length;
  const squeezed = axis.segs.filter((s) => s.squeezed).length;
  el("src").innerHTML = `Read when the page loads from <code>ledger/bets.jsonl</code> (${items.length - rec} bets), <code>ledger/steers.jsonl</code> and <code>ledger/human-odds.jsonl</code> (${steers.length} gold marks, ${oddsLines.length} odds lines), and each program's map (seed times${rec ? `, and ${rec} of program 1's first-day tests, from before the ledger began, drawn smaller and without odds` : ""}). ` +
    `${noClock ? `${noClock} settled bet${noClock === 1 ? "" : "s"} have no clock time in the ledger; each is placed at the time of the git commit that recorded its result (or, for a withdrawn bet, the design review that withdrew it), from <code>data/commit-times.json</code>, which the deploy writes from git. ` : ""}` +
    `${squeezed ? `${squeezed} quiet stretch${squeezed === 1 ? " is" : "es are"} squeezed so the busy hours have room; each is shaded and labelled with its real length. ` : ""}` +
    `The engine's score is the Brier score of every bet marked <code>scored: true</code> that has settled by that moment, the same rule as <code>ledger/brier.md</code>. All times America/Denver.`;
  lastW = el("draw").clientWidth;
  draw();
})();
