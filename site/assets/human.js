// The human hand: Sean's odds beside the engine's, direction by direction, with outcomes and both scores.
// Every number is read from files when the page loads: ledger/human-odds.jsonl (Sean's lines, saved from the
// cockpit), ledger/bets.jsonl (the engine's pre-registered odds, outcomes, and which bets carry Sean's odds),
// map/*.json (the engine's odds on a direction with no bet yet), ledger/steers.jsonl (his steers) and
// ledger/steer-values.jsonl (what each steer was worth, under operators/steers.md).
import { header, esc, inline, parseDate, fmtDate, programTitle, page } from "./common.js";
import { loadBets, loadMaps, loadSteers, loadHumanOdds, loadSteerValues } from "./data.js";

header();
const main = document.getElementById("main");
const pct = (p) => `${Math.round(p * 100)}%`;
const GOLD = "#f2c14e", ENG = "#ece9e2", HIT = "#5cc98a", KILL = "#e47272";
// "program-2-map P2-6" -> "P2-6", the same rule as ledger/human_odds_match.py
const token = (d) => String(d ?? "").trim().split(/\s+/).pop() || "";
const brier = (rows, k) => rows.length ? rows.reduce((a, r) => a + (r[k] - r.outcome) ** 2, 0) / rows.length : null;
const ACTION = {
  choose_seed: "Chose a seed question", set_rule: "Set a rule", add_question: "Added a question", veto: "Vetoed a direction",
  architecture: "Decided how the system works", budget: "Set a budget", set_frame: "Set the frame", human_odds: "Gave his own odds",
};

function rowsFrom(lines, bets, maps) {
  // The first line for a direction is the one that counts (the cockpit's rule, and data.js joinHumanOdds).
  const first = new Map();
  for (const o of [...lines].sort((a, b) => String(a.recorded).localeCompare(String(b.recorded)))) {
    const k = `${o.program}|${o.direction}`;
    if (!first.has(k)) first.set(k, o);
  }
  const out = [], noEngine = [];
  for (const o of first.values()) {
    const cands = bets.filter((b) => b.program === o.program && token(b.direction) === o.direction && b.raw.verdict !== "withdrawn")
      .sort((a, b) => String(a.raw.prereg_time).localeCompare(String(b.raw.prereg_time)));
    const bet = cands.find((b) => b.human != null) || cands[0] || null;
    const prog = maps.find((p) => p.id === o.program);
    const dir = prog?.directions.find((d) => d.id === o.direction);
    const mapOdds = dir?.raw?.engine_odds ?? null;
    const engine = bet?.engine ?? mapOdds;
    if (engine == null || o.human_odds == null) { noEngine.push(o); continue; }
    const r = bet?.raw;
    const settled = bet && bet.status !== "running" && bet.status !== "open";
    const outcome = r && r.scored === true && !r.secondary_of && (r.outcome === 0 || r.outcome === 1) ? r.outcome : null;   // rule 15: one scored bet per run
    out.push({
      o, bet, dir, prog, engine, human: +o.human_odds, mapOdds,
      engineFrom: bet ? `bet ${bet.id}, pre-registered ${fmtDate(parseDate(r.prereg_time))}` : `the map's odds for ${o.direction} (no bet yet)`,
      engineEvent: bet ? bet.oddsEvent : dir?.raw?.odds_event || "",
      outcome, settled,
      counts: !!(bet && bet.human != null && outcome != null),
      carries: bet ? bet.human != null : null,
      note: r?.human_odds_note || "",
    });
  }
  const n = (r) => +(String(programTitle(r.o.program, maps)).match(/\d+/)?.[0] || 99);
  out.sort((a, b) => n(a) - n(b) || String(a.o.direction).localeCompare(String(b.o.direction), undefined, { numeric: true }));
  return { rows: out, noEngine };
}

// One line from 0% to 100%, the engine's mark and Sean's, and the outcome at the end it landed on.
function lineSVG(r) {
  // drawn at about the size it is shown, so the labels stay readable on a phone
  const W = window.innerWidth < 640 ? Math.max(300, window.innerWidth - 60) : 560, H = 64, L = 18, R = 18, y = 38;
  const x = (p) => L + p * (W - L - R);
  const xe = x(r.engine), xh = x(r.human);
  const close = Math.abs(xe - xh) < 78;
  const lo = xe <= xh ? "e" : "h";
  const lab = (who, xx, txt, col) => {
    const anchor = close ? ((who === lo) ? "end" : "start") : "middle";
    const dx = close ? (who === lo ? 4 : -4) : 0;
    return `<text x="${xx + dx}" y="${y - 16}" text-anchor="${anchor}" fill="${col}" font-size="14" font-weight="700">${txt}</text>`;
  };
  let out = "";
  if (r.outcome != null) {
    const xo = x(r.outcome), c = r.outcome ? HIT : KILL;
    out = `<rect x="${xo - 3}" y="${y - 9}" width="6" height="18" rx="2" fill="${c}"/>
      <text x="${xo + (r.outcome ? -8 : 8)}" y="${y + 24}" text-anchor="${r.outcome ? "end" : "start"}" fill="${c}" font-size="13" font-weight="700">${r.outcome ? "came true" : "did not come true"}</text>`;
  }
  const ticks = [0, 0.25, 0.5, 0.75, 1].map((p) => `<line x1="${x(p)}" x2="${x(p)}" y1="${y - 4}" y2="${y + 4}" stroke="#4a525c"/>
    <text x="${x(p)}" y="${y + 20}" text-anchor="middle" fill="#8d8a82" font-size="12">${p * 100}%</text>`).join("");
  return `<svg viewBox="0 0 ${W} ${H}" width="100%" role="img" aria-label="Engine ${pct(r.engine)}, Sean ${pct(r.human)}${r.outcome != null ? `, ${r.outcome ? "came true" : "did not come true"}` : ""}">
    <line x1="${L}" x2="${W - R}" y1="${y}" y2="${y}" stroke="#3a414a" stroke-width="2"/>${ticks}
    <line x1="${xe}" x2="${xh}" y1="${y}" y2="${y}" stroke="${GOLD}" stroke-opacity="0.45" stroke-width="4"/>
    ${out}
    <circle cx="${xe}" cy="${y}" r="7.5" fill="#191c20" stroke="${ENG}" stroke-width="2.6"/>
    <path d="M${xh} ${y - 9}L${xh + 9} ${y}L${xh} ${y + 9}L${xh - 9} ${y}Z" fill="${GOLD}" stroke="#191c20" stroke-width="1.5"/>
    ${lab("e", xe, `Engine ${pct(r.engine)}`, ENG)}${lab("h", xh, `Sean ${pct(r.human)}`, GOLD)}
  </svg>`;
}

// Who scored the steers, said honestly and from the lines themselves (scored_by, scorer_wrote_steer), not typed.
function scorerSentence(valued, scorers, scoredOn) {
  if (!valued.length) return "No steer has been scored yet.";
  const wrote = valued.filter((v) => v.scorer_wrote_steer === true).length, unknown = valued.filter((v) => typeof v.scorer_wrote_steer !== "boolean").length;
  const claude = scorers.every((x) => /claude/i.test(x));
  return `The scorer is ${scorers.length === 1 ? "one session" : `${scorers.length} sessions`} (${esc(scorers.join("; "))})${scoredOn.length ? `, scoring on ${esc(scoredOn.join(", "))}` : ""}` +
    `${claude ? ", a Claude model: the same model family that runs the engine Sean steers, so it is not an independent judge" : ""}. ` +
    (wrote ? `It wrote ${wrote} of the steers it scored.` : unknown ? `On ${unknown} line${unknown === 1 ? "" : "s"} it is not recorded whether it wrote the steer.` : "It did not write any of the steers it scored.");
}

function rowHTML(r, maps) {
  const status = r.outcome != null ? (r.outcome ? "Came true" : "Did not come true")
    : r.bet ? (r.settled ? `Settled, not scored (${esc(r.bet.verdictRaw)})` : "Bet placed, no result yet") : "No bet placed yet";
  const counts = r.counts ? `<span class="hh-tag yes">counts toward both scores</span>`
    : r.bet && r.carries === false ? `<span class="hh-tag no">does not count: this bet was pre-registered before his line reached the ledger</span>`
    : r.bet && r.carries ? `<span class="hh-tag">carries his odds; counts once it settles</span>`
    : `<span class="hh-tag">the next bet on this direction must carry his line</span>`;
  const sameEvent = !r.engineEvent || r.engineEvent.trim() === String(r.o.event || "").trim();
  const det = [
    ["Sean's line", `${esc(r.o.id)}, saved ${esc(fmtDate(parseDate(r.o.recorded)))} from the cockpit; he ${r.o.saw_engine_odds ? "had" : "had not"} seen the engine's odds`],
    ["Would he spend it?", `${r.o.worth_spend === true ? "Yes" : r.o.worth_spend === false ? "No" : "Not answered"}${r.o.spend_asked ? ` (${esc(r.o.spend_asked)})` : ""}`],
    ["Expects a hit?", r.o.expects_hit === true ? "Yes" : r.o.expects_hit === false ? "No" : "Not answered"],
    ["The event his odds are for", inline(r.o.event || "")],
    ["The engine's number", `${pct(r.engine)}, from ${esc(r.engineFrom)}${r.bet && r.mapOdds != null && Math.abs(r.mapOdds - r.engine) > 1e-9 ? `; the map said ${pct(r.mapOdds)} before the bet` : ""}`],
    sameEvent ? null : ["The engine's event", `${inline(r.engineEvent)} <span class="muted">(worded differently from his; the bet's own event is what it is scored on)</span>`],
    r.note && r.bet && !r.carries ? ["Why the bet does not carry his odds", esc(r.note)] : null,
    r.bet?.result && r.settled ? ["Result", inline(r.bet.result)] : null,
  ].filter(Boolean);
  return `<li class="hh-row">
    <div class="hh-top"><span>${esc(programTitle(r.o.program, maps))} · <b>${esc(r.o.direction)}</b></span><span class="hh-st">${status}</span></div>
    <p class="hh-q">${esc(r.o.question || r.dir?.title || r.o.direction)}</p>
    ${r.o.hit_means ? `<p class="hh-hit">A hit means: ${esc(r.o.hit_means)}</p>` : ""}
    <div class="hh-line">${lineSVG(r)}</div>
    <p class="hh-cnt">${counts}</p>
    <details><summary>Where each number comes from</summary><dl>${det.map(([k, v]) => `<dt>${k}</dt><dd>${v}</dd>`).join("")}</dl></details>
  </li>`;
}

(async () => {
  const [bets, maps, lines, steers, values] = await Promise.all([loadBets(), loadMaps(), loadHumanOdds(), loadSteers(), loadSteerValues()]);
  const { rows, noEngine } = rowsFrom(lines, bets, maps);
  const saves = new Set(lines.map((o) => String(o.recorded).slice(0, 16))).size;
  const higher = rows.filter((r) => r.human > r.engine + 1e-9).length, lower = rows.filter((r) => r.human < r.engine - 1e-9).length;
  const gap = rows.length ? rows.reduce((a, r) => a + (r.human - r.engine), 0) / rows.length : 0;
  const spend = rows.filter((r) => r.o.worth_spend === true).length, hit = rows.filter((r) => r.o.expects_hit === true).length;
  const scored = rows.filter((r) => r.counts);
  const carrying = bets.filter((b) => b.human != null);
  const missed = rows.filter((r) => r.bet && r.carries === false);
  const eAll = bets.filter((b) => b.raw.scored === true && !b.raw.secondary_of && b.engine != null && (b.raw.outcome === 0 || b.raw.outcome === 1));
  const eAllB = eAll.length ? eAll.reduce((a, b) => a + (b.engine - b.raw.outcome) ** 2, 0) / eAll.length : null;

  let scoreHTML;
  if (scored.length) {
    const eb = brier(scored, "engine"), hb = brier(scored, "human");
    scoreHTML = `<div class="stats">
      <div class="stat"><div class="label">Sean's Brier score</div><div class="value" style="color:${GOLD}">${hb.toFixed(3)}</div><div class="note">on ${scored.length} settled bet${scored.length === 1 ? "" : "s"} carrying his odds</div></div>
      <div class="stat"><div class="label">The engine's, on the same bets</div><div class="value">${eb.toFixed(3)}</div><div class="note">lower is better; always saying 50% scores 0.250</div></div>
      <div class="stat"><div class="label">Who was closer</div><div class="value">${hb < eb - 1e-9 ? "Sean" : eb < hb - 1e-9 ? "Engine" : "Tie"}</div><div class="note">${scored.length < 20 ? `${scored.length} bet${scored.length === 1 ? " is" : "s are"} far too few to tell skill from luck; the ledger's rule is 20 before judging` : "on these bets"}</div></div>
    </div>`;
  } else {
    const why = carrying.length
      ? `${carrying.length} bet${carrying.length === 1 ? " carries" : "s carry"} his odds, and none has a scored result yet.`
      : `No bet in the ledger carries his odds yet.${missed.length ? ` The ${missed.length === 1 ? "one bet" : `${missed.length} bets`} already placed on his directions (${missed.map((r) => esc(r.bet.id)).join(", ")}) ${missed.length === 1 ? "was" : "were"} pre-registered before his line reached the ledger, so under the rule that odds are never filled in afterwards ${missed.length === 1 ? "it" : "they"} will not count; the next bet on each of his directions must carry his line.` : ""}`;
    scoreHTML = `<p class="hh-none"><b>None of Sean's odds has settled yet, so there is no score for him or for the engine on his directions.</b> ${why} Both scores appear here, side by side, the moment the first one settles.</p>`;
  }

  const byAction = {};
  for (const s of steers) byAction[s.action] = (byAction[s.action] || 0) + 1;
  // The Steers panel: each steer's valuation from ledger/steer-values.jsonl (operators/steers.md), helped X of Y.
  const LABEL = { helped: HIT, neutral: "#8d8a82", hurt: KILL };
  const valued = steers.map((s) => values.get(s.id)).filter(Boolean);
  const nv = { helped: 0, neutral: 0, hurt: 0 };
  for (const v of valued) if (v.value in nv) nv[v.value] += 1;
  const unscored = steers.length - valued.length;
  const scorers = [...new Set(valued.map((v) => v.scored_by).filter(Boolean))];
  const scoredOn = [...new Set(valued.map((v) => v.scored_at).filter(Boolean))].sort();
  const strength = { measured: 0, traced: 0, early: 0 };
  for (const v of valued) if (v.evidence_strength in strength) strength[v.evidence_strength] += 1;
  const labelTag = (v) => v ? `<span class="hh-tag" style="color:${LABEL[v.value] || "inherit"};border-color:${LABEL[v.value] || "currentColor"}">${esc(v.value)}</span>` : `<span class="hh-tag">not yet scored</span>`;
  const shared = new Map();
  for (const s of steers) { const w = s.words || s.reason; if (w) shared.set(w, (shared.get(w) || 0) + 1); }
  const steerList = [...steers].reverse().map((s) => {
    const v = values.get(s.id);
    return `<li class="hh-steer">
    <div class="hh-top"><span>${esc(s.id)} · ${esc(fmtDate(parseDate(s.date), false))}${s.time ? `, ${esc(s.time)}` : ""} · ${esc(ACTION[s.action] || s.action)}${s.program ? ` · ${esc(programTitle(s.program, maps))}` : ""}</span><span class="hh-st">${labelTag(v)}</span></div>
    <p class="hh-q">${v?.steer_in_short ? esc(v.steer_in_short) : inline(s.words || s.reason || "")}</p>
    ${v ? `<p class="hh-hit"><b>${esc(v.value)}</b> (${esc(v.evidence_strength || "")}): ${inline(v.reason || "")}</p>
    <details><summary>What it changed, what the engine would have done, and the number</summary><dl>
      <dt>Changed in the record</dt><dd>${(v.changed || []).map((c) => inline(c)).join("; ") || "—"}</dd>
      <dt>Without it</dt><dd>${inline(v.counterfactual || "")}${v.counterfactual_file ? ` <span class="muted">(shown by ${inline(v.counterfactual_file)})</span>` : ""}</dd>
      <dt>Measurable effect</dt><dd>${v.effect ? inline(v.effect) : "none recorded"}</dd>
      <dt>Scored by</dt><dd>${esc(v.scored_by || "")}${v.scored_at ? `, ${esc(v.scored_at)}` : ""}${v.history && v.history.length ? `; ${v.history.length} earlier valuation${v.history.length === 1 ? "" : "s"} kept` : ""}</dd>
    </dl></details>` : `<p class="hh-hit muted">Logged after the last scoring pass; it is valued at the next one.</p>`}
    ${v?.steer_in_short && (s.words || s.reason) ? `<details><summary>His words, as logged</summary><p>${inline(s.words || s.reason)}</p>${shared.get(s.words || s.reason) > 1 ? `<p class="muted small">One message in the chat decided ${shared.get(s.words || s.reason)} steers; each is valued on its own.</p>` : ""}</details>` : ""}
    ${s.value_judgment ? `<details><summary>What the logging session wrote at the time</summary><p>${inline(s.value_judgment)}</p>${s.value_judged_by ? `<p class="muted small">Written by ${esc(s.value_judged_by)}; the record of the time, not a valuation under the method.</p>` : ""}</details>` : ""}
  </li>`;
  }).join("");
  const steersTable = valued.length ? `<table class="hh-vtable"><thead><tr><th>steer</th><th>what Sean decided, in short</th><th>label</th><th>why, in one line</th></tr></thead><tbody>${
    steers.map((s) => { const v = values.get(s.id); return `<tr><td>${esc(s.id)}</td><td>${v ? esc(v.steer_in_short) : esc((s.words || s.reason || "").slice(0, 120))}</td><td>${labelTag(v)}</td><td>${v ? inline(v.reason) : "not yet scored"}</td></tr>`; }).join("")
  }</tbody></table>` : "";
  const steersPanel = `<div class="stats">
      <div class="stat"><div class="label">Steers that helped</div><div class="value" style="color:${HIT}">${nv.helped} of ${steers.length}</div><div class="note">${nv.neutral} neutral, ${nv.hurt} hurt${unscored ? `, ${unscored} not yet scored` : ""}</div></div>
      <div class="stat"><div class="label">What decided the labels</div><div class="value">${strength.measured}</div><div class="note">by a number in the ledger; ${strength.traced} by a chain of named files; ${strength.early} given early, most of the effect still to come</div></div>
      <div class="stat"><div class="label">Who scored them</div><div class="value">Claude</div><div class="note">${scorers.length ? esc(scorers.join("; ")) : "no scoring yet"}${scoredOn.length ? `, on ${esc(scoredOn.join(", "))}` : ""}; re-scored monthly</div></div>
    </div>
    <p class="lede"><b>Helped ${nv.helped} of ${steers.length}.</b> Of the ${steers.length} steers Sean has made, a scoring session read what each one changed in the record, what the engine would have done without it, and any number that shows the difference, and labelled ${nv.helped} helped, ${nv.neutral} neutral and ${nv.hurt} hurt${unscored ? `; ${unscored} ${unscored === 1 ? "is" : "are"} not scored yet` : ""}.</p>
    <p class="how">${scorerSentence(valued, scorers, scoredOn)} A label is a reading of the record against the default the record shows, with the files that show both; it is not a controlled comparison and not a measurement of Sean's skill. The method is published, <code>operators/steers.md</code>, so a reader can disagree, and every label is re-scored monthly. The one measurement of his judgment the ledger has is the two scores above; his odds steer is labelled by that column's own rule. The table is <code>ledger/steers.md</code>; the lines are <code>ledger/steer-values.jsonl</code>.</p>
    ${steersTable}`;

  main.innerHTML = `<h1>The human hand</h1>
    <p class="how">Sean steers this project, and he can also say how likely he thinks a test is to come back a hit, in the cockpit, before any data and without ever being shown the engine's number. This page puts his number beside the engine's on every direction he has answered, shows how each one came out, and scores both once results land. Every number is read from <code>ledger/human-odds.jsonl</code>, <code>ledger/bets.jsonl</code>, the maps and <code>ledger/steers.jsonl</code> when the page loads.</p>
    <p class="lede">${lines.length ? `Sean has given odds on <b>${first(lines)}</b> direction${first(lines) === 1 ? "" : "s"}, saved from the cockpit ${saves === 1 ? "once" : `${saves} times`}. On ${rows.length} of them the engine has a number too${noEngine.length ? ` (${noEngine.length} ha${noEngine.length === 1 ? "s" : "ve"} none yet)` : ""}.` : "Sean has not given any odds yet. When he does, from the cockpit, each one appears here beside the engine's."}</p>
    ${rows.length ? `<p class="hh-sum">His number was higher than the engine's on <b>${higher}</b>, lower on <b>${lower}</b>${rows.length - higher - lower ? `, the same on <b>${rows.length - higher - lower}</b>` : ""}; on average <b>${Math.abs(Math.round(gap * 100))} points ${gap >= 0 ? "higher" : "lower"}</b>. He said he would spend the money on ${spend} of ${rows.length} and expects a hit on ${hit}.</p>` : ""}
    <div class="key hh-key"><span><svg width="18" height="18" viewBox="-9 -9 18 18" aria-hidden="true"><circle r="6.5" fill="#191c20" stroke="${ENG}" stroke-width="2.4"/></svg><b>The engine's odds</b></span>
      <span><svg width="18" height="18" viewBox="-9 -9 18 18" aria-hidden="true"><path d="M0 -8L8 0L0 8L-8 0Z" fill="${GOLD}"/></svg><b style="color:${GOLD}">Sean's odds</b></span>
      <span><svg width="12" height="18" viewBox="-6 -9 12 18" aria-hidden="true"><rect x="-3" y="-8" width="6" height="16" rx="2" fill="${HIT}"/></svg><b>How it came out</b> <span class="muted">(at 100% if it came true, 0% if not)</span></span></div>
    <h2 class="hh-h">The two scores</h2>
    ${scoreHTML}
    <p class="muted small">For reference, the engine's score on all ${eAll.length} of its scored bets is ${eAllB == null ? "not yet available" : eAllB.toFixed(3)} (<a href="${page("calibration.html")}">Calibration</a>).</p>
    <h2 class="hh-h">Direction by direction</h2>
    ${rows.length ? `<ol class="hh-rows">${rows.map((r) => rowHTML(r, maps)).join("")}</ol>` : `<div class="empty">No direction has both numbers yet.</div>`}
    <h2 class="hh-h" id="steers">Sean's steers, valued</h2>
    <p class="how">The other half of his hand: every question he chose, rule he set, veto and budget, from <code>ledger/steers.jsonl</code>. ${steers.length} so far: ${Object.entries(byAction).map(([a, n]) => `${n} ${esc((ACTION[a] || a).toLowerCase())}`).join(", ")}. Each one is a gold mark on the <a href="${page("replay.html")}">Replay</a>.</p>
    ${steersPanel}
    <h3 class="hh-h">Each steer, newest first</h3>
    <ol class="hh-steers">${steerList}</ol>`;
})();

function first(lines) { return new Set(lines.map((o) => `${o.program}|${o.direction}`)).size; }
