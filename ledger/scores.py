"""Regenerate ledger/scores.md: the engine's checks on itself. No network, no keys.

    python3 ledger/scores.py

Reads only committed ledger files. brier.py covers calibration (H1); this file
covers the scored veto (operators/veto.md) the auditor's catch rate on
sealed plants (operators/plant.md), pre-mortems (operators/premortem.md), and hardware tiebreaks and beacon
seeds (operators/hardware.md), and the feedback loop and design review
(operators/learn.md, operators/design-review.md). Do not edit scores.md by hand.
"""
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name):
    p = HERE / name
    if not p.exists():
        return []
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()]


def wilson(k, n, z=1.96):
    if n == 0:
        return None
    ph = k / n
    d = 1 + z * z / n
    c = (ph + z * z / (2 * n)) / d
    h = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)


def brier(pairs):
    return sum((p - o) ** 2 for p, o in pairs) / len(pairs) if pairs else None


def fmt(x, nd=3):
    return "—" if x is None else f"{x:.{nd}f}"


def section_vetoes(w):
    steers = load("steers.jsonl")
    shadows = load("shadows.jsonl")
    vetoes = [s for s in steers if s["action"] == "veto"]
    by = lambda k, v: [s for s in shadows if s.get(k) == v]
    shadowable = [s for s in shadows if s["shadow_status"] not in ("not_applicable",)]
    run = by("shadow_status", "run")
    val = {v: len(by("veto_value", v)) for v in ("saved", "probably_saved", "killed_hit", "undecided")}
    saved_usd = sum(s["usd_saved"] or 0 for s in by("veto_value", "saved"))
    spent = sum(s["cost_usd"] or 0 for s in shadows)
    scored = [s for s in run if s["outcome"] in ("hit", "miss")]
    hum = [(s["human_odds_at_veto"], 1 if s["outcome"] == "hit" else 0) for s in scored if s["human_odds_at_veto"] is not None]
    eng = [(s["engine_odds_at_veto"], 1 if s["outcome"] == "hit" else 0) for s in scored if s["engine_odds_at_veto"] is not None]
    unaudited = [s for s in by("veto_value", "saved") if not s.get("audit_path")]

    w("## The scored veto (operators/veto.md)")
    w("")
    w(f"{len(vetoes)} veto{'es' if len(vetoes) != 1 else ''} logged in `steers.jsonl`; {len(shadows)} shadow row{'s' if len(shadows) != 1 else ''} in `shadows.jsonl`. "
      f"{len(shadowable)} concern a research direction; {len(run)} shadow check{'s have' if len(run) != 1 else ' has'} run.")
    if not run:
        na = ", ".join(s["steer_id"] for s in by("shadow_status", "not_applicable"))
        w("No veto has been scored yet." + (f" Vetoes of something other than a research direction, so not shadowable: {na} (see each row's note)." if na else ""))
    w("")
    w("| | count |")
    w("|---|---|")
    for st in ("scheduled", "preregistered", "run", "unshadowable", "not_applicable", "expired"):
        w(f"| shadow status: {st} | {len(by('shadow_status', st))} |")
    for v, k in val.items():
        w(f"| veto value: {v} | {k} |")
    w(f"| dollars saved (direct shadows only) | ${saved_usd:.2f} |")
    w(f"| dollars spent on shadows | ${spent:.2f} |")
    w(f"| `saved` verdicts not yet audited | {len(unaudited)} |")
    w(f"| Brier on shadow outcomes, human (n = {len(hum)}) | {fmt(brier(hum))} |")
    w(f"| Brier on shadow outcomes, engine (n = {len(eng)}) | {fmt(brier(eng))} |")
    w("")
    w("Shadow outcomes are proxies, so these Brier scores are never pooled with H1 or H3. "
      "`probably_saved` comes from partial or weak shadows, which miss more easily than the full test would have, and is never added to `saved`.")
    w("")


def section_plants(w):
    rows = load("plants.jsonl")
    sealed = [r for r in rows if r["status"] == "sealed"]
    rev = [r for r in rows if r["status"] == "revealed"]
    planted = [r for r in rev if r["plaintext"]["planted"]]
    caught = [r for r in planted if r["caught"]]
    w("## The auditor's catch rate (operators/plant.md)")
    w("")
    w(f"{len(rows)} audit{'s' if len(rows) != 1 else ''} prepared with a sealed plant line: {len(sealed)} still sealed, {len(rev)} revealed, "
      f"of which {len(planted)} carried a plant. "
      + ("No plant has been revealed yet, so there is no catch rate to report." if not planted else ""))
    w("")
    if planted:
        ci = wilson(len(caught), len(planted))
        w(f"**Catch rate: {len(caught)}/{len(planted)} = {len(caught) / len(planted):.2f}, 95% Wilson interval [{ci[0]:.2f}, {ci[1]:.2f}].** "
          "External yardstick: an LLM auditor caught 82% of planted flaws with logs and code, 55% from the paper alone (Luo, Kasirzadeh & Shah 2025). "
          f"H2 needs the lower bound above 0.50 on at least 10 plants; {'reached' if len(planted) >= 10 else f'n = {len(planted)} is below that, so the arm is untestable for now'}.")
        w("")
        w("| class / subclass | planted | caught | missed: expected checklist line |")
        w("|---|---|---|---|")
        keys = sorted({(r["plaintext"]["class"], r["plaintext"]["subclass"]) for r in planted})
        for c, sc in keys:
            cell = [r for r in planted if (r["plaintext"]["class"], r["plaintext"]["subclass"]) == (c, sc)]
            miss = [r["plaintext"]["expect"] for r in cell if not r["caught"]]
            w(f"| {c} / {sc} | {len(cell)} | {sum(1 for r in cell if r['caught'])} | {', '.join(miss) or '—'} |")
        w("")
        w("| plant | bet | class | caught | where (from the audit) | planter model |")
        w("|---|---|---|---|---|---|")
        for r in planted:
            pt = r["plaintext"]
            w(f"| {r['id']} | {r['bet']} | {pt['class']}/{pt['subclass']} | {'yes' if r['caught'] else 'no'} | {r['caught_where']} | {r['planter_model']} |")
        w("")
    lim = [r for r in rev if r.get("limits")]
    if lim:
        w("**Limits, stated with the number:**")
        w("")
        for r in lim:
            w(f"- {r['id']}: {r['limits']}")
        w("")
    w("Verify every revealed commitment with `python3 ledger/plants.py verify`.")
    w("")


def section_premortems(w):
    bets = load("bets.jsonl")
    written = [b for b in bets if b.get("premortem")]
    failed = [b for b in written if b.get("failed") and b.get("premortem_score") not in (None, "unclear")]
    named = [b for b in failed if b["premortem_score"] == "named"]
    kind = [b for b in failed if b["premortem_score"] in ("named", "kind_only")]
    all_failed = [b for b in bets if b.get("failed")]
    world = [b for b in all_failed if b.get("failure_kind") == "world"]
    hum = [b for b in bets if b.get("human_premortem") and b.get("failed") and b.get("human_premortem_score") not in (None, "unclear")]
    w("## Pre-mortems (operators/premortem.md)")
    w("")
    w(f"{len(written)} of {len(bets)} bets carry an engine pre-mortem; {len(failed)} of those have failed and been scored. "
      f"{len(bets) - len(written)} have none; each row's `premortem_note` says why (most were pre-registered before pre-mortems existed).")
    w("")
    def rate(k, n):
        if not n:
            return "—"
        lo, hi = wilson(k, n)
        return f"{k}/{n} = {k / n:.2f} [{lo:.2f}, {hi:.2f}]"
    w("| measure | value (95% Wilson interval) |")
    w("|---|---|")
    w(f"| engine: named the main reason | {rate(len(named), len(failed))} |")
    w(f"| engine: named it or its kind | {rate(len(kind), len(failed))} |")
    w(f"| lazy baseline: failures whose reason was 'the effect is not there' | {rate(len(world), len(all_failed))} |")
    w(f"| human: named the main reason | {rate(sum(1 for b in hum if b['human_premortem_score'] == 'named'), len(hum))} |")
    w("")
    if failed:
        kinds = ("world", "design", "execution", "artefact")
        w("| stated kind \\ actual kind | " + " | ".join(kinds) + " |")
        w("|---|" + "---|" * len(kinds))
        for sk in kinds:
            w(f"| {sk} | " + " | ".join(str(sum(1 for b in failed if b['premortem_kind'] == sk and b.get('failure_kind') == ak)) for ak in kinds) + " |")
        w("")
    w("Descriptive under Q1 until there are at least 15 failed bets with pre-mortems.")
    w("")


def section_hardware(w):
    bets = load("bets.jsonl")
    tb = [b for b in bets if b.get("bet_type") == "tiebreak"]
    done = [b for b in tb if b["tiebreak"] and b["tiebreak"].get("agree") is not None]
    eng = [(b["engine_odds"], int(b["tiebreak"]["agree"])) for b in done if b.get("engine_odds") is not None]
    hum = [(b["human_odds"], int(b["tiebreak"]["agree"])) for b in done if b.get("human_odds") is not None]
    qpu = sum((b["tiebreak"] or {}).get("qpu_s_used") or 0 for b in tb)
    src = {}
    for b in bets:
        src[b.get("seed_source") or "none recorded"] = src.get(b.get("seed_source") or "none recorded", 0) + 1
    w("## Hardware: tiebreaks and beacon seeds (operators/hardware.md)")
    w("")
    w("The chip is a referee and the beacon a seed source; neither computes anything the engine uses.")
    w("")
    w("| | value |")
    w("|---|---|")
    w(f"| tiebreak bets logged / resolved | {len(tb)} / {len(done)} |")
    w(f"| chip agreed with the simulator | {sum(1 for b in done if b['tiebreak']['agree'])} of {len(done)} |")
    w(f"| Brier on tiebreaks, engine (n = {len(eng)}) | {fmt(brier(eng))} |")
    w(f"| Brier on tiebreaks, human (n = {len(hum)}) | {fmt(brier(hum))} |")
    w(f"| QPU seconds used by tiebreaks | {qpu:g} |")
    for k in sorted(src):
        w(f"| bets by seed source: {k} | {src[k]} |")
    w("")


RULE_FROM = "2026-11-04 17:00"   # operators/learn.md and operators/design-review.md apply from here


def section_learning(w):
    bets = load("bets.jsonl")
    rows = load("lessons.jsonl")
    pats = {r["id"]: r for r in rows if r.get("kind") == "pattern"}
    lessons = {r["bet"]: r for r in rows if r.get("kind") == "lesson"}
    since = [b for b in bets if (b.get("prereg_time") or "") >= RULE_FROM and b.get("verdict") != "withdrawn"]
    withdrawn = [b for b in bets if b.get("verdict") == "withdrawn"]
    no_lesson = [b["id"] for b in since if b["id"] not in lessons]
    reviewed = lambda b: (b.get("design_review") or {}).get("verdict") in ("go", "fix-first", "redesign")
    awaiting = [b["id"] for b in since if not reviewed(b) and not b.get("result_commit")]
    no_review = [b["id"] for b in since if not reviewed(b) and b.get("result_commit")]   # ran without a review: a violation
    flagged = [b["id"] for b in bets if b.get("rule_violation")]
    w("## The feedback loop (operators/learn.md) and design review (operators/design-review.md)")
    w("")
    w(f"Both are mandatory for every pre-registration from {RULE_FROM} America/Denver. "
      f"{len(pats)} patterns from past misses and audit cuts are on file in `lessons.jsonl`; {len(lessons)} lesson line{'s' if len(lessons) != 1 else ''} written.")
    w("")
    w("| | count |")
    w("|---|---|")
    w(f"| pre-registrations since the rule | {len(since)} |")
    w(f"| with a lesson line | {len(since) - len(no_lesson)} |")
    w(f"| with a design review verdict | {sum(1 for b in since if reviewed(b))} |")
    w(f"| awaiting their design review (nothing may run yet) | {len(awaiting)}{': ' + ', '.join(awaiting) if awaiting else ''} |")
    w(f"| **violations** (no lesson, or a result without a review) | {len(set(no_lesson) | set(no_review))}{': ' + ', '.join(sorted(set(no_lesson) | set(no_review))) if no_lesson or no_review else ''} |")
    w(f"| bets flagged `rule_violation` | {len(flagged)}{': ' + ', '.join(flagged) if flagged else ''} |")
    w(f"| withdrawn after a design review said redesign | {len(withdrawn)} |")
    w("")
    revs = [b["design_review"] for b in bets if (b.get("design_review") or {}).get("verdict")]
    if revs:
        vc = {v: sum(1 for r in revs if r["verdict"] == v) for v in ("go", "fix-first", "redesign")}
        missed = [r for r in revs if r.get("missed")]
        w(f"Design reviews: {vc['go']} go, {vc['fix-first']} fix-first, {vc['redesign']} redesign; "
          f"{len(missed)} later found by the post-result audit to have missed a flaw they should have caught.")
        w("")
    scored = [l for l in lessons.values() if l.get("scored")]
    pairs, pairs_all = [], []
    for l in scored:
        per = l.get("odds_by_bet") or {l["bet"]: {"odds_before_lesson": l.get("odds_before_lesson"), "odds_after_lesson": l.get("odds_after_lesson")}}
        for bid, od in per.items():
            b = next((x for x in bets if x["id"] == bid), None)
            if b and b.get("scored") and od.get("odds_before_lesson") is not None and od.get("odds_after_lesson") is not None:
                pairs_all.append((od["odds_before_lesson"], od["odds_after_lesson"], b["outcome"]))
                if not b.get("secondary_of"):   # rule 15: one scored bet per run
                    pairs.append((od["odds_before_lesson"], od["odds_after_lesson"], b["outcome"]))
    w("| pattern | title | cited by | recurred after citing |")
    w("|---|---|---|---|")
    for pid, pr in pats.items():
        cit = [l for l in lessons.values() if pid in (l.get("patterns") or [])]
        rec = sum(1 for l in cit if l.get("recurred") is True)
        w(f"| {pid} | {pr['title']} | {len(cit)} | {rec} of {sum(1 for l in cit if l.get('recurred') is not None)} scored |")
    w("")
    if pairs:
        bb = brier([(p, o) for p, _, o in pairs]); ba = brier([(q, o) for _, q, o in pairs])
        w(f"**Does the loop help?** On {len(pairs)} scored bets (one per run, rule 15), Brier with the odds before the lesson is {fmt(bb)}, after it {fmt(ba)}."
          + (f" Counting secondary bets too: {fmt(brier([(p, o) for p, _, o in pairs_all]))} before, {fmt(brier([(q, o) for _, q, o in pairs_all]))} after, on {len(pairs_all)}."
             if len(pairs_all) != len(pairs) else ""))
    else:
        w("**Does the loop help?** Not measurable yet: no bet with a lesson has a scored outcome. The test is Brier with the odds before the lesson against after it, paired.")
    w("")


def main():
    L = []
    w = L.append
    w("# The engine's checks on itself")
    w("")
    w("Generated by `python3 ledger/scores.py` from the committed ledger. Do not edit by hand. "
      "Calibration of the engine's odds is in `brier.md`.")
    w("")
    section_vetoes(w)
    section_plants(w)
    section_premortems(w)
    section_hardware(w)
    section_learning(w)
    (HERE / "scores.md").write_text("\n".join(L) + "\n")
    print("wrote ledger/scores.md")


if __name__ == "__main__":
    main()
