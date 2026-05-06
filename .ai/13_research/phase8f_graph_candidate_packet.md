# Phase 8F Graph / Node Improvement Candidate Packet

**Date:** 2026-05-06

## Candidate Packet Result

One graph relationship candidate is proposed for delegated review and dry-run approval.

No Resource Layer mutation, Resource creation, nodeResourceLink creation, learner exposure, node merge, alias, redirect, tombstone, P0/P1 mutation, protected payload storage, or source-truth claim is proposed.

## Proposed Graph Relationship Candidate

| Field | Value |
|---|---|
| Candidate ID | `phase8f-bim-schemas-ifc-exchange-resource-backed` |
| Source node | `VTN-DOM-0000092` / `BIM Schemas` |
| Target node | `VTN-DOM-0000646` / `IFC Exchange` |
| Relation | `INFORMS` |
| Direction | outgoing |
| Weight | 0.42 |
| Supporting Resource | `res_9c586758-66e4-46f2-b62a-8720db1c0976` |
| Supporting nodeResourceLink | `nrl_521bc0e1-130d-4332-91b9-68ab8f83efc7` |
| Supporting source family | `buildingsmart` |
| Supporting URL | `https://www.buildingsmart.org/standards/bsi-standards/industry-foundation-classes/` |

Rationale:

`BIM Schemas` informs `IFC Exchange` because the accepted buildingSMART IFC Resource Layer link connects official IFC public metadata to BIM Schemas and the existing IFC Exchange node represents IFC model exchange context.

Caveats:

- Public metadata only.
- Protected specification content was not stored.
- No schema completeness claim.
- No edition/version/current/governing claim.
- No compliance, AHJ, jurisdiction, or source-truth claim.
- No learner exposure change.

## Resource-Layer-Only Boundaries

### WBDG Fire Protection

Kept as Resource Layer evidence only for this packet.

Reason:

- The accepted WBDG link supports evidence visibility for the `Fire Protection` node.
- The current public metadata does not justify a new non-hierarchical graph relationship without content-level, code, compliance, or fire-authority claims.

### Uniclass

Kept as Resource Layer evidence only for this packet.

Reason:

- The graph already contains `Classification Systems broader_than Uniclass Mapping`.
- A new edge would duplicate existing taxonomy or overclaim jurisdictional/adoption authority.

## Dry-Run Preview

The proposed BIM Schemas -> IFC Exchange edge was previewed with `previewCanonicalRelationshipAdmissionDecision`.

Result:

- Blockers: 0
- Warnings: 0
- Graph node mutation: false
- Edge endpoint mutation: false
- Resource Layer mutation: false
- Alias/redirect/tombstone mutation: false
- Rollback capability: full
- Affected Resource Layer link: `nrl_521bc0e1-130d-4332-91b9-68ab8f83efc7`

Preview edge:

```json
{
  "sourceNodeId": "VTN-DOM-0000092",
  "targetNodeId": "VTN-DOM-0000646",
  "relationType": "INFORMS",
  "rationale": "BIM Schemas informs IFC Exchange because the accepted buildingSMART IFC resource links official IFC public metadata to BIM Schemas and the existing IFC Exchange node represents IFC model exchange context; caveated as metadata-only with no schema completeness, edition/version, current/governing, compliance, AHJ, or source-truth claim."
}
```
