---
task: aec-mepfs-shadow-evidence-repo-state-hardening
phase: validation
created: 2026-04-26
author: CODEX
status: PASS
---

# AEC-MEPFS Shadow Evidence Repo-State Hardening Validation

## Scope

Twenty-seventh AEC-MEPFS shadow slice: distinguish source-tree dirtiness from
generated-evidence dirtiness in file-backed shadow evidence reports, API
preview metadata, and the explicit-action Explorer evidence preview.

## Files Changed

- `scripts/vitruvius/kg/backbone_api_route_inventory.py`
- `scripts/vitruvius/kg/backbone_shadow_boundary_audit.py`
- `scripts/vitruvius/kg/backbone_shadow_benchmark.py`
- `scripts/vitruvius/kg/backbone_shadow_evidence_manifest.py`
- `scripts/tests/test_kg_backbone_api_route_inventory.py`
- `scripts/tests/test_kg_backbone_shadow_boundary_audit.py`
- `scripts/tests/test_kg_backbone_shadow_benchmark.py`
- `scripts/tests/test_kg_backbone_shadow_evidence_manifest.py`
- `api/index.ts`
- `api/v2Backbone.test.ts`
- `explorer/src/components/explorer-rail/BackbonePreviewPanel.tsx`
- `explorer/src/components/componentInteraction.test.tsx`
- `explorer/src/app.searchInspector.integration.test.tsx`
- `explorer/src/types/index.ts`
- `api/README.md`
- `explorer/README.md`
- `.ai/01_roadmap/current-phase.md`
- `.ai/01_roadmap/milestone-tracker.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/README.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/readiness-closure-scorecard.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/twenty-seventh-shadow-evidence-repo-state-hardening-packet.md`
- `.ai/03_plans/INDEX.md`
- `.ai/ACTIVE_WORK.md`
- `.ai/STRATEGIC_NEXT_MOVE.md`

## Verification Commands

- `git diff --check`
  - Result: passed.
- `(cd api && bun test v2Backbone.test.ts)`
  - Result: 60 passed, 214 assertions.
- `(cd explorer && bun test src/components/componentInteraction.test.tsx src/app.searchInspector.integration.test.tsx src/api/graphApi.test.ts)`
  - Result: 25 passed, 182 assertions.
- `PYTHONPATH=scripts python3 -m pytest -q scripts/tests/test_kg_backbone_api_route_inventory.py scripts/tests/test_kg_backbone_shadow_benchmark.py scripts/tests/test_kg_backbone_shadow_boundary_audit.py scripts/tests/test_kg_backbone_shadow_evidence_manifest.py`
  - Result: 49 passed.
- `PYTHONPATH=scripts python3 -m pytest -q scripts/tests/test_kg_backbone_contracts.py scripts/tests/test_kg_backbone_shadow_staging.py scripts/tests/test_kg_backbone_shadow_report_reader.py scripts/tests/test_kg_backbone_api_route_inventory.py scripts/tests/test_kg_backbone_parity_runner.py scripts/tests/test_kg_backbone_shadow_boundary_audit.py scripts/tests/test_kg_backbone_shadow_benchmark.py scripts/tests/test_kg_backbone_shadow_evidence_manifest.py scripts/tests/test_kg_backbone_placement_qa.py scripts/tests/test_kg_backbone_resolver_qa.py`
  - Result: 153 passed.
- `(cd api && bun test)`
  - Result: 78 passed, 279 assertions.
- `(cd explorer && bun test)`
  - Result: 45 passed, 217 assertions.
- `(cd explorer && bun run lint)`
  - Result: passed.
- `(cd explorer && bun run build)`
  - Result: passed with the existing Vite chunk-size warning.

## Advisory Review

- Gemini CLI was discovered at `/opt/homebrew/bin/gemini` and attempted with a
  sanitized diff prompt. It failed before review with the existing 403
  service-disabled response; no findings were produced.
- Kimi CLI was discovered at `/Users/philiplewis/.local/bin/kimi` and used for
  advisory review. It found repo-state freshness visibility/test gaps and later
  cross-report freshness gaps; the implementation was updated to render all
  freshness fields, test them in Explorer, represent legacy manifests as
  `unknown`, fail closed on explicit source-tree dirtiness, and reject
  divergent/source-dirty input report repo-state metadata where present.
- Native verifier initially rejected the slice for weak Explorer visibility and
  missing tests; those issues were fixed.

## Safety Invariant Confirmation

- No Neo4j writes or queries.
- No KG rebuild/reset/load.
- No protected content ingest.
- No feature-flag cutover.
- No `/v2/resolve` or `/v2/resolve/trace` route mounting.
- No Explorer default graph adoption.
- Preview/read-only/shadow-only behavior remains opt-in.
- Generated artifacts remain file-backed and auditable.
- Legacy manifests are not misrepresented as source-clean; freshness fields are
  shown as `unknown` until refreshed.
- Refreshed manifests fail closed when they explicitly report source-tree
  dirtiness.
- The evidence manifest rejects divergent input-report commit metadata and
  source-dirty input-report metadata where those fields are present.

## Residual Risks

- This slice intentionally does not generate the final refreshed evidence
  packet because doing that before commit would record the source tree as dirty.
- The next slice must run the report chain from a clean committed source tree
  and commit the refreshed generated evidence.
- API `reportPath` remains part of the compact evidence preview contract from
  earlier slices; it is not newly introduced here.

## Next Recommended Safe Slice

Commit and push this hardening slice, refresh GitNexus, then generate a fresh
route inventory, boundary audit, benchmark, and evidence manifest packet from a
clean source tree. Do not promote to live graph, write Neo4j, rebuild KG
artifacts, ingest protected content, flip feature flags, mount resolver routes,
or make Explorer adopt the shadow graph by default.
