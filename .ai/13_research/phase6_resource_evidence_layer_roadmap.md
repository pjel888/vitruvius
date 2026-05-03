# Phase 6 Resource / Evidence Layer Roadmap

**Generated:** 2026-05-03T01:00:00+08:00
**Status:** Phases 6A–6F complete and accepted.

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
- 21 API evidence-path regression tests
- 4 Explorer Source Custody tab tests
- Evidence-path quality contract
- No-mutation regression verification
- Coverage matrix
- **Status:** ACCEPTED.

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

**Phase 6E** is complete. Next steps require explicit authorization:

1. **Phase 6G** — External candidate persistence (apply/create mutation route)
2. **Independent audit** of Phase 6A–6E evidence layer (preferred before persistence)
3. **Standards context completion** for ASCE 7 and ACI 318 (requires real source research)

All subject to:
- External URL/Book/PDF metadata workflows remain candidate/reviewer-only.
- No fake DOI, ISBN, edition, version, jurisdiction, or AHJ adoption metadata.
- No learner exposure until reviewer acceptance and validation.

---

*Roadmap current as of 2026-05-03.*
