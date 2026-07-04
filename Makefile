.PHONY: generate validate harbor-run-one clean

generate:
	python3 scripts/generate_tasks.py

validate:
	python3 scripts/validate_tasks.py

harbor-run-one:
	@test -n "$(AGENT)" || (echo "AGENT is required" >&2; exit 2)
	@test -n "$(MODEL)" || (echo "MODEL is required" >&2; exit 2)
	@test -n "$(TASK)" || (echo "TASK is required" >&2; exit 2)
	scripts/run_harbor.sh --agent "$(AGENT)" --model "$(MODEL)" --task "$(TASK)"

clean:
	rm -rf .harbor runs results
