#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "fail",
  "risk": "critical",
  "s1_state": "planned",
  "s2_conditions": [],
  "s3_percent": 0,
  "findings": [
    "weather limit exceeded",
    "delay lift"
  ],
  "actions": [
    "postpone delay no go"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "OSHA 1926.1400",
    "load charts"
  ]
}
JSON
