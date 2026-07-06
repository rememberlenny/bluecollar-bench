#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "pass",
  "risk": "low",
  "work_stage": "rough-complete",
  "component_conditions": [],
  "percent_complete": 90,
  "findings": [
    "recognized",
    "serviceable",
    "undamaged"
  ],
  "actions": [
    "document",
    "release"
  ],
  "rationale": "The observed condition satisfies the requested acceptance criteria or the disruption is absorbed without a required rejection.",
  "references": [
    "NEC Art. 408",
    "110.26 (working clearance)",
    "200.4"
  ]
}
JSON
