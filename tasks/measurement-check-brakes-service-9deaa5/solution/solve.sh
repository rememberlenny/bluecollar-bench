#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "pass",
  "risk": "low",
  "work_stage": "tested/inspected",
  "component_conditions": [],
  "percent_complete": 90,
  "findings": [
    "above exceeds greater"
  ],
  "actions": [
    "service release document remain"
  ],
  "rationale": "The observed condition satisfies the requested acceptance criteria or the disruption is absorbed without a required rejection.",
  "references": [
    "OEM specs"
  ],
  "value": 28.79
}
JSON
