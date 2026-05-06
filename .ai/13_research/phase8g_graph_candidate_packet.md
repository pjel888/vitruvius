# Phase 8G Graph Candidate Packet

**Date:** 2026-05-06

## Candidate

| Field | Value |
|---|---|
| Candidate ID | `phase8g-wbdg-wind-load-path-resource-backed` |
| Proposed edge | `Structural Wind Load INFORMS Load Path` |
| Source node | `VTN-DOM-0012777` / `Structural Wind Load` |
| Relation | `INFORMS` |
| Target node | `VTN-DOM-0012160` / `Load Path` |
| Supporting Resource | `res-wbdg-wind-safety-building-envelope` |
| Supporting Resource title | `Wind Safety of the Building Envelope` |
| Supporting links | `nrl-wind-load-wbdg-wind`, `nrl-load-path-wbdg-wind` |
| Candidate type | Non-destructive graph relationship overlay between existing nodes |
| Proposed weight | `0.42` |
| Proposed risk | `low` |

## Proposed Rationale

`Structural Wind Load` informs `Load Path` because one accepted WBDG wind-safety Resource has accepted `nodeResourceLinks` to both nodes. The Resource Layer evidence supports only contextual design-guidance metadata around wind effects and load-path continuity. It does not support code, numerical, project-specific, current/governing, compliance, AHJ, jurisdiction, source-truth, or design-adequacy claims.

## Proposed Provenance

Resource-backed Phase 8G proposal using accepted nodeResourceLinks `nrl-wind-load-wbdg-wind` and `nrl-load-path-wbdg-wind` plus Resource `res-wbdg-wind-safety-building-envelope`; metadata/rationale only, protected payload not stored.

## Dry Run

Command shape:

```powershell
@' <bounded Bun dry-run script> '@ | bun -
```

Dry-run result:

- Decision blockers: 0
- Decision warnings: 0
- Proposed relationship count: 1
- Affected graph edges: 16
- Affected Resource Layer links: `nrl-load-path-wbdg-wind`, `nrl-wind-load-wbdg-wind`, `nrl-load-path-ice`, `nrl-wind-load-asce-7-needs-review`
- Graph node mutation: false
- Resource Layer mutation: false
- Rollback capability: full

## Non-Claims

This packet does not claim:

- WBDG is a code, standard, AHJ, or governing source.
- The relationship is mandatory, complete, current, jurisdiction-specific, or compliant.
- The WBDG page proves design adequacy or numerical wind/load-path criteria.
- Protected content was downloaded or stored.
- P0 Concrete/Reinforced Concrete was changed.
- Learner-facing Resource visibility changed.

## Deferred Candidates

The remaining accepted Resource links stay Resource Layer evidence only for this batch. They either duplicate existing graph semantics, require protected/source-text interpretation, or risk overclaiming authority/adoption/compliance.
