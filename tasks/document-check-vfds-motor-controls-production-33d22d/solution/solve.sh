#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "fail",
  "risk": "medium",
  "work_stage": "tested/inspected",
  "component_conditions": [
    "installed-defective"
  ],
  "percent_complete": 85,
  "findings": [
    "430 reactor separation",
    "reflected interference insulation nuisance"
  ],
  "actions": [
    "compare",
    "correct",
    "document"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "NEC 430",
    "mfr manuals"
  ]
}
JSON
