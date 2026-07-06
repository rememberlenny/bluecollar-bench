#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  scripts/run_harbor.sh --agent <agent> --model <model> [--task <task-id>] [--n-concurrent N] [--extra "..."]

Examples:
  scripts/run_harbor.sh --agent codex --model openai/gpt-5 --task electrical-panel-subpanel-defects
  scripts/run_harbor.sh --agent claude-code --model anthropic/claude-sonnet-4-6 --n-concurrent 8

If --task is omitted, the repository dataset.toml is run as a Harbor dataset.
EOF
}

AGENT=""
MODEL=""
TASK_ID=""
N_CONCURRENT="48"
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
    --n-concurrent|-n)
      N_CONCURRENT="$2"
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

# GPT/codex runs go directly to OpenAI. A shell-level OPENAI_BASE_URL override
# (e.g. pointing at OpenRouter) is forwarded into agent containers by Harbor
# and silently breaks codex auth, so drop it for codex runs. Set
# HARBOR_KEEP_OPENAI_BASE_URL=1 to opt out of this hygiene.
if [[ "$AGENT" == codex* && -z "${HARBOR_KEEP_OPENAI_BASE_URL:-}" ]]; then
  if [[ -n "${OPENAI_BASE_URL:-}${OPENAI_API_BASE:-}" ]]; then
    echo "note: unsetting OPENAI_BASE_URL/OPENAI_API_BASE for codex (direct OpenAI)" >&2
    unset OPENAI_BASE_URL OPENAI_API_BASE
  fi
fi

# The claude CLI expects bare Anthropic model ids (claude-sonnet-5), not
# provider-prefixed ones (anthropic/claude-sonnet-5), which it rejects at
# runtime with a model-not-found error.
if [[ "$AGENT" == claude-code* ]]; then
  MODEL="${MODEL#anthropic/}"
fi

if command -v harbor >/dev/null 2>&1; then
  HARBOR_BIN="$(command -v harbor)"
elif [[ -x ".venv/bin/harbor" ]]; then
  HARBOR_BIN=".venv/bin/harbor"
else
  echo "harbor is not installed. Install with: uv tool install harbor" >&2
  exit 127
fi

if [[ -n "$TASK_ID" ]]; then
  echo "==> harbor run -p tasks/$TASK_ID -a $AGENT -m $MODEL"
  "$HARBOR_BIN" run -p "tasks/$TASK_ID" -a "$AGENT" -m "$MODEL" -n "$N_CONCURRENT" "${EXTRA_ARGS[@]}"
else
  echo "==> harbor run -p . -a $AGENT -m $MODEL -n $N_CONCURRENT"
  "$HARBOR_BIN" run -p . -a "$AGENT" -m "$MODEL" -n "$N_CONCURRENT" "${EXTRA_ARGS[@]}"
fi
