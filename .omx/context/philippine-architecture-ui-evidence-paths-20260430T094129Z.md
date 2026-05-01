# Philippine Architecture UI Evidence Paths Context Snapshot

## Task statement
Continue architecture / AEC / LEA-ALE KG and Explorer UI verification work with focused browser-equivalent UI smoke, stronger Filipino/Philippine architecture evidence paths, engineer-architect collaboration paths, and regression protection for bad labels/stale artifacts/highlighting.

## Desired outcome
Learner-facing Explorer remains clean and current; graph gains source-backed Philippine person-work-material/system/movement paths; resolver/API/UI tests prove current data source, clean labels, direct visible-edge highlighting, and source-rights filtering.

## Known facts/evidence
Previous committed baseline at 1e75fd45: 9,834 nodes, 12,970 relationships, 105 source-rights rows, 97 resolver cases; bad learner-facing label hits 0; Kimi final audit approved; no protected payload/live graph mutation.

## Constraints
Use Kimi for advisory/final audit; do not use Codex Spark. No Neo4j/live promotion, KG rebuild/reload/reset, destructive graph ops, protected source ingestion, reviewer/exam/code/table/figure/diagram payload copying. Windows-safe file/path names only.

## Unknowns/open questions
Whether in-app browser tooling is available from this surface; exact current frontend dev-server workflow; which Filipino architects/works already exist and which source-safe additions are highest value.

## Likely codebase touchpoints
scripts/vitruvius/kg/architecture_interconnectivity_enrichment.py; scripts/tests/test_kg_architecture_interconnectivity_enrichment.py; scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json; scripts/tests/fixtures/aec_mepfs_backbone/valid_readiness_s2.json; api/v2Backbone.test.ts; api/v2Resolver.test.ts; explorer graph/component tests; shadow staging reports.
