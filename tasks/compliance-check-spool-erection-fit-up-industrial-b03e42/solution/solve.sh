#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "fail",
  "risk": "high",
  "work_stage": "rough-complete",
  "component_conditions": [
    "installed-defective",
    "non-compliant"
  ],
  "percent_complete": 70,
  "findings": [
    "b31 isometric alignment",
    "stress strain leak fitup"
  ],
  "actions": [
    "correct",
    "inspect",
    "before acceptance"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "ASME B31.3",
    "project iso drawings"
  ]
}
JSON
