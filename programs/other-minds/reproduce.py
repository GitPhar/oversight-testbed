#!/usr/bin/env python3
"""Rebuild every results table of program 2 (other-minds) from the archived JSON, with no API key, no network and
only the standard library plus numpy, and check it against the committed files.

    python3 programs/other-minds/reproduce.py        (from the repository root; numpy installed)

What it does, file by file. Each analysis is the experiment's own code, imported from a git-HEAD snapshot and run on
the archived call caches (results/*-calls.json), so the statistics themselves are recomputed, not just reformatted.
Each analysis also rewrites its results JSON inside the snapshot; that JSON is compared, number by number (relative
tolerance 1e-9), with the committed one.

  p2-6-tables.md, p2-6r-tables.md,  written whole by write_md() in p2_6_position_label.py / p2_6r_replication.py /
  p2-7-tables.md                    p2_7_format_fingerprint.py. Regenerated from p2-6-calls.json / p2-6r-calls.json /
                                    p2-7-calls.json (with program 1's gm3b and mm-gm3b archives) and compared byte for
                                    byte.
  p2-6-position-or-label.md,        hand-written write-ups that reproduce those generated tables under "## Tables".
  p2-6r-replication.md,             Every regenerated table must appear, line for line, in the write-up. The prose
  p2-7-format-fingerprint.md
                                    (and an audit note added to one bullet of p2-6r) is hand-written and not compared.
  p2-1-framing.md, p2-2-perspective.md, p2-3b-simpletom-lowsev.md, p2-3b-pilot.md, p2-4-interpersonal.md,
  p2-5-egocentric.md                hand-written write-ups whose tables were filled in from the analysis JSON. Each
                                    analysis is re-run from its call cache (p2_1_framing.analyse and
                                    p2_1_exploratory.main; p2_2_perspective.analyse; p2_3b_simpletom_lowsev.main
                                    --analyse and pilot_summary; p2_4_interpersonal.analyse; p2_5_egocentric.analyse),
                                    and every table in the write-up is rebuilt from the regenerated numbers with the
                                    write-up's own labels and rounding, then compared line for line. Two table cells
                                    are not in any JSON and are recomputed here from the cache: P2-2's median of
                                    (3f - i) over the 49 templates, and the per-step call counts and distinct request
                                    IDs in the run records of P2-3b and P2-5. The prose is not compared; the
                                    analysis JSON it quotes from is checked number by number.
  p2-3-simpletom.md                 a stopped run (26 calls before a refusal). Its one table (planned and made calls
                                    per step) is rebuilt from p2_3_simpletom.jobs() over data/p2-3-items.json, the
                                    26-call cache and the refused job named in refusal-p2-3.md.
  refusal-p2-3.md                   a refusal record, not a table: skipped.

Program 2's code reads program 1 (programs/entangled-mind: exp5_run, bm_runs, gm2_self_conditioning,
bm0_source_distance_lag, entangled_mind and their archives), so those folders are in the snapshot. om_common.py
names program 1 by the absolute path of its old stand-alone checkout (/Users/seanpharris/entangled-mind); this script
points om_common.P1 at the snapshot's programs/entangled-mind instead and removes that absolute path from sys.path,
so nothing outside the snapshot can be read. The run logs (results/*.log) are not tables and are not listed.

Nothing here needs a file the archive lacks: there are no gaps."""
import importlib
import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # programs/
import repro_common as R  # noqa: E402

P1_OLD = Path("/Users/seanpharris/entangled-mind")              # om_common.P1 as committed (the old checkout)
P1_REPO = "programs/entangled-mind"
TOL = 1e-9
MINUS = "−"


# ----- formatting, as the write-ups round -----------------------------------------------------------------------

def n(x, dp, sign=False):
    """x to dp decimals; '+' on non-negatives if sign; the write-ups' Unicode minus."""
    return (f"{x:+.{dp}f}" if sign else f"{x:.{dp}f}").replace("-", MINUS)


def nci(v, dp, sign=False):
    """[point, lo, hi] as 'point [lo, hi]'."""
    return f"{n(v[0], dp, sign)} [{n(v[1], dp, sign)}, {n(v[2], dp, sign)}]"


def thou(k):
    return f"{k:,}"


def row(*cells):
    """A markdown table row; an empty cell is written '| |', as in the write-ups."""
    return "|" + "|".join(f" {c} " if c else " " for c in cells) + "|"


def sep(k):
    return "|" + "---|" * k


# ----- JSON comparison ------------------------------------------------------------------------------------------

def json_diff(a, b, path=""):
    """First difference between two parsed JSON values, as (path, committed, regenerated), or None.
    Numbers are equal within a relative TOL; NaN equals NaN; key order does not matter."""
    if isinstance(a, dict) and isinstance(b, dict):
        if set(a) != set(b):
            return path or "/", f"keys {sorted(set(a) - set(b))[:4]}", f"keys {sorted(set(b) - set(a))[:4]}"
        for k in a:
            d = json_diff(a[k], b[k], f"{path}/{k}")
            if d:
                return d
        return None
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return path, f"length {len(a)}", f"length {len(b)}"
        for i, (x, y) in enumerate(zip(a, b)):
            d = json_diff(x, y, f"{path}/{i}")
            if d:
                return d
        return None
    num = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool)
    if num(a) and num(b):
        na, nb = isinstance(a, float) and math.isnan(a), isinstance(b, float) and math.isnan(b)
        if na or nb:
            return None if na and nb else (path, repr(a), repr(b))
        return None if abs(a - b) <= TOL * max(1.0, abs(a), abs(b)) else (path, repr(a), repr(b))
    return None if a == b else (path, repr(a)[:80], repr(b)[:80])


class Checker:
    """One row per results .md: its tables (and, as an extra, the JSON its analysis regenerated)."""

    def __init__(self, rep, root, committed):
        self.rep, self.root, self.committed = rep, root, committed

    def tables(self, name, tables, jsons=(), whole=None):
        """name: results/x.md. tables: regenerated tables (lists of lines) that must appear in the committed file.
        jsons: results/y.json files the analysis rewrote in the snapshot, checked against the committed copies.
        whole: a regenerated text to compare byte for byte instead of tables."""
        text = self.committed[name]
        have = R.tables_of(text)
        bad_table = whole is not None and whole != text or whole is None and any(t not in have for t in tables)
        if not bad_table:
            for j in jsons:
                d = json_diff(json.loads(self.committed[j]), json.loads((self.root / j).read_text()))
                if d:
                    path, a, b = d
                    self.rep.compare(name, [f"{j}{path}: {a}"], [f"{j}{path}: {b}"], what=f"regenerated {j}")
                    return
        if whole is not None:
            self.rep.compare(name, text, whole)
        else:
            self.rep.compare_tables(name, text, tables)


# ----- the snapshot's modules -----------------------------------------------------------------------------------

def load_modules(tmp, root):
    """Import program 2's experiment modules from the snapshot, with program 1 (also from the snapshot) under them."""
    p1 = tmp / P1_REPO
    sys.path[:0] = [str(root / "experiments"), str(p1 / "src"), str(p1 / "experiments")]
    # Program 1 first, from the snapshot, so om_common's own sys.path insert of the old checkout finds them loaded.
    p1_mods = {m: importlib.import_module(m) for m in ("entangled_mind.config", "gm_common", "exp5_run", "bm_runs",
                                                         "gm2_self_conditioning", "bm0_source_distance_lag")}
    om = importlib.import_module("om_common")
    sys.path[:] = [p for p in sys.path if not (p == str(P1_OLD) or p.startswith(str(P1_OLD) + "/"))]
    om.P1 = p1                                   # harness path fix: program 1 lives at programs/entangled-mind here
    mods = {"om": om}
    for m in ("p2_1_framing", "p2_1_exploratory", "p2_2_perspective", "p2_3_simpletom", "p2_3b_simpletom_lowsev",
              "p2_4_interpersonal", "p2_5_egocentric", "p2_6_position_label", "p2_6r_replication",
              "p2_7_format_fingerprint"):
        mods[m] = importlib.import_module(m)
    for name, mod in list(sys.modules.items()):  # nothing of either program may come from outside the snapshot
        f = getattr(mod, "__file__", None) or ""
        if f.startswith(str(P1_OLD) + "/") or (f.startswith(str(R.ENGINE / "programs"))
                                                and name not in ("__main__", "repro_common")):
            raise RuntimeError(f"module {name} was imported from outside the snapshot: {f}")
    inside = (tmp, tmp.resolve())                # macOS: /var/folders is /private/var/folders once resolved
    for name, mod in {**p1_mods, **mods}.items():  # and every file path a module holds points into the snapshot
        for attr, v in vars(mod).items():
            if (name, attr) == ("om", "p"):      # om_common's loop variable over the sys.path entries removed above
                continue
            if isinstance(v, Path) and v.is_absolute() and not any(v.is_relative_to(t) for t in inside):
                raise RuntimeError(f"{name}.{attr} = {v} points outside the snapshot")
    return mods


def run_main(mod, *args):
    """Call a module's main() with sys.argv as its own command line would set it."""
    old = sys.argv
    sys.argv = [Path(mod.__file__).name, *args]
    try:
        return mod.main()
    except SystemExit as e:                      # a script's own stop (sys.exit) is a failure of this table
        raise RuntimeError(f"{Path(mod.__file__).name} exited: {e}") from None
    finally:
        sys.argv = old


# ----- per-file table builders (labels and rounding as in the committed write-ups) ------------------------------

def p2_1_tables(fr, ex):
    F = fr["framings"]
    words = {"a": "how likely is it that this statement is true (program 1)", "b": "how confident are you",
             "c": "another AI assistant who read exactly this", "d": "Sam, a person who read exactly this",
             "p1F1": "program 1's gm3b F1, archived (same wording as a)"}
    t1 = [row("framing", "wording", "mean", "mean \\|m − 50\\|", "within-claim SD", "split-half reliability ρ"),
          sep(6)]
    for f in ("a", "b", "c", "d", "p1F1"):
        x = F[f]
        t1.append(row("p1" if f == "p1F1" else f, words[f], n(x["mean"], 1), n(x["extremity_mean_abs_minus_50"], 1),
                      n(x["within_claim_sd"], 2), n(x["split_half_reliability"], 3)))
    t2 = [row("pair", "Q", "shift (points)", "r"), sep(4)]
    names = {"a-b": "a – b (primary)", "a-c": "a – c", "a-d": "a – d", "b-c": "b – c",
             "b-d": "b – d (secondary)", "c-d": "c – d", "a-p1F1": "a – p1 (test–retest)"}
    for k in ("a-b", "a-c", "a-d", "b-c", "b-d", "c-d", "a-p1F1"):
        p = fr["pairs"][k]
        cells = [names[k], nci([p["Q"], *p["Q_ci"]], 3), nci([p["shift_b_minus_a"], *p["shift_ci"]], 2, True)]
        if k == "a-b":
            cells = [f"**{c}**" for c in cells]
        t2.append(row(*cells, n(p["r"], 3)))
    t3 = [row("a", "b", "claim"), sep(3)]
    for x in ex["largest_diffs"][:6]:
        t3.append(row(str(x["a"]), str(x["b"]), x["claim"]))
    return [t1, t2, t3]


def p2_2_tables(o, median_3f_i):
    t1 = [row("", "n", "Q(i, ii)", "ρ_i", "ρ_ii", "mean (i)", "mean (ii)", "shift ii − i"), sep(8)]
    p = o["primary"]
    t1.append(row("**pooled (primary)**", str(p["n_items"]), f"**{nci([p['Q'], *p['Q_ci']], 3)}**", n(p["rel_i"], 3),
                  n(p["rel_ii"], 3), "", "", ""))
    for cond, lab in (("TB", "true belief (TB)"), ("FB", "false belief (FB)")):
        w = o[f"within_{cond}"]
        t1.append(row(lab, str(o["rewrites_ok"]), nci([w["Q"], *w["Q_ci"]], 3), n(w["rel_i"], 3), n(w["rel_ii"], 3),
                      n(w["mean_i"], 1), n(w["mean_ii"], 1), nci([w["shift_ii_minus_i"], *w["shift_ci"]], 1, True)))
    m = o["two_by_two_means"]
    t2 = [row("", "full story", "filtered story"), sep(3),
          row("third person, \"how likely is it that Noor believes X\"", f"i: {n(m['i|FB'], 1)}", f"3f: {n(m['3f|FB'], 1)}"),
          row("second person, \"how likely is it that X\"", f"2u: {n(m['2u|FB'], 1)}", f"ii: {n(m['ii|FB'], 1)}")]
    t3 = [row("effect", "points [95% CI]"), sep(2),
          row("filtering, third person (3f − i), consistent with a curse of knowledge (secondary)",
              f"{nci(o['filter_effect_3rd_FB'], 1, True)}; median {n(median_3f_i, 1, True)}"),
          row("filtering, second person (ii − 2u)", nci(o["filter_effect_2nd_FB"], 1, True)),
          row("person and question, filtered (ii − 3f)", nci(o["person_effect_filtered_FB"], 1, True)),
          row("person and question, full (2u − i)", nci(o["person_effect_full_FB"], 1, True))]
    t4 = [row("rendering", "TB", "FB"), sep(3)]
    for cell, lab in (("i", "(i) third person, belief"), ("ii", "(ii) second person, filtered, world")):
        t4.append(row(lab, nci(o[f"order_effect_{cell}_TB"], 1, True), nci(o[f"order_effect_{cell}_FB"], 1, True)))
    return [t1, t2, t3, t4]


def p2_2_median_3f_minus_i(mod):
    """Median over the 2 x 2 subset's templates of mean(3f) - mean(i), FB (a write-up cell not in the JSON),
    from the call cache, with the analysis's own subset, rewrite check and clipping."""
    import numpy as np
    items = json.loads(mod.ITEMS.read_text())
    cache = json.loads(mod.CACHE.read_text())
    sp = {int(k): v for k, v in json.loads(mod.REWRITE.read_text()).items()}
    ok = {t for t in sp if mod.rewrite_ok(items[t], sp[t])}
    S = [t for t in mod.subset(items) if t in ok]

    def mean(t, cell):
        return np.mean([min(100, max(0, cache[f"{t}|FB|{cell}|single|{r}"]["value"])) for r in range(mod.R)])
    return float(np.median([mean(t, "3f") - mean(t, "i") for t in S]))


def p2_3_table(mod, root):
    items = json.loads(mod.ITEMS.read_text())
    cache = json.loads(mod.CACHE.read_text())
    refused = re.search(r"job `([^`]+)`", (root / "results" / "refusal-p2-3.md").read_text())[1]
    J = mod.jobs(items)
    steps = (("1. own awareness answer", lambda j: j[1] == "ms"), ("2. behaviour × 6 conditions",
             lambda j: j[4] == "action"), ("3. judgment × 6 conditions", lambda j: j[4] == "judge"))
    t = [row("step", "planned calls", "made", "status"), sep(4)]
    for lab, sel in steps:
        keys = [j[0] for j in J if sel(j)]
        made = sum(k in cache for k in keys)
        if refused in keys:
            status = f"stopped at `{refused.replace('|', chr(92) + '|')}` (refused)"
        else:
            status = "not run" if made == 0 else "complete" if made == len(keys) else "partial"
        t.append(row(lab, thou(len(keys)), thou(made), status))
    return [t]


def p2_3b_tables(o, mod, cache, ordered, pilot):
    rate, acc, st = o["aware_answer_rate"], o["accuracy"], o["stats"]
    names = {"c1_not_asked": "c1 not asked", "c2_filler": "c2 filler", "c3_redacted": "c3 redacted",
             "c4_remind_own": "c4 remind, own", "c5_planted_own": "c5 planted own",
             "c6_planted_other": "c6 planted other"}
    t1 = [row("condition", "behaviour y", "behaviour accuracy", "judgment y", "judgment accuracy"), sep(5)]
    for c in mod.CONDS:
        t1.append(row(names[c], n(rate[f"action|{c}"], 3), n(acc[f"action|{c}"], 3), n(rate[f"judge|{c}"], 3),
                      n(acc[f"judge|{c}"], 3)))
    s3 = lambda k: (n(st[k][0], 3, True), f"[{n(st[k][1], 3, True)}, {n(st[k][2], 3, True)}]")
    s2 = lambda k: (n(st[k][0], 2), f"[{n(st[k][1], 2)}, {n(st[k][2], 2)}]")
    # stories with both planted conditions answered, by severity (the counts in the severity row)
    Y = mod.responses(ordered, cache)
    comp = [i for i in range(len(ordered)) if not math.isnan(Y[("action", "c5_planted_own")][i])
            and not math.isnan(Y[("action", "c6_planted_other")][i])]
    sev = {s: sum(ordered[i]["severity"] == s for i in comp) for s in (1, 2)}
    d1, d2 = s3("delta_sev1"), s3("delta_sev2")
    op, ot = s3("own_pull_judge"), s3("other_pull_judge")
    t2 = [row("statistic", "value", "95% CI"), sep(3),
          row("**Δ = y(c5) − y(c6), behaviour (primary)**", *(f"**{x}**" for x in s3("delta"))),
          row(f"Δ_match ({o['complete_match']} stories, planted letter = aware option's letter)", *s3("delta_match")),
          row(f"Δ_mismatch ({o['complete_primary'] - o['complete_match']} stories)", *s3("delta_mismatch")),
          row("letter-copy baseline's Δ (what a pure letter-copier would show against this c6)",
              *s3("delta_letter_copy_baseline")),
          row(f"Δ, severity 1 ({sev[1]}) / severity 2 ({sev[2]})", f"{d1[0]} / {d2[0]}", f"{d1[1]} / {d2[1]}"),
          row("own pull, behaviour (y₅ − y₃)", *s3("own_pull_action")),
          row("other pull, behaviour (y₆ − y₃)", *s3("other_pull_action")),
          row("R_MS, behaviour", *s2("R_MS_action")),
          row("Δ, judgment (secondary)", *s3("delta_judge")),
          row("own pull / other pull, judgment", f"{op[0]} / {ot[0]}", f"{op[1]} / {ot[1]}"),
          row("R_MS, judgment", *s2("R_MS_judge")),
          row("awareness-question accuracy", n(o["ms_accuracy"], 3), "—")]
    y6 = rate["action|c6_planted_other"]
    v, why = o["primary_verdict"], o["verdict_reason"]
    testable = v != "untestable"
    met = st["delta"][0] >= 0.10 - mod.EPS and st["delta"][1] > 0
    lo = o["loo_core"]
    flips = len(lo["label_flips"])
    t3 = [row("step", "condition", "result"), sep(3),
          row("untestable?", f"complete < {mod.MIN_COMPLETE}; y(c6) > {mod.CEILING:.2f}",
              f"{o['complete_primary']} complete; y(c6) = {n(y6, 3)}: {'testable' if testable else 'untestable'}"),
          row("Δ ≥ 0.10 and CI lower > 0", f"{n(st['delta'][0], 3)}, lower {n(st['delta'][1], 3)}",
              "met" if met else "not met"),
          row("letter guards", "not reached" if not met else "reached", "—"),
          row("**verdict**", "", f"**{v} (\"{why}\")**"),
          row("om-p2-3's rule on these data (reported beside, never in place)", "Δ ≥ 0.10 and CI lower > 0",
              o["verdict_under_om_p2_3_rule"]),
          row(f"leave one core scenario out ({o['cores']})", "Δ range; the full rule re-applied",
              f"{n(lo['delta_range'][0], 3)} to {n(lo['delta_range'][1], 3)}; {flips} label flips "
              f"({'fragile' if lo['fragile'] else 'not fragile'})")]
    kinds = {k: sum(1 for key in cache if key.split("|")[0] == k) for k in ("ms", "action", "judge")}
    rids = [v["request_id"] for v in cache.values()]
    refusals = sum(1 for v in cache.values() if v.get("refused"))
    tot = o["cost_usd"] + pilot["cost_usd"]
    t4 = [row("", ""), sep(2),
          row("calls", f"{thou(o['calls'])} = {kinds['ms']} awareness + {thou(kinds['action'])} behaviour + "
                       f"{thou(kinds['judge'])} judgment" + (", each with a unique request ID"
                                                             if len(set(rids)) == len(rids) else "")),
          row("refusals / stops", f"{refusals} / " + ("none (no `results/refusal.md`, no stop record)"
                                                      if o["stop"] is None else "stopped")),
          row("cache content check", "every entry's SHA-256 of model, max_tokens and messages verified at analysis "
                                     "(D9 F4)"),
          row("spend", f"test ${o['cost_usd']:.4f} (cap ${mod.CAP:.2f}); pilot ${pilot['cost_usd']:.4f} "
                       f"(cap ${mod.PILOT_CAP:.2f}); total ${tot:.3f}"),
          row("archive", "`results/p2-3b-calls.json`, `results/p2-3b-simpletom-lowsev.json`; pilot "
                         "`results/p2-3b-pilot.json`, `results/p2-3b-pilot-calls.json`, `results/p2-3b-pilot.md`")]
    return [t1, t2, t3, t4]


def p2_3b_pilot_tables(p):
    return [[row("", ""), sep(2),
             row("stories", str(p["pilot_stories"])),
             row("calls planned / made", f"{p['planned_calls']} / {p['made']}"),
             row("refusals", str(p["refusals"])),
             row("cost", f"${p['cost_usd']:.5f}"),
             row("record", "`results/p2-3b-pilot.json`, cache `results/p2-3b-pilot-calls.json`")]]


def p2_4_tables(o, mod):
    E = o["effects"]
    labels = {"u_own_10": "u own, 10", "u_own_30": "u own, 30", "u_own_60": "u own, 60", "u_other_10": "u other, 10",
              "u_other_30": "u other, 30", "u_other_60": "u other, 60", "OE": "OE (order)", "RA_shown": "RA shown",
              "RA_redacted": "RA redacted", "RA_high": "RA planted high", "RA_low": "RA planted low"}
    t1 = [row("effect", "measured", "(a) self", "(b) Sam", "(c) one-line observer", "always-50"), sep(6)]
    for k in mod.EFFECTS:
        t1.append(row(labels[k], *(n(E[s][k], 3) for s in ("measured", "a", "b", "c", "n50"))))
    yes = lambda b: "yes" if b else "no"
    rw = o["r_with_measured"]
    mae = lambda s: nci([o["mae"][s], *o["mae_ci"][s]], 3)
    t2 = [row("statistic", "value", "rule", "met"), sep(4),
          row("gate: r(arm − n50, measured − n50)", f"(a) {nci(rw['a'], 3)}; (b) {nci(rw['b'], 3)}",
              "one arm's CI above 0", yes(o["gate_above_chance"])),
          row("MAE (a)", mae("a"), "", ""),
          row("MAE (b)", mae("b"), "", ""),
          row("**ΔMAE = (a) − (b)**", f"**{nci(o['dmae_a_minus_b'], 3, True)}**", "CI not wholly below 0",
              yes(o["part1_a_not_better"])),
          row("**r(a, b)** on departures from n50", f"**{nci([o['r_ab_effects'], *o['r_ab_ci']], 3)}**",
              "≥ 0.70", yes(o["part2_r_ab_ge_0_7"]))]
    C = o["contrasts"]
    three = lambda k, f: "; ".join(f(C[s][k]) for s in ("measured", "a", "b"))
    t3 = [row("statistic", "value"), sep(2),
          row("MAE (c), one-line observer", mae("c")),
          row("ΔMAE (a) − (c); (b) − (c)",
              f"{nci(o['dmae_a_minus_c'], 3, True)}; {nci(o['dmae_b_minus_c'], 3, True)}"),
          row("MAE always-50", mae("n50")),
          row("r(c − n50, measured − n50)", nci(rw["c"], 3)),
          row("raw r(a, b) on effects", n(o["r_ab_raw_effects"], 3)),
          row("cell-level r(a, b), all prediction cells", n(o["cell_level_r_ab"], 3)),
          row("own − other uptake: measured; (a); (b)", three("own_minus_other", lambda v: nci(v, 3))),
          row("own uptake 10 − 60: measured; (a); (b)", three("own_10_minus_60", lambda v: n(v[0], 3))),
          row("RA shown − redacted: measured; (a); (b)", three("RA_shown_minus_redacted", lambda v: n(v[0], 3)))]
    us = [f"u_{s}_{d}" for s in ("own", "other") for d in (10, 30, 60)]
    cr = o["causal_report"]
    t4 = [row("", "own 10", "own 30", "own 60", "other 10", "other 30", "other 60", "MAE vs measured u",
              "r vs measured u"), sep(9),
          row("measured uptake", *(n(E["measured"][u], 3) for u in us), "", "")]
    for arm, lab in (("a", "(a) self"), ("b", "(b) Sam")):
        t4.append(row(lab, *(n(cr[f"{arm}|{u}"], 3) for u in us), n(o[f"causal_report_mae_{arm}"], 3),
                      n(o[f"causal_report_r_{arm}"], 3)))
    return [t1, t2, t3, t4]


def p2_5_tables(o, mod, cache):
    p, c = o["point"], o["ci"]
    v3 = lambda k: nci([p[k], *c[k]], 3, True)
    nv = o["n_complete_vignettes"]
    E = mod.EPS
    ok = {"1": nv >= mod.MIN_VIGNETTES, "2": c["U_self_own"][0] > E,
          "3": p["U_sam_own"] >= mod.BAR - E and c["U_sam_own"][0] > E,
          "4": p["dU"] >= mod.MARGIN - E and c["dU"][0] > E, "5": c["copy_guard"][0] > E,
          "5b": c["sam_minus_self"][0] > E}
    met = lambda k: "met" if ok[k] else "not met"
    t1 = [row("step", "statistic", "estimate [95% CI]", "condition", "outcome"), sep(5),
          row("1", "complete vignettes", f"{nv} of 16 (k = {o['complete_repeats_k']} repeats)",
              f"≥ {mod.MIN_VIGNETTES}", "testable" if ok["1"] else "untestable"),
          row("2", "U_self(OWN), the model's own re-rating", v3("U_self_own"), "CI lower > 0",
              "manipulation took" if ok["2"] else "untestable"),
          row("3", "U_sam(OWN), Sam (person, uninformed)", v3("U_sam_own"), "≥ 0.10 and CI lower > 0", met("3")),
          row("4", "ΔU = U_sam(OWN) − U_sam(SWAP)", v3("dU"), "≥ 0.05 and CI lower > 0", met("4")),
          row("5", "G = U_inf(OWN) − U_sam(OWN), copy guard", v3("copy_guard"), "CI lower > 0", met("5")),
          row("5b", "U_sam(OWN) − U_self(OWN)", v3("sam_minus_self"), "fail if CI lower > 0",
              "**fail (not inherited)**" if ok["5b"] else "met")]
    t2 = [row("statistic", "estimate [95% CI]"), sep(2)]
    for k, lab in (("U_self_own", "U_self(OWN)"),
                   ("U_self_swap", "U_self(SWAP): Alex's number on the model's own re-rating"),
                   ("U_sam_own", "U_sam(OWN)"), ("U_sam_swap", "U_sam(SWAP)"),
                   ("U_inst_own", "U_inst(OWN): Sam as \"another instance of you\""), ("U_inst_swap", "U_inst(SWAP)"),
                   ("dU_inst", "ΔU_inst"), ("inst_minus_person_own", "instance minus person, OWN"),
                   ("U_inf_own", "U_inf(OWN): Sam has seen the model's answer"), ("U_inf_swap", "U_inf(SWAP)")):
        t2.append(row(lab, v3(k)))
    t2.append(row("leakage ratio U_sam(OWN) / U_self(OWN)", nci([p["leak_ratio"], *c["leak_ratio"]], 2)))
    qn = {"self": "self", "sam_p": "Sam, person", "sam_i": "Sam, instance", "sam_inf": "Sam, informed"}
    bc, bb = o["by_class"], o["by_band"]["uptake"]
    lo, hi = (f"{b[0]}–{b[1] - 1}" for b in o["by_band"]["bands"][:2])
    b3 = o["by_band"]["bands"][2]
    t3 = [row("condition", "question", "by nominal \\|d\\|: 10 / 30 / 60",
              f"by real \\|V − m\\|: {lo} / {hi} / {b3[0]}–{b3[1] - 1}"), sep(4)]
    for cond in mod.CONDS:
        for q in mod.QUESTIONS:
            t3.append(row(cond, qn[q], " / ".join(n(bc[f"{cond}|{q}|{k}"], 3) for k in mod.CLASSES),
                          " / ".join(n(bb[f"{cond}|{q}|{k}"], 3) for k in mod.CLASSES)))
    loo = o["loo"]
    same = sum((x["label"], x["reason"]) == (o["label"], o["reason"]) for x in loo)
    lab = f"{o['label']} ({o['reason'].replace('_', ' ')})" if o["reason"] else o["label"]
    rng = lambda k: f"{min(x[k] for x in loo):.3f}–{max(x[k] for x in loo):.3f}"
    dd = o["dedup"]
    dp, dc = dd["point"], dd["ci"]
    dl, dr = dd["rule_would_give"]
    t4 = [row("check", "result"), sep(2),
          row(f"leave-one-vignette-out, full rule re-applied ({len(loo)} refits)",
              f"{same} of {len(loo)} {lab}; U_sam(OWN) {rng('U_sam_own')}; ΔU {rng('dU')}; "
              + ("no flips" if not o["loo_flips"] else f"{len(o['loo_flips'])} flips")),
          row("each distinct prompt counted once (`dedup`)",
              f"U_sam(OWN) {dp['U_sam_own']:.3f}, U_self(OWN) {dp['U_self_own']:.3f}, ΔU {dp['dU']:.3f}, "
              f"G {dp['copy_guard']:.3f}, Sam minus own {dp['sam_minus_self']:.3f} "
              f"[{dc['sam_minus_self'][0]:.3f}, {dc['sam_minus_self'][1]:.3f}]: "
              + (f"{dl} ({dr.replace('_', ' ')})" if dr else dl)),
          row("REF self re-rating minus archived anchor m", f"{n(o['anchor_vs_ref_self'], 2, True)} points on average"),
          row(f"median within-cell SD over {o['complete_repeats_k']} repeats", f"{o['within_cell_sd_median']:g} points")]
    rids = {v["request_id"] for v in cache.values() if not v.get("refused")}
    t5 = [row("item", "value"), sep(2),
          row("calls", f"{thou(o['planned_calls'])} planned, {thou(o['calls'])} made, {thou(len(rids))} distinct "
                       "request IDs"),
          row("cost", f"${o['cost_usd']:.6f} (cap ${mod.CAP:.2f}, enforced in code)"),
          row("refusals", f"{o['refused']} (no `results/refusal.md` from this run)"),
          row("out-of-range values", str(o["out_of_range"])),
          row("complete repeats k", str(o["complete_repeats_k"])),
          row("cache content check", "every entry's SHA-256 matches its prompt (asserted at analysis)")]
    return [t1, t2, t3, t4, t5]


# ----- main -----------------------------------------------------------------------------------------------------

def main():
    tmp = R.snapshot(["programs/other-minds", f"{P1_REPO}/src", f"{P1_REPO}/experiments", f"{P1_REPO}/results"])
    try:
        root = tmp / "programs/other-minds"
        rep = R.Report("other-minds", root, results_globs=("results/*.md",))
        committed = {p.relative_to(root).as_posix(): p.read_text() for p in (root / "results").iterdir()
                     if p.suffix in (".md", ".json") and not p.name.endswith("-calls.json")}
        ck = Checker(rep, root, committed)
        print("other-minds: rebuilding the results tables from the archived JSON (no API, no network)")
        rep.skip("results/refusal-p2-3.md", "refusal record of the stopped P2-3 run, not a table")
        mods = rep.run("results/p2-1-framing.md", lambda: load_modules(tmp, root))
        if mods is None:
            for name in rep.expected:
                if name not in rep.seen:
                    rep.error(name, RuntimeError("not rebuilt: the experiment modules did not import (see above)"))
            return rep.finish()
        res = root / "results"
        load = lambda f: json.loads((res / f).read_text())

        # P2-1: analysis and exploratory analysis from p2-1-calls.json (+ program 1's gm3b-calls.json for the retest)
        name = "results/p2-1-framing.md"

        def p21():
            mods["p2_1_framing"].analyse()
            mods["p2_1_exploratory"].main()
            return p2_1_tables(load("p2-1-framing.json"), load("p2-1-exploratory.json"))
        t = rep.run(name, p21)
        if t is not None:
            ck.tables(name, t, ["results/p2-1-framing.json", "results/p2-1-exploratory.json"])

        # P2-2: from p2-2-calls.json, data/p2-2-items.json and data/p2-2-second-person.json
        name = "results/p2-2-perspective.md"

        def p22():
            m = mods["p2_2_perspective"]
            m.analyse()
            return p2_2_tables(load("p2-2-perspective.json"), p2_2_median_3f_minus_i(m))
        t = rep.run(name, p22)
        if t is not None:
            ck.tables(name, t, ["results/p2-2-perspective.json"])

        # P2-3: the stopped run's step table (no analysis JSON was written: the run never reached the conditions)
        name = "results/p2-3-simpletom.md"
        t = rep.run(name, lambda: p2_3_table(mods["p2_3_simpletom"], root))
        if t is not None:
            ck.tables(name, t)

        # P2-3b: the pilot summary from p2-3b-pilot-calls.json, then the test analysis from p2-3b-calls.json
        m3b = mods["p2_3b_simpletom_lowsev"]
        name = "results/p2-3b-pilot.md"

        def pilot():
            items = json.loads(m3b.ITEMS.read_text())
            _, pil = m3b.split(items)
            pil = sorted(pil, key=lambda it: it["id"])               # as main() orders the pilot
            s = m3b.pilot_summary(pil, json.loads(m3b.PILOT_CACHE.read_text()))
            m3b.PILOT_OUT.write_text(json.dumps(s, indent=1))           # as main() writes it (into the snapshot)
            return p2_3b_pilot_tables(s)
        t = rep.run(name, pilot)
        if t is not None:
            ck.tables(name, t, ["results/p2-3b-pilot.json"])
        name = "results/p2-3b-simpletom-lowsev.md"

        def p23b():
            run_main(m3b, "--analyse")
            items = json.loads(m3b.ITEMS.read_text())
            test, _ = m3b.split(items)
            ordered = m3b.run_order(test, json.loads(m3b.SEEDF.read_text())["seed32_order"])
            return p2_3b_tables(load("p2-3b-simpletom-lowsev.json"), m3b, json.loads(m3b.CACHE.read_text()), ordered,
                                load("p2-3b-pilot.json"))
        t = rep.run(name, p23b)
        if t is not None:
            ck.tables(name, t, ["results/p2-3b-simpletom-lowsev.json"])

        # P2-4: from p2-4-calls.json and program 1's bm0/bm1/exp4-run-3/gm2/gm2b archives
        name = "results/p2-4-interpersonal.md"

        def p24():
            mods["p2_4_interpersonal"].analyse()
            return p2_4_tables(load("p2-4-interpersonal.json"), mods["p2_4_interpersonal"])
        t = rep.run(name, p24)
        if t is not None:
            ck.tables(name, t, ["results/p2-4-interpersonal.json"])

        # P2-5: from p2-5-calls.json and program 1's exp4 items and anchors
        name = "results/p2-5-egocentric.md"

        def p25():
            m = mods["p2_5_egocentric"]
            run_main(m, "--analyse")
            return p2_5_tables(load("p2-5-egocentric.json"), m, json.loads(m.CACHE.read_text()))
        t = rep.run(name, p25)
        if t is not None:
            ck.tables(name, t, ["results/p2-5-egocentric.json"])

        # P2-6 then P2-6r (P2-6r's Haiku column reads the P2-6 JSON just regenerated): write_md() output compared
        # byte for byte; the write-ups must contain every generated table.
        for mod, tables_md, writeup, js in (
                ("p2_6_position_label", "results/p2-6-tables.md", "results/p2-6-position-or-label.md",
                 "results/p2-6-position-or-label.json"),
                ("p2_6r_replication", "results/p2-6r-tables.md", "results/p2-6r-replication.md",
                 "results/p2-6r-replication.json"),
                ("p2_7_format_fingerprint", "results/p2-7-tables.md", "results/p2-7-format-fingerprint.md",
                 "results/p2-7-format-fingerprint.json")):
            ok = rep.run(tables_md, lambda mod=mod: run_main(mods[mod], "--analyse") or True)
            if ok is None:
                rep.error(writeup, RuntimeError(f"not compared: {tables_md} could not be regenerated (see above)"))
                continue
            new = (root / tables_md).read_text()
            ck.tables(tables_md, None, [js], whole=new)
            ck.tables(writeup, R.tables_of(new))
        return rep.finish()
    finally:
        R.cleanup(tmp)


if __name__ == "__main__":
    R.main_guard(main)
