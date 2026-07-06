#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "fail",
  "risk": "critical",
  "work_stage": "planned",
  "component_conditions": [],
  "percent_complete": 0,
  "findings": [
    "exceeds over above overload"
  ],
  "actions": [
    "rerig shorten longer higher rated stop"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "ASME B30.9",
    "OSHA 1926.251"
  ],
  "value": 3536
}
JSON
