#!/usr/bin/env python3
"""Program 5 (self-grading): rebuild every results table and analysis from the archived call caches, and check them.

    python3 programs/self-grading/reproduce.py        # from the repo root; stdlib and numpy only, no keys, no network

In plain English: each bet's script (experiments/sg_b1_placement.py, sg_b2_label.py, sg_b3_flaw.py) has an `analyse`
step that makes no calls. It reads the cached model answers (results/<bet>-write-calls*.json, <bet>-grade-calls*.json)
and writes results/<bet>-analysis*.json: the per-model differences, bootstrap intervals, readings and verdict. This
script runs that same step on a copy of the program taken at git HEAD, with keys removed, the network blocked and
every package except numpy stubbed out, and compares what it writes with the committed file, byte for byte.

The write-ups (results/sg-b1-placement.md, sg-b2-label.md, sg-b3-flaw.md) were written by hand from those analyses.
For each one, every table is rebuilt from the regenerated analysis (not from the committed JSON) and from the call
caches (call counts, spend), with the write-up's labels, rounding, signs (the Unicode minus) and bold, and compared
line for line with the committed table. Every number is recomputed, including the n in a row label ("randomised
(n 23)"). Descriptive cells (column headers, row labels without a number) are copied from the committed table and
counted; model names and readings are rebuilt. The number of tables in each file is checked too, so a table added
later fails until it is taught here. A list of in-text numbers that the plain-English part copies from the analysis
or the caches (calls, spend, pooled estimates, tie counts, gate values, verdict) is checked the same way.
A number that is an exact decimal tie at the printed precision (63.05 = 3783/60, to one place) matches either
rounding: Python rounds the binary float down (63.0), the write-ups round such ties either way (sg-b3: 63.05 as 63.1,
8.85 as 8.9, but 89.85 as 89.8). Each such cell is counted in the output (two today, both in sg-b3-flaw.md).
Not checked, because no archived code computes them: the logit-scale gaps in sg-b3-flaw.md (0.97, 1.19), the
audit's domain bootstrap quoted there, and sg-b1's own − fresh2 interval (−1.0 [−1.6, −0.4]; its seed is not stated).

Registered files (every one must be accounted for, or the run fails):
  results/*-analysis.json         rebuilt by the bet's own analyse() and compared byte for byte
  results/*-analysis-pilot.json   the same, byte for byte, except a pilot listed in PREDATES: it was written before
                                  later design-review fixes added fields, so every field it has is compared exactly
                                  (serialised in its own order, byte for byte) and the added fields are counted and
                                  named, not compared. A field present in both that differs is still a mismatch.
  results/*.md                    the three write-ups above, every table rebuilt
The call caches and run logs are the inputs, not outputs, so they are not compared.
"""
import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # programs/
import repro_common as R  # noqa: E402

PROGRAM = "self-grading"
BETS = {"sg-b1": "sg_b1_placement", "sg-b2": "sg_b2_label", "sg-b3": "sg_b3_flaw"}
# Follow-ups of sg-b3 (2026-11-05): their write-ups' tables are printed by each script's tables(); every table is
# regenerated from the regenerated analysis and compared line for line, plus the verdict and spend in the prose.
FOLLOWUPS = {"sg-b4": ("sg_b4_quoted", "results/sg-b4-quoted.md"), "sg-b5": ("sg_b5_length", "results/sg-b5-length.md")}
BETS.update({k: v[0] for k, v in FOLLOWUPS.items()})
WRITEUPS = {"sg-b1": "results/sg-b1-placement.md", "sg-b2": "results/sg-b2-label.md", "sg-b3": "results/sg-b3-flaw.md"}
MODELS = ("haiku", "sonnet", "opus")
FULL = {"haiku": "claude-haiku-5-5", "sonnet": "claude-sonnet-5-5", "opus": "claude-opus-5-5"}

# Pilot analyses committed before a later code change added fields (see the docstring).
PREDATES = {"results/sg-b3-analysis-pilot.json":
            "committed with the design review (bfea579), before D9a-D9g (b8d6ee3, 37d81f8) added fields"}

# The program's spend as each write-up states it: every cache that existed when it was written (git order).
SPENT_AT = {"sg-b1": ["sg-b1-write-calls-pilot", "sg-b1-grade-calls-pilot", "sg-b1-write-calls", "sg-b1-grade-calls"],
            "sg-b2": ["sg-b3-grade-calls-pilot", "sg-b2-grade-calls"],
            "sg-b3": ["sg-b3-grade-calls"]}

MINUS = "−"


# ----- formatting, as the write-ups print numbers ---------------------------------------------------------------

TIES = {}    # printed number -> its other printing, for exact decimal ties; cleared after each table or in-text value


def _num(x, nd, sign):
    """x to nd places. An exact decimal tie (63.05 = 3783/60, to one place) has two faithful printings: Python rounds
    the binary float (63.0), a reader rounds half up (63.1); the write-ups do both (sg-b3: 89.85 printed 89.8, 63.05
    printed 63.1). The other printing is registered in TIES so either matches; every such cell is counted."""
    spec = f"{'+' if sign else ''}.{nd}f"
    out = format(x, spec).replace("-", MINUS)
    sc = x * 10 ** nd
    lo = math.floor(sc)
    if abs((sc - lo) - 0.5) < 1e-7:
        for y in (lo / 10 ** nd, (lo + 1) / 10 ** nd):
            o = format(y, spec).replace("-", MINUS)
            if o != out:
                TIES[out] = o
    return out


def f(x, nd=2):
    return _num(x, nd, False)


def s(x, nd=2):
    return _num(x, nd, True)


def ci(c, nd=2, fmt=None):
    fmt = fmt or s
    return f"[{fmt(c[0], nd)}, {fmt(c[1], nd)}]"


def pct(x):
    return f"{x * 100:.0f}%"


def usd(x):
    return f"${x:.3f}"


def name(m):
    return m.capitalize()


# ----- table rebuilding (the pattern of programs/nature-graded/reproduce.py) ------------------------------------

K = object()     # descriptive cell: copied from the committed table (a header or a label without a number)
NUM = re.compile(r"([\u2212+-]?\d[\d,]*(?:\.\d+)?)")     # numbers inside a cell (split keeps them at odd indices)


def tie(got, committed):
    """True if `committed` is `got` with one or more exact ties printed rounded the other way (see _num)."""
    g, c = NUM.split(got), NUM.split(committed or "")
    return (len(g) == len(c) and g != c
            and all(a == b or (k % 2 and TIES.get(a) == b) for k, (a, b) in enumerate(zip(g, c))))


def split_row(line):
    inner = line.strip()
    inner = inner[1:] if inner.startswith("|") else inner
    inner = inner[:-1] if inner.endswith("|") else inner
    return [c.strip() for c in inner.split("|")]


def join_row(cells):
    return "|" + "|".join(f" {c} " if c != "" else " " for c in cells) + "|"


class Tables:
    """Rebuild a write-up's tables. add() takes the committed table's index and the rebuilt rows (one list of cells per
    row below the header); the header's cells are copied (counted). intext() checks a number in the prose."""

    def __init__(self, text):
        self.text = text
        self.have = R.tables_of(text)
        self.regen, self.inline = [], []
        self.n = {"calc": 0, "kept": 0, "tie": 0}

    def _cell(self, got, committed):
        if got is K:
            self.n["kept"] += 1
            return committed if committed is not None else "<missing in committed table>"
        self.n["calc"] += 1
        bare = committed[2:-2] if committed and committed.startswith("**") and committed.endswith("**") else committed
        if bare == got:                                 # bold is the author's emphasis
            return committed
        if tie(got, bare):
            self.n["tie"] += 1
            return committed
        return got

    def add(self, idx, rows):
        have = self.have[idx] if idx < len(self.have) else []
        cells = [split_row(l) for l in have]
        missing = "<missing in committed table>"

        def build(r, j):
            c = cells[j] if j < len(cells) else []
            return join_row([self._cell(x, c[k] if k < len(c) else None) for k, x in enumerate(r)])

        ind = have[0][:len(have[0]) - len(have[0].lstrip())] if have else ""     # a table inside a list item
        head = ind + build([K] * len(cells[0]), 0) if cells else missing
        lines = [head, have[1] if len(have) > 1 else missing] + [ind + build(r, j + 2) for j, r in enumerate(rows)]
        self.regen.append((idx, lines))
        TIES.clear()

    def intext(self, label, pattern, *expected):
        """`pattern` has one group per expected value; the committed side is what the text holds there."""
        m = re.search(pattern, self.text, flags=re.S)
        got = " | ".join(m.groups()) if m else "<not found in the text>"
        exp = " | ".join(str(e) for e in expected)
        if m and tie(exp, got):
            self.n["tie"] += 1
            exp = got
        self.inline.append((label, got, exp))
        TIES.clear()

    def check(self, rep, name_):
        committed = [f"[{len(self.have)} table(s) in the file]"] + ["\n".join(self.have[i]) if i < len(self.have)
                                                                    else "" for i, _ in self.regen]
        rebuilt = [f"[{len({i for i, _ in self.regen})} table(s) in the file]"] + ["\n".join(l) for _, l in self.regen]
        committed += [f"in text, {lab}: {c}" for lab, c, _ in self.inline]
        rebuilt += [f"in text, {lab}: {e}" for lab, _, e in self.inline]
        what = (f"{len(self.regen)} tables: {self.n['calc']} cells recomputed, {self.n['kept']} descriptive cells "
                f"copied; {len(self.inline)} in-text values"
                + (f"; {self.n['tie']} exact tie(s) printed rounded the other way" if self.n["tie"] else ""))
        rep.compare(name_, "\n\n".join(committed), "\n\n".join(rebuilt), what=what)


# ----- inputs from the caches ------------------------------------------------------------------------------------

def caches(root):
    return {p.stem: json.loads(p.read_text()) for p in sorted((root / "results").glob("*-calls*.json"))}


def spent(cs, names):
    return sum(v["cost"] for n in names for v in cs[n].values())


def program_spent(cs, bet):
    names = []
    for b in BETS:
        names += SPENT_AT[b]
        if b == bet:
            return spent(cs, names)


def refusal(root):
    return "refusal" if (root / "results" / "refusal.md").exists() else "no refusal"


# ----- sg-b1 -------------------------------------------------------------------------------------------------------

def tables_b1(t, a, cs, root):
    pm = a["per_model"]
    t.add(0, [[name(m), s(pm[m]["D"], 1), ci(pm[m]["ci"], 1)] for m in MODELS])
    t.add(1, [[name(m), s(r["D"]), ci(r["ci"]), r["reading"], f(r["mean"]["own"]), f(r["mean"]["fresh"]),
               f(r["mean"]["fresh2"]), f(r["sd_diff"]), pct(r["share_own_higher"]), pct(r["share_tied"]),
               s(r["D0"]), ci(r["D0_ci"]), ci(r["robustness"]["loo_range"])] for m, r in ((m, pm[m]) for m in MODELS)])
    rob = {m: pm[m]["robustness"] for m in MODELS}
    rows = [[K] + [f"{rob[m]['n_ties']} / {s(rob[m]['ties_excluded_mean'])} / {rob[m]['ties_excluded_reading']}"
                   for m in MODELS]]
    for dsg, lab in (("randomised", "randomised studies"), ("before-after", "before-after"),
                     ("self-selected", "self-selected")):
        rows.append([f"D, {lab} (n {same_n(rob, dsg)})"] + [s(rob[m]["by_design"][dsg]["mean"]) for m in MODELS])
    t.add(2, rows)
    sp = a["spend_by_model"]
    t.add(3, [[name(m), usd(sp["write"][FULL[m]]), usd(sp["grade"][FULL[m]])] for m in MODELS]
          + [[K, usd(sum(sp["write"].values())), usd(sum(sp["grade"].values()))]])

    wc, gc = cs["sg-b1-write-calls"], cs["sg-b1-grade-calls"]
    pilot = spent(cs, ["sg-b1-write-calls-pilot", "sg-b1-grade-calls-pilot"])
    t.intext("calls and spend", r"\*\*(\d+ calls \(\d+ writes, \d+ grades\), complete, no refusal, \$[\d.]+)\*\*",
             f"{len(wc) + len(gc)} calls ({len(wc)} writes, {len(gc)} grades), complete, {refusal(root)}, "
             f"{usd(a['spend_usd'])}")
    t.intext("with the pilot", r"With the review's pilot \(\$([\d.]+)\), the bet spent \$([\d.]+)\.",
             usd(pilot)[1:], f"{pilot + a['spend_usd']:.2f}")
    t.intext("ties", r"\((\d+) of (\d+) in all\).*?\*\*Haiku:\*\* (\d+) of (\d+) got.*?\*\*Sonnet:\*\* (\d+) of (\d+)\."
             r".*?\*\*Opus:\*\* (\d+) of (\d+)\.",
             sum(rob[m]["n_ties"] for m in MODELS), sum(pm[m]["n_usable"] for m in MODELS),
             *[x for m in MODELS for x in (rob[m]["n_ties"], pm[m]["n_usable"])])
    t.intext("Opus re-grade gap", r"identical fresh grades \(([^)]+)\)", s(pm["opus"]["D0"]))
    t.intext("Haiku, ties excluded", r"Haiku becomes \"undetermined\" \(([^)]+)\)",
             s(rob["haiku"]["ties_excluded_mean"], 1))
    t.intext("gate D0", r"every model \(Haiku ([^,]+), Sonnet ([^,]+), Opus ([^)]+)\)",
             *[s(pm[m]["D0"]) for m in MODELS])
    t.intext("Opus D0 interval", r"The Opus difference was ([^ ]+ \[[^\]]+\])",
             f"{s(pm['opus']['D0'])} {ci(pm['opus']['D0_ci'])}")
    grades = {m: [v["grade"] for v in gc.values() if v["model"] == FULL[m]] for m in MODELS}
    allg = [x for m in MODELS for x in grades[m]]
    top = {m: pct(sum(x >= 95 for x in grades[m]) / len(grades[m])) for m in MODELS}
    t.intext("ceiling", r"Grades ran (\d+)–(\d+), with (no 100)\. Sonnet gave 95 or 96 to (\d+%) of its grades; "
             r"Haiku and Opus did so for (\d+%) and (\d+%)",
             min(allg), max(allg), "no 100" if max(allg) < 100 else "a 100", top["sonnet"], top["haiku"], top["opus"])
    common(t, a, cs, "sg-b1", "D", "Pooled D")


# ----- sg-b2 -------------------------------------------------------------------------------------------------------

def tables_b2(t, a, cs, root):
    pm = a["per_model"]
    t.add(0, [[name(m), s(pm[m]["L"], 1), ci(pm[m]["ci"], 1)] for m in MODELS])
    t.add(1, [[name(m), s(r["L"]), ci(r["ci"]), r["reading"],
               f"{s(r['self_minus_none'])} {ci(r['self_minus_none_ci'])}",
               f"{s(r['other_minus_none'])} {ci(r['other_minus_none_ci'])}",
               f(r["mean"]["self"]), f(r["mean"]["other"]), f(r["mean"]["none"]), f(r["sd_diff"]),
               pct(r["share_self_higher"]), pct(r["share_tied"]), f"{s(r['D0'])} {ci(r['D0_ci'])}",
               ci(r["robustness"]["loo_range"])] for m, r in ((m, pm[m]) for m in MODELS)])
    rob = {m: pm[m]["robustness"] for m in MODELS}
    rows = [[K] + [f"{rob[m]['n_ties']} / {s(rob[m]['ties_excluded_mean'])} / {rob[m]['ties_excluded_reading']}"
                   for m in MODELS]]
    for dsg in ("randomised", "before-after", "self-selected"):
        rows.append([f"L, {dsg} (n {same_n(rob, dsg)})"] + [s(rob[m]["by_design"][dsg]["mean"]) for m in MODELS])
    t.add(2, rows)
    sp = a["spend_by_model"]
    t.add(3, [[K] + [usd(sp[FULL[m]]) for m in MODELS] + [usd(a["spend_usd"])]])

    gc, b1 = cs["sg-b2-grade-calls"], cs["sg-b1-grade-calls"]
    t.intext("calls and spend", r"\*\*(\d+ calls, complete, no refusal, \$[\d.]+)\*\*",
             f"{len(gc)} calls, complete, {refusal(root)}, {usd(a['spend_usd'])}")
    o = pm["opus"]
    t.intext("Opus, below the bar", r"on the primary statistic too: ([^ ]+ \[[^\]]+\]) against \"another AI model\".*?"
             r"and ([^ ]+ \[[^\]]+\]) against no label",
             f"{s(o['L'])} {ci(o['ci'])}", f"{s(o['self_minus_none'])} {ci(o['self_minus_none_ci'])}")
    t.intext("ties", r"\((\d+) of (\d+); on Sonnet.*?- Haiku: (\d+) of (\d+);.*?- Sonnet: (\d+) of (\d+);"
             r".*?- Opus: (\d+) of (\d+)\.",
             sum(rob[m]["n_ties"] for m in MODELS), sum(pm[m]["n_usable"] for m in MODELS),
             *[x for m in MODELS for x in (rob[m]["n_ties"], pm[m]["n_usable"])])
    none = {(v["model"], v["task"]): v["grade"] for v in gc.values() if v["cond"] == "none"}
    fresh = {(v["model"], v["task"]): v["grade"] for v in b1.values() if v["cond"] == "fresh"}
    same = [sum(none[k] == fresh.get(k) for k in none if k[0] == FULL[m]) for m in MODELS]
    t.intext("identical-prompt ties", r"gave the identical grade about as often: (\d+), (\d+) and (\d+) of (\d+)",
             *same, pm["haiku"]["n_usable"])
    t.intext("gate D0", r"every model \(Haiku ([^,]+), Sonnet ([^,]+), Opus ([^)]+)\)",
             *[s(pm[m]["D0"]) for m in MODELS])
    common(t, a, cs, "sg-b2", "L", "Pooled L")
    t.intext("program spend and sg-b3 pilot", r"The program has spent \$([\d.]+) of \$5\.00, including sg-b3's "
             r"design-review pilot of \$([\d.]+)\.",
             f"{program_spent(cs, 'sg-b2'):.2f}", usd(spent(cs, ["sg-b3-grade-calls-pilot"]))[1:])


# ----- sg-b3 -------------------------------------------------------------------------------------------------------

def tables_b3(t, a, cs, root):
    pm = a["per_model"]
    t.add(0, [[name(m), f(pm[m]["P_fresh"], 0), f(pm[m]["P_own"], 0), f(pm[m]["G"], 1), ci(pm[m]["ci"], 1, f)]
              for m in ("haiku", "opus", "sonnet")])

    def reading(r):
        if r["note"]:
            return f"{r['reading']} ({r['note'].replace(' (', '; ').rstrip(')')})"
        return r["reading"]

    t.add(1, [[name(m), s(r["G"]), ci(r["ci"]), reading(r), f"{f(r['P_fresh'], 1)} {ci(r['P_fresh_ci'], 1, f)}",
               f"{f(r['P_own'], 1)} {ci(r['P_own_ci'], 1, f)}", f(r["mean"]["own-clean"], 1),
               f(r["mean"]["own-flawed"], 1), f(r["mean"]["fresh-clean"], 1), f(r["mean"]["fresh-flawed"], 1),
               f"{s(r['flawed_D'])} {ci(r['flawed_D_ci'])}", f"{s(r['clean_D'])} {ci(r['clean_D_ci'])}",
               f(r["sd_G"], 1), ci(r["robustness"]["loo_range"], 2, f), "yes" if r["at_floor"] else "no"]
              for m, r in ((m, pm[m]) for m in MODELS)])
    rob = {m: pm[m]["robustness"] for m in MODELS}
    sec = {m: pm[m]["secondaries"] for m in MODELS}
    rows = [[f"G, {dsg} (n {same_n(rob, dsg)})"] + [f(rob[m]["by_design"][dsg]["mean"], 1) for m in MODELS]
            for dsg in ("randomised", "before-after", "self-selected")]

    def sn(key):
        ns = {sec[m][key]["n"] for m in MODELS}
        return ns.pop() if len(ns) == 1 else "differs by model"

    def g1(x):
        return "—" if x is None else f(x, 1)

    rows.append([f"G, study interval excludes 0 (n {sn('G_ci_excludes_0_True')}) / includes 0 "
                 f"(n {sn('G_ci_excludes_0_False')})"]
                + [f"{g1(sec[m]['G_ci_excludes_0_True']['mean'])} / {g1(sec[m]['G_ci_excludes_0_False']['mean'])}"
                   for m in MODELS])
    rows.append([K] + [f"{g1(sec[m]['G_over3_True']['mean'])} ({sec[m]['G_over3_True']['n']}) / "
                       f"{g1(sec[m]['G_over3_False']['mean'])} ({sec[m]['G_over3_False']['n']})" for m in MODELS])
    rows.append([K] + [f"{rob[m]['n_ties']} / {rob[m]['ties_excluded_reading']}" for m in MODELS])
    t.add(2, rows)
    sp = a["spend_by_model"]
    t.add(3, [[K] + [usd(sp[FULL[m]]) for m in MODELS] + [usd(a["spend_usd"])]])

    gc = cs["sg-b3-grade-calls"]
    pilot = spent(cs, ["sg-b3-grade-calls-pilot"])
    t.intext("pilot", r"with a pilot of \$([\d.]+) on", usd(pilot)[1:])
    t.intext("calls and spend", r"\*\*(\d+ calls, complete, no refusal, \$[\d.]+)\*\*",
             f"{len(gc)} calls, complete, {refusal(root)}, {usd(a['spend_usd'])}")
    t.intext("with the pilot", r"With the pilot, the bet spent \$([\d.]+)\.", f"{pilot + a['spend_usd']:.2f}")
    docked = [pm[m][k] for m in MODELS for k in ("P_fresh", "P_own")]
    t.intext("points docked", r"On average it cost (\d+) to (\d+) points", f(min(docked), 0), f(max(docked), 0))
    h, o = pm["haiku"], pm["opus"]
    t.intext("flawed text, Haiku", r"\*\*Haiku:\*\* ([\d.]+) in its own conversation against ([\d.]+) fresh \(([^)]+)\)",
             f(h["mean"]["own-flawed"], 1), f(h["mean"]["fresh-flawed"], 1), f"{s(h['flawed_D'], 1)} {ci(h['flawed_D_ci'], 1)}")
    t.intext("flawed text, Opus", r"\*\*Opus:\*\* ([\d.]+) against ([\d.]+) \(([^)]+)\)",
             f(o["mean"]["own-flawed"], 1), f(o["mean"]["fresh-flawed"], 1), f"{s(o['flawed_D'], 1)} {ci(o['flawed_D_ci'], 1)}")
    t.intext("clean text", r"own − fresh was ([^ ]+) \(Haiku\), ([^ ]+) \(Sonnet\) and ([^ ]+) \(Opus\)",
             *[s(pm[m]["clean_D"], 1) for m in MODELS])
    lr = {m: "–".join(f(x, 1) for x in rob[m]["loo_range"]) for m in MODELS}
    t.intext("leave one out", r"Haiku's difference ranges ([\d.]+–[\d.]+)\..*?Opus's ranges ([\d.]+–[\d.]+),",
             lr["haiku"], lr["opus"])
    t.intext("floor", r"for Sonnet \(([\d.]+)\) and Opus \(([\d.]+)\)",
             f(pm["sonnet"]["mean"]["fresh-flawed"], 1), f(o["mean"]["fresh-flawed"], 1))
    bd = {m: [f(rob[m]["by_design"][d]["mean"], 1) for d in ("randomised", "before-after", "self-selected")]
          for m in MODELS}
    t.intext("by design", r"- Haiku: ([\d.]+) randomised, ([\d.]+) before-after, ([\d.]+) self-selected;"
             r"\s+- Opus: ([\d.]+), ([\d.]+) and ([\d.]+)\.", *bd["haiku"], *bd["opus"])
    t.intext("study interval", r"\((\d+) studies, where the appended sentence contradicts the data\), against the "
             r"(\d+) whose interval excludes 0.*?- Haiku: ([\d.]+) against ([\d.]+);\s+- Opus: ([\d.]+) against ([\d.]+)\.",
             sec["haiku"]["G_ci_excludes_0_False"]["n"], sec["haiku"]["G_ci_excludes_0_True"]["n"],
             *[g1(sec[m][k]["mean"]) for m in ("haiku", "opus") for k in ("G_ci_excludes_0_False", "G_ci_excludes_0_True")])
    t.intext("over three sentences", r"past three sentences in (\d+) studies;\*\* there its difference was ([\d.]+), "
             r"against ([\d.]+) elsewhere", sec["haiku"]["G_over3_True"]["n"],
             g1(sec["haiku"]["G_over3_True"]["mean"]), g1(sec["haiku"]["G_over3_False"]["mean"]))
    t.intext("gate", r"It is met by (every model)\.",
             "every model" if all(pm[m]["gate_ok"] for m in MODELS) else "not every model")
    common(t, a, cs, "sg-b3", "G", "Pooled G")


# ----- shared -------------------------------------------------------------------------------------------------------

def same_n(rob, dsg):
    ns = {rob[m]["by_design"][dsg]["n"] for m in MODELS}
    return ns.pop() if len(ns) == 1 else "differs by model"


def common(t, a, cs, bet, stat, label):
    p = a[f"pooled_{stat}"]
    t.intext(label.lower(), rf"\*\*{label}\*\*.*?: \*\*(.+?)\*\*", f"{s(p['mean'])} {ci(p['ci'])}")
    t.intext("pre-registered verdict", r"\*\*Pre-registered verdict: ([\w-]+)", a["verdict"])
    t.intext("verdict", r"→ \*\*([\w-]+)\*\*\. Score", a["verdict"])
    if bet != "sg-b2":
        t.intext("program spend", r"The program has spent (?:\*\*)?\$([\d.]+) of \$5\.00",
                 f"{program_spent(cs, bet):.2f}")


TABLES = {"sg-b1": tables_b1, "sg-b2": tables_b2, "sg-b3": tables_b3}


# ----- analysis JSON ------------------------------------------------------------------------------------------------

def project(committed, regen, path, added, missing):
    """The regenerated analysis cut down to the committed file's fields, in the committed order."""
    if isinstance(committed, dict) and isinstance(regen, dict):
        added += [f"{path}{k}" for k in regen if k not in committed]
        out = {}
        for k, v in committed.items():
            if k in regen:
                out[k] = project(v, regen[k], f"{path}{k}.", added, missing)
            else:
                missing.append(f"{path}{k}")
                out[k] = "<absent from the regenerated analysis>"
        return out
    if isinstance(committed, list) and isinstance(regen, list) and len(committed) == len(regen):
        return [project(c, r, f"{path}{i}.", added, missing) for i, (c, r) in enumerate(zip(committed, regen))]
    return regen


def leaves(x):
    if isinstance(x, dict):
        return sum(leaves(v) for v in x.values())
    if isinstance(x, list):
        return sum(leaves(v) for v in x) if x else 1
    return 1


def check_analysis(rep, root, name_, r):
    text = (root / name_).read_text()
    regen = json.dumps(r, indent=1)
    if name_ not in PREDATES or text == regen:
        rep.compare(name_, text, regen)
        return
    committed = json.loads(text)
    added, missing = [], []
    cut = json.dumps(project(committed, r, "", added, missing), indent=1)
    keys = sorted({a.split(".")[-1] for a in added})
    rep.compare(name_, text, cut, what=f"every one of its {leaves(committed)} values compared byte for byte; "
                f"{len(added)} fields the current code adds are not compared ({', '.join(keys)}): "
                f"{PREDATES[name_]}")


def main():
    tmp = R.snapshot([f"programs/{PROGRAM}"])
    try:
        root = tmp / "programs" / PROGRAM
        sys.path[:0] = [str(root / "experiments")]
        rep = R.Report(PROGRAM, root, results_globs=("results/*.md", "results/*-analysis*.json"))
        cs = caches(root)
        main_runs = {}
        for bet, mod in BETS.items():
            for pilot in (True, False):
                name_ = f"results/{bet}-analysis{'-pilot' if pilot else ''}.json"
                if not (root / name_).exists():
                    continue
                m = __import__(mod)
                # sg_common puts /Users/seanpharris/entangled-mind/src on sys.path (the program's run-time client);
                # nothing outside the snapshot may be read here, so drop it again.
                sys.path[:] = [p for p in sys.path if "/entangled-mind" not in p or p.startswith(str(tmp))]
                r = rep.run(name_, lambda: m.analyse(pilot))
                if r is not None:
                    check_analysis(rep, root, name_, r)
                    if not pilot:
                        main_runs[bet] = r
        for bet, (mod, md) in FOLLOWUPS.items():
            if not (root / md).exists():
                continue
            if bet not in main_runs:
                rep.error(md, RuntimeError(f"results/{bet}-analysis.json could not be regenerated"))
                continue
            text = (root / md).read_text()
            r = main_runs[bet]
            try:
                regen = __import__(mod).tables(r)
                v = re.search(r"\*\*Pre-registered verdict: ([\w, -]+?)\.\*\*", text).group(1)
                want = {"pass": "pass, unreplicated"}.get(r["verdict"], r["verdict"])
                if v != want:
                    raise RuntimeError(f"verdict in the prose reads {v!r}; the analysis gives {want!r}")
                cost = re.search(r"\*\*(\d+) calls, complete, no refusal, \$([\d.]+)\*\*", text)
                n = sum(1 for k in cs.get(f"{bet}-grade-calls", {}))
                if cost is None or int(cost.group(1)) != n or cost.group(2) != f"{r['spend_usd']:.3f}":
                    raise RuntimeError(f"calls/spend in the prose do not match the cache ({n} calls, ${r['spend_usd']:.3f})")
            except Exception as e:  # noqa: BLE001
                rep.error(md, e)
                continue
            rep.compare_tables(md, text, regen)
        for bet, md in WRITEUPS.items():
            if not (root / md).exists():
                continue
            if bet not in main_runs:
                rep.error(md, RuntimeError(f"results/{bet}-analysis.json could not be regenerated, so its tables "
                                           "cannot be rebuilt"))
                continue
            t = Tables((root / md).read_text())
            try:
                TABLES[bet](t, main_runs[bet], cs, root)
            except Exception as e:  # noqa: BLE001
                rep.error(md, e)
                continue
            t.check(rep, md)
        return rep.finish()
    finally:
        R.cleanup(tmp)


if __name__ == "__main__":
    R.main_guard(main)
