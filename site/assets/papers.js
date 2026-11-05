import { header, esc, manifest } from "./common.js";
import { listFromManifest, loadPaper, firstHeading } from "./papers-common.js";

header();
const main = document.getElementById("main");

const GROUPS = [
  ["Read these first", (k) => /plain words|main paper|short paper|theory|one page/i.test(k)],
  ["The maps and the record", (k) => /map|record|related/i.test(k)],
  ["The engine", (k) => /engine/i.test(k)],
  ["Working notes and earlier drafts", () => true],
];

(async () => {
  const m = await manifest();
  const items = listFromManifest(m);
  main.innerHTML = `<h1>Papers</h1>
    <p class="how">The write-ups from the programs, as pages you can read here. Each one is rendered straight from the repository's markdown, so it is always the current version. Start with the first group.</p>
    <div id="groups"></div>`;
  const placed = new Set();
  let html = "";
  for (const [name, test] of GROUPS) {
    const g = items.filter((it) => !placed.has(it.p) && test(it.kind));
    if (!g.length) continue;
    g.forEach((it) => placed.add(it.p));
    html += `<h2>${name}</h2><ul class="papers">${g.map((it) => `<li><a href="${it.href || "paper.html?p=" + encodeURIComponent(it.p)}" data-p="${esc(it.p)}">
      <div class="kind">${esc(it.kind)}</div><b>${esc(it.p.replace(/^engine\//, "").replace(/-/g, " "))}</b>${it.blurb ? `<span>${esc(it.blurb)}</span>` : ""}</a></li>`).join("")}</ul>`;
  }
  document.getElementById("groups").innerHTML = html;
  // Replace file names with each document's own title.
  document.querySelectorAll("[data-p]").forEach(async (a) => {
    const { text } = await loadPaper(a.dataset.p);
    const fixed = items.find((it) => it.p === a.dataset.p)?.title;
    const t = fixed || firstHeading(text);
    if (t) a.querySelector("b").textContent = t;
    else if (text == null) a.closest("li").remove();
  });
})();
