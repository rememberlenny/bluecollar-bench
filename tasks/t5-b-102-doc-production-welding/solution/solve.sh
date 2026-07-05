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
    "installed-defective"
  ],
  "s3_percent": 85,
  "findings": [
    "parameters",
    "outside",
    "window"
  ],
  "actions": [
    "compare",
    "correct",
    "document"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "AWS D1.1/D1.3",
    "shop WPS"
  ]
}
JSON
