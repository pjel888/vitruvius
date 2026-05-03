# Continuous Vitruvius Decision Log

Date: 2026-05-03T02:15:00+08:00

## Decision

Phase 5 quality gate hardening: turn the Phase 5 audit and targeted gap closure into durable automated quality gates. No new graph admissions. No merge, alias, redirect, tombstone, or Resource Layer mutation.

## Accepted

- 4 new reasoning-path tests added to `api/graphReasoningPaths.test.ts`:
  - No active CROSS_DOMAIN_EQUIVALENT edge
  - Sendai Mediatheque / Toyo Ito visibility
  - Deep/Shallow Foundations distinction
  - Building Envelope taxonomy visibility
- Base-edge normalization in test file for robust BFS traversal.
- 7 new/updated quality hardening reports in `.ai/13_research/`.
- Relation family count corrected from 16 to 15 (reporting error fixed).

## Rejected/deferred

- No new graph edges admitted.
- No high-risk P1 packets admitted.
- No P0 concrete disambiguation performed.
- No `.gitignore` changes applied to untracked source markdowns (deferred to future triage).
- No P1 source snapshot regeneration (deferred; deemed unnecessary).

## Standing Rules

1. Do not resume raw edge scaling.
2. Do not admit new graph edges unless strictly required for a repair.
3. Do not mutate Resource Layer data.
4. Do not merge, alias, redirect, tombstone, rename, delete, or rewrite graph nodes.
5. Do not process P0 Concrete/Reinforced Concrete without human review.
6. Do not admit high-risk P1 packets without human domain review.
