---
task: architecture-licensure-taxonomy-expansion-validation
phase: AEC-MEPFS taxonomy expansion
status: completed
created: 2026-04-28
---

# Architecture Licensure Taxonomy Expansion Validation

## Scope

Expanded only the rights-safe Architecture (`ARC`) branch of the AEC-MEPFS backbone using public licensure, registration, professional-practice, and curriculum structures as topic signals.

## Branch and commit state

- Branch: `main`
- Starting commit: `c9499807` (`Make Explorer edges visually lighter`)
- Run ID: `20260428T144427Z`
- Final commit: to be recorded by git history for this validation slice

## Files inspected

- `.ai/01_roadmap/current-phase.md`
- `.ai/01_roadmap/milestone-tracker.md`
- `.ai/13_research/governed taxonomy/deep-research-report.md`
- `.ai/13_research/AECMEPFS++/deep-research-report.md`
- `scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json`
- `scripts/tests/test_kg_backbone_contracts.py`
- `api/v2Backbone.test.ts`
- `explorer/src/app.searchInspector.integration.test.tsx`
- `explorer/src/components/componentInteraction.test.tsx`

## Files changed

- `.ai/01_roadmap/current-phase.md`
- `.ai/01_roadmap/milestone-tracker.md`
- `.ai/02_audits/2026-04-28_architecture_taxonomy_expansion_audit.md`
- `.ai/03_plans/INDEX.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/README.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-28_architecture_licensure_taxonomy_expansion_packet.md`
- `.ai/05_logs/2026-04-28_architecture_licensure_taxonomy_expansion_validation.md`
- `.ai/13_research/2026-04-28_architecture_licensure_taxonomy_research.md`
- `scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json`
- `scripts/tests/test_kg_backbone_contracts.py`
- `api/v2Backbone.test.ts`
- `explorer/src/app.searchInspector.integration.test.tsx`
- `explorer/src/components/componentInteraction.test.tsx`
- `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260428T144427Z/`
- `006_System-Manifests/aec-mepfs-backbone/api-route-inventory/20260428T144427Z/`
- `006_System-Manifests/aec-mepfs-backbone/taxonomy-expansion/20260428T144427Z/architecture-taxonomy-expansion-report.json`

## Implementation summary

- Added 273 Architecture `BackboneNode` records:
  - 21 L2 professional topic families
  - 84 L3 subtopics
  - 168 L4 concept/rule-context anchors
- New total fixture count: 2697 nodes and 2673 `broader_than` relationships.
- New Architecture branch count: 374 nodes, with 31 L2 topics, 114 L3 subtopics, and 228 L4 anchors.
- Added topic coverage for theory, history, professional practice, building technology, materials, site planning, environmental controls, sustainability, urban design, accessibility, fire life safety, codes, BIM, studio methods, programming, advanced typologies, housing, detailing, conservation, communication, and regional practice/licensure.
- Regenerated file-backed shadow staging, shadow graph, consumer report, and route inventory for run `20260428T144427Z`.

## Commands run

```bash
git status --short --branch
git rev-parse --short HEAD
git log --oneline -n 8
omx explore --prompt "Map the AEC-MEPFS Architecture taxonomy fixture and tests impacted by expanding ARC path nodes. Return file paths, count assertions, and regeneration commands only."
rg -n "2424|2400|20260428T063500Z|BackboneNode|Architecture total|ARC\." scripts/tests api explorer .ai/01_roadmap .ai/03_plans/AEC-MEPFS-Backbone .ai/05_logs 2>/dev/null | head -200
PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_shadow_staging --repo-root . --run-id 20260428T144427Z --backbone-nodes scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json
PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_shadow_report_reader --repo-root . --run-id 20260428T144427Z
PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_api_route_inventory --repo-root . --run-id 20260428T144427Z
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_contracts.py -q
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_shadow_staging.py scripts/tests/test_kg_backbone_api_route_inventory.py -q
bun --cwd api test v2Backbone.test.ts
bun --cwd explorer test src/app.searchInspector.integration.test.tsx src/components/componentInteraction.test.tsx src/components/graph/VisNetworkHost.test.ts
bun --cwd api test
bun --cwd explorer test
git diff --check
rg -n "MATCH \(n\) DETACH DELETE|DETACH DELETE|DROP DATABASE|CREATE OR REPLACE|run-kg-pipeline|--reset|--reload|protected content|protected ingest|live_neo4j_writes.*true|kg_rebuild.*true" scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json .ai/13_research/2026-04-28_architecture_licensure_taxonomy_research.md .ai/03_plans/AEC-MEPFS-Backbone/2026-04-28_architecture_licensure_taxonomy_expansion_packet.md .ai/02_audits/2026-04-28_architecture_taxonomy_expansion_audit.md 006_System-Manifests/aec-mepfs-backbone/taxonomy-expansion/20260428T144427Z/architecture-taxonomy-expansion-report.json || true
```

## Test results

- `PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_contracts.py -q` — **48 passed** after updating level/count assertions.
- `PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_shadow_staging.py scripts/tests/test_kg_backbone_api_route_inventory.py -q` — **22 passed**.
- Combined focused Python command — **70 passed**.
- `bun --cwd api test v2Backbone.test.ts` — **69 passed** after updating deterministic search totals for the larger taxonomy.
- `bun --cwd api test` — **102 passed**.
- Focused Explorer tests — **57 passed**.
- `bun --cwd explorer test` — **74 passed**.
- `git diff --check` — **passed**.

## Generated evidence

- `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260428T144427Z/shadow-staging-report.json`
- `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260428T144427Z/shadow-staging-consumer-report.json`
- `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260428T144427Z/shadow-backbone-graph.json`
- `006_System-Manifests/aec-mepfs-backbone/api-route-inventory/20260428T144427Z/api-route-inventory-report.json`
- `006_System-Manifests/aec-mepfs-backbone/taxonomy-expansion/20260428T144427Z/architecture-taxonomy-expansion-report.json`

## Safety invariant confirmation

- Protected content ingest: **not performed**.
- Neo4j mutation: **not performed**.
- KG rebuild/reload/reset: **not performed**.
- API runtime behavior change: **not performed**; API changes are test-count/search-total assertions only.
- Explorer runtime behavior change: **not performed**; Explorer changes are test-count assertions only.
- Generated route inventory still reports file-backed resolver routes under the existing default-on resolver policy and no unauthorized route drift.

## Residual risks

- The Architecture branch is substantially larger, but still metadata-level. It does not yet include typed cross-relationships among topics or source-overlay mappings.
- Public licensure sources were normalized into global canonical families; jurisdiction-specific details should be represented later as mappings/overlays, not taxonomy forks.
- The fixture is now larger and should continue to be monitored with Explorer performance tests when additional branches are expanded.

## Next safe follow-up

Continue with typed relationship/source-overlay enrichment for the expanded Architecture branch under a separate bounded packet, or expand another discipline branch using the same metadata-only method.
