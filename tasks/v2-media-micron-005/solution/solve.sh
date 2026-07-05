#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "fail",
  "risk": "medium",
  "s1_state": "tested/inspected",
  "s2_conditions": [
    "non-compliant"
  ],
  "s3_percent": 90,
  "findings": [
    "moisture dehydrate stall"
  ],
  "actions": [
    "evacuate triple continue"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "EPA 608",
    "mfr specs"
  ],
  "value": 1318
}
JSON
