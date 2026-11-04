// One paper, rendered from markdown: readable measure, a contents list, figures and links that work.
import { header, esc, slug, wrapTables } from "./common.js";
import { loadPaper, linkCommits, firstHeading } from "./papers-common.js";

header();
const main = document.getElementById("main");
const name = new URLSearchParams(location.search).get("p") || "no-credence-to-read";

function isAbsolute(u) { return /^(?:[a-z]+:)?\/\//i.test(u) || u.startsWith("#") || u.startsWith("mailto:"); }

(async () => {
  const { text, base, repo, blobBase } = await loadPaper(name);
  if (!text) {
    main.innerHTML = `<h1>Not found</h1><div class="empty">There is no paper called <code>${esc(name)}</code>. <a href="papers.html">See all papers</a>.</div>`;
    return;
  }
  const title = firstHeading(text) || name;
  document.title = title.length > 60 ? title.slice(0, 57) + "…" : title;
  main.innerHTML = `<div class="paper-layout"><article class="prose" id="doc"></article><nav class="toc" id="toc" aria-label="Contents"></nav></div>`;
  const doc = document.getElementById("doc");
  doc.innerHTML = `<p class="paper-meta"><a href="papers.html">← All papers</a> · <a href="${blobBase}${esc(name.replace(/^engine\//, ""))}.md">source on GitHub</a></p>` + window.marked.parse(text, { breaks: true });

  // figures and links relative to the paper's folder
  doc.querySelectorAll("img").forEach((img) => {
    const src = img.getAttribute("src");
    if (src && !isAbsolute(src) && !src.startsWith("data:")) img.src = base + src;
    img.loading = "lazy";
    if (/\.svg($|\?)/i.test(img.src)) img.classList.add("figure-invert");
  });
  doc.querySelectorAll("a[href]").forEach((a) => {
    const href = a.getAttribute("href");
    if (!href || isAbsolute(href)) return;
    const m = href.match(/^(?:\.\/)?([\w.-]+)\.md(#.*)?$/);
    if (m && !name.startsWith("engine/")) { a.href = `paper.html?p=${encodeURIComponent(m[1])}${m[2] || ""}`; return; }
    a.href = new URL(href, blobBase).href;      // ../results/x.md and the like: open on GitHub
  });
  wrapTables(doc);
  linkCommits(doc, repo);

  // contents list from h2s; ids on every heading
  const used = new Set();
  doc.querySelectorAll("h1, h2, h3").forEach((h) => {
    let id = slug(h.textContent) || "s";
    while (used.has(id)) id += "-";
    used.add(id);
    h.id = id;
  });
  const h2s = [...doc.querySelectorAll("h2")];
  document.getElementById("toc").innerHTML = h2s.length > 2
    ? `<b>Contents</b>${h2s.map((h) => `<a href="#${h.id}">${esc(h.textContent)}</a>`).join("")}` : "";
  if (location.hash) document.getElementById(decodeURIComponent(location.hash.slice(1)))?.scrollIntoView();
})();
