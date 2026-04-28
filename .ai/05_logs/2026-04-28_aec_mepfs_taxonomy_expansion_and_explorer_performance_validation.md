# AEC-MEPFS Taxonomy Expansion And Explorer Performance Validation

```yaml
status: VALIDATED
date: 2026-04-28
branch: main
start_commit: 21b95698
run_id: 20260428T021641Z
authority_packet: .ai/03_plans/AEC-MEPFS-Backbone/2026-04-28_aec_mepfs_taxonomy_expansion_and_explorer_performance_packet.md
gemini_used: false
kimi_status: timed_out_after_120s_no_actionable_findings
```

## Scope

This validation covers the correction from the seven-node AEC-MEPFS Explorer
stub to the governed first-slice L1/L2 taxonomy skeleton, plus API and Explorer
performance guardrails for the larger default graph.

The work remains file-backed and non-protected. It does not authorize or perform
Neo4j mutation, KG rebuild/reload/reset, protected content ingestion, production
graph promotion, or broad/global live-runtime authorization.

## Root Cause

Explorer was already pointed at AEC-MEPFS by default, but the graph being served
was still based on the small admitted fixture and old shadow staging run:

- fixture: `scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json`
- old staging run: `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260426T003710Z/`

That is why Explorer showed only seven nodes. The repository already contained a
governed first-slice L1/L2 taxonomy decision record, so the implementation was
expanded to match that skeleton.

## Files Inspected

- `.ai/03_plans/AEC-MEPFS-Backbone/master-taxonomy-l1-l2-decision-record.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-27_actual_aec_mepfs_implementation_cutover_packet.md`
- `.ai/05_logs/2026-04-28_aec_mepfs_actual_implementation_cutover_validation.md`
- `scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json`
- `scripts/vitruvius/kg/backbone_shadow_staging.py`
- `scripts/vitruvius/kg/backbone_shadow_report_reader.py`
- `scripts/vitruvius/kg/backbone_api_route_inventory.py`
- `scripts/tests/test_kg_backbone_contracts.py`
- `scripts/tests/test_kg_backbone_shadow_staging.py`
- `scripts/tests/test_kg_backbone_shadow_report_reader.py`
- `scripts/tests/test_kg_backbone_api_route_inventory.py`
- `api/index.ts`
- `api/v2Backbone.test.ts`
- `explorer/src/components/graph/VisNetworkHost.tsx`
- `explorer/src/app.searchInspector.integration.test.tsx`
- `explorer/src/components/componentInteraction.test.tsx`

## Files Changed

- `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-28_aec_mepfs_taxonomy_expansion_and_explorer_performance_packet.md`
- `.ai/05_logs/2026-04-28_aec_mepfs_taxonomy_expansion_and_explorer_performance_validation.md`
- `scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json`
- `scripts/tests/test_kg_backbone_contracts.py`
- `api/index.ts`
- `api/v2Backbone.test.ts`
- `explorer/src/components/graph/VisNetworkHost.tsx`
- `explorer/src/app.searchInspector.integration.test.tsx`
- `explorer/src/components/componentInteraction.test.tsx`
- `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260428T021641Z/`
- `006_System-Manifests/aec-mepfs-backbone/api-route-inventory/20260428T021641Z/api-route-inventory-report.json`
- `006_System-Manifests/aec-mepfs-backbone/explorer-performance/20260428T021641Z/explorer-performance-smoke-report.json`

## Implementation Summary

- Expanded the admitted non-protected L1/L2 taxonomy fixture from 7 nodes and 4
  relationships to 114 nodes and 95 relationships.
- Preserved existing IDs for the original seven admitted nodes.
- Added all 19 top-level domains from the first-slice decision record:
  `ARC`, `ACC`, `URB`, `CIV`, `STR`, `GEO`, `MEC`, `ELE`, `PLS`, `FLS`, `CON`,
  `MAT`, `COM`, `PER`, `SUS`, `DIG`, `OPS`, `HIS`, and `FIG`.
- Kept `HIS` and `FIG` as L1 roots with `parent_path_code: null`.
- Generated new shadow staging artifacts for `20260428T021641Z`.
- Changed the API default shadow report resolver to select the latest shadow
  staging consumer report unless explicitly overridden.
- Cached AEC file-backed graph artifacts by report/artifact/graph file size and
  mtime.
- Made `/health` skip Neo4j connectivity by default and validate AEC readiness
  using cheap report metadata.
- Made `/perspectives` avoid legacy Neo4j-backed count queries by default; use
  `?includeCounts=1` for those counts.
- Reused cached AEC graph artifacts for expand, path, taxonomy, and perspective
  graph routes.
- Added Explorer large-graph guardrails in `VisNetworkHost`:
  deterministic clustered placement, disabled physics for large graphs, reduced
  edge smoothing and shadows, hidden edges during drag, less camera sync churn,
  and visible graph-engine load errors.

## Commands Run

```bash
git status --short --branch
git rev-parse --short HEAD
git log --oneline -n 5
PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_shadow_staging --repo-root . --run-id 20260428T021641Z --backbone-nodes scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json
PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_shadow_report_reader --repo-root . --run-id 20260428T021641Z
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_contracts.py -q
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_contracts.py scripts/tests/test_kg_backbone_shadow_staging.py scripts/tests/test_kg_backbone_shadow_report_reader.py -q
(cd api && bun test v2Backbone.test.ts)
(cd explorer && bun test src/app.searchInspector.integration.test.tsx src/components/componentInteraction.test.tsx)
(cd explorer && bun run lint)
(cd explorer && bun run build)
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_api_route_inventory.py scripts/tests/test_kg_backbone_parity_runner.py scripts/tests/test_kg_backbone_shadow_boundary_audit.py -q
(cd api && bun test)
(cd explorer && bun test)
git diff --check
rg -n "LIVE_RUNTIME_AUTHORIZED|Neo4j|KG rebuild|KG reload|KG reset|protected ingest|protected content|Explorer default|default adoption|default-on|runtime threshold|passFailClaim|/v2/resolve" .ai api explorer scripts 006_System-Manifests || true
rg -n "MATCH \(n\) DETACH DELETE|DETACH DELETE|DROP DATABASE|CREATE OR REPLACE|run-kg-pipeline|--reset|--reload|Neo4jLoader|TaxonomyLoader|CanonicalNode" api explorer scripts .ai || true
```

## Test Results

- `scripts/tests/test_kg_backbone_contracts.py`: `48 passed`
- Contract + shadow staging + report reader suite: `81 passed`
- `api/v2Backbone.test.ts`: `69 pass`, `0 fail`
- Targeted Explorer tests: `26 pass`, `0 fail`
- Route inventory/parity/boundary focused Python suite: `44 passed`
- Fresh combined Python verification after resume: `125 passed`
- Full API Bun suite after resume: `102 pass`, `0 fail`
- Full Explorer Bun suite after resume: `48 pass`, `0 fail`
- Explorer lint after resume: passed
- Explorer build after resume: passed, with existing Vite chunk-size warning for the graph engine bundle
- `git diff --check`: passed

## Generated Evidence

- Shadow staging:
  `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260428T021641Z/`
- Route inventory:
  `006_System-Manifests/aec-mepfs-backbone/api-route-inventory/20260428T021641Z/api-route-inventory-report.json`
- Explorer performance smoke:
  `006_System-Manifests/aec-mepfs-backbone/explorer-performance/20260428T021641Z/explorer-performance-smoke-report.json`

Performance smoke results:

- `/health`: HTTP 200, about `21.26 ms`, `neo4j: "not checked"`,
  `aecMepfs: "ready"`.
- `/perspectives`: HTTP 200, about `0.78 ms`, AEC-MEPFS node count `114`.
- `/perspective/aec-mepfs/nodes`: HTTP 200, about `9.75 ms`, `114` nodes,
  `95` edges, `19` roots.

## Advisory Review

Read-only Explorer/performance subagent review found:

- `/health`, `/perspectives`, and `/perspective/aec-mepfs/nodes` were doing too
  much repeated file/graph work.
- Command bar health polling could magnify that cost.
- `vis-network` defaults were tuned for tiny graphs and could create avoidable
  jank on the expanded graph.
- Edge filters and tests were pinned to the old seven-node graph.
- Dynamic graph-engine import failures could leave a permanent loading state.

Accepted fixes were implemented and verified by the tests above.

Kimi/Moonshot was available at `/Users/philiplewis/.local/bin/kimi`. A bounded
read-only advisory review prompt was attempted with a 120 second timeout. Kimi
timed out without final actionable findings. No Gemini review was used.

## Evidence Manifest Note

An attempted full shadow evidence manifest refresh for `20260428T021641Z`
failed because the older full-manifest contract still enforces pre-cutover
resolver-route assumptions and stale benchmark/boundary anchors. The failed
generated report was discarded and is not committed as success evidence.

This does not invalidate the current slice evidence. The current slice uses the
new route inventory, shadow staging, performance smoke, tests, and safety greps
as its verification artifacts.

## Safety Invariants

- Broad/global `LIVE_RUNTIME_AUTHORIZED`: not granted.
- Protected content ingest: not performed.
- Protected payload exposure: not introduced.
- Neo4j writes/reset/reload/destructive mutation: not introduced.
- KG rebuild/reload/reset: not introduced.
- Production live graph promotion: not performed.
- Source-rights metadata and blocking notes remain metadata-only; no protected payloads were added to API/Explorer responses.
- Runtime resolver behavior: unchanged except for reading the latest file-backed
  taxonomy artifact through existing routes.
- Explorer default adoption: remains file-backed AEC-MEPFS-first with legacy
  escape behavior preserved.
- `HIS` and `FIG`: top-level L1 domains, not Architecture children.

## Residual Risks

- This is the governed L1/L2 skeleton, not a full L3/L4 deep taxonomy or a
  content-rich KG. Further depth requires dedicated taxonomy authoring and
  rights-safe admission work.
- The smoke performance evidence exercises API routes and build/test behavior;
  a manual browser pass on the user's machine is still useful for subjective
  canvas smoothness.
- The older full evidence-manifest contract should be reconciled separately if a
  new global manifest is required after the actual runtime cutover.
