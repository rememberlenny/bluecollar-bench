#!/usr/bin/env python3
"""Generate Harbor task directories from benchmark/items/items.json."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import naturalize_items as nat  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]
ITEMS_PATH = ROOT / "benchmark" / "items" / "items.json"
TASKS_DIR = ROOT / "tasks"
ORG = "bluecollar-bench"


DOCKERFILE = """\
FROM python:3.13-slim

WORKDIR /app
RUN apt-get update \\
    && apt-get install -y --no-install-recommends ca-certificates curl nodejs npm ripgrep \\
    && npm install -g @openai/codex@latest \\
    && rm -rf /var/lib/apt/lists/*
RUN useradd -m agent && mkdir -p /app /logs/verifier /logs/agent && chmod -R 777 /app /logs
"""


GRADE_PY = r'''#!/usr/bin/env python3
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

    schema_fields = ["decision", "risk", "s1_state", "s2_conditions", "findings", "actions"]
    schema_score = sum(1 for field in schema_fields if field in answer) / len(schema_fields)
    text = flatten_answer(answer)

    decision_text = normalize(answer.get("decision", ""))
    decision_score = 1.0 if normalize(item["decision"]) == decision_text else 0.0

    risk_text = normalize(answer.get("risk", ""))
    risk_score = 1.0 if normalize(item["risk"]) == risk_text else 0.0

    state_text = normalize(answer.get("s1_state", ""))
    state_score = 1.0 if normalize(item["s1_state"]) == state_text else 0.0

    s2_text = flatten_answer({"s2_conditions": answer.get("s2_conditions", [])})
    expected_s2 = item.get("s2_expected", [])
    s2_hits = sum(1 for condition in expected_s2 if normalize(condition) in s2_text)
    s2_score = s2_hits / max(1, len(expected_s2))

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
        + 0.10 * state_score
        + 0.10 * s2_score
        + 0.25 * findings_score
        + 0.05 * actions_score
    )
    reward = min(raw_reward, safety_gate)

    write_reward({
        "reward": round(reward, 4),
        "schema": round(schema_score, 4),
        "decision": round(decision_score, 4),
        "risk": round(risk_score, 4),
        "s1_state": round(state_score, 4),
        "s2_conditions": round(s2_score, 4),
        "findings": round(findings_score, 4),
        "actions": round(actions_score, 4),
        "safety_gate": round(safety_gate, 4),
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''


TEST_SH = """\
#!/usr/bin/env bash
set +e
mkdir -p /logs/verifier
python3 /tests/grade.py
exit 0
"""


def render_instruction(item: dict) -> str:
    s2 = ", ".join(f"`{c}`" for c in item["s2_expected"]) or "none flagged — judge from the evidence"
    media = item.get("media") or []
    stage = item["s1_state"]
    stage_phrase = nat.S1_PHRASE.get(stage, stage)
    lines = [
        f"# {item['title']}",
        "",
        "You are assessing real trade work the way a competent tradesperson or inspector would.",
        "Read the situation below and write your conclusions to `/app/answer.json`.",
        "",
        "## Context",
        "",
        f"- Setting: {nat.TIER_SETTING[item['tier']]}",
        f"- Trade: {nat.discipline_name(item)}",
        f"- Scope under review: {nat.element_name(item)}",
        f"- Your task: {nat.TASK_PHRASE[item['task_type']]}",
        f"- Stage of the work when observed: `{stage}` ({stage_phrase})",
        f"- Component condition categories that may apply: {s2}",
        "",
        "## Scenario",
        "",
        item["scenario"],
        "",
    ]
    if media:
        lines.extend(["## Media", ""])
        for entry in media:
            if isinstance(entry, str):
                media_path = entry
                media_type = item.get("modality", "media")
                media_alt = ""
            else:
                media_path = entry.get("path", "")
                media_type = entry.get("type", item.get("modality", "media"))
                media_alt = entry.get("alt", "")
            label = f"- `/app/media/{media_path}` ({media_type})"
            if media_alt:
                label += f": {media_alt}"
            lines.append(label)
        lines.append("")
    lines.extend(
        [
            "## Task",
            "",
            item["prompt"],
            "",
            "## Required output",
            "",
            "Write valid JSON to `/app/answer.json` with this shape:",
            "",
            "```json",
            "{",
            '  "decision": "pass | fail | needs_more_info",',
            '  "risk": "low | medium | high | critical",',
            '  "work_stage": "planned | staged | in-progress | rough-complete | tested/inspected | rework | accepted | in-service",',
            '  "component_conditions": ["installed-defective", "non-compliant", "worn", "degraded", "failed"],',
            '  "percent_complete": 0,',
            '  "value": 0,',
            '  "sound_source": "component or source of the sound, when asked",',
            '  "confidence": 0.0,',
            '  "event_time": 0.0,',
            '  "rate": 0.0,',
            '  "order": ["step-id", "..."],',
            '  "workable": ["activity ID", "..."],',
            '  "findings": ["short defect or hazard finding", "..."],',
            '  "actions": ["immediate corrective action", "..."],',
            '  "rationale": "brief explanation",',
            '  "references": ["code or standard anchors you relied on"]',
            "}",
            "```",
            "",
            "Do not write prose outside the JSON file. If the work is dangerous or non-compliant, `decision` must be `fail`.",
            "`work_stage` is how far the work has progressed; `percent_complete` is your numeric estimate of overall progress.",
            "`component_conditions` lists the condition categories that apply to the component; use an empty list if none apply.",
            "Use `value` for the numeric reading or computed quantity when the task asks for one.",
            "Use `sound_source`, `event_time`, `rate`, and `order` for audio/video-native tasks when requested.",
            "Use `workable` for a list of activity IDs when the task asks what work can still start.",
        ]
    )
    refs = nat.external_refs(item)
    if refs:
        lines.extend(
            [
                "",
                "## Reference material",
                "",
                "Apply these to the scenario rather than quoting them mechanically.",
                "",
            ]
        )
        lines.extend(f"- {ref}" for ref in refs)
    return "\n".join(lines) + "\n"


def render_solution(item: dict) -> str:
    decision = item["decision"]
    if decision == "pass":
        rationale = "The observed condition satisfies the requested acceptance criteria or the disruption is absorbed without a required rejection."
    elif decision == "needs_more_info":
        rationale = "The available evidence is insufficient to make the requested determination without additional information."
    else:
        rationale = "The scenario contains visible defects or hazards that make the work unacceptable until corrected."

    answer = {
        "decision": decision,
        "risk": item["risk"],
        "work_stage": item["s1_state"],
        "component_conditions": item["s2_expected"],
        "percent_complete": item.get("s3_percent"),
        "findings": [" ".join(group) for group in item["required_findings"]],
        "actions": [" ".join(group) for group in item["required_actions"]],
        "rationale": rationale,
        "references": item["source_refs"],
    }
    if isinstance(item.get("expected_value"), (int, float)):
        answer["value"] = item["expected_value"]
    if isinstance(item.get("expected_rate"), (int, float)):
        answer["rate"] = item["expected_rate"]
    if isinstance(item.get("expected_event_time"), (int, float)):
        answer["event_time"] = item["expected_event_time"]
    if isinstance(item.get("expected_order"), list):
        answer["order"] = item["expected_order"]
    if isinstance(item.get("expected_sound_source"), str):
        answer["sound_source"] = item["expected_sound_source"]
    elif isinstance(item.get("expected_sound_source"), list) and item["expected_sound_source"]:
        answer["sound_source"] = item["expected_sound_source"][0]
    if any(key in item for key in ["expected_sound_source", "expected_rate", "expected_event_time", "expected_order"]):
        answer["confidence"] = 1.0
    if item.get("expected_set") is not None:
        answer[item.get("set_field", "workable")] = item["expected_set"]
    payload = json.dumps(answer, indent=2)
    return f"""#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${{BLUECOLLAR_APP_DIR:-/app}}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{payload}
JSON
"""


def render_task_toml(item: dict) -> str:
    keywords = [
        "blue-collar",
        "trades",
        item["tier"].lower(),
        item["task_type"].lower(),
        item.get("discipline_code", "").replace(".", "-"),
    ]
    keywords_toml = ", ".join(json.dumps(k) for k in keywords)
    source_refs = ", ".join(json.dumps(ref) for ref in item["source_refs"])
    media_refs = ", ".join(json.dumps(entry if isinstance(entry, str) else entry.get("path", "")) for entry in item.get("media", []))
    expected_value = item.get("expected_value")
    value_tolerance = item.get("value_tolerance")
    expected_rate = item.get("expected_rate")
    rate_tolerance = item.get("rate_tolerance")
    expected_event_time = item.get("expected_event_time")
    event_time_tolerance = item.get("event_time_tolerance")
    expected_value_present = isinstance(expected_value, (int, float))
    value_tolerance_present = isinstance(value_tolerance, (int, float))
    expected_rate_present = isinstance(expected_rate, (int, float))
    rate_tolerance_present = isinstance(rate_tolerance, (int, float))
    expected_event_time_present = isinstance(expected_event_time, (int, float))
    event_time_tolerance_present = isinstance(event_time_tolerance, (int, float))
    expected_value_toml = str(float(expected_value)) if expected_value_present else "0.0"
    value_tolerance_toml = str(float(value_tolerance)) if value_tolerance_present else "0.0"
    expected_rate_toml = str(float(expected_rate)) if expected_rate_present else "0.0"
    rate_tolerance_toml = str(float(rate_tolerance)) if rate_tolerance_present else "0.0"
    expected_event_time_toml = str(float(expected_event_time)) if expected_event_time_present else "0.0"
    event_time_tolerance_toml = str(float(event_time_tolerance)) if event_time_tolerance_present else "0.0"
    expected_order = ", ".join(json.dumps(step) for step in item.get("expected_order", []))
    expected_sound_source = json.dumps(item.get("expected_sound_source", ""))
    confusable_with = json.dumps(item.get("confusable_with", ""))
    reduction_test = json.dumps(item.get("reduction_test", ""))
    return textwrap.dedent(
        f"""\
        schema_version = "1.3"

        [task]
        name = "{ORG}/{item["id"]}"
        description = "{item["title"]}"
        authors = [{{ name = "Blue-Collar Benchmark Maintainers" }}]
        keywords = [{keywords_toml}]

        [metadata]
        benchmark = "blue-collar-benchmark"
        benchmark_version = "0.1"
        item_id = "{item["id"]}"
        tier = "{item["tier"]}"
        discipline = "{item["discipline"]}"
        element = "{item["element"]}"
        task_type = "{item["task_type"]}"
        task_type_name = "{item.get("task_type_name", item["task_type"])}"
        s1_state = "{item["s1_state"]}"
        s3_percent = {float(item.get("s3_percent", 0))}
        expected_decision = "{item["decision"]}"
        expected_risk = "{item["risk"]}"
        modality = "{item.get("modality", "text")}"
        media = [{media_refs}]
        expected_value_present = {str(expected_value_present).lower()}
        expected_value = {expected_value_toml}
        value_tolerance = {value_tolerance_toml}
        expected_rate_present = {str(expected_rate_present).lower()}
        expected_rate = {expected_rate_toml}
        rate_tolerance = {rate_tolerance_toml}
        expected_event_time_present = {str(expected_event_time_present).lower()}
        expected_event_time = {expected_event_time_toml}
        event_time_tolerance = {event_time_tolerance_toml}
        expected_order = [{expected_order}]
        expected_sound_source = {expected_sound_source}
        confusable_with = {confusable_with}
        reduction_test = {reduction_test}
        generation = "{item.get("generation", "unknown")}"
        source_refs = [{source_refs}]

        [agent]
        timeout_sec = 300.0
        user = "agent"

        [verifier]
        timeout_sec = 120.0
        user = "root"

        [environment]
        network_mode = "public"
        build_timeout_sec = 600.0
        cpus = 1
        memory_mb = 1024
        storage_mb = 2048
        """
    )


def generate() -> None:
    if not ITEMS_PATH.exists():
        subprocess.run([sys.executable, str(ROOT / "scripts" / "build_item_catalog.py")], cwd=ROOT, check=True)
    items = json.loads(ITEMS_PATH.read_text(encoding="utf-8"))
    if TASKS_DIR.exists():
        shutil.rmtree(TASKS_DIR)
    TASKS_DIR.mkdir(parents=True)

    for item in items:
        task_dir = TASKS_DIR / item["id"]
        (task_dir / "environment").mkdir(parents=True)
        (task_dir / "tests").mkdir()
        (task_dir / "solution").mkdir()

        (task_dir / "instruction.md").write_text(render_instruction(item), encoding="utf-8")
        (task_dir / "task.toml").write_text(render_task_toml(item), encoding="utf-8")
        (task_dir / "environment" / "Dockerfile").write_text(DOCKERFILE, encoding="utf-8")
        (task_dir / "tests" / "grade.py").write_text(GRADE_PY, encoding="utf-8")
        (task_dir / "tests" / "test.sh").write_text(TEST_SH, encoding="utf-8")
        (task_dir / "tests" / "item.json").write_text(json.dumps(item, indent=2, sort_keys=True), encoding="utf-8")
        (task_dir / "solution" / "solve.sh").write_text(render_solution(item), encoding="utf-8")

        for script in [task_dir / "tests" / "test.sh", task_dir / "tests" / "grade.py", task_dir / "solution" / "solve.sh"]:
            script.chmod(0o755)

    print(f"Generated {len(items)} Harbor tasks in {TASKS_DIR}")


if __name__ == "__main__":
    generate()
