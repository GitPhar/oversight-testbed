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
# D21a (review 259c72d, F2): one criterion, the materials rule. A program is seeded by program 1 if its items, question
# pools or instruments come from program 1's archives: programs 2, 3 (the chip question from program 1's hardware run),
# 6 (ta-b1r2 and ta-b2 use program 1's question pools) and 7 are; programs 4 and 5 are not. Program 6 is kept as a
# secondary grouping ("alt"), tagged in the same packet.
BASELINE = ("settled-science", "self-grading")
ALT = ("test-awareness",)
# D21a (F1): the population frozen by bet id (settled at eaf8d1f's parent, 3a02570, as section 2 reads)
FROZEN = {"target": ["om-p2-3b", "om-p2-5", "om-p2-6", "om-p2-6r", "om-p2-7", "om-p2-15", "om-p2-5r"],
          "baseline": ["ss-b1", "ss-b2", "ss-b3", "ss-b5", "ss-b6", "ss-b7", "ss-b10", "ss-b11", "ss-b12", "sg-b1", "sg-b2", "sg-b3"],
          "alt": ["ta-b2", "ta-b3", "ta-b1r2"]}
# D21a (F4): the pilot set, excluded from the test: program 2's pre-cutoff bets and programs 3 and 7
PILOT = ["om-p2-1", "om-p2-2", "om-p2-3", "om-p2-4", "ng-p3-1", "ng-p3-5", "ng-p3-2", "ng-p3-15", "ng-p3-5c", "ng-p3-16",
         "ng-p3-18", "sv-b1", "sv-b2", "sv-b3"]
BAR, MARGIN, EPS = 0.50, 0.15, 1e-9
MIN_UNITS = {"target": 10, "baseline": 10}
SHUFFLE_SEED = 20261105                                          # fixed constant: only the packet order
TRAILING = re.compile(r"(?m)^(?:Also |No other |Optional|Not required|Ledger, not|Ledger fix|Suggested|Recommended|---|\*\*Required addition|\*\*Harness|The remaining sentence|.{0,40}[Nn]ot required:)")
INLINE_TAIL = re.compile(r"\s(?:Optional:|Optional,|Not required:|Recommended, not required)")
KIND = re.compile(r"\s*(?:\(?Kind:?\s*(?:world|design|execution|artefact)\.?\)?|\((?:world|design|execution|artefact)\)|\(Disclosure:[^)]*\))\s*", re.I)
PAT_ID = re.compile(r"\bP(?:1[0-7]|[1-9])\b")


def git_time(commit):
    return subprocess.run(["git", "-C", str(ENGINE), "log", "-1", "--format=%aI", commit], capture_output=True,
                          text=True, check=True).stdout.strip()


def population(groups=FROZEN):
    """The frozen bets (D21a F1), one entry per audit file (ss-b1..b3 share one audit and count once)."""
    bets = {json.loads(l)["id"]: json.loads(l) for l in (ENGINE / "ledger" / "bets.jsonl").read_text().splitlines() if l.strip()}
    seen, pop = set(), []
    for group, ids in groups.items():
        for i in ids:
            b = bets[i]
            assert b.get("audit") and (ENGINE / b["audit"]).exists(), i
            pop.append((group, b, b["audit"] not in seen))
            seen.add(b["audit"])
    return pop


def plants_by_bet():
    """{bet: {cut numbers}} from the revealed plants in ledger/plants.jsonl ('Required cuts, item N' / 'cut N')."""
    out = {}
    for l in (ENGINE / "ledger" / "plants.jsonl").read_text().splitlines():
        if not l.strip():
            continue
        r = json.loads(l)
        w = r.get("caught_where") or ""
        for n in re.findall(r"[Rr]equired cuts?,? (?:item )?(\d+)|[Cc]ut (\d+)", w):
            out.setdefault(r["bet"], set()).update(int(x) for x in n if x)
    return out


def plant_cuts(text):
    rev = text.split("Revealed", 1)[1] if "Revealed" in text else ""
    return {int(n) for pair in re.findall(r"[Rr]equired cut (\d+) is the plant|[Cc]ut (\d+) (?:was|is) (?:the )?plant|"
                                          r"[Rr]equired cuts?,? item (\d+)\)?[^.]*?(?:caught|plant)", rev) for n in pair if n}


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
        body = body[:t.start()] if t else body
        t2 = INLINE_TAIL.search(body)
        out.append((int(parts[i]), (body[:t2.start()] if t2 else body).strip()))
    return out


def clean(t):
    """D21a (F1): strip the auditor's kind label and disclosure from a miss, and mask pattern ids anywhere."""
    t = re.sub(r"^(?:world|design|execution|artefact):\s*", "", t.strip(), flags=re.I)
    return PAT_ID.sub("[pattern]", KIND.sub(" ", t)).strip()


def build_units(groups=FROZEN, prefix="U", seed=SHUFFLE_SEED):
    units = []
    pb = plants_by_bet()
    for group, b, first_for_audit in population(groups):
        text = (ENGINE / b["audit"]).read_text()
        if b.get("failed") and b.get("failure_reason"):
            units.append({"group": group, "program": b["program"], "bet": b["id"], "kind": "miss",
                          "bet_title": b.get("title", ""), "text": clean(b["failure_reason"]),
                          "source": f"{b['id']} ledger row failure_reason"})
        if not first_for_audit:
            continue
        plants = plant_cuts(text) | pb.get(b["id"], set()) | set().union(
            *[pb.get(x["id"], set()) for _, x, _ in population(groups) if x.get("audit") == b["audit"]])
        for n, txt in required_cuts(text):
            if n in plants or not txt:
                continue
            units.append({"group": group, "program": b["program"], "bet": b["id"], "kind": "cut",
                          "bet_title": b.get("title", ""), "text": PAT_ID.sub("[pattern]", txt),
                          "source": f"{b['audit']} Required cuts item {n}"})
    order = list(range(len(units)))
    random.Random(seed).shuffle(order)
    for k, i in enumerate(order):
        units[i]["unit"] = f"{prefix}{k + 1:03d}"
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
         "Reply with JSON only: `{\"<unit id>\": {\"patterns\": [\"P3\", ...] or [\"none\"], \"why\": \"<at most 25 words>\"}, "
         "...}`, one entry for every unit.", "", "## Patterns", ""]
    for p in pats:
        L.append(f"- **{p['id']}. {p['title']}.** What to do: {p['what_to_do']}")
    L += ["", "## Units", ""]
    for u in units:
        L.append(f"### {u['unit']} ({u['kind']})\n\nTest: {u['bet_title']}\n\n{u['text']}\n")
    PACKET.write_text("\n".join(L) + "\n")


PILOT_UNITS, PILOT_PACKET = DATA / "p2-path2-pilot-units.json", DATA / "p2-path2-pilot-packet.md"
PILOT_N, PILOT_SEED = 40, 11


def units_cmd():
    units = build_units()
    UNITS.write_text(json.dumps({"cutoff": CUTOFF, "target": TARGET, "baseline": list(BASELINE), "alt": list(ALT),
                                 "frozen": FROZEN, "units": units}, indent=1))
    write_packet(units, patterns_for_classifier())
    pilot = build_units({"pilot": PILOT}, "X", PILOT_SEED)
    pilot = sorted(random.Random(PILOT_SEED).sample(pilot, PILOT_N), key=lambda u: u["unit"])
    PILOT_UNITS.write_text(json.dumps({"pilot_bets": PILOT, "units": pilot}, indent=1))
    keep = PACKET.read_text()
    write_packet(pilot, patterns_for_classifier())
    PILOT_PACKET.write_text(PACKET.read_text())
    PACKET.write_text(keep)
    print(f"pilot: {len(pilot)} units sampled from {len(PILOT)} excluded bets")
    for g in ("target", "baseline", "alt"):
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


def shares(units, tags, p1, groups=("target", "baseline", "alt")):
    out = {}
    for g in groups:
        us = [u for u in units if u["group"] == g]
        k = sum(1 for u in us if set(tags[u["unit"]]["patterns"]) & p1)
        out[g] = {"n": len(us), "k": k, "share": k / len(us) if us else float("nan"),
                  "tags_per_unit": sum(len([p for p in tags[u["unit"]]["patterns"] if p != "none"]) for u in us) / max(1, len(us)),
                  "any_pattern": sum(1 for u in us if tags[u["unit"]]["patterns"] != ["none"]) / max(1, len(us))}
    return out


def diff_of(units, tags, p1, base=("baseline",)):
    t = [u for u in units if u["group"] == "target"]
    b = [u for u in units if u["group"] in base]
    c = lambda us: sum(1 for u in us if set(tags[u["unit"]]["patterns"]) & p1) / len(us)
    return c(t) - c(b)


def perm_p(units, tags, p1, base=("baseline",)):
    """D21a (F3): the origin-permutation null. Every way of choosing len(p1) of the 17 patterns as 'program 1' (all
    C(17, k) subsets, exactly); p = share of subsets whose program-2-minus-baseline difference is at least the
    observed one. Small p says the gap is specific to program 1's patterns, not to tagging rates or unit mix."""
    from itertools import combinations
    ids = [f"P{i}" for i in range(1, 18)]
    obs = diff_of(units, tags, p1, base)
    k = len(p1)
    t = [u for u in units if u["group"] == "target"]
    b = [u for u in units if u["group"] in base]
    tset = [set(tags[u["unit"]]["patterns"]) for u in t]
    bset = [set(tags[u["unit"]]["patterns"]) for u in b]
    n = ge = 0
    for comb in combinations(ids, k):
        cs = set(comb)
        d = sum(1 for x in tset if x & cs) / len(t) - sum(1 for x in bset if x & cs) / len(b)
        n += 1
        ge += d >= obs - EPS
    return ge / n, obs


def label_of(sh, p_perm=0.0):
    if sh["target"]["n"] < MIN_UNITS["target"] or sh["baseline"]["n"] < MIN_UNITS["baseline"]:
        return "untestable"
    ok = (sh["target"]["share"] >= BAR - EPS and sh["target"]["share"] - sh["baseline"]["share"] >= MARGIN - EPS
          and p_perm < PERM_ALPHA - EPS)                       # D21a (F3): added, not swapped (P17)
    return "pass" if ok else "fail"


PERM_ALPHA = 0.05


SENT = {
    "pass": ("Of program 2's {nt} misses and required audit cuts on bets pre-registered after 2026-11-04 17:00, {kt} "
             "({st:.0%}) carry a failure pattern found first in program 1's pre-gate work by the origin rule, against "
             "{sb:.0%} of {nb} from programs 4 and 5, as tagged by a fresh classifier blind to this bet's question and to "
             "each pattern's origin; the gap is larger than for {perm:.0%} of the other ways of choosing the same number of "
             "patterns. The pre-registered event occurred (at least half, at least 15 points above the baseline, and "
             "specific to program 1's patterns)."),
    "fail": ("Of program 2's {nt} misses and required audit cuts on bets pre-registered after 2026-11-04 17:00, {kt} "
             "({st:.0%}) carry a failure pattern found first in program 1's pre-gate work by the origin rule, against "
             "{sb:.0%} of {nb} from programs 4 and 5, as tagged by a fresh classifier blind to this bet's question and to "
             "each pattern's origin; {perm:.0%} of the other ways of choosing the same number of patterns give a gap at "
             "least as large. The pre-registered event did not occur (it needed at least half, at least 15 points above "
             "the baseline, and a gap specific to program 1's patterns)."),
    "untestable": "The test could not answer: {why}.",
}


def score_cmd():
    U = json.loads(UNITS.read_text())
    units = U["units"]
    pat_ids = {p["id"] for p in patterns_for_classifier()}
    p1 = origin_set()
    tA = json.loads(TAGS["A"].read_text())["tags"]
    bad = validate(units, tA, pat_ids)
    res = {"origin_program1": sorted(p1, key=lambda x: int(x[1:])), "validation": bad}
    if bad:
        res.update({"label": "untestable", "sentence": SENT["untestable"].format(why="; ".join(bad[:5]))})
    else:
        sh = shares(units, tA, p1)
        pp, obs = perm_p(units, tA, p1)
        lab = label_of(sh, pp)
        res.update({"label": lab, "shares": sh, "difference": obs, "perm_p": pp})
        res["sentence"] = SENT["untestable"].format(why="too few units") if lab == "untestable" else SENT[lab].format(
            nt=sh["target"]["n"], kt=sh["target"]["k"], st=sh["target"]["share"], sb=sh["baseline"]["share"],
            nb=sh["baseline"]["n"], perm=1 - pp if lab == "pass" else pp)
        cuts = [u for u in units if u["kind"] == "cut"]
        res["cuts_only"] = {"shares": shares(cuts, tA, p1), "difference": diff_of(cuts, tA, p1)}
        alt_units = [dict(u, group="baseline") if u["group"] == "alt" else u for u in units]
        sh_alt = shares(alt_units, tA, p1, ("target", "baseline"))
        pp_alt, _ = perm_p(alt_units, tA, p1)
        res["grouping_4_5_6"] = {"shares": sh_alt, "perm_p": pp_alt, "label_would_be": label_of(sh_alt, pp_alt)}
        res["baseline_by_program"] = {}
        for prog in BASELINE + ALT:
            us = [u for u in units if u["program"] == prog]
            res["baseline_by_program"][prog] = {"n": len(us), "share": sum(1 for u in us if set(tA[u["unit"]]["patterns"]) & p1) / len(us)}
        res["leave_one_baseline_program_out"] = {}
        for prog in BASELINE:
            sub = [u for u in units if u["program"] != prog]
            shs = shares(sub, tA, p1, ("target", "baseline"))
            res["leave_one_baseline_program_out"][prog] = {"baseline_share": shs["baseline"]["share"],
                                                           "label_would_be": label_of(shs, perm_p(sub, tA, p1)[0]) if shs["baseline"]["n"] >= MIN_UNITS["baseline"] else "too few"}
        flipped = p1 ^ {"P9"}
        shp = shares(units, tA, flipped)
        res["sensitivity_p9_flipped"] = {"target": shp["target"]["share"], "baseline": shp["baseline"]["share"],
                                         "label_would_be": label_of(shp, perm_p(units, tA, flipped)[0])}
        res["leave_one_bet_out_flips"] = []
        for b in dict.fromkeys(u["bet"] for u in units if u["group"] in ("target", "baseline")):
            sub = [u for u in units if u["bet"] != b]
            if label_of(shares(sub, tA, p1, ("target", "baseline")), perm_p(sub, tA, p1)[0]) != lab:
                res["leave_one_bet_out_flips"].append(b)
        counts = {}
        for u in units:
            for p_ in tA[u["unit"]]["patterns"]:
                counts.setdefault(u["group"], {}).setdefault(p_, 0)
                counts[u["group"]][p_] += 1
        res["pattern_counts"] = counts
    if TAGS["B"].exists():
        tB = json.loads(TAGS["B"].read_text())["tags"]
        badB = validate(units, tB, pat_ids)
        if badB:
            res["classifier_B"] = {"validation": badB, "note": "fails validation; reported, not used"}
        elif "shares" in res:
            shB = shares(units, tB, p1)
            a_ = [bool(set(tA[u["unit"]]["patterns"]) & p1) for u in units]
            b_ = [bool(set(tB[u["unit"]]["patterns"]) & p1) for u in units]
            n = len(a_)
            po = sum(x == y for x, y in zip(a_, b_)) / n
            pa, pb = sum(a_) / n, sum(b_) / n
            pe = pa * pb + (1 - pa) * (1 - pb)
            res["classifier_B"] = {"shares": shB, "perm_p": perm_p(units, tB, p1)[0], "label_would_be": label_of(shB, perm_p(units, tB, p1)[0]),
                                   "agreement": po, "kappa": (po - pe) / (1 - pe) if pe < 1 else 1.0}
    OUT.write_text(json.dumps(res, indent=1))
    L = ["# P2-path2 tables (generated by experiments/p2_path2.py score; do not edit)", "", f"**{res['label']}.** {res['sentence']}", ""]
    if "shares" in res:
        L += ["| group | units | carry a program-1 pattern | share | tags per unit | carry any pattern |", "|---|---|---|---|---|---|"]
        for g, nm in (("target", "program 2"), ("baseline", "programs 4, 5 (baseline)"), ("alt", "program 6 (secondary grouping)")):
            x = res["shares"][g]
            L.append(f"| {nm} | {x['n']} | {x['k']} | {x['share']:.3f} | {x['tags_per_unit']:.2f} | {x['any_pattern']:.3f} |")
        L += ["", f"Difference (program 2 minus baseline): {res['difference']:+.3f}; origin-permutation p = {res['perm_p']:.4f} "
              f"(bar: share >= 0.50, difference >= +0.15, p < 0.05). Cuts only: difference {res['cuts_only']['difference']:+.3f}.",
              f"Program-1 patterns by the origin rule: {', '.join(res['origin_program1'])}.",
              f"Grouping 4, 5, 6: baseline {res['grouping_4_5_6']['shares']['baseline']['share']:.3f}, p = {res['grouping_4_5_6']['perm_p']:.4f}, label would be {res['grouping_4_5_6']['label_would_be']}.",
              "Baseline by program: " + "; ".join(f"{k} {v['share']:.3f} (n {v['n']})" for k, v in res["baseline_by_program"].items()) + ".",
              "Leave one baseline program out: " + "; ".join(f"without {k}: baseline {v['baseline_share']:.3f}, label {v['label_would_be']}" for k, v in res["leave_one_baseline_program_out"].items()) + ".",
              f"With P9's origin flipped: program 2 {res['sensitivity_p9_flipped']['target']:.3f}, baseline {res['sensitivity_p9_flipped']['baseline']:.3f}, label {res['sensitivity_p9_flipped']['label_would_be']}.",
              f"Leave-one-bet-out label flips: {res['leave_one_bet_out_flips'] or 'none'}.", "",
              "| unit | group | bet | kind | patterns (A) | program-1 pattern | why (A) |", "|---|---|---|---|---|---|---|"]
        for u in units:
            t = tA[u["unit"]]
            L.append(f"| {u['unit']} | {u['group']} | {u['bet']} | {u['kind']} | {', '.join(t['patterns'])} | "
                     f"{'yes' if set(t['patterns']) & p1 else 'no'} | {t.get('why', '').replace('|', '/')} |")
    if "classifier_B" in res:
        c = res["classifier_B"]
        L += [""] + ([f"Classifier B fails validation ({len(c['validation'])} problems; first: {c['validation'][0]}); not used."] if "validation" in c else
                     [f"Classifier B: program 2 {c['shares']['target']['share']:.3f}, baseline {c['shares']['baseline']['share']:.3f}, p = {c['perm_p']:.4f}, "
                      f"label would be {c['label_would_be']}; agreement with A on 'carries a program-1 pattern' {c['agreement']:.2f}, kappa {c['kappa']:.2f}."])
    TABLES.write_text("\n".join(L) + "\n")
    print(TABLES.read_text())


PILOT_TAGS = DATA / "p2-path2-pilot-tags.json"


def dryrun_cmd(sims=1500):
    """D11 on measured tag sets (D21a F4): the pilot's tags (classifier A's model on 40 excluded units) are resampled
    into the real group sizes. Null world: every unit draws a pilot tag set at random (no path dependence). Path
    worlds: as null, but each program 2 unit also gains one random program-1 pattern with probability q."""
    U = json.loads(UNITS.read_text())["units"]
    nt = sum(u["group"] == "target" for u in U)
    nb = sum(u["group"] == "baseline" for u in U)
    pool = [v["patterns"] for v in json.loads(PILOT_TAGS.read_text())["tags"].values()]
    p1 = sorted(origin_set(), key=lambda x: int(x[1:]))
    rate = sum(1 for x in pool if set(x) & set(p1)) / len(pool)
    print(f"units: program 2 {nt}, baseline {nb}; pilot tag sets {len(pool)}, carrying a program-1 pattern {rate:.3f}")
    rng = random.Random(3)
    for q in (0.0, 0.25, 0.5, 0.75):
        n = 0
        for _ in range(sims):
            fake = []
            for i in range(nt):
                t = list(rng.choice(pool))
                if rng.random() < q:
                    t = [x for x in t if x != "none"] + [rng.choice(p1)]
                fake.append({"unit": f"t{i}", "group": "target", "patterns": t})
            for i in range(nb):
                fake.append({"unit": f"b{i}", "group": "baseline", "patterns": list(rng.choice(pool))})
            tags = {f["unit"]: {"patterns": f["patterns"]} for f in fake}
            sh = shares(fake, tags, set(p1), ("target", "baseline"))
            pp, _ = perm_p(fake, tags, set(p1)) if sh["target"]["share"] >= BAR - EPS and sh["target"]["share"] - sh["baseline"]["share"] >= MARGIN - EPS else (1.0, None)
            n += label_of(sh, pp) == "pass"
        print(f"  q = {q:.2f}: P(pass) {n / sims:.3f}")
    print("  boundary and validation checks: run in the earlier dry run (experiments/p2-path2-dryrun-output.txt)")


PROMPT_HEAD = ("You are a classifier. Use no tools of any kind: do not read, search, run or open anything. Everything you "
               "need is below. Read the packet and reply with the JSON object it asks for and nothing else.\n\n")


def prompts_cmd():
    """D21a (F5): the exact classifier prompts, written to files with their SHA-256, committed before any tag."""
    import hashlib
    rec = {}
    for name, packet in (("pilot", PILOT_PACKET), ("test", PACKET)):
        text = PROMPT_HEAD + packet.read_text()
        f = DATA / f"p2-path2-prompt-{name}.txt"
        f.write_text(text)
        rec[name] = {"file": f.name, "sha256": hashlib.sha256(text.encode()).hexdigest(), "chars": len(text)}
    (DATA / "p2-path2-prompts.sha256.json").write_text(json.dumps(rec, indent=1))
    print(json.dumps(rec, indent=1))


def save_tags_cmd():
    """python3 experiments/p2_path2.py save <A|B|pilot> <reply file> <tool_uses>: store a classifier's reply verbatim
    with its parsed tags; a reply that is not one JSON object, or a session that used any tool, is stored as untestable."""
    which, reply_file, tool_uses = sys.argv[2], Path(sys.argv[3]), int(sys.argv[4])
    raw = reply_file.read_text()
    m = re.search(r"\{.*\}", raw, re.S)
    try:
        tags = json.loads(m.group(0)) if m else None
    except json.JSONDecodeError:
        tags = None
    out = {"raw_reply": raw, "tool_uses": tool_uses, "tags": tags if (tags is not None and tool_uses == 0) else {},
           "untestable_reason": None if (tags is not None and tool_uses == 0) else
           ("used a tool" if tool_uses else "reply is not a JSON object")}
    f = PILOT_TAGS if which == "pilot" else TAGS[which]
    f.write_text(json.dumps(out, indent=1))
    print(f"{f.name}: {len(out['tags'])} units tagged; tool uses {tool_uses}; {out['untestable_reason'] or 'ok'}")


if __name__ == "__main__":
    {"units": units_cmd, "score": score_cmd, "dryrun": dryrun_cmd, "prompts": prompts_cmd, "save": save_tags_cmd}[sys.argv[1]]()
