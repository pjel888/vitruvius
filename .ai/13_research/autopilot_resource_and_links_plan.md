# Autopilot Resource-And-Links Promotion Plan

**Date:** 2026-05-05
**Phase:** 6P
**Status:** PLAN_READY_FOR_AUDIT

## Scope

Implement `applyMode=resource_and_links` as an extension of the already validated resource-only external candidate promotion workflow.

This phase may create Resource Layer records only through dev/admin-gated apply routes, transaction manifests, and temp test fixtures unless a real production candidate exists and passes every gate. Current production external metadata candidate count is 0, so implementation and validation must keep production resources at 7 and production nodeResourceLinks at 9.

## Boundaries

- No external fetching, URL reachability, DOI lookup, ISBN lookup, book API, PDF fetch, or source verification.
- No graph, canonical, P0, high-risk P1, merge, alias, redirect, tombstone, or graph-edge admission mutation.
- No ASCE 7 or ACI 318 context invention.
- No learner exposure from candidates, resource-only promoted resources, or newly created needs_review links.
- No source markdown artifacts staged.

## Apply Contract

Required request fields:

- `applyMode: "resource_and_links"`.
- `reviewer`, `rationale`, `sourceOfContext`, `promotionCaveat`.
- `previewHash` and `acknowledgeWarnings: true`.
- `proposedNodeIds`: non-empty explicit node IDs.
- `proposedRelation`: one value from `NODE_RESOURCE_RELATIONSHIPS`.
- `perNodeRationales`: object keyed by node ID; every proposed node requires a non-placeholder rationale.

Optional request fields:

- `acceptedLinkReview`: defaults to false.
- `linkReviewStatus`: only `needs_review` or `accepted`; default `needs_review`.
- `linkNotes` / `perNodeNotes` for reviewer-only context.

Rejected request fields/claims:

- `learnerVisible=true`.
- `verificationStatus=verified`, `source_verified`, `urlReachable`, `doiVerified`, `isbnVerified`, `sourceVerified`.
- Any unsupported governing/current/AHJ/compliance assertion.
- `resource_only` semantics inside `resource_and_links` apply.

## Gate Model

Reuse Phase 6N gates A, B, C, D, E, G, H, and I:

- Candidate must be `ready_for_promotion_review`.
- Reviewer, rationale, sourceOfContext, promotionCaveat, previewHash, and warning acknowledgement are mandatory.
- Placeholders/fake metadata are rejected.
- Unsupported verification claims are rejected.
- Incomplete standard context is rejected, with ASCE 7 and ACI 318 remaining blocked unless real reviewer-supplied context already exists.
- Learner visibility must be false.

Add Gate F for resource_and_links:

- `proposedNodeIds` must be non-empty.
- Every proposed node must exist in the current AEC-MEPFS Explorer graph/node set.
- Every proposed node must have its own non-placeholder rationale.
- `proposedRelation` must be a valid `NodeResourceRelationship`.
- Duplicate node IDs are rejected.
- No implicit multi-link creation from candidate-level rationale alone.
- No accepted link may be produced unless accepted-link eligibility passes.

## Link Status And Learner Eligibility

Default link status:

- `needs_review`.

Accepted status is allowed only when all accepted-link gates pass:

- Resource verification is not `unverified` or `rejected`.
- External resources have `lastCheckedAt`.
- Resource has source-rights declared use boundary and admission provenance.
- Rights are not protected-content.
- Standard/code resources have complete edition/version, jurisdiction/geographicScope, and citation/scope context, or structured reviewer/source justification.
- `isLearnerSidebarEligible(link, resource)` returns true.

If accepted-link gates do not pass:

- The route must either downgrade to `needs_review` with explicit warnings or reject an explicit `accepted` request.
- Learner eligibility is computed only by `isLearnerSidebarEligible`; it is never asserted manually.

Given the current no-external-verification rule, newly promoted external resources should normally remain `verificationStatus: "unverified"` and newly created links should remain `needs_review`.

## Resource Creation

- Create a new Resource only when duplicate detection finds no existing matching Resource.
- Duplicate matches block this phase; reuse of existing Resource for new links is deferred unless a later plan defines an explicit `useExistingResourceId` contract.
- Resource defaults stay reviewer-only:
  - `displayPolicy: "reviewer_only"` or `dev_only`.
  - `learnerVisibleDefault: false`.
  - `verificationStatus: "unverified"` unless a real prior review state supports a stronger non-external status.
  - source truth, rights, and standards caveats preserved.

## NodeResourceLink Creation

For each explicit proposed node:

- Create exactly one nodeResourceLink.
- Use the explicit node-specific rationale.
- Use the explicit valid relationship.
- Set scores conservatively from request values only if in 0..1; otherwise default to low reviewer-only values.
- Set `reviewStatus: "needs_review"` unless accepted-link gates pass.
- Set `verifiedBy` only if backed by reviewer identity and review status supports it.
- Include `reviewNotes` documenting no external verification and no learner exposure.

## Transaction Manifest

Actual apply must run through `withResourceLayerTransaction` and include:

- `resources.json`.
- `node-resource-links.json`.
- `external-metadata-candidates.json`.

The result must report:

- created Resource IDs.
- created nodeResourceLink IDs.
- link review statuses.
- learner eligibility per link.
- transaction manifest ID.
- rollback plan.
- no graph/canonical mutation.
- no external verification.
- no learner exposure unless accepted eligibility passes.

## Rollback

Rollback preview must list:

- created Resource IDs.
- created nodeResourceLink IDs.
- candidate decision IDs.
- whether hard delete is possible.

Rollback apply must:

- remove created nodeResourceLinks first.
- remove the created Resource if no remaining links depend on it.
- otherwise mark the Resource rolled back.
- write a rollback transaction manifest touching all Resource Layer files changed by rollback.
- preserve audit/candidate decision history where available.

## API/UI Plan

API:

- Extend the existing Hono promotion apply route to dispatch `resource_and_links`.
- Add or extend apply preview to show proposed link writes, default statuses, learner eligibility, and rollback plan.
- Keep every route behind `requireLocalDevAdmin`.

Explorer:

- Add client helpers only after API implementation tests pass.
- ResourceReviewAdmin may remain preview-only in this phase if documented, but must not imply link apply is available until controls are implemented and gated.

## Tests

Focused API tests must prove:

- dev/admin gate required.
- `resource_only` still works.
- `resource_and_links` requires proposedNodeIds.
- missing per-node rationale is blocked.
- invalid node is blocked.
- invalid relation is blocked.
- duplicate proposed nodes are blocked.
- incomplete standards and ASCE/ACI fake context are blocked.
- unknown/restricted rights block learner eligibility.
- resource_and_links creates one temp Resource and explicit temp links only.
- default link status is `needs_review`.
- no link is learner eligible unless `isLearnerSidebarEligible` returns true.
- transaction manifest includes resources, links, and external candidates.
- rollback removes temp links and Resource.
- production resources remain 7.
- production nodeResourceLinks remain 9.
- production external candidates remain 0.

Explorer/API tests must prove:

- NodeInspector learner mode shows only accepted eligible links.
- candidates and reviewer-only items remain hidden from learner endpoints.
- source-custody queue classifies new needs_review links as reviewer-only in temp fixtures.

## Validation

After implementation:

- `bun run api/validateResourceLayer.ts -- --no-write`
- `bun run api/validateGraphRelationships.ts -- --no-write`
- `bun run api/validateCanonicalGraphStewardship.ts -- --no-write`
- focused resource_and_links tests
- `cd api && bun test`
- `cd explorer && bun test`
- `cd explorer && bun run build`
- `.venv\Scripts\python.exe -m pytest scripts/tests/test_kg_aec_relationship_improvement.py`

## Implementation Permission

This plan is implementation-ready only if the independent plan audit passes. If the audit identifies blockers, do not implement until those blockers are resolved.
