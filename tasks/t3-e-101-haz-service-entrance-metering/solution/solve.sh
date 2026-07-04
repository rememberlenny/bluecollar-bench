#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "fail",
  "risk": "critical",
  "s1_state": "in-progress",
  "s2_conditions": [
    "installed-defective",
    "non-compliant"
  ],
  "s3_percent": 45,
  "findings": [
    "service",
    "entrance",
    "unsealed",
    "weatherhead",
    "penetration",
    "hazard"
  ],
  "actions": [
    "stop work",
    "control hazard",
    "verify"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "NEC Art. 230"
  ]
}
JSON
