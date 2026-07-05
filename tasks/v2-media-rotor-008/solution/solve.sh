#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "pass",
  "risk": "low",
  "s1_state": "tested/inspected",
  "s2_conditions": [],
  "s3_percent": 90,
  "findings": [
    "above exceeds greater"
  ],
  "actions": [
    "service release document remain"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "OEM specs"
  ],
  "value": 27.08
}
JSON
