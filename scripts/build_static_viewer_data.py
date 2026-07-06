#!/usr/bin/env python3
"""Build the static JSON payload used by the GitHub-hosted task viewer."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "docs/viewer/data/viewer-data.json"
COMPONENT_KEYS = [
    "schema",
    "decision",
    "risk",
    "s1",
    "s2",
    "s3",
    "findings",
    "actions",
    "forbidden_clean",
    "dangerous_false_pass",
    "alarmist_false_fail",
]
ANSWER_KEYS = [
    "decision",
    "risk",
    "s1_state",
    "s2_conditions",
    "s3_percent",
    "value",
    "sound_source",
    "confidence",
    "event_time",
    "rate",
    "order",
    "workable",
    "findings",
    "actions",
    "rationale",
    "references",
]


def load_json(path: Path, fallback: Any = None) -> Any:
    if not path.exists():
        return fallback
    with path.open() as f:
        return json.load(f)


def load_answer_json(path: Path) -> Any | None:
    try:
        return json.loads(path.read_text(errors="replace"), strict=False)
    except (OSError, json.JSONDecodeError):
        return None


def compact_text(value: Any, limit: int = 420) -> str:
    text = str(value)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "..."


def compact_answer(value: Any) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        return None
    answer: dict[str, Any] = {}
    for key in ANSWER_KEYS:
        if key not in value:
            continue
        item = value[key]
        if isinstance(item, str):
            answer[key] = compact_text(item)
        elif isinstance(item, list):
            answer[key] = [compact_text(entry, 240) for entry in item[:8]]
            if len(item) > 8:
                answer[key].append(f"... {len(item) - 8} more")
        elif isinstance(item, (int, float, bool)) or item is None:
            answer[key] = item
        else:
            answer[key] = compact_text(json.dumps(item, sort_keys=True), 240)
    return answer or None


def parse_json_text(text: str) -> Any | None:
    try:
        return json.loads(text, strict=False)
    except json.JSONDecodeError:
        return None


def extract_answer_from_patch(patch: str) -> dict[str, Any] | None:
    if "/app/answer.json" not in patch:
        return None
    lines = []
    in_file = False
    for line in patch.splitlines():
        if line.startswith("*** Add File: /app/answer.json") or line.startswith("*** Update File: /app/answer.json"):
            in_file = True
            continue
        if in_file and line.startswith("*** End Patch"):
            break
        if in_file and line.startswith("+") and not line.startswith("+++"):
            lines.append(line[1:])
    return compact_answer(parse_json_text("\n".join(lines)))


def extract_answer_from_trajectory(path: Path) -> dict[str, Any] | None:
    data = load_json(path, {})
    for step in data.get("steps", []):
        for call in step.get("tool_calls", []):
            args = call.get("arguments", {})
            if isinstance(args, dict):
                patch = args.get("input") or args.get("cmd") or ""
            else:
                patch = str(args)
            answer = extract_answer_from_patch(patch)
            if answer:
                answer["source"] = "trajectory patch"
                return answer
        extra = step.get("extra", {})
        details = extra.get("tool_call_details", {}) if isinstance(extra, dict) else {}
        for detail in details.values():
            answer = extract_answer_from_patch(str(detail.get("raw_arguments", "")))
            if answer:
                answer["source"] = "trajectory patch"
                return answer
    return None


def extract_answer_from_jsonl(path: Path) -> dict[str, Any] | None:
    try:
        lines = path.read_text(errors="replace").splitlines()
    except OSError:
        return None
    for line in lines:
        event = parse_json_text(line)
        if not isinstance(event, dict):
            continue
        payload = event.get("payload", {})
        if isinstance(payload, dict):
            # Codex rollout logs include patch content in either the custom tool
            # call input or in the patch-apply event's file-change payload.
            answer = extract_answer_from_patch(str(payload.get("input", "")))
            if answer:
                answer["source"] = "agent transcript"
                return answer
            changes = payload.get("changes", {})
            if isinstance(changes, dict):
                changed = changes.get("/app/answer.json", {})
                content = changed.get("content") if isinstance(changed, dict) else None
                answer = compact_answer(parse_json_text(content or ""))
                if answer:
                    answer["source"] = "agent transcript"
                    return answer
        item = event.get("item", {})
        if isinstance(item, dict) and item.get("type") == "file_change":
            for change in item.get("changes", []):
                if change.get("path") == "/app/answer.json" and change.get("content"):
                    answer = compact_answer(parse_json_text(change["content"]))
                    if answer:
                        answer["source"] = "agent transcript"
                        return answer
        message = event.get("message", {})
        if isinstance(message, dict):
            for content in message.get("content", []):
                if not isinstance(content, dict):
                    continue
                if content.get("type") == "tool_use":
                    tool_input = content.get("input", {})
                    if isinstance(tool_input, dict) and tool_input.get("file_path") == "/app/answer.json":
                        answer = compact_answer(parse_json_text(tool_input.get("content", "")))
                        if answer:
                            answer["source"] = "agent transcript"
                            return answer
    return None


def extract_answer_from_trial(trial_dir: Path) -> dict[str, Any] | None:
    answer_path = trial_dir / "answer.json"
    if answer_path.exists():
        answer = compact_answer(load_answer_json(answer_path))
        if answer:
            answer["source"] = str(answer_path.relative_to(ROOT)) if answer_path.is_relative_to(ROOT) else str(answer_path)
            return answer

    trajectory_path = trial_dir / "agent/trajectory.json"
    if trajectory_path.exists():
        answer = extract_answer_from_trajectory(trajectory_path)
        if answer:
            return answer

    for transcript in sorted((trial_dir / "agent").glob("**/*.jsonl")):
        answer = extract_answer_from_jsonl(transcript)
        if answer:
            return answer
    for transcript in sorted((trial_dir / "agent").glob("*.txt")):
        answer = extract_answer_from_jsonl(transcript)
        if answer:
            return answer
    return None


def trial_dir_from_reward_path(path_text: str) -> Path | None:
    if not path_text:
        return None
    path = Path(path_text)
    if not path.is_absolute():
        path = ROOT / path
    for candidate in [path.parent, *path.parents]:
        if (candidate / "answer.json").exists() or (candidate / "result.json").exists() or (candidate / "agent").exists():
            return candidate
    return None


def answer_for_reward_path(path_text: str) -> dict[str, Any] | None:
    trial_dir = trial_dir_from_reward_path(path_text)
    if not trial_dir:
        return None
    return extract_answer_from_trial(trial_dir)


def git_output(args: list[str]) -> str:
    try:
        return subprocess.check_output(args, cwd=ROOT, text=True).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def github_repo() -> str:
    remote = git_output(["git", "remote", "get-url", "origin"])
    match = re.search(r"github\.com[:/](?P<repo>[^/]+/[^/.]+)(?:\.git)?$", remote)
    return match.group("repo") if match else ""


def current_ref() -> str:
    ref = git_output(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    return ref or "master"


def media_type(filename: str) -> str:
    suffix = Path(filename).suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}:
        return "image"
    if suffix in {".wav", ".mp3", ".ogg", ".m4a"}:
        return "audio"
    if suffix in {".mp4", ".webm", ".mov"}:
        return "video"
    return "file"


def short_result(row: dict[str, Any]) -> dict[str, Any]:
    result = {
        "reward": row.get("reward"),
        "difficulty": difficulty_bucket(row.get("reward")),
        "reward_path": row.get("reward_path", ""),
    }
    answer = answer_for_reward_path(row.get("reward_path", ""))
    if answer:
        result["answer"] = answer
    for key in COMPONENT_KEYS:
        if key in row:
            result[key] = row[key]
    return result


def run_label(run_id: str) -> str:
    lowered = run_id.lower()
    if "gpt55_missing" in lowered or "delta" in lowered:
        return "GPT-5.5 text delta"
    if "gpt55" in lowered and "merged" in lowered:
        return "GPT-5.5 full merged"
    if "gpt55" in lowered and "20260705" in lowered:
        return "GPT-5.5 full 2026-07-05"
    if "gpt55" in lowered:
        return "GPT-5.5"
    if "sonnet5" in lowered:
        return "Sonnet 5"
    if "deepseek" in lowered:
        return "DeepSeek v4 Pro"
    if "glm52" in lowered or "glm-5.2" in lowered:
        return "GLM 5.2"
    if "gemini35" in lowered or "gemini_35" in lowered:
        return "Gemini 3.5 Flash"
    if "codex" in lowered:
        return "Codex GPT-5"
    return run_id.replace("_", " ")


def difficulty_bucket(reward: Any) -> str:
    if not isinstance(reward, (int, float)):
        return "unscored"
    if reward <= 0.25:
        return "hard"
    if reward <= 0.65:
        return "medium"
    if reward <= 0.9:
        return "light"
    return "solved"


def compact_item(
    item: dict[str, Any],
    results: dict[str, dict[str, Any]],
    default_run: str,
    repo: str,
    ref: str,
) -> dict[str, Any]:
    task_id = item["id"]
    task_path = f"tasks/{task_id}"
    media = []
    for name in item.get("media", []):
        media_path = f"benchmark/media/{name}"
        media_item = {
            "name": name,
            "type": media_type(name),
            "repo_path": media_path,
            "root_relative": f"../../{media_path}",
        }
        if repo:
            media_item["raw_url"] = f"https://raw.githubusercontent.com/{repo}/{ref}/{media_path}"
        media.append(media_item)

    links = {
        "task": task_path,
        "instruction": f"{task_path}/instruction.md",
        "item_json": f"{task_path}/tests/item.json",
        "grade": f"{task_path}/tests/grade.py",
    }
    if repo:
        links.update(
            {
                "github_task": f"https://github.com/{repo}/tree/{ref}/{task_path}",
                "github_instruction": f"https://github.com/{repo}/blob/{ref}/{task_path}/instruction.md",
                "github_item_json": f"https://github.com/{repo}/blob/{ref}/{task_path}/tests/item.json",
            }
        )

    return {
        "id": task_id,
        "title": item.get("title", task_id),
        "tier": item.get("tier", ""),
        "discipline": item.get("discipline", ""),
        "discipline_code": item.get("discipline_code", ""),
        "element": item.get("element", ""),
        "element_code": item.get("element_code", ""),
        "subcategory": item.get("subcategory", ""),
        "task_type": item.get("task_type", ""),
        "task_type_name": item.get("task_type_name", ""),
        "generation": item.get("generation", ""),
        "modality": item.get("modality", ""),
        "decision": item.get("decision", ""),
        "risk": item.get("risk", ""),
        "s1_state": item.get("s1_state", ""),
        "s2_expected": item.get("s2_expected", []),
        "s3_percent": item.get("s3_percent"),
        "prompt": item.get("prompt", ""),
        "scenario": item.get("scenario", ""),
        "source_refs": item.get("source_refs", []),
        "required_findings": item.get("required_findings", []),
        "required_actions": item.get("required_actions", []),
        "forbidden": item.get("forbidden", []),
        "leakage_ratio": item.get("leakage_ratio"),
        "media": media,
        "links": links,
        "result": results.get(default_run),
        "results": results,
    }


def run_summary(metadata: dict[str, Any], rows: list[dict[str, Any]]) -> dict[str, Any]:
    rewards = [row["reward"] for row in rows if isinstance(row.get("reward"), (int, float))]
    gates = {
        "dangerous_false_pass": sum(1 for row in rows if row.get("dangerous_false_pass") == 0.0),
        "alarmist_false_fail": sum(1 for row in rows if row.get("alarmist_false_fail") == 0.0),
    }
    run_id = metadata.get("run", "")
    return {
        "run": run_id,
        "label": run_label(run_id),
        "path": metadata.get("path", ""),
        "collected_at": metadata.get("collected_at", ""),
        "git_commit": metadata.get("git_commit", ""),
        "catalog_sha256": metadata.get("catalog_sha256", ""),
        "catalog_sha256_16": metadata.get("catalog_sha256_16", metadata.get("catalog_sha256", "")[:16]),
        "source_runs_dir": metadata.get("source_runs_dir", ""),
        "tasks_scored": len(rows),
        "mean_reward": round(sum(rewards) / len(rewards), 4) if rewards else None,
        "min_reward": min(rewards) if rewards else None,
        "max_reward": max(rewards) if rewards else None,
        "gates": gates,
    }


def discover_runs() -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, dict[str, dict[str, Any]]]]:
    runs_index = load_json(ROOT / "benchmark/runs/index.json", {})
    indexed = {
        entry.get("run"): entry
        for entry in runs_index.get("runs", [])
        if entry.get("run")
    }
    candidates: dict[str, dict[str, Any]] = dict(indexed)
    for metrics_path in sorted((ROOT / "benchmark/runs").glob("*/metrics.json")):
        run_dir = metrics_path.parent
        manifest = load_json(run_dir / "manifest.json", {})
        run_id = manifest.get("run", run_dir.name)
        candidates.setdefault(
            run_id,
            {
                **manifest,
                "run": run_id,
                "path": str(run_dir.relative_to(ROOT)),
            },
        )

    runs: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    results_by_task: dict[str, dict[str, dict[str, Any]]] = {}
    for run_id, metadata in candidates.items():
        run_path = metadata.get("path")
        if not run_path:
            continue
        metrics = load_json(ROOT / run_path / "metrics.json", {})
        rows = metrics.get("rows", [])
        summary = run_summary(metadata, rows)
        if not rows:
            skipped.append({**summary, "skip_reason": "no metric rows"})
            continue
        runs.append(summary)
        for row in rows:
            results_by_task.setdefault(row["task"], {})[run_id] = short_result(row)

    runs.sort(key=lambda run: (run.get("collected_at") or "", run["run"]))
    skipped.sort(key=lambda run: (run.get("collected_at") or "", run["run"]))
    return runs, skipped, results_by_task


def build_payload() -> dict[str, Any]:
    items = load_json(ROOT / "benchmark/items/items.json", [])
    taxonomy = load_json(ROOT / "benchmark/taxonomy.json", {})
    runs, skipped_runs, results_by_task = discover_runs()
    default_run = runs[-1]["run"] if runs else ""
    repo = github_repo()
    ref = current_ref()
    compact_items = [
        compact_item(item, results_by_task.get(item["id"], {}), default_run, repo, ref)
        for item in sorted(items, key=lambda entry: entry["id"])
    ]
    tasks_with_results = sum(1 for item in compact_items if item["results"])
    result_count = sum(len(item["results"]) for item in compact_items)
    summary = {
        "items": len(compact_items),
        "runs": len(runs),
        "scored": tasks_with_results,
        "result_count": result_count,
        "unscored": sum(1 for item in compact_items if not item["results"]),
        "by_tier": dict(sorted(Counter(item["tier"] for item in compact_items).items())),
        "by_task_type": dict(sorted(Counter(item["task_type"] for item in compact_items).items())),
        "by_modality": dict(sorted(Counter(item["modality"] for item in compact_items).items())),
        "by_decision": dict(sorted(Counter(item["decision"] for item in compact_items).items())),
    }
    return {
        "schema_version": 1,
        "generated_at": git_output(["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"]),
        "repo": repo,
        "ref": ref,
        "summary": summary,
        "run": runs[-1] if runs else None,
        "runs": runs,
        "skipped_runs": skipped_runs,
        "default_run": default_run,
        "taxonomy": taxonomy.get("axes", {}),
        "items": compact_items,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    payload = build_payload()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as f:
        json.dump(payload, f, indent=2, sort_keys=True)
        f.write("\n")
    print(f"wrote {args.output.relative_to(ROOT)} with {len(payload['items'])} items")


if __name__ == "__main__":
    main()
