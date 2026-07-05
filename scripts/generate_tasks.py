#!/usr/bin/env python3
"""Generate Harbor task directories from benchmark/items/items.json."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path


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
    s2 = ", ".join(item["s2_expected"]) or "none"
    media = item.get("media") or []
    lines = [
        f"# {item['title']}",
        "",
        "You are evaluating a blue-collar trade-work scenario. Produce a concise, inspection-grade answer in `/app/answer.json`.",
        "",
        "## Item metadata",
        "",
        f"- ID: `{item['id']}`",
        f"- Tier: `{item['tier']}`",
        f"- Discipline: `{item['discipline']}`",
        f"- Element: `{item['element']}`",
        f"- Task type: `{item['task_type']}`",
        f"- Expected lifecycle state to assess: `{item['s1_state']}`",
        f"- Relevant S2 condition classes: `{s2}`",
        f"- Modality: `{item.get('modality', 'text')}`",
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
            '  "s1_state": "planned | staged | in-progress | rough-complete | tested/inspected | rework | accepted | in-service",',
            '  "s2_conditions": ["installed-defective", "non-compliant", "worn", "degraded", "failed"],',
            '  "s3_percent": 0,',
            '  "value": 0,',
            '  "workable": ["activity ID", "..."],',
            '  "findings": ["short defect or hazard finding", "..."],',
            '  "actions": ["immediate corrective action", "..."],',
            '  "rationale": "brief explanation",',
            '  "references": ["code or standard anchors you relied on"]',
            "}",
            "```",
            "",
            "Do not write prose outside the JSON file. If the work is dangerous or non-compliant, `decision` must be `fail`.",
            "Use `value` for the numeric reading or computed quantity when the task asks for one.",
            "Use `workable` for a list of activity IDs when the task asks what work can still start.",
            "",
            "## Source anchors",
            "",
            "These anchors are provided for context; apply them to the scenario rather than quoting them mechanically.",
            "",
        ]
    )
    lines.extend(f"- {ref}" for ref in item["source_refs"])
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
        "s1_state": item["s1_state"],
        "s2_conditions": item["s2_expected"],
        "s3_percent": item.get("s3_percent"),
        "findings": [" ".join(group) for group in item["required_findings"]],
        "actions": [" ".join(group) for group in item["required_actions"]],
        "rationale": rationale,
        "references": item["source_refs"],
    }
    if isinstance(item.get("expected_value"), (int, float)):
        answer["value"] = item["expected_value"]
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
    expected_value_present = isinstance(expected_value, (int, float))
    value_tolerance_present = isinstance(value_tolerance, (int, float))
    expected_value_toml = str(float(expected_value)) if expected_value_present else "0.0"
    value_tolerance_toml = str(float(value_tolerance)) if value_tolerance_present else "0.0"
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
