# KG-first cleanup planning context

## Task statement
Plan a safe cleanup/refactor of Vitruvius from the old raw-source -> raw-conversion -> canonical-knowledge pipeline-first model toward the current KG-first model.

## Desired outcome
Create a plan folder under `.ai/03_plans/` with a blast-radius-aware cleanup plan. Do not delete or refactor production code yet.

## Known facts/evidence
- AEC-MEPFS taxonomy backbone is now file-backed and scaffold-free at commit e4fe2aff.
- Current fixture has 8935 records, 8911 relationships, and 0 L4 scaffold labels.
- Old pipeline code still exists for scan/convert/OCR/canonical/promote workflows.

## Constraints
- Planning only; no destructive cleanup yet.
- Preserve source ingestion/evidence extraction capabilities.
- No protected source payload exposure.
- No Neo4j/KG mutation.
- Use GitNexus/code graph/chunkhound availability where possible.

## Unknowns/open questions
- Which old pipeline modules are still imported by tests/CLI/runtime?
- Which docs still present the old layer model as primary truth?
- Which code should be kept, moved, deprecated, or deleted later?

## Likely codebase touchpoints
- `scripts/pipeline_cli.py`
- `scripts/vitruvius/`
- `scripts/tests/`
- `.ai/01_roadmap/`
- `.ai/03_plans/`
- README/docs references to six-layer pipeline
