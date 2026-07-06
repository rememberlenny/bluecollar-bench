FROM python:3.13-slim

WORKDIR /app
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl nodejs npm ripgrep \
    && npm install -g @openai/codex@latest \
    && rm -rf /var/lib/apt/lists/*
RUN useradd -m agent && mkdir -p /app /logs/verifier /logs/agent && chmod -R 777 /app /logs
