# Phase 8F Graph Improvement Apply Report

**Date:** 2026-05-06

## Applied Improvement

One Kimi-reviewed, evidence-backed, non-destructive graph overlay edge was admitted:

| Field | Value |
|---|---|
| Edge ID | `VTN-DOM-0000092--informs--VTN-DOM-0000646` |
| Source node | `VTN-DOM-0000092` / `BIM Schemas` |
| Relation | `INFORMS` |
| Target node | `VTN-DOM-0000646` / `IFC Exchange` |
| Supporting Resource | `res_9c586758-66e4-46f2-b62a-8720db1c0976` |
| Supporting nodeResourceLink | `nrl_521bc0e1-130d-4332-91b9-68ab8f83efc7` |
| Active decision | `canonical-20260506122951-e122a4a40ecf` |
| Active approval | `canonical-approval-20260506122951-4c36fe69da29` |

## Preview / Apply Path

The edge was admitted through the existing canonical relationship admission workflow:

1. `previewCanonicalRelationshipAdmissionDecision`
2. `recordCanonicalRelationshipAdmissionDecision`
3. `previewCanonicalApproval`
4. `approveCanonicalDecision`

Preview result:

- Decision blockers: 0
- Decision warnings: 0
- Approval blockers: 0
- Approval warnings: 0
- Rollback capability: full
- Mutation scope: `non_destructive_edge_admission`

## Transaction Manifests

Initial wording-only admission:

- Decision manifest: `canonical-tx-20260506122700-6c083b3a4905`
- Approval manifest: `canonical-tx-20260506122700-75f81c552b0a`

Safety hygiene rollback:

- Rollback manifest: `canonical-tx-20260506122915-7732219460b9`
- Reason: API-visible provenance included the guarded phrase `protected content`; the edge was re-admitted with `protected payload not stored` wording.

Active sanitized admission:

- Decision manifest: `canonical-tx-20260506122951-fe07363f3179`
- Approval manifest: `canonical-tx-20260506122951-e5f84387d87f`

## Safety Result

- Resource Layer mutation: none
- Node creation: none
- Node endpoint mutation: none
- Alias/redirect/tombstone mutation: none
- P0 Concrete/Reinforced Concrete mutation: none
- High-risk P1 packet mutation: none
- `CROSS_DOMAIN_EQUIVALENT`: not admitted
- Generic `related_to`: not admitted
- Protected payload stored: no
- Source truth/current/governing/compliance/AHJ claim: no
- Learner exposure change: no Resource/candidate/link visibility change

## Deferred Items

WBDG Fire Protection and Uniclass remain Resource Layer evidence only in Phase 8F:

- WBDG public metadata does not justify a new specific non-hierarchical fire-protection graph relation.
- Uniclass would duplicate the existing `Classification Systems broader_than Uniclass Mapping` hierarchy or overclaim authority/adoption.
