---
task: kg-first-cleanup
phase: cleanup-planning-index
created: 2026-04-29
author: CODEX
status: PLANNED_NOT_IMPLEMENTED
---

# KG-First Cleanup Plan Folder

This folder is the planning surface for cleaning up Vitruvius after the product
shift from a layer-first document pipeline toward a KG-first workflow.

The cleanup target is **not** to delete useful ingestion/extraction machinery.
It is to stop presenting the old raw -> conversion -> canonical path as the
primary product architecture when the current product direction is:

1. authored AEC-MEPFS knowledge graph/backbone first,
2. attach sources, evidence spans, and provenance to graph nodes,
3. index raw/source materials as evidence inputs,
4. expose file-backed/API/Explorer graph surfaces, and
5. keep production Neo4j/protected payload gates explicit.

## Planning Artifacts

| File | Purpose | Status |
|---|---|---|
| `2026-04-29_research_pack.md` | Tool-backed discovery summary from GitNexus, OMX Explore, ChunkHound, and local code inspection. | complete |
| `2026-04-29_blast_radius_audit.md` | Cleanup blast-radius map, keep/deprecate/delete-later candidates, and risk classification. | complete |
| `2026-04-29_cleanup_strategy_plan.md` | Phased cleanup strategy and guarded execution sequence. | complete |
| `2026-04-29_plan_critique.md` | Adversarial critique of the cleanup strategy before implementation. | complete |
| `2026-04-29_execution_checklist.md` | Gate checklist for the first implementation slice after planning. | complete |
| `2026-04-29_validation_log.md` | Evidence log for this planning-only pass. | complete |

## Non-Goals For This Planning Pass

- No product code refactor.
- No deletion of legacy pipeline code.
- No filesystem layer rename.
- No raw/canonical evidence deletion.
- No KG rebuild/reload/reset.
- No Neo4j mutation.
- No protected source ingest or payload exposure.
- No API or Explorer behavior change.

## First Safe Implementation Direction

The first cleanup implementation slice should be documentation and operator
surface reconciliation only: update live docs and CLI descriptions so the legacy
pipeline is described as **source ingestion/evidence preparation** beneath the
KG-first architecture. Do not delete or move runtime code until regression tests
pin the old behavior and GitNexus impact analysis is rerun for the exact edited
symbols.
