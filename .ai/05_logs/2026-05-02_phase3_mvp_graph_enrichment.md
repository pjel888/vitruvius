# Phase 3 MVP Graph Enrichment Admission Report

Date: 2026-05-02T10:24:13Z

## Summary

- Baseline admitted relationships: 14.
- Final admitted relationships: 26.
- New Phase 3 MVP admitted overlays: 12.
- Base graph edges: 13,670.
- Effective graph edges after overlays: 13,696.
- Approvals: 6.
- P1 packets reviewed/unreviewed: 20 / 0.
- P1 packet snapshots rebased: 20.
- Aliases / redirects / tombstones: 0 / 0 / 0.
- Resource Layer mutation: none.
- Merge: none.
- Fake source/standard/AHJ/numerical/protected-payload claim: none.

## Admitted edges

| Candidate | Edge ID | Source | Relation | Target | Review basis |
|---|---|---|---|---|---|
| phase3-acs-001 | `VTN-DOM-0012267--transfers_load_to--VTN-DOM-0012263` | `VTN-DOM-0012267` One Way Slab | `TRANSFERS_LOAD_TO` | `VTN-DOM-0012263` Beam | Kimi accepted structural load-path edge. |
| phase3-acs-002 | `VTN-DOM-0012268--transfers_load_to--VTN-DOM-0012263` | `VTN-DOM-0012268` Two Way Slab | `TRANSFERS_LOAD_TO` | `VTN-DOM-0012263` Beam | Kimi accepted structural load-path edge. |
| phase3-acs-003 | `VTN-DOM-0012268--transfers_load_to--VTN-DOM-0012269` | `VTN-DOM-0012268` Two Way Slab | `TRANSFERS_LOAD_TO` | `VTN-DOM-0012269` Column | Kimi accepted structural load-path edge. |
| phase3-acs-004 | `VTN-DOM-0012785--transfers_load_to--VTN-DOM-0012273` | `VTN-DOM-0012785` Grade Beam | `TRANSFERS_LOAD_TO` | `VTN-DOM-0012273` Foundation System | Kimi accepted structural load-path edge. |
| phase3-acs-005 | `VTN-DOM-0012293--constrains--VTN-DOM-0012786` | `VTN-DOM-0012293` Soil Bearing Capacity | `CONSTRAINS` | `VTN-DOM-0012786` Slab-On-Grade | Kimi accepted non-numerical geotechnical constraint. |
| phase3-acs-006 | `VTN-DOM-0002906--coordinates_with--VTN-DOM-0005262` | `VTN-DOM-0002906` Site Grading | `COORDINATES_WITH` | `VTN-DOM-0005262` Stormwater Flow Path | Kimi accepted reciprocal site/drainage coordination. |
| phase3-acs-007 | `VTN-DOM-0005262--coordinates_with--VTN-DOM-0002906` | `VTN-DOM-0005262` Stormwater Flow Path | `COORDINATES_WITH` | `VTN-DOM-0002906` Site Grading | Kimi accepted reciprocal site/drainage coordination. |
| phase3-acs-008 | `VTN-DOM-0012742--coordinates_with--VTN-DOM-0012764` | `VTN-DOM-0012742` Roof Drainage Interface | `COORDINATES_WITH` | `VTN-DOM-0012764` Roof Drainage Discharge Interface | Kimi accepted reciprocal roof drainage interface coordination. |
| phase3-acs-009 | `VTN-DOM-0012764--coordinates_with--VTN-DOM-0012742` | `VTN-DOM-0012764` Roof Drainage Discharge Interface | `COORDINATES_WITH` | `VTN-DOM-0012742` Roof Drainage Interface | Kimi accepted reciprocal roof drainage interface coordination. |
| phase3-acs-010 | `VTN-DOM-0012280--constrains--VTN-DOM-0012273` | `VTN-DOM-0012280` Foundation Settlement | `CONSTRAINS` | `VTN-DOM-0012273` Foundation System | Kimi accepted non-numerical settlement/foundation constraint. |
| phase3-acs-011 | `VTN-DOM-0012749--coordinates_with--VTN-DOM-0012740` | `VTN-DOM-0012749` Site Finished Floor Elevation Interface | `COORDINATES_WITH` | `VTN-DOM-0012740` Architectural Finished Floor Datum | Kimi timed out; admitted under timeout rule as plainly safe non-numerical interface coordination. |
| phase3-acs-012 | `VTN-DOM-0012740--coordinates_with--VTN-DOM-0012749` | `VTN-DOM-0012740` Architectural Finished Floor Datum | `COORDINATES_WITH` | `VTN-DOM-0012749` Site Finished Floor Elevation Interface | Kimi timed out; admitted under timeout rule as plainly safe reciprocal datum coordination. |

## Deferred or rejected

| Candidate | Relationship | Relation | Status |
|---|---|---|---|
| phase3-acs-defer-001 | VTN-DOM-0000317 Groundwater -> VTN-DOM-0000313 Excavation Support | `CONSTRAINS` | Deferred because Kimi requested source/reference support despite general plausibility. |
| phase3-acs-defer-002 | VTN-DOM-0012743 Facade Anchor Interface -> VTN-DOM-0012313 Facade Assembly | `COORDINATES_WITH` | Deferred because Kimi requested source/assembly context. |
| phase3-acs-defer-003 | VTN-DOM-0012210 Shaft Planning <-> VTN-DOM-0012790 Structural Core | `COORDINATES_WITH` | Deferred because Kimi requested source/directionality context. |
| phase3-acs-reject-001 | VTN-DOM-0012293 Soil Bearing Capacity -> VTN-DOM-0012273 Foundation System | `CONSTRAINS` | Rejected/no-op because the base graph already contains this edge. |

## Transaction and rollback

- Decision ID: `canonical-20260502102405-64a25eeccbb2`.
- Approval ID: `canonical-approval-20260502102405-baf8f5958e7d`.
- Decision manifest: `canonical-tx-20260502102405-0be77a0941bd`.
- Approval/admission manifest: `canonical-tx-20260502102405-9531f5e3690d`.
- P1 rebase manifest: `canonical-tx-20260502102405-c20aaacb8002`.
- Rollback plan: rollback by decision ID marks the admitted overlay edges and scoped approval as `rolled_back`; base graph, Resource Layer, aliases, redirects, and tombstones remain unchanged.

## Visibility validation

- Checked all 12 newly admitted edges through `GET /node/:id/neighborhood?depth=1&direction=both`.
- All expected target nodes, edge IDs, and relation types were returned.
- Dynamic graph edge filters include `TRANSFERS_LOAD_TO`, `CONSTRAINS`, and `COORDINATES_WITH`.
- `CROSS_DOMAIN_EQUIVALENT` remains absent from active graph filters.

## Validation status

- Targeted `validateGraphRelationships`, `validateCanonicalGraphStewardship`, and `validateResourceLayer` passed after admission.
- Broad API/Explorer/build/Python validation still required before commit.
