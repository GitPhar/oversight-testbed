// Plain words on every page (site walk 2026-11-05; panel review, Part 3 "Anything a reader cannot follow"):
//   1. every bet id, on its first use on the page, carries its plain question beside it, read from
//      map/plain-questions.jsonl and the other plain sources in data.js loadPlainQuestions (never typed here);
//   2. Brier, pre-registration, plant and steer each get one glossary line where they first appear on the page.
// It runs on the page's <main> once the page has finished drawing (no change for a moment), and again after any later
// redraw (a map tab, a filter), so a first use that was redrawn away is annotated again. SVG text, code, closed folds
// and tooltips are left alone.
import { esc } from "./common.js";
import { loadBets, loadMaps, loadPlainQuestions } from "./data.js";

// One line each, in plain words. These are definitions, not ledger numbers.
export const GLOSSARY = [
  { key: "brier", re: /\bBrier\b/, term: "Brier score",
    def: "the average of (stated odds − what happened)², where what happened is 1 if the test passed and 0 if not. 0 is perfect; always saying 50% scores 0.25; lower is better." },
  { key: "prereg", re: /\bpre-?regist(?:er|ers|ered|ering|ration|rations)\b/i, term: "Pre-registration",
    def: "the test's pass rule, statistic and budget, written down and committed before any data are seen, so the bar cannot move afterwards." },
  { key: "plant", re: /\b(?:plants?|planted (?:claims?|mistakes?))\b/i, term: "Plant",
    def: "a known mistake slipped in secret into a result before its audit, to measure whether the auditor catches it." },
  { key: "steer", re: /\bsteer(?:s|ed|ing)?\b/i, term: "Steer",
    def: "a decision by the human, Sean, that changes what the engine does (a seed question, a veto, a rule, a budget, his odds); each is logged and later valued as helped, neutral or hurt." },
];

const SKIP = "svg, code, pre, script, style, button, select, textarea, input, .tip, .pq, .gloss, [data-plain-skip]";
const BLOCK = "p, li, td, th, dd, dt, h1, h2, h3, h4, figcaption, summary, .note, .label, .value, div";

function visibleText(node) {
  const el = node.parentElement;
  if (!el || el.closest(SKIP)) return false;
  // inside a closed fold (but not its summary): not seen until opened
  const d = el.closest("details");
  if (d && !d.open && !el.closest("summary")) return false;
  return !el.closest("[hidden]");
}

function textNodes(root) {
  const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, { acceptNode: (n) => (n.nodeValue.trim() && visibleText(n) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT) });
  const out = [];
  for (let n = w.nextNode(); n; n = w.nextNode()) out.push(n);
  return out;
}

// Split a text node so [start, end) is its own node; returns that node.
function isolate(node, start, end) {
  const mid = node.splitText(start);
  mid.splitText(end - start);
  return mid;
}

// Where an inline note goes: after the outermost inline wrapper (a link, bold, a span) inside the block.
function afterInline(node) {
  let n = node;
  while (n.parentElement && n.parentElement.matches("a, b, strong, em, i, span, abbr, label") && !n.parentElement.matches(".hh-q, .hc-q, .f-said, .ev-q, .t-title")) n = n.parentElement;
  return n;
}

function annotateIds(main, pq, idRe) {
  if (!idRe) return 0;
  let added = 0;
  const present = new Set([...main.querySelectorAll(".pq[data-pq]")].map((e) => e.dataset.pq));
  for (const node of textNodes(main)) {
    idRe.lastIndex = 0;
    let m;
    while ((m = idRe.exec(node.nodeValue))) {
      const id = m[1];
      if (present.has(id)) continue;
      present.add(id);
      const info = pq.get(id);
      const q = info?.q || info?.title;
      if (!q) continue;
      const block = node.parentElement.closest(BLOCK) || node.parentElement;
      // the plain question is already beside the id (the calibration page's human column, the human page)
      const bt = block.textContent, at = bt.indexOf(id);
      if (at >= 0 && bt.slice(Math.max(0, at - 200), at + id.length + 200).includes(q.slice(0, 70))) continue;
      const hit = isolate(node, m.index, m.index + id.length);
      const span = document.createElement("span");
      span.className = "pq";
      span.dataset.pq = id;
      span.title = info?.q ? `Plain question, from ${info.from}` : "The ledger's title for this bet (no plain question is on file for it yet)";
      span.textContent = ` (${q.replace(/\s*\.$/, "")})`;
      afterInline(hit).after(span);
      added++;
      break;   // the node was split; the rest of it is the next text node, which the outer loop does not see, so rescan later
    }
  }
  return added;
}

function glossOnce(main) {
  let added = 0;
  for (const g of GLOSSARY) {
    if (main.querySelector(`.gloss[data-gloss="${g.key}"]`)) continue;
    const node = textNodes(main).find((n) => g.re.test(n.nodeValue));
    if (!node) continue;
    const el = node.parentElement;
    const block = el.closest(BLOCK) || el;
    const line = document.createElement(block.matches("h1, h2, h3, h4, summary, .label, .value, div") ? "p" : "span");
    line.className = "gloss";
    line.dataset.gloss = g.key;
    line.innerHTML = `<b>${esc(g.term)}:</b> ${esc(g.def)}`;
    if (block.matches("h1, h2, h3, h4")) block.after(line);
    else if (block.matches("summary")) block.closest("details").after(line);
    else if (block.matches(".label, .value")) (block.closest(".stat") || block).append(line);
    else if (block.matches("div") && block.children.length) block.prepend(line);
    else block.append(line);
    added++;
  }
  return added;
}

export async function start() {
  const main = document.querySelector("main");
  if (!main) return;
  const [bets, maps] = await Promise.all([loadBets(), loadMaps()]);
  const pq = await loadPlainQuestions(bets, maps);
  const ids = [...pq.keys()].filter(Boolean).sort((a, b) => b.length - a.length).map((s) => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));
  const idRe = ids.length ? new RegExp(`(?<![\\w-])(${ids.join("|")})(?![\\w-])`, "g") : null;
  let timer = null, obs = null;
  const run = () => {
    obs.disconnect();
    // repeated until nothing changes: a split text node hides the rest of itself from one pass
    for (let i = 0; i < 400 && annotateIds(main, pq, idRe); i++);
    glossOnce(main);
    obs.observe(main, { childList: true, subtree: true });
  };
  obs = new MutationObserver(() => { clearTimeout(timer); timer = setTimeout(run, 400); });
  obs.observe(main, { childList: true, subtree: true });
  main.addEventListener("toggle", () => { clearTimeout(timer); timer = setTimeout(run, 100); }, true);   // a fold opened
  timer = setTimeout(run, 700);
}
