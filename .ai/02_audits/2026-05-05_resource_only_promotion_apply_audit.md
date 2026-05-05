# Resource-Only Promotion Apply Audit

**Date:** 2026-05-05
**Phase:** 6O audit of recovered Phase 6N
**Verdict:** PASS_RESOURCE_ONLY_BASELINE

## Audit Scope

Audited the recovered resource-only external candidate promotion apply implementation after terminal validation.

Files in scope:

- `api/index.ts`
- `api/resourceLayer/externalCandidatePromotionApply.ts`
- `api/resourceLayer/types.ts`
- `api/resourceLayerExternalCandidatePromotionApply.test.ts`
- Related focused Resource/Evidence tests

## Findings

| Requirement | Result | Evidence |
|---|---:|---|
| Production Resource remains 7 when production candidate count is 0 | PASS | `validateResourceLayer` reports `resources: 7` |
| Production nodeResourceLinks remain 9 | PASS | `validateResourceLayer` reports `nodeResourceLinks: 9` |
| External candidate production registry remains 0 | PASS | focused tests clean registry; production diff is empty |
| resource_only route exists and is gated | PASS | Hono routes in `api/index.ts`, focused route tests |
| resource_and_links remains unimplemented | PASS | apply returns `F0`; tests assert no writes |
| Apply creates no nodeResourceLinks | PASS | temp apply test asserts zero links |
| Apply writes transaction manifest | PASS | temp apply test asserts manifest file |
| Rollback preview/apply works | PASS | temp rollback test asserts resource removal and manifest |
| No learner exposure | PASS | `learnerVisible=false`; existing learner endpoint tests pass |
| No external verification | PASS | verification flags false; no external fetch/API used |
| No graph/canonical mutation | PASS | graph/canonical validators pass unchanged baseline |
| ASCE 7 / ACI 318 fake context not invented | PASS | standards tests and validator warnings remain unchanged |

## Validation Commands

- `bun test api/resourceLayerExternalCandidatePromotionApply.test.ts`
- `bun test api/resourceLayerExternalCandidatePromotionPreview.test.ts`
- `bun test api/resourceLayerExternalCandidateReview.test.ts`
- `bun test api/resourceLayerExternalCandidates.test.ts`
- `bun test api/resourceEvidencePath.test.ts`
- `bun test api/resourceLayer.test.ts`
- `bun test api/resourceLayerStandardsContext.test.ts`
- `bun run api/validateResourceLayer.ts -- --no-write`
- `bun run api/validateGraphRelationships.ts -- --no-write`
- `bun run api/validateCanonicalGraphStewardship.ts -- --no-write`
- `cd api && bun test`
- `cd explorer && bun test`
- `cd explorer && bun run build`
- `.venv\Scripts\python.exe -m pytest scripts/tests/test_kg_aec_relationship_improvement.py`

## Caveats

The repository has a large unrelated dirty worktree. GitNexus whole-repo change detection reports HIGH risk because it includes those unrelated files. Scoped staging must include only the Phase 6N files before commit.

ChunkHound and code-review-graph refresh completed, but:

- ChunkHound reported 96 timed-out source files and embedding provider errors.
- code-review-graph reported YAML parser warnings due missing `tree-sitter-yaml`.

These warnings do not invalidate the Phase 6N Resource/Evidence validation evidence above.

## Next Gate

`resource_and_links` must remain blocked until its plan and independent audit are created. The plan must define per-node rationale, node existence checks, relation validation, learner eligibility computation, rights/standards gates, transaction manifests, and rollback.
