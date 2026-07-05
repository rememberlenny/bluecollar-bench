# Codex Full Suite Run - 2026-07-04

## Summary

- Agent/model: `codex` / `openai/gpt-5`
- Task directories reviewed: `977`
- Unique tasks with a successful result: `977`
- Remaining unrun or only-failed tasks: `0`
- Superseded exception result files from interrupted/failed attempts: `203`
- Reported Harbor cost sum across listed jobs: `$34.166294`

## Validation

- `make validate` passed: `Validated 977 task(s).`

## Jobs

| Job | Completed | Errored | Cancelled | Cost USD |
| --- | ---: | ---: | ---: | ---: |
| `codex-full-suite` | 89 | 6 | 6 | 2.768699 |
| `codex-full-suite-remaining` | 114 | 27 | 27 | 2.911552 |
| `codex-full-suite-remaining-64` | 320 | 51 | 51 | 9.681555 |
| `codex-full-suite-remaining-128` | 235 | 109 | 109 | 4.307564 |
| `codex-full-suite-remaining-128b` | 356 | 7 | 2 | 12.293589 |
| `codex-full-suite-final-7` | 7 | 0 | 0 | 0.194049 |
| `codex-full-suite-final-media-56` | 56 | 3 | 0 | 1.918655 |
| `codex-full-suite-final-media-3` | 3 | 0 | 0 | 0.090631 |

## Reconciliation

Every current `tasks/*/task.toml` directory has at least one successful Harbor result. Earlier exception files were from interrupted or superseded attempts and are not counted as final coverage gaps.
