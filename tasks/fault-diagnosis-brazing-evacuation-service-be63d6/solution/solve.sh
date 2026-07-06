#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "fail",
  "risk": "high",
  "work_stage": "in-service",
  "component_conditions": [
    "degraded",
    "failed"
  ],
  "percent_complete": 100,
  "findings": [
    "nitrogen micron evacuation",
    "oxide moisture acid contamination"
  ],
  "actions": [
    "diagnose",
    "repair",
    "verify"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "mfr specs",
    "ACCA",
    "EPA 608"
  ]
}
JSON
