#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${BLUECOLLAR_APP_DIR:-/app}"
mkdir -p "$APP_DIR"
cat > "$APP_DIR/answer.json" <<'JSON'
{
  "decision": "fail",
  "risk": "critical",
  "s1_state": "in-service",
  "s2_conditions": [
    "installed-defective",
    "non-compliant"
  ],
  "findings": [
    "return air garage",
    "vent clearance combustible",
    "condensate slope"
  ],
  "actions": [
    "shut down",
    "relocate return",
    "correct vent clearance",
    "repipe condensate"
  ],
  "rationale": "The scenario contains visible defects or hazards that make the work unacceptable until corrected.",
  "references": [
    "IRC M1801",
    "NFPA 54",
    "H-102"
  ]
}
JSON
