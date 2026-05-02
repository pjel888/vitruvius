# Resource Layer Final Report

Date: 2026-05-01
Status: implementation loop 1 completed

## 1. Summary
Implemented a real file-backed Resource Layer for Vitruvius. Selected eligible nodes can now receive ranked, source-backed resources through API node detail and the Explorer sidebar. The implementation uses separate Resource and NodeResourceLink registries and does not turn URLs into graph nodes.

## 2. Files changed
- `api/resourceLayer/types.ts`
- `api/resourceLayer/normalization.ts`
- `api/resourceLayer/sourceFamilies.ts`
- `api/resourceLayer/deduplication.ts`
- `api/resourceLayer/verification.ts`
- `api/resourceLayer/ranking.ts`
- `api/resourceLayer/registry.ts`
- `api/resourceLayer/validation.ts`
- `api/resourceLayer/localCorpusScanner.ts`
- `api/resourceLayer/adapters/types.ts`
- `api/resourceLayer/adapters/openLibrary.ts`
- `api/validateResourceLayer.ts`
- `api/indexLocalResources.ts`
- `api/resourceLayer.test.ts`
- `api/index.ts`
- `explorer/src/types/index.ts`
- `explorer/src/components/inspector/NodeInspector.tsx`
- `explorer/src/components/componentInteraction.test.tsx`
- `006_System-Manifests/resource-layer/*.json`
- `docs/knowledge-graph/resource-layer.md`
- `.ai/02_audits/resource-layer-implementation-audit.md`
- `.ai/03_plans/resource-layer-implementation-plan.md`
- `.ai/10_state/decisions.md`
- `.ai/13_research/resource_layer_implementation_progress.md`
- `.ai/13_research/resource_layer_kimi_final_review.md`

## 3. Data model changes
Added Resource, NodeResourceLink, SourceFamily, ResourceCheck, ResourceCandidate, and NodeResourceSummary types. Resource records include source-rights and admission-provenance fields added after Kimi final review.

## 4. Sidebar changes
The `NodeInspector` Sources tab now renders a Resources / References section with:
- title, organization/publisher/year,
- resource type, authority, verification, review, and access badges,
- relevance/authority/confidence scores,
- rationale,
- jurisdiction/scope warning,
- page/chapter/section refs when present,
- online and local-file affordances,
- safe empty states for zero resources.

## 5. Local corpus indexing status
Implemented a safe metadata/hash scanner. The scanner indexed 25 real markdown files from the resource-layer plan pack into `006_System-Manifests/resource-layer/local-file-index.json` with 0 errors. These records are not automatically admitted as node links.

## 6. Source adapter status
Implemented the adapter interface and an Open Library adapter. It is candidate-only, needs no API key, fails gracefully on non-OK responses, and is tested with mocked fetch responses.

## 7. Verification and ranking status
Implemented URL/canonical/identifier/local-file verification helpers, duplicate detection, and deterministic ranking. Ranking hides candidate/needs_review/rejected links by default and exposes them only when `includeCandidates=true`.

## 8. Validation/tests added
Validation detects missing required metadata, invalid URL/DOI/ISBN, duplicate DOI/ISBN/canonical URL/hash, accepted external records without `lastCheckedAt`, accepted local records without path/hash, bad node/resource links, bad score ranges, accepted links to rejected/unverified resources, standards without jurisdiction/scope, and standards missing edition/version context.

## 9. Seed/backfill results
Accepted seed links:
- `VTN-DOM-0004630` Accessible Route Continuity -> U.S. Access Board ADA Chapter 4.
- `VTN-DOM-0012160` Load Path -> ICE Structural Load Paths.
- `VTN-DOM-0012160` Load Path -> WBDG Wind Safety as contextual guidance.
- `VTN-DOM-0012777` Structural Wind Load -> WBDG Wind Safety as contextual guidance.
- `VTN-DOM-0012778` Structural Seismic Load -> WBDG Seismic Design Principles as contextual guidance.

Held/rejected:
- ASCE 7 landing page links to wind/seismic remain `needs_review`.
- FHWA Earth Retaining Structures to Structural Retaining Wall remains `needs_review`.
- ACI 318 portal to Structural Column is `rejected`.

## 10. Kimi review summary
Seed review accepted the Access Board, WBDG, and ICE mappings listed above.
Seed review warned against overclaiming ASCE/FHWA/ACI.
Final review corrections accepted:
- Add source-rights/admission provenance to Resource.
- Make ranking penalties explicit constants.
- Warn on standards without edition/version context.
- Treat WBDG as contextual guidance, not primary standard authority.

Final review correction rejected/qualified:
- Kimi said accepted resources were hidden; this was inaccurate. Accepted/human_reviewed links are shown by default. Candidate/needs_review/rejected links are intentionally hidden per the plan unless an API caller opts in.

## 11. Metrics
- Total resources in main registry: 7
- Resources by type: government_guidance 2; professional_guidance 3; standard 2
- Resources by authority: government 4; professional_body 3
- Resources by verification status: link_verified 7
- Source families: 25
- Resource checks: 15
- Node-resource links: 9
- Accepted links: 5
- Candidate links: 0
- Needs-review links: 3
- Rejected links: 1
- Resource candidates: 4
- Eligible nodes with accepted resources: 4
- High-priority nodes with at least three accepted resources: 0
- Duplicate resources detected: 0
- Broken links detected: 0
- Local files indexed: 25

## 12. Commands run
- `./scripts/refresh_code_intelligence.sh`
- `npx.cmd --yes gitnexus@1.6.4-rc.32 status --repo vitruvius`
- GitNexus impact checks for `NodeInspector`, `buildAecMepfsNodeDetail`, `buildAecMepfsNodeDetailFromIndex`
- PowerShell URL HEAD checks for seed URLs
- `bun run api/validateResourceLayer.ts`
- `bun run api/indexLocalResources.ts --dir=.ai/13_research/vitruvius_resource_layer_markdown_pack --maxFiles=50`
- `bun test` in `api/`
- `bun test` in `explorer/`
- `bun run build` in `explorer/`
- Kimi seed review and Kimi final review

## 13. Test/validation results
- API tests: 123 pass, 0 fail.
- Explorer tests: 102 pass, 0 fail.
- Explorer production build: pass, with existing large chunk-size warning.
- Resource validation: ok. Warnings are limited to ASCE 7 and ACI 318 standard landing pages missing edition/version context; those links are not accepted primary references.

## 14. Remaining gaps
- No broad backfill was attempted.
- No candidate reviewer/admin sidebar mode was added.
- Only Open Library adapter was implemented in this loop.
- ASCE/ACI accepted standards links require edition/section-specific metadata before promotion.
- Local indexed files are metadata records only and need separate review before node linkage.
- Rule/Definition/Procedure/Exception/Evidence/Document node creation was not performed.

## 15. Recommended next loop
Build a reviewer workflow for candidate resources, then add Crossref/OpenAlex/Google Books adapters with mocked tests. Promote standards only after edition/section-specific verification and human review.

---

# Loop 2 Addendum - Reviewer/Admin Workflow

Date: 2026-05-01
Status: implementation loop 2 completed

## Summary
Loop 2 added a local/dev reviewer workflow for Resource Layer candidates, needs_review links, rejected links, standards missing context, and indexed local files. It preserves the loop 1 registry and seed decisions without broad backfill or automatic promotion.

## Files changed in loop 2
- `api/resourceLayer/types.ts`
- `api/resourceLayer/registry.ts`
- `api/resourceLayer/validation.ts`
- `api/resourceLayer/reviewWorkflow.ts`
- `api/index.ts`
- `api/validateResourceLayer.ts`
- `api/resourceLayer.test.ts`
- `explorer/src/types/index.ts`
- `explorer/src/api/graphApi.ts`
- `explorer/src/api/graphApi.test.ts`
- `explorer/src/App.tsx`
- `explorer/src/components/HomeScreen.tsx`
- `explorer/src/components/resource-review/ResourceReviewAdmin.tsx`
- `explorer/src/components/resource-review/ResourceReviewAdmin.test.tsx`
- `explorer/src/app.searchInspector.integration.test.tsx`
- `006_System-Manifests/resource-layer/review-decisions.json`
- `docs/knowledge-graph/resource-layer.md`
- `.ai/13_research/resource_layer_implementation_progress.md`
- `.ai/05_logs/2026-05-01_resource_layer_review_workflow.md`
- `.ai/10_state/decisions.md`

## New routes
- `GET /resources/review/queue`
- `GET /resources/review/candidates`
- `GET /resources/review/local-files`
- `GET /resources/review/standards`
- `GET /resources/review/report`
- `POST /resources/review/link/:linkId/decision`
- `POST /resources/review/candidate/:candidateId/decision`
- `POST /resources/review/local-file/:fileId/decision`

## New UI surface
- `/dev/resource-review` in the Explorer.
- Home screen link: `Resource Review (local/dev)`.

## Registry/status changes
- Added empty append-only review log `review-decisions.json`.
- No production resource, candidate, local file, or node-resource-link status was changed.
- No broad backfill was performed.

## Kimi review summary
Accepted Kimi corrections: block standard/code candidate promotion without edition and jurisdiction/scope; include resource snapshots in link decision logs; require local indexed path existence before local-file admission/linking; include local file path/hash origin in local-file link notes.

Deferred/qualified: auth/role gate, cross-file locking/transaction manifest, and full reviewer forms are recommended hardening for the next loop. The `Resource.year` critique was rejected because the type exists and publication-year context is an explicit standards-review requirement.

## Metrics after loop 2
- Resources: 7
- Node-resource links: 9
- Source families: 25
- Resource candidates: 4
- Accepted links: 5
- Needs-review links: 3
- Rejected links: 1
- Local files indexed: 25
- Local files admitted: 0
- Standards missing context: 2
- Duplicate groups: 0
- Broken link checks: 0
- Validation blockers: 0
- Validation errors: 0
