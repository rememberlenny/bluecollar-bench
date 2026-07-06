#!/usr/bin/env python3
"""Build a browsable synthesis wiki for a collected benchmark run."""

from __future__ import annotations

import argparse
import html
import json
import statistics
import tomllib
from collections import Counter, defaultdict
from pathlib import Path


DEFAULT_RUN = Path("benchmark/runs/gpt55_full_20260705_5b2c706")

TASK_TYPE_LABELS = {
    "CC": "Code/spec compliance",
    "DOC": "Document interpretation",
    "FD": "Fault diagnosis",
    "HAZ": "Hazard spotting",
    "ID": "Identification",
    "ME": "Measurement & estimation",
    "PA": "Progress assessment",
    "RES": "Resource & constraint reasoning",
    "SEQ": "Procedure sequencing",
    "TRD": "Tradeoff judgment",
    "TS": "Tool & material selection",
}

TASK_TYPE_NOTES = {
    "TS": (
        "Works well when the answer is a concrete selection: choose the right "
        "device, material, or tool and reject the unsafe substitute."
    ),
    "HAZ": (
        "One of the strongest formats. The model usually recognizes familiar "
        "critical hazards and maps them to a fail decision."
    ),
    "SEQ": (
        "Strong overall because procedure order gives the model a structured "
        "reasoning path. The misses are usually omitted lockout, verification, "
        "or prerequisite steps."
    ),
    "RES": (
        "Usually good on schedule/resource images when the blocking constraint "
        "is visually explicit, but brittle on a few CPM delay cases."
    ),
    "PA": (
        "Generally mid-to-strong. The model can assess progress when the "
        "unfinished state is explicit, but loses detail when the punch item is "
        "subtle."
    ),
    "TRD": (
        "Mixed and small-sample. The model handles many obvious safety "
        "tradeoffs, but struggles when the task asks for judgment around a "
        "marginal exception."
    ),
    "CC": (
        "Mixed. The model can apply broad code/spec rules, but repeated "
        "electrical detail traps caused several of the lowest scores."
    ),
    "ME": (
        "Bimodal. Visual measurements can be excellent when scale and threshold "
        "are clear, but critical sling/load measurements produced hard failures."
    ),
    "DOC": (
        "Moderate. Image document reads were often clean, while dense electrical "
        "document interpretation was weaker."
    ),
    "FD": (
        "High variance. The model can identify many visual and mechanical "
        "faults, but audio diagnosis and some text-only troubleshooting cases "
        "are major failure modes."
    ),
    "ID": (
        "The weakest task type by mean reward. Identification tasks demand "
        "specific component/defect naming, and partial recognition often does "
        "not recover enough reward."
    ),
}

CONCLUSIONS = [
    (
        "Task format matters more than nominal tier.",
        "Tier means were tightly clustered, while task-type means ranged from "
        "0.709 for ID to 0.841 for TS. Treat the benchmark as a test of task "
        "shape, not just task difficulty.",
    ),
    (
        "The model is good at the top-level call but weaker at the work plan.",
        "Schema, decision, and safety-gate scores were high; actions and the "
        "final-state component were the main drag. In practice it often knows "
        "whether to pass/fail but is less consistent about the concrete next "
        "steps.",
    ),
    (
        "Structured safety recognition is a strength.",
        "HAZ, SEQ, and TS were among the best task types. These formats reward "
        "standard jobsite reasoning: identify the hazard, sequence the control, "
        "or choose the right tool/material.",
    ),
    (
        "Precise identification and diagnosis are the main weakness.",
        "ID was the lowest task type, FD had the most low-score items, and "
        "audio FD had the highest low-score rate. The model is much less "
        "reliable when it must name the exact component, sound source, or "
        "defect from sparse cues.",
    ),
    (
        "Image results are strong but not uniformly safe.",
        "Image tasks had the best mean reward and many perfect scores, but "
        "critical sling/load and CPM delay tasks also produced zero-score "
        "false-pass cases. The visual modality is powerful, not automatically "
        "safe.",
    ),
    (
        "Electrical detail remains the highest-priority domain weakness.",
        "Electrical had the lowest discipline mean and the largest count of "
        "low-score tasks. Terminations/splices and motor-circuit document cases "
        "are especially useful regression examples.",
    ),
]


def fmt(value: float) -> str:
    return f"{value:.3f}"


def pct(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "0%"
    return f"{100 * numerator / denominator:.1f}%"


def rel_task_link(task: str) -> str:
    return f"[`{task}`](../../../../tasks/{task}/task.toml)"


def load_rows(run_dir: Path) -> list[dict]:
    metrics_path = run_dir / "metrics.json"
    with metrics_path.open() as f:
        rows = json.load(f)["rows"]
    for row in rows:
        row["meta"] = load_task_meta(Path("tasks") / row["task"] / "task.toml")
    return rows


def load_task_meta(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open("rb") as f:
        data = tomllib.load(f)
    task = data.get("task", {})
    metadata = data.get("metadata", {})
    return {
        "description": task.get("description", ""),
        "discipline_name": metadata.get("discipline", ""),
        "element": metadata.get("element", ""),
        "expected_decision": metadata.get("expected_decision", ""),
        "expected_risk": metadata.get("expected_risk", ""),
        "task_type_name": metadata.get("task_type_name", ""),
        "source_refs": ", ".join(metadata.get("source_refs", [])),
    }


def group_stats(rows: list[dict], key: str) -> list[dict]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        groups[str(row[key])].append(row)
    stats = []
    for group, group_rows in groups.items():
        rewards = [row["reward"] for row in group_rows]
        low = sum(row["reward"] <= 0.5 for row in group_rows)
        high = sum(row["reward"] >= 0.9 for row in group_rows)
        stats.append(
            {
                "group": group,
                "n": len(group_rows),
                "mean": statistics.fmean(rewards),
                "low": low,
                "high": high,
                "rows": group_rows,
            }
        )
    return sorted(stats, key=lambda item: (item["mean"], item["group"]))


def metric_mean(rows: list[dict], key: str) -> float:
    return statistics.fmean(row[key] for row in rows)


def example_table(rows: list[dict], heading: str | None = None, limit: int = 5) -> str:
    lines = []
    if heading:
        lines.append(f"#### {heading}")
        lines.append("")
    lines.append(
        "| task | reward | type | modality | tier | expected | why it matters |"
    )
    lines.append("|---|---:|---|---|---|---|---|")
    for row in rows[:limit]:
        meta = row["meta"]
        expected = (
            f"{meta.get('expected_decision', '')}/{meta.get('expected_risk', '')}"
        ).strip("/")
        why = meta.get("element") or meta.get("description") or row["task"]
        lines.append(
            "| "
            + " | ".join(
                [
                    rel_task_link(row["task"]),
                    fmt(row["reward"]),
                    row["task_type"],
                    row["modality"],
                    row["tier"],
                    expected,
                    why.replace("|", "/"),
                ]
            )
            + " |"
        )
    return "\n".join(lines)


def stats_table(stats: list[dict], label: str = "group") -> str:
    lines = [
        f"| {label} | n | mean reward | <=0.50 | >=0.90 |",
        "|---|---:|---:|---:|---:|",
    ]
    for item in stats:
        lines.append(
            f"| {item['group']} | {item['n']} | {fmt(item['mean'])} | "
            f"{item['low']} ({pct(item['low'], item['n'])}) | "
            f"{item['high']} ({pct(item['high'], item['n'])}) |"
        )
    return "\n".join(lines)


def by_reward(rows: list[dict], reverse: bool = False) -> list[dict]:
    return sorted(rows, key=lambda row: (row["reward"], row["task"]), reverse=reverse)


def write_page(path: Path, title: str, body: str) -> None:
    path.write_text(f"# {title}\n\n{body.rstrip()}\n", encoding="utf-8")


def build_readme(run_dir: Path, rows: list[dict]) -> str:
    manifest = json.loads((run_dir / "manifest.json").read_text())
    saturated = sum(row["reward"] >= 0.95 for row in rows)
    floored = sum(row["reward"] <= 0.05 for row in rows)
    dangerous = sum(row["dangerous_false_pass"] < 1.0 for row in rows)
    alarmist = sum(row["alarmist_false_fail"] < 1.0 for row in rows)
    mean_reward = metric_mean(rows, "reward")

    lines = [
        "This wiki synthesizes the `gpt55_full_20260705_5b2c706` full-suite run.",
        "It is meant to be read as an interpretation layer above the raw metrics, plots, and per-task artifacts.",
        "",
        "## Navigation",
        "",
        "- [Task type breakdown](task-types.md)",
        "- [Modality and media breakdown](modality-and-media.md)",
        "- [Discipline and tier breakdown](discipline-and-tier.md)",
        "- [Failure patterns and safety gates](failure-patterns.md)",
        "- [Example index](example-index.md)",
        "- [Plots dashboard](../plots/index.html)",
        "- [Original analysis](../analysis.md)",
        "",
        "## At a glance",
        "",
        "| metric | value |",
        "|---|---:|",
        f"| tasks scored | {len(rows)} |",
        f"| mean reward | {fmt(mean_reward)} |",
        f"| saturated tasks, reward >= 0.95 | {saturated} ({pct(saturated, len(rows))}) |",
        f"| floored tasks, reward <= 0.05 | {floored} ({pct(floored, len(rows))}) |",
        f"| dangerous false pass gate hits | {dangerous} |",
        f"| alarmist false fail gate hits | {alarmist} |",
        f"| catalog sha256 | `{manifest['catalog_sha256_16']}` |",
        "",
        "## Component diagnosis",
        "",
        "| component | mean | interpretation |",
        "|---|---:|---|",
        f"| schema | {fmt(metric_mean(rows, 'schema'))} | Output shape is not the problem. |",
        f"| decision | {fmt(metric_mean(rows, 'decision'))} | Top-level pass/fail/NMI decisions are usually right. |",
        f"| risk | {fmt(metric_mean(rows, 'risk'))} | Risk level is weaker than decision, especially in false-pass cases. |",
        f"| findings | {fmt(metric_mean(rows, 'findings'))} | The model often notices relevant facts. |",
        f"| actions | {fmt(metric_mean(rows, 'actions'))} | The largest actionable gap is specifying the right next steps. |",
        f"| s3 | {fmt(metric_mean(rows, 's3'))} | Final-state/completion evidence is rarely captured completely. |",
        "",
        "## Important conclusions",
        "",
    ]
    for index, (title, text) in enumerate(CONCLUSIONS, start=1):
        lines.append(f"{index}. **{title}** {text}")

    lines += [
        "",
        "## Representative examples",
        "",
        example_table(by_reward(rows, reverse=True), "Strongest examples", 6),
        "",
        example_table(by_reward(rows), "Weakest examples", 8),
    ]
    return "\n".join(lines)


def build_task_types(rows: list[dict]) -> str:
    stats = group_stats(rows, "task_type")
    lines = [
        "[Back to wiki index](README.md)",
        "",
        "Task type is the clearest performance separator in this run.",
        "The model succeeds most on structured safety, sequencing, and selection tasks; it fails most on exact identification and high-variance diagnosis.",
        "",
        stats_table(stats, "task type"),
        "",
    ]

    for stat in sorted(stats, key=lambda item: item["mean"], reverse=True):
        task_type = stat["group"]
        label = TASK_TYPE_LABELS.get(task_type, task_type)
        group_rows = stat["rows"]
        lines += [
            f"## {task_type}: {label}",
            "",
            f"Mean reward: **{fmt(stat['mean'])}** over **{stat['n']}** tasks. "
            f"Low-score rate: **{pct(stat['low'], stat['n'])}**. "
            f"High-score rate: **{pct(stat['high'], stat['n'])}**.",
            "",
            TASK_TYPE_NOTES.get(task_type, "No manual note available."),
            "",
            example_table(by_reward(group_rows, reverse=True), "Successful examples", 4),
            "",
            example_table(by_reward(group_rows), "Failure examples", 4),
            "",
        ]
    return "\n".join(lines)


def build_modality(rows: list[dict]) -> str:
    stats = group_stats(rows, "modality")
    audio = [row for row in rows if row["modality"] == "audio"]
    image = [row for row in rows if row["modality"] == "image"]
    text = [row for row in rows if row["modality"] == "text"]

    lines = [
        "[Back to wiki index](README.md)",
        "",
        "The modality story is not simply text versus media.",
        "Image tasks were the best group on average, but the severe misses were also visually grounded.",
        "Audio was the most volatile modality.",
        "",
        stats_table(stats, "modality"),
        "",
        "## Image",
        "",
        "Image tasks had the highest mean and many perfect scores, especially gas-meter reads, HVAC-R micron-gauge examples, rotor measurements, and several CPM constraints. The weak side is critical measurement and scheduling interpretation, where the wrong final decision can zero the task.",
        "",
        example_table(by_reward(image, reverse=True), "Image successes", 6),
        "",
        example_table(by_reward(image), "Image failures", 6),
        "",
        "## Audio",
        "",
        "Audio tasks had the highest low-score rate. Bearing and engine examples often scored well, but hum/hammer items show that sound-source and low-risk/pass judgments are brittle.",
        "",
        example_table(by_reward(audio, reverse=True), "Audio successes", 6),
        "",
        example_table(by_reward(audio), "Audio failures", 6),
        "",
        "## Text",
        "",
        "Text tasks are broad and therefore average out near the overall mean. The strongest text examples are structured hazard, sequence, and tool-selection tasks. The weakest are detailed electrical code/spec, identification, and document interpretation cases.",
        "",
        example_table(by_reward(text, reverse=True), "Text successes", 6),
        "",
        example_table(by_reward(text), "Text failures", 6),
    ]
    return "\n".join(lines)


def build_discipline_tier(rows: list[dict]) -> str:
    discipline_stats = group_stats(rows, "discipline")
    tier_stats = group_stats(rows, "tier")
    discipline_names = {}
    for row in rows:
        if row["meta"].get("discipline_name"):
            discipline_names[row["discipline"]] = row["meta"]["discipline_name"]

    lines = [
        "[Back to wiki index](README.md)",
        "",
        "Discipline explains more than tier. Electrical was the weakest major discipline, while safety/rigging was the strongest. Tier means were close together and not monotonic.",
        "",
        "## Discipline summary",
        "",
        "| discipline | name | n | mean reward | <=0.50 | >=0.90 |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for item in discipline_stats:
        name = discipline_names.get(item["group"], "")
        lines.append(
            f"| {item['group']} | {name} | {item['n']} | {fmt(item['mean'])} | "
            f"{item['low']} ({pct(item['low'], item['n'])}) | "
            f"{item['high']} ({pct(item['high'], item['n'])}) |"
        )

    lines += [
        "",
        "## Tier summary",
        "",
        stats_table(tier_stats, "tier"),
        "",
        "## What this means",
        "",
        "- **Electrical is the first regression target.** It had the lowest mean and the most low-score tasks, including repeated terminations/splices failures.",
        "- **Safety & rigging is a relative strength.** It had the best discipline mean and many high-scoring HAZ/TS examples.",
        "- **Tier alone is a poor predictor.** T4 was the strongest tier by mean, while T2/T5/T3 were close together. Future analysis should stratify by task type before drawing conclusions from tier.",
        "",
    ]

    for item in discipline_stats:
        group_rows = item["rows"]
        name = discipline_names.get(item["group"], item["group"])
        lines += [
            f"## {item['group']}: {name}",
            "",
            f"Mean reward: **{fmt(item['mean'])}** over **{item['n']}** tasks.",
            "",
            example_table(by_reward(group_rows, reverse=True), "Success examples", 3),
            "",
            example_table(by_reward(group_rows), "Failure examples", 3),
            "",
        ]
    return "\n".join(lines)


def build_failure_patterns(rows: list[dict]) -> str:
    dangerous = [row for row in rows if row["dangerous_false_pass"] < 1.0]
    alarmist = [row for row in rows if row["alarmist_false_fail"] < 1.0]
    low = [row for row in rows if row["reward"] <= 0.5]
    low_by_type = Counter(row["task_type"] for row in low)
    low_by_modality = Counter(row["modality"] for row in low)

    lines = [
        "[Back to wiki index](README.md)",
        "",
        "The main failure modes are clustered and therefore actionable.",
        "",
        "## Failure pattern summary",
        "",
        "| pattern | evidence | conclusion |",
        "|---|---|---|",
        f"| Exact identification/diagnosis | FD contributed {low_by_type['FD']} low-score tasks and ID contributed {low_by_type['ID']}. | Add or emphasize exact component, defect, and source-name checks. |",
        f"| Audio brittleness | Audio had {low_by_modality['audio']} low-score tasks out of {sum(row['modality'] == 'audio' for row in rows)}. | Treat audio FD as a separate benchmark capability, not just another FD variant. |",
        f"| Electrical code/detail traps | Discipline 2.1 had {sum(row['discipline'] == '2.1' and row['reward'] <= 0.5 for row in rows)} low-score tasks. | Electrical detail cases should be kept as regression anchors. |",
        f"| Critical visual false passes | {len(dangerous)} dangerous false pass gate hits. | Image strength does not eliminate safety-critical visual misses. |",
        f"| Over-failing safe audio cases | {len(alarmist)} alarmist false fail gate hits. | Some low-risk/pass sound cases are incorrectly treated as unsafe. |",
        "",
        "## Dangerous false pass examples",
        "",
        "These are the highest-priority review items because the expected answer is unsafe/fail but the model missed the final safety call.",
        "",
        example_table(by_reward(dangerous), None, len(dangerous)),
        "",
        "## Alarmist false fail examples",
        "",
        "These are safe/pass items that the model treated too harshly, all from audio in this run.",
        "",
        example_table(by_reward(alarmist), None, len(alarmist)),
        "",
        "## Lowest-score cluster examples",
        "",
        example_table(by_reward(rows), None, 20),
    ]
    return "\n".join(lines)


def build_example_index(rows: list[dict]) -> str:
    lines = [
        "[Back to wiki index](README.md)",
        "",
        "This page is a quick lookup for concrete examples mentioned across the synthesis.",
        "",
        "## Top-scoring examples",
        "",
        example_table(by_reward(rows, reverse=True), None, 25),
        "",
        "## Bottom-scoring examples",
        "",
        example_table(by_reward(rows), None, 25),
        "",
        "## Most useful regression examples",
        "",
        "These examples cover distinct weakness families and should be kept in view when testing future changes.",
        "",
    ]

    regression_tasks = [
        "t1-e-303-cc-terminations-splices",
        "t2-e-303-cc-terminations-splices",
        "t5-e-105-doc-motor-circuits-disconnects",
        "t2-e-602-id-equipment-bonding",
        "v2-audio-hammer-000",
        "v2-audio-hum-002",
        "v2-cpm-delay-001",
        "v2-media-sling-004",
        "v2-trd-s302-t1-wind-pick",
        "t5-e-105-ts-motor-circuits-disconnects",
        "t3-c-101-haz-form-build-bracing",
        "t5-m-101-seq-bf-005-baseplates-anchor-bolts",
    ]
    row_by_task = {row["task"]: row for row in rows}
    selected = [row_by_task[task] for task in regression_tasks if task in row_by_task]
    lines.append(example_table(selected, None, len(selected)))
    return "\n".join(lines)


def build_html_index(wiki_dir: Path, readme_body: str) -> None:
    cards = [
        ("Task Types", "task-types.md", "Which task formats succeed or fail."),
        ("Modality", "modality-and-media.md", "Text, image, and audio patterns."),
        ("Disciplines", "discipline-and-tier.md", "Domain and tier differences."),
        ("Failures", "failure-patterns.md", "Safety gates and low-score clusters."),
        ("Examples", "example-index.md", "Concrete task links for review."),
        ("Plots", "../plots/index.html", "The chart dashboard."),
    ]
    html_cards = "\n".join(
        f'<a class="card" href="{href}"><strong>{html.escape(title)}</strong>'
        f"<span>{html.escape(desc)}</span></a>"
        for title, href, desc in cards
    )
    body = html.escape(readme_body.split("## Component diagnosis")[0])
    body = body.replace("\n", "<br>\n")
    wiki_dir.joinpath("index.html").write_text(
        f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>gpt55 full suite synthesis wiki</title>
  <style>
    body {{ margin: 0; font-family: system-ui, sans-serif; color: #24313a; background: #f3f6f8; }}
    main {{ max-width: 1060px; margin: 0 auto; padding: 32px 20px 48px; }}
    h1 {{ margin: 0 0 8px; font-size: 30px; }}
    .intro {{ margin: 0 0 24px; color: #53636f; line-height: 1.6; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; }}
    .card {{ display: block; padding: 16px; border: 1px solid #d8e0e6; border-radius: 8px; background: #fff; color: inherit; text-decoration: none; }}
    .card strong {{ display: block; margin-bottom: 6px; }}
    .card span {{ color: #667783; font-size: 14px; line-height: 1.4; }}
    .note {{ margin-top: 24px; padding: 16px; background: #fff; border: 1px solid #d8e0e6; border-radius: 8px; font-size: 14px; line-height: 1.5; }}
  </style>
</head>
<body>
  <main>
    <h1>gpt55 full suite synthesis wiki</h1>
    <p class="intro">A browsable interpretation layer for the full benchmark run.</p>
    <section class="grid">
      {html_cards}
    </section>
    <section class="note">{body}</section>
  </main>
</body>
</html>
""",
        encoding="utf-8",
    )


def build_wiki(run_dir: Path) -> Path:
    rows = load_rows(run_dir)
    wiki_dir = run_dir / "wiki"
    wiki_dir.mkdir(parents=True, exist_ok=True)

    readme = build_readme(run_dir, rows)
    pages = {
        "README.md": ("Full Suite Synthesis Wiki", readme),
        "task-types.md": ("Task Type Breakdown", build_task_types(rows)),
        "modality-and-media.md": ("Modality And Media Breakdown", build_modality(rows)),
        "discipline-and-tier.md": (
            "Discipline And Tier Breakdown",
            build_discipline_tier(rows),
        ),
        "failure-patterns.md": (
            "Failure Patterns And Safety Gates",
            build_failure_patterns(rows),
        ),
        "example-index.md": ("Example Index", build_example_index(rows)),
    }

    for filename, (title, body) in pages.items():
        write_page(wiki_dir / filename, title, body)
    build_html_index(wiki_dir, readme)
    return wiki_dir


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "run_dir",
        nargs="?",
        type=Path,
        default=DEFAULT_RUN,
        help="Collected run directory containing metrics.json and manifest.json.",
    )
    args = parser.parse_args()
    wiki_dir = build_wiki(args.run_dir)
    print(f"Wrote synthesis wiki to {wiki_dir}")


if __name__ == "__main__":
    main()
