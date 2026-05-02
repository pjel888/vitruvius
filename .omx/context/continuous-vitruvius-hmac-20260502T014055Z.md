# Continuous Vitruvius HMAC Loop Context

## Task statement
Implement optional HMAC/signature support for P1 packet evidence locks, validate it, expose status in canonical review UI, record Kimi review, then continue to next safe unblocked task if runtime permits.

## Desired outcome
P1 packets can be signed with an env key, validation reports signed/unsigned/invalid/strict behavior, UI shows signature/snapshot status, and no canonical approvals/merges/resources are faked.

## Known facts/evidence
- Last pushed HEAD: 059c328b.
- Current working tree has one dirty file: scripts/vitruvius/kg/aec_relationship_improvement.py; this is outside immediate HMAC scope and must not be overwritten.
- Current P1 packets already include sourceSnapshot.snapshotHash, packetContentHash, groupInputHash, candidateEdgeNeighborhoodHash, and truthCaveat.
- P0 Concrete/Reinforced Concrete lack approval and remain proposed/unresolved.

## Constraints
- No fake approval, no merges, no fake resources, no production P0/P1 destructive action.
- Preserve graph relationship, Resource Layer, canonical API, and UI behavior.
- Signature must not imply ontology truth, source truth, approval, or merge safety.
- Do not expose HMAC secrets or sensitive key hints.

## Unknowns/open questions
- Exact relation to existing transaction HMAC convention in canonical manifests.
- Whether existing P1 packet validation should warn for unsigned packets by default.
- How much UI detail can be added without overloading CanonicalReviewAdmin.

## Likely touchpoints
- api/graph/canonicalStewardship.ts
- api/validateCanonicalGraphStewardship.ts
- api/canonicalGraphStewardship.test.ts
- explorer/src/types/index.ts
- explorer/src/components/canonical-review/CanonicalReviewAdmin.tsx
- 006_System-Manifests/graph-canonical/p1-decision-packets.json after regeneration
- .ai/13_research continuous loop logs/reports
