#!/usr/bin/env python3
"""Program 3 (nature-graded): rebuild every results table from the archived JSON, and check it against the write-ups.

    python3 programs/nature-graded/reproduce.py      # from the repo root; stdlib and numpy only, no keys, no network

In plain English: no script in this program writes a results .md. Each write-up (results/*.md) was written by hand
after a run, and its tables were copied from the run's numbers. This script recomputes those numbers from the
archive and rebuilds every table in every write-up, cell by cell, then compares each rebuilt table with the
committed one, line for line. The chip is a referee here, never a computational resource: its archived counts are
inputs, and nothing is sent to it.

Where the numbers come from (the rawest archive numpy can handle):
  - Chip runs (P3-2/3, P3-15, P3-16): the raw counts in data/*-raw.json and the archived simulator predictions in
    data/*-predictions.json. Each bet's own `analyse()` (p3_2_3_job, p3_15_repeat, p3_16_lone) is run on them in a
    snapshot of the repository, and the analysis it writes (results/<bet>.json) is compared byte for byte with the
    committed one. The tables are then rebuilt from that recomputed analysis.
  - Simulator runs (P3-1): the archived simulated counts in results/p3-1-*.json. P(yes), its SE and the per-qubit
    P(1) are recomputed from those counts with program 1's readout; the simulations themselves (qiskit-aer) are not
    repeated. Program 1's 3 November numbers are recomputed from its archived counts (entangled-mind
    results/stage1-run-1.json).
  - Fits (P3-5, P3-5c): the fits (scipy) and the simulated reference states (qiskit-aer) are not repeated; their
    archived outputs in results/p3-5-coherent-fits.json and results/p3-5c-nested.json are the inputs. What can be
    recomputed with numpy is: the saturated log-likelihood (from program 1's archived tomography counts,
    entangled-mind results/witness-run-1.json), every ΔlogL and LR (from the archived log-likelihoods), every
    bootstrap p-value and null 99th percentile (from the 1,000 archived null draws), the deviance, the per-setting
    shares, and the labels. The χ² 99th percentile, which the program got from scipy, is computed here with a small
    stdlib implementation (regularised incomplete gamma by series, then bisection); it matches scipy's archived value
    to 1e-9.
  - Post hoc simulations for P3-2/3 (data/p3-2-3-arm-sims-posthoc.json, data/p3-2-3-mirror-posthoc-sim.json) are
    archived simulator outputs, used as they are.

How a table is compared: every number in a table is recomputed. Descriptive cells (a row's "what" text, a column
header) are copied from the committed table, so the check is on the numbers; the script says how many cells of each
kind each file has. Bold emphasis is the author's: a recomputed "0.30" matches a committed "**0.30**". Execution
times printed to the second match either the floor or the nearest second of IBM's timestamp (the write-ups use both).
A number that is an exact decimal tie at the printed precision (815 of 1,000 shots, to two places) matches either
rounding: Python rounds the binary float down (0.81), the write-ups sometimes round half up (0.82). Each such cell is
counted in the output (three today: two per-qubit cells in p3-15-repeat.md, E3's 0.2765 in p3-1-scheduled-sim.md).
A few cells are quoted from outside the archive and are copied, not checked: the auditor's re-run column in
p3-1-rerun.md (the auditor's runs are not archived) and the predictions-commit hashes in p3-15-repeat.md (git
history, not JSON). Every file's table count is checked too, so a table added later fails until it is taught here.

Also registered: results/*.json. The three chip analyses are rebuilt byte for byte; for the simulator and fit
outputs, the fields recomputable from the archive (listed above) are compared exactly.

The .qpy circuit files need qiskit to read. No table depends on them: every table here comes from counts,
predictions and fit outputs archived as JSON.
"""
import datetime as dt
import json
import math
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True                                  # nothing is written into the working tree
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # programs/
import repro_common as R  # noqa: E402

PROGRAM = "nature-graded"
EM_FILES = ["programs/entangled-mind/src",                          # encoder + readout (numpy only)
            "programs/entangled-mind/results/pool-run-1.json",      # the q01 web the readout uses
            "programs/entangled-mind/results/stage1-run-1.json",    # 3 November counts (ideal, noisy sim, chip)
            "programs/entangled-mind/results/witness-run-1.json",   # program 1's tomography counts (P3-5, P3-5c)
            "programs/entangled-mind/results/ibm-usage.json"]       # the QPU ledger ("cumulative of 420")
LEDGER_FILES = ["ledger/spend.jsonl"]                               # P3-16's approved QPU seconds (br-003)
ORIG = [117, 125, 124, 123, 144, 136, 143, 141, 142]

MINUS = "−"


# ----- formatting, as the write-ups print numbers ---------------------------------------------------------------

TIES = {}    # printed number -> its other printing, for exact decimal ties (0.815 to two places); reset per table


def _num(x, nd, sign=False, comma=False):
    """x to nd places. An exact tie (counts / shots = 0.815, printed to 2 places) has two faithful printings: Python
    rounds the binary float (0.81), a reader rounds half up (0.82); the write-ups do both. The other printing is
    registered in TIES so either matches; every such cell is counted and reported."""
    spec = f"{'+' if sign else ''}{',' if comma else ''}.{nd}f"
    out = format(x, spec).replace("-", MINUS)
    sc = x * 10 ** nd
    lo = math.floor(sc)
    if abs((sc - lo) - 0.5) < 1e-7:
        for y in (lo / 10 ** nd, (lo + 1) / 10 ** nd):
            o = format(y, spec).replace("-", MINUS)
            if o != out:
                TIES[out] = o
    return out


def f(x, nd=3):
    return _num(x, nd)


def s(x, nd=3):
    return _num(x, nd, sign=True)


def s0(x, nd=3):
    """Signed, except an exact zero prints unsigned (P3-15's 'predicted barrier effect 0.000')."""
    return f(x, nd) if x == 0 else s(x, nd)


def th(x, nd=1):
    return _num(x, nd, comma=True)


def ci(c, nd=3):
    return f"{s(c[0], nd)} to {s(c[1], nd)}"


def g2(x):
    return f"{round(x, 2):g}"


def denver(ts):
    t = dt.datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
    if t.tzinfo is None:
        t = t.replace(tzinfo=dt.timezone.utc)
    try:
        from zoneinfo import ZoneInfo
        return t.astimezone(ZoneInfo("America/Denver"))
    except Exception:  # noqa: BLE001  no tz database: MST is exact for every run here (2026-11-01 to 2027-03-14)
        assert dt.datetime(2026, 11, 1, 8, tzinfo=dt.timezone.utc) <= t < dt.datetime(2027, 3, 14, 9, tzinfo=dt.timezone.utc)
        return t.astimezone(dt.timezone(dt.timedelta(hours=-7)))


def secs(t, how):
    """A Denver time to the second: 'floor' or 'round'."""
    if how == "round":
        t = t + dt.timedelta(microseconds=500_000)
    return t.replace(microsecond=0)


def span_cells(start, finish, with_date):
    """Every way the write-ups print an execution window: start and finish each floored or rounded to the second."""
    a, b = denver(start), denver(finish)
    out = []
    for ha in ("round", "floor"):
        for hb in ("round", "floor"):
            x, y = secs(a, ha), secs(b, hb)
            c = (x.strftime("%Y-%m-%d %H:%M:%S") if with_date else x.strftime("%H:%M:%S")) + "–" + y.strftime("%H:%M:%S")
            if c not in out:
                out.append(c)
    return Alt(out)


# ----- table rebuilding ----------------------------------------------------------------------------------------

K = object()     # descriptive cell: copied from the committed table (a label, not a number)
Q = object()     # a number quoted from outside the archive: copied, not checked (counted separately)
NUM = re.compile(r"([\u2212+-]?\d[\d,]*(?:\.\d+)?)")     # numbers inside a cell (split keeps them at odd indices)


class Alt:
    """A recomputed cell with more than one faithful printing (see span_cells). The first is the default."""

    def __init__(self, options):
        self.options = list(options)


def split_row(line):
    inner = line.strip()
    inner = inner[1:] if inner.startswith("|") else inner
    inner = inner[:-1] if inner.endswith("|") and not inner.endswith("\\|") else inner
    return [c.strip() for c in re.split(r"(?<!\\)\|", inner)]


def join_row(cells):
    return "|" + "|".join(f" {c} " if c != "" else " " for c in cells) + "|"


class Tables:
    """Rebuild a write-up's tables. add() takes the committed table's index and the rebuilt rows (one list of cells
    per row below the header); the header and the |---| line are copied unless `head` gives the header's cells."""

    def __init__(self, text):
        self.have = R.tables_of(text)
        self.done, self.regen = [], []
        self.n = {"calc": 0, "kept": 0, "quoted": 0, "tie": 0}

    def _cell(self, got, committed):
        if got is K or got is Q:
            self.n["kept" if got is K else "quoted"] += 1
            return committed if committed is not None else "<missing in committed table>"
        self.n["calc"] += 1
        opts = got.options if isinstance(got, Alt) else [got]
        bare = committed[2:-2] if committed and committed.startswith("**") and committed.endswith("**") else committed
        for o in opts:
            if bare == o:                           # bold is the author's emphasis
                return committed
        for o in opts:                              # an exact tie printed the other way (see _num)
            g, c = NUM.split(o), NUM.split(bare or "")
            if len(g) == len(c) and g != c and all(a == b or (k % 2 and TIES.get(a) == b) for k, (a, b) in enumerate(zip(g, c))):
                self.n["tie"] += 1
                return committed
        return opts[0]

    def add(self, idx, rows, head=None):
        have = self.have[idx] if idx < len(self.have) else []
        cells = [split_row(l) for l in have]
        missing = "<missing in committed table>"

        def build(r, j):
            c = cells[j] if j < len(cells) else []
            return join_row([self._cell(x, c[k] if k < len(c) else None) for k, x in enumerate(r)])

        lines = [build(head, 0) if head else (have[0] if have else missing),      # header
                 have[1] if len(have) > 1 else missing]                             # the |---| line
        lines += [build(r, j + 2) for j, r in enumerate(rows)]
        TIES.clear()
        self.done.append(idx)
        self.regen.append((idx, lines))

    def check(self, rep, name):
        committed = [f"[{len(self.have)} table(s) in the file]"] + ["\n".join(self.have[i]) if i < len(self.have) else ""
                                                                    for i, _ in self.regen]
        rebuilt = [f"[{len(set(self.done))} table(s) in the file]"] + ["\n".join(l) for _, l in self.regen]
        n = self.n
        what = (f"{len(self.regen)} tables: {n['calc']} cells recomputed, {n['kept']} descriptive cells copied"
                + (f", {n['quoted']} quoted from outside the archive, not checked" if n["quoted"] else "")
                + (f"; {n['tie']} exact tie(s) printed rounded the other way" if n["tie"] else ""))
        rep.compare(name, "\n\n".join(committed), "\n\n".join(rebuilt), what=what)


def qubit_head():
    return [K] + [f"{k} ({q})" for k, q in enumerate(ORIG)]


def p2(xs):
    return [f(x, 2) for x in xs]


def check_fields(rep, name, committed, rebuilt, what):
    """Exact comparison of the recomputed fields of an archived JSON with the committed ones."""
    a = json.dumps(committed, indent=1, sort_keys=True)
    b = json.dumps(rebuilt, indent=1, sort_keys=True)
    rep.compare(name, a, b, what=what)


# ----- χ² quantile (scipy.stats.chi2.ppf), stdlib -----------------------------------------------------------------

def chi2_cdf(x, k):
    """Regularised lower incomplete gamma P(k/2, x/2), by its power series (converges for every x > 0)."""
    a, z = k / 2, x / 2
    if z <= 0:
        return 0.0
    term = total = 1.0 / a
    n = 1
    while abs(term) > 1e-17 * abs(total):
        term *= z / (a + n)
        total += term
        n += 1
    return math.exp(a * math.log(z) - z - math.lgamma(a)) * total


def chi2_ppf(q, k):
    lo, hi = 0.0, 10.0 * k + 100
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if chi2_cdf(mid, k) < q else (lo, mid)
    return (lo + hi) / 2


# ----- main ----------------------------------------------------------------------------------------------------

def main():
    tmp = R.snapshot([f"programs/{PROGRAM}", *EM_FILES, *LEDGER_FILES])
    try:
        root = tmp / "programs" / PROGRAM
        em = tmp / "programs" / "entangled-mind"
        sys.path[:0] = [str(root / "experiments"), str(em / "src")]
        rep = R.Report(PROGRAM, root, results_globs=("results/*.md", "results/*.json"))
        md = {f"results/{p.name}": p.read_text() for p in (root / "results").glob("*.md")}
        committed_json = {p.name: p.read_text() for p in (root / "results").glob("*.json")}
        load = lambda p: json.loads((root / p).read_text())

        import p3sim  # noqa: E402  (imports qiskit names: stubbed, never called below)
        assert p3sim.EM.resolve() == em.resolve(), "p3sim must read program 1's archive from the snapshot"
        web = p3sim.stage1_web()
        stage1 = json.loads((em / "results" / "stage1-run-1.json").read_text())["arms"]
        nov3 = {k: {"p_yes": p3sim.p_yes(v["counts"], web), "shots": sum(v["counts"].values()),
                    "marginals_p1": p3sim.marginals_p1(v["counts"], 9)} for k, v in stage1.items()}
        hw3 = nov3["hardware"]
        usage = json.loads((em / "results" / "ibm-usage.json").read_text())

        def cumulative(job_id):
            tot = 0.0
            for e in usage:
                tot += float(e["quantum_seconds"])
                if e["job_id"] == job_id:
                    return tot
            raise KeyError(f"{job_id} is not in program 1's QPU ledger")

        # ---- the chip analyses: each bet's own analyse(), from raw counts and archived predictions --------------
        mods = {}
        for mod, out in (("p3_2_3_job", "p3-2-3-job.json"), ("p3_15_repeat", "p3-15-repeat.json"),
                         ("p3_16_lone", "p3-16-lone-job.json")):
            name = f"results/{out}"
            (root / name).unlink()                       # rebuilt from scratch
            m = __import__(mod)
            if rep.run(name, m.analyse) is not None or (root / name).exists():
                rep.compare(name, committed_json[out], (root / name).read_text(),
                            what=f"rebuilt by {mod}.analyse() from the raw counts, byte for byte")
                mods[mod] = m
        j23 = load("results/p3-2-3-job.json") if "p3_2_3_job" in mods else None
        j15 = load("results/p3-15-repeat.json") if "p3_15_repeat" in mods else None
        j16 = load("results/p3-16-lone-job.json") if "p3_16_lone" in mods else None

        # ---- P3-2 / P3-3 -------------------------------------------------------------------------------------
        name = "results/p3-2-3-job.md"
        try:
            pred = load("data/p3-2-3-predictions.json")
            post = load("data/p3-2-3-arm-sims-posthoc.json")["arms"]
            mir = load("data/p3-2-3-mirror-posthoc-sim.json")
            sim_shots = mods["p3_2_3_job"].SIM_SHOTS
            a, P = j23["arms"], pred["predictions"]
            t = Tables(md[name])
            lay = pred["layout_qubits_in_clbit_order"]
            rows = [["S", f"corrected-sim prediction, original layout (live calibration "
                          f"{denver(pred['calibration']['read_at']):%H:%M}, {sim_shots:,} shots)",
                     f(P["A_orig"]["p_yes"]), f(P["A_orig"]["se"])]]
            for g in ("A", "B", "B2", "C", "D"):
                rows.append([K, K, f(a[g]["p_yes"]), f(a[g]["se"])])
            for g in ("L1", "L2"):
                rows.append([g, f"original circuit on qubits {', '.join(map(str, lay[g]))} (sim {f(P[g]['p_yes'])})",
                             f(a[g]["p_yes"]), f(a[g]["se"])])
            rows.append([K, K, f(hw3["p_yes"]), f(math.sqrt(hw3["p_yes"] * (1 - hw3["p_yes"]) / hw3["shots"]))])
            t.add(0, rows)
            t.add(1, [[K, *p2(P["A_orig"]["marginals_p1"])], [K, *p2(a["A"]["marginals_p1"])],
                      [K, *p2(hw3["marginals_p1"])], [K, *p2(a["B"]["marginals_p1"])],
                      [K, *p2(j23["readout"]["p1_given_0"])], [K, *p2(j23["readout"]["p0_given_1"])],
                      [K, *p2(a["M"]["marginals_p1"])], [K, *p2(mir["per_qubit_error"])]], head=qubit_head())
            rows = []
            for g in ("B2", "C", "D", "L1", "L2"):
                pre = g in ("L1", "L2")
                sim = P[g]["marginals_p1"] if pre else post[g]["marginals_p1"]
                chip, n = a[g]["marginals_p1"], a[g]["shots"]
                z = [(c - m) / math.sqrt(c * (1 - c) / n) for c, m in zip(chip, sim)]
                rows += [[g, "physical qubit", *map(str, lay[g] if pre else ORIG)],
                         [g, "chip", *p2(chip)],
                         [g, f"sim (pre-registered, {sim_shots:,})" if pre else "sim (post hoc)", *p2(sim)],
                         [g, "chip − sim (z)", *[f"{c - m:+.2f} ({zz:+.0f})" for c, m, zz in zip(chip, sim, z)]]]
            t.add(2, rows)
            t.check(rep, name)
        except Exception as e:  # noqa: BLE001
            rep.error(name, e)

        # ---- P3-15 -------------------------------------------------------------------------------------------
        name = "results/p3-15-repeat.md"
        try:
            M15 = mods["p3_15_repeat"]
            r1, r2 = j15["runs"]["1"], j15["runs"]["2"]
            raws = {k: load(f"data/p3-15-run{k}-raw.json") for k in (1, 2)}
            preds = {k: load(f"data/p3-15-run{k}-predictions.json") for k in (1, 2)}
            t = Tables(md[name])
            ts = {k: raws[k]["timestamps"] for k in (1, 2)}
            gap = (denver(ts[2]["running"]) - denver(ts[1]["finished"])).total_seconds()
            hm = round(gap / 60)
            rows = []
            for k in (1, 2):
                span = span_cells(ts[k]["running"], ts[k]["finished"], True)
                if k == 2:
                    span = Alt([o + f", {hm // 60} h {hm % 60:02d} min after run 1" for o in span.options])
                u = raws[k]["usage"]
                rows.append([f"run {k}", f"`{u['job_id']}`", Q, span,
                             f"{u['quantum_seconds']:.1f} (estimate {g2(preds[k]['estimate_qpu_s'])})",
                             f"{cumulative(u['job_id']):.0f}"])
            t.add(0, rows)
            dr = j15["drift_run2_minus_run1"]
            rows = []
            for arm in ("BB", "NB", "BI", "NI", "B_pooled", "N_pooled"):
                x1, x2 = r1["arms"][arm], r2["arms"][arm]
                assert x1["shots"] == x2["shots"]
                rows.append([K, K, f"{x1['shots']:,}", f(x1["p_yes"]), f(x2["p_yes"]),
                             f"{s(dr[arm]['diff'])} ({ci(dr[arm]['ci90'])})"])
            p1, p2_ = preds[1]["predictions"], preds[2]["predictions"]
            same = lambda key: "barrier = no barrier" if p1[f"barrier_{key}"]["p_yes"] == p1[f"nobarrier_{key}"]["p_yes"] else "?"
            rows.append(["prediction", f"live calibration, ALAP ({same('ALAP')})", f"{M15.SIM_SHOTS:,}",
                         *[f"{f(pp['barrier_ALAP']['p_yes'], 4)} (read {denver(preds[k]['calibration']['read_at']):%H:%M})"
                           for k, pp in ((1, p1), (2, p2_))], ""])
            rows.append(["prediction", "ASAP: barrier / no barrier", f"{M15.SIM_SHOTS:,}",
                         *[f"{f(pp['barrier_ASAP']['p_yes'], 4)} / {f(pp['nobarrier_ASAP']['p_yes'], 4)}" for pp in (p1, p2_)], ""])
            rows.append(["3 November", f"barrier, own job of {hw3['shots']:,} shots (archived)", f"{hw3['shots']:,}",
                         f(hw3["p_yes"]), "", ""])
            a4 = j23["arms"]["A"]
            rows.append(["4 November", K, f"{a4['shots']:,}", f(a4["p_yes"]), "", ""])
            assert a4["p_yes"] == M15.NOV4_NI and j15["control_NI_vs_nov4"]["nov4"] == a4["p_yes"]
            t.add(1, rows)
            cls = {"within": "within ±0.05", "between": "between", "big": "clear"}
            rows = []
            for key in ("BB_minus_NB", "barrier_pooled", "grouping_pooled"):
                c1, c2 = r1["comparisons"][key], r2["comparisons"][key]
                rows.append([K, f"{s(c1['diff'])} ({ci(c1['ci90'])})", cls[r1["classes"][key]],
                             f"{s(c2['diff'])} ({ci(c2['ci90'])})", cls[r2["classes"][key]]])
            bi = [M15._diff(r["arms"]["BI"], r["arms"]["NI"]) for r in (r1, r2)]
            inside = lambda d: "within ±0.05" if d["within_equiv"] else "not inside ±0.05"
            rows.append([K, f"{s(bi[0]['diff'])} ({ci(bi[0]['ci90'])})", inside(bi[0]),
                         f"{s(bi[1]['diff'])} ({ci(bi[1]['ci90'])})", inside(bi[1])])
            e1, e2 = r1["predicted_barrier_effect"], r2["predicted_barrier_effect"]
            rows.append([K, f"{s0(e1['if_ALAP'])} (if ALAP), {s0(e1['if_ASAP'])} (if ASAP)", "",
                         "same" if e1 == e2 else f"{s0(e2['if_ALAP'])} (if ALAP), {s0(e2['if_ASAP'])} (if ASAP)", ""])
            t.add(2, rows)
            rows = [[K, *p2(p1["barrier_ALAP"]["marginals_p1"])]]
            for k, r in (("1", r1), ("2", r2)):
                for arm in ("BB", "NB", "BI", "NI"):
                    rows.append([f"run {k} {arm}", *p2(r["arms"][arm]["marginals_p1"])])
            t.add(3, rows, head=qubit_head())
            t.check(rep, name)
        except Exception as e:  # noqa: BLE001
            rep.error(name, e)

        # ---- P3-16 -------------------------------------------------------------------------------------------
        name = "results/p3-16-lone-job.md"
        try:
            M16 = mods["p3_16_lone"]
            pred = load("data/p3-16-predictions.json")
            raws = {j: load(f"data/p3-16-job{j}-raw.json") for j in "ABC"}
            t = Tables(md[name])
            rows = []
            for n, j in enumerate(pred["job_order"]):
                u, tsj = raws[j]["usage"], raws[j]["timestamps"]
                rows.append([f"{j} `{u['job_id']}`", K, span_cells(tsj["running"], tsj["finished"], n == 0),
                             f"{u['quantum_seconds']:.1f} (estimate {g2(pred['estimate_qpu_s'][j])})",
                             f"{cumulative(u['job_id']):.0f}"])
            billed = sum(raws[j]["usage"]["quantum_seconds"] for j in "ABC")
            last = raws[pred["job_order"][-1]]["usage"]["job_id"]
            rows.append(["total", "", f"{j16['spread_minutes']:.1f} minutes, first start to last finish",
                         f"**{billed:.1f}** of {M16.approved_qpu_s():g} approved (estimate {g2(pred['estimate_total_qpu_s'])})",
                         f"{cumulative(last):.0f}"])
            t.add(0, rows)
            arms, pp = j16["arms"], pred["predictions"]
            p15 = [j15["runs"][k]["arms"]["BB"]["p_yes"] for k in ("1", "2")]
            pooled15 = sum(p15) / 2
            rows = [[a_, K, f(arms[a_]["p_yes"]), f(arms[a_]["se"]), f(arms[a_]["entropy_bits"], 2)]
                    for a_ in ("A", "B", "CB", "CN")]
            alap_same = pp["barrier_ALAP"]["p_yes"] == pp["nobarrier_ALAP"]["p_yes"]
            rows.append(["prediction", f"live calibration, ALAP ({'barrier = no barrier' if alap_same else '?'}), "
                                       f"{M16.SIM_SHOTS:,} shots", f(pp["barrier_ALAP"]["p_yes"], 4), "", ""])
            rows.append(["prediction", "ASAP: barrier / no barrier",
                         f"{f(pp['barrier_ASAP']['p_yes'], 4)} / {f(pp['nobarrier_ASAP']['p_yes'], 4)}", "", ""])
            rows.append(["P3-15 (4 November)", K, f"{f(p15[0])}, {f(p15[1])} (pooled {f(pooled15, 4)})", "", ""])
            rows.append(["3 November", f"barrier, own job of {hw3['shots']:,} shots (archived)", f(hw3["p_yes"]), "", ""])
            t.add(1, rows)
            cls = {"within": "within ±0.05", "between": "not within, not clear", "big": "clear"}
            rows = []
            for key, c in j16["comparisons"].items():
                rows.append([K, s(c["diff"]), ci(c["ci90"]), s(c["z"], 2), cls[j16["classes"][key]]])
            ctrl = arms["CB"]["p_yes"] - pooled15
            rows.append([K, s(ctrl), "", "", "within the ±0.05 band" if abs(ctrl) <= M16.CONTROL_TOL else "outside the ±0.05 band"])
            rows.append([K, s(hw3["p_yes"] - arms["A"]["p_yes"]), "", "", ""])
            t.add(2, rows)
            t.add(3, [[K, *p2(pp["barrier_ALAP"]["marginals_p1"])]]
                  + [[a_, *p2(arms[a_]["marginals_p1"])] for a_ in ("A", "B", "CB", "CN")], head=qubit_head())
            t.check(rep, name)
        except Exception as e:  # noqa: BLE001
            rep.error(name, e)

        # ---- P3-1: simulated counts archived; P(yes), SE and marginals recomputed from them ----------------------
        def from_counts(r):
            c = r["counts"]
            p = p3sim.p_yes(c, web)
            n = sum(c.values())
            return {"p_yes": p, "se": math.sqrt(p * (1 - p) / n), "shots": n, "marginals_p1": p3sim.marginals_p1(c, 9)}

        p31 = {}
        for out in ("p3-1-scheduled-sim.json", "p3-1-rerun.json"):
            name = f"results/{out}"
            try:
                d = json.loads(committed_json[out])
                runs = {"control_unscheduled": d["control_unscheduled"], "scheduled": d["scheduled"],
                        **{k: v for k, v in d["exploratory"].items() if isinstance(v, dict)}}
                mine = {k: from_counts(v) for k, v in runs.items()}
                keep = {k: {x: v[x] for x in ("p_yes", "se", "shots", "marginals_p1")} for k, v in runs.items()}
                M1 = __import__("p3_1_scheduled")
                arch = {k: {"p_yes": v["p_yes"], "marginals_p1": v["marginals_p1"]} for k, v in nov3.items()}
                ok_c = abs(mine["control_unscheduled"]["p_yes"] - M1.CONTROL_TARGET) <= M1.CONTROL_TOL
                verdict = "untestable" if not ok_c else ("pass" if mine["scheduled"]["p_yes"] >= M1.PASS_AT else "fail")
                mine_all = {"runs": mine, "archived": arch, "verdict": verdict,
                            "rule": {"pass_at": M1.PASS_AT, "control_target": M1.CONTROL_TARGET,
                                     "control_tol": M1.CONTROL_TOL, "control_ok": ok_c}}
                theirs = {"runs": keep, "archived": d["archived"], "verdict": d["verdict"], "rule": d["rule"]}
                if "secondary_marginal_control" in d:
                    na = arch["noisy_sim"]["marginals_p1"]
                    se_a = [math.sqrt(max(m * (1 - m), 1e-9) / 1000) for m in na]
                    max_z = lambda m: max(abs(x - y) / e for x, y, e in zip(m, na, se_a))
                    smc = d["secondary_marginal_control"]
                    mine_all["max_z"] = {"noiseless": max_z(smc["noiseless"]["marginals_p1"]),
                                         "control_unscheduled": max_z(mine["control_unscheduled"]["marginals_p1"])}
                    theirs["max_z"] = {"noiseless": smc["noiseless"]["max_z"],
                                       "control_unscheduled": smc["control_unscheduled"]["max_z"]}
                check_fields(rep, name, theirs, mine_all,
                             "P(yes), SE, shots and per-qubit P(1) recomputed from the archived simulated counts; "
                             "3 November recomputed; verdict; simulations not repeated")
                p31[out] = {**mine, "n_delays": d["n_delays"]}
            except Exception as e:  # noqa: BLE001
                rep.error(name, e)

        name = "results/p3-1-scheduled-sim.md"
        try:
            m = p31["p3-1-scheduled-sim.json"]
            ide, noi = nov3["ideal_sim"], nov3["noisy_sim"]
            t = Tables(md[name])
            t.add(0, [[f"ideal (archived, {ide['shots']:,} shots)", f(ide["p_yes"]), "—"],
                      [f"program 1 noisy sim (archived, {noi['shots']:,} shots)", f(noi["p_yes"]), "—"],
                      [K, f(m["control_unscheduled"]["p_yes"]), f(m["control_unscheduled"]["se"], 4)],
                      [f"**primary:** rebuild, ALAP-scheduled ({m['n_delays']} delays)", f(m["scheduled"]["p_yes"]),
                       f(m["scheduled"]["se"], 4)],
                      [f"hardware (archived, {hw3['shots']:,} shots)", f(hw3["p_yes"]),
                       f(math.sqrt(hw3["p_yes"] * (1 - hw3["p_yes"]) / hw3["shots"]))]])
            e2, e3 = m["E2_scheduled_zz_0.1rad_per_cz"], m["E3_scheduled_errors_x3"]
            t.add(1, [[K, f"not applied (bug: all-qubit ZZ error overridden by local CZ errors); {f(e2['p_yes'])} is the "
                          f"scheduled model at {e2['shots']:,} shots"],
                      [K, f(e3["p_yes"])],
                      [K, K]])
            t.add(2, [[K, *p2(ide["marginals_p1"])], [K, *p2(noi["marginals_p1"])],
                      [K, *p2(m["control_unscheduled"]["marginals_p1"])], [K, *p2(m["scheduled"]["marginals_p1"])],
                      [K, *p2(e3["marginals_p1"])], [K, *p2(hw3["marginals_p1"])]], head=qubit_head())
            t.check(rep, name)
        except Exception as e:  # noqa: BLE001
            rep.error(name, e)

        name = "results/p3-1-rerun.md"
        try:
            a_, b_ = p31["p3-1-scheduled-sim.json"], p31["p3-1-rerun.json"]
            E2, E3 = "E2_scheduled_zz_0.1rad_per_cz", "E3_scheduled_errors_x3"
            t = Tables(md[name])
            t.add(0, [[f"control, unscheduled, {b_['control_unscheduled']['shots']:,} shots",
                       f(a_["control_unscheduled"]["p_yes"], 4), f(b_["control_unscheduled"]["p_yes"], 4), Q],
                      [f"primary, ALAP-scheduled, {b_['scheduled']['shots']:,} shots",
                       f(a_["scheduled"]["p_yes"], 4), f(b_["scheduled"]["p_yes"], 4), Q],
                      [f"E2: scheduled + ZZ 0.1 rad per CZ, {b_[E2]['shots']:,}",
                       f"{f(a_[E2]['p_yes'], 4)} (twist not applied)", f(b_[E2]["p_yes"], 4), Q],
                      [f"E3: scheduled, errors ×3, T1 and T2 ÷3, {b_[E3]['shots']:,}",
                       f"{f(a_[E3]['p_yes'], 4)} (T1/T2 not divided)", f(b_[E3]["p_yes"], 4), Q]])
            t.add(1, [[K, *p2(b_["scheduled"]["marginals_p1"])], [K, *p2(b_[E2]["marginals_p1"])],
                      [K, *p2(hw3["marginals_p1"])]], head=qubit_head())
            t.check(rep, name)
        except Exception as e:  # noqa: BLE001
            rep.error(name, e)

        # ---- P3-5 and P3-5c: fits archived; likelihood bookkeeping, bootstrap p and quantiles recomputed ---------
        import p3_5_fits as F  # noqa: E402  (scipy stubbed: only its numpy helpers are called)
        witness = {it["id"]: it for it in json.loads((em / "results" / "witness-run-1.json").read_text())["items"]}

        def sat(item_id):
            counts = {st: F.counts_vec(c) for st, c in zip(F.SETTINGS, witness[item_id]["hardware_counts"][:9])}
            return F.saturated(counts)

        name = "results/p3-5-coherent-fits.json"
        try:
            d = json.loads(committed_json["p3-5-coherent-fits.json"])
            theirs, mine = {}, {}
            for it in d["items"]:
                w = witness[it["id"]]
                theirs[it["id"]] = {"negativity_hardware_archived": it["negativity_hardware_archived"],
                                    "negativity_noisy_sim_archived": it["negativity_noisy_sim_archived"],
                                    "physical_qubits": it["physical_qubits"]}
                mine[it["id"]] = {"negativity_hardware_archived": w["hardware"]["negativity"],
                                  "negativity_noisy_sim_archived": w["noisy_sim"]["negativity"],
                                  "physical_qubits": w["physical_qubits"]}
                for ref in ("primary", "secondary_ideal_reference"):
                    r = it[ref]
                    theirs[it["id"]][ref] = {"logL_saturated": r["logL_saturated"], "dlogL": r["dlogL"]}
                    mine[it["id"]][ref] = {"logL_saturated": sat(it["id"]),
                                           "dlogL": r["coherent"]["logL"] - r["incoherent"]["logL"]}
            n_pass = sum(it["primary"]["coherent"]["logL"] - it["primary"]["incoherent"]["logL"] >= F.PASS_DLOGL
                         for it in d["items"])
            theirs["verdict"] = [d["n_items_coherent_wins"], d["verdict"]]
            mine["verdict"] = [n_pass, "pass" if n_pass >= F.PASS_ITEMS else "fail"]
            check_fields(rep, name, theirs, mine, "saturated logL from program 1's counts, ΔlogL, verdict and archived "
                                                  "negativities recomputed; fits not repeated")
        except Exception as e:  # noqa: BLE001
            rep.error(name, e)

        name = "results/p3-5-coherent-fits.md"
        try:
            d = json.loads(committed_json["p3-5-coherent-fits.json"])
            t = Tables(md[name])
            rows = []
            for it in d["items"]:
                r = it["primary"]
                dl = r["coherent"]["logL"] - r["incoherent"]["logL"]
                rows.append([f"{it['id']} ({', '.join(map(str, it['physical_qubits']))})", th(r["logL_ref"]),
                             th(r["coherent"]["logL"]), th(r["incoherent"]["logL"]), th(sat(it["id"])), s(dl, 1),
                             "yes" if dl >= F.PASS_DLOGL else "no"])
            t.add(0, rows)
            t.add(1, [[it["id"], f(it["primary"]["negativity_ref"]), f(it["primary"]["coherent"]["negativity"]),
                       f(it["primary"]["incoherent"]["negativity"]), f(witness[it["id"]]["hardware"]["negativity"]),
                       f(witness[it["id"]]["noisy_sim"]["negativity"])] for it in d["items"]])
            t.check(rep, name)
        except Exception as e:  # noqa: BLE001
            rep.error(name, e)

        import numpy as np  # noqa: E402
        import p3_5c_fits as C  # noqa: E402

        def boot(null, lr):
            return {"p": float((1 + sum(x >= lr for x in null)) / (len(null) + 1)), "B": len(null),
                    "floor": 1 / (len(null) + 1), "q99": float(np.percentile(null, 99))}

        def nested(r, sets):
            c, i, full = sets
            lr_c, lr_i = 2 * (r["logL"][full] - r["logL"][i]), 2 * (r["logL"][full] - r["logL"][c])
            bc, bi = boot(r["boot_rotation"]["null"], lr_c), boot(r["boot_blur"]["null"], lr_i)
            return {"LR_rotation_given_blur": lr_c, "LR_blur_given_rotation": lr_i, "boot_rotation": bc, "boot_blur": bi,
                    "label_rotation": "present" if bc["p"] < C.ALPHA else "not detected",
                    "label_blur": "present" if bi["p"] < C.ALPHA else "not detected"}

        def nested_theirs(r):
            return {k: ({x: r[k][x] for x in ("p", "B", "floor", "q99")} if k.startswith("boot") else r[k])
                    for k in ("LR_rotation_given_blur", "LR_blur_given_rotation", "boot_rotation", "boot_blur",
                              "label_rotation", "label_blur")}

        p5c = {}
        name = "results/p3-5c-nested.json"
        try:
            d = json.loads(committed_json["p3-5c-nested.json"])
            theirs, mine = {}, {}
            for r in d["items"]:
                full = "full16"
                k_full = len(C.zero(full))
                dev = 2 * (sat(r["id"]) - r["logL"][full])
                df = 27 - k_full
                q99 = chi2_ppf(0.99, df)
                sh = {}
                for kind, lr in (("rotation", 2 * (r["logL"][full] - r["logL"]["inc9"])),
                                 ("blur", 2 * (r["logL"][full] - r["logL"]["coh"]))):
                    ps = r["setting_shares"][kind]["per_setting"]
                    top = max(ps, key=ps.get)
                    sh[kind] = {"top_setting": top, "top_share": ps[top] / lr if lr > 0 else None}
                g = r["goodness_of_fit"]
                mine[r["id"]] = {**nested(r, C.SETS["primary"]),
                                 "secondary14": nested(r["secondary14"], C.SETS["secondary14"]),
                                 "goodness_of_fit": {"deviance": dev, "df": df, "chi2_q99": f"{q99:.9g}", "misfit": dev > q99},
                                 "shares": sh,
                                 "cv_agrees": {"rotation": (r["cv_gain_rotation"] > 0) == (r["label_rotation"] == "present"),
                                               "blur": (r["cv_gain_blur"] > 0) == (r["label_blur"] == "present")},
                                 "9-knob comparison": r["logL"]["coh"] - r["logL"]["inc9"]}
                theirs[r["id"]] = {**nested_theirs(r), "secondary14": nested_theirs(r["secondary14"]),
                                   "goodness_of_fit": {**g, "chi2_q99": f"{g['chi2_q99']:.9g}"},
                                   "shares": {k: {x: r["setting_shares"][k][x] for x in ("top_setting", "top_share")}
                                              for k in ("rotation", "blur")},
                                   "cv_agrees": r["cv_agrees"],
                                   "9-knob comparison": r["p3_5_comparison"]["9-knob blur family (with decay), fixed reference"]}
                p5c[r["id"]] = mine[r["id"]]
            check_fields(rep, name, theirs, mine, "LRs, bootstrap p and null 99th percentiles (from the archived null "
                                                  "draws), labels, deviance, χ² quantile (to 9 digits), setting shares "
                                                  "recomputed; fits not repeated")
        except Exception as e:  # noqa: BLE001
            rep.error(name, e)

        name = "results/p3-5c-nested.md"
        try:
            d = json.loads(committed_json["p3-5c-nested.json"])
            p35 = {it["id"]: it["primary"] for it in json.loads(committed_json["p3-5-coherent-fits.json"])["items"]}
            t = Tables(md[name])
            rows = []
            for r in d["items"]:
                x = p5c[r["id"]]
                both = (x["label_rotation"], x["label_blur"]) == ("present", "present")
                lab = "both present" if both else f"rotation {x['label_rotation']}, blur {x['label_blur']}"
                rows.append([f"{r['id']} ({', '.join(map(str, r['physical_qubits']))})",
                             f(x["LR_rotation_given_blur"], 1), f(x["boot_rotation"]["q99"], 1), f(x["boot_rotation"]["p"]),
                             f(x["LR_blur_given_rotation"], 1), f(x["boot_blur"]["q99"], 1), f(x["boot_blur"]["p"]), lab])
            t.add(0, rows)
            gofs = {x["goodness_of_fit"]["df"] for x in p5c.values()}
            assert len(gofs) == 1
            q99 = chi2_ppf(0.99, gofs.pop())
            rows = []
            for r in d["items"]:
                x, sh, ng = p5c[r["id"]], p5c[r["id"]]["shares"], r["negativity"]
                gf = x["goodness_of_fit"]
                rows.append([r["id"], f(gf["deviance"], 1) + (" (misfit)" if gf["misfit"] else ""),
                             f"{f(sh['rotation']['top_share'], 2)} ({sh['rotation']['top_setting']})",
                             f"{f(sh['blur']['top_share'], 2)} ({sh['blur']['top_setting']})",
                             s(r["cv_gain_rotation"], 1), s(r["cv_gain_blur"], 1),
                             " / ".join(f(ng[k]) for k in ("ref", "coh", "inc9", "full16"))])
            t.add(1, rows, head=[K, f"full16 deviance ({x['goodness_of_fit']['df']} df; q99 {f(q99, 1)})", K, K, K, K, K])
            rows = []
            for r in d["items"]:
                c3 = r["p3_5_comparison"]
                pub = p35[r["id"]]["coherent"]["logL"] - p35[r["id"]]["incoherent"]["logL"]
                rows.append([r["id"], s(pub, 1), *[s(c3[k], 2) for k in list(c3)[:3]], s(p5c[r["id"]]["9-knob comparison"], 2)])
            t.add(2, rows)
            rows = []
            for r in d["items"]:
                if "spectator" in r:
                    sp = r["spectator"]
                    rows.append([r["id"], f(sp["trace_distance_to_ref"]),
                                 *[str(sp["outcomes"][o]) for o in ("detected as rotation", "absorbed as blur", "invisible")]])
            t.add(3, rows)
            t.check(rep, name)
        except Exception as e:  # noqa: BLE001
            rep.error(name, e)

        # ---- P3-18: fresh chip job; fits archived, everything else recomputed from the raw counts and the nulls -----
        import p3_18_fresh as P18  # noqa: E402  (scipy/qiskit stubbed: only numpy helpers and the sentence code run)
        p18 = {}
        name = "results/p3-18-fresh-job.json"
        try:
            d = json.loads(committed_json["p3-18-fresh-job.json"])
            prep, raw = load("data/p3-18-prepared.json"), load("data/p3-18-raw.json")
            pairs = P18.per_pair(prep, raw, {it: None for it in P18.ITEMS})
            theirs, mine = {}, {}
            for r in d["items"]:
                it, P = r["id"], pairs[r["id"]]
                lr_c, lr_i = 2 * (r["logL"]["full16"] - r["logL"]["inc9"]), 2 * (r["logL"]["full16"] - r["logL"]["coh"])
                bc, bi = boot(r["boot_rotation"]["null"], lr_c), boot(r["boot_blur"]["null"], lr_i)
                dev = 2 * (F.saturated(P["counts"]) - r["logL"]["full16"])
                sc = max(1.0, dev / 11)
                sh = {}
                for kind, lr in (("rotation", lr_c), ("blur", lr_i)):
                    ps = r["setting_shares"][kind]["per_setting"]
                    top = max(ps, key=ps.get)
                    sh[kind] = {"top_setting": top, "top_share": ps[top] / lr if lr > 0 else None}
                mine[it] = {"assignment_matrix": P["A"].tolist(), "shots_per_setting": P["n"], "LR_rotation_given_blur": lr_c,
                            "LR_blur_given_rotation": lr_i, "boot_rotation": bc, "boot_blur": bi,
                            "label_rotation": "present" if bc["p"] < C.ALPHA else "not detected",
                            "label_blur": "present" if bi["p"] < C.ALPHA else "not detected",
                            "deviance": dev, "misfit": dev > chi2_ppf(0.99, 11), "overdispersion": sc, "shares": sh}
                g = r["goodness_of_fit"]
                theirs[it] = {"assignment_matrix": r["assignment_matrix"], "shots_per_setting": r["shots_per_setting"],
                              **{k: r[k] for k in ("LR_rotation_given_blur", "LR_blur_given_rotation", "label_rotation", "label_blur")},
                              "boot_rotation": {x: r["boot_rotation"][x] for x in ("p", "B", "floor", "q99")},
                              "boot_blur": {x: r["boot_blur"][x] for x in ("p", "B", "floor", "q99")},
                              "deviance": g["deviance"], "misfit": g["misfit"], "overdispersion": g["overdispersion"],
                              "shares": {k: {x: r["setting_shares"][k][x] for x in ("top_setting", "top_share")} for k in sh}}
                p18[it] = (r, mine[it])
            labels = {it: {"rotation": m["label_rotation"] == "present", "blur": m["label_blur"] == "present"} for it, (_, m) in p18.items()}
            infos = {it: {"shares": {k: r["setting_shares"][k]["per_setting"] for k in ("rotation", "blur")},
                          "LR_rotation": m["LR_rotation_given_blur"], "LR_blur": m["LR_blur_given_rotation"],
                          "gof": {"misfit": m["misfit"], "deviance": m["deviance"], "overdispersion": m["overdispersion"]},
                          "q99_rotation": m["boot_rotation"]["q99"], "q99_blur": m["boot_blur"]["q99"]} for it, (r, m) in p18.items()}
            v = P18.verdict(labels, infos=infos)
            day = denver(raw["timestamps"]["running"])
            sent = [x.replace("{date}", f"{day.day} November") for x in v["sentences"]]
            sec2 = d["secondary_prepared_reference"]
            lab2 = {r["id"]: {"rotation": boot(r["boot_rotation"]["null"], 2 * (r["logL"]["full16"] - r["logL"]["inc9"]))["p"] < C.ALPHA,
                              "blur": boot(r["boot_blur"]["null"], 2 * (r["logL"]["full16"] - r["logL"]["coh"]))["p"] < C.ALPHA}
                    for r in sec2["items"]}
            word = lambda L: ("both" if L["rotation"] and L["blur"] else "rotation only" if L["rotation"] else "blur only" if L["blur"] else "neither")
            sent.append("Under the reference prepared before submission (IBM's calibration read at preparation; nulls at "
                        f"B = 100 only), the labels are {'; '.join(f'{it}: ' + word(lab2[it]) for it in P18.ITEMS)}. Reported, not scored.")
            theirs["verdict"], mine["verdict"] = [d["verdict"], d["n_both"], d["sentences"]], [v["verdict"], v["n_both"], sent]
            theirs["qpu_s"], mine["qpu_s"] = d["qpu_s"], raw["usage"]["quantum_seconds"]
            check_fields(rep, name, theirs, mine, "assignment matrices from the raw calibration counts, LRs, bootstrap p and "
                                                  "99th percentiles (archived null draws), labels, deviance (saturated logL from "
                                                  "the raw counts), overdispersion, shares, verdict and every sentence "
                                                  "(p3_18_fresh.verdict) recomputed; fits not repeated")
        except Exception as e:  # noqa: BLE001
            rep.error(name, e)

        name = "results/p3-18-fresh-job.md"
        try:
            d = json.loads(committed_json["p3-18-fresh-job.json"])
            p35 = {r["id"]: r for r in json.loads(committed_json["p3-5c-nested.json"])["items"]}
            t = Tables(md[name])
            rows = []
            for it, (r, m) in p18.items():
                both = m["label_rotation"] == m["label_blur"] == "present"
                lab = "both present" if both else ("rotation only" if m["label_rotation"] == "present" else
                                                   "blur only" if m["label_blur"] == "present" else "neither")
                q = p35[it]
                rows.append([f"{it} ({', '.join(map(str, q['physical_qubits']))})",
                             f(m["LR_rotation_given_blur"], 1), f(m["boot_rotation"]["q99"], 1),
                             f"{f(m['boot_rotation']['p'])} ({m['boot_rotation']['B']})",
                             f(m["LR_blur_given_rotation"], 1), f(m["boot_blur"]["q99"], 1),
                             f"{f(m['boot_blur']['p'])} ({m['boot_blur']['B']})", lab,
                             f"{f(2 * (q['logL']['full16'] - q['logL']['inc9']), 1)} / {f(2 * (q['logL']['full16'] - q['logL']['coh']), 1)}"])
            t.add(0, rows)
            rows = []
            for it, (r, m) in p18.items():
                sc, ng, sh = m["overdispersion"], r["negativity"], m["shares"]
                rows.append([it, f(m["deviance"], 1) + (" (misfit)" if m["misfit"] else ""), f(sc, 2),
                             f"{f(m['LR_rotation_given_blur'] / sc, 1)} / {f(m['LR_blur_given_rotation'] / sc, 1)}",
                             f"{f(sh['rotation']['top_share'], 2)} ({sh['rotation']['top_setting']})",
                             f"{f(sh['blur']['top_share'], 2)} ({sh['blur']['top_setting']})",
                             " / ".join(f(ng[k]) for k in ("ref", "coh", "inc9", "full16"))])
            t.add(1, rows)
            rows = []
            for r in d["secondary_prepared_reference"]["items"]:
                lc, li = 2 * (r["logL"]["full16"] - r["logL"]["inc9"]), 2 * (r["logL"]["full16"] - r["logL"]["coh"])
                bc, bi = boot(r["boot_rotation"]["null"], lc), boot(r["boot_blur"]["null"], li)
                pp = lambda x: f(x, 4) if x < 0.01 else f(x)
                lab = {(True, True): "both", (True, False): "rotation only", (False, True): "blur only", (False, False): "neither"}[
                    (bc["p"] < C.ALPHA, bi["p"] < C.ALPHA)]
                rows.append([r["id"], f(lc, 1), pp(bc["p"]), f(li, 1), pp(bi["p"]), lab])
            t.add(2, rows)
            t.check(rep, name)
            sent = json.loads(committed_json["p3-18-fresh-job.json"])["sentences"]
            missing = [x for x in sent if x not in md[name]]
            rep.compare(name + " (pre-registered sentences)", "all present", "all present" if not missing else
                        "missing from the write-up: " + " | ".join(missing), what=f"{len(sent)} sentences found verbatim")
        except Exception as e:  # noqa: BLE001
            rep.error(name, e)

        return rep.finish()
    finally:
        R.cleanup(tmp)


if __name__ == "__main__":
    R.main_guard(main)
