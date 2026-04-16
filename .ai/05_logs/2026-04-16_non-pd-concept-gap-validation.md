# 2026-04-16 Non-PD Concept Coverage Gap Validation

## Purpose
Record the fresh evidence explaining why `BP-344` and `BP-220` remain `partial` after M2A source admission and M2B dataset-safe stage wiring.

## Fresh evidence
### BP-220
Dataset-safe extraction / review evidence:
- extraction file: `006_System-Manifests/runs/datasets/laws-core-bundle-m1/check-Revised_IRR_BP220_/extract.json`
- triage file: `006_System-Manifests/runs/datasets/laws-core-bundle-m1/check-Revised_IRR_BP220_/triage.json`
- review file: `006_System-Manifests/runs/datasets/laws-core-bundle-m1/check-Revised_IRR_BP220_/review.json`

Observed result:
- sections: `47`
- extracted relationships: `3`
- high-confidence admitted relationships: `0`

Why:
- extracted candidates mapped onto existing PD-1096-centric concepts in ways that do not survive even deterministic triage, e.g.:
  - `concept-floor-area requires concept-setbacks`
  - `concept-stairs requires concept-setbacks`
  - `concept-means-of-egress defines concept-stairs`
- these are structurally weak for BP-220 and are rejected as unsupported or registry-incompatible.

### BP-344
Dataset-safe extraction / review evidence:
- extraction file: `006_System-Manifests/runs/datasets/laws-core-bundle-m1/m2b-bp344-v1/extract.json`
- triage file: `006_System-Manifests/runs/datasets/laws-core-bundle-m1/m2b-bp344-v1/triage.json`
- review file: `006_System-Manifests/runs/datasets/laws-core-bundle-m1/m2b-bp344-v1/review.json`

Observed result:
- sections: `5`
- extracted relationships: `3`
- high-confidence admitted relationships: `0`

Why:
- source→concept `governs` candidates target generic PD-1096 concepts (`stairs`, `means-of-egress`) with evidence snippets that are accessibility-oriented but not yet specific enough for automatic truth admission
- one concept→concept candidate (`means-of-egress requires stairs`) remains too weak / indirect and routes to review_further rather than keep

### RA-9514 contrast
- `RA-9514` extraction quality improved enough to yield real dataset-safe admissions
- after manual audit, 2 promoted RA-9514 relationships were admitted and the law is now `covered`

## Conclusion
The current limiting factor for `BP-344` and `BP-220` is no longer source admission or dataset-safe stage wiring.

It is **concept coverage / concept fit**:
- the current shared concept set is still dominated by PD-1096 concepts
- non-PD laws are being forced into concept mappings that are often too generic or semantically off-target
- further truthful progress likely requires either:
  1. admission of additional law-appropriate concepts, or
  2. more conservative extraction logic keyed to the currently admitted concept set

## Current truthful official state
From the latest official scoped graph report:
- `PD-1096` → `covered`
- `RA-9514` → `covered`
- `BP-344` → `partial`
- `BP-220` → `partial`
