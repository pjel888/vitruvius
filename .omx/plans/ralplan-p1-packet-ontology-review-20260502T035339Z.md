# Ralplan - P1 Packet Ontology Review

## Intent
Implement advisory-only P1 per-packet ontology review metadata and UI/API workflow without mutating graph/resource/canonical admission data.

## Acceptance Criteria
1. P1 packet review metadata exists in a separate registry so packet custody hashes remain stable.
2. API supports filtered P1 packet list, packet detail, review preview, and gated review apply.
3. Review apply requires reviewer/source/summary/nextAction as appropriate, writes transaction manifest, appends history, and does not mutate graph/aliases/redirects/tombstones/approvals/admitted relationships/resources.
4. Canonical validation reports review metrics, invalid/stale/missing-review records, and strict-mode coverage if configured.
5. /dev/canonical-review exposes P1 packet review list, filters, detail, custody hashes, review form, preview, and disabled/gated apply behavior.
6. Tests cover valid/invalid/stale/missing review states, API preview/apply behavior, UI rendering, and regressions.
7. Kimi review is recorded or timeout is documented.
8. Broad validation passes.

## Implementation Slices
- Add P1 packet review types, registry path, read/write helpers, validation helpers, and transaction-backed preview/apply service.
- Add API route handlers and parser for review decisions.
- Extend validation summary/report output.
- Extend Explorer API/types and CanonicalReviewAdmin UI/tests.
- Add report/state/log updates.

## Plan Critique
- Risk: in-packet mutable metadata invalidates packet hashes. Mitigation: separate p1-packet-reviews.json registry.
- Risk: review wording implies approval. Mitigation: reviewCaveat and validation blockers for approval-like wording/actions.
- Risk: apply route mutates graph indirectly. Mitigation: transaction file list limited to review registry; tests assert counts remain zero.
- Risk: unrelated dirty AEC files get committed. Mitigation: stage only bounded files.

## Execution Checklist
- [x] Verify dirty worktree and current packet data.
- [x] Refresh code intelligence before edits.
- [x] Implement review registry/service/API.
- [x] Implement validation metrics.
- [x] Implement UI and tests.
- [x] Run targeted and broad validation.
- [x] Record Kimi suggestions and outcomes.
- [ ] Code-review/change-scope checks.
- [ ] Commit/push coherent bounded changes.
