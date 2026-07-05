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
  "s3_percent": 5,
  "findings": [
    "oxygen o2 deficient"
  ],
  "actions": [
    "no entry ventilate prohibit"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "OSHA 1910.146"
  ]
}
JSON
