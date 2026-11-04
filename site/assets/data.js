// Loads the ledger and the maps, and joins them. Every page reads through here.
import { DATA, getJSON, getJSONL, getText, manifest, normBet, normStatus, num } from "./common.js";

const FALLBACK_MAPS = ["entangled-mind.json", "other-minds.json"];

export async function loadBets() {
  const rows = (await getJSONL(DATA + "ledger/bets.jsonl")) || [];
  return rows.map(normBet);
}

export async function loadSteers() {
  return (await getJSONL(DATA + "ledger/steers.jsonl")) || [];
}

export async function loadBrierMd() {
  return getText(DATA + "ledger/brier.md");
}

// map/<program>.json, or one file holding {programs:[...]}
export async function loadMaps() {
  const m = await manifest();
  const names = (m.map && m.map.length ? m.map : FALLBACK_MAPS).filter((n) => n.endsWith(".json"));
  const got = await Promise.all(names.map((n) => getJSON(DATA + "map/" + n)));
  const programs = [];
  got.forEach((g, i) => {
    if (!g) return;
    const list = Array.isArray(g.programs) ? g.programs : [g];
    for (const p of list) programs.push(normProgram(p, names[i].replace(/\.json$/, "")));
  });
  return programs;
}

function normProgram(p, fallbackId) {
  const dirs = p.directions || p.nodes || p.map || [];
  return {
    id: p.program || p.id || fallbackId,
    title: p.title || p.name || p.program || fallbackId,
    seed: p.seed_question || p.question || p.seed || "",
    seedDate: p.seed_date || p.opened || "",
    directions: dirs.map((d) => ({
      raw: d,
      id: String(d.id ?? d.direction ?? d.title),
      parent: d.parent ?? d.parent_id ?? d.from ?? null,
      title: d.title || d.label || d.name || d.assumption_at_stake || String(d.id),
      label: d.short || d.label || null,
      status: normStatus(d.status ?? d.verdict ?? d.state),
      engine: num(d.engine_odds ?? d.engine_p ?? d.odds ?? d.p),
      human: num(d.human_odds ?? d.human_p),
      cost: d.cost || d.cheapest_test_cost || "",
      test: d.cheapest_test || d.test || "",
      diagnosis: d.diagnosis || "",
      result: d.result || "",
      opened: d.opened || d.created || d.date_opened || "",
      resolved: d.resolved || d.closed || d.date_resolved || "",
    })),
  };
}

// A bet in the ledger is fresher than the map: its verdict, odds and dates win.
// A node links to bets by id ("bets": [...]); failing that, by direction id within the same program.
export function joinBets(programs, bets) {
  for (const p of programs) {
    for (const d of p.directions) {
      const ids = [].concat(d.raw.bets || d.raw.bet || []).map(String);
      const b = ids.length ? bets.find((x) => x.id === ids[0])
        : bets.find((x) => (!x.program || x.program === p.id) && x.direction !== "" && String(x.direction) === d.id);
      if (!b) continue;
      d.bet = b;
      d.status = b.status;
      if (b.engine != null) d.engine = b.engine;
      if (b.human != null) d.human = b.human;
      if (b.diagnosis) d.diagnosis = b.diagnosis;
      if (b.result) d.result = b.result;
      if (b.cost) d.cost = b.cost;
      if (!d.opened) d.opened = b.opened || "";
      if (b.landed && b.status !== "open" && b.status !== "running") d.resolved = b.landed;
    }
  }
  return programs;
}

// Kills come from three places; nothing is dropped, duplicates are merged.
export async function loadKills() {
  const [explicit, bets, maps] = await Promise.all([
    getJSONL(DATA + "ledger/kills.jsonl"), loadBets(), loadMaps(),
  ]);
  joinBets(maps, bets);
  const out = [];
  const seen = new Map();
  const add = (k) => {
    const key = (k.key ? `bet|${k.key}` : `${k.program}|${k.direction || k.title}`).toLowerCase();
    if (seen.has(key)) {
      const prev = seen.get(key);
      for (const f of ["diagnosis", "evidence", "date", "title", "prereg"]) if (!prev[f] && k[f]) prev[f] = k[f];
      return;
    }
    seen.set(key, k);
    out.push(k);
  };
  for (const k of explicit || []) add({
    program: k.program || "", direction: String(k.direction ?? k.id ?? ""), title: k.title || k.direction || "",
    diagnosis: k.diagnosis || k.why || "", evidence: k.evidence || "", date: k.date || "", prereg: k.prereg_commit || "",
  });
  for (const p of maps) for (const d of p.directions) if (d.status === "killed") add({
    program: p.id, programTitle: p.title, direction: d.id, title: d.title, diagnosis: d.diagnosis,
    evidence: d.result || "", date: d.resolved || "", prereg: d.bet?.prereg || "", bet: d.bet || null,
    key: d.bet ? d.bet.id : null,
  });
  for (const b of bets) if (b.status === "killed") add({
    program: b.program, direction: String(b.direction || b.id), title: b.title, diagnosis: b.diagnosis,
    evidence: b.result, date: b.landed || b.date, prereg: b.prereg, bet: b, key: b.id,
  });
  const titles = Object.fromEntries(maps.map((p) => [p.id, p.title]));
  for (const k of out) k.programTitle = k.programTitle || titles[k.program] || k.program;
  return out;
}
