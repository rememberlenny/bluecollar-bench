#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  scripts/run_harbor.sh --agent <agent> --model <model> [--task <task-id>] [--extra "..."]

Examples:
  scripts/run_harbor.sh --agent codex --model openai/gpt-5 --task electrical-panel-subpanel-defects
  scripts/run_harbor.sh --agent claude-code --model anthropic/claude-sonnet-4-6

If --task is omitted, every task under tasks/ is run sequentially.
EOF
}

AGENT=""
MODEL=""
TASK_ID=""
EXTRA_ARGS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --agent)
      AGENT="$2"
      shift 2
      ;;
    --model)
      MODEL="$2"
      shift 2
      ;;
    --task)
      TASK_ID="$2"
      shift 2
      ;;
    --extra)
      # shellcheck disable=SC2206
      EXTRA_ARGS=($2)
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ -z "$AGENT" || -z "$MODEL" ]]; then
  usage >&2
  exit 2
fi

if ! command -v harbor >/dev/null 2>&1; then
  echo "harbor is not installed. Install with: uv tool install harbor" >&2
  exit 127
fi

run_one() {
  local task_path="$1"
  echo "==> harbor run -p $task_path -a $AGENT -m $MODEL"
  harbor run -p "$task_path" -a "$AGENT" -m "$MODEL" "${EXTRA_ARGS[@]}"
}

if [[ -n "$TASK_ID" ]]; then
  run_one "tasks/$TASK_ID"
else
  for task_path in tasks/*; do
    [[ -d "$task_path" ]] || continue
    run_one "$task_path"
  done
fi
