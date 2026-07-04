# Blue-Collar AI Benchmark — Working Docs v0.1

Multimodal eval for trades work: electricians, ironworkers, technicians, assembly workers, mechanics, and more.

## Contents (read in this order)

1. **blue-collar-benchmark-taxonomy-v0.1.md** — The framework. Three axes (Tier × Discipline × Task type), the unified state model (S1 work lifecycle, S2 component condition, S3 progress/rules-of-credit), coverage matrix, and open questions for v0.2.
2. **electrical-element-tree-v0.1.md** — Discipline 2.1 fleshed to element level; the template all other disciplines follow. Defines what counts as an "element" and the per-element schema (Tiers, Task fit, Defect library, Ref).
3. **element-trees-construction-v0.1.md** — Disciplines 2.2–2.6 and 2.11: Piping/Plumbing, HVAC-R, Structural/Iron, Concrete/Masonry, Carpentry/Finishes, Sitework.
4. **element-trees-industrial-service-v0.1.md** — Disciplines 2.7–2.10 and 2.12: Millwright, Instrumentation, Automotive, Assembly/Fab, and the cross-cutting Safety overlay. Ends with the full ~100-element / ~350-defect rollup.

## Status

- v0.1 = unvalidated first pass. All code/standard references and defect attributions were generated from model knowledge and REQUIRE journeyman/SME red-team review before use.
- Item coding convention: `Tier × Element × Task type` (e.g., `T3 × E-102 × CC`).
- Next planned deliverable: item templates + scoring rubrics (incl. "partially right but dangerous = fail" rule).

## Open questions carried into v0.2

1. Skill-level tags (DIY/apprentice/journeyman/master) vs. splitting Tier 3
2. Jurisdiction/code-edition tagging
3. Modality tags (photo/video/audio/IR/document) as fourth axis or metadata
4. True-up CII element definitions if member access is available
