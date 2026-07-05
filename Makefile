.PHONY: generate media validate dataset harbor-run-one clean

generate:
	python3 scripts/build_item_catalog.py
	python3 scripts/generate_tasks_v2.py

media:
	$$(test -x .venv/bin/python && echo .venv/bin/python || echo python3) scripts/gen_media_items.py

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

harbor-run-one:
	@test -n "$(AGENT)" || (echo "AGENT is required" >&2; exit 2)
	@test -n "$(MODEL)" || (echo "MODEL is required" >&2; exit 2)
	@test -n "$(TASK)" || (echo "TASK is required" >&2; exit 2)
	scripts/run_harbor.sh --agent "$(AGENT)" --model "$(MODEL)" --task "$(TASK)"

clean:
	rm -rf .harbor runs results
