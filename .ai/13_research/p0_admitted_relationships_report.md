# P0 Admitted Relationships Report

Date: 2026-05-02

## Current admitted relationship status

No P0 production graph relationship was admitted in this loop.

- Approval records: 0
- Admitted relationship records: 0
- Production graph edge count: unchanged at 13,670
- Aliases: 0
- Redirects: 0
- Tombstones: 0
- Merges: 0

## Concrete proposed relationship

- Decision: `canonical-20260501155958-e011dc288980`
- Group: `dup-0aa1351d9475`
- Proposal: `VTN-DOM-0000267 RELATED_SPECIALIZATION_OF VTN-DOM-0000068`
- Status: proposed-only metadata
- Admission status: not admitted because no real steward approval record exists

## Reinforced Concrete proposed relationships

- Decision: `canonical-20260501155958-f8da3711275f`
- Group: `dup-3751564358d7`
- Existing proposed metadata: reciprocal `CROSS_DOMAIN_EQUIVALENT`
- Admission behavior: normalized to reciprocal `CROSS_DOMAIN_ALIGNMENT` before any future production admission
- Admission status: not admitted because no real steward approval record exists

## Admission requirements now enforced

Before any future admitted relationship is written:
1. Decision must exist and not already be admitted.
2. Direct disambiguation decisions must be proposed first; direct apply is blocked.
3. Approval must include reviewer, role, rationale, mutation scope, rollback plan, validation snapshot, decision hash, and risk acknowledgment when high risk.
4. Admin/mutation gate must pass.
5. Endpoint nodes must exist.
6. Relation type must be valid and not `CROSS_DOMAIN_EQUIVALENT`.
7. Duplicate and self-loop checks must pass.
8. Transaction manifest must be written.
9. Rollback preview/apply path must exist.
10. Future graph cache invalidation is covered by including `admitted-relationships.json` in the AEC Explorer cache key.
