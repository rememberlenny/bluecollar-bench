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
    "installed-defective"
  ],
  "s3_percent": 45,
  "findings": [
    "work",
    "work",
    "over",
    "sewer",
    "sequence"
  ],
  "actions": [
    "stop",
    "resequence",
    "verify"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "NFPA 51B",
    "OSHA 1926 Subpart J"
  ]
}
JSON
