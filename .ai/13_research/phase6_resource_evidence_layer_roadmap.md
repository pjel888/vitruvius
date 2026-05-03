# Phase 6 Resource / Evidence Layer Roadmap

**Generated:** 2026-05-03T01:00:00+08:00
**Status:** Phases 6A–6G complete and accepted. Phase 6H planning complete.

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
- **Status:** PLANNING COMPLETE. Implementation awaiting authorization.
- **Constraints:** planning only, no promotion implementation, no resource creation, no nodeResourceLink creation, no graph mutation, no learner exposure.
- **Deliverables:**
  - Review state machine design (`phase6h_external_candidate_review_states.md`)
  - Review decision record shape (`phase6h_external_candidate_review_decision_record.md`)
  - Promotion readiness gate design (`phase6h_external_candidate_promotion_gate_design.md`)
  - Preview/decision/apply workflow design (`phase6h_external_candidate_review_workflow_design.md`)
  - API route plan (`phase6h_external_candidate_api_plan.md`)
  - UI plan (`phase6h_external_candidate_ui_plan.md`)
  - Test plan (`phase6h_external_candidate_test_plan.md`)
- **Next step:** Await explicit authorization to implement review-decision routes and UI.

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

**Phase 6A–6G** are complete. **Phase 6H planning** is complete.

Next steps require explicit authorization:

1. **Phase 6H implementation:** review-decision workflow (correction preview/apply, review decision preview/apply, decision history)
2. **Phase 6I (future):** candidate-to-resource promotion apply (explicit authorization required)
3. **Independent audit** of full Phase 6A–6H evidence layer
4. **Standards context completion** for ASCE 7 and ACI 318 (requires real source research)

All subject to:
- External metadata workflows remain candidate/reviewer-only.
- No fake DOI, ISBN, edition, version, jurisdiction, or AHJ adoption metadata.
- No learner exposure until reviewer acceptance and validation.
- No graph admissions without P1 review.

---

*Roadmap current as of 2026-05-03.*
