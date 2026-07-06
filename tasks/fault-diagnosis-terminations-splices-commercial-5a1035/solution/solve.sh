#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "fail",
  "risk": "critical",
  "work_stage": "in-service",
  "component_conditions": [
    "installed-defective"
  ],
  "percent_complete": 100,
  "findings": [
    "crackle sizzle irregular arcing"
  ],
  "actions": [
    "de-energize deenergize electrician immediately"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "NEC 110.14"
  ],
  "sound_source": "electrical panel",
  "confidence": 1.0
}
JSON
