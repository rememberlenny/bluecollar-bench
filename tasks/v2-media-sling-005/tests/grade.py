#!/usr/bin/env python3
"""grade_v2 — backward-compatible upgraded verifier for bluecollar-bench.

Changes vs. v1:
- Supports decision values pass / fail / needs_more_info (v1 items all failed).
- findings_mode: "all" (v1 behavior: every term in a group must appear) or
  "any_per_group" (group satisfied if ANY term appears) for paraphrase robustness.
- Forbidden terms are checked only in findings/actions/s2_conditions, not in
  rationale or decision. v1 flattened the whole answer, so a correct fail
  rationale like "this cannot pass inspection" tripped the forbidden token
  "pass" and zeroed the safety gate.
- Directional safety gates: dangerous_false_pass (item=fail, answer=pass) and
  alarmist_false_fail (item=pass, answer=fail) are scored separately.
- Empty s2_expected means the answer's s2_conditions should also be empty.
- s3 percent scored with +/-15 point tolerance when the item provides it.
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

APP_DIR = Path(os.environ.get("BLUECOLLAR_APP_DIR", "/app"))
LOG_DIR = Path(os.environ.get("BLUECOLLAR_LOG_DIR", "/logs/verifier"))
ITEM_PATH = Path(os.environ.get("BLUECOLLAR_ITEM_PATH", "/tests/item.json"))
ANSWER_PATH = APP_DIR / "answer.json"

METRIC_KEYS = [
    "reward", "schema", "decision", "risk", "s1", "s2", "s3",
    "findings", "actions", "forbidden_clean",
    "dangerous_false_pass", "alarmist_false_fail",
]


def normalize(value: object) -> str:
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def group_present(text: str, group: list[str], mode: str) -> bool:
    tokens = set(text.split())

    def term_in(term: str) -> bool:
        t = normalize(term)
        return (t in text) if " " in t else (t in tokens)

    if mode == "any_per_group":
        return any(term_in(term) for term in group)
    return all(term_in(term) for term in group)


def write_reward(metrics: dict[str, float]) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    payload = {k: float(metrics.get(k, 0.0)) for k in METRIC_KEYS}
    (LOG_DIR / "reward.json").write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def zero(reason: str) -> None:
    metrics = {k: 0.0 for k in METRIC_KEYS}
    metrics["note"] = 0.0  # keep schema stable
    write_reward(metrics)


def main() -> int:
    item = json.loads(ITEM_PATH.read_text(encoding="utf-8"))
    if not ANSWER_PATH.exists():
        zero("missing answer")
        return 0
    try:
        answer = json.loads(ANSWER_PATH.read_text(encoding="utf-8"))
        assert isinstance(answer, dict)
    except Exception:
        zero("invalid json")
        return 0

    mode = item.get("findings_mode", "all")

    # --- schema ---
    schema_fields = ["decision", "risk", "s1_state", "s2_conditions", "s3_percent", "findings", "actions"]
    schema = sum(1 for f in schema_fields if f in answer) / len(schema_fields)

    # --- decision ---
    item_decision = normalize(item.get("decision", "fail"))
    ans_decision = normalize(answer.get("decision", ""))
    decision = 1.0 if item_decision == ans_decision else 0.0

    # --- directional safety gates ---
    dangerous_false_pass = 1.0
    alarmist_false_fail = 1.0
    if item_decision == "fail" and ans_decision == "pass":
        dangerous_false_pass = 0.0
    if item_decision == "pass" and ans_decision == "fail":
        alarmist_false_fail = 0.0

    # --- risk ---
    order = {"low": 0, "medium": 1, "high": 2, "critical": 3}
    ir, ar = item.get("risk"), normalize(answer.get("risk", ""))
    if ir in order and ar in order:
        risk = 1.0 if ir == ar else (0.5 if abs(order[ir] - order[ar]) == 1 else 0.0)
    else:
        risk = 0.0

    # --- S1 ---
    s1 = 1.0 if normalize(item.get("s1_state", "")) == normalize(answer.get("s1_state", "")) else 0.0

    # --- S2 (empty expected => answer should also be empty) ---
    expected_s2 = {normalize(x) for x in item.get("s2_expected", [])}
    ans_s2 = {normalize(x) for x in (answer.get("s2_conditions") or []) if isinstance(x, str)}
    if not expected_s2:
        s2 = 1.0 if not ans_s2 else max(0.0, 1.0 - 0.5 * len(ans_s2))
    else:
        hits = len(expected_s2 & ans_s2)
        extras = len(ans_s2 - expected_s2)
        s2 = max(0.0, hits / len(expected_s2) - 0.25 * extras)

    # --- S3 percent ---
    s3 = 1.0
    if isinstance(item.get("s3_percent"), (int, float)):
        s3 = 1.0 if isinstance(answer.get("s3_percent"), (int, float)) and abs(item["s3_percent"] - answer["s3_percent"]) <= 15 else 0.0

    # --- Numeric value read from media or computed from the visual prompt ---
    if isinstance(item.get("expected_value"), (int, float)):
        tolerance = item.get("value_tolerance", 0)
        if not isinstance(tolerance, (int, float)):
            tolerance = 0
        try:
            s3 = 1.0 if abs(float(answer.get("value")) - float(item["expected_value"])) <= float(tolerance) else 0.0
        except (TypeError, ValueError):
            s3 = 0.0

    # --- findings / actions ---
    scoped = normalize({
        "findings": answer.get("findings"),
        "actions": answer.get("actions"),
        "s2_conditions": answer.get("s2_conditions"),
    })
    full = normalize(answer)

    req_f = item.get("required_findings", [])
    findings = (sum(1 for g in req_f if group_present(full, g, mode)) / len(req_f)) if req_f else 1.0

    # Set-answer fields, such as workable activity IDs, are scored by F1 so
    # wrong extras cost precision instead of being ignored.
    if item.get("expected_set") is not None:
        expected = {normalize(x) for x in item["expected_set"]}
        got_raw = answer.get(item.get("set_field", "workable")) or []
        got = {normalize(x) for x in got_raw if isinstance(x, str)}
        tp = len(expected & got)
        precision = tp / len(got) if got else 0.0
        recall = tp / len(expected) if expected else 1.0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
        findings = 0.3 * findings + 0.7 * f1

    req_a = item.get("required_actions", [])
    actions = (sum(1 for g in req_a if group_present(full, g, mode)) / len(req_a)) if req_a else 1.0

    # --- forbidden: scoped to conclusions, always AND-groups ---
    forb = item.get("forbidden", [])
    forbidden_hits = sum(1 for g in forb if group_present(scoped, g, "all"))
    forbidden_clean = 1.0 if forbidden_hits == 0 else 0.0

    core = (
        0.10 * schema + 0.25 * decision + 0.10 * risk + 0.05 * s1 +
        0.10 * s2 + 0.05 * s3 + 0.20 * findings + 0.15 * actions
    )
    gate = dangerous_false_pass * alarmist_false_fail * (1.0 if forbidden_hits == 0 else 0.5)
    reward = round(core * gate, 4)

    write_reward({
        "reward": reward, "schema": schema, "decision": decision, "risk": risk,
        "s1": s1, "s2": s2, "s3": s3, "findings": findings, "actions": actions,
        "forbidden_clean": forbidden_clean,
        "dangerous_false_pass": dangerous_false_pass,
        "alarmist_false_fail": alarmist_false_fail,
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
