#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "fail",
  "risk": "high",
  "s1_state": "in-service",
  "s2_conditions": [
    "degraded",
    "failed"
  ],
  "s3_percent": 100,
  "findings": [
    "play specification wear",
    "alignment separation control camber"
  ],
  "actions": [
    "diagnose",
    "repair",
    "verify"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "OEM",
    "alignment specs"
  ]
}
JSON
