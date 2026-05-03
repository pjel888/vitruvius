# Phase 6 Resource / Evidence Layer Roadmap

Date: 2026-05-03T05:15:00+08:00

## Overview

Phase 6 deepens the Resource / Evidence Layer without mutating graph topology or admitting new graph edges. The goal is trustworthy node-resource recommendations, source-custody discipline, and reviewer workflow improvements.

## Loop 6A: Source-Custody Schema/Model Design

**Status:** ✅ COMPLETED

**Deliverables:**
- Finalize source-custody model documentation (this report set).
- Confirm existing `api/resourceLayer/types.ts` covers all required fields.
- Add validation tests for new custody rules if gaps found.
- Define `displayPolicy` enum and rules.

**Constraints:**
- No Resource Layer registry mutation.
- No new resource admissions.
- Tests only.

**Completion Gate:**
- Schema review complete.
- Validation tests pass.
- No production data changes.

## Loop 6D: Standards-Context Enforcement Hardening

**Status:** ✅ COMPLETED

**Deliverables:**
- Validation: ASCE/ACI links without context cannot be promoted.
- UI: Standards show context-completeness indicator.
- Placeholder rejection expanded to cover justification fields in review workflow.
- `standardContextJustification` workflow tested.
- Reviewer cannot accidentally promote context-incomplete standards.
- Hardened `hasStructuredContextJustification` in `reviewWorkflow.ts` to reject placeholder values, matching `validation.ts`.
- Added focused test file `api/resourceLayerStandardsContext.test.ts` with 17 tests covering:
  - accepted standard missing context → blocker
  - needs-review standard missing context → warning only
  - rejected standard missing context → no blocker
  - placeholder rejection for edition, version, scope, sourceOfContext, rationale
  - complete context requirements
  - justified missing context requirements
  - placeholder justification blocking
  - ASCE 7 / ACI 318 production state verification
  - `isLearnerSidebarEligible` behavior
  - no-write safety

**Constraints:**
- No invented edition/version/scope.
- Missing context must be justified, not hidden.

**Completion Gate:**
- ASCE 7 and ACI 318 links remain blocked without real context.
- Validation tests cover all placeholder values.
- UI shows clear context status.
- Full API test suite passes (221 tests).

## Loop 6B: Node Sidebar Resource Ranking API

**Status:** ✅ COMPLETED

**Deliverables:**
- API endpoint: `GET /node/:id/resources` returns ranked, accepted-only resources.
- Hard limit: 8 resources.
- Apply standards-context modifiers.
- Apply relationship-specificity boosts.
- Return warning flags for incomplete context.
- Update `NodeInspector` Sources tab to consume ranked API.
- Add "Limited evidence" empty state.

**Constraints:**
- Only `accepted` and `human_reviewed` links shown to learners.
- No fake backfill.
- Standards with missing context show caveat, not authority.

**Completion Gate:**
- Sidebar shows 3–8 ranked resources per eligible node.
- Needs-review/candidate links hidden from learners.
- API tests cover ranking and filtering.
- Explorer tests pass.

## Loop 6C: Reviewer Source-Custody Queue

**Status:** ✅ COMPLETED

**Deliverables:**
- Enhanced `ResourceReviewAdmin` with custody-status visibility.
- Rights-status display in reviewer cards.
- Local file triage workflow: review 25 indexed files, admit suitable ones.
- Unified triage view combining links, candidates, local files, and standards.
- Decision preview shows full custody impact before apply.

**Constraints:**
- Local files require explicit reviewer decision; no auto-linking.
- Rights review required before admission.
- No fake source metadata.

**Completion Gate:**
- Reviewer can see custody status, rights, and verification together.
- Local file admission workflow tested.
- Decision history records custody rationale.

## Loop 6E: External URL/Book/PDF Metadata Candidate Workflow

**Status:** 📅 LATER

**Deliverables:**
- Open Library adapter improvements (already mocked/tested).
- Candidate creation for discovered books/URLs.
- Metadata-only recording; no full-text extraction.
- Optional DOI/ISBN normalization verification.
- No auto-verification; all candidates start as `needs_review`.

## Loop 6F: Evidence-Path Tests and Regression Guards

**Status:** ✅ COMPLETED

**Deliverables:**
- Resource Layer no-write audit tests.
- Selected-node sidebar resource regression tests.
- Standards-context regression tests.
- Local file custody regression tests.
- Evidence manifest health checks.

## Loop Sequence

```
6A (design) ✅ → 6D (standards hardening) ✅ → 6B (sidebar ranking) ✅ → 6C (reviewer queue) ✅ → 6F (regression tests) ✅ → 6E (candidates) 📅
```

Rationale: Harden standards context (6D) before exposing resources in sidebar (6B). Improve reviewer tools (6C) before expanding candidates (6E).

## Standing Constraints Across All Loops

- No new graph admissions.
- No graph topology mutation.
- No P0/P1/P2/P3 canonical decision mutation.
- No merge/alias/redirect/tombstone.
- No fake sources, URLs, editions, jurisdictions, or verification.
- No protected payload copying.
- No auto-linking local files.
- All Resource Layer mutations go through reviewer workflow with decision history.
