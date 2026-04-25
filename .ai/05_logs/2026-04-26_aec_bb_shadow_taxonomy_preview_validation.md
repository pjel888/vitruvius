# AEC-BB Shadow Taxonomy Preview Validation

**Date:** 2026-04-26
**Scope:** fifth AEC-MEPFS Backbone shadow slice:
`GET /v2/backbone/taxonomy` plus opt-in Explorer registry-readiness details.

## Outcome

PASS.

The route and Explorer preview are implemented as additive, read-only,
shadow-only surfaces. They do not read or write Neo4j, rebuild the KG, change
feature flags, replace the Explorer graph, or expose protected source content.

## Implementation Evidence

- `api/index.ts`
  - adds `SHADOW_BACKBONE_TAXONOMY_PREVIEW_SCHEMA_VERSION`
  - adds `buildShadowBackboneTaxonomyPreview`
  - adds `GET /v2/backbone/taxonomy`
  - validates the consumer report and referenced staging artifact boundaries
  - resolves the staging artifact only inside
    `006_System-Manifests/aec-mepfs-backbone/shadow-staging`
- `api/v2Backbone.test.ts`
  - covers success from the real default staging artifact
  - verifies sanitized output does not include `official_url`,
    `blocking_notes`, `examples`, or `non_examples`
  - verifies fail-closed behavior when artifact runtime boundaries are enabled
  - verifies escaped artifact paths are rejected before file reads
- `explorer/src/components/explorer-rail/BackbonePreviewPanel.tsx`
  - adds an explicit detail control inside the existing opt-in AEC-MEPFS panel
  - shows that the canonical tree is not admitted yet
- `explorer/src/app.searchInspector.integration.test.tsx`
  - verifies summary fetch remains opt-in
  - verifies detail fetch does not run by default
  - verifies summary refresh clears loaded detail metadata to prevent stale
    run/detail mismatch
  - verifies graph perspective, nodes, and edges remain unchanged

## Verification Commands

```bash
cd api && bun test
cd explorer && bun test
cd explorer && bun run lint
cd explorer && bun run build
curl -sS http://localhost:3001/v2/backbone/taxonomy | jq '{schemaVersion, runId, counts, readiness, firstPredicateCategory: .predicateCategories[0], sourceClearance: .clearanceStates}'
curl -sS http://localhost:3001/v2/backbone/taxonomy | jq 'tostring | contains("official_url") or contains("blocking_notes") or contains("examples") or contains("non_examples")'
curl -sS -I http://127.0.0.1:5174/explore
```

## Verification Results

- API tests: 25 pass, 0 fail.
- Explorer tests: 39 pass, 0 fail.
- Explorer lint: pass.
- Explorer production build: pass.
- Live route smoke:
  - schema: `aec-bb-shadow-v2-backbone-taxonomy-preview/v1`
  - run: `20260425T154000Z`
  - counts: 12 predicates, 29 source-rights rows
  - readiness reports `registry_metadata_only`
  - readiness reports `canonicalTaxonomyTreeAvailable: false`
  - readiness reports `backboneNodesAvailable: false`
- Live sanitization smoke: `false` for blocked raw-field names
  (`official_url`, `blocking_notes`, `examples`, `non_examples`).
- Explorer dev route: `HTTP/1.1 200 OK` at
  `http://127.0.0.1:5174/explore`.

## Blast Radius Evidence

- GitNexus status was up to date at commit `84e5e3d`.
- `buildShadowBackboneSummary`: LOW impact.
- `ExplorerRail`: LOW impact.
- `getBackboneSummary`: LOW impact.
- `BackbonePreviewPanel`: LOW impact.
- Shared frontend `api()` helper: CRITICAL impact, intentionally not modified.

## Residual Risk

- The route name includes `taxonomy`, but the payload is not an admitted
  canonical taxonomy tree. The response and UI explicitly state that only
  registry metadata is available.
- The route is tied to the current default shadow run until a later run-selection
  contract is implemented.
- Future work should prioritize admitted BackboneNode fixtures/model authoring
  before adding more UI-only preview surfaces.
