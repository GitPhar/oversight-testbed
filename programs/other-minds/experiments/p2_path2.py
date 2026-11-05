"""P2-path2 (proposal.md Q4; re-bet of the withdrawn om-p2-path, DEVIATIONS D19a): do program 2's misses and audit
cuts carry failure patterns first recorded in program 1, and more often than the same tagging finds in programs that
program 1 did not seed? Archive only, $0, as pre-registered in experiments/p2-path2.md (DEVIATIONS D21).

    python3 experiments/p2_path2.py units     # build data/p2-path2-units.json and the classifier packet (before any tag)
    python3 experiments/p2_path2.py dryrun    # D11: P(pass) for synthetic taggers on these unit counts
    python3 experiments/p2_path2.py score     # read data/p2-path2-tags-A.json (and -B), write results/p2-path2.json

Standard library only. Reads ledger/bets.jsonl, ledger/audits/*.md and ledger/lessons.jsonl at the engine root (units
only), data/p2-path2-origins.json (written by a fresh session that never saw the units, before this file's
pre-registration), and the tags files."""

import json
import random
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT.parents[1]
DATA, RESULTS = ROOT / "data", ROOT / "results"
UNITS, PACKET, ORIGINS = DATA / "p2-path2-units.json", DATA / "p2-path2-classifier-packet.md", DATA / "p2-path2-origins.json"
TAGS = {"A": DATA / "p2-path2-tags-A.json", "B": DATA / "p2-path2-tags-B.json"}
OUT, TABLES = RESULTS / "p2-path2.json", RESULTS / "p2-path2-tables.md"
CUTOFF = "2026-11-04T17:00:00-07:00"
TARGET = "other-minds"
BASELINE = ("settled-science", "self-grading", "test-awareness")   # programs not seeded by program 1 (§2)
BAR, MARGIN, EPS = 0.50, 0.15, 1e-9
MIN_UNITS = {"target": 10, "baseline": 10}
SHUFFLE_SEED = 20261105                                          # fixed constant: only the packet order
TRAILING = re.compile(r"(?m)^(?:Also |No other |Optional|Not required|Ledger, not|Suggested|---)")


def git_time(commit):
    return subprocess.run(["git", "-C", str(ENGINE), "log", "-1", "--format=%aI", commit], capture_output=True,
                          text=True, check=True).stdout.strip()


def population():
    """Bets of the target and baseline programs pre-registered after the cutoff and settled (a verdict other than open
    or withdrawn, and an audit on record), one entry per audit file (ss-b1..b3 share one audit and count once)."""
    bets = [json.loads(l) for l in (ENGINE / "ledger" / "bets.jsonl").read_text().splitlines() if l.strip()]
    seen, pop = set(), []
    for b in bets:
        prog = b.get("program")
        if prog != TARGET and prog not in BASELINE:
            continue
        if b.get("verdict") in (None, "open", "withdrawn") or not b.get("audit") or not (ENGINE / b["audit"]).exists():
            continue
        if git_time(b["prereg_commit"]) <= CUTOFF:
            continue
        group = "target" if prog == TARGET else "baseline"
        pop.append((group, b, b["audit"] not in seen))
        seen.add(b["audit"])
    return pop


def plant_cuts(text):
    rev = text.split("Revealed", 1)[1] if "Revealed" in text else ""
    return {int(n) for pair in re.findall(r"[Rr]equired cut (\d+) is the plant|[Cc]ut (\d+) was (?:the )?plant", rev)
            for n in pair if n}


def required_cuts(text):
    """Numbered items under '## Required cuts'. Each item's text stops before a trailing paragraph at the left margin
    that begins 'Also', 'No other', 'Optional', 'Not required', 'Ledger, not', 'Suggested' or a rule (D21 (4))."""
    m = re.search(r"^## Required cuts\s*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    if not m:
        return []
    parts = re.split(r"(?m)^(\d+)\.\s", m.group(1))
    out = []
    for i in range(1, len(parts) - 1, 2):
        body = parts[i + 1]
        t = TRAILING.search(body)
        out.append((int(parts[i]), (body[:t.start()] if t else body).strip()))
    return out


def build_units():
    units = []
    for group, b, first_for_audit in population():
        text = (ENGINE / b["audit"]).read_text()
        if b.get("failed") and b.get("failure_reason"):
            units.append({"group": group, "program": b["program"], "bet": b["id"], "kind": "miss",
                          "bet_title": b.get("title", ""), "text": b["failure_reason"],
                          "source": f"{b['id']} ledger row failure_reason"})
        if not first_for_audit:
            continue
        plants = plant_cuts(text)
        for n, txt in required_cuts(text):
            if n in plants or not txt:
                continue
            units.append({"group": group, "program": b["program"], "bet": b["id"], "kind": "cut",
                          "bet_title": b.get("title", ""), "text": txt, "source": f"{b['audit']} Required cuts item {n}"})
    order = list(range(len(units)))
    random.Random(SHUFFLE_SEED).shuffle(order)
    for k, i in enumerate(order):
        units[i]["unit"] = f"U{k + 1:02d}"
    return sorted(units, key=lambda u: u["unit"])


def patterns_for_classifier():
    pats = [json.loads(l) for l in (ENGINE / "ledger" / "lessons.jsonl").read_text().splitlines()
            if l.strip() and json.loads(l).get("kind") == "pattern"]
    return [{"id": p["id"], "title": p["title"], "what_to_do": p.get("do_this", "")} for p in pats]


def write_packet(units, pats):
    L = ["# Classification packet", "",
         "You will tag each numbered unit below with the failure patterns it carries. A unit is either a *miss* (why a "
         "pre-registered test failed, in its auditor's words) or a *cut* (a passage an auditor required to be removed "
         "or rewritten in a write-up, with the replacement). The units come from several research programs, in a "
         "random order.", "",
         "**Rule.** A unit carries a pattern when the fault the unit describes is an instance of that pattern's title, "
         "read with its 'what to do' line: the same kind of mistake, not merely the same topic. Tag every pattern the "
         "unit carries, and only those; tag `none` if it carries none. Judge each unit on its own text.", "",
         "Reply with JSON only: `{\"U01\": {\"patterns\": [\"P3\", ...] or [\"none\"], \"why\": \"<at most 25 words>\"}, "
         "...}`, one entry for every unit.", "", "## Patterns", ""]
    for p in pats:
        L.append(f"- **{p['id']}. {p['title']}.** What to do: {p['what_to_do']}")
    L += ["", "## Units", ""]
    for u in units:
        L.append(f"### {u['unit']} ({u['kind']})\n\nTest: {u['bet_title']}\n\n{u['text']}\n")
    PACKET.write_text("\n".join(L) + "\n")


def units_cmd():
    units = build_units()
    UNITS.write_text(json.dumps({"cutoff": CUTOFF, "target": TARGET, "baseline": list(BASELINE), "units": units}, indent=1))
    write_packet(units, patterns_for_classifier())
    for g in ("target", "baseline"):
        us = [u for u in units if u["group"] == g]
        print(f"{g}: {len(us)} units from {len({u['bet'] for u in us})} bets ({sum(u['kind'] == 'miss' for u in us)} misses)")


def origin_set():
    o = json.loads(ORIGINS.read_text())["patterns"]
    return {p for p, v in o.items() if v["origin"] == "program 1"}


def validate(units, tags, pat_ids):
    """Untestable conditions (D21 (5)): a unit missing, an empty list, an unknown id, or 'none' mixed with ids."""
    bad = []
    for u in units:
        t = tags.get(u["unit"])
        if t is None or not isinstance(t.get("patterns"), list) or not t["patterns"]:
            bad.append(f"{u['unit']}: missing or empty")
            continue
        ps = t["patterns"]
        if "none" in ps and len(ps) > 1:
            bad.append(f"{u['unit']}: 'none' mixed with ids")
        if any(p != "none" and p not in pat_ids for p in ps):
            bad.append(f"{u['unit']}: unknown id {ps}")
    return bad


def shares(units, tags, p1):
    out = {}
    for g in ("target", "baseline"):
        us = [u for u in units if u["group"] == g]
        k = sum(1 for u in us if set(tags[u["unit"]]["patterns"]) & p1)
        out[g] = {"n": len(us), "k": k, "share": k / len(us) if us else float("nan"),
                  "tags_per_unit": sum(len([p for p in tags[u["unit"]]["patterns"] if p != "none"]) for u in us) / max(1, len(us)),
                  "any_pattern": sum(1 for u in us if tags[u["unit"]]["patterns"] != ["none"]) / max(1, len(us))}
    return out


def label_of(sh):
    if sh["target"]["n"] < MIN_UNITS["target"] or sh["baseline"]["n"] < MIN_UNITS["baseline"]:
        return "untestable"
    ok = sh["target"]["share"] >= BAR - EPS and sh["target"]["share"] - sh["baseline"]["share"] >= MARGIN - EPS
    return "pass" if ok else "fail"


SENT = {
    "pass": ("Of program 2's {nt} misses and required audit cuts on bets pre-registered after 2026-11-04 17:00, {kt} "
             "({st:.0%}) carry a failure pattern recorded first in program 1 by the origin rule, against {sb:.0%} of {nb} "
             "from programs 4, 5 and 6, as tagged by a fresh classifier blind to this bet's question and to each "
             "pattern's origin. The pre-registered event occurred (at least half, and at least 15 points above the "
             "baseline)."),
    "fail": ("Of program 2's {nt} misses and required audit cuts on bets pre-registered after 2026-11-04 17:00, {kt} "
             "({st:.0%}) carry a failure pattern recorded first in program 1 by the origin rule, against {sb:.0%} of {nb} "
             "from programs 4, 5 and 6, as tagged by a fresh classifier blind to this bet's question and to each "
             "pattern's origin. The pre-registered event did not occur (it needed at least half, and at least 15 points "
             "above the baseline)."),
    "untestable": "The test could not answer: {why}.",
}


def score_cmd():
    U = json.loads(UNITS.read_text())
    units = U["units"]
    pat_ids = {p["id"] for p in patterns_for_classifier()}
    p1 = origin_set()
    tA = json.loads(TAGS["A"].read_text())
    bad = validate(units, tA, pat_ids)
    res = {"origin_program1": sorted(p1, key=lambda x: int(x[1:])), "validation": bad}
    if bad:
        res.update({"label": "untestable", "sentence": SENT["untestable"].format(why="; ".join(bad))})
    else:
        sh = shares(units, tA, p1)
        lab = label_of(sh)
        res.update({"label": lab, "shares": sh, "difference": sh["target"]["share"] - sh["baseline"]["share"]})
        res["sentence"] = SENT["untestable"].format(why="too few units") if lab == "untestable" else SENT[lab].format(
            nt=sh["target"]["n"], kt=sh["target"]["k"], st=sh["target"]["share"], sb=sh["baseline"]["share"],
            nb=sh["baseline"]["n"])
        p9 = shares(units, tA, p1 ^ {"P9"})
        res["sensitivity_p9_flipped"] = {"origin_set": sorted(p1 ^ {"P9"}, key=lambda x: int(x[1:])),
                                         "target": p9["target"]["share"], "baseline": p9["baseline"]["share"],
                                         "label_would_be": label_of(p9)}
        res["by_bet"] = {}
        for b in dict.fromkeys(u["bet"] for u in units):
            us = [u for u in units if u["bet"] == b]
            res["by_bet"][b] = {"group": us[0]["group"], "n": len(us),
                                "share": sum(1 for u in us if set(tA[u["unit"]]["patterns"]) & p1) / len(us)}
        loo = {}
        for b in res["by_bet"]:
            sub = [u for u in units if u["bet"] != b]
            loo[b] = label_of(shares(sub, tA, p1))
        res["leave_one_bet_out_flips"] = [b for b, l in loo.items() if l != lab]
        counts = {}
        for u in units:
            for p in tA[u["unit"]]["patterns"]:
                counts.setdefault(u["group"], {}).setdefault(p, 0)
                counts[u["group"]][p] += 1
        res["pattern_counts"] = counts
        if TAGS["B"].exists():
            tB = json.loads(TAGS["B"].read_text())
            if not validate(units, tB, pat_ids):
                shB = shares(units, tB, p1)
                a = [bool(set(tA[u["unit"]]["patterns"]) & p1) for u in units]
                b_ = [bool(set(tB[u["unit"]]["patterns"]) & p1) for u in units]
                n = len(a)
                po = sum(x == y for x, y in zip(a, b_)) / n
                pa, pb = sum(a) / n, sum(b_) / n
                pe = pa * pb + (1 - pa) * (1 - pb)
                res["classifier_B"] = {"shares": shB, "label_would_be": label_of(shB), "agreement": po,
                                       "kappa": (po - pe) / (1 - pe) if pe < 1 else 1.0}
    OUT.write_text(json.dumps(res, indent=1))
    L = ["# P2-path2 tables (generated by experiments/p2_path2.py score; do not edit)", "", f"**{res['label']}.** {res['sentence']}", ""]
    if "shares" in res:
        L += ["| group | units | carry a program-1 pattern | share | tags per unit | carry any pattern |", "|---|---|---|---|---|---|"]
        for g, nm in (("target", "program 2"), ("baseline", "programs 4, 5, 6")):
            s = res["shares"][g]
            L.append(f"| {nm} | {s['n']} | {s['k']} | {s['share']:.3f} | {s['tags_per_unit']:.2f} | {s['any_pattern']:.3f} |")
        L += ["", f"Difference (program 2 minus baseline): {res['difference']:+.3f} (bar: share at least 0.50 and difference at least +0.15).",
              f"Program-1 patterns by the origin rule: {', '.join(res['origin_program1'])}.",
              f"With P9's origin flipped: program 2 {res['sensitivity_p9_flipped']['target']:.3f}, baseline "
              f"{res['sensitivity_p9_flipped']['baseline']:.3f}, label would be {res['sensitivity_p9_flipped']['label_would_be']}.",
              f"Leave-one-bet-out label flips: {res['leave_one_bet_out_flips'] or 'none'}.", "",
              "| unit | group | bet | kind | patterns (A) | program-1 pattern | why (A) |", "|---|---|---|---|---|---|---|"]
        for u in units:
            t = tA[u["unit"]]
            L.append(f"| {u['unit']} | {u['group']} | {u['bet']} | {u['kind']} | {', '.join(t['patterns'])} | "
                     f"{'yes' if set(t['patterns']) & p1 else 'no'} | {t.get('why', '').replace('|', '/')} |")
        if "classifier_B" in res:
            c = res["classifier_B"]
            L += ["", f"Classifier B: program 2 {c['shares']['target']['share']:.3f}, baseline {c['shares']['baseline']['share']:.3f}, "
                  f"label would be {c['label_would_be']}; agreement with A on 'carries a program-1 pattern' {c['agreement']:.2f}, "
                  f"kappa {c['kappa']:.2f}."]
    TABLES.write_text("\n".join(L) + "\n")
    print(TABLES.read_text())


def dryrun_cmd(sims=4000):
    """D11 on the real unit counts: each unit carries a program-1 pattern with probability p_target or p_baseline.
    Worlds: no path dependence (equal p) at three tagging rates, and path dependence of several sizes."""
    U = json.loads(UNITS.read_text())["units"]
    nt = sum(u["group"] == "target" for u in U)
    nb = sum(u["group"] == "baseline" for u in U)
    rng = random.Random(7)
    print(f"units: program 2 {nt}, baseline {nb}")
    worlds = [(0.3, 0.3), (0.5, 0.5), (0.7, 0.7), (0.6, 0.4), (0.7, 0.45), (0.75, 0.4), (0.8, 0.5), (0.55, 0.35)]
    for pt, pb in worlds:
        n = 0
        for _ in range(sims):
            kt = sum(rng.random() < pt for _ in range(nt))
            kb = sum(rng.random() < pb for _ in range(nb))
            sh = {"target": {"n": nt, "share": kt / nt}, "baseline": {"n": nb, "share": kb / nb}}
            n += label_of(sh) == "pass"
        print(f"  p(program 2) {pt:.2f}, p(baseline) {pb:.2f}: P(pass) {n / sims:.3f}")
    for st, sb, want in ((0.5, 0.35, "pass"), (0.5, 0.3500001, "fail"), (0.4999, 0.0, "fail")):
        got = label_of({"target": {"n": nt, "share": st}, "baseline": {"n": nb, "share": sb}})
        assert got == want, (st, sb, got)
    assert label_of({"target": {"n": 9, "share": 1}, "baseline": {"n": nb, "share": 0}}) == "untestable"
    t = {u["unit"]: {"patterns": ["P2"]} for u in U}
    assert not validate(U, t, {"P2"})
    t[U[0]["unit"]] = {"patterns": []}
    assert validate(U, t, {"P2"})
    t[U[0]["unit"]] = {"patterns": ["none", "P2"]}
    assert validate(U, t, {"P2"})
    print("  boundary and validation checks: hold")


if __name__ == "__main__":
    {"units": units_cmd, "score": score_cmd, "dryrun": dryrun_cmd}[sys.argv[1]]()
