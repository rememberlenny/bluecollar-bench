#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "fail",
  "risk": "medium",
  "s1_state": "rough-complete",
  "s2_conditions": [
    "installed-defective"
  ],
  "s3_percent": 70,
  "findings": [
    "boxes",
    "fittings",
    "free",
    "conductor"
  ],
  "actions": [
    "identify",
    "document",
    "inspect"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "NEC 314.16",
    "300.14",
    "314.28 (pull box sizing)"
  ]
}
JSON
