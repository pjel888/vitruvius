---
task: aec-mepfs-shadow-evidence-explorer-preview
phase: 05
created: 2026-04-26
author: CODEX
status: COMPLETE
supersedes: null
---

# Twenty-Fifth Shadow Slice: Explorer Evidence Preview

## Scope

Add an explicit-action Explorer preview for the existing
`GET /v2/backbone/evidence` route inside the non-default AEC-MEPFS Backbone
rail panel.

This slice is frontend consumer parity only. It does not add new runtime graph
surfaces, promote a graph, mount `/v2/resolve`, query or write Neo4j, rebuild
the KG, ingest protected content, change feature flags, or make Explorer adopt
the shadow graph.

## Research Baseline

- The twenty-third slice added the compact API-only evidence preview route.
- The twenty-fourth slice hardened the consolidated evidence packet against
  stale API hashes and incomplete latest evidence-manifest runs.
- Explorer already has explicit-action preview controls for taxonomy readiness
  details and placement QA, both nested inside the opt-in AEC-MEPFS preview.
- GitNexus impact is LOW for `BackbonePreviewPanel`,
  `getBackbonePlacementQaPreview`, and `loadBackbonePlacementQaPreview`, which
  define the closest existing implementation pattern.

## Audit Findings

- Explorer can currently open the AEC-MEPFS preview, taxonomy detail preview,
  and placement QA preview, but it cannot display the consolidated evidence
  manifest summary.
- The API route is already file-backed and sanitized, so adding a frontend
  opt-in consumer improves consumer parity without widening runtime scope.
- The preview must reset on summary refresh, just like taxonomy and placement
  QA detail state, and must not write graph state.

## Implementation Plan

1. Add Explorer types and graph API client constants for
   `/v2/backbone/evidence`.
2. Add `ExplorerRail` state and an explicit loader for evidence preview.
3. Render the evidence summary inside `BackbonePreviewPanel` only after the
   explicit evidence control is clicked.
4. Extend component/API/integration tests to prove opt-in behavior, route
   contract parity, and no graph-state adoption.
5. Refresh parity/evidence reports and update state docs.

## Plan Critique

- [C001] Do not auto-fetch evidence just because the AEC-MEPFS preview opened.
- [C002] Do not expose raw input hashes or source report payloads in Explorer.
- [C003] Do not add or mount any new API route.
- [C004] Keep graph nodes, graph edges, selected perspective, and Explorer
  graph state unchanged.
- [C005] Keep this as a preview-only UI consumer over an existing sanitized
  API route.

## Execution Checklist

- [x] Inspect current Explorer preview pattern and GitNexus impact.
- [x] Implement explicit-action evidence preview consumer.
- [x] Extend focused API/Explorer tests.
- [x] Attempt Gemini/Kimi advisory review and record availability.
- [x] Regenerate parity/evidence reports as needed.
- [x] Run focused and broader affected verification.
- [x] Prepare commit-ready evidence; refresh GitNexus and push before next
  slice inspection.

## Explicit Non-Goals

- No new `/v2` route.
- No Neo4j write or query.
- No KG rebuild.
- No protected content ingest.
- No feature flag cutover.
- No Explorer default graph adoption.
- No `/v2/resolve` route mounting.
- No runtime latency claim.

## Implementation Evidence

- Explorer now has typed support for the sanitized
  `/v2/backbone/evidence` preview payload.
- `ExplorerRail` holds evidence-preview state separately from graph state,
  taxonomy detail state, and placement-QA state.
- `BackbonePreviewPanel` exposes a `Load evidence summary` control and renders
  the summary only after that explicit action.
- Component and integration tests prove that the evidence preview is not loaded
  when the AEC-MEPFS preview opens, does not replace graph nodes/edges or the
  selected perspective, and does not render raw `input_file_hashes_sha256`.
- The parity runner now requires
  `shadow_evidence_preview_opt_in_isolation`.

## Generated Evidence

- Route inventory:
  `006_System-Manifests/aec-mepfs-backbone/api-route-inventory/20260426T095439Z/api-route-inventory-report.json`
- API/Explorer parity:
  `006_System-Manifests/aec-mepfs-backbone/parity/20260426T095440Z/api-explorer-parity-report.json`
- Boundary audit:
  `006_System-Manifests/aec-mepfs-backbone/boundary-audit/20260426T100631Z/shadow-boundary-audit-report.json`
- Benchmark:
  `006_System-Manifests/aec-mepfs-backbone/benchmarks/20260426T100632Z/benchmark-report.json`
- Evidence manifest:
  `006_System-Manifests/aec-mepfs-backbone/evidence-manifest/20260426T100633Z/shadow-evidence-manifest-report.json`

Metrics:

- API/Explorer parity: 26/26 cases and 6/6 commands passed.
- Boundary audit: 10/10 checks passed.
- Benchmark: 5/5 file-backed operations passed.
- Evidence manifest: 9/9 artifacts ok, 7/7 preview routes present, graph
  counts remain 7 nodes, 4 edges, 3 roots, max depth 2.

## Verification

- `PYTHONPATH=scripts python3 -m pytest -q scripts/tests/test_kg_backbone_parity_runner.py scripts/tests/test_kg_backbone_shadow_boundary_audit.py scripts/tests/test_kg_backbone_shadow_benchmark.py scripts/tests/test_kg_backbone_shadow_evidence_manifest.py scripts/tests/test_kg_backbone_api_route_inventory.py`:
  56 passed.
- `PYTHONPATH=scripts python3 -m pytest -q scripts/tests/test_kg_backbone_contracts.py scripts/tests/test_kg_backbone_shadow_staging.py scripts/tests/test_kg_backbone_shadow_report_reader.py scripts/tests/test_kg_backbone_api_route_inventory.py scripts/tests/test_kg_backbone_parity_runner.py scripts/tests/test_kg_backbone_shadow_boundary_audit.py scripts/tests/test_kg_backbone_shadow_benchmark.py scripts/tests/test_kg_backbone_shadow_evidence_manifest.py scripts/tests/test_kg_backbone_placement_qa.py scripts/tests/test_kg_backbone_resolver_qa.py`:
  145 passed.
- `(cd api && bun test v2Backbone.test.ts)`: 57 passed.
- `(cd api && bun test)`: 75 passed.
- `(cd explorer && bun test src/api/graphApi.test.ts src/components/componentInteraction.test.tsx src/app.searchInspector.integration.test.tsx)`:
  25 passed.
- `(cd explorer && bun test)`: 45 passed.
- `(cd explorer && bun run lint)`: passed.
- `(cd explorer && bun run build)`: passed with the existing Vite chunk-size
  warning.
- `git diff --check`: passed.

## Advisory Review

- Gemini CLI was attempted but blocked by a 403 service-disabled response.
- Kimi CLI was attempted but produced no review output before timeout.
- Native verifier review was requested for the uncommitted diff.

## Safety Invariants

Confirmed for this slice:

- no Neo4j writes or queries
- no KG rebuild/reset/load
- no protected content ingest
- no feature-flag cutover
- no `/v2/resolve` route mounting
- no Explorer default graph adoption
- preview/read-only/shadow-only behavior remains opt-in
- generated artifacts remain file-backed and auditable
- API/consumer parity is covered by generated parity evidence
