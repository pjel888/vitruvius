# Phase 8F Relation Vocabulary Gate Report

**Date:** 2026-05-06

## Proposed Candidate

`VTN-DOM-0000092` / `BIM Schemas` -> `VTN-DOM-0000646` / `IFC Exchange`

Proposed relation: `INFORMS`

## Gate Result

| Gate | Result |
|---|---|
| Relation type exists in canonical stewardship vocabulary | PASS |
| Relation type is admissible | PASS |
| Not `CROSS_DOMAIN_EQUIVALENT` | PASS |
| Not generic `related_to` | PASS |
| Source node exists | PASS |
| Target node exists | PASS |
| No self-loop | PASS |
| No duplicate exact base tuple | PASS |
| No duplicate exact admitted tuple | PASS |
| No duplicate proposed tuple | PASS |
| Directionality justified | PASS |
| No Resource Layer mutation required | PASS |
| No node merge/alias/redirect/tombstone | PASS |
| No P0/high-risk P1 touch | PASS |

## Dry-Run Output Summary

`previewCanonicalRelationshipAdmissionDecision` returned:

- `blockers: []`
- `warnings: []`
- `rollbackCapability: full`
- `graphNodeMutation: false`
- `edgeEndpointMutation: false`
- `resourceLayerMutation: false`
- `aliasRedirectTombstoneMutation: false`

## Deferred Proposals

No graph relation is proposed for WBDG Fire Protection or Uniclass in this packet because the relation vocabulary gate would be semantically weak:

- Fire Protection public metadata does not support a specific new non-hierarchical relationship without overclaim.
- Classification Systems already has a base hierarchy edge to Uniclass Mapping.
