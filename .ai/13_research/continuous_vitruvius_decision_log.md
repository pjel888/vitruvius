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

---

## Decision: Phase 7 Candidate Review Wave 1 Needs-Review Status

**Date:** 2026-05-06
**Decision:** Mark the three source-family reference candidates as `needs_review`.

**Rationale:**
- Kimi reviewed the candidates as `project_owner_delegated_ai_reviewer` and returned `MARK_NEEDS_REVIEW` for all three.
- The candidates are legitimate repo-local source-family seeds, but each still carries `minimal_metadata` and `no_stable_identifier` warnings.
- Future source-custody review and/or metadata correction is needed before source verification, Resource creation, link creation, promotion readiness, or learner exposure.

**Scope:**
- Apply `mark_needs_review` decisions through the existing external-candidate review-decision route.
- Append candidate decision history and write three Resource Layer transaction manifests.
- Keep verification status unverified, display policy reviewer-only, and learner visibility false.

**Consequences:**
- External metadata candidate count remains 5.
- Three source-family candidates move from `candidate` to `needs_review`.
- Production Resources remain 7.
- Production nodeResourceLinks remain 9.
- No promotion, Resource creation, nodeResourceLink creation, learner exposure, graph/canonical mutation, P0 work, high-risk P1 work, external verification, URL/DOI/ISBN lookup, protected-content access, source-truth claim, current/governing/compliance/AHJ claim, or fake metadata occurred.

---

## Decision: Phase 7 Source-Family Official Domain Support

**Date:** 2026-05-06
**Decision:** Extend controlled source-verification official-domain support to buildingSMART, AISC, and AIA source-family candidates.

**Rationale:**
- Phase 7 candidate intake wave 1 created three reviewer-only source-family reference candidates for buildingSMART, AISC, and AIA.
- Candidate review wave 1 marked them `needs_review` because they still lacked stable source identifiers and metadata.
- Future source-custody review needs bounded official-domain checks for explicit reviewer-supplied URLs without broad crawling, source-truth claims, or learner exposure.
- Kimi reviewed the diff as `project_owner_delegated_ai_reviewer` and returned `PASS_SOURCE_FAMILY_OFFICIAL_DOMAIN_SUPPORT`.

**Scope:**
- Extend source-verification helper family classification to buildingSMART, AISC, and AIA.
- Allow only `buildingsmart.org`, `aisc.org`, `aia.org`, and their subdomains for those families.
- Add mocked tests for official-domain allowlist behavior, cross-family blocking, and preview route invariants.

**Consequences:**
- Future source-family source-custody review can preview explicit official URLs for buildingSMART, AISC, and AIA.
- This unit performed no live source verification and made no Resource Layer registry changes.
- External metadata candidate count remains 5.
- Production Resources remain 7.
- Production nodeResourceLinks remain 9.
- No promotion, Resource creation, nodeResourceLink creation, learner exposure, graph/canonical mutation, P0 work, high-risk P1 work, protected-content access, source-truth claim, current/governing/compliance/AHJ claim, or fake metadata occurred.

---

## Decision: Phase 7 Candidate Intake Wave 2 Source-Family Seeds

**Date:** 2026-05-06
**Decision:** Persist five more repo-local source-family references as reviewer-only external metadata candidates.

**Rationale:**
- `source-families.json` contains repo-local metadata for U.S. Access Board, WBDG/NIBS, IStructE, ICE, and RIBA.
- Kimi reviewed the intake packet as `project_owner_delegated_ai_reviewer` and returned `PASS_PERSIST_REVIEWER_ONLY_SOURCE_FAMILY_REFERENCES`.
- The records intentionally omit exact URLs and stable source identifiers because no exact source/resource URL was reviewed in this wave.
- ACI was skipped to avoid Concrete/Reinforced Concrete and standards-context risk.

**Scope:**
- Add five `source_family_reference` external metadata candidates.
- Keep all five as `candidate`, `unverified`, `reviewer_only`, and `learnerVisible: false`.
- Write transaction manifests through the existing external-candidate persistence workflow.

**Consequences:**
- External metadata candidate count increases from 5 to 10.
- Production Resources remain 7.
- Production nodeResourceLinks remain 9.
- No promotion, Resource creation, nodeResourceLink creation, learner exposure, graph/canonical mutation, P0 work, high-risk P1 work, external verification, URL/DOI/ISBN lookup, protected-content access, source-truth claim, current/governing/compliance/jurisdiction/AHJ claim, or fake metadata occurred.

---

## Decision: Phase 7 Candidate Review Wave 2 Needs-Review Status

**Date:** 2026-05-06
**Decision:** Mark the five wave 2 source-family reference candidates as `needs_review`.

**Rationale:**
- Kimi reviewed the candidates as `project_owner_delegated_ai_reviewer` and returned `MARK_NEEDS_REVIEW` for all five.
- The candidates are legitimate repo-local source-family seeds, but each still carries `minimal_metadata` and `no_stable_identifier` warnings.
- Future metadata correction, exact source locator review, rights/access review, and source-custody review are required before source verification, Resource creation, link creation, promotion readiness, or learner exposure.

**Scope:**
- Apply `mark_needs_review` decisions through the existing external-candidate review-decision route.
- Append candidate decision history and write five Resource Layer transaction manifests.
- Keep verification status unverified, display policy reviewer-only, and learner visibility false.

**Consequences:**
- External metadata candidate count remains 10.
- Five wave 2 source-family candidates move from `candidate` to `needs_review`.
- Production Resources remain 7.
- Production nodeResourceLinks remain 9.
- No promotion, Resource creation, nodeResourceLink creation, learner exposure, graph/canonical mutation, P0 work, high-risk P1 work, external verification, URL/DOI/ISBN lookup, protected-content access, source-truth claim, current/governing/compliance/AHJ claim, jurisdiction claim, or fake metadata occurred.

---

## Decision: Phase 7 Wave 2 Source-Family Official Domain Support

**Date:** 2026-05-06
**Decision:** Extend controlled source-verification official-domain support to the five Phase 7 wave 2 source-family candidates.

**Rationale:**
- Candidate review wave 2 moved U.S. Access Board, WBDG/NIBS, IStructE, ICE, and RIBA source-family references to `needs_review`.
- Future metadata correction and source-custody review need bounded official-domain checks for explicit reviewer-supplied URLs.
- Repo-local `source-families.json` already lists the official source-family domains.
- Kimi reviewed the diff as `project_owner_delegated_ai_reviewer` and returned `PASS_WAVE2_SOURCE_FAMILY_OFFICIAL_DOMAIN_SUPPORT`.

**Scope:**
- Add source-family identifiers to the controlled source-verification vocabulary.
- Allow only the repo-local official domains for those families.
- Add mocked helper and preview-route tests.

**Consequences:**
- Future source-family source-custody review can preview explicit official URLs for the five wave 2 families.
- This unit performed no live source verification and made no Resource Layer registry changes.
- External metadata candidate count remains 10.
- Production Resources remain 7.
- Production nodeResourceLinks remain 9.
- No promotion, Resource creation, nodeResourceLink creation, learner exposure, graph/canonical mutation, P0 work, high-risk P1 work, protected-content access, source-truth claim, current/governing/compliance/AHJ claim, jurisdiction claim, or fake metadata occurred.

---

## Decision: Phase 7 Autopilot Closure

**Date:** 2026-05-06
**Decision:** Close Phase 7 at the current stable reviewer-only baseline and block further Resource/graph growth until real source context or separate graph authorization is supplied.

**Rationale:**
- All currently unblocked Resource/Evidence, source-verification, candidate intake/review, ResourceReviewAdmin, NodeInspector, and Explorer visual-relationship guard work is complete.
- No external metadata candidate is `ready_for_promotion_review`.
- ASCE 7 still lacks real edition/version/year/scope/applicability/source context.
- Earth Retaining Structures still lacks complete rights/access/source-custody review.
- Ten source-family candidates still lack exact official source locators, rights/access review, and source-custody completion.
- Continuing without those inputs would require invented metadata or unsafe mutation.

**Scope:**
- Create final Phase 7 closure, Resource/Evidence, graph/visual, candidate/link, validation, next-action, and completion-log reports.
- Do not mutate Resource registries, graph/canonical registries, candidates, Resources, nodeResourceLinks, source artifacts, P0 records, or high-risk P1 packets in the closure unit.

**Consequences:**
- Phase 7 is complete for current unblocked work.
- Resources remain 7 and nodeResourceLinks remain 9.
- External metadata candidates remain 12, all reviewer-only, unverified, and learner-hidden.
- Promotion, Resource creation, nodeResourceLink creation, learner exposure, graph/canonical mutation, P0 work, high-risk P1 work, and protected-content/source-truth claims remain blocked until separately authorized.

---

## Decision: Phase 7 Candidate Intake Wave 3 Source-Family Seeds

**Date:** 2026-05-06
**Decision:** Persist two additional repo-local source-family references as reviewer-only external metadata candidates.

**Rationale:**
- `source-families.json` contains repo-local metadata for Uniclass/NBS and OmniClass/CSI.
- Kimi reviewed the intake packet as `project_owner_delegated_ai_reviewer` and returned `PASS_PERSIST_REVIEWER_ONLY_SOURCE_FAMILY_REFERENCES`.
- Both records intentionally omit exact URLs and stable source identifiers because no exact source/resource URL was reviewed in this wave.
- ACI, ISO, NIBS overlap, metadata/discovery-provider families, and general web source families were deferred for safety and scope reasons.

**Scope:**
- Add two `source_family_reference` external metadata candidates.
- Keep both as `candidate`, `unverified`, `reviewer_only`, and `learnerVisible: false`.
- Write transaction manifests through the existing external-candidate persistence workflow.

**Consequences:**
- External metadata candidate count increases from 10 to 12.
- Production Resources remain 7.
- Production nodeResourceLinks remain 9.
- No promotion, Resource creation, nodeResourceLink creation, learner exposure, graph/canonical mutation, P0 work, high-risk P1 work, external verification, URL/DOI/ISBN lookup, protected-content access, source-truth claim, current/governing/compliance/jurisdiction/AHJ claim, or fake metadata occurred.

---

## Decision: Phase 7 Candidate Review Wave 3 Needs-Review Status

**Date:** 2026-05-06
**Decision:** Mark the two wave 3 source-family reference candidates as `needs_review`.

**Rationale:**
- Kimi reviewed the candidates as `project_owner_delegated_ai_reviewer` and returned `MARK_NEEDS_REVIEW` for both.
- The candidates are legitimate repo-local source-family seeds, but each still carries `minimal_metadata` and `no_stable_identifier` warnings.
- Future metadata correction, exact source locator review, rights/access review, and source-custody review are required before source verification, Resource creation, link creation, promotion readiness, or learner exposure.

**Scope:**
- Apply `mark_needs_review` decisions through the existing external-candidate review-decision route.
- Append candidate decision history and write two Resource Layer transaction manifests.
- Keep verification status unverified, display policy reviewer-only, and learner visibility false.

**Consequences:**
- External metadata candidate count remains 12.
- Two wave 3 source-family candidates move from `candidate` to `needs_review`.
- Production Resources remain 7.
- Production nodeResourceLinks remain 9.
- No promotion, Resource creation, nodeResourceLink creation, learner exposure, graph/canonical mutation, P0 work, high-risk P1 work, external verification, URL/DOI/ISBN lookup, protected-content access, source-truth claim, current/governing/compliance/AHJ claim, jurisdiction claim, or fake metadata occurred.

---

## Decision: Phase 7 Wave 3 Source-Family Official Domain Support

**Date:** 2026-05-06
**Decision:** Extend controlled source-verification official-domain support to the two Phase 7 wave 3 source-family candidates.

**Rationale:**
- Candidate review wave 3 moved Uniclass/NBS and OmniClass/CSI source-family references to `needs_review`.
- Future metadata correction and source-custody review need bounded official-domain checks for explicit reviewer-supplied URLs.
- Repo-local `source-families.json` already lists the official source-family domains.
- Kimi reviewed the diff as `project_owner_delegated_ai_reviewer` and clarified `PASS_WAVE3_SOURCE_FAMILY_OFFICIAL_DOMAIN_SUPPORT` with no prohibited trust claim.

**Scope:**
- Add source-family identifiers to the controlled source-verification vocabulary.
- Allow only the repo-local official domains for those families.
- Add mocked helper and preview-route tests.

**Consequences:**
- Future source-family source-custody review can preview explicit official URLs for the two wave 3 families.
- This unit performed no live source verification and made no Resource Layer registry changes.
- External metadata candidate count remains 12.
- Production Resources remain 7.
- Production nodeResourceLinks remain 9.
- No promotion, Resource creation, nodeResourceLink creation, learner exposure, graph/canonical mutation, P0 work, high-risk P1 work, protected-content access, source-truth claim, current/governing/compliance/AHJ claim, jurisdiction claim, or fake metadata occurred.

---

## Decision: Phase 8B Duplicate Candidate Disposition

**Date:** 2026-05-06
**Decision:** Mark the ASCE 7 and FHWA Earth Retaining Structures external metadata candidates as duplicates of existing production Resources, and keep the 10 source-family candidates blocked in `needs_review`.

**Rationale:**
- The project owner authorized Phase 8B real evidence advancement but prohibited fake metadata, duplicate unsafe growth, learner exposure, and unreviewed graph/resource mutation.
- Controlled official-source previews confirmed ASCE/FHWA public landing metadata without protected payloads, but ASCE still lacks required standards context.
- Repo-local Resource Layer records already contain `res-asce-7-official-landing` and `res-fhwa-earth-retaining-structures`, plus existing needs-review nodeResourceLinks.
- Kimi, acting as delegated external AI reviewer, returned `PASS_DUPLICATE_STATUS_ONLY`.
- Creating new Resources or links from duplicate candidates would be unsafe duplication; advancing source-family candidates would require invented exact locators or missing custody metadata.

**Scope:**
- Apply `mark_duplicate` review decisions to two external metadata candidates.
- Write two Resource Layer transaction manifests.
- Keep candidates unverified, reviewer-only, learner-hidden, and not promoted.
- Do not change `resources.json`, `node-resource-links.json`, graph/canonical registries, P0 records, high-risk P1 packets, or Explorer UI.

**Consequences:**
- External metadata candidate statuses are now `duplicate_candidate`: 2 and `needs_review`: 10.
- Production Resources remain 7.
- Production nodeResourceLinks remain 9.
- No Resource creation, nodeResourceLink creation, graph/node/edge admission, learner exposure, protected payload download, source-truth claim, current/governing/compliance/AHJ claim, P0 mutation, or high-risk P1 mutation occurred.
- The exact next action is project-owner supplied real standards/source-custody context or a separately gated evidence-backed graph packet.

---

## Decision: Phase 8C Reviewer-Only Resource And Link Advancement

**Date:** 2026-05-06
**Decision:** Persist three official public metadata candidates, mark them source-custody verified for reviewer-only purposes, create reviewer-only Resources, and create `needs_review` nodeResourceLinks for the exact Kimi-approved node targets.

**Rationale:**
- Phase 8C authorized official-source locator discovery and bounded public metadata checks.
- buildingSMART IFC, WBDG Fire Protection, and Uniclass had official public locators, title/source-family matches, and direct node-specific rationale.
- Kimi, acting as delegated external AI reviewer, returned `PASS_RESOURCE_AND_LINKS_FOR_LISTED_CANDIDATES` and later `PASS_PHASE8C_FINAL_CLOSURE`.
- Learner exposure remains blocked because all new links are `needs_review` and `learnerEligible=false`.

**Scope:**
- Add three external metadata candidates.
- Apply source-custody and ready-for-promotion-review status decisions.
- Create three reviewer-only Resources.
- Create three `needs_review` nodeResourceLinks.
- Harden external-candidate promotion admission actor mapping so delegated AI reviewers are not recorded as biological human reviewers.

**Consequences:**
- Resources increase from 7 to 10.
- nodeResourceLinks increase from 9 to 12.
- External metadata candidates increase from 12 to 15.
- No accepted learner-visible link was created.
- No graph/canonical/P0/high-risk P1 mutation occurred.
- Future work should review the three new links for accepted-link eligibility through the Resource Layer workflow, or prepare a separately gated evidence-backed graph packet.

---

## Decision: Phase 8D Link Acceptance Review And Learner Visibility Guard

**Date:** 2026-05-06
**Decision:** Keep all three Phase 8C nodeResourceLinks as `needs_review` and gate `includeCandidates=true` to reviewer mode only.

**Rationale:**
- Accepted-link dry-runs for buildingSMART IFC, WBDG Fire Protection, and Uniclass all failed because the backing Resources remain `verificationStatus: unverified` and lack `lastCheckedAt`.
- Kimi, acting as project-owner-delegated external AI reviewer, returned `KEEP_NEEDS_REVIEW` for all three links and final `PASS_PHASE8D_LINK_REVIEW_CLOSURE`.
- Visibility verification found that learner-mode `/node/:id/resources?includeCandidates=true` could include reviewer-only Resources.
- Candidate/reviewer-only inclusion is a reviewer/admin capability and must not be activated by learner-mode query parameters.

**Scope:**
- Append transaction-backed `needs_review` decisions for the three existing nodeResourceLinks.
- Keep `learnerEligible=false` and `learnerExposure=false`.
- Update `api/index.ts` so `includeCandidates` is honored only when `mode=reviewer`.
- Add API regression coverage proving learner `includeCandidates=true` remains learner mode and hides reviewer-only Resources.

**Consequences:**
- Resources remain 10.
- nodeResourceLinks remain 12.
- accepted links remain 5.
- External metadata candidates remain 15.
- No Resource creation, nodeResourceLink creation, graph/canonical/P0/high-risk P1 mutation, protected payload storage, fake metadata, source-truth claim, or learner exposure occurred.
- Future accepted-link review requires Resource verification/custody completion, especially WBDG exact locator correction and `lastCheckedAt`/source-custody fields.

---

## Decision: Phase 8E Metadata-Only Source Custody Completion And Accepted Link Review

**Date:** 2026-05-06
**Decision:** Correct metadata-only source-custody fields for the three Phase 8C Resources and accept their existing nodeResourceLinks after preview/apply, Kimi review, and validation.

**Rationale:**
- Phase 8E authorized bounded official public metadata checks, Resource metadata correction, and accepted-link review for buildingSMART IFC, WBDG Fire Protection, and Uniclass.
- Official public locator checks supplied enough metadata to record final URLs, `lastCheckedAt`, source-custody metadata status, and caveats without protected payload storage or source-truth claims.
- Kimi, acting as project-owner-delegated external AI reviewer, returned `PASS_PHASE8E_SAFE_TO_COMMIT`.
- Existing link rationales are node-specific and the accepted-link workflow computed visibility without manually forcing learner eligibility.

**Scope:**
- Update three existing Resources with final URL/canonical URL where needed, `lastCheckedAt`, `verificationStatus: link_verified`, `custodyStatus: source_custody_metadata_checked`, metadata-only caveats, and warning flags.
- Correct WBDG URL to `https://www.wbdg.org/do/secure/fire-protection`.
- Move three existing nodeResourceLinks from `needs_review` to `accepted`.
- Add metadata-correction preview/apply routes and tests.
- Expose source-truth/rights caveats in learner resource summaries.

**Consequences:**
- Resources remain 10.
- nodeResourceLinks remain 12.
- Accepted links increase from 5 to 8.
- No new Resource, no new nodeResourceLink, no graph/canonical/P0/high-risk P1 mutation, no protected payload storage, and no source-truth/current/governing/compliance/AHJ claim occurred.
- Future graph/node improvement still requires a separate evidence-backed graph-admission packet.

---

## Decision: Phase 8F Evidence-Backed Graph Overlay Admission

**Date:** 2026-05-06
**Decision:** Admit one non-destructive, Resource-backed graph overlay edge: `BIM Schemas INFORMS IFC Exchange`.

**Rationale:**
- Phase 8F authorized graph/node improvements only where accepted Resource Layer evidence, source/context gates, relation vocabulary gates, delegated review, dry-run, transaction manifest, rollback, and validation all passed.
- The accepted buildingSMART IFC Resource Layer link to `BIM Schemas` supports a narrow metadata-context relation to the existing `IFC Exchange` node.
- WBDG Fire Protection and Uniclass did not support safe graph mutation from the available metadata-only evidence and remain Resource Layer evidence only.
- Kimi, acting as delegated external AI reviewer, returned `PASS_ADMIT_LISTED_GRAPH_EDGES` for the graph packet and `PASS_PHASE8F_FINAL_CLOSURE` after validation.

**Scope:**
- Roll back the first admission due API-visible wording hygiene.
- Re-admit the same reviewed edge with safe provenance wording and full graph-canonical transaction custody.
- Add API regression coverage for selected-node neighborhood and graph-filter visibility.
- Update fixed graph metric expectations from 13,934 to 13,935 effective edges.

**Consequences:**
- Admitted relationships increase from 264 to 265.
- Base edges remain 13,670.
- Effective edges increase from 13,934 to 13,935.
- `CROSS_DOMAIN_EQUIVALENT` remains 0.
- Resources remain 10 and nodeResourceLinks remain 12.
- No Resource Layer registry mutation, Resource creation, nodeResourceLink creation, learner exposure change, graph node mutation, alias/redirect/tombstone mutation, P0 mutation, or high-risk P1 mutation occurred.

---

## Decision: Phase 8G Evidence-Backed Graph Growth Batch 2

**Date:** 2026-05-06
**Decision:** Admit one non-destructive, Resource-backed graph overlay edge: `Structural Wind Load INFORMS Load Path`.

**Rationale:**
- Phase 8G inspected all 8 accepted Resource Layer links for graph potential.
- The WBDG wind-safety Resource has accepted links to both `Structural Wind Load` and `Load Path`.
- A weak `INFORMS` relation exposes useful visual reasoning context without asserting code status, source truth, current/governing authority, AHJ adoption, compliance, jurisdiction, numerical criteria, design adequacy, or completeness.
- Kimi, acting as delegated external AI reviewer, returned `PASS_ADMIT_LISTED_GRAPH_EDGES`.

**Scope:**
- Admit only `VTN-DOM-0012777--informs--VTN-DOM-0012160`.
- Use canonical relationship admission and approval manifests.
- Add API regression coverage for selected-node neighborhood and graph-filter visibility.
- Update fixed graph metric expectations from 13,935 to 13,936 effective edges.

**Consequences:**
- Admitted relationships increase from 265 to 266.
- Base edges remain 13,670.
- Effective edges increase from 13,935 to 13,936.
- `CROSS_DOMAIN_EQUIVALENT` remains 0.
- Resources remain 10 and nodeResourceLinks remain 12.
- No Resource Layer registry mutation, Resource creation, nodeResourceLink creation, learner exposure change, graph node mutation, alias/redirect/tombstone mutation, P0 mutation, high-risk P1 mutation, or protected payload storage occurred.

---

## Decision: Phase 8H Resource Layer Evidence Boundary And Caveat Standardization

**Date:** 2026-05-06
**Decision:** Keep Phase 8H graph candidates at the Resource Layer boundary and standardize metadata-only evidence caveats on four existing accepted public-web Resources.

**Rationale:**
- All 8 accepted Resource Layer links were inspected for graph potential.
- No additional graph edge passed both the source/context gate and relation vocabulary gate without duplication, overbreadth, or source-truth overclaim risk.
- Kimi, acting as delegated external AI reviewer, returned `PASS_RESOURCE_LAYER_ONLY_NO_GRAPH_MUTATION`.
- Four older accepted public-web Resources already had accepted links and last-checked metadata but lacked the newer standardized caveat fields introduced in later Phase 8 Resource workflows.

**Scope:**
- Update only existing Resource metadata and Resource Layer review history for:
  - `res-us-access-board-accessible-routes-ch4`
  - `res-wbdg-wind-safety-building-envelope`
  - `res-wbdg-seismic-design-principles`
  - `res-ice-structural-load-paths`
- Write Resource Layer transaction manifests for the four metadata correction decisions.
- Preserve Resources, nodeResourceLinks, link statuses, graph/canonical registries, learner visibility, and existing `lastCheckedAt` values.

**Consequences:**
- Resources remain 10.
- nodeResourceLinks remain 12.
- Accepted links remain 8.
- Admitted relationships remain 266.
- Effective edges remain 13,936.
- No new graph edge, node metadata mutation, Resource creation, nodeResourceLink creation, learner exposure, P0 mutation, high-risk P1 mutation, protected payload, `CROSS_DOMAIN_EQUIVALENT`, generic `related_to`, source-truth, current/governing, compliance, AHJ, jurisdiction, numerical, or rights-clearance claim occurred.
- Next safe action is Resource Layer source-custody advancement for blocked candidates and Resources before new graph packets.

---

## Decision: Full Autopilot Exhaustion Boundary

**Date:** 2026-05-07
**Decision:** Close the current full autopilot evidence/resource/link/graph/visual loop as exhausted for safe autonomous action after final validation and delegated review.

**Rationale:**
- All accepted Resource-backed links were inspected for graph, node metadata, and visual potential.
- The remaining `needs_review` links are standards-context blocked and cannot be accepted without real edition/version/scope/applicability context.
- Ten source-family candidates were advanced to `source_custody_in_review`, but they remain broad source-family references without Resource-specific promotion targets, rights/access review, or node-specific rationale.
- Public ASCE and ACI landing metadata is not enough to complete standards context, reverse rejected link disposition, or create learner-trusted claims.
- The current remaining graph candidates are duplicate, broad, overclaiming, or standards-context blocked.

**Scope:**
- No new Resources.
- No new nodeResourceLinks.
- One existing FHWA link accepted.
- Ten source-family candidate statuses advanced to `source_custody_in_review`.
- Explorer/NodeInspector/ResourceReviewAdmin evidence visibility improved.
- No graph/canonical registry mutation in the full loop after the Phase 8H baseline.

**Consequences:**
- Resources remain 10.
- nodeResourceLinks remain 12.
- Accepted links increase from 8 to 9 during the full loop.
- External candidates remain 15.
- Admitted relationships remain 266 and effective edges remain 13,936.
- Future work requires a new Resource-specific source-rights packet, real standards-context evidence, or a separately reviewed graph-admission packet.

---

## Decision: Post-Full Lane B Site/Civil Drainage Candidate Intake Boundary

**Date:** 2026-05-07
**Decision:** Persist two official-source reviewer-only site/civil drainage candidates and advance them only to `source_custody_in_review`.

**Rationale:**
- No project-owner source packet was supplied, so Lane B was the authorized continuation path.
- FHWA and WBDG official public pages provided real locator/public metadata for a narrow site/civil drainage wave.
- Kimi 1.41.0, acting as delegated external AI reviewer, returned `PASS_PERSIST_REVIEWER_ONLY_CANDIDATES`.
- The reviewer explicitly deferred Resource promotion and nodeResourceLinks until a later packet after candidate persistence and status history exist.

**Scope:**
- Add `ext-cand-urban-drainage-design-manual-fourth-edit-mouq8jic-79xs`.
- Add `ext-cand-low-impact-development-technologies-wbdg-mouq8kta-7j15`.
- Apply source verification decisions to `source_custody_in_review`.
- Preserve learner-hidden reviewer-only defaults.

**Consequences:**
- Resources remain 10.
- nodeResourceLinks remain 12.
- Accepted links remain 9.
- External metadata candidates increase from 15 to 17.
- No Resource promotion, nodeResourceLink creation, graph/canonical mutation, learner exposure, protected payload, source-truth, current/governing, AHJ, compliance, rights-clearance, or design-adequacy claim occurred.
