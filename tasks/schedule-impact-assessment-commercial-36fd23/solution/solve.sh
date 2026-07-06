#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "fail",
  "risk": "medium",
  "work_stage": "in-progress",
  "component_conditions": [],
  "percent_complete": 40,
  "findings": [
    "critical path"
  ],
  "actions": [
    "notify recover resequence crash accelerate"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "CPM computed ground truth",
    "expansion-plan track 3"
  ],
  "value": 2
}
JSON
