---
task: weird-zoom-interaction-taxonomy-fixes
phase: 00
created: 2026-04-30
author: PLANNER
supersedes: null
status: ACCEPTED
---

# Trigger and scope

Task: Fix Explorer graph interaction/navigation defects and add rights-safe AEC-MEPFS organizational metadata for architects, laws, standards, and architect-engineer overlaps.

## In scope
- Explorer graph interaction and camera behavior.
- AEC-MEPFS file-backed `/expand` behavior.
- Node inspector breadcrumbs.
- Existing AEC-MEPFS metadata-only enrichment scripts/tests/fixtures.

## Out of scope
- Production Neo4j mutation or promotion.
- Protected content ingestion.
- Raw source writes.
- Dependency additions.

## Risk
M - multi-file Explorer/API/data changes within current AEC-MEPFS file-backed surface.

## MCP precheck
GitNexus query and impact checks required for changed symbols. Graph exploration used before manual inspection.
