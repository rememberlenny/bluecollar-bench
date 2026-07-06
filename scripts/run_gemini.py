#!/usr/bin/env python3
"""Run bluecollar-bench tasks directly against the Google Gemini API.

The harness calls Gemini's generateContent REST API, writes the model response
to each task's expected /app/answer.json location, and runs the existing task
verifier locally. Raw outputs are compatible with scripts/collect_run_results.py
because reward.json paths include the task id.
"""
from __future__ import annotations

import argparse
import base64
import concurrent.futures
import json
import mimetypes
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TASKS_DIR = ROOT / "tasks"
ITEMS_PATH = ROOT / "benchmark" / "items" / "items.json"
GEMINI_API_BASE = "https://generativelanguage.googleapis.com/v1beta"
VERTEX_API_VERSION = "v1"

SYSTEM_PROMPT = """You are running a blue-collar trade-work benchmark task.
Return exactly one valid JSON object matching the requested answer schema.
Do not include prose, Markdown, code fences, or commentary outside JSON."""

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
AUDIO_EXTENSIONS = {".wav", ".mp3", ".aiff", ".aac", ".ogg", ".flac", ".m4a"}
MIME_OVERRIDES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
    ".gif": "image/gif",
    ".wav": "audio/wav",
    ".mp3": "audio/mpeg",
    ".aiff": "audio/aiff",
    ".aac": "audio/aac",
    ".ogg": "audio/ogg",
    ".flac": "audio/flac",
    ".m4a": "audio/mp4",
}


@dataclass(frozen=True)
class TaskSpec:
    task_id: str
    path: Path


@dataclass
class TaskResult:
    task_id: str
    ok: bool
    reward: float
    output_dir: Path
    error: str | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--model",
        required=True,
        help="Gemini model id or resource path, e.g. gemini-2.5-pro, models/gemini-3.5-flash",
    )
    parser.add_argument("--task", action="append", default=[], help="Task id or tasks/<id>; repeatable")
    parser.add_argument("--task-list", type=Path, help="File containing one task id per line")
    parser.add_argument("--all", action="store_true", help="Run every task in benchmark/items/items.json")
    parser.add_argument("--limit", type=int, help="Limit selected tasks after expansion")
    parser.add_argument("--raw-run-dir", type=Path, help="Directory for per-task raw outputs")
    parser.add_argument("--collect-run", help="Also collect raw rewards into benchmark/runs/<name>")
    parser.add_argument("--overwrite", action="store_true", help="Replace an existing raw run directory")
    parser.add_argument("--skip-existing", action="store_true", help="Skip tasks that already have reward.json")
    parser.add_argument("--n-concurrent", "-n", type=int, default=1, help="Parallel Gemini requests")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--max-tokens", type=int, default=8192, help="Gemini maxOutputTokens")
    parser.add_argument("--thinking-budget", type=int, help="Optional Gemini thinkingBudget")
    parser.add_argument("--timeout", type=float, default=180.0, help="HTTP timeout in seconds")
    parser.add_argument("--retries", type=int, default=2, help="Retries after the first API attempt")
    parser.add_argument(
        "--auth",
        choices=["api-key", "oauth"],
        default="api-key",
        help="Use an API key or a gcloud Application Default Credentials OAuth bearer token",
    )
    parser.add_argument(
        "--backend",
        choices=["developer", "vertex"],
        default="developer",
        help="Use Gemini Developer API or Google Cloud Vertex/Agent Platform endpoint",
    )
    parser.add_argument(
        "--location",
        default=os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1"),
        help="Google Cloud location for --backend vertex",
    )
    parser.add_argument(
        "--google-cloud-project",
        default=os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCLOUD_PROJECT"),
        help="Quota/billing project for OAuth requests; defaults to GOOGLE_CLOUD_PROJECT",
    )
    parser.add_argument(
        "--api-key-env",
        default="GEMINI_API_KEY",
        help="Environment variable holding the Gemini API key; GOOGLE_API_KEY is also accepted by default",
    )
    parser.add_argument("--no-response-mime-type", action="store_true", help="Do not request application/json output")
    parser.add_argument("--dry-run", action="store_true", help="Build requests and directories without calling Gemini")
    return parser.parse_args()


def load_catalog_task_ids() -> list[str]:
    items = json.loads(ITEMS_PATH.read_text(encoding="utf-8"))
    return [item["id"] for item in items]


def normalize_task_id(value: str) -> str:
    value = value.strip()
    if not value or value.startswith("#"):
        return ""
    return Path(value).name if "/" in value else value


def selected_tasks(args: argparse.Namespace) -> list[TaskSpec]:
    ids: list[str] = []
    if args.all:
        ids.extend(load_catalog_task_ids())
    ids.extend(normalize_task_id(task) for task in args.task)
    if args.task_list:
        lines = args.task_list.read_text(encoding="utf-8").splitlines()
        ids.extend(normalize_task_id(line) for line in lines)

    ids = [task_id for task_id in ids if task_id]
    if not ids:
        raise SystemExit("Pass at least one --task, --task-list, or --all.")

    seen: set[str] = set()
    specs: list[TaskSpec] = []
    for task_id in ids:
        if task_id in seen:
            continue
        seen.add(task_id)
        task_path = TASKS_DIR / task_id
        if not task_path.exists():
            raise SystemExit(f"Unknown task: {task_id} ({task_path} does not exist)")
        specs.append(TaskSpec(task_id=task_id, path=task_path))

    if args.limit is not None:
        if args.limit < 1:
            raise SystemExit("--limit must be >= 1")
        specs = specs[: args.limit]
    return specs


def safe_model_name(model: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "-", model).strip("-")


def default_raw_dir(model: str) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    return ROOT / "runs" / f"gemini_{safe_model_name(model)}_{stamp}"


def read_media_paths(task: TaskSpec) -> list[Path]:
    item = json.loads((task.path / "tests" / "item.json").read_text(encoding="utf-8"))
    paths: list[Path] = []
    for name in item.get("media", []):
        candidate = task.path / "environment" / "media" / name
        if not candidate.exists():
            raise FileNotFoundError(f"media file missing for {task.task_id}: {candidate}")
        paths.append(candidate)
    return paths


def mime_type(path: Path) -> str:
    suffix = path.suffix.lower()
    return MIME_OVERRIDES.get(suffix) or mimetypes.guess_type(path.name)[0] or "application/octet-stream"


def inline_part(path: Path) -> dict[str, Any]:
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return {"inlineData": {"mimeType": mime_type(path), "data": encoded}}


def build_user_parts(task: TaskSpec) -> list[dict[str, Any]]:
    instruction = (task.path / "instruction.md").read_text(encoding="utf-8")
    parts: list[dict[str, Any]] = [{"text": instruction}]
    for media_path in read_media_paths(task):
        suffix = media_path.suffix.lower()
        if suffix not in IMAGE_EXTENSIONS and suffix not in AUDIO_EXTENSIONS:
            raise ValueError(f"unsupported media type for {task.task_id}: {media_path}")
        parts.append(inline_part(media_path))
    return parts


def build_payload(task: TaskSpec, args: argparse.Namespace) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": [{"role": "user", "parts": build_user_parts(task)}],
        "generationConfig": {
            "temperature": args.temperature,
            "maxOutputTokens": args.max_tokens,
        },
    }
    if not args.no_response_mime_type:
        payload["generationConfig"]["responseMimeType"] = "application/json"
    if args.thinking_budget is not None:
        payload["generationConfig"]["thinkingConfig"] = {"thinkingBudget": args.thinking_budget}
    return payload


def api_key(args: argparse.Namespace) -> str:
    key = os.environ.get(args.api_key_env)
    if not key and args.api_key_env == "GEMINI_API_KEY":
        key = os.environ.get("GOOGLE_API_KEY")
    if not key and args.auth == "api-key" and not args.dry_run:
        fallback = " or GOOGLE_API_KEY" if args.api_key_env == "GEMINI_API_KEY" else ""
        raise SystemExit(f"{args.api_key_env}{fallback} is not set")
    return key or "dry-run"


def oauth_token(args: argparse.Namespace) -> str:
    if args.dry_run:
        return "dry-run"
    try:
        return subprocess.check_output(
            ["gcloud", "auth", "application-default", "print-access-token"],
            text=True,
            stderr=subprocess.PIPE,
        ).strip()
    except FileNotFoundError as exc:
        raise SystemExit("gcloud is required for --auth oauth") from exc
    except subprocess.CalledProcessError as exc:
        message = exc.stderr.strip() or "failed to print Application Default Credentials access token"
        raise SystemExit(message) from exc


def developer_model_path(model: str) -> str:
    known_prefixes = ("models/", "tunedModels/", "projects/")
    return model if model.startswith(known_prefixes) else f"models/{model}"


def vertex_model_path(model: str, args: argparse.Namespace) -> str:
    project = args.google_cloud_project
    if not project and not args.dry_run:
        raise SystemExit("--google-cloud-project or GOOGLE_CLOUD_PROJECT is required for --backend vertex")
    if model.startswith("projects/"):
        return model
    if model.startswith("publishers/") or model.startswith("endpoints/"):
        return f"projects/{project}/locations/{args.location}/{model}"
    if "/" in model and not model.startswith("models/"):
        publisher, model_id = model.split("/", 1)
        return f"projects/{project}/locations/{args.location}/publishers/{publisher}/models/{model_id}"
    model_id = model.removeprefix("models/")
    return f"projects/{project}/locations/{args.location}/publishers/google/models/{model_id}"


def endpoint(model: str, args: argparse.Namespace, key: str | None = None) -> str:
    if args.backend == "vertex":
        quoted_model = urllib.parse.quote(vertex_model_path(model, args), safe="/")
        host = "https://aiplatform.googleapis.com" if args.location == "global" else f"https://{args.location}-aiplatform.googleapis.com"
        return f"{host}/{VERTEX_API_VERSION}/{quoted_model}:generateContent"

    quoted_model = urllib.parse.quote(developer_model_path(model), safe="/")
    url = f"{GEMINI_API_BASE}/{quoted_model}:generateContent"
    if args.auth == "api-key":
        query = urllib.parse.urlencode({"key": key or api_key(args)})
        return f"{url}?{query}"
    return url


def manifest_endpoint(model: str, args: argparse.Namespace) -> str:
    if args.backend == "vertex":
        return endpoint(model, args)
    quoted_model = urllib.parse.quote(developer_model_path(model), safe="/")
    return f"{GEMINI_API_BASE}/{quoted_model}:generateContent"


def request_headers(args: argparse.Namespace, token: str | None = None) -> dict[str, str]:
    headers = {"Content-Type": "application/json"}
    if args.backend == "vertex" and args.auth != "oauth":
        raise SystemExit("--backend vertex requires --auth oauth")
    if args.auth == "oauth":
        project = args.google_cloud_project
        if not project and not args.dry_run:
            raise SystemExit("--google-cloud-project or GOOGLE_CLOUD_PROJECT is required for --auth oauth")
        headers["Authorization"] = f"Bearer {token or oauth_token(args)}"
        if project:
            headers["x-goog-user-project"] = project
    return headers


def call_gemini(payload: dict[str, Any], args: argparse.Namespace, key: str | None, token: str | None) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    last_error: str | None = None
    for attempt in range(args.retries + 1):
        request = urllib.request.Request(
            endpoint(args.model, args, key),
            data=body,
            headers=request_headers(args, token),
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=args.timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            error_body = exc.read().decode("utf-8", errors="replace")
            last_error = f"HTTP {exc.code}: {error_body}"
        except Exception as exc:  # noqa: BLE001 - preserve API failure text for run audit
            last_error = str(exc)
        if attempt < args.retries:
            time.sleep(min(2**attempt, 8))
    raise RuntimeError(last_error or "Gemini request failed")


def response_text(response: dict[str, Any]) -> str:
    candidates = response.get("candidates") or []
    if not candidates:
        return ""
    content = candidates[0].get("content") or {}
    parts = content.get("parts") or []
    texts = [part.get("text", "") for part in parts if isinstance(part, dict)]
    return "\n".join(text for text in texts if text)


def strip_code_fence(text: str) -> str:
    stripped = text.strip()
    match = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", stripped, flags=re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else stripped


def first_json_object(text: str) -> str:
    stripped = strip_code_fence(text)
    try:
        json.loads(stripped)
        return stripped
    except json.JSONDecodeError:
        pass

    start = stripped.find("{")
    if start == -1:
        return stripped

    depth = 0
    in_string = False
    escape = False
    for index, char in enumerate(stripped[start:], start=start):
        if in_string:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                candidate = stripped[start : index + 1]
                try:
                    json.loads(candidate)
                    return candidate
                except json.JSONDecodeError:
                    return stripped
    return stripped


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_grader(task: TaskSpec, app_dir: Path, logs_dir: Path) -> None:
    env = os.environ.copy()
    env.update({
        "BLUECOLLAR_APP_DIR": str(app_dir),
        "BLUECOLLAR_LOG_DIR": str(logs_dir / "verifier"),
        "BLUECOLLAR_ITEM_PATH": str(task.path / "tests" / "item.json"),
    })
    subprocess.run(
        [sys.executable, str(task.path / "tests" / "grade.py")],
        cwd=task.path,
        env=env,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def run_one(task: TaskSpec, raw_dir: Path, args: argparse.Namespace, key: str | None, token: str | None) -> TaskResult:
    task_out = raw_dir / task.task_id / "trial_000"
    reward_path = task_out / "logs" / "verifier" / "reward.json"
    if args.skip_existing and reward_path.exists():
        metrics = json.loads(reward_path.read_text(encoding="utf-8"))
        return TaskResult(task.task_id, True, float(metrics.get("reward", 0.0)), task_out)

    task_out.mkdir(parents=True, exist_ok=True)
    payload = build_payload(task, args)
    write_json(task_out / "request.json", payload)

    app_dir = task_out / "app"
    logs_dir = task_out / "logs"
    app_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    try:
        if args.dry_run:
            answer_text = "{}"
            response: dict[str, Any] = {"dry_run": True}
        else:
            response = call_gemini(payload, args, key, token)
            answer_text = response_text(response)

        write_json(task_out / "response.json", response)
        (task_out / "answer.raw.txt").write_text(answer_text, encoding="utf-8")
        extracted = first_json_object(answer_text)
        (app_dir / "answer.json").write_text(extracted.strip() + "\n", encoding="utf-8")
        shutil.copy2(app_dir / "answer.json", task_out / "answer.json")
        run_grader(task, app_dir, logs_dir)

        metrics = json.loads(reward_path.read_text(encoding="utf-8")) if reward_path.exists() else {}
        return TaskResult(task.task_id, True, float(metrics.get("reward", 0.0)), task_out)
    except Exception as exc:  # noqa: BLE001 - record per-task failures and continue the run
        error = str(exc)
        (task_out / "error.txt").write_text(error + "\n", encoding="utf-8")
        if not reward_path.exists():
            reward_path.parent.mkdir(parents=True, exist_ok=True)
            write_json(reward_path, {"reward": 0.0})
        return TaskResult(task.task_id, False, 0.0, task_out, error=error)


def prepare_raw_dir(raw_dir: Path, overwrite: bool, skip_existing: bool) -> None:
    if raw_dir.exists() and overwrite:
        shutil.rmtree(raw_dir)
    if raw_dir.exists() and any(raw_dir.iterdir()) and not overwrite and not skip_existing:
        raise SystemExit(f"{raw_dir} already exists and is not empty; pass --overwrite or choose --raw-run-dir")
    raw_dir.mkdir(parents=True, exist_ok=True)


def collect_run(raw_dir: Path, run_name: str) -> None:
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "collect_run_results.py"), str(raw_dir), run_name],
        cwd=ROOT,
        check=True,
    )


def main() -> int:
    args = parse_args()
    specs = selected_tasks(args)
    raw_dir = (args.raw_run_dir or default_raw_dir(args.model)).resolve()
    prepare_raw_dir(raw_dir, args.overwrite, args.skip_existing)
    key = api_key(args) if args.auth == "api-key" else None
    token = oauth_token(args) if args.auth == "oauth" else None

    manifest = {
        "schema_version": 1,
        "runner": "gemini",
        "model": args.model,
        "backend": args.backend,
        "endpoint": manifest_endpoint(args.model, args),
        "auth": args.auth,
        "google_cloud_project": args.google_cloud_project if args.auth == "oauth" else None,
        "location": args.location if args.backend == "vertex" else None,
        "created_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "tasks_requested": [spec.task_id for spec in specs],
        "n_concurrent": args.n_concurrent,
        "temperature": args.temperature,
        "max_tokens": args.max_tokens,
        "thinking_budget": args.thinking_budget,
        "response_mime_type": None if args.no_response_mime_type else "application/json",
        "dry_run": args.dry_run,
    }
    write_json(raw_dir / "manifest.json", manifest)

    print(f"Gemini raw run: {raw_dir}")
    print(f"Tasks: {len(specs)}; model: {args.model}; concurrency: {args.n_concurrent}")

    results: list[TaskResult] = []
    workers = max(1, args.n_concurrent)
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_task = {
            executor.submit(run_one, spec, raw_dir, args, key, token): spec
            for spec in specs
        }
        for future in concurrent.futures.as_completed(future_to_task):
            result = future.result()
            results.append(result)
            status = "ok" if result.ok else "failed"
            print(f"{status}\t{result.task_id}\treward={result.reward:.4f}")

    results.sort(key=lambda result: result.task_id)
    summary = {
        "schema_version": 1,
        "tasks": len(results),
        "ok": sum(1 for result in results if result.ok),
        "failed": sum(1 for result in results if not result.ok),
        "mean_reward": sum(result.reward for result in results) / len(results) if results else 0.0,
        "rows": [
            {
                "task": result.task_id,
                "ok": result.ok,
                "reward": result.reward,
                "output_dir": str(result.output_dir),
                "error": result.error,
            }
            for result in results
        ],
    }
    write_json(raw_dir / "summary.json", summary)

    print(f"Summary: {summary['ok']} ok, {summary['failed']} failed, mean reward {summary['mean_reward']:.4f}")
    if args.collect_run:
        collect_run(raw_dir, args.collect_run)
    return 1 if summary["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
