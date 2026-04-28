---
task: architecture-licensure-taxonomy-expansion
phase: AEC-MEPFS taxonomy expansion
status: BOUNDARY_APPROVED
created: 2026-04-28
---

# Architecture Licensure Taxonomy Expansion Packet

## Authority

Project-owner request on 2026-04-28: expand the Architecture taxonomy using licensure/professional subject structures from the Philippines, Hong Kong, Singapore, Indonesia, Thailand, and repo research.

## Allowed scope

- Add rights-safe Architecture `BackboneNode` topics under `ARC`.
- Add L3 subtopics and L4 `Concepts` / `Rule Context` anchors.
- Use public source structures as taxonomy inspiration only.
- Regenerate file-backed shadow staging and route inventory evidence.
- Update focused tests/count assertions.

## Blocked scope

- No protected source-text, table, figure, clause, exam-question, or standard-payload ingestion.
- No Neo4j mutation.
- No KG rebuild/reload/reset.
- No production graph promotion.
- No Explorer behavior change in this slice.
- No API runtime behavior change in this slice.

## Implementation plan

1. Research official/institution subject families and repo taxonomy governance research.
2. Append Architecture L2/L3/L4 records under `ARC` using existing fixture schema.
3. Generate run `20260428T144427Z` shadow staging, graph, consumer report, and route inventory.
4. Update expected count/run-id assertions in focused Python/API/Explorer tests.
5. Produce validation/evidence artifacts.
6. Run focused tests and safety checks.

## Expected expansion

- Add 273 new Architecture records:
  - 21 L2 topic families
  - 84 L3 subtopics
  - 168 L4 concept/rule-context anchors
- New total fixture counts after applying this slice:
  - 2697 `BackboneNode` records
  - 2673 `broader_than` relationships
  - 24 roots
  - max depth 4
- Architecture branch after expansion:
  - 374 records total
  - 1 L1 root
  - 31 L2 topics
  - 114 L3 subtopics
  - 228 L4 anchors

## Verification plan

- `PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_contracts.py -q`
- `PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_shadow_staging.py scripts/tests/test_kg_backbone_api_route_inventory.py -q`
- `bun --cwd api test v2Backbone.test.ts`
- `bun --cwd explorer test src/app.searchInspector.integration.test.tsx src/components/componentInteraction.test.tsx src/components/graph/VisNetworkHost.test.ts`
- `git diff --check`

## Rollback

Git revert this slice. Generated evidence is timestamped under `20260428T144427Z` and can be ignored or removed by revert without affecting prior run `20260428T063500Z`.
