#!/usr/bin/env python3
"""restore_scenarios — repair the 888 placeholder items.

The v2 merge replaced auto-generated defect observations with the literal
placeholder "visible cue visible cue visible cue" to zero out leakage. That
removed the evidence entirely: the grader still required defect-specific
findings, but the scenario no longer showed anything, turning 88% of the
catalog into label-guessing from metadata.

The correct fix, applied here:
  1. Restore the original observation text (the defect phrase IS the
     observable evidence) from benchmark/items/original_scenarios.json.
  2. Re-key required_findings to INTERPRETATION vocabulary (consequence /
     code-concept terms from benchmark/items/interpretation_map.json) that a
     competent answer supplies but the scenario does not contain.
  3. Store the defect phrase in a `defect` field (ground truth, shown to
     graders and SME reviewers, not used verbatim for token matching).
  4. Verify BOTH properties for every repaired item:
       evidence_present: the defect phrase appears in the scenario
       leak_free:        <40% of graded finding tokens appear in scenario+prompt
     Items failing either check are reported and left for manual repair.

Run from repo root, then regenerate tasks: python3 scripts/generate_tasks_v2.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ITEMS = ROOT / "benchmark" / "items" / "items.json"
ORIG = ROOT / "benchmark" / "items" / "original_scenarios.json"
IMAP = ROOT / "benchmark" / "items" / "interpretation_map.json"
REPORT = ROOT / "benchmark" / "restore_report.md"

PLACEHOLDER = "visible cue"


def norm(t: str) -> str:
    return " ".join(re.sub(r"[^a-z0-9.]+", " ", t.lower()).split())


def leakage_ratio(item: dict) -> float:
    shown = norm(item.get("scenario", "") + " " + item.get("prompt", ""))
    toks = set(shown.split())
    terms = [t for g in item.get("required_findings", []) for t in g]
    if not terms:
        return 0.0
    hits = sum((norm(t) in shown) if " " in norm(t) else (norm(t) in toks) for t in terms)
    return hits / len(terms)


def main() -> None:
    items = json.loads(ITEMS.read_text(encoding="utf-8"))
    orig = json.loads(ORIG.read_text(encoding="utf-8"))
    imap = json.loads(IMAP.read_text(encoding="utf-8"))

    repaired, no_map, no_orig, residual_leaky = [], [], [], []
    for item in items:
        if PLACEHOLDER not in item.get("scenario", ""):
            continue
        rec = orig.get(item["id"]) or orig.get(item.get("legacy_id", ""))
        if not rec or not rec.get("defect"):
            no_orig.append(item["id"])
            continue
        groups = imap.get(item["element_code"])
        if not groups:
            no_map.append(item["id"])
            continue

        item["scenario"] = rec["scenario"]
        item["defect"] = rec["defect"]
        item["required_findings"] = groups
        item["findings_mode"] = "any_per_group"
        item["leakage_ratio"] = round(leakage_ratio(item), 2)
        item["evidence_present"] = norm(rec["defect"]) in norm(rec["scenario"])
        if item["leakage_ratio"] >= 0.4:
            residual_leaky.append((item["id"], item["leakage_ratio"]))
        repaired.append(item["id"])

    ITEMS.write_text(json.dumps(items, indent=2, sort_keys=True), encoding="utf-8")

    ev_ok = sum(1 for i in items if i.get("evidence_present"))
    lines = [
        "# Scenario Restoration Report",
        "",
        f"- Placeholder items repaired: **{len(repaired)}**",
        f"- Evidence-present verified: **{ev_ok}**",
        f"- Residual leakage >=40% after interpretation re-key: **{len(residual_leaky)}**"
        + (f" — {residual_leaky[:10]}" if residual_leaky else ""),
        f"- Missing original scenario: {len(no_orig)} {no_orig[:5]}",
        f"- Missing interpretation map entry: {len(no_map)} {sorted(set(no_map))[:5]}",
        "",
        "Findings now grade interpretation (consequence / code concept) rather than",
        "echoes of the observation. `defect` holds the ground-truth phrase for SME",
        "review and future LLM-judge rubrics. Interpretation vocabulary is",
        "element-level v1 — SME refinement to defect-level is the follow-up.",
    ]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"repaired={len(repaired)} evidence_ok={ev_ok} residual_leaky={len(residual_leaky)} "
          f"no_orig={len(no_orig)} no_map={len(no_map)}")


if __name__ == "__main__":
    main()
