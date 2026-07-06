# Blue-Collar Benchmark Viewer

Static GitHub Pages viewer for quickly inspecting benchmark sections, tasks, expected answers, media, and latest run results.

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

The JSON payload lives at `docs/viewer/data/viewer-data.json` and is intentionally committed so the viewer does not need a build step or backend.
