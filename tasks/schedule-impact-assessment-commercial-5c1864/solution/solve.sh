#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "pass",
  "risk": "low",
  "work_stage": "in-progress",
  "component_conditions": [],
  "percent_complete": 40,
  "findings": [
    "blocked downstream hold predecessor"
  ],
  "actions": [
    "resequence reassign proceed backlog"
  ],
  "rationale": "The observed condition satisfies the requested acceptance criteria or the disruption is absorbed without a required rejection.",
  "references": [
    "CPM computed ground truth",
    "expansion-plan track 3"
  ],
  "workable": [
    "F",
    "H"
  ]
}
JSON
