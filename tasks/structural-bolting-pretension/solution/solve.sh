#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "fail",
  "risk": "high",
  "s1_state": "rough-complete",
  "s2_conditions": [
    "installed-defective",
    "non-compliant"
  ],
  "findings": [
    "pretension",
    "snug tight",
    "wrong grade",
    "match marks"
  ],
  "actions": [
    "verify bolt grade",
    "replace bolts",
    "pretension",
    "inspect"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "RCSC Specification",
    "S-102"
  ]
}
JSON
