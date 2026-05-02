# Resource Layer Implementation Progress

Status: completed for implementation loop 1
Last updated: 2026-05-01
Context snapshot: `.omx/context/resource-layer-20260501T102153Z.md`

## Phase 1 - Repository and plan ingestion
- [x] Read every markdown file in `.ai/13_research/vitruvius_resource_layer_markdown_pack`.
- [x] Read required state docs and confirmed the current phase remains file-backed AEC-MEPFS with production/live gates blocked.
- [x] Mapped frontend/backend/sidebar/data/test architecture.
- [x] Refreshed code-intelligence indices before editing with `./scripts/refresh_code_intelligence.sh`.
- [x] Ran GitNexus impact for `NodeInspector`, `buildAecMepfsNodeDetail`, and `buildAecMepfsNodeDetailFromIndex`; all reported LOW risk.
- [x] Ran Kimi seed source review before accepting seed links.

## Repository map
- Frontend: React 19, TypeScript, Vite, Bun in `explorer/`.
- Backend: Bun and Hono API in `api/index.ts`.
- Graph runtime: AEC-MEPFS file-backed JSON under `006_System-Manifests/aec-mepfs-backbone/shadow-staging/`.
- Selected node detail path: Explorer selected node -> API `/node/:id` -> `NodeInspector`.
- Existing source UI before this loop: evidence-span-only Sources tab; AEC file-backed node detail returned `evidence: []`.
- Durable resource layer path: `006_System-Manifests/resource-layer/`.

## Implementation checklist
- [x] Resource, NodeResourceLink, SourceFamily, ResourceCandidate, and ResourceCheck types.
- [x] File-backed resource registry service.
- [x] Normalization, dedupe, verification, ranking, and validation services.
- [x] Local corpus metadata/hash scanner and runnable local indexing script.
- [x] Candidate-only Open Library adapter with mocked tests.
- [x] `/node/:id/resources`, `/resources/:id`, `/resources/metrics`, and `resources` included in `NodeDetail`.
- [x] Sidebar Resource / References cards and empty state.
- [x] Seed accepted links only where Kimi accepted and URL checks passed.
- [x] Candidate, needs_review, and rejected records for corrected seed items.
- [x] Metrics endpoint and final implementation report.
- [x] QA cycle completed with API tests, Explorer tests, Explorer build, resource validation, local indexing, and post-edit code-intelligence refresh/change detection.

## Kimi review log summary
- Seed review accepted: U.S. Access Board Accessible Routes; WBDG Wind Safety; WBDG Seismic Design Principles; ICE Structural Load Paths.
- Seed review held/rejected: ASCE 7 landing page needs edition/section/adoption review; FHWA retaining-wall mapping needs U.S. transportation scope review; ACI 318 portal to Structural Column rejected as too broad.
- Final review accepted corrections: add source-rights/admission provenance fields, make ranking penalties explicit, warn on standards without edition/version, and treat WBDG as contextual guidance instead of primary standard authority.
- Final review rejected/qualified: Kimi's statement that accepted resources are hidden was inaccurate; accepted links are displayed by default, while needs_review/candidate/rejected links are intentionally hidden unless `includeCandidates=true`.

## Validation summary
- `bun test` in `api/`: 123 pass, 0 fail.
- `bun test` in `explorer/`: 102 pass, 0 fail.
- `bun run build` in `explorer/`: pass with existing chunk-size warning.
- `bun run api/validateResourceLayer.ts`: ok, 7 resources, 9 links, 25 source families, 0 duplicate groups, 0 broken link checks, 2 warnings for standard landing pages missing edition/version context.
- `bun run api/indexLocalResources.ts --dir=.ai/13_research/vitruvius_resource_layer_markdown_pack --maxFiles=50`: indexed 25 real local markdown files with hashes, 0 errors.

---

## Implementation loop 2 - Reviewer/admin workflow
Status: completed for implementation loop 2
Last updated: 2026-05-01
Context snapshot: `.omx/context/resource-layer-review-workflow-20260501T114806Z.md`

### Scope completed
- [x] Added file-backed review queue and decision helpers in `api/resourceLayer/reviewWorkflow.ts`.
- [x] Added review decision history model and empty append-only log at `006_System-Manifests/resource-layer/review-decisions.json`.
- [x] Added review API routes for queue, candidates, local files, standards, report, link decisions, candidate decisions, and local-file decisions.
- [x] Extended metrics to include local indexed/admitted counts, standards missing context, duplicate warnings, broken link warnings, authority tier distribution, source family distribution, and decision history count.
- [x] Hardened validation with blockers for unsafe accepted standard/code links, accepted links missing source-rights/admission provenance, ASCE/ACI promotions without context, FHWA scope promotion without review, and WBDG primary/governing misuse.
- [x] Added candidate/local-file mutation safeguards: no silent acceptance, no candidate promotion without provenance/source family/reference, no standard/code candidate promotion without edition and jurisdiction/scope, no local-file admission when the indexed path no longer exists, and no local auto-linking.
- [x] Added Explorer local/dev admin route `/dev/resource-review` with queue tabs, metrics, warnings, decision actions, loading/error/empty states, and explicit no-auto-link/no-Neo4j disclaimer.
- [x] Preserved learner-facing `NodeInspector` Sources tab behavior; accepted links remain visible and candidate/needs_review/rejected links remain hidden by default.
- [x] Added API and Explorer tests for review queue, metrics, safe mutation helpers, decision logging, standard promotion blocking, candidate hold/rejection paths, local-file no-auto-link behavior, UI rendering, and decision POST refresh.

### Statuses deliberately unchanged
- ASCE 7 wind/seismic links remain `needs_review`.
- FHWA retaining-wall link remains `needs_review`.
- ACI 318 -> Structural Column remains `rejected`.
- WBDG/NIBS remains contextual guidance.
- No broad backfill was performed.
- No local indexed file was admitted or linked.
- No candidate was promoted in the production registry.

### Kimi loop 2 review
Kimi returned concrete critiques on 2026-05-01. Accepted corrections:
- Block standard/code candidate promotion unless edition/version and jurisdiction/geographic scope are supplied.
- Include resource before/after snapshots in link decision logs when link decisions alter resource metadata.
- Require an indexed local path to still exist before local-file admission/linking.
- Add local path/hash origin notes to local-file-created links.

Qualified or deferred corrections:
- Kimi flagged `year` in standards review as invalid, but `Resource.year` exists in the type and publication-year context is part of the user requirement; no code change made.
- Kimi recommended a full auth/role gate and file-lock transaction system. Loop 2 remains a labeled local/dev admin tool per requirement; production auth and stronger multi-file transaction/locking are recommended next-loop hardening before shared deployment.
- Kimi recommended rejecting resource metadata corrections on link decisions. The user explicitly requested edition/version/section and provenance correction fields on link decisions, so loop 2 preserves them but now logs resource before/after snapshots.

### Validation summary (latest focused loop)
- `bun test api/resourceLayer.test.ts`: 15 pass, 0 fail.
- `bun test explorer/src/components/resource-review/ResourceReviewAdmin.test.tsx`: 3 pass, 0 fail.
- `bun test` in `api/`: 129 pass, 0 fail.
- `bun test` in `explorer/`: 106 pass, 0 fail.
- `bun run build` in `explorer/`: pass with existing chunk-size warning.
- `bun run api/validateResourceLayer.ts`: ok; 7 resources, 9 node-resource links, 25 source families, 4 candidates, 25 local indexed files, 0 local admitted files, 5 accepted links, 3 needs_review links, 1 rejected link, 2 standards_missing_context warnings, 0 blockers, 0 errors.

### Remaining gaps
- Mutation routes are local/dev only and not protected by authentication or role middleware.
- Multi-file writes are atomic per file but not protected by a cross-file lock/transaction manifest.
- Decision UI still uses browser confirm/prompt; a structured reviewer form is recommended before shared use.
- Candidate `accept_as_resource` and `link_to_node` paths are API-supported but intentionally not used on production records in this loop.
