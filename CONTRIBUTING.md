# Contributing

This benchmark is safety-sensitive. Treat source items as hypotheses until a qualified SME review has confirmed them.

## Item Requirements

- Use a concrete, inspectable scenario.
- Include tier, discipline, element, task type, S1 state, expected S2 conditions, decision, and risk.
- Prefer defects that are visible or directly inferable from the scenario.
- Include source anchors such as standards, code articles, OEM procedures, drawings, or manufacturer instructions.
- Avoid jurisdiction-specific claims unless the scenario states the jurisdiction or code edition.

## Validation

Run this before opening a PR:

```bash
make generate
make validate
```

Generated task directories should be committed so Harbor users can run the benchmark without regenerating it first.
