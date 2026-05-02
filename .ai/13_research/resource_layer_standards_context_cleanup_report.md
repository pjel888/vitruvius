# Resource Layer Standards Context Cleanup Report

Date: 2026-05-02
Status: implemented and validated

## Summary
Implemented a guarded standards-context review workflow for standard/code-like Resource Layer records, focused on the current ASCE 7 and ACI 318 warnings. No edition, version, scope, jurisdiction, source metadata, resource, node-resource link, or review status was invented or promoted in production data.

## What changed
- Added structured standards-context types for identifiers, edition/version context, jurisdiction/scope context, and review context.
- Added standards-context validation metrics and stricter accepted/promotion blockers.
- Added standards-context detail, preview, and decision service functions.
- Added read/detail and preview/apply API routes under `/resources/review/standards`.
- Added `/dev/resource-review` Standards Missing Context cards with structured context form, safety wording, promotion blockers, and non-mutating diff preview.
- Added tests for missing context, placeholder rejection, incomplete promotion blocking, preview immutability, transaction-manifested apply on copied registry, API routes, UI form rendering, gate-disabled apply, and regression routes.

## ASCE 7 status
- Resource: `res-asce-7-official-landing`
- Links: `nrl-wind-load-asce-7-needs-review`, `nrl-seismic-load-asce-7-needs-review`
- Review status remains `needs_review`.
- Missing fields shown: edition/version and citation/scope.
- Current jurisdiction/geographic scope text remains unchanged.
- Promotion remains blocked until a reviewer supplies complete source-backed context or a structured reviewer/source justification.
- No edition/version values were added.

## ACI 318 status
- Resource: `res-aci-318-building-code-portal`
- Link: `nrl-structural-column-aci-rejected`
- Review status remains `rejected` because the current link remains too broad.
- Missing fields shown: edition/version and citation/scope.
- Promotion remains blocked until a future reviewer supplies section-specific and source-backed context for an appropriate node relationship.
- No edition/version values were added.

## No production data mutation
Production Resource Layer registry files were restored after an accidental test-route mutation during development and are unchanged by this final workflow implementation. The apply path is tested only against copied registries and remains local/dev gated for live use.

## Kimi review summary
Accepted:
- Keep needs-review ASCE/ACI missing context as warnings.
- Treat accepted/promoted standard/code links missing complete context as blockers.
- Reject placeholder values such as `latest`, `current`, `unknown`, `TBD`, `sample`, and `varies`.
- Require reviewer/rationale and sourceOfContext for complete or not-required decisions.
- Avoid wording that implies governing/applicable/current standards without jurisdiction/adoption evidence.

Deferred:
- External authoritative recrawl/lookup.
- AHJ/adoption effective-date modeling.
- Multi-jurisdiction applicability modeling.
- Full standards evidence span admission.
- Automatic edition inference from titles or URLs.

Rejected:
- Treating a magic review-note phrase as sufficient for accepted/promoted standard context. The implementation now prefers structured review context.

## Files changed
- `api/resourceLayer/types.ts`
- `api/resourceLayer/validation.ts`
- `api/resourceLayer/reviewWorkflow.ts`
- `api/resourceLayer/registry.ts`
- `api/validateResourceLayer.ts`
- `api/index.ts`
- `api/resourceLayer.test.ts`
- `explorer/src/types/index.ts`
- `explorer/src/api/graphApi.ts`
- `explorer/src/api/graphApi.test.ts`
- `explorer/src/app.searchInspector.integration.test.tsx`
- `explorer/src/components/resource-review/ResourceReviewAdmin.tsx`
- `explorer/src/components/resource-review/ResourceReviewAdmin.test.tsx`
- `docs/knowledge-graph/resource-layer.md`
- `.ai/13_research/resource_layer_standards_context_cleanup_report.md`
- `.ai/13_research/resource_layer_standards_context_validation_report.md`
- `.ai/13_research/resource_layer_standards_context_kimi_review.md`
- `.ai/05_logs/2026-05-02_resource_layer_standards_context_cleanup.md`

## Commands run
- `bun test api/resourceLayer.test.ts`
- `cd api && bun test`
- `cd explorer && bun test`
- `cd explorer && bun run build`
- `bun run api/validateResourceLayer.ts`
- `bun run api/validateGraphRelationships.ts`
- `bun run api/validateCanonicalGraphStewardship.ts`
- `.venv\Scripts\python.exe -m pytest scripts/tests/test_kg_aec_relationship_improvement.py`

## Next recommended action
Add per-P1-packet ontology review status and filters in `/dev/canonical-review`, keeping P1 packets advisory and non-destructive.
