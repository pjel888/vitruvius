# Canonical Graph Stewardship Final Report

Date: 2026-05-01

## 1. Implementation summary
This loop implemented a safe Canonical Graph Stewardship workflow instead of merging production duplicates directly. It adds file-backed duplicate candidate groups, stewardship decisions, alias records, redirect records, transaction manifests, canonical validation, canonical review API routes, and a local/dev Explorer UI at `/dev/canonical-review`. It also hardened the Resource Layer reviewer workflow with explicit dev/admin gates, typed forms, request validation, file locks, transaction manifests, and clearer metrics.

## 2. Files changed
- `api/graph/canonicalStewardship.ts`
- `api/canonicalGraphStewardship.test.ts`
- `api/validateCanonicalGraphStewardship.ts`
- `api/index.ts`
- `api/resourceLayer/registry.ts`
- `api/resourceLayer/reviewWorkflow.ts`
- `api/resourceLayer/transactionManifest.ts`
- `api/resourceLayer.test.ts`
- `explorer/src/api/graphApi.ts`
- `explorer/src/api/graphApi.test.ts`
- `explorer/src/App.tsx`
- `explorer/src/types/index.ts`
- `explorer/src/components/canonical-review/CanonicalReviewAdmin.tsx`
- `explorer/src/components/canonical-review/CanonicalReviewAdmin.test.tsx`
- `explorer/src/components/resource-review/ResourceReviewAdmin.tsx`
- `explorer/src/components/resource-review/ResourceReviewAdmin.test.tsx`
- `explorer/src/app.searchInspector.integration.test.tsx`
- `.ai/13_research/canonical_graph_stewardship_loop_progress.md`
- `.ai/13_research/canonical_graph_stewardship_final_report.md`
- `.ai/13_research/canonical_graph_stewardship_validation_report.md`
- `.ai/13_research/canonical_graph_stewardship_decision_log.md`
- `.ai/05_logs/2026-05-01_canonical_graph_stewardship_loop.md`
- `.ai/10_state/decisions.md`
- `docs/knowledge-graph/resource-layer.md`

## 3. Baseline duplicate/canonical findings
- Duplicate normalized-label groups: 544.
- Safe duplicate review candidates from previous graph validation: 251.
- Unsafe/manual review candidates from previous graph validation: 293.
- Current canonical stewardship validation unresolved groups: 544.
- Applied stewardship decisions: 0.
- Aliases: 0.
- Redirects: 0.
- Blockers: 0.

## 4. Concrete duplicate investigation
### concrete
- IDs: `VTN-DOM-0000068`, `VTN-DOM-0000267`.
- `VTN-DOM-0000068`: `Concrete`, type `topic`, taxonomy `MAT > MAT.CON`, aliases include `cementitious materials` and `cast concrete`, edge count 4.
- `VTN-DOM-0000267`: `Concrete`, type `subtopic`, taxonomy `STR > STR.MAT > STR.MAT.CON`, aliases include `structural materials concrete`, edge count 6.
- Decision/status: no merge. High-risk duplicate group remains unresolved and available in `/dev/canonical-review` and `GET /graph/canonical/duplicates?concreteOnly=true`.

### reinforced concrete
- IDs: `VTN-DOM-0000271`, `VTN-DOM-0012147`.
- `VTN-DOM-0000271`: type `subtopic`, structural taxonomy, edge count 7.
- `VTN-DOM-0012147`: type `concept`, architectural-material taxonomy, aliases include `RC`, edge count 33.
- Decision/status: no merge. High-risk duplicate group remains unresolved and review-gated.

## 5. Canonical stewardship model
Decision types:
- `MERGE_INTO_CANONICAL`
- `ALIAS_TO_CANONICAL`
- `KEEP_SEPARATE`
- `NEEDS_HUMAN_REVIEW`
- `REJECT_DUPLICATE_CANDIDATE`
- `SPLIT_OR_RETYPE_NEEDED`

Decision records include reviewer, rationale, candidate group, canonical target, source nodes, affected edge IDs, affected Resource Layer link IDs, aliases/search terms, risk level, before snapshot, after preview, status, validation result, and optional Kimi notes.

Risk scoring considers node type differences, taxonomy differences, combined edge count, Resource Layer link count, and subtype/homonym signals. Destructive merge apply is blocked for non-low-risk groups. Alias application is non-destructive and does not tombstone source nodes. Proposed decisions can be recorded without applying aliases or redirects.

## 6. API routes added/updated
- `GET /graph/canonical/duplicates`
- `GET /graph/canonical/duplicates/:groupId`
- `POST /graph/canonical/duplicates/:groupId/preview`
- `POST /graph/canonical/duplicates/:groupId/decision`
- `GET /graph/canonical/decisions`
- `GET /graph/canonical/node/:nodeId`
- `GET /graph/canonical/search?q=`
- `GET /graph/canonical/validation`
- Existing AEC-MEPFS `/search` now prepends canonical-preferred results only when approved aliases/redirects exist.

## 7. UI routes/components added/updated
- Added `/dev/canonical-review`.
- Added duplicate group list/detail, risk badges, concrete quick filter, node summaries, structured stewardship form, and dry-run diff preview.
- Updated `/dev/resource-review` to remove prompt/confirm-based mutation and use a structured reviewer decision form.
- Both review surfaces show local/dev admin gating language.

## 8. Search behavior changes
Canonical-preferred search is general and decision-driven. It uses approved alias/redirect records from `006_System-Manifests/graph-canonical/`. With no applied decisions, current search behavior is unchanged. Once a reviewer applies an alias/merge decision, canonical results are ranked ahead of duplicate/deprecated entries while specific subtypes remain searchable.

## 9. Edge/resource preservation behavior
Dry-run previews show:
- affected edges,
- projected source/target rewrites,
- self-loop risks,
- duplicate edge consolidations against existing canonical edges,
- affected Resource Layer `nodeResourceLinks`,
- aliases/search terms that would be added,
- redirect records for merge decisions only.

This loop does not rewrite production graph edges or Resource Layer links. It records safe alias/redirect decisions for downstream resolution. Resource Layer links pointing at redirected nodes are preserved and reported by validation rather than deleted.

## 10. Resource Layer hardening changes
- Server-side local/dev gate added to Resource Layer mutation POST routes.
- `/dev/resource-review` now uses typed reviewer forms instead of browser prompt/confirm.
- Review request bodies validate decision values, reviewer/rationale types, refs arrays, scores, and object fields.
- File-backed Resource Layer mutations now use `.resource-layer-review.lock`, stale-lock cleanup, and transaction manifests under `006_System-Manifests/resource-layer/transaction-manifests/`.
- Review mutation responses include `transactionManifest`.
- Metrics now distinguish `resourcesTotal`, `resourcesNonRejected`, `resourcesWithAcceptedLinks`, and `acceptedNodeResourceLinks` while preserving `acceptedResources` for compatibility.

## 11. Tests added
- `api/canonicalGraphStewardship.test.ts`
- `explorer/src/components/canonical-review/CanonicalReviewAdmin.test.tsx`
- Updated Resource Layer tests for transaction manifests.
- Updated graph API client tests for canonical endpoints.
- Existing Sendai Mediatheque/Toyo Ito regression remains covered in API tests.

## 12. Validation scripts added/updated
- Added `api/validateCanonicalGraphStewardship.ts`.
- Existing `api/validateGraphRelationships.ts` and `api/validateResourceLayer.ts` still pass.

## 13. Commands run
- `bash ./scripts/refresh_code_intelligence.sh`
- `bun test api/canonicalGraphStewardship.test.ts`
- `bun test api/resourceLayer.test.ts`
- `cd api && bun test`
- `cd explorer && bun test`
- `cd explorer && bun run build`
- `bun run api/validateGraphRelationships.ts`
- `bun run api/validateResourceLayer.ts`
- `bun run api/validateCanonicalGraphStewardship.ts`
- Kimi review commands through local CLI.

## 14. Test/build/validation results
- API tests: 142 passed, 0 failed.
- Explorer tests: 111 passed, 0 failed.
- Explorer build: passed. Vite emitted the pre-existing large chunk warning for >500 kB chunks.
- Graph relationship validation: OK, 0 relationship issues; duplicate normalized labels remain 544 for review.
- Resource Layer validation: OK; warnings remain for ASCE 7 and ACI 318 missing edition/version context; blockers 0.
- Canonical stewardship validation: OK; duplicate groups 544, unresolved 544, concrete groups 2, decisions 0, aliases 0, redirects 0, blockers 0.

## 15. Kimi review summary
### Strategy review
Accepted:
- Keep concrete/reinforced-concrete as high-risk review candidates rather than auto-merging.
- Add non-destructive alias semantics and decision-gated canonical search.
Deferred:
- Partial-overlap / external equivalence / temporal version states.
- Reviewer priority severity workflow.

### Dry-run/merge review
Accepted:
- Alias does not tombstone source nodes.
- Non-low-risk destructive merges are blocked.
- Validation checks redirected canonical targets and alias records pointing to redirected nodes.
Deferred:
- Rollback/unmerge implementation.
- Predicate domain/range validation.
- Node property merge strategy for true merges.
- Signed manifests.

### Resource Layer hardening review
Accepted:
- Server-side dev/admin gate and stale lock cleanup.
- Structured reviewer forms and transaction manifests.
Deferred:
- Production auth, CSRF/rate limiting, signed manifests, bulk queue UX, richer metric-delta diff.

### Final review
Final Kimi review was requested after implementation and is summarized in the log as a risk review item: current workflow safely avoids destructive production merges but still needs rollback and richer ontology states in a later loop.

## 16. Regression status
- Sendai Mediatheque/Toyo Ito: passed (`VTN-DOM-0012495` neighborhood includes `VTN-DOM-0012436` and edge `VTN-DOM-0012436--has_facet--VTN-DOM-0012495`).
- Resource Layer routes: API tests passed.
- `/dev/resource-review`: tests and build passed.
- Selected-node relationship visibility: graph relationship validation and API tests passed.

## 17. Remaining gaps
- No production duplicate merges were applied.
- No rollback/unmerge flow yet.
- No production auth/CSRF/rate limiting for shared deployments.
- No predicate domain/range validation for canonical rewrites yet.
- No rich ontology states for partial equivalence, external equivalence, or version-scoped equivalence.
- No batch review UX yet.

## 18. Recommended next loop
Add a steward packet workflow for one or two concrete duplicate groups with Kimi/steward review, including explicit KEEP_SEPARATE vs ALIAS_TO_CANONICAL decisions, reviewer diff evidence, rollback metadata, and domain/range validation before any merge-like apply path is considered.

## Kimi final implementation review addendum
Kimi final verdict: the loop safely addressed the canonical fragmentation workflow by building deterministic custody and blocking unsafe ontology merges. Kimi explicitly agreed that preserving Concrete/Reinforced Concrete as high-risk review groups was the right stop condition. Accepted follow-up: next loop should triage the two concrete groups through the UI to validate the end-to-end flow. Deferred: objective auto-merge criteria for truly obvious cases, batch review UI, operational queue-age metrics, rollback query UI, and roadmap/milestone reconciliation beyond this implementation report.
