# Phase 6 Resource / Evidence Layer Roadmap

**Generated:** 2026-05-03T01:00:00+08:00
**Status:** Phases 6A–6K complete and accepted. 6L audit pending.

---

## Completed Phases

### Phase 6A: Resource Layer Foundation
- Resource registry schema
- URL health checks
- Canonical URL normalization
- Deduplication checks

### Phase 6B: Node Sidebar Resource Ranking
- `GET /node/:id/resources` learner-safe API
- Resource ranking by status (accepted > human_reviewed > needs_review)
- NodeInspector Sources tab integration
- 8/8 resource ranking rules enforced

### Phase 6C: Source-Custody Reviewer Queue
- `GET /resources/review/source-custody` grouped queue API
- 9 custody groups (learnerVisible, reviewerOnly, needsReview, candidates, localFilesIndexedOnly, standardsContextIncomplete, rightsLimited, rejected, blocked)
- ResourceReviewAdmin Source Custody tab
- Safe badge wording for learner-facing labels

### Phase 6D: Standards-Context Enforcement Hardening
- Incomplete standards blocked from learner view
- Context-preview workflow for standards
- Dry-run decision gates

### Phase 6E: External URL/Book/PDF Metadata Candidate Workflow
- **Status:** COMPLETE and ACCEPTED.
- **Constraints:** reviewer-only, candidate-only, no auto-verification, no fake metadata, no learner exposure.
- **Deliverables:**
  - `api/resourceLayer/externalMetadataCandidates.ts` — pure validation helpers
  - `GET /resources/review/external-candidates/schema` — schema route
  - `POST /resources/review/external-candidates/preview` — preview route (dev-gated, read-only)
  - External Candidates tab in ResourceReviewAdmin
  - 24 API tests + 2 Explorer tests
- **Closure verification:** `.ai/13_research/phase6e_closure_verification_report.md`

### Phase 6F: Evidence-Path Regression Tests and Quality Gate
- **Status:** ACCEPTED.
- **Deliverables:** 21 API evidence-path regression tests, 4 Explorer Source Custody tab tests, evidence-path quality contract, no-mutation regression verification.

### Phase 6G: External Metadata Candidate Persistence
- **Status:** COMPLETE and ACCEPTED.
- **Constraints:** reviewer-only, unverified, no auto-promotion, no auto-linking, no learner exposure, transaction-manifest-backed.
- **Deliverables:**
  - `api/resourceLayer/externalCandidateRegistry.ts` — registry helpers with transaction manifests
  - `006_System-Manifests/resource-layer/external-metadata-candidates.json` — dedicated registry
  - `POST /resources/review/external-candidates` — persist route
  - `GET /resources/review/external-candidates` — list route
  - `GET /resources/review/external-candidates/:candidateId` — detail route
  - Source-custody queue `externalCandidates` group
  - ResourceReviewAdmin save button and persisted list
  - Source-custody route gated
  - 21 new API tests + updated Explorer tests
  - Audit findings reconciled (CROSS_DOMAIN_EQUIVALENT=0, source-custody gated)
  - Test artifact cleanup completed (afterAll + transaction manifest cleanup)
- **Reports:** `.ai/13_research/phase6g_*.md`

### Phase 6H: External Candidate Review Decision Workflow and Promotion Gate Design
- **Status:** PLANNING COMPLETE.
- **Deliverables:**
  - Review state machine design (`phase6h_external_candidate_review_states.md`)
  - Review decision record shape (`phase6h_external_candidate_review_decision_record.md`)
  - Promotion readiness gate design (`phase6h_external_candidate_promotion_gate_design.md`)
  - Preview/correction/apply workflow design (`phase6h_external_candidate_review_workflow_design.md`)
  - API route plan (`phase6h_external_candidate_api_plan.md`)
  - UI plan (`phase6h_external_candidate_ui_plan.md`)
  - Test plan (`phase6h_external_candidate_test_plan.md`)

### Phase 6J: Audit Remediation
- **Status:** COMPLETE and ACCEPTED.
- **Deliverables:**
  - Fixed Explorer test import error (missing graphApi mock exports)
  - Fixed API test flakiness (retry loop for parallel test interference)
  - Fixed registry timestamp dirtiness (deterministic timestamp)
  - Created consolidated Phase 6I traceability document
  - All tests pass, validators clean

### Phase 6K: Promotion Preview Only
- **Status:** COMPLETE and ACCEPTED.
- **Constraints:** preview ONLY, no promotion apply, no resource creation, no nodeResourceLink creation, no graph mutation, no learner exposure, no external verification.
- **Deliverables:**
  - `api/resourceLayer/externalCandidatePromotionPreview.ts` — pure read-only promotion preview helper
  - `POST /resources/review/external-candidates/:candidateId/promotion-preview` — read-only promotion preview route
  - Updated `explorer/src/components/resource-review/ResourceReviewAdmin.tsx` — Promotion Preview tab in ExternalCandidateReviewPanel
  - Updated `explorer/src/api/graphApi.ts` — `previewExternalCandidatePromotion` client function
  - 14 new API tests in `api/resourceLayerExternalCandidatePromotionPreview.test.ts`
  - All 342 API tests pass, 118 Explorer tests pass, build succeeds
  - Validators pass with no new warnings
- **Reports:** `.ai/13_research/phase6k_*.md`

### Phase 6L: Promotion Apply Planning
- **Status:** PLANNING COMPLETE.
- **Constraints:** planning ONLY, no implementation, no resource creation, no nodeResourceLink creation, no graph mutation, no learner exposure.
- **Deliverables:**
  - Promotion apply philosophy (2 apply modes: resource-only, resource+links)
  - 9 promotion apply eligibility gates (A-I)
  - Future Resource record shape with safe defaults and forbidden fields
  - Future NodeResourceLink record shape with link acceptance rules
  - 4 future API routes (apply-preview, apply, rollback-preview, rollback)
  - Transaction/rollback model with manifest requirements
  - Promotion apply UI plan with safe wording requirements
  - 21 API tests + 10 UI tests planned for future implementation
  - 38 hard stop conditions + 4 warning conditions
- **Reports:** `.ai/13_research/phase6l_*.md`

### Phase 6I: External Candidate Correction and Review Decision Workflow Implementation
- **Status:** COMPLETE and ACCEPTED.
- **Constraints:** correction and review decisions only, no promotion apply, no resource creation, no nodeResourceLink creation, no graph mutation, no learner exposure, no external verification.
- **Deliverables:**
  - `api/resourceLayer/externalCandidateReview.ts` — review state/decision types, promotion readiness helper, correction preview/apply, review decision preview/apply, decision history
  - `POST /resources/review/external-candidates/:candidateId/correction-preview` — read-only correction preview
  - `POST /resources/review/external-candidates/:candidateId/correction` — apply metadata correction
  - `POST /resources/review/external-candidates/:candidateId/review-preview` — read-only decision preview
  - `POST /resources/review/external-candidates/:candidateId/review-decision` — apply review decision
  - `GET /resources/review/external-candidates/:candidateId/history` — decision history
  - Updated `api/resourceLayer/externalCandidateRegistry.ts` — expanded status types, `decisions` field
  - Updated `api/resourceLayer/sourceCustodyQueue.ts` — review-state-aware nextReviewAction
  - Updated `explorer/src/components/resource-review/ResourceReviewAdmin.tsx` — ExternalCandidateReviewPanel with detail, correction, decision, history tabs
  - Updated `explorer/src/api/graphApi.ts` — new API client functions
  - 26 new API tests in `api/resourceLayerExternalCandidateReview.test.ts`
  - All 328 API tests pass
  - Explorer build succeeds
  - Validators pass with no new warnings
- **Reports:** `.ai/13_research/phase6i_*.md`

---

## Standing Constraints (All of Phase 6)

- No Wave 10.
- No graph topology changes without P1 review.
- No production Resource Layer mutation without reviewer workflow.
- No auto-linking local files.
- No auto-promoting resources, candidates, standards, or local files.
- ASCE 7 and ACI 318 remain blocked until real standards context is supplied.
- P0 Concrete/Reinforced Concrete remains gated.

---

## Next Authorized Work

**Phase 6A–6L** are complete.

Next steps require explicit authorization:

1. **Phase 6M audit** — Independent audit of promotion apply plan (resource-only first)
2. **Phase 6N (future, needs separate authorization)** — Resource-only promotion apply implementation
3. **Phase 6O (future, needs separate authorization)** — Resource + nodeResourceLink promotion apply implementation
4. **Phase 6P (future, needs separate authorization)** — Link acceptance workflow
5. **Standards context completion** for ASCE 7 and ACI 318 (requires real source research)

All subject to:
- External metadata workflows remain candidate/reviewer-only.
- No fake DOI, ISBN, edition, version, jurisdiction, or AHJ adoption metadata.
- No learner exposure until reviewer acceptance and validation.
- No graph admissions without P1 review.
- Promotion apply must not be implemented without explicit project-owner steward authorization.

---

*Roadmap current as of 2026-05-03.*
