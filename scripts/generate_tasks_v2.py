#!/usr/bin/env python3
"""generate_tasks_v2 — merge v2 control items and regenerate Harbor tasks
with the grade_v2 verifier template.

Reuses render_instruction / render_solution / render_task_toml / DOCKERFILE /
TEST_SH from scripts/generate_tasks.py; only the item set and the grader
template change. Run from repo root: python3 scripts/generate_tasks_v2.py
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import generate_tasks as g1  # noqa: E402
import build_item_catalog as catalog  # noqa: E402

CONTROL = ROOT / "benchmark" / "items" / "control_items_v2.json"
MEDIA_ITEMS = ROOT / "benchmark" / "items" / "media_items_v2.json"
CPM_ITEMS = ROOT / "benchmark" / "items" / "cpm_items_v2.json"
AUDIO_ITEMS = ROOT / "benchmark" / "items" / "audio_items_v2.json"
TEXT_REBALANCE_ITEMS = ROOT / "benchmark" / "items" / "text_rebalance_items_v2.json"
MEDIA_DIR = ROOT / "benchmark" / "media"
ITEMS = ROOT / "benchmark" / "items" / "items.json"
GRADE_V2 = (ROOT / "scripts" / "grade_v2.py").read_text(encoding="utf-8")
TASKS = ROOT / "tasks"


def normalize_item(item: dict) -> dict:
    item = dict(item)
    item.setdefault("modality", "text")
    item.setdefault("media", [])
    return item


def media_paths(item: dict) -> list[str]:
    paths: list[str] = []
    for entry in item.get("media", []) or []:
        if isinstance(entry, str):
            paths.append(entry)
        elif isinstance(entry, dict) and entry.get("path"):
            paths.append(str(entry["path"]))
    return paths


def merged_items() -> list[dict]:
    items = [normalize_item(item) for item in json.loads(ITEMS.read_text(encoding="utf-8"))]
    by_id = {i["id"]: i for i in items}
    added = 0
    for src in (CONTROL, MEDIA_ITEMS, CPM_ITEMS, AUDIO_ITEMS, TEXT_REBALANCE_ITEMS):
        if not src.exists():
            continue
        for item in json.loads(src.read_text(encoding="utf-8")):
            item = normalize_item(item)
            if item["id"] not in by_id:
                by_id[item["id"]] = item
                added += 1
    merged = list(by_id.values())
    ITEMS.write_text(json.dumps(merged, indent=2, sort_keys=True), encoding="utf-8")
    print(f"Merged {added} v2 items; catalog now {len(merged)} items")
    return merged


def main() -> None:
    merged_items()
    restore_script = ROOT / "scripts" / "restore_scenarios.py"
    if restore_script.exists():
        subprocess.run([sys.executable, str(restore_script)], cwd=ROOT, check=True)
    subprocess.run([sys.executable, str(ROOT / "scripts" / "leakage_audit.py")], cwd=ROOT, check=True)
    items = json.loads(ITEMS.read_text(encoding="utf-8"))
    catalog.write_coverage(items, catalog.parse_elements())
    if TASKS.exists():
        shutil.rmtree(TASKS)
    TASKS.mkdir(parents=True)
    for item in items:
        d = TASKS / item["id"]
        (d / "environment").mkdir(parents=True)
        (d / "tests").mkdir()
        (d / "solution").mkdir()
        (d / "instruction.md").write_text(g1.render_instruction(item), encoding="utf-8")
        (d / "task.toml").write_text(g1.render_task_toml(item), encoding="utf-8")
        dockerfile = g1.DOCKERFILE
        paths = media_paths(item)
        if paths:
            media_dst = d / "environment" / "media"
            media_dst.mkdir(parents=True, exist_ok=True)
            for media_path in paths:
                src = MEDIA_DIR / media_path
                if not src.exists():
                    raise FileNotFoundError(f"Missing media fixture for {item['id']}: {src}")
                dst = media_dst / media_path
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
            dockerfile += "COPY media/ /app/media/\nRUN chmod -R 755 /app/media\n"
        (d / "environment" / "Dockerfile").write_text(dockerfile, encoding="utf-8")
        (d / "tests" / "grade.py").write_text(GRADE_V2, encoding="utf-8")
        (d / "tests" / "test.sh").write_text(g1.TEST_SH, encoding="utf-8")
        (d / "tests" / "item.json").write_text(json.dumps(item, indent=2, sort_keys=True), encoding="utf-8")
        (d / "solution" / "solve.sh").write_text(g1.render_solution(item), encoding="utf-8")
        for s in [d / "tests" / "test.sh", d / "tests" / "grade.py", d / "solution" / "solve.sh"]:
            s.chmod(0o755)
    print(f"Generated {len(items)} Harbor tasks with grade_v2 in {TASKS}")


if __name__ == "__main__":
    main()
