"""The work to be graded: short study write-ups, each with its data, for which a model writes a conclusion.

    python3 programs/self-grading/experiments/sg_items.py <items-seed>        -> data/sg-tasks.json

Each task is a small, made-up study (20 domains x 3 designs x 6 complications), with a result whose 95% interval is
computed from the drawn n and effect. A good conclusion states what the data show and no more: the design (randomised,
self-selected, before-after), the uncertainty, and the complication. A conclusion that claims more than that should get
a lower grade. The tasks are generated, not copied, so no grader has seen them, and they carry no real-world content
likely to be refused.

62 tasks are drawn: t01-t60 are the test set; p01-p02 are a pilot set, excluded from every test statistic, for the
design review's optional execution pilot (operators/design-review.md D6). The draw uses only the seed given, which is
the beacon seed of sg-b1 (purpose "items"), fixed after the pre-registration commit.
"""
import json
import math
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# (intervention, population, outcome, unit, baseline mean, outcome SD, decimals, site word)
DOMAINS = [
    ("a phonics reading app", "second-grade pupils", "reading score", "points on a 100-point test", 61, 14, 1, "school"),
    ("a magnesium sleep supplement", "adults who reported poor sleep", "total sleep time", "minutes per night", 362, 48, 0, "clinic"),
    ("a redesigned onboarding email", "new users of a budgeting app", "30-day retention", "percent of users", 41, 18, 1, "country"),
    ("a slow-release fertilizer", "tomato plots", "yield", "kg per plot", 23.5, 5.2, 1, "farm"),
    ("weekly peer tutoring", "ninth-grade algebra students", "end-of-term exam score", "points out of 100", 64, 15, 1, "school"),
    ("a 10-minute daily meditation app", "office workers", "wellbeing score", "points on a 50-point scale", 31, 7, 1, "company"),
    ("a new caching layer", "web servers", "throughput", "requests per second", 1840, 260, 0, "data centre"),
    ("text-message vaccination reminders", "parents of toddlers", "on-time vaccination", "percent of children", 72, 20, 1, "clinic"),
    ("a standing-desk programme", "call-centre staff", "calls handled per shift", "calls", 54, 9, 1, "call centre"),
    ("a probiotic yogurt", "adults over 70", "grip strength", "kg", 26.2, 6.1, 1, "care home"),
    ("a gamified physiotherapy app", "knee-surgery patients", "knee range of motion", "degrees", 104, 13, 1, "hospital"),
    ("a pricing-page redesign", "website visitors", "sign-up rate", "percent of visitors", 6.4, 3.1, 2, "market"),
    ("a cognitive-training game", "retirees", "memory test score", "points out of 50", 33, 6.5, 1, "town"),
    ("a free school breakfast", "primary-school pupils", "attendance", "days per 60-day term", 53.1, 4.2, 1, "school"),
    ("a new irrigation schedule", "vineyard rows", "grape yield", "kg per row", 412, 70, 0, "vineyard"),
    ("a code-review checklist", "software teams", "defects caught before release", "per 1,000 lines of code", 3.1, 1.2, 2, "company"),
    ("a nurse-led phone call after discharge", "heart-failure patients", "days at home in the next 90 days", "days", 78, 11, 1, "hospital"),
    ("a quieter classroom ventilation unit", "classrooms", "average reading-test score", "points out of 100", 66, 8, 1, "district"),
    ("a bike-lane extension", "city streets", "daily cyclist count", "cyclists per day", 310, 95, 0, "city"),
    ("a spaced-repetition flashcard app", "first-year medical students", "anatomy exam score", "points out of 100", 70, 11, 1, "university"),
]
DESIGNS = ["randomised", "self-selected", "before-after"]
COMPLICATIONS = ["none", "subgroup", "dropout", "many-outcomes", "single-site", "short-follow-up"]
NS = [14, 22, 35, 60, 110, 240, 600]
DELTAS = [0.0, 0.0, 0.12, 0.25, 0.45]          # true standardised effects; two zeros so about 40% have none
SUBGROUPS = ["women over 50", "the youngest third", "participants in the north", "those with the lowest baseline",
             "weekday participants", "first-time users"]


def fmt(x, d):
    return f"{x:,.{d}f}" if d else f"{round(x):,}"


def render(rng, k, tid):
    interv, pop, out, unit, base, sd, d, site = DOMAINS[k % len(DOMAINS)]
    design = rng.choice(DESIGNS)
    comp = rng.choice(COMPLICATIONS)
    n = rng.choice(NS)
    delta = rng.choice(DELTAS)
    se = sd * math.sqrt(2 / n) if design != "before-after" else sd * math.sqrt(2 / n) * 0.8
    diff = delta * sd + rng.gauss(0, se)
    lo, hi = diff - 1.96 * se, diff + 1.96 * se
    m0 = base + rng.gauss(0, sd * 0.05)
    m1 = m0 + diff
    if design == "randomised":
        lines = [f"Study: {pop} were randomly assigned either to {interv} or to carry on as usual.",
                 f"Groups: {interv} (n = {n}) and usual practice (n = {n})."]
        g1, g0 = interv, "usual practice"
    elif design == "self-selected":
        lines = [f"Study: {pop} chose for themselves whether to use {interv}; those who did were compared with those who did not.",
                 f"Groups: chose {interv} (n = {n}) and did not (n = {n})."]
        g1, g0 = f"chose {interv}", "did not"
    else:
        lines = [f"Study: the outcome was measured in the same {n} {pop} before and after {interv} was introduced. There was no comparison group.",
                 f"Measurements: before (n = {n}) and after (n = {n})."]
        g1, g0 = "after", "before"
    lines.append(f"Outcome: {out}, in {unit} (higher is better).")
    lines.append(f"Result: mean {fmt(m1, d)} ({g1}) against {fmt(m0, d)} ({g0}); difference {fmt(diff, d)} "
                 f"(95% interval {fmt(lo, d)} to {fmt(hi, d)}).")
    sig = lo > 0 or hi < 0
    if comp == "subgroup":
        lines.append(f"Six subgroups were also examined; the difference was statistically significant (p = 0.03) only among {rng.choice(SUBGROUPS)}.")
    elif comp == "dropout":
        a, b = rng.choice([(31, 9), (26, 12), (34, 8)])
        lines.append(f"Before the outcome was measured, {a}% of the {g1} group and {b}% of the {g0} group dropped out.")
    elif comp == "many-outcomes":
        lines.append("This was one of nine outcomes measured; it is the only one with p < 0.05." if sig else
                     "This was one of nine outcomes measured; none of the nine reached p < 0.05.")
    elif comp == "single-site":
        lines.append(f"Everyone in the study came from a single {site}.")
    elif comp == "short-follow-up":
        lines.append("The outcome was measured once, one week after the start.")
    return {"id": tid, "domain": k % len(DOMAINS), "design": design, "complication": comp, "n_per_group": n,
            "true_delta": delta, "diff": round(diff, 4), "ci": [round(lo, 4), round(hi, 4)], "ci_excludes_0": sig,
            "study": "\n".join(lines)}


def main():
    seed = int(sys.argv[1])
    rng = random.Random(seed)
    order = list(range(60)) + [rng.randrange(20), rng.randrange(20)]   # 3 tasks per domain on the test set
    rng.shuffle(order[:60])
    tasks = [render(rng, k, f"t{i + 1:02d}") for i, k in enumerate(order[:60])]
    tasks += [render(rng, k, f"p{i + 1:02d}") for i, k in enumerate(order[60:])]
    out = {"seed": seed, "generator": "experiments/sg_items.py", "n_test": 60, "n_pilot": 2, "tasks": tasks}
    (ROOT / "data").mkdir(exist_ok=True)
    (ROOT / "data" / "sg-tasks.json").write_text(json.dumps(out, indent=1))
    print(f"wrote data/sg-tasks.json: {len(tasks)} tasks (seed {seed})")


if __name__ == "__main__":
    main()
