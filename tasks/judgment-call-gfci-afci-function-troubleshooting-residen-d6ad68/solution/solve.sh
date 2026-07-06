#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "fail",
  "risk": "high",
  "work_stage": "in-progress",
  "component_conditions": [
    "installed-defective",
    "non-compliant"
  ],
  "percent_complete": 45,
  "findings": [
    "210.8 210.12 line load",
    "protection downstream nuisance shock"
  ],
  "actions": [
    "reject shortcut",
    "follow",
    "document"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "NEC 210.8",
    "210.12"
  ]
}
JSON
