#!/usr/bin/env python3
"""Local validation for generated Harbor tasks.

This does not replace `harbor run`, but it catches broken task structure,
invalid JSON, and verifier/oracle mismatches without Docker.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TASKS_DIR = ROOT / "tasks"


REQUIRED_FILES = [
    "instruction.md",
    "task.toml",
    "environment/Dockerfile",
    "tests/test.sh",
    "tests/grade.py",
    "tests/item.json",
    "solution/solve.sh",
]


def validate_task(task_dir: Path) -> tuple[bool, str]:
    for rel in REQUIRED_FILES:
        if not (task_dir / rel).exists():
            return False, f"missing {rel}"

    try:
        item = json.loads((task_dir / "tests" / "item.json").read_text(encoding="utf-8"))
    except Exception as exc:
        return False, f"invalid tests/item.json: {exc}"

    for key in ["id", "decision", "risk", "required_findings", "required_actions"]:
        if key not in item:
            return False, f"item missing {key}"

    for entry in item.get("media", []) or []:
        media_path = entry if isinstance(entry, str) else entry.get("path", "")
        if not media_path:
            return False, "media entry missing path"
        if not (task_dir / "environment" / "media" / media_path).exists():
            return False, f"missing media fixture {media_path}"

    with tempfile.TemporaryDirectory(prefix=f"{task_dir.name}-") as tmp:
        tmp_path = Path(tmp)
        app_dir = tmp_path / "app"
        log_dir = tmp_path / "logs" / "verifier"
        app_dir.mkdir(parents=True)
        log_dir.mkdir(parents=True)

        env = os.environ.copy()
        env["BLUECOLLAR_APP_DIR"] = str(app_dir)
        env["BLUECOLLAR_LOG_DIR"] = str(log_dir)
        env["BLUECOLLAR_ITEM_PATH"] = str(task_dir / "tests" / "item.json")

        solve = subprocess.run(["bash", str(task_dir / "solution" / "solve.sh")], cwd=ROOT, env=env, text=True, capture_output=True)
        if solve.returncode != 0:
            return False, f"solution failed: {solve.stderr.strip()}"

        grade = subprocess.run([sys.executable, str(task_dir / "tests" / "grade.py")], cwd=ROOT, env=env, text=True, capture_output=True)
        if grade.returncode != 0:
            return False, f"grader failed: {grade.stderr.strip()}"

        reward_path = log_dir / "reward.json"
        if not reward_path.exists():
            return False, "grader did not write reward.json"

        reward = json.loads(reward_path.read_text(encoding="utf-8"))
        if reward.get("reward", 0.0) < 0.99:
            return False, f"oracle reward below 0.99: {reward}"

    return True, "ok"


def main() -> int:
    if not TASKS_DIR.exists():
        print("tasks/ does not exist; run scripts/generate_tasks.py", file=sys.stderr)
        return 1

    failures: list[str] = []
    task_dirs = sorted(p for p in TASKS_DIR.iterdir() if p.is_dir())
    for task_dir in task_dirs:
        ok, message = validate_task(task_dir)
        if len(task_dirs) <= 80 or not ok:
            status = "ok" if ok else "FAIL"
            print(f"{status:4} {task_dir.name}: {message}")
        if not ok:
            failures.append(task_dir.name)

    if failures:
        print(f"\n{len(failures)} task(s) failed validation: {', '.join(failures)}", file=sys.stderr)
        return 1
    print(f"Validated {len(task_dirs)} task(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
