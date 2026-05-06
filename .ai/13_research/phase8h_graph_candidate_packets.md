# Phase 8H Graph Candidate Packets

**Date:** 2026-05-06

## Packet Summary

No new graph-edge admission packet is proposed in Phase 8H after the full accepted-link sweep.

The Phase 8H packet contains:

1. Visual-only verification candidates for already-admitted evidence-backed relationships and accepted Resource evidence.
2. Resource-layer-only candidates where graph mutation would duplicate existing semantics or overclaim source meaning.
3. Explicit blockers for every accepted Resource-backed link.

## Visual-Only Candidates

| Candidate ID | Evidence | Existing Graph Context | Proposed Action | Reason No Registry Mutation Is Needed |
|---|---|---|---|---|
| `phase8h-visual-wbdg-wind-load-path-existing-edge` | `res-wbdg-wind-safety-building-envelope`, `nrl-load-path-wbdg-wind`, `nrl-wind-load-wbdg-wind` | Phase 8G admitted `Structural Wind Load INFORMS Load Path` | Verify Explorer/NodeInspector exposes the existing edge and caveats. | The edge already exists; re-admission would duplicate. Existing tests cover Phase 8G selected-node visibility. |
| `phase8h-visual-buildingsmart-ifc-existing-edge` | `res_9c586758-66e4-46f2-b62a-8720db1c0976`, `nrl_521bc0e1-130d-4332-91b9-68ab8f83efc7` | Phase 8F admitted `BIM Schemas INFORMS IFC Exchange` | Verify Explorer/NodeInspector exposes the existing edge and caveats. | The edge already exists; re-admission would duplicate. Existing tests cover Phase 8F selected-node visibility. |
| `phase8h-visual-accessible-route-disambiguation` | `res-us-access-board-accessible-routes-ch4`, `nrl-accessible-route-usab-ch4` | `Barrier Free Routes broader_than Accessible Route Continuity` | Verify path/parent context and source caveat display in reviewer/learner-safe surfaces. | Duplicate accessible-route labels make graph mutation unsafe; no new visual code was identified as required after current Explorer tests. |

## Resource-Layer-Only Candidates

| Candidate ID | Evidence | Blocker |
|---|---|---|
| `phase8h-wbdg-fire-protection-resource-layer-only` | `res_115f8683-e9a2-4ce8-9575-d6b9b6c9ce40`, `nrl_68b933e6-36b9-4dbb-a628-8a5d923fc485` | Existing Fire Protection/Egress overlays already carry graph semantics; new edges risk code/compliance/AHJ overclaim. |
| `phase8h-uniclass-classification-resource-layer-only` | `res_4b0866ea-2ae0-4172-8f43-ea3d34ffd67c`, `nrl_d2eb1f9c-7502-40bf-a7d8-ae2c50bd2477` | Classification Systems already has `Uniclass Mapping` child; new edge risks adoption/current/universal-authority overclaim. |
| `phase8h-wbdg-seismic-resource-layer-only` | `res-wbdg-seismic-design-principles`, `nrl-seismic-load-wbdg-seismic` | No second endpoint is safely justified from metadata alone; seismic/code/numerical/design-adequacy claims are blocked. |
| `phase8h-ice-load-path-resource-layer-only` | `res-ice-structural-load-paths`, `nrl-load-path-ice` | Strong direct evidence for Load Path, but no second graph endpoint is supported without source-text interpretation; duplicate load-path review risk remains. |

## Rejected Edge Ideas

| Idea | Reason Rejected |
|---|---|
| Re-admit `BIM Schemas INFORMS IFC Exchange` | Already active from Phase 8F; re-admission would duplicate. |
| Re-admit `Structural Wind Load INFORMS Load Path` | Already active from Phase 8G; re-admission would duplicate. |
| `Fire Protection` to additional egress/sprinkler/standpipe/fire pump edges | Existing graph already has child concepts and Fire Protection/Egress overlays; WBDG metadata alone does not authorize code/compliance semantics. |
| `Classification Systems` to Uniclass/OmniClass/MasterFormat mapping edges | Existing hierarchy already models mappings; Uniclass metadata alone does not authorize adoption or authority semantics. |
| `Structural Seismic Load` to `Load Path` or `Diaphragm Action` | Existing graph already has `Structural Seismic Load REQUIRES Diaphragm Action`; WBDG metadata alone does not justify additional non-duplicative relation. |
| `Accessible Route Continuity` to compliance/accessibility/code nodes | Duplicate labels and compliance/govening applicability risk require a separate canonical/source-context review. |

## Non-Claims

This packet does not claim:

- source truth;
- current, governing, mandatory, AHJ, jurisdictional, or compliance status;
- standard edition/version/scope;
- numerical criteria;
- protected content access or ingestion;
- learner exposure changes;
- P0/P1 mutation.
