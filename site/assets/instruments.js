// Instruments: one gauge per published number, each read live from the repositories' own files.
// Sources (all copied under data/ by site/assemble.sh):
//   ledger/bets.jsonl                         Brier, hits vs expected, referees, timeline
//   map/<program>.json                        phase-A results on the timeline; kills (with ledger/kills.jsonl)
//   programs/entangled-mind/audits/SUMMARY.md overclaim and verdict-reversal rates
//   programs/entangled-mind/results/ibm-usage.json, api-usage.md   QPU seconds; itemised API dollars
//   engine/CONTEXT.md                         the stated API spend and budget (§1 "Cost rule")
//   programs/nature-graded/map/program-3-map.json   chip-graded bets and the odds-stability check (optional)
import { header, esc, DATA, getText, getJSON, getJSONL, parseDate, fmtDate, markSVG, outcomeOf, num, STATUS, refereeOf } from "./common.js";
import { loadBets, loadMaps, loadKills } from "./data.js";

header();

const C = {
  text: "#ece9e2", text2: "#bcb8ae", muted: "#8d8a82", line: "#2c3138", surface: "#191c20", surface2: "#20242a",
  track: "#262b31", bar: "#3a4048", engine: "#3987e5", engineSoft: "#9cc0ef", human: "#e07a3f",
  hit: STATUS.hit.hex, kill: STATUS.killed.hex, run: STATUS.running.hex, mixed: STATUS.mixed.hex,
};
const SVGNS = "http://www.w3.org/2000/svg";
const EM = "programs/entangled-mind/";
const NG = "programs/nature-graded/";
const REPO = {
  engine: "https://github.com/GitPhar/oversight-testbed/blob/main/",
  em: "https://github.com/GitPhar/oversight-testbed/blob/main/programs/entangled-mind/",
  ng: "https://github.com/GitPhar/oversight-testbed/blob/main/programs/nature-graded/",
};

// ---------- small helpers ----------
const $ = (id) => document.getElementById(id);
const pct = (x, d = 0) => (x == null ? "—" : (x * 100).toFixed(d) + "%");
const f3 = (x) => (x == null ? "—" : x.toFixed(3));
const plural = (n, one, many = one + "s") => `${n} ${n === 1 ? one : many}`;
function s(tag, attrs = {}, parent) {
  const e = document.createElementNS(SVGNS, tag);
  for (const [k, v] of Object.entries(attrs)) if (v != null) e.setAttribute(k, v);
  if (parent) parent.append(e);
  return e;
}
function t(parent, x, y, str, attrs = {}) {
  const e = s("text", { x, y, fill: C.text2, "font-size": 14, ...attrs }, parent);
  e.textContent = str;
  return e;
}
function svgFor(box, H, label) {
  const W = Math.max(260, Math.floor(box.clientWidth));
  const svg = s("svg", { viewBox: `0 0 ${W} ${H}`, width: W, height: H, role: "img", "aria-label": label });
  box.innerHTML = "";
  box.append(svg);
  return { svg, W };
}
const src = (path, label, base = REPO.engine) => `<a href="${base}${path}">${esc(label || path)}</a>`;

// A gauge card: label, headline value, a drawing, one caption line, and where the number came from.
function card(id, { label, value, unit = "", caption, source, empty = false }) {
  const el = $(id);
  el.classList.toggle("is-empty", empty);
  el.innerHTML = `<h3 class="g-label">${label}</h3>
    <div class="g-value">${value}${unit ? ` <span class="g-unit">${unit}</span>` : ""}</div>
    <div class="g-viz"></div>
    <p class="g-cap">${caption}</p>
    <p class="g-src">${source}</p>`;
  return el.querySelector(".g-viz");
}
function missing(id, label, what) {
  card(id, { label, value: "—", caption: `No data yet: ${what}`, source: "", empty: true });
}

// Redraw every drawing at its box's real width, so text keeps its stated size on a phone.
const draws = [];
function drawn(box, fn) { draws.push([box, fn]); fn(box); }
let lastW = window.innerWidth;
window.addEventListener("resize", () => {
  if (Math.abs(window.innerWidth - lastW) < 30) return;
  lastW = window.innerWidth;
  for (const [b, fn] of draws) fn(b);
});

// ---------- tooltip ----------
const tip = document.createElement("div");
tip.className = "tip"; tip.style.position = "fixed"; tip.hidden = true;
document.body.append(tip);
function showTip(target, html) {
  tip.innerHTML = html; tip.hidden = false;
  const r = target.getBoundingClientRect();
  const tw = Math.min(320, window.innerWidth - 24);
  tip.style.maxWidth = tw + "px";
  let x = r.right + 10, y = r.top - 6;
  if (x + tw > window.innerWidth - 12) x = Math.max(12, r.left - tw - 10);
  if (x < 12 || x + tip.offsetWidth > window.innerWidth - 12) x = Math.max(12, Math.min(window.innerWidth - tip.offsetWidth - 12, r.left));
  if (y + tip.offsetHeight > window.innerHeight - 12) y = window.innerHeight - tip.offsetHeight - 12;
  tip.style.left = x + "px"; tip.style.top = Math.max(64, y) + "px";
}
function tipOn(el, html) {
  el.setAttribute("tabindex", "0");
  el.style.cursor = "pointer";
  el.addEventListener("mouseenter", () => showTip(el, html));
  el.addEventListener("focus", () => showTip(el, html));
  el.addEventListener("click", (e) => { e.stopPropagation(); showTip(el, html); });
  el.addEventListener("mouseleave", () => (tip.hidden = true));
  el.addEventListener("blur", () => (tip.hidden = true));
}
document.addEventListener("click", () => (tip.hidden = true));
window.addEventListener("scroll", () => (tip.hidden = true), { passive: true });

// ---------- statistics ----------
const brier = (pts) => (pts.length ? pts.reduce((a, p) => a + (p.p - p.o) ** 2, 0) / pts.length : null);
function poissonBinomial(ps) {
  let d = [1];
  for (const p of ps) {
    const n = new Array(d.length + 1).fill(0);
    d.forEach((v, k) => { n[k] += v * (1 - p); n[k + 1] += v * p; });
    d = n;
  }
  return d;
}
function wilson(k, n, z = 1.96) {
  if (!n) return null;
  const ph = k / n, den = 1 + z * z / n;
  const c = (ph + z * z / (2 * n)) / den, h = (z * Math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n))) / den;
  return [Math.max(0, c - h), Math.min(1, c + h)];
}

// ---------- referees ----------
// A bet's referee is what decides its outcome (common.js refereeOf): model, chip, published record, or mathematics.

// ---------- parsing the files ----------
function tableRows(md, headingRe) {
  const lines = md.split("\n");
  let on = false;
  const rows = [];
  for (const L of lines) {
    if (/^#{1,4}\s/.test(L)) { on = headingRe.test(L); continue; }
    if (on && L.trim().startsWith("|") && !/^\s*\|[\s:|-]+\|\s*$/.test(L)) {
      rows.push(L.trim().replace(/^\||\|$/g, "").split("|").map((c) => c.replace(/\*\*|`/g, "").trim()));
    }
  }
  return rows;
}
const pair = (str) => { const m = String(str || "").match(/(\d+)\s*\/\s*(\d+)/); return m ? [+m[1], +m[2]] : null; };
function readAudit(md) {
  if (!md) return null;
  const rows = tableRows(md, /headline rates/i);
  const find = (re) => rows.find((r) => re.test(r[0]))?.[1];
  const out = {
    overclaim: pair(find(/overclaim sentence to cut/i)),
    claims: pair(find(/claims checked/i)),            // "checked / failed"
    reversed: pair(find(/reversal rate/i)),
    undetermined: pair(find(/undetermined/i)),
    fragile: pair(find(/fails under one defensible check/i)),
    date: (md.match(/\b(20\d\d-\d\d-\d\d)\b/) || [])[1] || "",
  };
  return out.overclaim || out.reversed ? out : null;
}
function readContext(md) {
  if (!md) return {};
  const spend = md.match(/\$(\d+(?:\.\d+)?) of the \$(\d+(?:\.\d+)?)\/month API credit was used/i);
  const plan = md.match(/plan to ([A-Z][a-z]{2} \d+) is about \$(\d+(?:\.\d+)?) more/i);
  const stop = md.match(/hard stop (\d+) s/i);
  return {
    spent: spend ? +spend[1] : null, budget: spend ? +spend[2] : null,
    planTo: plan ? plan[1] : null, planMore: plan ? +plan[2] : null,
    hardStop: stop ? +stop[1] : null,
    rewritten: (md.match(/Last rewritten:\s*([^,\n]+)/) || [])[1] || "",
  };
}

// ---------- drawing: a horizontal Brier scale ----------
function brierScale(box, { value, coin = 0.25, color, emptyText }) {
  drawn(box, (b) => {
    const H = 92;
    const { svg, W } = svgFor(b, H, value == null ? "Brier scale, no score yet" : `Brier ${f3(value)} against ${f3(coin)} for a coin flip`);
    const max = value != null && value > 0.5 ? 1 : 0.5;
    const L = 10, R = W - 10, x = (v) => L + (v / max) * (R - L);
    const ty = 44;
    s("rect", { x: L, y: ty - 6, width: R - L, height: 12, rx: 6, fill: C.track }, svg);
    s("rect", { x: L, y: ty - 6, width: x(coin) - L, height: 12, rx: 6, fill: "#2a3a4c" }, svg);
    t(svg, L, ty - 14, "better than a coin", { "font-size": 13, fill: C.muted });
    s("line", { x1: x(coin), x2: x(coin), y1: ty - 12, y2: ty + 14, stroke: C.text2, "stroke-width": 2, "stroke-dasharray": "3 3" }, svg);
    t(svg, x(coin), ty + 32, `coin flip ${f3(coin)}`, { "text-anchor": "middle", "font-size": 14, fill: C.text2 });
    t(svg, L, ty + 32, "0", { "font-size": 13, fill: C.muted });
    t(svg, R, ty + 32, String(max), { "font-size": 13, fill: C.muted, "text-anchor": "end" });
    t(svg, L, H - 4, "lower is better", { "font-size": 13, fill: C.muted });
    if (value == null) {
      t(svg, R, ty - 14, emptyText || "no score yet", { "text-anchor": "end", "font-size": 13, fill: C.text2, "font-style": "italic" });
      return;
    }
    const cx = x(Math.min(value, max));
    s("circle", { cx, cy: ty, r: 10, fill: C.surface }, svg);
    s("circle", { cx, cy: ty, r: 8, fill: color }, svg);
    const lab = t(svg, Math.min(R, Math.max(L, cx)), ty - 16, f3(value), { "font-size": 15, fill: C.text, "font-weight": 700,
      "text-anchor": cx > R - 30 ? "end" : cx < L + 30 ? "start" : "middle" });
    void lab;
  });
}

// ---------- drawing: horizontal meter ----------
function meter(box, { value, max, unit, marker, markerLabel, color = C.run }) {
  drawn(box, (b) => {
    const H = marker != null ? 72 : 52;
    const { svg, W } = svgFor(b, H, `${value} of ${max} ${unit}`);
    const L = 2, R = W - 2, x = (v) => L + Math.min(1, v / max) * (R - L);
    const ty = marker != null ? 30 : 12;
    s("rect", { x: L, y: ty, width: R - L, height: 14, rx: 7, fill: C.track }, svg);
    if (value > 0) s("rect", { x: L, y: ty, width: Math.max(8, x(value) - L), height: 14, rx: 7, fill: color }, svg);
    if (marker != null) {
      const mx = x(marker);
      s("line", { x1: mx, x2: mx, y1: ty - 8, y2: ty + 22, stroke: C.kill, "stroke-width": 2 }, svg);
      t(svg, mx - 6, ty - 12, markerLabel, { "font-size": 13, fill: C.text2, "text-anchor": "end" });
    }
    t(svg, L, ty + 36, "0", { "font-size": 13, fill: C.muted });
    t(svg, R, ty + 36, `${max} ${unit}`, { "font-size": 13, fill: C.muted, "text-anchor": "end" });
  });
}

// ---------- drawing: unit cells (one per item) ----------
function cells(box, groups) {
  // groups: [{ n, cls, word }]; one cell per item, in group order, with a key below.
  box.innerHTML = `<div class="cells" role="img" aria-label="${esc(groups.map((g) => `${g.n} ${g.word}`).join(", "))}">${
    groups.map((g) => `<span class="cell ${g.cls}"></span>`.repeat(g.n)).join("")}</div>
    <div class="cellkey">${groups.map((g) => `<span><span class="cell ${g.cls}"></span>${g.n} ${esc(g.word)}</span>`).join("")}</div>`;
}

// ---------- gauge: engine Brier ----------
function gaugeEngineBrier(pts) {
  const b = brier(pts), n = pts.length;
  if (!n) return missing("g-brier-engine", "Engine Brier score", "no scored bets in <code>ledger/bets.jsonl</code>.");
  const d = b - 0.25;
  const verdict = Math.abs(d) < 0.02 ? "About the same as always saying 50%" : d < 0 ? "Better than always saying 50%" : "Worse than always saying 50%";
  const box = card("g-brier-engine", {
    label: "Engine Brier score",
    value: f3(b), unit: "vs 0.250 for a coin flip",
    caption: `${verdict}: on ${plural(n, "scored bet")} the engine's odds have ${d < -0.02 ? "beaten" : "not beaten"} a coin${n < 20 ? ", and that is too few bets to mean much yet" : ""}.`,
    source: `${src("ledger/bets.jsonl")}, ${plural(n, "row")} with <code>scored: true</code> · same as ${src("ledger/brier.md", "brier.md")}`,
  });
  brierScale(box, { value: b, color: C.engine });
}

// ---------- gauge: human Brier ----------
function gaugeHumanBrier(bets, pts, p3) {
  const b = brier(pts);
  const withOdds = bets.filter((x) => x.human != null).length;
  const p3n = p3 ? p3.directions.length : 0, p3h = p3 ? p3.directions.filter((d) => num(d.human_odds) != null).length : 0;
  const box = card("g-brier-human", {
    label: "Human Brier score (Sean)",
    value: b == null ? "none yet" : f3(b), unit: b == null ? "" : "vs 0.250 for a coin flip",
    empty: b == null,
    caption: b == null
      ? `Nothing to score yet: ${withOdds} of ${bets.length} ledger bets${p3 ? ` and ${p3h} of ${p3n} program-3 directions` : ""} carry a human number. The founding week's odds were never written down, and are not filled in from memory.`
      : `Over ${plural(pts.length, "bet")} with a human number written before data.`,
    source: `${src("ledger/bets.jsonl")}, <code>human_odds</code> · the form: ${src("map/human-odds-template.md", "human-odds-template.md")}`,
  });
  brierScale(box, { value: b, color: C.human, emptyText: "no human odds recorded" });
}

// ---------- gauge: hits vs expected ----------
function gaugeHits(pts) {
  const n = pts.length;
  if (!n) return missing("g-hits", "Hits vs expected", "no scored bets.");
  const ps = pts.map((p) => p.p), obs = pts.reduce((a, p) => a + p.o, 0);
  const exp = ps.reduce((a, b) => a + b, 0);
  const dist = poissonBinomial(ps);
  const up = obs >= exp;
  const tail = up ? dist.slice(obs).reduce((a, b) => a + b, 0) : dist.slice(0, obs + 1).reduce((a, b) => a + b, 0);
  const odd = tail < 0.05;
  const box = card("g-hits", {
    label: "Hits vs expected",
    value: `${obs}`, unit: `hit${obs === 1 ? "" : "s"}, ${exp.toFixed(2)} expected`,
    caption: `If the odds were right, ${obs} or ${up ? "more" : "fewer"} hits would happen ${pct(tail)} of the time: ${odd ? `the odds look too ${up ? "low" : "high"}.` : "no sign yet that the odds are off."}`,
    source: `${src("ledger/bets.jsonl")}: the ${plural(n, "scored bet")}' stated odds, added up (Poisson-binomial)`,
  });
  drawn(box, (b) => {
    const H = 132;
    const { svg, W } = svgFor(b, H, `Chance of each number of hits; observed ${obs}, expected ${exp.toFixed(2)}`);
    const top = 26, base = H - 40, L = 4, R = W - 4;
    const slot = (R - L) / dist.length, bw = Math.min(46, slot - 8);
    const cx = (k) => L + slot * (k + 0.5);
    const mx = Math.max(...dist);
    s("line", { x1: L, x2: R, y1: base, y2: base, stroke: C.line }, svg);
    dist.forEach((v, k) => {
      const h = Math.max(2, (v / mx) * (base - top));
      const g = s("g", {}, svg);
      s("rect", { x: cx(k) - bw / 2, y: base - h, width: bw, height: h, rx: 4, fill: k === obs ? C.hit : C.bar }, g);
      s("rect", { x: cx(k) - slot / 2, y: top, width: slot, height: base - top + 20, fill: "transparent" }, g);
      t(svg, cx(k), base + 18, String(k), { "text-anchor": "middle", "font-size": 14, fill: k === obs ? C.text : C.muted, "font-weight": k === obs ? 700 : 400 });
      if (k === obs) t(svg, cx(k), base + 35, "got", { "text-anchor": "middle", "font-size": 13, fill: C.text, "font-weight": 700 });
      tipOn(g, `<div class="t-title">${k} hit${k === 1 ? "" : "s"}${k === obs ? " (what happened)" : ""}</div><div>Chance, if the odds were right: <b>${pct(v, 1)}</b></div>`);
    });
    const ex = L + slot * (exp + 0.5);
    s("line", { x1: ex, x2: ex, y1: top - 8, y2: base, stroke: C.text2, "stroke-width": 2, "stroke-dasharray": "4 3" }, svg);
    t(svg, ex + (ex > W - 120 ? -6 : 6), top - 10, `expected ${exp.toFixed(2)}`, { "font-size": 13, fill: C.text2, "text-anchor": ex > W - 120 ? "end" : "start" });
    t(svg, L, base + 35, "hits", { "font-size": 13, fill: C.muted });
  });
}

// ---------- gauge: odds stability ----------
function gaugeStability(p3) {
  const rows = (p3?.directions || []).filter((d) => d.elicitation_check && num(d.engine_odds) != null).map((d) => {
    const v1 = num(d.engine_odds), para = num(d.elicitation_check.paraphrase);
    const negNot = num(d.elicitation_check.negation_not_pass);
    const neg = negNot == null ? null : 1 - negNot;
    const vals = [v1, para, neg].filter((v) => v != null);
    return { id: d.id, title: d.title, v1, para, neg, spread: Math.max(...vals) - Math.min(...vals),
      incoh: d.elicitation_check.incoherence != null ? num(d.elicitation_check.incoherence) ?? 0 : (neg != null ? Math.abs(v1 - neg) : null) };
  });
  if (!rows.length) return missing("g-stability", "Odds stability", "program 3's map (with its elicitation check) is not deployed with the site.");
  // incoherence is stored as a fraction (0.08 = 8 points); num() leaves fractions alone.
  const mean = (a) => a.reduce((x, y) => x + y, 0) / a.length;
  const negPts = Math.round(mean(rows.map((r) => r.incoh)) * 1000) / 10;
  const paraPts = Math.round(mean(rows.filter((r) => r.para != null).map((r) => Math.abs(r.v1 - r.para))) * 1000) / 10;
  const el = $("g-stability");
  el.classList.add("wide");
  const box = card("g-stability", {
    label: "Odds stability (program 3)",
    value: `${Math.round(negPts)} points`, unit: "average shift when the question is turned around",
    caption: `Asked "will it fail?" instead of "will it pass?", the engine's odds moved ${negPts.toFixed(1)} points on average, up to ${Math.round(Math.max(...rows.map((r) => r.incoh)) * 100)}; rewording moved them ${paraPts.toFixed(1)}. Any calibration gap smaller than this is noise.`,
    source: `<a href="${DATA}${NG}map/odds-elicitation/README.md">program 3's odds-elicitation check</a> (nature-graded <code>map/program-3-map.json</code>): a random ${rows.length} of ${p3.directions.length} directions, re-asked by fresh contexts`,
  });
  box.insertAdjacentHTML("beforebegin", `<div class="key small g-key">
    <span><svg width="14" height="14"><circle cx="7" cy="7" r="6" fill="${C.engine}"/></svg>asked directly</span>
    <span><svg width="14" height="14"><circle cx="7" cy="7" r="5" fill="none" stroke="${C.engineSoft}" stroke-width="2"/></svg>reworded</span>
    <span><svg width="16" height="16"><path d="M8 1l7 7-7 7-7-7z" fill="${C.text2}"/></svg>asked as "will it fail?", flipped</span></div>`);
  rows.sort((a, b) => b.spread - a.spread);
  drawn(box, (b) => {
    const rowH = 30, top = 22;
    const H = top + rows.length * rowH + 30;
    const { svg, W } = svgFor(b, H, `Odds for ${rows.length} directions asked three ways`);
    const L = 58, R = W - 44, x = (v) => L + v * (R - L);
    for (const v of [0, 0.25, 0.5, 0.75, 1]) {
      s("line", { x1: x(v), x2: x(v), y1: top, y2: top + rows.length * rowH, stroke: C.line }, svg);
      t(svg, x(v), H - 8, `${v * 100}%`, { "text-anchor": "middle", "font-size": 13, fill: C.muted });
    }
    t(svg, R + 40, 13, "spread", { "font-size": 13, fill: C.muted, "text-anchor": "end" });
    rows.forEach((r, i) => {
      const cy = top + i * rowH + rowH / 2 + 4;
      const vals = [r.v1, r.para, r.neg].filter((v) => v != null);
      const g = s("g", {}, svg);
      s("rect", { x: 0, y: cy - rowH / 2, width: W, height: rowH, fill: "transparent" }, g);
      t(g, 0, cy + 5, r.id, { "font-size": 14, fill: C.text2 });
      s("rect", { x: x(Math.min(...vals)), y: cy - 3, width: Math.max(2, x(Math.max(...vals)) - x(Math.min(...vals))), height: 6, rx: 3, fill: C.bar }, g);
      if (r.neg != null) s("path", { d: `M${x(r.neg)} ${cy - 7}l7 7-7 7-7-7z`, fill: C.text2, stroke: C.surface, "stroke-width": 1.5 }, g);
      if (r.para != null) s("circle", { cx: x(r.para), cy, r: 5.5, fill: C.surface, stroke: C.engineSoft, "stroke-width": 2 }, g);
      s("circle", { cx: x(r.v1), cy, r: 6, fill: C.engine, stroke: C.surface, "stroke-width": 1.5 }, g);
      t(g, R + 40, cy + 5, String(Math.round(r.spread * 100)), { "font-size": 14, fill: r.spread >= 0.15 ? C.text : C.text2, "font-weight": r.spread >= 0.15 ? 700 : 400, "text-anchor": "end" });
      tipOn(g, `<div class="t-status">${esc(r.id)}</div><div class="t-title">${esc(r.title)}</div>
        <div>Asked directly: <b>${pct(r.v1)}</b><br>Reworded: <b>${pct(r.para)}</b><br>"Will it fail?": ${pct(r.neg == null ? null : 1 - r.neg)}, so pass = <b>${pct(r.neg)}</b></div>
        <div class="t-meta">Spread ${Math.round(r.spread * 100)} points</div>`);
    });
  });
}

// ---------- gauges: audit ----------
// Audit gauges read the ledger: every bet with an audit file, its cuts, and whether its verdict stood.
// Program 1's founding-week audits (entangled-mind audits/SUMMARY.md) and round 2's summary are added in the caption.
function auditedBets(bets) { return bets.filter((b) => b.raw?.audit_path); }
function roundTwo(md) {
  if (!md) return null;
  const ch = md.match(/verdict changed by the audit \|\s*\**(\d+)\s*\/\s*(\d+)/i);
  const rows = [...md.matchAll(/^\|\s*\[`[^`]+`\][^|]*\|[^|]*\|[^|]*\|\s*(\d+)\s*\/\s*(\d+)\s*\/\s*(\d+)\s*\|/gm)];
  return { changed: ch ? [+ch[1], +ch[2]] : null, results: rows.length, withCuts: rows.filter((m) => +m[3] > 0).length };
}
const cutsOf = (b) => { const m = String(b.raw.audit_status || "").match(/(\d+) cuts/); return m ? +m[1] : 0; };
function gaugeOverclaim(a, bets, r2) {
  const ab = auditedBets(bets);
  if (!ab.length) return missing("g-overclaim", "Audit: overclaim rate", "no audited bet in <code>ledger/bets.jsonl</code>.");
  const cut = ab.filter((b) => cutsOf(b) > 0).length, n = ab.length;
  const r1 = a?.overclaim ? `founding week ${a.overclaim[0]} of ${a.overclaim[1]} results` : "";
  const r2s = r2?.results ? `round 2 ${r2.withCuts} of ${r2.results}` : "";
  const box = card("g-overclaim", {
    label: "Audit: overclaim rate",
    value: pct(cut / n), unit: `${cut} of ${n} audited bets`,
    caption: `An auditor who had not seen the work required at least one sentence cut or rewritten in ${cut} of ${n} audited ledger bets. Over every audited result (${[r1, r2s].filter(Boolean).join("; ")}), nearly every write-up said more than its data somewhere.`,
    source: `${src("ledger/bets.jsonl")} (<code>audit_path</code>, <code>audit_status</code>) · ${src("ledger/audits/SUMMARY-2.md", "SUMMARY-2.md")} · ${src("audits/SUMMARY.md", "entangled-mind audits/SUMMARY.md", REPO.em)}`,
  });
  cells(box, [{ n: cut, cls: "c-over", word: "with a cut" }, { n: n - cut, cls: "c-clean", word: "clean" }]);
}
function gaugeReversal(a, bets, r2) {
  const ab = auditedBets(bets);
  if (!ab.length) return missing("g-reversal", "Audit: verdict reversals", "no audited bet in <code>ledger/bets.jsonl</code>.");
  const rev = ab.filter((b) => b.raw.verdict_stands === false), n = ab.length;
  const r1 = a?.reversed ? `founding week ${a.reversed[0]} of ${a.reversed[1]}` : "";
  const r2s = r2?.changed ? `round 2 ${r2.changed[0]} of ${r2.changed[1]}` : "";
  const box = card("g-reversal", {
    label: "Audit: verdict reversals",
    value: `${rev.length} of ${n}`, unit: "audited bets overturned",
    caption: `${rev.length ? `Overturned: ${rev.map((b) => `${esc(b.id)}, now ${esc(b.raw.verdict)}`).join("; ")}.` : "No audited bet was overturned."} Counting every audited result, not only ledger bets: ${[r1, r2s].filter(Boolean).join(", ")} verdicts changed.`,
    source: `${src("ledger/bets.jsonl")} (<code>verdict_stands</code>) · ${src("ledger/audits/SUMMARY-2.md", "SUMMARY-2.md")} · ${src("audits/SUMMARY.md", "entangled-mind audits/SUMMARY.md", REPO.em)}`,
  });
  cells(box, [{ n: rev.length, cls: "c-rev", word: "overturned" }, { n: n - rev.length, cls: "c-stand", word: "stands" }]);
}

// The auditor's own catch rate: known-bad claims planted before an audit, sealed, then revealed (operators/plant.md).
function gaugeCatch(plants) {
  const rev = (plants || []).filter((r) => r.status === "revealed" && r.plaintext);
  const planted = rev.filter((r) => r.plaintext.planted);
  const sealed = (plants || []).filter((r) => r.status === "sealed").length;
  if (!planted.length) return missing("g-catch", "Audit: the auditor's catch rate", `no planted claim revealed yet${sealed ? ` (${sealed} sealed)` : ""} in <code>ledger/plants.jsonl</code>.`);
  const k = planted.filter((r) => r.caught).length, n = planted.length;
  const [lo, hi] = wilson(k, n);
  const lim = planted.map((r) => r.limits).filter(Boolean);
  const box = card("g-catch", {
    label: "Audit: the auditor's catch rate",
    value: `${k} of ${n}`, unit: `planted claim${n === 1 ? "" : "s"} caught`,
    caption: `95% interval ${pct(lo)}–${pct(hi)}. Another session hid a known-bad claim in a results file and sealed it before the audit; the auditor ${k === n ? "found every one" : `found ${k}`}. ${n < 10 ? `With ${n === 1 ? "one plant" : n + " plants"} this is not a rate yet (H2 needs 10).` : ""} ${lim.length ? "Limits: " + esc(lim[0].split(". ").slice(0, 2).join(". ")) + "." : ""}`,
    source: `${src("ledger/plants.jsonl")} (hash-checked by <code>ledger/plants.py verify</code>) · ${src("ledger/scores.md", "scores.md")}`,
  });
  cells(box, [{ n: k, cls: "c-over", word: "caught" }, { n: n - k, cls: "c-rev", word: "missed" }]);
}

// The feedback loop: every pre-registration from the rule's start carries a lesson and a design review.
function gaugeLearning(bets, lessons) {
  const RULE_FROM = "2026-11-04 17:00";
  const L = lessons || [];
  const pats = L.filter((r) => r.kind === "pattern");
  const les = new Map(L.filter((r) => r.kind === "lesson").map((r) => [r.bet, r]));
  const since = bets.filter((b) => (b.raw?.prereg_time || "") >= RULE_FROM && b.raw?.verdict !== "withdrawn");
  const reviewed = (b) => ["go", "fix-first", "redesign"].includes(b.raw?.design_review?.verdict);
  const bad = since.filter((b) => !les.has(b.id) || (!reviewed(b) && b.raw?.result_commit)).map((b) => b.id);
  const awaiting = since.filter((b) => !reviewed(b) && !b.raw?.result_commit).map((b) => b.id);
  const pairs = [...les.values()].flatMap((l) => {
    const b = bets.find((x) => x.id === l.bet); const o = b ? outcomeOf(b) : null;
    return o != null && l.odds_before_lesson != null && l.odds_after_lesson != null ? [[l.odds_before_lesson, l.odds_after_lesson, o]] : [];
  });
  const bb = brier(pairs.map(([p, , o]) => ({ p, o }))), ba = brier(pairs.map(([, q, o]) => ({ p: q, o })));
  const box = card("g-learn", {
    label: "Learning: lessons before every bet",
    value: since.length ? `${since.length - bad.length} of ${since.length}` : "0", unit: since.length ? "new bets with a lesson, none run without a design review" : "new bets since the rule",
    caption: `${pats.length} patterns from past misses and audit cuts are on file. Before each new bet the engine must say which one it is correcting and how its odds reflect it, and a fresh auditor must dry-run the design. ${bad.length ? `<b>Violations: ${bad.map(esc).join(", ")}.</b> ` : ""}${awaiting.length ? `Awaiting their design review: ${awaiting.map(esc).join(", ")}. ` : ""}${pairs.length ? `Brier with the odds before the lesson ${f3(bb)}, after it ${f3(ba)} (n = ${pairs.length}).` : "Whether the lessons improve the odds is measured once lesson-carrying bets resolve: Brier before the lesson against after it."}`,
    source: `${src("ledger/lessons.jsonl")} · ${src("operators/learn.md", "learn.md")} · ${src("operators/design-review.md", "design-review.md")}`,
  });
  cells(box, [{ n: since.length - bad.length, cls: "c-clean", word: "with lesson + review" }, { n: bad.length, cls: "c-over", word: "violation" }]);
}

function gaugeKills(kills, p3) {
  const n = kills.length, diag = kills.filter((k) => String(k.diagnosis || "").trim()).length;
  const scout = (p3?.closed || []).filter((c) => String(c.status || "killed") === "killed");
  const scoutDiag = scout.filter((c) => String(c.diagnosis || "").trim()).length;
  const box = card("g-kills", {
    label: "Kills with a diagnosis",
    value: `${diag} of ${n}`, unit: "with a diagnosis",
    caption: n === 0 ? "Nothing has been killed yet." : diag === n
      ? "Every dead direction stays on the record with the reason it died; none was quietly dropped."
      : `${n - diag} dead direction${n - diag === 1 ? " is" : "s are"} still missing the reason ${n - diag === 1 ? "it" : "they"} died.`,
    source: `the <a href="kills.html">kill log</a>: killed map nodes, <code>null</code> bets and <code>ledger/kills.jsonl</code>, merged`,
  });
  const marks = kills.map((k) => `<span class="km" data-i="${kills.indexOf(k)}">${markSVG(String(k.diagnosis || "").trim() ? "killed" : "open", 18)}</span>`).join("");
  box.innerHTML = `<div class="kmarks">${marks}</div>${scout.length ? `<p class="g-sub">Plus ${scout.length} program-3 directions closed at scouting, before any bet, ${scoutDiag === scout.length ? "all" : scoutDiag} with a diagnosis.</p>` : ""}`;
  box.querySelectorAll(".km").forEach((m) => {
    const k = kills[+m.dataset.i];
    tipOn(m, `<div class="t-status">${markSVG("killed", 13)} Killed${k.date ? " · " + esc(fmtDate(parseDate(k.date))) : ""}</div><div class="t-title">${esc(k.title)}</div>
      ${k.diagnosis ? `<div class="t-diag">${esc(k.diagnosis)}</div>` : `<div class="t-meta">No diagnosis recorded.</div>`}`);
  });
}

// ---------- gauges: spend ----------
// API dollars: a dated baseline plus everything itemised after it, so the number moves on every push.
// Baseline and non-bet runs: ledger/spend.jsonl. Bets: cost_usd of every bet pre-registered after the baseline.
function gaugeAPI(ctx, bets, apiMd, spend) {
  const base = (spend || []).find((r) => r.kind === "baseline");
  if (!base) return missing("g-api", "Spend: API dollars", "<code>ledger/spend.jsonl</code> has no baseline row.");
  const runs = (spend || []).filter((r) => r.kind === "run");
  const later = bets.filter((b) => (b.raw?.prereg_time || "") > base.as_of && b.raw?.cost_usd != null);
  const fromBets = later.reduce((a, b) => a + Number(b.raw.cost_usd || 0), 0);
  const fromRuns = runs.reduce((a, r) => a + Number(r.usd || 0), 0);
  const spent = base.usd + fromBets + fromRuns;
  const budget = ctx.budget || 200;
  const box = card("g-api", {
    label: "Spend: API dollars",
    value: "$" + spent.toFixed(2), unit: `of $${budget} this month`,
    caption: `${pct(spent / budget)} of the month's API credit: $${base.usd.toFixed(2)} through ${esc(base.as_of)}, then $${fromBets.toFixed(2)} on ${plural(later.length, "bet")} and $${fromRuns.toFixed(2)} on ${plural(runs.length, "other run")}.${ctx.planMore ? ` The plan to ${esc(ctx.planTo)} adds about $${ctx.planMore}.` : ""}`,
    source: `${src("ledger/spend.jsonl")} (baseline and non-bet runs) · ${src("ledger/bets.jsonl")} (<code>cost_usd</code> after the baseline)`,
  });
  drawn(box, (b) => meter(b, { value: spent, max: budget, unit: "$", marker: ctx.planMore ? Math.min(budget, spent + ctx.planMore) : null, markerLabel: ctx.planMore ? `with the plan to ${ctx.planTo}` : "" }));
}
function gaugeQPU(ibm, ctx, p3) {
  if (!Array.isArray(ibm)) return missing("g-qpu", "Spend: QPU seconds", "<code>results/ibm-usage.json</code> from program 1 is not deployed with the site.");
  const used = ibm.reduce((a, j) => a + (Number(j.quantum_seconds) || 0), 0);
  const limit = Math.max(0, ...ibm.map((j) => Number(j.service_after?.usage_limit_seconds || j.service_before?.usage_limit_seconds) || 0)) || 600;
  const stop = p3?.qpu?.hard_stop_s ?? ctx.hardStop ?? null;
  const box = card("g-qpu", {
    label: "Spend: quantum chip seconds",
    value: `${used} s`, unit: `of ${limit} s a month`,
    caption: `${pct(used / limit)} of the monthly chip time is used, in ${plural(ibm.length, "job")}${stop ? `; the code refuses any job past ${stop} s` : ""}.`,
    source: `${src("results/ibm-usage.json", "entangled-mind results/ibm-usage.json", REPO.em)} (one row per job; limit as IBM reports it)${stop ? ` · hard stop from ${p3?.qpu ? "program 3's map" : "CONTEXT.md"}` : ""}`,
  });
  meter(box, { value: used, max: limit, unit: "s", marker: stop, markerLabel: stop ? `hard stop ${stop} s` : "", color: C.run });
}

// ---------- referees: calibration side by side ----------
function refPanel(box, { scored, waiting, emptyText }) {
  drawn(box, (b) => {
    const narrow = b.clientWidth < 380;
    const STRIP = 34, GAP = 14, PLOT = narrow ? 130 : 150;
    const M = { l: narrow ? 76 : 92, r: 10, t: 4 };
    const yTrue = M.t, yPlot = yTrue + STRIP + GAP, yFalse = yPlot + PLOT + GAP, yWait = yFalse + STRIP + 16;
    const H = yWait + STRIP + 40;
    const { svg, W } = svgFor(b, H, `Calibration: ${scored.length} settled bets, ${waiting.length} with odds awaiting a result`);
    const x = (p) => M.l + p * (W - M.l - M.r);
    const y = (f) => yPlot + PLOT - f * PLOT;
    for (const [yy, word] of [[yTrue, "came true"], [yFalse, "did not"], [yWait, "no score"]]) {
      s("rect", { x: M.l, y: yy, width: W - M.l - M.r, height: STRIP, rx: 6, fill: C.surface2 }, svg);
      t(svg, M.l - 8, yy + STRIP / 2 + 5, word, { "text-anchor": "end", "font-size": 13, fill: yy === yWait ? C.text2 : C.text, "font-weight": 700 });
    }
    for (const f of [0, 0.5, 1]) {
      s("line", { x1: M.l, x2: W - M.r, y1: y(f), y2: y(f), stroke: C.line }, svg);
      t(svg, M.l - 8, y(f) + 5, `${f * 100}%`, { "text-anchor": "end", "font-size": 13, fill: C.muted });
    }
    for (const p of [0, 0.5, 1]) {
      s("line", { x1: x(p), x2: x(p), y1: yTrue, y2: yWait + STRIP, stroke: C.line }, svg);
      t(svg, x(p), H - 22, `${p * 100}%`, { "text-anchor": p === 0 ? "start" : p === 1 ? "end" : "middle", "font-size": 13, fill: C.muted });
    }
    t(svg, M.l + (W - M.l - M.r) / 2, H - 4, "odds stated before data", { "text-anchor": "middle", "font-size": 13, fill: C.text2 });
    s("line", { x1: x(0), y1: y(0), x2: x(1), y2: y(1), stroke: "#6b7079", "stroke-width": 1.5, "stroke-dasharray": "5 4" }, svg);
    if (!scored.length) {
      t(svg, M.l + (W - M.l - M.r) / 2, yPlot + PLOT / 2 + 5, emptyText, { "text-anchor": "middle", "font-size": 15, fill: C.text2, "font-style": "italic" });
    }
    // buckets of width 0.1, with 95% Wilson intervals
    const bk = new Map();
    for (const p of scored) { const i = Math.min(9, Math.floor(p.p * 10 + 1e-9)); if (!bk.has(i)) bk.set(i, []); bk.get(i).push(p); }
    for (const [i, list] of bk) {
      const mp = list.reduce((a, q) => a + q.p, 0) / list.length, k = list.reduce((a, q) => a + q.o, 0), n = list.length;
      const ci = wilson(k, n), fo = k / n;
      s("line", { x1: x(mp), x2: x(mp), y1: y(ci[0]), y2: y(ci[1]), stroke: C.engine, "stroke-width": 2, "stroke-opacity": 0.55, "stroke-linecap": "round" }, svg);
      const g = s("g", {}, svg);
      s("path", { d: `M${x(mp)} ${y(fo) - 9}l9 9-9 9-9-9z`, fill: C.engine, stroke: C.surface, "stroke-width": 2 }, g);
      s("rect", { x: x(mp) - 14, y: y(fo) - 14, width: 28, height: 28, fill: "transparent" }, g);
      tipOn(g, `<div class="t-status">odds ${i * 10}–${i * 10 + 10}%</div><div class="t-title">${plural(n, "bet")}, average stated ${pct(mp)}</div><div>Came true: ${k} of ${n}<br>95% interval ${pct(ci[0])}–${pct(ci[1])}</div>`);
    }
    // one dot per bet, stacked where odds coincide
    const place = (list, yy, draw) => {
      const groups = new Map();
      for (const p of list) { const key = Math.round(p.p * 100); if (!groups.has(key)) groups.set(key, []); groups.get(key).push(p); }
      for (const grp of groups.values()) grp.forEach((p, i) => {
        const cy = yy + STRIP / 2 + (i - (grp.length - 1) / 2) * Math.min(13, (STRIP - 14) / Math.max(1, grp.length - 1));
        draw(p, x(p.p), cy);
      });
    };
    place(scored.filter((p) => p.o === 1), yTrue, dot);
    place(scored.filter((p) => p.o === 0), yFalse, dot);
    place(waiting, yWait, ring);
    function dot(p, cx, cy) {
      const g = s("g", {}, svg);
      s("circle", { cx, cy, r: 7, fill: C.engine, stroke: C.surface2, "stroke-width": 2 }, g);
      s("rect", { x: cx - 12, y: cy - 12, width: 24, height: 24, fill: "transparent" }, g);
      tipOn(g, `<div class="t-status">${p.o ? "came true" : "did not come true"}</div><div class="t-title">${esc(p.title)}</div><div>Odds before data: <b>${pct(p.p)}</b></div><div class="t-meta">${esc(p.id)}</div>`);
    }
    function ring(p, cx, cy) {
      const g = s("g", {}, svg);
      s("circle", { cx, cy, r: 6, fill: C.surface2, stroke: C.engineSoft, "stroke-width": 2 }, g);
      s("rect", { x: cx - 10, y: cy - 10, width: 20, height: 20, fill: "transparent" }, g);
      tipOn(g, `<div class="t-status">${esc(p.why)}</div><div class="t-title">${esc(p.title)}</div><div>Odds before data: <b>${pct(p.p)}</b></div><div class="t-meta">${esc(p.id)}</div>`);
    }
  });
}
function gaugeReferee(bets, p3) {
  const el = $("g-referee");
  const mk = () => ({ scored: [], waiting: [], noOdds: 0, total: 0 });
  const sides = { model: mk(), chip: mk(), record: mk(), maths: mk() };
  const inLedger = new Set();
  for (const b of bets) {
    const side = sides[refereeOf(b.raw)];
    side.total++;
    if (b.raw.direction != null) inLedger.add(`${b.program}|${b.raw.direction}`);
    const o = outcomeOf(b);
    if (b.engine == null) { side.noOdds++; continue; }
    if (o != null) side.scored.push({ id: b.id, title: b.title, p: b.engine, o, aud: b.raw.verdict_after_audit || "" });
    else side.waiting.push({ id: b.id, title: b.title, p: b.engine, why: b.raw.scored === false && b.landed ? "settled, but not scorable by its rule" : "awaiting its result" });
  }
  // Program 3's directions carry odds before any bet is placed; they wait here until they enter the ledger.
  let p3Waiting = 0;
  for (const d of p3?.directions || []) {
    if (inLedger.has(`nature-graded|${d.id}`) || num(d.engine_odds) == null) continue;
    const side = sides[refereeOf({ referee: d.referee, program: "nature-graded" })];
    side.waiting.push({ id: d.id, title: d.title, p: num(d.engine_odds), why: "odds stated; not yet pre-registered" });
    if (side === sides.chip) p3Waiting++;
  }
  const A = sides.model, Ch = sides.chip, Rc = sides.record;
  const expChip = Ch.waiting.reduce((a, p) => a + p.p, 0);
  const bA = brier(A.scored), bC = brier(Ch.scored), bR = brier(Rc.scored);
  el.innerHTML = `<p class="g-cap g-lead">The same engine, three referees. A language model's behaviour decided programs 1 and 2's bets; the <code>ibm_fez</code> quantum chip decides program 3's; the published literature decides program 4's. The chip and the record cannot share the engine's habits. If the odds only hold up when an AI does the grading, the engine's judgment is borrowed from its grader.</p>
    <div class="refs refs3">
      <section class="ref" id="ref-ai">
        <h3 class="g-label">Model-graded</h3>
        <div class="g-value">${A.total} <span class="g-unit">bets · ${A.scored.length} settled and scored${bA != null ? ` · Brier ${f3(bA)}` : ""}</span></div>
        <div class="g-viz"></div>
        <p class="g-cap">${A.scored.length ? `${A.scored.filter((p) => p.o).length} of ${A.scored.length} came true against ${A.scored.reduce((a, p) => a + p.p, 0).toFixed(2)} expected; ${A.noOdds} more bets were placed without odds and cannot be scored.` : "Nothing settled yet."}</p>
      </section>
      <section class="ref" id="ref-chip">
        <h3 class="g-label">Chip-graded</h3>
        <div class="g-value">${Ch.total} <span class="g-unit">bets · ${Ch.scored.length} settled and scored${bC != null ? ` · Brier ${f3(bC)}` : ""}</span></div>
        <div class="g-viz"></div>
        <p class="g-cap">${Ch.scored.length ? `${Ch.scored.filter((p) => p.o).length} of ${Ch.scored.length} came true against ${Ch.scored.reduce((a, p) => a + p.p, 0).toFixed(2)} expected; ${Ch.waiting.length} more carry odds and wait.` : p3 ? `Nothing has settled: no circuit has run. If the ${Ch.waiting.length} stated odds are honest, about ${expChip.toFixed(1)} will pass.` : "Program 3's map is not deployed with the site, so this side is empty."}</p>
      </section>
      <section class="ref" id="ref-record">
        <h3 class="g-label">Record-graded</h3>
        <div class="g-value">${Rc.total} <span class="g-unit">bets · ${Rc.scored.length} settled and scored${bR != null ? ` · Brier ${f3(bR)}` : ""}</span></div>
        <div class="g-viz"></div>
        <p class="g-cap">${Rc.scored.length ? `${Rc.scored.filter((p) => p.o).length} of ${Rc.scored.length} came true against ${Rc.scored.reduce((a, p) => a + p.p, 0).toFixed(2)} expected${(() => { const u = Rc.scored.filter((p) => /unreplicated/i.test(p.aud)).length; return u ? `; the audit marked ${u === Rc.scored.length ? "every one" : u} <b>pass-unreplicated</b>: it held once, on one model and one item set` : ""; })()}.` : "Nothing settled yet."}</p>
      </section>
    </div>
    <p class="g-src">${src("ledger/bets.jsonl")} (<code>referee</code>: model, nature, published-record) · nature-graded <code>map/program-3-map.json</code>, <code>referee</code> field${sides.maths.waiting.length ? ` · ${plural(sides.maths.waiting.length, "direction")} decided by mathematics, not the chip, ${sides.maths.waiting.length === 1 ? "is" : "are"} left out` : ""} · <a href="calibration.html">full calibration chart</a></p>`;
  refPanel(el.querySelector("#ref-ai .g-viz"), { scored: A.scored, waiting: A.waiting, emptyText: "nothing settled yet" });
  refPanel(el.querySelector("#ref-chip .g-viz"), { scored: Ch.scored, waiting: Ch.waiting, emptyText: "nothing settled yet" });
  refPanel(el.querySelector("#ref-record .g-viz"), { scored: Rc.scored, waiting: Rc.waiting, emptyText: "nothing settled yet" });
  void p3Waiting;
}

// ---------- timeline ----------
function dayKey(d) { return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`; }
function gaugeTimeline(bets, maps, p3) {
  const ev = [];
  const push = (when, kind, status, title, id, note) => { const d = parseDate(when); if (d) ev.push({ d, kind, status, title, id, note }); };
  for (const b of bets) {
    push(b.opened, "placed", "running", b.title, b.id, "pre-registered");
    if (b.landed && ["hit", "mixed", "killed"].includes(b.status))
      push(b.landed, b.status === "killed" ? "killed" : "settled", b.status, b.title, b.id, b.verdictRaw ? `verdict: ${b.verdictRaw}` : "");
  }
  // Phase-A results came before the ledger began; the map carries them with their own dates.
  for (const p of maps) for (const d of p.directions) {
    if (d.raw.bets?.length || d.bet || !["hit", "mixed", "killed"].includes(d.status)) continue;
    push(d.opened, "placed", "running", d.title, d.id, "phase A (from the map)");
    push(d.resolved, d.status === "killed" ? "killed" : "settled", d.status, d.title, d.id, "phase A (from the map)");
  }
  const odds = [];
  for (const d of p3?.directions || []) { const w = parseDate(d.engine_odds_at); if (w) odds.push({ d: w, id: d.id, title: d.title }); }
  const el = $("g-timeline");
  if (!ev.length) { el.innerHTML = `<div class="empty">No dated bets yet.</div>`; return; }
  const all = [...ev.map((e) => e.d), ...odds.map((o) => o.d)];
  const first = new Date(Math.min(...all)); first.setHours(0, 0, 0, 0);
  const today = new Date(); today.setHours(0, 0, 0, 0);
  const lastEv = new Date(Math.max(...all)); lastEv.setHours(0, 0, 0, 0);
  const end = today > lastEv ? today : lastEv;
  const days = [];
  for (let d = new Date(first); d <= end; d.setDate(d.getDate() + 1)) days.push(new Date(d));
  const byDay = new Map(days.map((d) => [dayKey(d), { d, placed: [], settled: [], killed: [], odds: [] }]));
  for (const e of ev.sort((a, b) => a.d - b.d)) byDay.get(dayKey(e.d))?.[e.kind].push(e);
  for (const o of odds) byDay.get(dayKey(o.d))?.odds.push(o);

  const placed = ev.filter((e) => e.kind === "placed").length, settled = ev.filter((e) => e.kind === "settled").length, killed = ev.filter((e) => e.kind === "killed").length;
  const open = placed - settled - killed;
  const LANES = [["placed", "Placed", "running"], ["settled", "Settled", null], ["killed", "Killed", "killed"]];
  // Runs of quiet days fold into one line, so a long gap does not push the record off the screen.
  const rows = [];
  let quiet = [];
  const flush = () => { if (quiet.length) rows.push({ quiet: quiet.slice() }); quiet = []; };
  for (const day of byDay.values()) {
    const n = day.placed.length + day.settled.length + day.killed.length + day.odds.length;
    if (!n && day.d.getTime() !== today.getTime()) { quiet.push(day); continue; }
    flush(); rows.push(day);
  }
  flush();
  el.innerHTML = `<div class="g-value">${placed} <span class="g-unit">bets placed in ${plural(days.length, "day")} · ${settled} settled · ${killed} killed · ${open} still running</span></div>
    <p class="g-cap">Each bet is placed (pre-registered) before any data, then it settles or dies.${open > 0 ? ` ${plural(open, "bet")} ${open === 1 ? "is" : "are"} still out.` : ""} A hit every day would be a warning sign; kills are the method working.</p>
    <div class="key small g-key"><span>${markSVG("running", 15)} placed (pre-registered)</span><span>${markSVG("hit", 15)} came true</span><span>${markSVG("mixed", 15)} mixed</span><span>${markSVG("killed", 15)} killed</span></div>
    <ol class="tl">${rows.map((r) => r.quiet ? `<li class="tl-quiet">${r.quiet.length === 1 ? fmtDate(r.quiet[0].d, false) : `${fmtDate(r.quiet[0].d, false)} – ${fmtDate(r.quiet.at(-1).d, false)}`}: nothing placed, settled or killed</li>` : `
      <li class="tl-day">
        <div class="tl-date">${fmtDate(r.d, false)}${r.d.getTime() === today.getTime() ? ` <span class="muted">today</span>` : ""}</div>
        <div class="tl-lanes">${LANES.map(([k, word]) => `<div class="tl-lane"><span class="tl-word">${word} <b>${r[k].length}</b></span><span class="tl-marks">${
          r[k].map((e, i) => `<span class="tm" data-k="${k}" data-i="${i}">${markSVG(e.status, 16)}</span>`).join("") || `<span class="muted small">—</span>`}</span></div>`).join("")}
        ${r.odds.length ? `<div class="tl-note"><svg width="16" height="16" aria-hidden="true"><circle cx="8" cy="8" r="6" fill="none" stroke="${C.engineSoft}" stroke-width="2"/></svg> ${plural(r.odds.length, "program-3 direction")} given odds by the engine (not yet pre-registered, so not placed)</div>` : ""}</div>
      </li>`).join("")}</ol>
    <p class="g-src">${src("ledger/bets.jsonl")} (<code>prereg_time</code>, <code>result_time</code>, <code>verdict</code>) · phase-A results from ${src("map/entangled-mind.json")} · times America/Denver</p>`;
  const dayRows = rows.filter((r) => !r.quiet);
  el.querySelectorAll(".tl-day").forEach((li, di) => {
    const r = dayRows[di];
    li.querySelectorAll(".tm").forEach((m) => {
      const e = r[m.dataset.k][+m.dataset.i];
      tipOn(m, `<div class="t-status">${markSVG(e.status, 13)} ${m.dataset.k} · ${esc(fmtDate(e.d))}</div><div class="t-title">${esc(e.title)}</div><div class="t-meta">${esc(e.id)}${e.note ? " · " + esc(e.note) : ""}</div>`);
    });
  });
}

// ---------- page ----------
(async () => {
  const [bets, maps, kills, auditMd, ibm, apiMd, ctxMd, p3, plants, lessons, spend, r2Md] = await Promise.all([
    loadBets(), loadMaps(), loadKills(),
    getText(DATA + EM + "audits/SUMMARY.md"),
    getJSON(DATA + EM + "results/ibm-usage.json"),
    getText(DATA + EM + "results/api-usage.md"),
    getText(DATA + "engine/CONTEXT.md"),
    getJSON(DATA + NG + "map/program-3-map.json"),
    getJSONL(DATA + "ledger/plants.jsonl"),
    getJSONL(DATA + "ledger/lessons.jsonl"),
    getJSONL(DATA + "ledger/spend.jsonl"),
    getText(DATA + "ledger/audits/SUMMARY-2.md"),
  ]);
  const r2 = roundTwo(r2Md);
  const ctx = readContext(ctxMd);
  const audit = readAudit(auditMd);
  const scored = (side) => bets.flatMap((b) => {
    const o = outcomeOf(b), p = side === "engine" ? b.engine : b.human;
    return o != null && p != null ? [{ p, o, id: b.id, title: b.title }] : [];
  });
  const run = (f) => { try { f(); } catch (e) { console.error(e); } };
  run(() => gaugeEngineBrier(scored("engine")));
  run(() => gaugeHumanBrier(bets, scored("human"), p3));
  run(() => gaugeHits(scored("engine")));
  run(() => gaugeStability(p3));
  run(() => gaugeOverclaim(audit, bets, r2));
  run(() => gaugeReversal(audit, bets, r2));
  run(() => gaugeCatch(plants));
  run(() => gaugeKills(kills, p3));
  run(() => gaugeLearning(bets, lessons));
  run(() => gaugeAPI(ctx, bets, apiMd, spend));
  run(() => gaugeQPU(ibm, ctx, p3));
  run(() => gaugeReferee(bets, p3));
  run(() => gaugeTimeline(bets, maps, p3));
})();
