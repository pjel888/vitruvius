# Continuous Vitruvius Decision Log

Date: 2026-05-03T03:40:00+08:00

## Decision

Phase 5 final custody closure: close manifest afterHash drift from fire/egress metadata-only rationale repair, complete no-write validator coverage, run full validation, and commit clean state.

## Accepted

- Deleted `api/wave10TargetedGapClosure.ts` (unsafe admission-capable untracked script).
- Fixed duplicate-base-edge test normalization bug in `api/graphReasoningPaths.test.ts`.
- Strengthened reasoning-path tests with exact edge ID assertions.
- Strengthened Drainage test to assert both DRAINS_TO and DISCHARGES_TO independently.
- Added semantic assertions for underrepresented relation families.
- Updated report snapshot drift (14→18 tests, 257→264 edges, 16→15 families).
- Documented fire/egress rationale review; queued for future metadata repair.
- Reclassified 2 COORDINATES_WITH NEEDS_REVIEW edges as PASS_WITH_MINOR_CAVEAT.
- Documented traceability gaps as acceptable at current scale.
- Confirmed high-risk P1 packets remain blocked.

## Rejected/deferred

- No new graph edges admitted.
- No high-risk P1 packets admitted.
- No P0 concrete disambiguation performed.
- No registry metadata mutations (rationale updates deferred).
- No `.gitignore` changes applied to untracked source markdowns.
- No per-edge transactionManifestId/rollbackPlan schema migration (deferred).

## Standing Rules

1. Do not resume raw edge scaling.
2. Do not admit new graph edges unless strictly required for a repair.
3. Do not mutate Resource Layer data.
4. Do not merge, alias, redirect, tombstone, rename, delete, or rewrite graph nodes.
5. Do not process P0 Concrete/Reinforced Concrete without human review.
6. Do not admit high-risk P1 packets without human domain review.
