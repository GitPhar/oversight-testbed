#!/usr/bin/env python3
"""Rebuild every settled-science results table from the archived bets and items, and check it against the committed one.

    python3 programs/settled-science/reproduce.py            # from the repo root; needs numpy, no keys, no network
    python3 programs/settled-science/reproduce.py --serial   # the same, without worker processes (about 2.5 minutes)

In plain English. The program's numbers all come from one scorer, scoring/score.py, run four ways. It reads only archived
files: the items (items/items.jsonl, items/r2/items.jsonl) and the bettor's and raters' answers (bettor/bets.jsonl,
bettor/r2-bets.jsonl, bettor/r2-valence.jsonl, bettor/r2-valence-retest.jsonl, bettor/r2-striking.jsonl,
bettor/r2-striking-retest.jsonl). It makes no model call. This script takes the program's files as they are at git HEAD
into a temporary folder, blocks keys, the network and every package except numpy, and runs the scorer there:

  round 1 (ss-b1..b3)   score.py         -> scoring/tables.md, scoring/scores.json
  round 2 (ss-b4, b5)   score.py --r2    -> scoring/r2-tables.md, scoring/r2-scores.json
  ss-b6 (valence)       score.py --b6    -> scoring/b6-scores.json
  ss-b7 (striking)      score.py --b7    -> scoring/b7-scores.json

The two tables files are wholly generated ("do not edit by hand") and are compared byte for byte. The four scores files
are compared byte for byte too, except for a newline at the very end of the file (the committed b7-scores.json ends with
one; score.py writes none). Bootstrap intervals and null simulations use the scorer's own seeds (BOOT_SEED 20261104 and
the 20 seeds after it); nothing is reseeded here.

Speed, and why it changes nothing. score.py --b7 runs 21 null simulations of 100 leave-one-out logistic fits each, which
take about 2.5 minutes in one process. This script runs those 21 calls of score.null_sims, with the same arguments and
seeds, in parallel worker processes first, and hands score_b7 the results. If score_b7 asks for anything else (other rows,
another sigma or seed), it runs the original function itself. The output is compared with the committed file either way;
`--serial` skips the workers.

The four results/*.md files are hand-written write-ups. Their prose, process-and-spend tables and "where it stands"
tables are not generated, so they are not compared as text. What is checked, cell by cell or number by number, is every
table cell and in-text number that the write-up copies from the scorer's output, rendered from the regenerated scores in
the write-up's own style (Unicode minus, bold where the write-up bolds). Labels in the first column, odds, costs, and
hand-written qualifiers ("unreplicated") are not checked. In detail:

  ss-b1-results.md  the verdict column of the three bets; the cutoff-side, field (post and pre), year, publication-bias
                    and calibration tables; the leakage-check table's rewritten/clean split (bootstrapped with the
                    scorer's seed), leave-one-out, Option-1 count and out-of-range/long-rationale counts; the plain-English
                    and order-check numbers. Not checked: the up-word rule row of the leakage-check table (exploratory, no
                    archived code), the confidence gap in plain English, the leave-one-field-out bound (+0.019, the
                    audit's), the engine-calibration Brier (from the odds), and the spend table.
  ss-b5-results.md  the ss-b5 verdict and its sentence's two intervals; the measures, query-bucket and calibration
                    tables; the exploratory up/down and word-pair table and the September-onward subset (recomputed from
                    the regenerated rows with the scorer's boot_ci and seed); the order check; leave-one-bucket-out sizes;
                    plain-English numbers. Not checked: leakage-check counts (146 of 243), the greedy count of 9, spend.
  ss-b6-results.md  the verdict (after an audit reversal: the ledger's verdict with the scorer's label beside it) and the pre-registered sentence (exact); gates, measures, robustness and rater-noise
                    tables; the opposite-sentence paragraph; plain-English numbers. Not checked: the design review's
                    and the auditor's simulation rates (8%, 20-66%, 58%), spend.
  ss-b7-results.md  the verdict and the pre-registered sentence (exact); the noise-margin, gates, measures and robustness
                    tables; plain-English and subset numbers. Not checked: the six near-50 ratings, the 82%/17 split and
                    the auditor's +0.0001 subset margin, the reading of the 14 G3 rationales, spend, and the summary table.

Nothing is a gap: every file the scorer needs is in the archive. The leakage checks, the bettor and the raters made the
archived answers with model calls; those calls are not rerun, so this checks the scoring, not the answers.
"""
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # programs/
import repro_common as R  # noqa: E402

M = "−"   # the write-ups' minus sign


# ---------------- number styles used in the write-ups ----------------
def u(x, nd=3, plus=False):
    s = f"{x:.{nd}f}"
    if plus and not s.startswith("-"):
        s = "+" + s
    return s.replace("-", M)


def iv(c, nd=3, plus=False):
    return f"[{u(c[0], nd, plus)}, {u(c[1], nd, plus)}]"


def dci(d, c, nd=3, plus=False, plus_ci=None):
    return f"{u(d, nd, plus)} {iv(c, nd, plus if plus_ci is None else plus_ci)}"


def pct(x):
    return f"{x * 100:.0f}%"


def join_and(xs):
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def sci(p):
    """1.4e-09 -> '1.4 × 10⁻⁹' (the write-up's style)."""
    m, e = f"{p:.1e}".split("e")
    sup = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
    return f"{m} × 10{str(int(e)).translate(sup)}"


# ---------------- the write-up check ----------------
def cells(line):
    return [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]


def check_writeup(rep, name, text, tables, values):
    """tables: [(table index, {data row index: {column index: regenerated text, or (text, 'prefix')}})];
    values: [(label, regex with groups over the committed text, regenerated text with groups joined by ' / ')].
    Both sides become 'label: value' lines; rep.compare reports the first that differs."""
    have = R.tables_of(text)
    com, gen, n_cells = [], [], 0
    for j, rows in tables:
        for i, cols in rows.items():
            for col, want in cols.items():
                prefix = isinstance(want, tuple)
                want = want[0] if prefix else want
                try:
                    cell = cells(have[j][2 + i])[col]
                except IndexError:
                    cell = "<no such cell in the committed file>"
                if prefix:
                    cell = cell[:len(want)]
                tag = f"table {j + 1}, row {i + 1}, column {col + 1}{' (start)' if prefix else ''}"
                com.append(f"{tag}: {cell}")
                gen.append(f"{tag}: {want}")
                n_cells += 1
    for label, pat, want in values:
        m = re.search(pat, text, re.M)
        com.append(f"{label}: {' / '.join(m.groups()) if m else '<not found in the committed text>'}")
        gen.append(f"{label}: {want}")
    rep.compare(name, com, gen, what=f"{n_cells} table cells in {len(tables)} tables and {len(values)} numbers in the text")


def lines(p):
    return [json.loads(l) for l in Path(p).read_text().splitlines() if l.strip()]


# ---------------- parallel null simulations (same function, same arguments, same seeds) ----------------
def _worker_init(scoring_dir):
    R.lockdown()
    sys.dont_write_bytecode = True
    sys.path.insert(0, scoring_dir)


def _null_sims(args):
    import score
    rows, sigma, seed = args
    return seed, score.null_sims(rows, sigma, seed=seed)


def prepare_b7(score, workers):
    """Run score_b7's 21 null_sims calls in parallel; patch score.null_sims to return them when asked for exactly them."""
    items = {it["id"]: it for it in lines(score.R2_ITEMS)}
    bets, rater, retest = lines(score.R2_BETS), lines(score.R2_STRIKING), lines(score.R2_STRIKING_RETEST)
    base = score.score_b6(items, bets, rater, gate_g1=False)
    if base["n"] < 60 or "leg1" not in base:
        return 0
    rows = base["rows"]
    sigma, npairs = score.retest_sigma({v["id"]: v for v in rater}, {v["id"]: v for v in retest})
    if sigma is None or npairs < score.MIN_RETEST:
        return 0
    seeds = [score.BOOT_SEED] + [score.BOOT_SEED + 1 + k for k in range(score.N_SEEDS)]
    import multiprocessing as mp
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(max_workers=min(workers, len(seeds)), mp_context=mp.get_context("spawn"),
                             initializer=_worker_init, initargs=(str(Path(score.__file__).parent),)) as ex:
        done = dict(ex.map(_null_sims, [(rows, sigma, sd) for sd in seeds]))
    key = json.dumps(rows, sort_keys=True)
    orig = score.null_sims

    def null_sims(rows_, sigma_, seed=score.BOOT_SEED):
        if seed in done and sigma_ == sigma and json.dumps(rows_, sort_keys=True) == key:
            return done[seed].copy()
        return orig(rows_, sigma_, seed=seed)
    score.null_sims = null_sims
    return len(seeds)


# ---------------- the write-ups ----------------
def check_b1(rep, root, s):
    name = "results/ss-b1-results.md"
    text = (root / name).read_text()
    import score
    items = score.load_items()
    bets = lines(score.BETS)
    pp, pc, bs = s["primary_post"], s["pre_cutoff"], s["bets"]
    lab = lambda b: bs[b].get("label_reported", bs[b]["label"])  # noqa: E731
    side = lambda v, bold=False: {1: str(v["n"]), 2: f"**{u(v['brier'])}**" if bold else u(v["brier"]), 3: iv(v["brier_ci"]),  # noqa: E731
                                  4: f"{v['accuracy']:.2f}", 5: u(v["headline_brier"]),
                                  6: dci(v["minus_headline"], v["minus_headline_ci"])}
    fld = lambda v, g, base=True: {0: g.replace("-", " "), 1: str(v["n"]), 2: u(v["brier"]), 3: iv(v["brier_ci"]),  # noqa: E731
                                   4: f"{v['accuracy']:.2f}", **({5: dci(v["minus_headline"], v["minus_headline_ci"])} if base else {})}
    yr = lambda v, bold=False: {2: f"**{v['n']}**" if bold else str(v["n"]), 3: f"**{u(v['brier'])}**" if bold else u(v["brier"]),  # noqa: E731
                                4: iv(v["brier_ci"]), 5: f"{v['accuracy']:.2f}"}
    cal = lambda cs: {i: {0: c["bucket"].replace("-", "–"), 1: str(c["n"]), 2: f"{c['mean_conf']:.2f}", 3: f"{c['hit_rate']:.2f}"}  # noqa: E731
                      for i, c in enumerate(cs)}
    post_rows = [r for r in s["rows"] if r["side"] == "post"]
    split = {}
    for st in ("rewritten", "clean"):
        rs = [r for r in post_rows if (items[r["id"]]["leakage_status"] == "clean") == (st == "clean")]
        split[st] = (score.brier([r["p_true"] for r in rs]), score.boot_ci([(1 - r["p_true"]) ** 2 for r in rs]), len(rs))
    rw, cl = split["rewritten"], split["clean"]
    flips = sorted({i for b in bs.values() for i in b["fragile_items"]})
    prim = [b for b in bets if b["kind"] == "primary"]
    opt1 = sum(1 for b in prim if items[b["id"]]["side"] == "post" and b["option_1_is"] == items[b["id"]]["true_option"])
    long_rat = sum(1 for b in bets if len((b.get("rationale") or "").split()) > 100)
    bf = s["by_field"]
    other = s["by_headline"]["post"]["true-is-other"]
    cp = s["calibration_post"]
    hi = [c for c in cp if c["bucket"] in ("0.7-0.8", "0.8-0.9", "0.9-1.0")]
    hi_n, hi_k = sum(c["n"] for c in hi), round(sum(c["hit_rate"] * c["n"] for c in hi))
    c78 = next(c for c in cp if c["bucket"] == "0.7-0.8")
    c67 = next(c for c in cp if c["bucket"] == "0.6-0.7")
    oc = s["order_check"]
    pm = s["pre_minus_post"]
    tables = [
        (0, {i: {2: f"**{lab(b)}, unreplicated**"} for i, b in enumerate(("ss-b1", "ss-b2", "ss-b3"))}),
        (1, {0: side(s["by_side"]["post"]["post"], bold=True), 1: side(s["by_side"]["pre"]["pre"])}),
        (2, {i: fld(v, g) for i, (g, v) in enumerate(bf["post"].items())}),
        (3, {i: fld(v, g, base=False) for i, (g, v) in enumerate(bf["pre"].items())}),
        (4, {0: yr(s["by_year"]["pre"]["2024"]), 1: yr(s["by_year"]["pre"]["2025"]), 2: yr(s["by_year"]["pre"]["2026-pre"]),
             3: yr(s["by_year"]["pre"]["2026-moved"]), 4: yr(s["by_year"]["post"]["2026-post"], bold=True)}),
        (5, {i: {1: str(v["n"]), 2: u(v["brier"]), 3: f"{v['accuracy']:.2f}", 4: u(v["headline_brier"])}
             for i, v in enumerate(s["by_headline"]["post"][g] for g in ("none", "true-is-headline", "true-is-other"))}),
        (6, cal(cp)),
        (7, {0: {2: f"rewritten {u(rw[0])} {iv(rw[1])}, n = {rw[2]}; clean {u(cl[0])} {iv(cl[1])}, n = {cl[2]}"},
             1: {2: "no flips" if not flips else "flips: " + ", ".join(flips)},
             3: {2: (f"{opt1} of {pp['n']}", "prefix")},
             4: {2: f"{s['clipped']}; {long_rat}"}}),
    ]
    values = [
        ("ss-b1 sentence", r"\| ss-b1 \|.*On (\d+) findings.*\(Brier ([^)]*)\)", f"{pp['n']} / {u(pp['brier'])} {iv(pp['brier_ci'])}"),
        ("pre minus post", r"Pre minus post: (\S+ \[[^\]]+\])\.", dci(pm["diff"], pm["ci"])),
        ("share right, post", r"reported direction (\d+%) of the time", pct(pp["accuracy"])),
        ("Brier, post", r"Its Brier score was ([\d.]+) \(95% interval ([\d.]+) to ([\d.]+)\)",
         f"{pp['brier']:.3f} / {pp['brier_ci'][0]:.3f} / {pp['brier_ci'][1]:.3f}"),
        ("baseline", r"leaned 75% toward that side scored (\d+\.\d+)", f"{pp['headline_brier']:.3f}"),
        ("beat the baseline by", r"The bettor beat it by ([\d.]+) \(interval ([\d.]+) to ([\d.]+)\)",
         f"{-pp['minus_headline']:.3f} / {-pp['minus_headline_ci'][1]:.3f} / {-pp['minus_headline_ci'][0]:.3f}"),
        ("against the headline", r"\*against\* its own headline \((\d+) items\), the bettor still got (\d+) of (\d+)",
         f"{other['n']} / {round(other['accuracy'] * other['n'])} / {other['n']}"),
        ("pre-cutoff", r"\((\d+) items, Brier ([\d.]+), (\d+%) right\)", f"{pc['n']} / {pc['brier']:.3f} / {pct(pc['accuracy'])}"),
        ("fields", r"scalable oversight \((\d+%) right\) and interpretability \((\d+%)\)",
         f"{pct(bf['post']['scalable-oversight']['accuracy'])} / {pct(bf['post']['interpretability']['accuracy'])}"),
        ("model psychology", r"model psychology \((\d+%) right, Brier ([\d.]+), interval ([\d.]+) to ([\d.]+)",
         (lambda v: f"{pct(v['accuracy'])} / {v['brier']:.3f} / {v['brier_ci'][0]:.3f} / {v['brier_ci'][1]:.3f}")(bf["post"]["model-psychology"])),
        ("60-70% calls", r"60–70% calls were overconfident \(right (\d+%) of the time\)", pct(c67["hit_rate"])),
        ("70-80% calls", r"When it said 70–80%, it was right (\d+%) of the time \((\d+) of (\d+)\)",
         f"{pct(c78['hit_rate'])} / {round(c78['hit_rate'] * c78['n'])} / {c78['n']}"),
        ("70%+ calls", r"70%\+ calls were right (\d+%) of the time \((\d+) of (\d+)\)", f"{pct(hi_k / hi_n)} / {hi_k} / {hi_n}"),
        ("leave-one-item-out", r"Leave-one-item-out \(D16, 10,000 resamples per bound\): ([^,]+),",
         "no single item flips any of the three labels" if not flips else "flips: " + ", ".join(flips)),
        ("order check", r"(\d+) items \(a beacon-drawn half\).*?same side both times on (\d+%) of them\. Its two probabilities summed "
         r"to 100 within ([\d.]+) points on average\. The pull toward whichever option is shown first was (\S+) points (\[[^\]]+\])",
         f"{oc['n']} / {pct(oc['same_side_rate'])} / {oc['mean_incoherence']:.1f} / {u(oc['mean_first_shown_bonus'], 1)} / "
         f"{iv(oc['first_shown_bonus_ci'], 1)}"),
    ]
    check_writeup(rep, name, text, tables, values)


def check_b5(rep, root, r, s1):
    name = "results/ss-b5-results.md"
    text = (root / name).read_text()
    import score
    items = {it["id"]: it for it in lines(score.R2_ITEMS)}
    sm, pr, b5 = r["summary"], r["pair_rule"], r["bets"]["ss-b5"]
    rows = r["rows"]
    se = lambda rs: [(1 - x["p_true"]) ** 2 for x in rs]  # noqa: E731
    d_up = lambda rs: [(1 - x["p_true"]) ** 2 - (1 - x["headline_p"]) ** 2 for x in rs]  # noqa: E731
    d_pair = lambda rs: [(1 - x["p_true"]) ** 2 - (1 - x["pair_p"]) ** 2 for x in rs]  # noqa: E731
    mean = lambda v: sum(v) / len(v)  # noqa: E731

    def sub(rs, rules=True):
        k = sum(1 for x in rs if x["p_true"] > 0.5)
        out = {1: str(len(rs)), 2: f"{k} ({k / len(rs):.2f})", 3: u(score.brier([x["p_true"] for x in rs])), 4: iv(score.boot_ci(se(rs)))}
        if rules:
            out[5] = dci(mean(d_up(rs)), score.boot_ci(d_up(rs)), plus=True, plus_ci=False)
            out[6] = dci(mean(d_pair(rs)), score.boot_ci(d_pair(rs)), plus=True, plus_ci=False)
        return out
    up = [x for x in rows if x["headline_p"] > 0.5]
    down = [x for x in rows if x["headline_p"] < 0.5]
    sept = [x for x in rows if items[x["id"]]["v1_date"] >= "2026-09"]
    cal = r["calibration"]
    oc = r["order_check"]
    lofo = b5["leave_one_field_out"]
    tables = [
        (0, {0: {2: f"**{b5.get('label_reported', b5['label'])}, unreplicated**"}}),
        (1, {0: {1: str(sm["n"]), 2: f"**{u(sm['brier'])}**", 3: iv(sm["brier_ci"]), 4: f"{sm['accuracy']:.2f}"},
             1: {1: str(sm["n"]), 2: u(sm["headline_brier"])}, 2: {1: str(sm["n"]), 2: u(pr["brier"])}, 3: {1: str(sm["n"])}}),
        (2, {i: {0: g.replace("-", " "), 1: str(v["n"]), 2: u(v["brier"]), 3: iv(v["brier_ci"]), 4: f"{v['accuracy']:.2f}",
                 5: u(v["headline_brier"]), 6: dci(v["minus_headline"], v["minus_headline_ci"])}
             for i, (g, v) in enumerate(r["by_field"].items())}),
        (3, {i: {0: c["bucket"].replace("-", "–"), 1: str(c["n"]), 2: f"{c['mean_conf']:.2f}", 3: f"{c['hit_rate']:.2f}"}
             for i, c in enumerate(cal)}),
        (4, {0: sub(up), 1: sub(down), 2: sub([x for x in rows if x["pair"] == "more/less"], rules=False),
             3: sub([x for x in rows if x["pair"] != "more/less"], rules=False)}),
    ]
    k_down = sum(1 for x in down if x["p_true"] > 0.5)
    values = [
        ("ss-b5 sentence", r"\| ss-b5 \|.*paired Brier difference (\S+ \[[^\]]+\])\) and a rule that uses only which comparative "
         r"word was flipped \((\S+ \[[^\]]+\])\)", f"{dci(sm['minus_headline'], sm['minus_headline_ci'])} / {dci(pr['bettor_minus_pair'], pr['ci'])}"),
        ("ss-b5 sentence n", r"\| ss-b5 \|.*?On (\d+) comparative sentences", str(sm["n"])),
        ("ss-b4 row", r"the bettor's Brier is (\d+\.\d+) against the up-word rule's (\d+\.\d+)", f"{sm['brier']:.3f} / {sm['headline_brier']:.3f}"),
        ("minus up-word rule", r"Bettor minus the up-word rule: (\S+ \[[^\]]+\])\.", dci(sm["minus_headline"], sm["minus_headline_ci"])),
        ("minus swap-pair rule", r"Bettor minus the swap-pair rule: (\S+ \[[^\]]+\])\.", dci(pr["bettor_minus_pair"], pr["ci"])),
        ("picked the published sentence", r"published sentence (\d+%) of the time\*\* \((\d+) of (\d+)\), with a Brier score of ([\d.]+) "
         r"\(interval ([\d.]+) to ([\d.]+)\)", f"{pct(sm['accuracy'])} / {round(sm['accuracy'] * sm['n'])} / {sm['n']} / {sm['brier']:.3f} / "
         f"{sm['brier_ci'][0]:.3f} / {sm['brier_ci'][1]:.3f}"),
        ("up-word rule", r"wording, Brier ([\d.]+), which it beat by ([\d.]+);", f"{sm['headline_brier']:.3f} / {-sm['minus_headline']:.3f}"),
        ("swap-pair rule", r"published one, Brier ([\d.]+), which it beat by ([\d.]+)\.", f"{pr['brier']:.3f} / {-pr['bettor_minus_pair']:.3f}"),
        ("down-word items", r"comes entirely from the (\d+) items where the published sentence carries the 'down' word, where the up-word "
         r"rule is wrong: the bettor was right on (\d+) of them", f"{len(down)} / {k_down}"),
        ("up-word items", r"On the other (\d+) it was no better than the up-word rule \((\S+ \[[^\]]+\])\) and slightly worse than the "
         r"swap-pair rule \((\S+ \[[^\]]+\])\)", f"{len(up)} / {dci(mean(d_up(up)), score.boot_ci(d_up(up)))} / "
         f"{dci(mean(d_pair(up)), score.boot_ci(d_pair(up)), plus=True, plus_ci=False)}"),
        ("down word, still right", r"the bettor was still right on (\d+) of (\d+) \(Brier ([\d.]+)\)",
         f"{k_down} / {len(down)} / {score.brier([x['p_true'] for x in down]):.3f}"),
        ("rounds compared", r"two rounds' scores \(([\d.]+) here, ([\d.]+) in round 1\)", f"{sm['brier']:.3f} / {s1['primary_post']['brier']:.3f}"),
        ("July-August", r"\((\d+) of them in July–August\)", str(sum(1 for x in rows if items[x["id"]]["v1_date"] < "2026-09"))),
        ("from September on", r"On the (\d+) items posted from September on, the bettor still beats both rules \((\S+ \[[^\]]+\]); "
         r"(\S+ \[[^\]]+\])\)", f"{len(sept)} / {dci(mean(d_up(sept)), score.boot_ci(d_up(sept)))} / "
         f"{dci(mean(d_pair(sept)), score.boot_ci(d_pair(sept)))}"),
        ("leave-one-item-out", r"\*\*Leave-one-item-out:\*\* ([^.]+)\.", "no flips" if not b5["fragile_items"] else ", ".join(b5["fragile_items"])),
        ("leave-one-bucket-out", r"ss-b5 (\w+) without interpretability \(n = (\d+)\), without model psychology \((\d+)\), without quantum "
         r"devices \((\d+)\) and without scalable oversight \((\d+)\)",
         " / ".join(["passes" if all(v["label"] == "pass" for v in lofo.values()) else "<not all pass>"]
                    + [str(lofo[f]["n"]) for f in ("interpretability", "model-psychology", "quantum-devices", "scalable-oversight")])),
        ("mean confidence", r"Mean confidence was ([\d.]+), against ([\d.]+) right",
         f"{sum(c['mean_conf'] * c['n'] for c in cal) / sum(c['n'] for c in cal):.2f} / {sm['accuracy']:.2f}"),
        ("order check", r"(\d+) items were asked twice with the options reversed\. The bettor chose the same side (\d+%) of the time\. "
         r"Its two probabilities summed to within ([\d.]+) points of 100 on average\. It showed a pull toward whichever option is shown "
         r"first of (\S+) points (\[[^\]]+\])", f"{oc['n']} / {pct(oc['same_side_rate'])} / {oc['mean_incoherence']:.1f} / "
         f"{u(oc['mean_first_shown_bonus'], 1, plus=True)} / {iv(oc['first_shown_bonus_ci'], 1)}"),
        ("round 1 order check", r"Round 1's was (\S+ \[[^\]]+\])",
         dci(s1["order_check"]["mean_first_shown_bonus"], s1["order_check"]["first_shown_bonus_ci"], nd=1)),
    ]
    check_writeup(rep, name, text, tables, values)


def check_b6(rep, root, b, r):
    name = "results/ss-b6-results.md"
    text = (root / name).read_text()
    L1, L2, sec, g, rn = b["leg1"], b["leg2"], b["secondaries"], b["gates"], b["rater_noise"]
    lofo = b["leave_one_bucket_out"]
    first = [True]

    def without(f):
        s = f"without {f.replace('-', ' ')} " + (f"(n = {lofo[f]['n']})" if first[0] else f"({lofo[f]['n']})")
        first[0] = False
        return s
    lobo = "; ".join(f"{lab} " + " and ".join(without(f) for f in lofo if lofo[f]["label"] == lab)
                     for lab in ("null", "pass") if any(v["label"] == lab for v in lofo.values()))
    leg = lambda v: dci(v["d"], v["ci"], plus=True)  # noqa: E731
    dc, op = b["discordant"], sec["opposite_sides"]
    # The verdict cell: the label the scorer gives, or, once an audit has reversed it, the ledger's verdict with the
    # scorer's label kept beside it ("**undetermined** (round-3 audit; the pre-registered rule was met: ...)").
    rule = f"{b.get('label_reported', b['label'])}, unreplicated"
    led = next((x for x in lines(root.parents[1] / "ledger" / "bets.jsonl") if x.get("id") == "ss-b6"), {})
    v = led.get("verdict")
    verdict = (f"**{v}** (round-3 audit; the pre-registered rule was met: {rule})"
               if v and not rule.startswith(v) else f"**{rule}**")
    tables = [
        (0, {0: {2: verdict}}),
        (1, {0: {1: f"{g['G1_x']} of {g['G1_n']} ({g['G1_share_up']:.2f})"}, 1: {1: f"{g['G1_share_up']:.2f}"},
             2: {1: f"{g['G3_matches']} of {b['n']}"}}),
        (2, {0: {1: str(b["n"]), 2: u(L1["bettor_brier"]), 3: iv(sec["bettor_brier_ci"])},
             1: {1: str(b["n"]), 2: u(L1["valence_brier"]), 3: iv(sec["valence_brier_ci"])},
             2: {1: str(b["n"]), 2: f"{L1['valence_accuracy']:.2f}", 3: iv(sec["valence_accuracy_ci"], 2)},
             3: {1: str(b["n"]), 2: f"**{u(L1['d'])}**", 3: iv(L1["ci"])},
             4: {1: str(b["n"]), 2: f"**{u(L2['d'])}**", 3: iv(L2["ci"])},
             5: {1: str(b["n"]), 2: f"{L2['bettor_recal_brier']:.3f} / {L2['rival_recal_brier']:.3f}"}}),
        (3, {0: {1: f"**flips** on {join_and(b['fragile_items'])}" if b["fragile_items"] else "no flips"},
             1: {1: lobo},
             2: {1: (f"removing **{b['greedy_flip']['k']}** chosen item", "prefix")},
             3: {0: f"leg 1 on the {sec['leg1_up_word']['n']} up-word items", 1: leg(sec["leg1_up_word"])},
             4: {0: f"leg 1 on the {sec['leg1_down_word']['n']} down-word items", 1: leg(sec["leg1_down_word"])},
             5: {0: f"leg 2 on the {b['leg2_up_word']['n']} up-word items", 1: (leg(b["leg2_up_word"]), "prefix")},
             6: {0: f"leg 2 on the {b['leg2_down_word']['n']} down-word items", 1: leg(b["leg2_down_word"])},
             7: {1: (leg(sec["leg2_without_near50_term"]), "prefix")},
             8: {1: f"{dc['n']}; bettor right on {'both' if dc['n'] == dc['bettor_right'] == 2 else dc['bettor_right']}; "
                    f"one-sided sign test p = {dc['one_sided_sign_p']:.2f}"}}),
        (4, {i: {1: str(v["n"]), 2: f"{v['mean_abs_incoherence']:.1f}", 3: iv(v["incoherence_ci"], 1), 4: f"{v['same_side']:.2f}"}
             for i, v in enumerate((rn["rater"], rn["bettor_same_items"]))}),
    ]
    values = [
        ("pre-registered sentence", r"^> (.*)$", b["sentence"]),
        ("flattery rule", r"\*\*That flattery rule alone picked the published sentence (\d+%) of the time\*\* \(Brier ([\d.]+)\), against "
         r"the bettor's (\d+%) \(Brier ([\d.]+)\)", f"{pct(L1['valence_accuracy'])} / {L1['valence_brier']:.3f} / "
         f"{pct(r['summary']['accuracy'])} / {L1['bettor_brier']:.3f}"),
        ("raw comparison", r"the bettor wins by ([\d.]+) \(interval ([\d.]+) to ([\d.]+)\)",
         f"{-L1['d']:.3f} / {-L1['ci'][1]:.3f} / {-L1['ci'][0]:.3f}"),
        ("recalibrated comparison", r"it wins by ([\d.]+) \(interval ([\d.]+) to ([\d.]+)\)",
         f"{-L2['d']:.3f} / {-L2['ci'][1]:.3f} / {-L2['ci'][0]:.3f}"),
        ("fragile items", r"removing any one of three items \(([^)]+)\)", ", ".join(b["fragile_items"])),
        ("rater noise", r"the rater gave the same side (\d+%) of the time, against the bettor's (\d+%) on the same items\. Its average "
         r"inconsistency was ([\d.]+) points against ([\d.]+) \(paired difference (\S+ \[[^\]]+\])\)",
         f"{pct(rn['rater']['same_side'])} / {pct(rn['bettor_same_items']['same_side'])} / {rn['rater']['mean_abs_incoherence']:.1f} / "
         f"{rn['bettor_same_items']['mean_abs_incoherence']:.1f} / "
         f"{dci(rn['paired_incoherence_diff']['d'], rn['paired_incoherence_diff']['ci'], nd=1, plus=True)}"),
        ("opposite sentences", r"pick opposite sentences on only (\d+) of (\d+) items \(([^)]+)\), and the rater says 50 on one more "
         r"\(([^)]+)\); the bettor is right on (\d+) of the (\d+)\. Those (\d+) items carry (\d+%) of leg 1's gap",
         f"{len(op['items'])} / {b['n']} / {', '.join(op['items'])} / {', '.join(op['rater_at_50'])} / {op['bettor_right']} / "
         f"{len(op['items'])} / {len(op['items']) + len(op['rater_at_50'])} / {pct(op['share_of_leg1_gap'])}"),
        ("pre-registered discordant count", r"The pre-registered discordant count, (\d+), uses", str(dc["n"])),
    ]
    check_writeup(rep, name, text, tables, values)


def check_b7(rep, root, k, b6, r):
    name = "results/ss-b7-results.md"
    text = (root / name).read_text()
    import score
    n_retest = sum(1 for x in lines(score.R2_BETS) if x["kind"] == "order-check")
    L1, L2, sec, g = k["leg1"], k["leg2"], k["secondaries"], k["gates"]
    sl = k["seed_labels"]
    lofo = k["leave_one_bucket_out"]
    ns = [v["n"] for v in lofo.values()]
    lobo = (f"pass without each of the four buckets (n = {min(ns)}–{max(ns)})" if all(v["label"] == "pass" for v in lofo.values())
            else "; ".join(f"{f}: {v['label']}" for f, v in lofo.items()))
    leg = lambda v: dci(v["d"], v["ci"])  # noqa: E731
    dc, op = k["discordant"], sec["opposite_sides"]
    tables = [
        (0, {0: {2: f"**{k['verdict_reported']}**"}}),
        (1, {0: {1: f"{k['retest_pairs']} of {n_retest}"}, 1: {1: f"{k['sigma_retest']:.3f}"}, 2: {1: u(k["margin"], 4)},
             3: {1: (f"{k['null_false_pass_at_0']:.2f}", "prefix")}, 4: {1: f"{k['sigma_dis']:.2f}"}, 5: {1: f"{k['world_b_pass_rate']:.2f}"},
             6: {0: f"the label under {len(sl)} extra seeds ({score.BOOT_SEED + 1}–{(score.BOOT_SEED + len(sl)) % 100})",
                 1: f"{k['label']} on {sum(1 for x in sl if x == k['label'])} of {len(sl)}"}}),
        (2, {0: {1: f"{g['G1_x']} of {g['G1_n']} ({g['G1_share_up']:.2f})"}, 1: {1: f"{g['G3_matches']} of {k['n']}"}}),
        (3, {0: {1: str(k["n"]), 2: u(L1["bettor_brier"]), 3: iv(sec["bettor_brier_ci"])},
             1: {1: str(k["n"]), 2: u(L1["valence_brier"]), 3: iv(sec["valence_brier_ci"])},
             2: {1: str(k["n"]), 2: f"{L1['valence_accuracy']:.2f}", 3: iv(sec["valence_accuracy_ci"], 2)},
             3: {1: str(k["n"]), 2: f"**{u(L1['d'])}**", 3: iv(L1["ci"])},
             4: {1: str(k["n"]), 2: f"**{u(L2['d'])}**", 3: iv(L2["ci"])},
             5: {1: str(k["n"]), 2: f"{L2['bettor_recal_brier']:.3f} / {L2['rival_recal_brier']:.3f}"},
             6: {1: str(k["n"]), 2: u(sec["leg2_without_near50_term"]["d"]), 3: iv(sec["leg2_without_near50_term"]["ci"])}}),
        (4, {0: {0: f"leg 1, up-word items ({sec['leg1_up_word']['n']})", 1: leg(sec["leg1_up_word"])},
             1: {0: f"leg 1, down-word items ({sec['leg1_down_word']['n']})", 1: leg(sec["leg1_down_word"])},
             2: {0: f"leg 2, up-word items ({k['leg2_up_word']['n']})", 1: leg(k["leg2_up_word"])},
             3: {0: f"leg 2, down-word items ({k['leg2_down_word']['n']})", 1: leg(k["leg2_down_word"])},
             4: {1: "no flips" if not k["fragile_items"] else "flips on " + join_and(k["fragile_items"])},
             5: {1: lobo},
             6: {1: f"{dc['n']}; bettor right on {dc['bettor_right']}; one-sided sign test p = {sci(dc['one_sided_sign_p'])}"},
             7: {1: f"{len(op['items'])} items; bettor right on {op['bettor_right']}"}}),
    ]
    values = [
        ("pre-registered sentence", r"^> (.*)$", k["sentence"]),
        ("round 2 and ss-b6", r"Round 2's bettor picked the published sentence (\d+%) of the time\. A same-model rater asked which version "
         r"flatters the paper matched most of that, at (\d+%)", f"{pct(r['summary']['accuracy'])} / {pct(b6['leg1']['valence_accuracy'])}"),
        ("striking rule", r"It picked the published sentence (\d+%) of the time \(Brier ([\d.]+),",
         f"{pct(L1['valence_accuracy'])} / {L1['valence_brier']:.3f}"),
        ("extra seeds", r"all (\d+) extra seeds agree", str(len(sl)) if k["seeds_other"] == 0 else f"<{k['seeds_other']} disagree>"),
        ("opposite sentences", r"favoured different sentences on (\d+) items, and the bettor was right on (\d+)",
         f"{len(op['items'])} / {op['bettor_right']}"),
        ("discordant count", r"gives (\d+) items and (\d+)\.", f"{dc['n']} / {dc['bettor_right']}"),
        ("world B", r"would pass about (\d+%) of the time", pct(k["world_b_pass_rate"])),
        ("leg 2 up-word bound and full-set margin", r"On the (\d+) up-word items leg 2's bound \((\S+)\).*the full-set margin \((\S+)\)",
         f"{k['leg2_up_word']['n']} / {u(k['leg2_up_word']['ci'][1])} / {u(k['margin'], 4)}"),
    ]
    check_writeup(rep, name, text, tables, values)


# ---------------- ss-b10, ss-b11, ss-b12 (scorers of their own; D51-D53) ----------------
NEW_SCORERS = (  # (results file, scorer module in scoring/, generated files)
    ("results/ss-b10-results.md", "score_bb", ("scoring/bb-tables.md", "scoring/bb-scores.json")),
    ("results/ss-b11-results.md", "score_f3", ("scoring/f3-tables.md", "scoring/f3-scores.json")),
    ("results/ss-b12-results.md", "score_f4", ("scoring/f4-tables.md", "scoring/f4-scores.json")),
    ("results/ss-b13-results.md", "score_f1", ("scoring/f1-tables.md", "scoring/f1-scores.json")),   # D62
    ("results/ss-b10c-results.md", "score_bbb", ("scoring/bbb-tables.md", "scoring/bbb-scores.json")),   # D70
    ("results/ss-b16-results.md", "score_b16", ("scoring/b16-tables.md", "scoring/b16-scores.json")),   # D80
    ("results/ss-b17-results.md", "score_b17", ("scoring/b17-tables.md", "scoring/b17-scores.json")),   # D81
)


def check_new_scorers(rep, root):
    """Each scorer rebuilds its JSON and tables from the archive; both must match byte for byte, and every table in the
    generated tables file must appear, line for line, in the hand-written results file (which quotes them verbatim)."""
    import importlib
    for name, mod, outs in NEW_SCORERS:
        if not (root / name).exists():
            continue
        committed = {f: (root / f).read_text() for f in outs if (root / f).exists()}
        for f in committed:
            (root / f).unlink()
        try:
            m = importlib.import_module(mod)
            sys.argv = [mod + ".py"]
            R.quiet(m.main)
        except Exception as e:  # noqa: BLE001
            for f in outs:
                rep.error(f, e)
            rep.error(name, RuntimeError("its scorer could not be rerun"))
            continue
        ok = True
        for f in outs:
            if f not in committed:
                rep.error(f, FileNotFoundError(f"{f} is not archived"))
                ok = False
            elif not (root / f).exists():
                rep.error(f, FileNotFoundError(f"{mod}.py did not write {f}"))
                ok = False
            else:
                ok &= rep.compare(f, committed[f], (root / f).read_text())
        md = (root / outs[0]).read_text() if (root / outs[0]).exists() else ""
        if ok:
            rep.compare_tables(name, (root / name).read_text(), R.tables_of(md))
        else:
            rep.error(name, RuntimeError("the scores it copies could not be regenerated (see above)"))


# ---------------- main ----------------
def main():
    tmp = R.snapshot(["programs/settled-science", "ledger/bets.jsonl"])  # the ledger: read only, for audit-reversed verdicts     # score.py imports only json, math, random, re, sys and numpy
    try:
        root = tmp / "programs/settled-science"
        sys.path[:0] = [str(root / "scoring")]
        rep = R.Report("settled-science", root, results_globs=("results/*.md", "scoring/*.md"))
        outs = {"": ["scoring/tables.md", "scoring/scores.json"], "--r2": ["scoring/r2-tables.md", "scoring/r2-scores.json"],
                "--b6": ["scoring/b6-scores.json"], "--b7": ["scoring/b7-scores.json"]}
        committed = {f: (root / f).read_text() for fs in outs.values() for f in fs}
        for f in committed:
            (root / f).unlink()                       # every output is rebuilt from scratch
        import score
        workers = 1 if "--serial" in sys.argv else (os.cpu_count() or 1)
        ok = {}
        for flag, files in outs.items():
            def run(flag=flag):
                sys.argv = ["score.py"] + ([flag] if flag else [])
                if flag == "--b7" and workers > 1:
                    prepare_b7(score, workers)
                {"": score.main, "--r2": score.main_r2, "--b6": score.main_b6, "--b7": score.main_b7}[flag]()
            try:
                R.quiet(run)
                ok[flag] = True
            except Exception as e:  # noqa: BLE001
                for f in files:
                    rep.error(f, e)
                ok[flag] = False
                continue
            for f in files:
                p = root / f
                if not p.exists():
                    rep.error(f, FileNotFoundError(f"score.py {flag} did not write {f}"))
                elif f.endswith(".md"):
                    rep.compare(f, committed[f], p.read_text())               # wholly generated: byte for byte
                else:                                                         # the numbers the tables come from
                    rep.compare(f, committed[f].rstrip("\n"), p.read_text().rstrip("\n"),
                                what="byte for byte, apart from a final newline")
        load = lambda f: json.loads((root / f).read_text())  # noqa: E731
        for name, need, fn in (
                ("results/ss-b1-results.md", ("",), lambda: check_b1(rep, root, load("scoring/scores.json"))),
                ("results/ss-b5-results.md", ("", "--r2"),
                 lambda: check_b5(rep, root, load("scoring/r2-scores.json"), load("scoring/scores.json"))),
                ("results/ss-b6-results.md", ("--r2", "--b6"),
                 lambda: check_b6(rep, root, load("scoring/b6-scores.json"), load("scoring/r2-scores.json"))),
                ("results/ss-b7-results.md", ("--r2", "--b6", "--b7"),
                 lambda: check_b7(rep, root, load("scoring/b7-scores.json"), load("scoring/b6-scores.json"),
                                  load("scoring/r2-scores.json")))):
            if not all(ok[f] for f in need):
                rep.error(name, RuntimeError("the scores it copies could not be regenerated (see above)"))
                continue
            try:
                fn()
            except Exception as e:  # noqa: BLE001
                rep.error(name, e)
        check_new_scorers(rep, root)
        return rep.finish()
    finally:
        R.cleanup(tmp)


if __name__ == "__main__":
    R.main_guard(main)
