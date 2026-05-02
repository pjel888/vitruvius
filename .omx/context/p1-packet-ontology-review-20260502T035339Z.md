# Context - P1 Packet Ontology Review

Task: Implement bounded P1 per-packet ontology review workflow.

Desired outcome: P1 decision packets become reviewable ontology packets with mutable review metadata, filters, detail view, preview/apply review metadata path, validation metrics, and Kimi/human review notes while preserving packet custody hashes and avoiding graph/resource/canonical mutation.

Known evidence:
- HEAD/origin main: c6ac91c2 Add standards context review workflow.
- Current P1 packet file: 006_System-Manifests/graph-canonical/p1-decision-packets.json with 20 packets, unsigned in this environment.
- Existing canonical implementation: api/graph/canonicalStewardship.ts, api/index.ts, explorer/src/components/canonical-review/CanonicalReviewAdmin.tsx, explorer/src/api/graphApi.ts, explorer/src/types/index.ts.
- Existing validation covers P1 packet hash/signature/source snapshot custody.

Constraints:
- No production graph mutation, no approval/merge/alias/redirect/tombstone/admitted relationships.
- Review metadata must not invalidate immutable packetContentHash/sourceSnapshot/hash/signature fields.
- Use a separate review registry if safest.
- Apply path must be dev/admin gated and transaction-manifest-backed.
- Preserve unrelated dirty AEC worktree files.

Unknowns:
- Kimi final response timing; if unavailable, record timeout/deferred rather than fabricating review.
- Exact route naming can adapt to existing p1-decision-packets route convention.

Likely touchpoints:
- api/graph/canonicalStewardship.ts
- api/index.ts
- api/canonicalGraphStewardship.test.ts
- api/validateCanonicalGraphStewardship.ts
- explorer/src/api/graphApi.ts
- explorer/src/types/index.ts
- explorer/src/components/canonical-review/CanonicalReviewAdmin.tsx
- explorer/src/components/canonical-review/CanonicalReviewAdmin.test.tsx
- 006_System-Manifests/graph-canonical/p1-packet-reviews.json
- .ai/13_research and .ai/05_logs reports
