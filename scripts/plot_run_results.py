#!/usr/bin/env python3
"""Create simple SVG plots for a collected benchmark run.

Usage:
  python3 scripts/plot_run_results.py benchmark/runs/<run_name>

Outputs:
  benchmark/runs/<run_name>/plots/index.html
  benchmark/runs/<run_name>/plots/*.svg
"""
from __future__ import annotations

import argparse
import html
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]

COLORS = [
    "#2f6f73",
    "#b64f35",
    "#6f5aa8",
    "#9a6b16",
    "#2f5f9f",
    "#4f7d3a",
    "#9b3f6d",
    "#5f6b2f",
    "#316d9b",
    "#8a4c2f",
    "#56636f",
    "#7a5a2f",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path)
    return parser.parse_args()


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def fmt(value: float) -> str:
    return f"{value:.3f}"


def load_run(run_dir: Path) -> tuple[dict, list[dict]]:
    metrics_path = run_dir / "metrics.json"
    data = json.loads(metrics_path.read_text(encoding="utf-8"))
    return data["manifest"], data["rows"]


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def grouped_means(rows: list[dict], axis: str) -> list[tuple[str, int, float]]:
    groups: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        groups[str(row.get(axis, "?"))].append(float(row.get("reward", 0.0)))
    return sorted(
        [(group, len(values), mean(values)) for group, values in groups.items()],
        key=lambda item: item[2],
    )


def horizontal_bar_svg(
    title: str,
    subtitle: str,
    rows: list[tuple[str, int, float]],
    x_label: str = "Mean reward",
    width: int = 960,
) -> str:
    left = 190
    right = 95
    top = 92
    row_h = 34
    bottom = 54
    height = top + bottom + max(1, len(rows)) * row_h
    plot_w = width - left - right
    max_value = max([value for _, _, value in rows] + [1.0])
    max_value = max(1.0, max_value)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "<style>",
        "text{font-family:Arial,Helvetica,sans-serif;fill:#1f2933} .muted{fill:#607080} .grid{stroke:#d7dde3;stroke-width:1} .axis{stroke:#8b98a5;stroke-width:1.2}",
        "</style>",
        f'<rect width="{width}" height="{height}" fill="#ffffff"/>',
        f'<text x="24" y="34" font-size="24" font-weight="700">{esc(title)}</text>',
        f'<text x="24" y="59" font-size="14" class="muted">{esc(subtitle)}</text>',
    ]
    for tick in [0, 0.25, 0.5, 0.75, 1.0]:
        x = left + tick * plot_w
        parts.append(f'<line x1="{x:.1f}" y1="{top - 18}" x2="{x:.1f}" y2="{height - bottom + 8}" class="grid"/>')
        parts.append(f'<text x="{x:.1f}" y="{height - 18}" text-anchor="middle" font-size="12" class="muted">{tick:.2f}</text>')
    parts.append(f'<line x1="{left}" y1="{height - bottom + 8}" x2="{left + plot_w}" y2="{height - bottom + 8}" class="axis"/>')
    parts.append(f'<text x="{left + plot_w / 2:.1f}" y="{height - 4}" text-anchor="middle" font-size="12" class="muted">{esc(x_label)}</text>')

    for i, (label, n, value) in enumerate(rows):
        y = top + i * row_h
        bar_w = (value / max_value) * plot_w
        color = COLORS[i % len(COLORS)]
        parts.append(f'<text x="{left - 12}" y="{y + 20}" text-anchor="end" font-size="13">{esc(label)}</text>')
        parts.append(f'<rect x="{left}" y="{y + 5}" width="{bar_w:.1f}" height="20" rx="3" fill="{color}"/>')
        parts.append(f'<text x="{left + bar_w + 8:.1f}" y="{y + 20}" font-size="12">{fmt(value)}  n={n}</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def component_scores_svg(rows: list[dict], width: int = 960) -> str:
    metrics = [
        "schema",
        "decision",
        "risk",
        "s1",
        "s2",
        "s3",
        "findings",
        "actions",
        "dangerous_false_pass",
        "alarmist_false_fail",
        "reward",
    ]
    values = []
    for key in metrics:
        values.append((key, len(rows), mean(float(row.get(key, 0.0)) for row in rows)))
    return horizontal_bar_svg(
        "Average Component Scores",
        "Higher is better. Safety gates are shown as clean-pass rates.",
        values,
    )


def histogram_svg(rows: list[dict], width: int = 960, height: int = 440) -> str:
    rewards = [float(row.get("reward", 0.0)) for row in rows]
    bins = [(i / 10, (i + 1) / 10) for i in range(10)]
    counts = []
    for low, high in bins:
        if high >= 1.0:
            count = sum(1 for value in rewards if low <= value <= high)
        else:
            count = sum(1 for value in rewards if low <= value < high)
        counts.append(count)
    left = 68
    right = 24
    top = 72
    bottom = 58
    plot_w = width - left - right
    plot_h = height - top - bottom
    bar_gap = 8
    bar_w = (plot_w - bar_gap * (len(counts) - 1)) / len(counts)
    max_count = max(counts) or 1
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "<style>text{font-family:Arial,Helvetica,sans-serif;fill:#1f2933}.muted{fill:#607080}.grid{stroke:#d7dde3;stroke-width:1}.axis{stroke:#8b98a5;stroke-width:1.2}</style>",
        f'<rect width="{width}" height="{height}" fill="#ffffff"/>',
        '<text x="24" y="34" font-size="24" font-weight="700">Reward Distribution</text>',
        '<text x="24" y="59" font-size="14" class="muted">How many tasks landed in each reward range.</text>',
    ]
    for tick in [0, 0.25, 0.5, 0.75, 1.0]:
        y = top + plot_h - tick * plot_h
        count = int(round(tick * max_count))
        parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{width - right}" y2="{y:.1f}" class="grid"/>')
        parts.append(f'<text x="{left - 10}" y="{y + 4:.1f}" text-anchor="end" font-size="12" class="muted">{count}</text>')
    parts.append(f'<line x1="{left}" y1="{top + plot_h}" x2="{width - right}" y2="{top + plot_h}" class="axis"/>')
    for i, count in enumerate(counts):
        x = left + i * (bar_w + bar_gap)
        h = count / max_count * plot_h
        y = top + plot_h - h
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{h:.1f}" rx="3" fill="{COLORS[i % len(COLORS)]}"/>')
        parts.append(f'<text x="{x + bar_w / 2:.1f}" y="{y - 7:.1f}" text-anchor="middle" font-size="12">{count}</text>')
        parts.append(f'<text x="{x + bar_w / 2:.1f}" y="{top + plot_h + 22}" text-anchor="middle" font-size="12" class="muted">{bins[i][0]:.1f}-{bins[i][1]:.1f}</text>')
    parts.append(f'<text x="{left + plot_w / 2:.1f}" y="{height - 8}" text-anchor="middle" font-size="12" class="muted">Reward range</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def gate_hits_svg(rows: list[dict], width: int = 760, height: int = 330) -> str:
    gates = [
        ("Dangerous false pass", sum(1 for row in rows if float(row.get("dangerous_false_pass", 1.0)) == 0.0)),
        ("Alarmist false fail", sum(1 for row in rows if float(row.get("alarmist_false_fail", 1.0)) == 0.0)),
    ]
    left = 190
    right = 36
    top = 92
    row_h = 60
    plot_w = width - left - right
    max_count = max([count for _, count in gates] + [1])
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "<style>text{font-family:Arial,Helvetica,sans-serif;fill:#1f2933}.muted{fill:#607080}.grid{stroke:#d7dde3;stroke-width:1}</style>",
        f'<rect width="{width}" height="{height}" fill="#ffffff"/>',
        '<text x="24" y="34" font-size="24" font-weight="700">Safety Gate Hits</text>',
        '<text x="24" y="59" font-size="14" class="muted">Counts of tasks that triggered each directional failure gate.</text>',
    ]
    for i, (label, count) in enumerate(gates):
        y = top + i * row_h
        bar_w = count / max_count * plot_w
        parts.append(f'<text x="{left - 12}" y="{y + 28}" text-anchor="end" font-size="14">{esc(label)}</text>')
        parts.append(f'<rect x="{left}" y="{y + 9}" width="{bar_w:.1f}" height="26" rx="4" fill="{COLORS[i + 1]}"/>')
        parts.append(f'<text x="{left + bar_w + 10:.1f}" y="{y + 28}" font-size="14">{count}</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def write_html(run_dir: Path, plots_dir: Path, manifest: dict, rows: list[dict], plot_files: list[str]) -> None:
    rewards = [float(row.get("reward", 0.0)) for row in rows]
    gate_danger = sum(1 for row in rows if float(row.get("dangerous_false_pass", 1.0)) == 0.0)
    gate_alarm = sum(1 for row in rows if float(row.get("alarmist_false_fail", 1.0)) == 0.0)
    saturated = sum(1 for value in rewards if value >= 0.95)
    floored = sum(1 for value in rewards if value <= 0.05)
    hardest = sorted(rows, key=lambda row: float(row.get("reward", 0.0)))[:20]
    cards = [
        ("Tasks scored", str(len(rows))),
        ("Mean reward", fmt(mean(rewards))),
        ("Saturated tasks", str(saturated)),
        ("Floored tasks", str(floored)),
        ("Dangerous false pass hits", str(gate_danger)),
        ("Alarmist false fail hits", str(gate_alarm)),
        ("Catalog", manifest.get("catalog_sha256_16", "")),
    ]
    card_html = "\n".join(
        f'<section class="card"><span>{esc(label)}</span><strong>{esc(value)}</strong></section>'
        for label, value in cards
    )
    plot_html = "\n".join(
        f'<section class="plot"><img src="{esc(name)}" alt="{esc(name)}"></section>' for name in plot_files
    )
    rows_html = "\n".join(
        "<tr>"
        f"<td>{esc(row['task'])}</td>"
        f"<td>{fmt(float(row.get('reward', 0.0)))}</td>"
        f"<td>{esc(row.get('tier', ''))}</td>"
        f"<td>{esc(row.get('task_type', ''))}</td>"
        f"<td>{esc(row.get('modality', ''))}</td>"
        "</tr>"
        for row in hardest
    )
    html_text = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(manifest.get("run", "Run"))} Plots</title>
  <style>
    body {{ margin: 0; font-family: Arial, Helvetica, sans-serif; color: #1f2933; background: #f5f7f9; }}
    main {{ max-width: 1120px; margin: 0 auto; padding: 28px; }}
    h1 {{ margin: 0 0 8px; font-size: 30px; }}
    .meta {{ color: #607080; margin-bottom: 22px; }}
    .cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 12px; margin-bottom: 18px; }}
    .card {{ background: #fff; border: 1px solid #dfe5eb; border-radius: 8px; padding: 14px; }}
    .card span {{ display: block; color: #607080; font-size: 13px; margin-bottom: 8px; }}
    .card strong {{ font-size: 24px; }}
    .plot {{ background: #fff; border: 1px solid #dfe5eb; border-radius: 8px; padding: 10px; margin: 14px 0; overflow-x: auto; }}
    .plot img {{ display: block; width: 100%; min-width: 720px; height: auto; }}
    table {{ width: 100%; border-collapse: collapse; background: #fff; border: 1px solid #dfe5eb; border-radius: 8px; overflow: hidden; }}
    th, td {{ padding: 9px 11px; border-bottom: 1px solid #e8edf2; text-align: left; font-size: 14px; }}
    th {{ background: #e9eef3; }}
  </style>
</head>
<body>
<main>
  <h1>{esc(manifest.get("run", "Run"))}</h1>
  <div class="meta">Collected at {esc(manifest.get("collected_at", ""))}. Source commit {esc(manifest.get("git_commit", ""))}.</div>
  <div class="cards">{card_html}</div>
  {plot_html}
  <h2>Lowest Reward Tasks</h2>
  <table>
    <thead><tr><th>Task</th><th>Reward</th><th>Tier</th><th>Type</th><th>Modality</th></tr></thead>
    <tbody>{rows_html}</tbody>
  </table>
</main>
</body>
</html>
"""
    write(plots_dir / "index.html", html_text)


def main() -> int:
    args = parse_args()
    run_dir = args.run_dir.resolve()
    manifest, rows = load_run(run_dir)
    plots_dir = run_dir / "plots"
    plots_dir.mkdir(parents=True, exist_ok=True)

    plot_specs = [
        ("component_scores.svg", component_scores_svg(rows)),
        ("reward_distribution.svg", histogram_svg(rows)),
        ("mean_reward_by_tier.svg", horizontal_bar_svg("Mean Reward by Tier", "Work setting tiers, sorted from hardest to easiest.", grouped_means(rows, "tier"))),
        ("mean_reward_by_modality.svg", horizontal_bar_svg("Mean Reward by Modality", "Text, image, and audio task performance.", grouped_means(rows, "modality"))),
        ("mean_reward_by_task_type.svg", horizontal_bar_svg("Mean Reward by Task Type", "Task types, sorted from hardest to easiest.", grouped_means(rows, "task_type"))),
        ("mean_reward_by_discipline.svg", horizontal_bar_svg("Mean Reward by Discipline", "Discipline codes, sorted from hardest to easiest.", grouped_means(rows, "discipline"))),
        ("mean_reward_by_generation.svg", horizontal_bar_svg("Mean Reward by Generation Source", "How generated and curated item groups performed.", grouped_means(rows, "generation"))),
        ("safety_gate_hits.svg", gate_hits_svg(rows)),
    ]
    for name, svg in plot_specs:
        write(plots_dir / name, svg)
    write_html(run_dir, plots_dir, manifest, rows, [name for name, _ in plot_specs])
    print(f"Wrote {len(plot_specs)} SVG plots and index.html to {plots_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
