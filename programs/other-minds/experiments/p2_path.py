"""P2-path (proposal.md Q4): do program 2's misses and audit cuts carry failure patterns first seen in program 1?
Archive only, $0, as pre-registered in experiments/p2-path.md (DEVIATIONS D19).

    python3 experiments/p2_path.py units      # build data/p2-path-units.json and the classifier's packet (before any tag)
    python3 experiments/p2_path.py score      # read data/p2-path-tags-A.json (and -B), write results/p2-path.json

Run from programs/other-minds with any Python 3 (standard library only). Reads ledger/bets.jsonl, ledger/audits/*.md and
ledger/lessons.jsonl at the engine root."""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT.parents[1]
DATA, RESULTS = ROOT / "data", ROOT / "results"
UNITS, PACKET = DATA / "p2-path-units.json", DATA / "p2-path-classifier-packet.md"
TAGS = {"A": DATA / "p2-path-tags-A.json", "B": DATA / "p2-path-tags-B.json"}
OUT, TABLES = RESULTS / "p2-path.json", RESULTS / "p2-path-tables.md"
CUTOFF = "2026-11-04T17:00:00-07:00"
BAR = 0.5

# Which patterns were first seen in program 1, by the pre-registered rule (experiments/p2-path.md §2): a pattern is
# program-1-origin if (a) its evidence cites a program 1 instance from audit round 1 (entangled-mind audits, the
# founding week, before program 2 opened at 2026-11-04 10:19), or (b) every instance it cites is a program 1 bet.
# Computed by hand from each pattern line's `evidence` and `sources` at the pre-registration commit; written here
# before any classification, and never shown to the classifier.
ORIGIN_P1 = {"P2": "a: round 1, v2-run-1 (no equivalence margin)", "P3": "a: round 1, one-bit 'model said no' predictor",
             "P8": "a: round 1, own vs other differed in instruction, schema and turn",
             "P10": "a: round 1, two of ten items drove direction 2", "P11": "b: em-qwalk only",
             "P12": "b: em-qwalk2 only", "P17": "b: em-gm2bf1 only"}
NOT_P1 = {"P1": "program 2 (om-p2-1..4) and brier.md", "P4": "program 3", "P5": "program 3", "P6": "program 3",
          "P7": "program 2", "P9": "audit round 2 (programs 1, 2 and 3 at once); round 1's wording fault was a different one",
          "P13": "programs 2 and 3", "P14": "program 5", "P15": "program 6", "P16": "program 7"}
SENSITIVITY_P9_AS_P1 = True                     # secondary: the same share with P9 counted as program-1-origin


def ledger_bets():
    return [json.loads(l) for l in (ENGINE / "ledger" / "bets.jsonl").read_text().splitlines() if l.strip()]


def prereg_time(commit):
    import subprocess
    return subprocess.run(["git", "-C", str(ENGINE), "log", "-1", "--format=%aI", commit], capture_output=True,
                          text=True, check=True).stdout.strip()


def population(bets):
    """Program 2 bets pre-registered after the cutoff and settled: a verdict other than open or withdrawn, and an audit
    file on record. Order: pre-registration time."""
    pop = []
    for b in bets:
        if b.get("program") != "other-minds" or b.get("verdict") in (None, "open", "withdrawn"):
            continue
        if not b.get("audit") or not (ENGINE / b["audit"]).exists():
            continue
        t = prereg_time(b["prereg_commit"])
        if t > CUTOFF:
            pop.append((t, b))
    return [b for _, b in sorted(pop, key=lambda x: x[0])]


def plant_cuts(audit_text):
    """Numbers of the required cuts that the audit's 'Revealed' note says were the plant (not applied to the record)."""
    rev = audit_text.split("Revealed", 1)[1] if "Revealed" in audit_text else ""
    return {int(n) for n in re.findall(r"[Rr]equired cut (\d+) is the plant|[Cc]ut (\d+) was (?:the )?plant", rev)
            for n in n if n} if rev else set()


def required_cuts(audit_text):
    """The numbered items under '## Required cuts', each with its full text (continuation lines included)."""
    m = re.search(r"^## Required cuts\s*\n(.*?)(?=^## |\Z)", audit_text, re.S | re.M)
    if not m:
        return []
    body = m.group(1)
    items = re.split(r"(?m)^(\d+)\.\s", body)
    out = []
    for i in range(1, len(items) - 1, 2):
        txt = items[i + 1]
        txt = re.split(r"(?m)^(?:Ledger, not the results file|Optional|Not required|---)", txt)[0]
        out.append((int(items[i]), txt.strip()))
    return out


def build_units():
    units = []
    for b in population(ledger_bets()):
        text = (ENGINE / b["audit"]).read_text()
        title = b.get("title", "")
        if b.get("failed") or b.get("outcome") == 0 or b.get("verdict") in ("null", "fail", "mixed", "classical", "tie"):
            if b.get("failure_reason"):
                units.append({"unit": f"{b['id']}:miss", "bet": b["id"], "kind": "miss", "bet_title": title,
                              "text": b["failure_reason"], "source": f"{b['audit']} front matter failure_reason (ledger row)"})
        plants = plant_cuts(text)
        for n, txt in required_cuts(text):
            if n in plants:
                continue
            units.append({"unit": f"{b['id']}:cut{n}", "bet": b["id"], "kind": "cut", "bet_title": title, "text": txt,
                          "source": f"{b['audit']} Required cuts item {n}"})
    return units


def patterns_for_classifier():
    pats = [json.loads(l) for l in (ENGINE / "ledger" / "lessons.jsonl").read_text().splitlines()
            if l.strip() and json.loads(l).get("kind") == "pattern"]
    return [{"id": p["id"], "title": p["title"], "what_to_do": p.get("do_this", "")} for p in pats]


def write_packet(units, pats):
    L = ["# Classification packet", "",
         "You will tag each numbered unit below with the failure patterns it carries. A unit is either a *miss* (why a "
         "pre-registered test failed, in its auditor's words) or a *cut* (a sentence an auditor required to be removed "
         "or rewritten in a write-up, with the replacement).", "",
         "**Rule.** A unit carries a pattern when the fault the unit describes is an instance of that pattern's title, "
         "read with its 'what to do' line: the same kind of mistake, not merely the same topic. Tag every pattern the "
         "unit carries; tag `none` if it carries none. Judge each unit on its own text. Do not guess which project, "
         "program or test a unit or a pattern came from; that is not part of the rule.", "",
         "Reply as JSON: `{\"<unit id>\": {\"patterns\": [\"P3\", ...] or [\"none\"], \"why\": \"<at most 25 words>\"}, ...}`, "
         "covering every unit.", "", "## Patterns", ""]
    for p in pats:
        L.append(f"- **{p['id']}. {p['title']}.** What to do: {p['what_to_do']}")
    L += ["", "## Units", ""]
    for u in units:
        L.append(f"### {u['unit']} ({u['kind']})\n\nTest: {u['bet_title']}\n\n{u['text']}\n")
    PACKET.write_text("\n".join(L) + "\n")


def units_cmd():
    units = build_units()
    pats = patterns_for_classifier()
    UNITS.write_text(json.dumps({"cutoff": CUTOFF, "origin_p1": ORIGIN_P1, "not_p1": NOT_P1, "units": units}, indent=1))
    write_packet(units, pats)
    print(f"{len(units)} units from {len({u['bet'] for u in units})} bets: "
          + ", ".join(f"{b} {sum(1 for u in units if u['bet'] == b)}" for b in dict.fromkeys(u['bet'] for u in units)))


def share(units, tags, p1):
    carry = [u["unit"] for u in units if set(tags[u["unit"]]["patterns"]) & p1]
    return len(carry) / len(units), carry


def kappa_any(units, ta, tb, p1):
    """Cohen's kappa on the binary 'carries a program-1-origin pattern' between classifiers A and B."""
    a = [bool(set(ta[u["unit"]]["patterns"]) & p1) for u in units]
    b = [bool(set(tb[u["unit"]]["patterns"]) & p1) for u in units]
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    pa, pb = sum(a) / n, sum(b) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0, po


def score_cmd():
    U = json.loads(UNITS.read_text())
    units = U["units"]
    tA = json.loads(TAGS["A"].read_text())
    missing = [u["unit"] for u in units if u["unit"] not in tA]
    if missing:
        sys.exit(f"classifier A did not tag {missing}")
    p1 = set(ORIGIN_P1)
    s, carry = share(units, tA, p1)
    label = "pass" if s >= BAR - 1e-9 else "fail"
    res = {"n_units": len(units), "share_p1": s, "units_carrying_p1": carry, "label": label,
           "by_kind": {k: share([u for u in units if u["kind"] == k], tA, p1)[0] for k in ("miss", "cut")
                       if any(u["kind"] == k for u in units)},
           "by_bet": {b: share([u for u in units if u["bet"] == b], tA, p1)[0] for b in dict.fromkeys(u["bet"] for u in units)},
           "share_p9_as_p1": share(units, tA, p1 | {"P9"})[0],
           "share_any_pattern": sum(1 for u in units if tA[u["unit"]]["patterns"] != ["none"]) / len(units),
           "pattern_counts": {}}
    for u in units:
        for p in tA[u["unit"]]["patterns"]:
            res["pattern_counts"][p] = res["pattern_counts"].get(p, 0) + 1
    if TAGS["B"].exists():
        tB = json.loads(TAGS["B"].read_text())
        if all(u["unit"] in tB for u in units):
            sB, _ = share(units, tB, p1)
            k, po = kappa_any(units, tA, tB, p1)
            res["classifier_B"] = {"share_p1": sB, "label_would_be": "pass" if sB >= BAR - 1e-9 else "fail",
                                   "agreement": po, "kappa": k}
    # leave-one-bet-out
    res["leave_one_bet_out"] = {b: share([u for u in units if u["bet"] != b], tA, p1)[0] for b in res["by_bet"]}
    res["loo_flips"] = [b for b, v in res["leave_one_bet_out"].items() if (v >= BAR - 1e-9) != (label == "pass")]
    n1 = len(carry)
    res["sentence"] = (f"Of program 2's {len(units)} misses and required audit cuts on bets pre-registered after "
                       f"2026-11-04 17:00, {n1} ({s:.0%}) carry a failure pattern first seen in program 1, as tagged by a "
                       f"fresh classifier blind to the bet and to each pattern's origin; the bar was half. "
                       + ("The pre-registered event occurred." if label == "pass" else "The pre-registered event did not occur."))
    OUT.write_text(json.dumps(res, indent=1))
    L = ["# P2-path tables (generated by experiments/p2_path.py score; do not edit)", "", res["sentence"], "",
         "| unit | kind | patterns (classifier A) | carries a program-1 pattern | why (A) |", "|---|---|---|---|---|"]
    for u in units:
        t = tA[u["unit"]]
        L.append(f"| {u['unit']} | {u['kind']} | {', '.join(t['patterns'])} | {'yes' if set(t['patterns']) & p1 else 'no'} | "
                 f"{t.get('why', '').replace('|', '/')} |")
    L += ["", f"Share: {s:.3f} ({n1}/{len(units)}); with P9 counted as program 1: {res['share_p9_as_p1']:.3f}; units "
          f"carrying any pattern: {res['share_any_pattern']:.3f}.", "",
          "| bet | share | leave this bet out |", "|---|---|---|"]
    for b, v in res["by_bet"].items():
        L.append(f"| {b} | {v:.2f} | {res['leave_one_bet_out'][b]:.2f} |")
    if "classifier_B" in res:
        c = res["classifier_B"]
        L += ["", f"Classifier B: share {c['share_p1']:.3f} ({c['label_would_be']}); agreement with A on 'carries a "
              f"program-1 pattern' {c['agreement']:.2f}, kappa {c['kappa']:.2f}."]
    L += ["", "Pattern counts (A): " + ", ".join(f"{k} {v}" for k, v in sorted(res["pattern_counts"].items(),
                                                                         key=lambda x: (x[0] == 'none', int(x[0][1:]) if x[0] != 'none' else 0)))]
    TABLES.write_text("\n".join(L) + "\n")
    print(TABLES.read_text())


if __name__ == "__main__":
    {"units": units_cmd, "score": score_cmd}[sys.argv[1]]()
