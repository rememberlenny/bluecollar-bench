#!/usr/bin/env python3
"""Collect, version, and analyze per-task rewards from Harbor runs.

Usage:
  python3 scripts/collect_run_results.py <harbor_runs_dir> <run_name>

Outputs, by default:
  benchmark/runs/<run_name>/
    manifest.json          run metadata, catalog hash, source path, git commit
    metrics.json           per-task reward rows
    analysis.md            first-order psychometric report
    catalog.snapshot.json  exact items.json evaluated by this collector

The collector refuses to overwrite an existing run directory unless
`--overwrite` is provided. It also maintains benchmark/runs/index.json and
benchmark/runs/latest.json so repeated suite runs can be compared without
losing older measurements.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
ITEMS = ROOT / "benchmark" / "items" / "items.json"
DEFAULT_RUNS = ROOT / "benchmark" / "runs"


def mean(values: Iterable[float]) -> float:
    xs = list(values)
    return sum(xs) / len(xs) if xs else 0.0


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_value(*args: str) -> str | None:
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("harbor_runs_dir", type=Path)
    parser.add_argument("run_name")
    parser.add_argument("--output-root", type=Path, default=DEFAULT_RUNS)
    parser.add_argument("--overwrite", action="store_true", help="replace an existing run directory")
    return parser.parse_args()


def load_items() -> tuple[list[dict], dict[str, dict]]:
    items = json.loads(ITEMS.read_text(encoding="utf-8"))
    return items, {item["id"]: item for item in items}


def collect_rows(runs_dir: Path, by_id: dict[str, dict]) -> list[dict]:
    task_ids = set(by_id)
    rows: dict[str, dict] = {}
    for reward_path in runs_dir.rglob("reward.json"):
        task_id = next((part for part in reversed(reward_path.parts) if part in task_ids), None)
        if not task_id:
            trial_dir = reward_path.parents[1]
            for metadata_path in [trial_dir / "result.json", trial_dir / "config.json"]:
                try:
                    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
                except Exception:
                    continue
                task_path = metadata.get("task_id", {}).get("path") or metadata.get("task", {}).get("path")
                if task_path:
                    candidate = Path(task_path).name
                    if candidate in task_ids:
                        task_id = candidate
                        break
        if not task_id:
            continue
        try:
            metrics = json.loads(reward_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        numeric_metrics = {k: v for k, v in metrics.items() if isinstance(v, (int, float))}
        reward = float(numeric_metrics.get("reward", 0.0))
        previous = rows.get(task_id)
        if previous is None or reward > previous.get("reward", 0.0):
            item = by_id[task_id]
            rows[task_id] = {
                "task": task_id,
                "tier": item.get("tier", "?"),
                "discipline": item.get("discipline_code", "?"),
                "task_type": item.get("task_type", "?"),
                "decision": item.get("decision", "?"),
                "modality": item.get("modality", "text"),
                "generation": item.get("generation", "auto"),
                "reward_path": str(reward_path),
                **numeric_metrics,
            }
    return sorted(rows.values(), key=lambda row: row["task"])


def axis_table(rows: list[dict], axis: str) -> list[str]:
    groups: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        groups[str(row.get(axis, "?"))].append(float(row.get("reward", 0.0)))
    lines = [f"\n### By {axis}\n", "| group | n | mean reward |", "|---|---:|---:|"]
    for group, rewards in sorted(groups.items(), key=lambda item: mean(item[1])):
        lines.append(f"| {group} | {len(rewards)} | {mean(rewards):.3f} |")
    return lines


def gate_hits(rows: list[dict], key: str) -> int:
    return sum(1 for row in rows if row.get(key, 1) == 0)


def write_analysis(run_name: str, manifest: dict, rows: list[dict], path: Path) -> None:
    rewards = [float(row.get("reward", 0.0)) for row in rows]
    saturated = sum(1 for value in rewards if value >= 0.95)
    floored = sum(1 for value in rewards if value <= 0.05)
    lines = [
        f"# Run Analysis - {run_name}",
        "",
        f"- Tasks scored: **{len(rows)}**",
        f"- Catalog sha256: `{manifest['catalog_sha256']}`",
        f"- Collected at: `{manifest['collected_at']}`",
        f"- Mean reward: **{mean(rewards):.3f}**",
        f"- Saturated (>=0.95): {saturated} ({saturated / max(1, len(rewards)):.0%})",
        f"- Floored (<=0.05): {floored}",
        f"- **dangerous_false_pass** gate hits: {gate_hits(rows, 'dangerous_false_pass')}",
        f"- **alarmist_false_fail** gate hits: {gate_hits(rows, 'alarmist_false_fail')}",
    ]
    for axis in ["tier", "discipline", "task_type", "decision", "modality", "generation"]:
        lines += axis_table(rows, axis)

    hardest = sorted(rows, key=lambda row: float(row.get("reward", 0.0)))[:15]
    lines += ["\n### Hardest 15 Items\n", "| task | reward |", "|---|---:|"]
    lines += [f"| `{row['task']}` | {float(row.get('reward', 0.0)):.3f} |" for row in hardest]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def load_index(output_root: Path) -> dict:
    path = output_root / "index.json"
    if not path.exists():
        return {"schema_version": 1, "runs": []}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {"schema_version": 1, "runs": []}


def update_index(output_root: Path, manifest: dict) -> None:
    index = load_index(output_root)
    runs = [run for run in index.get("runs", []) if run.get("run") != manifest["run"]]
    runs.append({
        "run": manifest["run"],
        "path": manifest["path"],
        "collected_at": manifest["collected_at"],
        "tasks_scored": manifest["tasks_scored"],
        "catalog_sha256": manifest["catalog_sha256"],
        "git_commit": manifest.get("git_commit"),
        "source_runs_dir": manifest["source_runs_dir"],
    })
    runs.sort(key=lambda run: run["collected_at"])
    index = {"schema_version": 1, "latest": manifest["run"], "runs": runs}
    (output_root / "index.json").write_text(json.dumps(index, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (output_root / "latest.json").write_text(json.dumps(runs[-1], indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    runs_dir = args.harbor_runs_dir.resolve()
    output_root = args.output_root.resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    run_dir = output_root / args.run_name
    if run_dir.exists():
        if not args.overwrite:
            raise SystemExit(f"{run_dir} already exists; use --overwrite or choose a new run_name")
        shutil.rmtree(run_dir)
    run_dir.mkdir(parents=True)

    items, by_id = load_items()
    rows = collect_rows(runs_dir, by_id)
    catalog_hash = sha256(ITEMS)
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    manifest = {
        "schema_version": 1,
        "run": args.run_name,
        "path": str(run_dir.relative_to(ROOT)) if run_dir.is_relative_to(ROOT) else str(run_dir),
        "source_runs_dir": str(runs_dir),
        "collected_at": now,
        "tasks_scored": len(rows),
        "catalog_sha256": catalog_hash,
        "catalog_sha256_16": catalog_hash[:16],
        "catalog_items": len(items),
        "git_commit": git_value("rev-parse", "HEAD"),
        "git_branch": git_value("branch", "--show-current"),
        "git_dirty": bool(git_value("status", "--short")),
    }
    metrics = {"schema_version": 1, "manifest": manifest, "rows": rows}

    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (run_dir / "metrics.json").write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (run_dir / "catalog.snapshot.json").write_bytes(ITEMS.read_bytes())
    write_analysis(args.run_name, manifest, rows, run_dir / "analysis.md")
    update_index(output_root, manifest)

    print(f"Scored {len(rows)} tasks -> {run_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
