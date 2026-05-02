# Ralplan - Resource Layer Standards Context Cleanup

## Intent
Build a non-destructive standards-context review workflow for Resource Layer standard/code references, especially ASCE 7 and ACI 318, without inventing context values or auto-promoting links.

## Acceptance Criteria
1. ASCE 7 and ACI 318 missing context appear in review API/UI with missing-field and promotion-blocker reasons.
2. Needs-review standards with missing context remain warnings, not blockers.
3. Accepted/promoted standards missing required context are blockers.
4. Candidate/link promotion is blocked unless required standard context is complete or explicitly reviewer-justified with rationale/source.
5. Context preview returns before/after diff and validation impact without mutation.
6. Context apply requires reviewer, rationale, admin/dev mutation gate, writes review history, and writes a Resource Layer transaction manifest.
7. Placeholder values are rejected.
8. Resource Layer, graph relationship, and canonical stewardship validations pass.
9. No resource, nodeResourceLink, graph edge, approval, merge, alias, redirect, or tombstone is mutated except an explicitly applied context fixture/test path.

## Implementation Slices
- Extend types minimally for standardIdentifier, editionContext, jurisdictionContext, and reviewContext on resources/links where useful.
- Add validation helpers/metrics for standards context.
- Add standards-context preview/apply service functions and API routes.
- Update /dev/resource-review Standards tab with detail form, preview, safety wording, and disabled apply gating.
- Add tests for validation, preview/apply, request validation, UI, and regressions.
- Update reports, Kimi log, decisions, and validation logs.

## Plan Critique
- Risk: overblocking current needs_review ASCE/ACI records. Mitigation: warning-only until accepted/promoted.
- Risk: implied source truth from reviewer form. Mitigation: UI wording and required sourceOfContext/reviewer-supported rationale.
- Risk: touching unrelated dirty AEC files. Mitigation: stage only Resource Layer/coherent report files.

## Execution Checklist
- [x] Verify dirty worktree and avoid unrelated AEC files.
- [x] Refresh code intelligence before code edits.
- [x] Implement service/API/data-model changes.
- [x] Implement UI changes.
- [x] Add targeted tests.
- [x] Run targeted and broad validation.
- [x] Record Kimi suggestions and outcomes.
- [x] Commit/push coherent Resource Layer changes only if validation passes.
