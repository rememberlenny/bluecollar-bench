.PHONY: generate media audio restore validate dataset collect-run compare-runs harbor-run-one clean

generate:
	python3 scripts/build_item_catalog.py
	python3 scripts/gen_text_rebalance_items.py
	python3 scripts/generate_tasks_v2.py

media:
	$$(test -x .venv/bin/python && echo .venv/bin/python || echo python3) scripts/gen_media_items.py

audio:
	$$(test -x .venv/bin/python && echo .venv/bin/python || echo python3) scripts/gen_audio_items.py

restore:
	python3 scripts/restore_scenarios.py

validate:
	python3 scripts/validate_tasks.py

dataset:
	@test -x ".venv/bin/harbor" || command -v harbor >/dev/null || (echo "harbor is required" >&2; exit 127)
	@tmp_dir=$$(mktemp -d); \
	harbor_bin=$$(command -v harbor || echo .venv/bin/harbor); \
	$$harbor_bin init --dataset bluecollar-bench/blue-collar-benchmark --description "Comprehensive blue-collar trade-work evaluation tasks" --author "Blue-Collar Benchmark Maintainers" --output-dir "$$tmp_dir"; \
	$$harbor_bin add tasks --scan --to "$$tmp_dir"; \
	mv "$$tmp_dir/dataset.toml" dataset.toml; \
	rm -rf "$$tmp_dir"

collect-run:
	@test -n "$(RUNS_DIR)" || (echo "RUNS_DIR is required" >&2; exit 2)
	@test -n "$(RUN_NAME)" || (echo "RUN_NAME is required" >&2; exit 2)
	python3 scripts/collect_run_results.py "$(RUNS_DIR)" "$(RUN_NAME)"

compare-runs:
	@test -n "$(BASE_RUN)" || (echo "BASE_RUN is required" >&2; exit 2)
	@test -n "$(CANDIDATE_RUN)" || (echo "CANDIDATE_RUN is required" >&2; exit 2)
	python3 scripts/compare_runs.py "$(BASE_RUN)" "$(CANDIDATE_RUN)"

harbor-run-one:
	@test -n "$(AGENT)" || (echo "AGENT is required" >&2; exit 2)
	@test -n "$(MODEL)" || (echo "MODEL is required" >&2; exit 2)
	@test -n "$(TASK)" || (echo "TASK is required" >&2; exit 2)
	scripts/run_harbor.sh --agent "$(AGENT)" --model "$(MODEL)" --task "$(TASK)"

clean:
	rm -rf .harbor runs results
