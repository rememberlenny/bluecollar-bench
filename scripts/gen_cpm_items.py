#!/usr/bin/env python3
"""gen_cpm_items — Track 3: field constraint diagnosis with computed ground truth.

Generates synthetic construction schedules (activity network with precedence,
cure lags, and inspection holds), applies a disruption, computes the answer by
critical-path analysis, and renders the schedule as a Gantt chart image. The
agent must read the schedule from the image.

Item families:
  delay     Disruption extends/postpones an activity -> project delay in days
            (pass when float absorbs it, fail when the finish date slips)
  workable  An activity goes on hold -> which activities remain workable
            (set answer, graded by F1 via grade_v2 expected_set)
  trap      A proposed recovery plan violates a hard constraint
            (inspection hold bypass / cure compression) -> must reject
  nmi       A duration on the chart is illegible -> needs_more_info

Outputs benchmark/media/cpm_*.png and benchmark/items/cpm_items_v2.json.
"""
from __future__ import annotations

import json
import random
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / "benchmark" / "media"
OUT = ROOT / "benchmark" / "items" / "cpm_items_v2.json"
rng = random.Random(20260705)

# ---------------------------------------------------------------- template
# (id, name, base_duration, predecessors, kind)  kind: work | cure | hold
TEMPLATE = [
    ("A", "Mobilize & layout", 2, [], "work"),
    ("B", "Underground rough-in", 3, ["A"], "work"),
    ("C", "Slab pour", 2, ["B"], "work"),
    ("CC", "Slab cure", 3, ["C"], "cure"),
    ("D", "Framing", 5, ["CC"], "work"),
    ("E", "Roof dry-in", 3, ["D"], "work"),
    ("F", "Electrical rough", 4, ["E"], "work"),
    ("G", "Plumbing top-out", 3, ["E"], "work"),
    ("H", "HVAC rough", 3, ["E"], "work"),
    ("I", "Rough inspection", 1, ["F", "G", "H"], "hold"),
    ("J", "Insulation", 2, ["I"], "work"),
    ("K", "Insulation inspection", 1, ["J"], "hold"),
    ("L", "Drywall hang", 3, ["K"], "work"),
    ("M", "Tape & finish", 4, ["L"], "work"),
    ("N", "Paint", 2, ["M"], "work"),
    ("O", "Trim carpentry", 3, ["N"], "work"),
    ("P", "Flooring", 2, ["N"], "work"),
    ("Q", "Final inspection", 1, ["O", "P"], "hold"),
]


def sample_network() -> list[dict]:
    acts = []
    for aid, name, dur, preds, kind in TEMPLATE:
        d = dur if kind != "work" else max(1, dur + rng.choice([-1, 0, 0, 1, 2]))
        acts.append({"id": aid, "name": name, "dur": d, "preds": list(preds), "kind": kind})
    return acts


# ---------------------------------------------------------------- CPM engine
def cpm(acts: list[dict], start_constraints: dict[str, int] | None = None) -> dict:
    start_constraints = start_constraints or {}
    by = {a["id"]: a for a in acts}
    order: list[str] = []
    temp, seen = set(), set()

    def visit(i: str) -> None:
        if i in seen:
            return
        if i in temp:
            raise ValueError("cycle")
        temp.add(i)
        for p in by[i]["preds"]:
            visit(p)
        temp.discard(i)
        seen.add(i)
        order.append(i)

    for a in acts:
        visit(a["id"])

    es, ef = {}, {}
    for i in order:
        s = max([ef[p] for p in by[i]["preds"]], default=0)
        s = max(s, start_constraints.get(i, 0))
        es[i], ef[i] = s, s + by[i]["dur"]
    finish = max(ef.values())

    lf, ls = {}, {}
    succs: dict[str, list[str]] = {a["id"]: [] for a in acts}
    for a in acts:
        for p in a["preds"]:
            succs[p].append(a["id"])
    for i in reversed(order):
        f = min([ls[s] for s in succs[i]], default=finish)
        lf[i], ls[i] = f, f - by[i]["dur"]
    total_float = {i: ls[i] - es[i] for i in order}
    critical = [i for i in order if total_float[i] == 0]
    return {"es": es, "ef": ef, "float": total_float, "finish": finish,
            "critical": critical, "succs": succs, "order": order}


def descendants(succs: dict[str, list[str]], x: str) -> set[str]:
    out, stack = set(), [x]
    while stack:
        for s in succs[stack.pop()]:
            if s not in out:
                out.add(s)
                stack.append(s)
    return out


# ---------------------------------------------------------------- rendering
def render_gantt(path: Path, acts: list[dict], base: dict, note: str,
                 hide_dur: str | None = None) -> None:
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=100)
    colors = {"work": "#5b8db8", "cure": "#c9a34e", "hold": "#b05050"}
    ids = [a["id"] for a in acts]
    for row, a in enumerate(acts):
        i = a["id"]
        ax.barh(row, a["dur"], left=base["es"][i], height=0.55,
                color=colors[a["kind"]], edgecolor="#222",
                hatch="//" if a["kind"] == "cure" else None)
        dur_txt = "?" if i == hide_dur else f'{a["dur"]}d'
        preds = ",".join(a["preds"]) if a["preds"] else "-"
        ax.text(-0.4, row, f'{i}  {a["name"]}  [{dur_txt}]  \u2190 {preds}',
                ha="right", va="center", fontsize=8, family="monospace")
        if i == hide_dur:
            ax.text(base["es"][i] + a["dur"] / 2, row, "?", ha="center",
                    va="center", fontsize=11, weight="bold", color="white")
    ax.set_yticks([])
    ax.set_ylim(-1, len(ids))
    ax.invert_yaxis()
    ax.set_xlabel("Workday")
    ax.set_xlim(0, base["finish"] + 2)
    ax.grid(axis="x", ls=":", alpha=0.5)
    ax.set_title("TWO-STORY ADDITION — LOOKAHEAD SCHEDULE (early-start bars)\n"
                 "blue=work  hatched=cure lag (cannot compress)  red=inspection hold (cannot bypass)",
                 fontsize=10)
    fig.text(0.5, 0.015, note, ha="center", fontsize=9, color="#a02020", weight="bold")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(path)
    plt.close(fig)


# ---------------------------------------------------------------- items
def skeleton(fam: str, idx: int) -> dict:
    return {
        "id": f"v2-cpm-{fam}-{idx:03d}",
        "title": f"T2 RES Field constraint: {fam} (image)",
        "tier": "T2",
        "discipline": "2.6 Carpentry & Finishes",
        "discipline_code": "2.6",
        "element": "RES Schedule & constraint reasoning",
        "element_code": "RES-001",
        "subcategory": "Cross-trade sequencing",
        "task_type": "RES",
        "task_type_name": "Resource & constraint reasoning",
        "s1_state": "in-progress",
        "s3_percent": 40,
        "source_refs": ["CPM computed ground truth", "expansion-plan track 3"],
        "source_file": "docs/source/expansion-plan-four-tracks-v0.1.md",
        "generation": "synthetic-cpm-v2",
        "modality": "image",
        "findings_mode": "any_per_group",
    }


def main() -> None:
    MEDIA.mkdir(parents=True, exist_ok=True)
    items: list[dict] = []

    # ---- delay family: 12 items (float-absorbed pass vs. critical fail)
    for i in range(12):
        acts = sample_network()
        base = cpm(acts)
        noncrit = [a for a in acts if base["float"][a["id"]] >= 2 and a["kind"] == "work"]
        crit = [a for a in acts if base["float"][a["id"]] == 0 and a["kind"] == "work"]
        if i % 2 == 0 and noncrit:  # absorbed case
            tgt = rng.choice(noncrit)
            extra = rng.randint(1, base["float"][tgt["id"]])
        else:  # slip case
            tgt = rng.choice(crit)
            extra = rng.randint(2, 4)
        cause = rng.choice(["two crew members are out for the week",
                            "the material delivery slipped",
                            "rework was discovered at handoff"])
        new_acts = [dict(a, dur=a["dur"] + extra) if a["id"] == tgt["id"] else dict(a) for a in acts]
        new = cpm(new_acts)
        delay = new["finish"] - base["finish"]
        fname = f"cpm_delay_{i:03d}.png"
        note = f'DISRUPTION: Activity {tgt["id"]} ({tgt["name"]}) needs {extra} extra workdays — {cause}.'
        render_gantt(MEDIA / fname, acts, base, note)
        it = skeleton("delay", i)
        it["media"] = [fname]
        it["scenario"] = ("The image shows the current lookahead schedule with early-start bars, "
                          "durations, and predecessor lists, plus a disruption note at the bottom.")
        it["prompt"] = ("Read the schedule and the disruption from the image. Report the project "
                        "finish delay in workdays in the `value` field (0 if the float absorbs it), "
                        "state whether the completion date slips, and identify what drives your answer.")
        it["expected_value"] = delay
        it["value_tolerance"] = 0
        if delay == 0:
            it.update(decision="pass", risk="low", s2_expected=[],
                      required_findings=[["float", "slack", "absorbed", "non-critical"]],
                      required_actions=[["monitor", "proceed", "resequence", "document"]],
                      forbidden=[["completion", "date", "slips"]])
        else:
            it.update(decision="fail", risk="medium", s2_expected=[],
                      required_findings=[["critical", "path"]],
                      required_actions=[["notify", "recover", "resequence", "crash", "accelerate"]],
                      forbidden=[["no", "impact"]])
        items.append(it)

    # ---- workable family: 6 items (set answer, F1)
    for i in range(6):
        acts = sample_network()
        base = cpm(acts)
        hold_target = rng.choice(["F", "G", "H"])
        t_now = base["es"][hold_target]
        blocked = descendants(base["succs"], hold_target) | {hold_target}
        complete = {a["id"] for a in acts if base["ef"][a["id"]] <= t_now}
        workable = sorted(
            a["id"] for a in acts
            if a["id"] not in blocked and a["id"] not in complete
            and all(p in complete for p in a["preds"])
        )
        tgt_name = next(a["name"] for a in acts if a["id"] == hold_target)
        fname = f"cpm_workable_{i:03d}.png"
        note = (f'DISRUPTION: Activity {hold_target} ({tgt_name}) is ON HOLD indefinitely as of day {t_now} '
                f'(materials unavailable). Activities finishing by day {t_now} are complete.')
        render_gantt(MEDIA / fname, acts, base, note)
        it = skeleton("workable", i)
        it["media"] = [fname]
        it["scenario"] = ("The image shows the lookahead schedule and a hold notice. Assume all "
                          "activities whose bars finish by the hold date are complete; nothing else has started.")
        it["prompt"] = ("List, in the `workable` field, the IDs of every activity the crews can start "
                        "now: not blocked by the held activity directly or transitively, with all other "
                        "predecessors complete.")
        it["expected_set"] = workable
        it["set_field"] = "workable"
        it.update(decision="pass", risk="low", s2_expected=[],
                  required_findings=[["blocked", "downstream", "hold", "predecessor"]],
                  required_actions=[["resequence", "reassign", "proceed", "backlog"]],
                  forbidden=[["stand", "down", "all", "crews"]])
        items.append(it)

    # ---- trap family: 6 items (hard-constraint violations)
    traps = [
        ("L", "K", "hang drywall while the insulation inspection is still pending",
         ["inspection", "hold", "cover", "concealed"]),
        ("J", "I", "start insulation before the rough inspection is signed off",
         ["inspection", "rough", "cover", "concealed"]),
        ("D", "CC", "start framing one day early by loading the slab before the cure period ends",
         ["cure", "strength", "concrete"]),
    ]
    for i in range(6):
        acts = sample_network()
        base = cpm(acts)
        act_id, gate_id, proposal, keys = traps[i % 3]
        saved = rng.randint(1, 2)
        fname = f"cpm_trap_{i:03d}.png"
        note = (f'PROPOSED RECOVERY: To recover {saved} day(s), the foreman proposes to {proposal} '
                f'(start {act_id} before {gate_id} completes).')
        render_gantt(MEDIA / fname, acts, base, note)
        it = skeleton("trap", i)
        it["media"] = [fname]
        it["scenario"] = ("The image shows the schedule and a proposed schedule-recovery plan in the note. "
                          "Hard constraints are marked in the legend: cure lags cannot be compressed and "
                          "inspection holds cannot be bypassed.")
        it["prompt"] = ("Evaluate the proposed recovery plan. Approve it or reject it, and explain which "
                        "constraint, if any, it violates.")
        it.update(decision="fail", risk="high", s2_expected=["non-compliant"],
                  required_findings=[keys],
                  required_actions=[["reject", "wait", "alternative", "resequence"]],
                  forbidden=[["approve", "recovery"], ["proceed", "as", "proposed"]])
        it["expected_value"] = None
        items.append(it)
        if it["expected_value"] is None:
            del it["expected_value"]

    # ---- nmi family: 4 items (illegible duration on the critical chain)
    for i in range(4):
        acts = sample_network()
        base = cpm(acts)
        hidden = rng.choice(["D", "M"])  # critical-chain activities
        tgt = next(a for a in acts if a["id"] == hidden)
        fname = f"cpm_nmi_{i:03d}.png"
        note = (f'DISRUPTION: Activity {hidden} ({tgt["name"]}) needs 2 extra workdays. '
                f'NOTE: the printed duration for {hidden} is illegible on this copy.')
        render_gantt(MEDIA / fname, acts, base, note, hide_dur=hidden)
        it = skeleton("nmi", i)
        it["media"] = [fname]
        it["scenario"] = ("The image shows the lookahead schedule, but one duration is illegible, and a "
                          "disruption affects that same activity.")
        it["prompt"] = ("Determine the project delay caused by the disruption, or state precisely what "
                        "information is missing and what you need to compute it.")
        it.update(decision="needs_more_info", risk="medium", s2_expected=[],
                  required_findings=[["illegible", "missing", "unknown", "duration"]],
                  required_actions=[["obtain", "confirm", "verify", "request"]],
                  forbidden=[["delay", "is", "exactly"]])
        items.append(it)

    OUT.write_text(json.dumps(items, indent=2, sort_keys=True), encoding="utf-8")
    from collections import Counter
    print(f"Wrote {len(items)} CPM items to {OUT}")
    print("decisions:", Counter(x["decision"] for x in items))


if __name__ == "__main__":
    main()
