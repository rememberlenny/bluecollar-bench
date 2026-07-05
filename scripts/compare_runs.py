#!/usr/bin/env python3
"""Compare two collected benchmark runs.

Usage:
  python3 scripts/compare_runs.py <base_run> <candidate_run>

Run arguments may be run names under benchmark/runs or explicit paths to run
directories / metrics.json files. The script writes a Markdown comparison to
stdout unless `--output` is provided.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUNS = ROOT / "benchmark" / "runs"


def mean(values: Iterable[float]) -> float:
    xs = list(values)
    return sum(xs) / len(xs) if xs else 0.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base_run")
    parser.add_argument("candidate_run")
    parser.add_argument("--runs-root", type=Path, default=DEFAULT_RUNS)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def resolve_metrics(value: str, runs_root: Path) -> Path:
    path = Path(value)
    candidates = []
    if path.exists():
        candidates.append(path)
    candidates.extend([
        runs_root / value / "metrics.json",
        runs_root / f"{value}_metrics.json",
    ])
    for candidate in candidates:
        if candidate.is_dir():
            candidate = candidate / "metrics.json"
        if candidate.exists():
            return candidate.resolve()
    raise SystemExit(f"Could not resolve run metrics for {value!r}")


def load_run(value: str, runs_root: Path) -> dict:
    metrics_path = resolve_metrics(value, runs_root)
    data = json.loads(metrics_path.read_text(encoding="utf-8"))
    if "manifest" not in data:
        data = {
            "schema_version": 0,
            "manifest": {
                "run": data.get("run", metrics_path.stem.replace("_metrics", "")),
                "catalog_sha256": data.get("catalog_sha256") or data.get("catalog_sha256_16"),
                "tasks_scored": data.get("tasks_scored", len(data.get("rows", []))),
                "path": str(metrics_path),
            },
            "rows": data.get("rows", []),
        }
    data["_metrics_path"] = str(metrics_path)
    return data


def row_map(run: dict) -> dict[str, dict]:
    return {row["task"]: row for row in run.get("rows", [])}


def reward(row: dict | None) -> float:
    return float((row or {}).get("reward", 0.0))


def axis_deltas(base_rows: dict[str, dict], cand_rows: dict[str, dict], axis: str) -> list[str]:
    groups: dict[str, list[tuple[float, float]]] = defaultdict(list)
    for task in sorted(set(base_rows) & set(cand_rows)):
        group = str(cand_rows[task].get(axis, base_rows[task].get(axis, "?")))
        groups[group].append((reward(base_rows[task]), reward(cand_rows[task])))
    lines = [f"\n### Delta By {axis}\n", "| group | n | base | candidate | delta |", "|---|---:|---:|---:|---:|"]
    for group, pairs in sorted(groups.items(), key=lambda item: mean(c - b for b, c in item[1])):
        base_mean = mean(b for b, _ in pairs)
        cand_mean = mean(c for _, c in pairs)
        lines.append(f"| {group} | {len(pairs)} | {base_mean:.3f} | {cand_mean:.3f} | {cand_mean - base_mean:+.3f} |")
    return lines


def gate_hits(rows: Iterable[dict], key: str) -> int:
    return sum(1 for row in rows if row.get(key, 1) == 0)


def build_report(base: dict, candidate: dict) -> str:
    base_manifest = base["manifest"]
    cand_manifest = candidate["manifest"]
    base_rows = row_map(base)
    cand_rows = row_map(candidate)
    common = sorted(set(base_rows) & set(cand_rows))
    added = sorted(set(cand_rows) - set(base_rows))
    removed = sorted(set(base_rows) - set(cand_rows))
    pairs = [(task, reward(base_rows[task]), reward(cand_rows[task])) for task in common]
    regressions = sorted(pairs, key=lambda item: item[2] - item[1])[:15]
    improvements = sorted(pairs, key=lambda item: item[2] - item[1], reverse=True)[:15]
    base_rewards = [b for _, b, _ in pairs]
    cand_rewards = [c for _, _, c in pairs]
    hash_match = base_manifest.get("catalog_sha256") == cand_manifest.get("catalog_sha256")

    lines = [
        f"# Run Comparison - {base_manifest.get('run')} vs {cand_manifest.get('run')}",
        "",
        f"- Base metrics: `{base.get('_metrics_path')}`",
        f"- Candidate metrics: `{candidate.get('_metrics_path')}`",
        f"- Catalog hashes match: **{hash_match}**",
        f"- Base catalog: `{base_manifest.get('catalog_sha256')}`",
        f"- Candidate catalog: `{cand_manifest.get('catalog_sha256')}`",
        f"- Common tasks: **{len(common)}**",
        f"- Added tasks: {len(added)}",
        f"- Removed tasks: {len(removed)}",
        f"- Base mean reward on common tasks: **{mean(base_rewards):.3f}**",
        f"- Candidate mean reward on common tasks: **{mean(cand_rewards):.3f}**",
        f"- Delta: **{mean(cand_rewards) - mean(base_rewards):+.3f}**",
        f"- Base dangerous_false_pass hits: {gate_hits((base_rows[t] for t in common), 'dangerous_false_pass')}",
        f"- Candidate dangerous_false_pass hits: {gate_hits((cand_rows[t] for t in common), 'dangerous_false_pass')}",
        f"- Base alarmist_false_fail hits: {gate_hits((base_rows[t] for t in common), 'alarmist_false_fail')}",
        f"- Candidate alarmist_false_fail hits: {gate_hits((cand_rows[t] for t in common), 'alarmist_false_fail')}",
    ]
    if not hash_match:
        lines += [
            "",
            "> Catalog hashes differ. Treat reward deltas as model+catalog deltas unless you intentionally compare across benchmark versions.",
        ]

    for axis in ["tier", "discipline", "task_type", "decision", "modality", "generation"]:
        lines += axis_deltas(base_rows, cand_rows, axis)

    lines += ["\n### Largest Regressions\n", "| task | base | candidate | delta |", "|---|---:|---:|---:|"]
    lines += [f"| `{task}` | {b:.3f} | {c:.3f} | {c - b:+.3f} |" for task, b, c in regressions]
    lines += ["\n### Largest Improvements\n", "| task | base | candidate | delta |", "|---|---:|---:|---:|"]
    lines += [f"| `{task}` | {b:.3f} | {c:.3f} | {c - b:+.3f} |" for task, b, c in improvements]
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    base = load_run(args.base_run, args.runs_root.resolve())
    candidate = load_run(args.candidate_run, args.runs_root.resolve())
    report = build_report(base, candidate)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
