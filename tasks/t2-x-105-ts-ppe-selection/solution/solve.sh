#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "fail",
  "risk": "critical",
  "s1_state": "staged",
  "s2_conditions": [
    "installed-defective"
  ],
  "s3_percent": 15,
  "findings": [
    "70e category class",
    "arc flash exposure inadequate"
  ],
  "actions": [
    "replace",
    "select",
    "verify"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "NFPA 70E",
    "OSHA 1910 Subpart I"
  ]
}
JSON
