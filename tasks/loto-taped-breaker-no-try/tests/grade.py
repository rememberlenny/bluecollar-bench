#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
from pathlib import Path


APP_DIR = Path(os.environ.get("BLUECOLLAR_APP_DIR", "/app"))
LOG_DIR = Path(os.environ.get("BLUECOLLAR_LOG_DIR", "/logs/verifier"))
ITEM_PATH = Path(os.environ.get("BLUECOLLAR_ITEM_PATH", "/tests/item.json"))
ANSWER_PATH = APP_DIR / "answer.json"


def normalize(value: object) -> str:
    if isinstance(value, str):
        text = value
    else:
        text = json.dumps(value, sort_keys=True)
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def flatten_answer(answer: dict) -> str:
    return normalize(answer)


def group_present(text: str, group: list[str]) -> bool:
    tokens = set(text.split())
    for term in group:
        normalized = normalize(term)
        if " " in normalized:
            if normalized not in text:
                return False
        elif normalized not in tokens:
            return False
    return True


def write_reward(metrics: dict[str, float]) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    (LOG_DIR / "reward.json").write_text(json.dumps(metrics, indent=2, sort_keys=True), encoding="utf-8")


def main() -> int:
    item = json.loads(ITEM_PATH.read_text(encoding="utf-8"))
    if not ANSWER_PATH.exists():
        write_reward({
            "reward": 0.0,
            "schema": 0.0,
            "decision": 0.0,
            "risk": 0.0,
            "findings": 0.0,
            "actions": 0.0,
            "safety_gate": 0.0,
        })
        return 0

    try:
        answer = json.loads(ANSWER_PATH.read_text(encoding="utf-8"))
    except Exception:
        write_reward({
            "reward": 0.0,
            "schema": 0.0,
            "decision": 0.0,
            "risk": 0.0,
            "findings": 0.0,
            "actions": 0.0,
            "safety_gate": 0.0,
        })
        return 0

    schema_fields = ["decision", "risk", "findings", "actions"]
    schema_score = sum(1 for field in schema_fields if field in answer) / len(schema_fields)
    text = flatten_answer(answer)

    decision_text = normalize(answer.get("decision", ""))
    decision_score = 1.0 if normalize(item["decision"]) == decision_text else 0.0

    risk_text = normalize(answer.get("risk", ""))
    risk_score = 1.0 if normalize(item["risk"]) == risk_text else 0.0

    required_findings = item.get("required_findings", [])
    finding_hits = sum(1 for group in required_findings if group_present(text, group))
    findings_score = finding_hits / max(1, len(required_findings))

    required_actions = item.get("required_actions", [])
    action_hits = sum(1 for group in required_actions if group_present(text, group))
    actions_score = action_hits / max(1, len(required_actions))

    forbidden_hits = sum(1 for group in item.get("forbidden", []) if group_present(text, group))
    safety_gate = 1.0
    if item["decision"] == "fail" and decision_text in {"pass", "acceptable", "accept"}:
        safety_gate = 0.0
    if forbidden_hits:
        safety_gate = min(safety_gate, 0.49)
    if item["risk"] == "critical" and findings_score < 0.75:
        safety_gate = min(safety_gate, 0.49)

    raw_reward = (
        0.10 * schema_score
        + 0.25 * decision_score
        + 0.15 * risk_score
        + 0.35 * findings_score
        + 0.15 * actions_score
    )
    reward = min(raw_reward, safety_gate)

    write_reward({
        "reward": round(reward, 4),
        "schema": round(schema_score, 4),
        "decision": round(decision_score, 4),
        "risk": round(risk_score, 4),
        "findings": round(findings_score, 4),
        "actions": round(actions_score, 4),
        "safety_gate": round(safety_gate, 4),
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
