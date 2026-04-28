---
task: aec-mepfs-all-taxonomy-deep-population
phase: AEC-MEPFS taxonomy expansion
status: BOUNDARY_APPROVED
created: 2026-04-29
---

# AEC-MEPFS All-Taxonomy Deep Population Packet

## Authority

Project-owner request on 2026-04-29: continuously expand all AEC-MEPFS taxonomies with topics, subtopics, concepts, rules, history, laws, MEPFS, security, smart systems, and other professional domains using online research, local research, and raw-source filename signals.

## Allowed scope

- Add rights-safe `BackboneNode` metadata topics across all existing root taxonomies.
- Add L2 topic families, L3 subtopics, and L4 concept/rule-context anchors.
- Use public source structures and local raw-source filenames as taxonomy inspiration only.
- Regenerate file-backed shadow staging, shadow graph, consumer report, route inventory, and taxonomy-expansion report.
- Update focused Python/API/Explorer test count and run-id assertions.
- Update roadmap/plan status documentation.

## Blocked scope

- No protected source-text, table, figure, clause, dataset, standard-payload, or exam-question ingestion.
- No Neo4j mutation.
- No KG rebuild/reload/reset.
- No production graph promotion.
- No API runtime behavior change.
- No Explorer runtime behavior change.
- No source-rights/currentness claim based only on file presence.

## Implementation plan

1. Use OMX read-only team workers plus web research to identify all-domain gaps.
2. Append deterministic L2/L3/L4 `BackboneNode` records using existing fixture schema.
3. Generate run `20260428T174344Z` shadow staging, graph, consumer report, and route inventory.
4. Generate taxonomy-expansion report for the all-domain slice.
5. Update focused count/run-id assertions in Python/API/Explorer tests.
6. Run focused and affected broad tests.
7. Run safety greps and Kimi advisory review.
8. Commit and push when verified.

## Expected expansion

- Add 1908 new `BackboneNode` records.
- New total fixture counts:
  - 4605 `BackboneNode` records
  - 4581 `broader_than` relationships
  - 24 roots
  - max depth 4
- New level counts:
  - L1: 24
  - L2: 399
  - L3: 1394
  - L4: 2788

## Verification plan

- `PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_contracts.py -q`
- `PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_shadow_staging.py scripts/tests/test_kg_backbone_api_route_inventory.py -q`
- `bun --cwd api test v2Backbone.test.ts`
- `bun --cwd explorer test src/app.searchInspector.integration.test.tsx src/components/componentInteraction.test.tsx src/components/graph/VisNetworkHost.test.ts`
- `bun --cwd api test`
- `bun --cwd explorer test`
- `git diff --check`

## Rollback

Git revert this slice. Generated evidence is timestamped under `20260428T174344Z` and can be ignored or removed by revert without affecting prior run `20260428T144427Z`.
