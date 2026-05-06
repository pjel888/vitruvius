# Phase 7B Autopilot Plan

**Date:** 2026-05-06
**Task:** Phase 7B - Review and Correction Decisions for Phase 7A Evidence Candidates
**Workflow:** `$ralplan -> $ralph -> $code-review`

## Intent

Run reviewer/correction decision workflows for exactly the two Phase 7A external metadata candidates and keep them reviewer-only, unverified, unpromoted, and learner-hidden.

## Acceptance Criteria

- Branch is `main`, `HEAD` matches `origin/main`, and latest commit is `d7cc5a21f1b13c4c545b6dba4ee6bdd9c844a54e` or later.
- Resource Layer remains at 7 Resources and 9 nodeResourceLinks.
- External metadata candidates remain exactly 2.
- ASCE 7 receives only a conservative review decision such as `request_standards_context` / `standards_context_needed`, unless gates prove a safer conservative state.
- FHWA Earth Retaining Structures receives only a conservative review decision such as `request_source_custody_review`, `request_rights_review`, or `needs_review`.
- No candidate is promoted or marked `ready_for_promotion_review` unless all gates pass without invented metadata or verification.
- No Resource, nodeResourceLink, graph/canonical registry, P0 Concrete/Reinforced Concrete, or high-risk P1 mutation occurs.
- No learner exposure and no external verification/fetching/API lookup occurs.
- Review decisions are previewed before apply and transaction-manifest-backed if applied.
- Dirty worktree quarantine remains unstaged.
- Validators, focused Resource/Evidence tests, full API tests, Explorer tests/build, and Python KG regression pass.
- Kimi/Claude/OpenCode review and final code-review artifacts record delegated AI identity honestly.

## Plan

1. Preflight repo state, validators, and focused tests.
2. Inspect the two candidate records and current decision history.
3. Build a delegated-review packet with conservative decision options.
4. Use the available external AI reviewer and record verdicts honestly.
5. Preview and apply only reviewer-supported safe decisions through the existing external-candidate review workflow.
6. Verify reviewer-only visibility and no learner/resource/link/promotion side effects.
7. Run validators and UltraQA test cycle.
8. Update Phase 7B reports/state/logs.
9. Run staged scope checks and final code review.
10. Commit and push only scoped Phase 7B files.

## Stop Conditions

Stop if a review decision preview is blocked, source truth would need to be invented, external verification would be required, production Resources or nodeResourceLinks would change, graph/canonical mutation appears, or git/test/validator output becomes unreliable.
