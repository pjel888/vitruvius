# Continuous Vitruvius Decision Log — Phase 6N

**Created:** 2026-05-04

---

## Decision: Phase 6N Resource-Only Implementation

**Date:** 2026-05-04
**Decision:** Implement resource_only promotion apply infrastructure

**Rationale:**
- Phase 6M audit verdict: PASS_ALLOW_PHASE_6N_RESOURCE_ONLY_IMPLEMENTATION
- Phase 6L design specified all gates, API routes, transaction model, and rollback
- resource_only mode is safe: no nodeResourceLinks, no learner exposure, no external verification

**Scope:**
- Gate implementation A-I (skipping F for resource_only)
- 4 API routes: preview, apply, rollback-preview, rollback
- Transaction manifest + rollback model
- Test suite for all gate groups

**Consequences:**
- Promotion apply infrastructure exists (resource_only mode)
- resource_and_links remains blocked
- Next phase: 6O independent audit

---

## Decision: Resource ID Prefix

**Date:** 2026-05-04
**Decision:** Use `res_<uuid>` for resource IDs

**Rationale:**
- Clear prefix for identification
- UUID v4 ensures uniqueness
- No sequential IDs to prevent collision

---

## Decision: Manifest-based Rollback

**Date:** 2026-05-04
**Decision:** Rollback writes its own transaction manifest

**Rationale:**
- Audit trail preservation
- Rollback operations are traceable
- Supports both hard_delete and mark_rolled_back

---

## Decision: No Automated Production Promotion

**Date:** 2026-05-04
**Decision:** Phase 6N does not auto-promote any production candidates

**Rationale:**
- Production external candidate count is 0
- Any production promotion requires explicit authorization and passing all gates
- The infrastructure is implemented and tested, but not executed against production data

---

## Decision: Repair Phase 6N Against Runtime API

**Date:** 2026-05-05
**Decision:** Keep Phase 6N scoped to `resource_only` and repair it against the real Hono API, Resource Layer registry paths, and transaction wrapper.

**Rationale:**
- The 2026-05-04 Phase 6N run reported implementation but could not verify terminal output, tests, validators, or git state.
- The mounted runtime API is Hono, not the unmounted Express route file.
- Production external metadata candidates remain 0, so validation must use temp fixtures and keep production resources and links unchanged.

**Scope:**
- Mount resource-only promotion apply and rollback routes in `api/index.ts`.
- Use real Resource Layer registry paths and transaction manifests.
- Preserve `resource_and_links` as explicitly unimplemented pending Phase 6P planning and audit.
- Keep learner visibility false and create zero nodeResourceLinks in resource-only apply.

**Consequences:**
- Phase 6N is terminal-verified and audited as a resource-only infrastructure baseline.
- Production resources remain 7 and production nodeResourceLinks remain 9.
- Next phase is 6P resource_and_links planning, not implementation.

---

## Decision: Resource-And-Links Temp-Fixture Baseline

**Date:** 2026-05-05
**Decision:** Implement `resource_and_links` promotion mode only as a gated, transaction-backed Resource Layer operation, with production registries remaining unchanged unless a real production candidate exists and passes all gates.

**Rationale:**
- Phase 6P plan and audit allowed implementation under temp-fixture and production-cleanliness constraints.
- Production external metadata candidate count is 0, so production apply must not create Resources or nodeResourceLinks.
- Link learner eligibility must be computed by `isLearnerSidebarEligible`, never asserted manually.

**Scope:**
- Require explicit proposed node ids, valid node-resource relation, and per-node rationale.
- Validate route-mode node ids against the file-backed AEC-MEPFS Explorer graph.
- Default created links to `needs_review`.
- Block accepted/human_reviewed requested links unless accepted-link learner eligibility passes.
- Include resources, node-resource-links, and external candidate registry in transaction manifests.
- Roll back by removing owned links before the Resource for hard-delete rollback.

**Consequences:**
- Resource-only and resource_and_links promotion infrastructure are both implemented.
- Production resources remain 7 and production nodeResourceLinks remain 9.
- Learner exposure remains zero.
- External verification remains out of scope pending a separate plan.

---

## Decision: Seven-File Phase 7 Entry Blocker Disposition

**Date:** 2026-05-06
**Decision:** Commit the seven reviewed dirty root/scripts files and scoped reports, while keeping Phase 7 implementation blocked pending a separate project-owner implementation prompt.

**Rationale:**
- The seven files were the remaining Phase 7 entry blocker from the delegated reviewer gate.
- Codex classified and tested the seven-file diff.
- Kimi, acting as project-owner-delegated external AI reviewer, returned `PASS_COMMIT_SAFE_FILES`.
- `scripts/vitruvius/canonicalize.py` has CRITICAL GitNexus impact, so the disposition records a critical-impact caveat and does not authorize corpus-wide canonicalization, production mutation, or Phase 7 implementation.

**Scope:**
- Commit only the seven reviewed files and scoped `.ai` reports/logs/state updates.
- Do not stage quarantined `003_Canonical-Knowledge-Layer` files, generated conversion/source artifacts, production Resource Layer registries, graph-canonical registries, or transaction manifests.

**Consequences:**
- The seven-file dirty blocker is dispositioned and pushed in `faddb6e8ad7242cfddd2aa4359c913ceb1f2a0d6`.
- Phase 7 planning remains allowed.
- Phase 7 implementation remains blocked until a separate prompt authorizes a concrete candidate intake batch.

---

## Decision: Phase 7A Reviewer-Only Candidate Intake

**Date:** 2026-05-06
**Decision:** Persist only reviewer-only, unverified external metadata candidates for the first Phase 7A batch.

**Rationale:**
- The project owner explicitly authorized a bounded Phase 7A implementation prompt for reviewer-only candidate intake.
- Candidate metadata was found in repo-local Resource Layer records for ASCE 7 and FHWA Earth Retaining Structures.
- Kimi, acting as project-owner-delegated external AI reviewer, returned `PASS_PERSIST_REVIEWER_ONLY_CANDIDATES`.
- The AISC source-family reference lacked enough stable repo-local metadata and was deferred.

**Scope:**
- Persist two records in `006_System-Manifests/resource-layer/external-metadata-candidates.json`.
- Record transaction manifests for the external-candidate registry writes.
- Keep candidates `candidate`, `unverified`, `reviewer_only`, `learnerVisible=false`, and no-auto-verification/promotion/linking/exposure.
- Preserve production Resources at 7 and nodeResourceLinks at 9.

**Consequences:**
- Phase 7A candidate intake has started with two reviewer-only production external metadata candidates.
- No Resource creation, nodeResourceLink creation, promotion, source verification, learner exposure, graph/canonical mutation, P0 work, or high-risk P1 work occurred.
- Next safe action is review/correction decision workflow for these candidates, not promotion.

---

## Decision: Phase 7B Conservative Candidate Review Decisions

**Date:** 2026-05-06
**Decision:** Apply conservative review-decision statuses to the two Phase 7A external metadata candidates without promotion.

**Rationale:**
- The project owner authorized a bounded Phase 7B review/correction workflow for the two candidates only.
- Kimi, acting as project-owner-delegated external AI reviewer, returned `REQUEST_STANDARDS_CONTEXT` for ASCE 7 and `REQUEST_SOURCE_CUSTODY_REVIEW` for Earth Retaining Structures.
- ASCE 7 lacks real edition/version/scope/jurisdiction/source context, so promotion readiness would require invented context or external verification.
- Earth Retaining Structures has repo-local URL/source metadata only; reachability/source custody/rights suitability remain unverified.

**Scope:**
- Update only `006_System-Manifests/resource-layer/external-metadata-candidates.json`.
- Append one decision history entry per candidate.
- Write transaction manifests for both external-candidate review decisions.
- Keep candidates unverified, reviewer-only, and learner-hidden.

**Consequences:**
- ASCE 7 is now `standards_context_needed`.
- Earth Retaining Structures is now `source_custody_review_needed`.
- Production Resources remain 7 and nodeResourceLinks remain 9.
- External metadata candidate count remains 2.
- No promotion, Resource creation, nodeResourceLink creation, external verification, learner exposure, graph/canonical mutation, P0 work, or high-risk P1 work occurred.
- Next safe action requires real ASCE 7 context, a separately authorized FHWA source-custody/source-verification workflow, or another reviewer-only intake batch.

---

## Decision: Phase 7C Verification Workflow Planning Only

**Date:** 2026-05-06
**Decision:** Plan standards-context and source-custody verification workflows without performing verification or mutating production Resource Layer registries.

**Rationale:**
- ASCE 7 is blocked at `standards_context_needed` because edition/version/scope/jurisdiction/source context is missing.
- Earth Retaining Structures is blocked at `source_custody_review_needed` because repo-local URL/source metadata is candidate-only and reachability, rights, and custody are not verified.
- Moving either candidate toward promotion requires workflow gates before any future verification, Resource creation, link creation, or learner exposure can be considered.

**Scope:**
- Define standards-context required fields, placeholder blockers, statuses, and output rules.
- Define source-custody stages, required fields, future optional checks, and hard non-verification rules.
- Plan future preview/decision API routes only.
- Plan ResourceReviewAdmin panels and future tests.
- Update Phase 7 state/roadmap artifacts.

**Consequences:**
- Phase 7C remains planning only.
- No source verification, candidate promotion, Resource creation, nodeResourceLink creation, learner exposure, graph/canonical mutation, P0 work, or high-risk P1 work occurred.
- Next implementation requires a separate prompt authorizing standards-context/source-custody review preview and decision workflows only.

---

## Decision: Phase 7D Controlled Source Verification

**Date:** 2026-05-06
**Decision:** Implement controlled source-verification preview/decision workflows and apply conservative in-review statuses to the two existing Phase 7 candidates.

**Rationale:**
- The project owner explicitly authorized bounded official-source URL metadata checks for existing external metadata candidates.
- ASCE 7 official ASCE landing page metadata was reachable, but edition/version/year/scope/jurisdiction/applicability context remains missing.
- Earth Retaining Structures official FHWA `www.fhwa.dot.gov` page was reachable and title metadata matched, but rights/access/source custody review remains incomplete.
- Kimi, acting as project-owner-delegated external AI reviewer, supported `MARK_STANDARDS_CONTEXT_IN_REVIEW` and `MARK_SOURCE_CUSTODY_IN_REVIEW`.

**Scope:**
- Add source-verification helper code, preview routes, decision routes, status vocabulary, and focused tests.
- Update only external metadata candidate status/history for the two existing candidates.
- Write transaction manifests for both Phase 7D candidate decisions.
- Keep candidates unverified, reviewer-only, and learner-hidden.

**Consequences:**
- ASCE 7 is now `standards_context_in_review`.
- Earth Retaining Structures is now `source_custody_in_review`.
- Production Resources remain 7 and nodeResourceLinks remain 9.
- External metadata candidates remain 2.
- No promotion, Resource creation, nodeResourceLink creation, learner exposure, graph/canonical mutation, P0 work, high-risk P1 work, protected content ingestion, DOI lookup, ISBN lookup, source truth claim, current/governing/compliance/AHJ claim, or learner trust claim occurred.

---

## Decision: Phase 7 Autopilot Source Verification UI Support

**Date:** 2026-05-06
**Decision:** Add ResourceReviewAdmin UI/client support for existing Phase 7D source-verification preview and decision routes.

**Rationale:**
- Phase 7D backend routes already exist and are covered by API tests.
- Current next action listed ResourceReviewAdmin UI support as the safest unblocked objective.
- ASCE 7 and Earth Retaining Structures remain reviewer-only, unverified, and learner-hidden.
- UI support improves the reviewer workflow without creating Resources, nodeResourceLinks, promotions, graph/canonical changes, or learner exposure.

**Scope:**
- Explorer client route wrappers.
- Explorer source-verification preview types.
- ResourceReviewAdmin source-verification mode for persisted external candidates.
- Focused Explorer contract/component tests.
- Scoped `.ai` reports/logs.

**Consequences:**
- Reviewers can run preview/decision flows from the admin UI for existing backend routes.
- The UI displays source-check metadata, caveats, blockers, warnings, protected-content flags, and no-promotion/no-learner-exposure warnings.
- Backend gates remain authoritative for dev/admin access, blocker enforcement, preview rerun, transaction manifests, and candidate status/history-only writes.
- No Resource, nodeResourceLink, promotion, learner exposure, graph/canonical mutation, P0 work, high-risk P1 work, source-truth claim, current/governing/compliance/AHJ claim, or new external source check occurred in this UI unit.

---

## Decision: Phase 7 Candidate Intake Wave 1 Source-Family Seeds

**Date:** 2026-05-06
**Decision:** Persist three repo-local source-family references as reviewer-only external metadata candidates.

**Rationale:**
- `source-families.json` contains repo-local metadata for buildingSMART, AISC, and AIA.
- Kimi reviewed the intake packet as `project_owner_delegated_ai_reviewer` and returned `PASS_PERSIST_REVIEWER_ONLY_SOURCE_FAMILY_REFERENCES`.
- The records intentionally omit exact URLs and stable source identifiers because no exact source/resource URL was reviewed in this wave.

**Scope:**
- Add three `source_family_reference` external metadata candidates.
- Keep all three as `candidate`, `unverified`, `reviewer_only`, and `learnerVisible: false`.
- Write transaction manifests through the existing external-candidate persistence workflow.

**Consequences:**
- External metadata candidate count increases from 2 to 5.
- Production Resources remain 7.
- Production nodeResourceLinks remain 9.
- No promotion, Resource creation, nodeResourceLink creation, learner exposure, graph/canonical mutation, P0 work, high-risk P1 work, external verification, URL/DOI/ISBN lookup, protected-content access, source-truth claim, current/governing/compliance/AHJ claim, or fake metadata occurred.
