#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "fail",
  "risk": "critical",
  "s1_state": "rough-complete",
  "s2_conditions": [
    "installed-defective"
  ],
  "s3_percent": 70,
  "findings": [
    "1910.147 energy verification",
    "unexpected release stored startup"
  ],
  "actions": [
    "identify",
    "document",
    "inspect"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "OSHA 1910.147"
  ]
}
JSON
