// Loading and rendering the programs' markdown.
import { DATA, SITE, getText, esc } from "./common.js";

// The reading list, in the order a newcomer should read it. Anything else in paper/ is listed after these.
export const CATALOG = [
  { p: "no-credence-to-read", kind: "Main paper", blurb: "The live finding. A model's stated confidence is built by the question, the format and its own transcript. There is no stored credence for it to read out." },
  { p: "the-entangled-mind-paper", kind: "Short paper · negative result", blurb: "The original hypothesis, and how it died. Entangled belief states do not help a model judge, and here is the diagnosis." },
  { p: "clonable-minds", kind: "Theory note", blurb: "A model's state is a copyable string, so every order effect it shows must come from the question disturbing it. That is why editing the transcript can tell the causes apart." },
  { p: "one-page", kind: "One page", blurb: "The whole program on one page." },
  { p: "gold-map", kind: "Map", blurb: "Eleven candidate directions after experiment 5, each with its odds, cost and cheapest test." },
  { p: "biomimetic-map", kind: "Map", blurb: "Ten brain mechanisms scored against the measured fingerprint." },
  { p: "related-work", kind: "Related work", blurb: "Literature notes for the original program: what each paper tested and what we borrowed." },
  { p: "record", kind: "Record", blurb: "Every test in order. There is also a timeline view.", href: "record.html" },
  { p: "next-steps", kind: "Working note", blurb: "The pivot from error prediction to sequential judgment, with each outcome's reading fixed in advance." },
  { p: "morning-brief", kind: "Working note", blurb: "The overnight run, summarised for the morning: what ran and what it found." },
  { p: "the-entangled-mind-v3", kind: "Earlier draft", blurb: "Version 3 of the original paper, written while the quantum hypothesis was still open." },
  { p: "thought-experiment-v2", kind: "Earlier draft", blurb: "The plain-language companion to the proposal." },
  { p: "window-vignettes", kind: "Retired", blurb: "Notes from the “window” visualiser, which was retired because it was too complicated to help anyone." },
];
export const ENGINE_DOCS = [
  { p: "engine/proposal", title: "The testbed's research proposal", kind: "Engine · proposal", blurb: "The research proposal for the testbed itself: five questions about calibration, audit, human oversight, path dependence and where good bets come from." },
];
const SKIP = new Set(["README"]);

// name "x" → program 1's paper/x.md; "engine/x" → the engine's own x.md
export async function loadPaper(name) {
  const prog = SITE.programs["entangled-mind"];
  if (name.startsWith("engine/")) {
    const f = name.slice(7);
    return { text: await getText(`${DATA}engine/${f}.md`), base: `${DATA}engine/`, repo: SITE.engineRepo, blobBase: `${SITE.engineRepo}/blob/main/` };
  }
  const base = `${DATA}programs/entangled-mind/paper/`;
  let text = await getText(`${base}${name}.md`);
  let usedBase = base;
  if (text == null) { // not copied at deploy: read the public repository directly
    text = await getText(`${prog.raw}paper/${name}.md`);
    usedBase = `${prog.raw}paper/`;
  }
  return { text, base: usedBase, repo: prog.home, blobBase: `${prog.blob}paper/` };
}

// Short commit hashes in code spans become links to the commit.
export function linkCommits(root, repo) {
  root.querySelectorAll("code").forEach((c) => {
    if (c.closest("a") || c.closest("pre")) return;
    const t = c.textContent.trim();
    if (/^[0-9a-f]{7,12}$/.test(t)) {
      const a = document.createElement("a");
      a.href = `${repo}/commit/${t}`;
      a.title = "Open this commit on GitHub";
      c.replaceWith(a);
      a.append(c);
    }
  });
}

export function firstHeading(md) {
  const m = md && md.match(/^#\s+(.+)$/m);
  return m ? m[1].trim() : null;
}

export function listFromManifest(m) {
  const known = new Set(CATALOG.map((c) => c.p));
  const extra = (m.papers || []).map((f) => f.replace(/\.md$/, "")).filter((p) => !known.has(p) && !SKIP.has(p));
  const present = new Set((m.papers || []).map((f) => f.replace(/\.md$/, "")));
  const items = CATALOG.filter((c) => !m.papers || present.has(c.p));
  return [...ENGINE_DOCS, ...items, ...extra.map((p) => ({ p, kind: "Document", blurb: "" }))];
}
export { esc };
