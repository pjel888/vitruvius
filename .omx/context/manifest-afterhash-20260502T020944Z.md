# Ralph Context Snapshot - Manifest afterHash enforcement

Task statement: Implement latest transaction manifest afterHash/current-file validation for Vitruvius canonical/resource custody manifests.

Desired outcome: Validation identifies latest manifest per custody file, compares latest afterHash to current file hash, ignores superseded older manifests, supports strict/non-strict policy, exposes status in /dev/canonical-review, tests pass, and reports are updated.

Known facts/evidence:
- HEAD is d988f49e and synced with origin/main at loop start.
- Worktree was cleaned after stopping stale relationship-improvement background processes and removing an untracked generated overlay.
- Current canonical stewardship has hash-chained transaction manifests and optional HMAC signatures.
- P1 packets are unsigned because no HMAC key is configured; this is warning-only outside strict mode.

Constraints:
- No fake approvals/resources/graph content.
- No production duplicate merges or P0 edge admission without real approval.
- Preserve graph, canonical, Resource Layer routes and UI behavior.
- Avoid false positives for older superseded manifests and non-custody generated reports.

Unknowns/open questions:
- Exact transaction manifest shapes for canonical and Resource Layer need confirmed from code.
- Exact UI validation type additions needed for CanonicalReviewAdmin.
- Whether Resource Layer manifests share the same manifest schema or need separate status.

Likely touchpoints:
- api/graph/canonicalStewardship.ts
- api/validateCanonicalGraphStewardship.ts
- api/canonicalGraphStewardship.test.ts
- explorer/src/types/index.ts
- explorer/src/components/canonical-review/CanonicalReviewAdmin.tsx
- explorer/src/components/canonical-review/CanonicalReviewAdmin.test.tsx
- .ai/13_research/continuous_vitruvius_*.md/json
