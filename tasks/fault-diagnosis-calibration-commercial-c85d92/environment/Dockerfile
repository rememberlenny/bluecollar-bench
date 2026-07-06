FROM python:3.13-slim

WORKDIR /app
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl nodejs npm ripgrep \
    && npm install -g @openai/codex@latest \
    && rm -rf /var/lib/apt/lists/*
# Preinstall claude-code via the native installer so Harbor's claude-code
# agent skips its ~5-minute per-trial install. npm install of the package is
# avoided because its postinstall needs Node >=22 (image ships Debian Node).
RUN HOME=/opt/agent-home bash -c 'curl -fsSL https://downloads.claude.ai/claude-code-releases/bootstrap.sh | bash -s --' \
    && chmod -R a+rX /opt/agent-home \
    && ln -s /opt/agent-home/.local/bin/claude /usr/local/bin/claude
RUN useradd -m agent && mkdir -p /app /logs/verifier /logs/agent && chmod -R 777 /app /logs
