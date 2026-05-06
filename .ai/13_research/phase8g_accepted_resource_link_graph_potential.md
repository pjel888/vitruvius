# Phase 8G Accepted Resource Link Graph Potential

**Date:** 2026-05-06

## Scope

Phase 8G inspected all 8 accepted `nodeResourceLinks` for graph/node improvement potential. This inspection used existing Resource Layer metadata and graph neighborhoods only. No external source verification, protected content download, Resource Layer write, graph/canonical write, or learner exposure occurred in this stage.

## Accepted Link Inventory

| Link | Resource | Target node | Relationship | Graph potential | Decision |
|---|---|---|---|---|---|
| `nrl-accessible-route-usab-ch4` | `res-us-access-board-accessible-routes-ch4` / Guide to ADA Accessibility Standards Chapter 4 | `VTN-DOM-0004630` / Accessible Route Continuity | `provides_design_guidance` | The graph already represents the target as a child of Barrier Free Routes. A new edge would risk duplicating hierarchy or implying regulatory applicability. | Resource Layer evidence only. |
| `nrl-load-path-wbdg-wind` | `res-wbdg-wind-safety-building-envelope` / Wind Safety of the Building Envelope | `VTN-DOM-0012160` / Load Path | `provides_design_guidance` | Shares one accepted WBDG wind resource with Structural Wind Load. This can support a narrow contextual `INFORMS` proposal if caveated as design-guidance metadata only. | Candidate packet. |
| `nrl-wind-load-wbdg-wind` | `res-wbdg-wind-safety-building-envelope` / Wind Safety of the Building Envelope | `VTN-DOM-0012777` / Structural Wind Load | `provides_design_guidance` | Same accepted resource also targets Load Path. Candidate is directional from Structural Wind Load to Load Path, not code/compliance/current/AHJ/source-truth. | Candidate packet. |
| `nrl-seismic-load-wbdg-seismic` | `res-wbdg-seismic-design-principles` / Seismic Design Principles | `VTN-DOM-0012778` / Structural Seismic Load | `explains` | Existing graph already has `Structural Seismic Load REQUIRES Diaphragm Action`; a new edge would either duplicate semantics or overclaim. | Resource Layer evidence only. |
| `nrl-load-path-ice` | `res-ice-structural-load-paths` / Structural Load Paths | `VTN-DOM-0012160` / Load Path | `explains` | Strong evidence for the Load Path node but no new existing-node endpoint is justified without content overreach. | Resource Layer evidence only. |
| `nrl_521bc0e1-130d-4332-91b9-68ab8f83efc7` | `res_9c586758-66e4-46f2-b62a-8720db1c0976` / Industry Foundation Classes | `VTN-DOM-0000092` / BIM Schemas | `explains` | Phase 8F already admitted `BIM Schemas INFORMS IFC Exchange`; no additional edge is justified. | Already handled in Phase 8F. |
| `nrl_68b933e6-36b9-4dbb-a628-8a5d923fc485` | `res_115f8683-e9a2-4ce8-9575-d6b9b6c9ce40` / WBDG Fire Protection | `VTN-DOM-0000056` / Fire Protection | `explains` | Existing overlay already includes Fire Protection/Egress relationships. Additional graph growth risks code/compliance overclaim. | Resource Layer evidence only. |
| `nrl_d2eb1f9c-7502-40bf-a7d8-ae2c50bd2477` | `res_4b0866ea-2ae0-4172-8f43-ea3d34ffd67c` / Uniclass | `VTN-DOM-0000093` / Classification Systems | `explains` | Existing hierarchy already has Classification Systems child mapping nodes. Extra relations risk jurisdiction/adoption or authority overclaim. | Resource Layer evidence only. |

## Target Neighborhood Notes

### `Structural Wind Load`

- Node: `VTN-DOM-0012777`
- Existing accepted Resource evidence: `nrl-wind-load-wbdg-wind`
- Existing graph context includes `Structural Wind Load CONSTRAINS Facade Anchor Interface`, `Structural Wind Load REQUIRES Diaphragm Action`, and one admitted overlay `Structural Wind Load CONSTRAINS Facade Assembly`.
- No `Structural Wind Load INFORMS Load Path` edge currently exists.

### `Load Path`

- Node: `VTN-DOM-0012160`
- Existing accepted Resource evidence: `nrl-load-path-wbdg-wind`, `nrl-load-path-ice`
- Existing graph context includes parent/child structural-system context and component relationships.
- There is an existing incoming P0-sensitive edge from Reinforced Concrete. Phase 8G does not mutate, rely on, merge, alias, redirect, tombstone, or canonicalize that P0 node.

## Candidate Selected For Review

`Structural Wind Load INFORMS Load Path`

Rationale: one accepted WBDG wind-safety Resource has accepted links to both endpoints, and the proposed relation is a weak contextual `INFORMS` relation. It does not claim code status, currentness, jurisdictional applicability, AHJ adoption, numerical criteria, source truth, or design adequacy.

## Deferred / Blocked Items

- Accessible Route Continuity: no new non-hierarchical edge is justified without regulatory applicability overclaim.
- Structural Seismic Load: current graph semantics already cover primary seismic relationship context.
- ICE Structural Load Paths: useful as node evidence, but no new endpoint is justified.
- BIM Schemas: Phase 8F already admitted the one safe edge.
- Fire Protection: keep as Resource Layer evidence; avoid code/compliance authority implication.
- Classification Systems: keep as Resource Layer evidence; avoid adoption or external-classification authority implication.
