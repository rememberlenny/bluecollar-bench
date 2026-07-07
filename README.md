# Blue-Collar Benchmark Viewer

Static GitHub Pages viewer for quickly inspecting benchmark sections, tasks, expected answers, media, collected run results, and extracted model answers.

Current committed snapshot:

- 1,299 tasks
- 6 naturalized-catalog model runs in the viewer payload (superseded and stale coded-catalog runs are excluded)
- 2,670 scored result entries
- 2,492 extracted model-answer payloads

The full collected-run registry under `benchmark/runs/` may contain additional runs that are not in the viewer snapshot when their catalog hash or task coverage does not line up with the committed viewer payload. See `benchmark/runs/model_results_summary_20260706.md` for the latest documented run summary.

Regenerate the embedded data snapshot after catalog or run updates:

```bash
python3 scripts/build_static_viewer_data.py
```

The source viewer entrypoint is:

```text
docs/viewer/index.html
```

The deployed GitHub Pages URL is:

```text
https://rememberlenny.github.io/bluecollar-bench/
```

The JSON payload lives at `docs/viewer/data/viewer-data.json` and is intentionally committed so the viewer does not need a build step or backend. The viewer is a static shadcn-token styled page; it does not require React, Vite, Tailwind, or a Pages build step.
