#!/usr/bin/env python3
"""Audit benchmark/items/items.json for answer leakage.

An item "leaks" when the tokens a grader rewards (required_findings) already
appear verbatim in the scenario/prompt text an agent is shown — the agent can
score by echoing the question. Writes benchmark/leakage_report.md and adds a
`leakage_ratio` field to each item in-place (rounded, non-destructive).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ITEMS = ROOT / "benchmark" / "items" / "items.json"
REPORT = ROOT / "benchmark" / "leakage_report.md"


def norm(t: str) -> str:
    return " ".join(re.sub(r"[^a-z0-9]+", " ", t.lower()).split())


def main() -> None:
    items = json.loads(ITEMS.read_text(encoding="utf-8"))
    buckets = {"clean (<40%)": 0, "partial (40-79%)": 0, "leaked (>=80%)": 0}
    worst: list[tuple[float, str]] = []

    for item in items:
        shown = norm(item.get("scenario", "") + " " + item.get("prompt", ""))
        shown_tokens = set(shown.split())
        groups = item.get("required_findings", [])
        terms = [t for g in groups for t in g]
        if not terms:
            item["leakage_ratio"] = 0.0
            buckets["clean (<40%)"] += 1
            continue
        hits = 0
        for t in terms:
            n = norm(t)
            hits += (n in shown) if " " in n else (n in shown_tokens)
        ratio = round(hits / len(terms), 2)
        item["leakage_ratio"] = ratio
        if ratio >= 0.8:
            buckets["leaked (>=80%)"] += 1
            worst.append((ratio, item["id"]))
        elif ratio >= 0.4:
            buckets["partial (40-79%)"] += 1
        else:
            buckets["clean (<40%)"] += 1

    ITEMS.write_text(json.dumps(items, indent=2, sort_keys=True), encoding="utf-8")

    lines = [
        "# Leakage Audit",
        "",
        f"Total items: {len(items)}",
        "",
        "| Bucket | Items |",
        "|---|---:|",
    ]
    for k, v in buckets.items():
        lines.append(f"| {k} | {v} |")
    lines += [
        "",
        "Leaked items reward scenario-echoing. Remediation: rewrite scenarios as",
        "raw observations (what a camera sees) and keep conclusion vocabulary in",
        "required_findings only — see curated seeds and v2 control items for the",
        "target style. Items are tagged in-place with `leakage_ratio`.",
        "",
        "## Worst offenders (first 30)",
        "",
    ]
    for ratio, iid in sorted(worst, reverse=True)[:30]:
        lines.append(f"- `{iid}` — {int(ratio * 100)}%")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Report written to {REPORT}")
    print(buckets)


if __name__ == "__main__":
    main()
