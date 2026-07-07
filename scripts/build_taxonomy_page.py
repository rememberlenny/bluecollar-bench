#!/usr/bin/env python3
"""Refresh the data embedded in docs/viewer/taxonomy.html.

The taxonomy map is a single static page (force-directed graph of
discipline -> element -> task, with a per-task model-results sidebar).
Its graph structure and slim result scores are embedded inline so the
page also works without the 29MB data/viewer-data.json next to it; when
served on GitHub Pages it additionally fetches the full payload for
answers and traces.

Run this after task catalog or run updates (after
scripts/build_static_viewer_data.py) to re-embed fresh data in place:

    python3 scripts/build_taxonomy_page.py

The page's markup/CSS/JS are left untouched; only the four
`const DATA/RUNS/CTX/SLIM = ...;` lines are regenerated.
"""

from __future__ import annotations

import json
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = ROOT / "tasks"
PAGE = ROOT / "docs" / "viewer" / "taxonomy.html"
VIEWER_DATA = ROOT / "docs" / "viewer" / "data" / "viewer-data.json"

MODALITIES = ["audio", "image", "text"]


def load_task_rows() -> list[dict]:
    rows = []
    for task_dir in sorted(TASKS_DIR.iterdir()):
        toml_path = task_dir / "task.toml"
        if not toml_path.is_file():
            continue
        with toml_path.open("rb") as fh:
            meta = tomllib.load(fh).get("metadata", {})
        rows.append(
            {
                "id": task_dir.name,
                "tier": meta.get("tier", ""),
                "discipline": meta.get("discipline", ""),
                "element": meta.get("element", ""),
                "task_type": meta.get("task_type", ""),
                "modality": meta.get("modality", "text"),
            }
        )
    return rows


def discipline_code(discipline: str) -> str:
    return discipline.split(" ", 1)[0]


def code_sort_key(code: str) -> list[int]:
    return [int(part) for part in code.split(".")]


def build_blobs() -> dict[str, str]:
    rows = load_task_rows()
    viewer = json.loads(VIEWER_DATA.read_text())
    items_by_id = {item["id"]: item for item in viewer["items"]}
    taxonomy = viewer.get("taxonomy") or {}
    axes = taxonomy.get("axes") or json.loads(
        (ROOT / "benchmark" / "taxonomy.json").read_text()
    )["axes"]

    missing = [row["id"] for row in rows if row["id"] not in items_by_id]
    if missing:
        sys.exit(
            f"{len(missing)} tasks missing from viewer-data.json "
            f"(first: {missing[0]}); run scripts/build_static_viewer_data.py first"
        )

    codes = sorted({discipline_code(r["discipline"]) for r in rows}, key=code_sort_key)
    disciplines = [{"c": c, "n": axes["disciplines"][c]} for c in codes]
    disc_index = {c: i for i, c in enumerate(codes)}

    element_pairs = sorted(
        {(discipline_code(r["discipline"]), r["element"]) for r in rows},
        key=lambda pair: (code_sort_key(pair[0]), pair[1]),
    )
    elem_index = {pair: i for i, pair in enumerate(element_pairs)}
    elements = [[disc_index[c], name] for c, name in element_pairs]

    tiers = [[k, axes["tiers"][k]] for k in ["T1", "T2", "T3", "T4", "T5"]]
    tier_index = {t[0]: i for i, t in enumerate(tiers)}
    task_types = sorted(axes["task_types"].items())
    tt_index = {k: i for i, (k, _) in enumerate(task_types)}
    mod_index = {m: i for i, m in enumerate(MODALITIES)}

    tasks = []
    for row in rows:
        item = items_by_id[row["id"]]
        tasks.append(
            [
                elem_index[(discipline_code(row["discipline"]), row["element"])],
                tier_index[row["tier"]],
                tt_index[row["task_type"]],
                mod_index[row["modality"]],
                row["id"],
                item.get("title", ""),
            ]
        )

    data = {
        "d": disciplines,
        "e": elements,
        "t": tasks,
        "tiers": tiers,
        "tts": [[k, v] for k, v in task_types],
        "mods": MODALITIES,
    }

    runs = [
        {"run": r["run"], "label": r["label"], "model": r["model"], "mean": r["mean_reward"]}
        for r in viewer["runs"]
    ]

    def num(value, digits):
        try:
            return round(float(value), digits)
        except (TypeError, ValueError):
            return None

    ctx, slim = [], []
    for row in rows:
        item = items_by_id[row["id"]]
        ctx.append(
            {
                "t": item.get("title", ""),
                "s": item.get("scenario", ""),
                "p": item.get("prompt", ""),
                "d": item.get("decision", ""),
                "r": item.get("risk", ""),
                "s1": item.get("s1_state", ""),
                "s3": item.get("s3_percent"),
                "rf": item.get("required_findings", []),
                "ra": item.get("required_actions", []),
                "fb": item.get("forbidden", []),
            }
        )
        result_row = []
        for run in viewer["runs"]:
            res = (item.get("results") or {}).get(run["run"])
            if not res:
                result_row.append(None)
                continue
            result_row.append(
                [
                    num(res.get("reward"), 3),
                    num(res.get("decision"), 2),
                    num(res.get("dangerous_false_pass"), 0),
                    num(res.get("alarmist_false_fail"), 0),
                    (res.get("answer") or {}).get("decision", "") or "",
                ]
            )
        slim.append(result_row)

    compact = lambda value: json.dumps(value, separators=(",", ":"))
    return {
        "DATA": compact(data),
        "RUNS": compact(runs),
        "CTX": compact(ctx),
        "SLIM": compact(slim),
    }


def main() -> None:
    blobs = build_blobs()
    lines = PAGE.read_text().splitlines(keepends=True)
    replaced = set()
    for i, line in enumerate(lines):
        for name, blob in blobs.items():
            if line.startswith(f"const {name} = "):
                lines[i] = f"const {name} = {blob};\n"
                replaced.add(name)
    missing = set(blobs) - replaced
    if missing:
        sys.exit(f"could not find embedded blob line(s) in {PAGE}: {sorted(missing)}")
    PAGE.write_text("".join(lines))
    data = json.loads(blobs["DATA"])
    print(
        f"refreshed {PAGE.relative_to(ROOT)}: "
        f"{len(data['d'])} disciplines, {len(data['e'])} elements, "
        f"{len(data['t'])} tasks, {len(json.loads(blobs['RUNS']))} runs"
    )


if __name__ == "__main__":
    main()
