#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "fail",
  "risk": "high",
  "s1_state": "tested/inspected",
  "s2_conditions": [
    "worn"
  ],
  "s3_percent": 90,
  "findings": [
    "below under less"
  ],
  "actions": [
    "replace"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "OEM specs"
  ],
  "value": 26.68
}
JSON
