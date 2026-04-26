---
task: aec-mepfs-shadow-evidence-explorer-preview
phase: validation
created: 2026-04-26
author: CODEX
status: PASS
---

# AEC-MEPFS Shadow Evidence Explorer Preview Validation

## Scope

Twenty-fifth AEC-MEPFS shadow slice: add an explicit-action Explorer preview
for the existing sanitized `GET /v2/backbone/evidence` route.

This slice remains shadow-only and read-only. It adds no API route, no Neo4j
write/query path, no KG rebuild/reset/load, no protected content ingest, no
feature-flag cutover, no `/v2/resolve` route mounting, no Explorer default graph
adoption, and no graph promotion.

## Files Changed

- `.ai/01_roadmap/current-phase.md`
- `.ai/01_roadmap/milestone-tracker.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/README.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/readiness-closure-scorecard.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/readiness-spec-acceptance-record.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/twenty-fifth-shadow-evidence-explorer-preview-packet.md`
- `.ai/03_plans/INDEX.md`
- `.ai/ACTIVE_WORK.md`
- `.ai/STRATEGIC_NEXT_MOVE.md`
- `explorer/src/api/graphApi.ts`
- `explorer/src/api/graphApi.test.ts`
- `explorer/src/app.searchInspector.integration.test.tsx`
- `explorer/src/components/ExplorerRail.tsx`
- `explorer/src/components/componentInteraction.test.tsx`
- `explorer/src/components/explorer-rail/BackbonePreviewPanel.tsx`
- `explorer/src/types/index.ts`
- `scripts/tests/fixtures/aec_mepfs_backbone/api-explorer-parity-cases.json`
- `scripts/tests/test_kg_backbone_shadow_boundary_audit.py`
- `scripts/tests/test_kg_backbone_shadow_evidence_manifest.py`
- `scripts/vitruvius/kg/backbone_parity_runner.py`
- `scripts/vitruvius/kg/backbone_shadow_benchmark.py`
- `scripts/vitruvius/kg/backbone_shadow_boundary_audit.py`
- `scripts/vitruvius/kg/backbone_shadow_evidence_manifest.py`

## Generated Artifacts

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

## Metrics

- Parity: 26/26 cases passed, 6/6 commands passed.
- Route inventory: 22 Hono route declarations, 7/7 preview routes present,
  `/v2/resolve` and `/v2/resolve/trace` unmounted.
- Boundary audit: 10/10 checks passed.
- Benchmark: 5/5 file-backed operations passed.
- Evidence manifest: 9/9 artifacts ok.
- Shadow graph counts unchanged: 7 nodes, 4 edges, 3 roots, max depth 2.

## Verification Commands

- `PYTHONPATH=scripts python3 -m pytest -q scripts/tests/test_kg_backbone_parity_runner.py scripts/tests/test_kg_backbone_shadow_boundary_audit.py scripts/tests/test_kg_backbone_shadow_benchmark.py scripts/tests/test_kg_backbone_shadow_evidence_manifest.py scripts/tests/test_kg_backbone_api_route_inventory.py`
  - Result: 56 passed.
- `PYTHONPATH=scripts python3 -m pytest -q scripts/tests/test_kg_backbone_contracts.py scripts/tests/test_kg_backbone_shadow_staging.py scripts/tests/test_kg_backbone_shadow_report_reader.py scripts/tests/test_kg_backbone_api_route_inventory.py scripts/tests/test_kg_backbone_parity_runner.py scripts/tests/test_kg_backbone_shadow_boundary_audit.py scripts/tests/test_kg_backbone_shadow_benchmark.py scripts/tests/test_kg_backbone_shadow_evidence_manifest.py scripts/tests/test_kg_backbone_placement_qa.py scripts/tests/test_kg_backbone_resolver_qa.py`
  - Result: 145 passed.
- `(cd api && bun test v2Backbone.test.ts)`
  - Result: 57 passed, 208 assertions.
- `(cd api && bun test)`
  - Result: 75 passed, 273 assertions.
- `(cd explorer && bun test src/api/graphApi.test.ts src/components/componentInteraction.test.tsx src/app.searchInspector.integration.test.tsx)`
  - Result: 25 passed, 174 assertions.
- `(cd explorer && bun test)`
  - Result: 45 passed, 209 assertions.
- `(cd explorer && bun run lint)`
  - Result: passed.
- `(cd explorer && bun run build)`
  - Result: passed with the existing Vite chunk-size warning.
- `git diff --check`
  - Result: passed.

## Advisory Review

- Gemini CLI was attempted with a sanitized diff prompt. It failed before
  review with a 403 service-disabled response; no findings were produced.
- Kimi CLI was attempted with the same sanitized diff prompt. It found one
  actionable gap: the boundary audit's `no_explorer_default_adoption` invariant
  did not explicitly include `shadow_evidence_preview_opt_in_isolation`.
  The gap is fixed in `backbone_shadow_boundary_audit.py`, with a regression
  update in `test_kg_backbone_shadow_boundary_audit.py`; boundary/benchmark/
  manifest evidence was regenerated after the fix.
- Native verifier review returned PASS. It confirmed the route remains
  file-backed/read-only, the Explorer fetch is opt-in, no raw hashes are
  emitted, and no protected payloads are exposed.
- Ralph deslop hook path was checked, but
  `/Users/philiplewis/.codex/skills/ai-slop-cleaner/SKILL.md` was unavailable,
  so no automated ai-slop-cleaner pass could run.

## GitNexus Evidence

- `npx --yes gitnexus@1.6.2-rc.10 status`
  - Result: index was up to date at pre-commit HEAD `b0d3ba3`.
- `npx --yes gitnexus@1.6.2-rc.10 impact -r vitruvius BackbonePreviewPanel --direction upstream --depth 2 --include-tests`
  - Result: LOW risk, 0 impacted symbols.
- `npx --yes gitnexus@1.6.2-rc.10 impact -r vitruvius run_shadow_boundary_audit --direction upstream --depth 2 --include-tests`
  - Result: LOW risk, 16 impacted symbols, all in KG/tests modules.
- `gitnexus detect-changes` was attempted through the CLI but is not available
  in `gitnexus@1.6.2-rc.10`; status and impact checks were used as the CLI
  fallback.

## Safety Invariant Confirmation

- No Neo4j writes or queries.
- No KG rebuild/reset/load.
- No protected content ingest.
- No feature-flag cutover.
- No `/v2/resolve` route mounting.
- No Explorer default graph adoption.
- Preview/read-only/shadow-only behavior remains opt-in.
- Generated artifacts are file-backed and auditable.
- API/consumer parity is tested and recorded in the parity report.

## Residual Risks

- The evidence preview intentionally exposes sanitized report file paths and the
  git commit hash. It does not expose raw input hashes, full report payloads,
  source content, official URLs, blocking notes, or protected content.
- Runtime integration remains blocked by the existing readiness scorecard.

## Next Recommended Safe Slice

Run fresh inspection after this commit and prefer another bounded file-backed
QA/evidence hardening slice or a non-default preview parity improvement. Do not
promote to live graph, mount `/v2/resolve`, write Neo4j, rebuild KG artifacts,
ingest protected content, flip feature flags, or make Explorer adopt the shadow
graph by default.
