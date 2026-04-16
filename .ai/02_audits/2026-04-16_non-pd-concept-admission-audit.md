# Audit — Non-PD Concept Admission Slice

## Core finding
The remaining partial status for `BP-344` and `BP-220` is no longer caused by missing source pages or missing dataset-safe stage wiring. It is caused by concept mismatch.

The smallest honest fix is **not** broad concept expansion. It is a tiny law-specific concept-admission slice followed by whitelisted extraction.

## Why this is safer than broad concept admission
- reduces accidental concept-to-concept false positives
- keeps the blast radius small
- allows per-law validation after each concept addition
- preserves the ability to stop if the first concept still does not produce truthful candidates

## Recommended first slice
- admit `accessible ramps` for `BP-344`
- admit `socialized housing projects` for `BP-220`
- add extraction support for explicit concept-path filtering so dataset-safe runs can focus on those concepts only

## Blast radius
Likely touched:
- `scripts/vitruvius/concepts/__init__.py` only via existing CLI usage, not code changes
- `scripts/vitruvius/relationships_sections.py`
- `scripts/pipeline_cli.py`
- targeted extractor tests
- concept markdown files under `003_Canonical-Knowledge-Layer/shared/concepts/`

## Audit verdict
Proceedable as a bounded slice.
