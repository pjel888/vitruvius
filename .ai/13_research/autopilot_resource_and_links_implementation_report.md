# Autopilot Resource-And-Links Implementation Report

**Date:** 2026-05-05
**Phase:** 6P-impl
**Scope:** Resource/Evidence Layer only

## Verdict

`resource_and_links` promotion mode is implemented for reviewer-gated, transaction-backed Resource Layer promotion using temp fixtures in tests. Production registries remained unchanged because production external metadata candidate count is still 0.

## Implemented

- `POST /resources/review/external-candidates/:candidateId/promotion-apply-preview` now supports `resource_and_links`.
- `POST /resources/review/external-candidates/:candidateId/promotion-apply` now dispatches to resource-only or resource-and-links apply mode.
- `resource_and_links` requires:
  - local/dev/admin route gate,
  - candidate status `ready_for_promotion_review`,
  - reviewer, rationale, sourceOfContext, promotionCaveat,
  - previewHash and acknowledgeWarnings,
  - explicit `proposedNodeIds`,
  - existing AEC-MEPFS node ids when route mode is used,
  - valid `proposedRelation`,
  - per-node rationale for every proposed node.
- Created nodeResourceLinks default to `needs_review`.
- Requested accepted/human_reviewed links are blocked unless `isLearnerSidebarEligible(link, resource)` passes.
- Resource and nodeResourceLinks record:
  - no external verification,
  - no graph/canonical mutation,
  - no learner exposure,
  - promotion decision id,
  - transaction manifest id,
  - created-from external candidate id.
- Rollback now removes links created by the same promotion before removing the Resource for hard-delete rollback.
- Rollback blocks hard-delete when dependent links are not owned by the promotion.

## Files Changed

- `api/resourceLayer/externalCandidatePromotionApply.ts`
- `api/resourceLayer/types.ts`
- `api/index.ts`
- `api/resourceLayerExternalCandidatePromotionApply.test.ts`

## Safety Results

| Safety Boundary | Result |
|-----------------|--------|
| Production Resources | unchanged at 7 |
| Production nodeResourceLinks | unchanged at 9 |
| Production external metadata candidates | unchanged at 0 |
| Production Resource Layer manifests | unchanged at 0 files |
| Learner exposure | none |
| External verification | none |
| Graph/canonical mutation | none |
| ASCE 7 / ACI 318 | still incomplete and not learner-trusted |

## Test Evidence So Far

- `bun test api/resourceLayerExternalCandidatePromotionApply.test.ts`: PASS, 56 pass / 0 fail.
- `cd api && bun test`: PASS, 398 pass / 0 fail.
- `bunx tsc --noEmit --pretty false | Select-String changed files`: no diagnostics in changed files. Full API typecheck still has pre-existing unrelated diagnostics.
- `bun run api/validateResourceLayer.ts -- --no-write`: PASS, resources 7, nodeResourceLinks 9.
- `bun run api/validateGraphRelationships.ts -- --no-write`: PASS, admitted 264, base edges 13,670, effective edges 13,934.
- `bun run api/validateCanonicalGraphStewardship.ts -- --no-write`: PASS, admitted relationships 264, blockers [].
- `cd explorer && bun test`: PASS, 118 pass / 0 fail.
- `cd explorer && bun run build`: PASS, existing Vite chunk-size warning only.
- `.venv\Scripts\python.exe -m pytest scripts/tests/test_kg_aec_relationship_improvement.py`: PASS, 118 pass.
- `git diff --cached --check`: PASS.
- `npx.cmd --yes gitnexus@1.6.4-rc.32 detect-changes --scope staged --repo vitruvius`: PASS_LOW_RISK, 10 files, 53 symbols, 0 affected processes.

## Remaining Validation Before Commit

- final production registry diff check
