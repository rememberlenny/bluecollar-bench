# Blue-Collar AI Benchmark — Working Docs v0.1

Multimodal eval for trades work: electricians, ironworkers, technicians, assembly workers, mechanics, and more.

## Contents (read in this order)

1. **blue-collar-benchmark-taxonomy-v0.1.md** — The framework. Three axes (Tier × Discipline × Task type), the unified state model (S1 work lifecycle, S2 component condition, S3 progress/rules-of-credit), coverage matrix, and open questions for v0.2.
2. **electrical-element-tree-v0.1.md** — Discipline 2.1 fleshed to element level; the template all other disciplines follow. Defines what counts as an "element" and the per-element schema (Tiers, Task fit, Defect library, Ref).
3. **element-trees-construction-v0.1.md** — Disciplines 2.2–2.6 and 2.11: Piping/Plumbing, HVAC-R, Structural/Iron, Concrete/Masonry, Carpentry/Finishes, Sitework.
4. **element-trees-industrial-service-v0.1.md** — Disciplines 2.7–2.10 and 2.12: Millwright, Instrumentation, Automotive, Assembly/Fab, and the cross-cutting Safety overlay. Ends with the full ~100-element / ~350-defect rollup.
5. **expansion-plan-v0.1-four-new-capability-tracks.md** — Synthetic-parametric expansion plan for radio communications, progress estimation from frame sequences/video, field-constraint diagnosis, and DIY/building-science reasoning.

## Status

- v0.1 = unvalidated first pass. All code/standard references and defect attributions were generated from model knowledge and REQUIRE journeyman/SME red-team review before use.
- Item coding convention: `Tier × Element × Task type` (e.g., `T3 × E-102 × CC`).
- Next planned deliverable: P1 synthetic items and graders for the four expansion tracks, starting with CPM-backed field constraints and DIY/building-science physics.

## Open questions carried into v0.2

1. Skill-level tags (DIY/apprentice/journeyman/master) vs. splitting Tier 3; the expansion plan proposes `skill` and `escalation` item tags for this.
2. Jurisdiction/code-edition tagging
3. Modality tags (photo/video/audio/IR/document) as fourth axis or metadata; the expansion plan treats them as item metadata, including `audio`, `frame-sequence`, and `chart`.
4. True-up CII element definitions if member access is available
