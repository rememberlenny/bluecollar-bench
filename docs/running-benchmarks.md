# Running Benchmarks — Runbook

How to run the suite against each provider, which harness to use, and the
failure modes we have actually hit. Every recipe assumes repo root as cwd.

## Which harness for which model

| Model / provider | Harness | Agent | Endpoint | Modalities |
|---|---|---|---|---|
| GPT (gpt-5.5, ...) | Harbor | `codex` | **OpenAI direct** (`api.openai.com`) | text + image |
| Claude (claude-sonnet-5, ...) | Harbor | `claude-code` | Anthropic direct | text + image |
| Gemini (gemini-3.5-flash, ...) | `scripts/run_gemini.py` | — | Vertex (`--backend vertex --auth oauth`) or Developer API | text + image + audio |
| OpenRouter models (GLM, DeepSeek, Kimi, ...) | `scripts/run_openrouter.py` | — | openrouter.ai | text (+ image if the route supports it; audio usually 404s) |

Rules of thumb:

- **GPT goes to OpenAI, not OpenRouter.** The codex agent authenticates with
  `OPENAI_API_KEY` against the default OpenAI endpoint.
  `scripts/run_harbor.sh` automatically unsets `OPENAI_BASE_URL` /
  `OPENAI_API_BASE` for codex runs because a shell-level OpenRouter override
  is forwarded into the agent container and produces silent 401s on every
  trial (set `HARBOR_KEEP_OPENAI_BASE_URL=1` to opt out).
- **claude-code wants bare model ids.** Use `claude-sonnet-5`, not
  `anthropic/claude-sonnet-5` — the CLI rejects provider-prefixed ids at
  runtime ("model may not exist"), which scores 0 on every task while still
  looking like a running job. `run_harbor.sh` strips the `anthropic/` prefix
  automatically.
- **API-only models** (no agent loop) run through the direct harnesses,
  which send instruction + media to the provider, write the JSON reply to
  the task's expected answer path, and run the same local verifier.

## Recipes

Single task:

```bash
scripts/run_harbor.sh --agent codex --model gpt-5.5 --task plumbing-s-trap-vanity
scripts/run_harbor.sh --agent claude-code --model claude-sonnet-5 --task plumbing-s-trap-vanity
python3 scripts/run_gemini.py --model gemini-3.5-flash --auth oauth --backend vertex \
  --location global --google-cloud-project <project> --task plumbing-s-trap-vanity
python3 scripts/run_openrouter.py --model z-ai/glm-5.2 --task plumbing-s-trap-vanity
```

Full suite, direct API (auto-collects when `--collect-run` is given):

```bash
python3 scripts/run_openrouter.py --model deepseek/deepseek-v4-pro \
  --task-list <(python3 -c "import json; print('\n'.join(i['id'] for i in json.load(open('benchmark/items/items.json')) if i.get('modality','text')=='text'))") \
  --temperature 0.0 --max-tokens 1200 \
  --raw-run-dir runs/deepseek_<date> --collect-run deepseek_<date>
```

Full suite, Harbor (agentic): use a job config so the run is reproducible.
Checked-in templates live in `configs/harbor/`:

```bash
.venv/bin/harbor run -c configs/harbor/sonnet5.job.json
env -u OPENAI_BASE_URL -u OPENAI_API_BASE .venv/bin/harbor run -c configs/harbor/gpt55.job.json
```

Then collect and compare:

```bash
python3 scripts/collect_run_results.py jobs/<job_name> <run_name>
python3 scripts/compare_runs.py <base_run> <candidate_run>
python3 scripts/build_static_viewer_data.py   # refresh docs/viewer data
```

Runs collected before the 2026-07 id naturalization are keyed by legacy task
ids; join them to the current catalog through `benchmark/items/id_map.json`
(each item also carries its `legacy_id`).

## Environment requirements

| Variable | Needed by |
|---|---|
| `OPENAI_API_KEY` | codex agent (Harbor GPT runs) |
| `ANTHROPIC_API_KEY` | claude-code agent (Harbor Claude runs) |
| `OPENROUTER_API_KEY` | `run_openrouter.py` |
| gcloud ADC (`gcloud auth application-default login`) | `run_gemini.py --auth oauth --backend vertex` |

Concurrency defaults to 48 everywhere (`run_harbor.sh`, `run_gemini.py`,
`run_openrouter.py`). Two host-level prerequisites for 48-way Harbor runs:

1. **Docker address pools.** Each trial creates a compose network; stock
   Docker only has ~30 pool slots, so concurrent jobs die with "could not
   find an available, non-overlapping IPv4 address pool". Fix in
   `/etc/docker/daemon.json` (then `systemctl restart docker`):

   ```json
   { "default-address-pools": [ { "base": "10.64.0.0/10", "size": 24 } ] }
   ```

2. **AppArmor.** codex needs `apparmor=unconfined` on this host to create
   its signal socket; the GPT job config applies a compose overlay
   (`configs/harbor/apparmor-unconfined.compose.yaml`) for this.

## Task image

The generated task image (see `DOCKERFILE` in `scripts/generate_tasks.py`)
preinstalls both agents so Harbor's per-trial installer is skipped:

- codex via `npm install -g @openai/codex@latest`
- claude-code via Anthropic's native bootstrap installer into
  `/opt/agent-home`, symlinked to `/usr/local/bin/claude` (the npm package
  is avoided because its postinstall requires Node >= 22, newer than the
  image's Debian Node)

Before the preinstall, each claude-code trial spent ~5 minutes on
`apt-get + install`; after it, trial overhead is seconds and a full
1,299-task agentic suite finishes in about an hour at 48-way concurrency.

## Failure modes we have hit (and their signatures)

| Symptom | Cause | Fix |
|---|---|---|
| Every codex trial 0.0, transcript shows 401s against `openrouter.ai/api/v1/responses` | `OPENAI_BASE_URL` pointing at OpenRouter leaked into the container | Unset it (automatic in `run_harbor.sh`) |
| Every claude-code trial 0.0, result says "issue with the selected model (anthropic/...)" | Provider-prefixed model id | Use bare id (automatic in `run_harbor.sh`) |
| Trials fail instantly with "could not find an available, non-overlapping IPv4 address pool" | Docker network pool exhausted at high concurrency | daemon.json address pools (above) |
| Harbor image build fails, npm EACCES on `@anthropic-ai/claude-code` postinstall | Package needs Node >= 22 | Native bootstrap installer (already in the Dockerfile) |
| Vertex HTTP 429 on a slice of tasks | Gemini quota at 48-way | Delete the failed task dirs, rerun with `--skip-existing` |
| OpenRouter HTTP 404 "No endpoints found" on media tasks | Model route has no image/audio input support | Run text-only (`--task-list`), or accept 0s and read text-slice metrics |

A model that errors on every task still produces a complete-looking run —
zero rewards are indistinguishable from hard tasks in the progress counts.
**Always check that early rewards are non-zero** before letting a long run
continue (`find jobs/<job> -name reward.json | head` and inspect a few).
