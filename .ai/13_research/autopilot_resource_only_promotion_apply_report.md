# Autopilot Resource-Only Promotion Apply Report

**Date:** 2026-05-05
**Phase:** 6N recovery and repair
**Status:** IMPLEMENTED AND TERMINAL-VALIDATED

## Implementation Result

Resource-only external candidate promotion apply is now implemented against the real Resource Layer registry contract:

- Hono routes mounted in `api/index.ts`:
  - `POST /resources/review/external-candidates/:candidateId/promotion-apply-preview`
  - `POST /resources/review/external-candidates/:candidateId/promotion-apply`
  - `POST /resources/review/external-candidates/:candidateId/promotion-rollback-preview`
  - `POST /resources/review/external-candidates/:candidateId/promotion-rollback`
- The prior unmounted Express-only `promotionApplyRoutes.ts` was removed.
- Apply writes through `006_System-Manifests/resource-layer/resources.json`.
- Apply updates `006_System-Manifests/resource-layer/external-metadata-candidates.json`.
- Apply and rollback use `withResourceLayerTransaction`.
- Rollback checks dependent nodeResourceLinks before hard deletion.
- `resource_and_links` remains blocked with `F0`.

## Safety Gates

Confirmed in code and tests:

- `requireLocalDevAdmin` gates Hono mutation routes.
- Candidate must be `ready_for_promotion_review`.
- Reviewer, rationale, sourceOfContext, previewHash, warning acknowledgement, and promotion caveat are required for apply.
- Server-side gates rerun during apply.
- Placeholder URL/DOI/ISBN values are rejected.
- Unsupported verification claims are rejected.
- Incomplete ASCE 7 / ACI 318 context is rejected.
- `learnerVisible=true` is rejected.
- Apply creates exactly one Resource in temp fixtures.
- Apply creates zero nodeResourceLinks.
- Rollback preview/apply works in temp fixtures.
- Transaction manifests are written in temp fixture apply/rollback.

## Production State

Production counts after tests/validators:

- Resources: 7
- nodeResourceLinks: 9
- External metadata candidate records: 0
- No production Resource created.
- No production nodeResourceLink created.
- No learner exposure occurred.
- No external verification occurred.
- No graph/canonical mutation occurred.

## Validation Evidence

- `bun test api/resourceLayerExternalCandidatePromotionApply.test.ts`: 45 pass, 0 fail
- Focused Resource/Evidence tests:
  - promotion preview: 14 pass
  - external candidate review: 26 pass
  - external candidates: 46 pass
  - resource evidence path: 21 pass
  - resource layer: 38 pass
  - standards context: 17 pass
- `cd api && bun test`: 387 pass, 0 fail
- `cd explorer && bun test`: 118 pass, 0 fail
- `cd explorer && bun run build`: PASS, with Vite chunk-size warning
- `.venv\Scripts\python.exe -m pytest scripts/tests/test_kg_aec_relationship_improvement.py`: 118 pass
- No-write validators: all PASS

## Remaining Scope

`resource_and_links` is not implemented. It remains the next planned objective and must not create links until a separate audited plan defines link eligibility, per-node rationale, learner eligibility computation, transaction manifest coverage, and rollback behavior.
