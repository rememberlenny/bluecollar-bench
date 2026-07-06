# Blue-Collar Benchmark Viewer

Static GitHub Pages viewer for quickly inspecting benchmark sections, tasks, expected answers, media, and latest run results.

Regenerate the embedded data snapshot after catalog or run updates:

```bash
python3 scripts/build_static_viewer_data.py
```

The viewer entrypoint is:

```text
docs/viewer/index.html
```

Common GitHub Pages URLs:

- If Pages serves `docs/`: `https://rememberlenny.github.io/bluecollar-bench/viewer/`
- If Pages serves the repository root: `https://rememberlenny.github.io/bluecollar-bench/docs/viewer/`

The JSON payload lives at `docs/viewer/data/viewer-data.json` and is intentionally committed so the viewer does not need a build step or backend.
