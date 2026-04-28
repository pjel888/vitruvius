---
task: architecture-taxonomy-expansion-audit
phase: AEC-MEPFS taxonomy expansion
status: completed
created: 2026-04-28
---

# Architecture Taxonomy Expansion Audit

## Current implementation surface

Primary authored fixture:

- `scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json`

Generated projections and evidence:

- `006_System-Manifests/aec-mepfs-backbone/shadow-staging/<run-id>/`
- `006_System-Manifests/aec-mepfs-backbone/api-route-inventory/<run-id>/`

## Baseline before this slice

- Latest committed head: `c9499807`
- Latest committed shadow run used by API/Explorer tests: `20260428T063500Z`
- Existing expected counts in tests: 2424 nodes, 2400 edges
- Architecture branch remained narrower than the intended professional taxonomy scope.

## Gap

The user specifically identified Architecture as underpopulated. Official and institutional practice/exam sources show that Architecture needs coverage for theory, history, professional practice, statutory controls, building technology, materials, services, environmental controls, design/site planning, communication, and regional licensing context.

## Risk controls

- Add only metadata-level `BackboneNode` records.
- Keep path depth at existing max depth 4.
- Preserve existing `broader_than` hierarchy pattern.
- Generate file-backed shadow artifacts only.
- Do not touch Neo4j, KG rebuild/reload/reset paths, protected ingest, or production graph promotion.
- Update tests and evidence with exact new counts.

## Audit conclusion

A bounded Architecture branch expansion is safe and aligned with the current AEC-MEPFS taxonomy-first implementation because it only adds rights-safe labels, definitions, aliases, concept anchors, and rule-context anchors to the existing governed fixture.
