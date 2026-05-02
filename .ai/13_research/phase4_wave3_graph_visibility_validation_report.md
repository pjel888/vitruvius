# Phase 4 Wave 3 Graph Visibility Validation Report

Date: 2026-05-03T01:00:00Z

## Method

Visibility was validated through:
1. Existing API regression tests that verify selected-node neighborhoods
2. Canonical stewardship validation that verifies admitted edges are reachable
3. Explorer UI code review confirming dynamic filter reconciliation
4. Manual verification of Explorer color/filter mappings for new relation families

## New Relation Family Visibility

| Relation Family | Sample Edge | Verified In API Tests | Explorer Color | Explorer Filter |
|-----------------|-------------|----------------------|----------------|-----------------|
| INFORMS | VTN-DOM-0012769 → VTN-DOM-0012273 | Yes (canonical stewardship regressions) | #06b6d4 | Yes |
| AFFECTS | VTN-DOM-0012280 → VTN-DOM-0012273 | Yes (canonical stewardship regressions) | #06b6d4* | Yes |
| SUPPORTS | VTN-DOM-0012273 → VTN-DOM-0012269 | Yes (canonical stewardship regressions) | #84cc16 | Yes |
| RESISTS | VTN-DOM-0012282 → VTN-DOM-0000259 | Yes (canonical stewardship regressions) | #d946ef | Yes |
| COLLECTS | VTN-DOM-0012759 → VTN-DOM-0012758 | Yes (canonical stewardship regressions) | #f59e0b | Yes |
| CONVEYS | VTN-DOM-0012760 → VTN-DOM-0005262 | Yes (canonical stewardship regressions) | #3b82f6 | Yes |
| MITIGATES | VTN-DOM-0000224 → VTN-DOM-0012758 | Yes (canonical stewardship regressions) | #10b981 | Yes |
| DRAINS_TO | VTN-DOM-0012759 → VTN-DOM-0012760 | Yes (canonical stewardship regressions) | #6366f1 | Yes |
| COORDINATES_WITH | VTN-DOM-0000233 → VTN-DOM-0012749 | Yes (canonical stewardship regressions) | #0ea5e9 | Yes |
| TRANSFERS_LOAD_TO | VTN-DOM-0012311 → VTN-DOM-0012263 | Yes (canonical stewardship regressions) | #f43f5e | Yes |
| CONSTRAINS | VTN-DOM-0003029 → VTN-DOM-0002906 | Yes (canonical stewardship regressions) | existing | Yes |

*AFFECTS shares the INFORMS color mapping in the current Explorer UI (both use #06b6d4). This is acceptable for visibility but may be refined in a future UI pass.

## Regression Verification

| Legacy Overlay | Status |
|----------------|--------|
| Deep Foundations CROSS_DOMAIN_ALIGNMENT | Visible — confirmed by API regression tests |
| Shallow Foundations CROSS_DOMAIN_ALIGNMENT | Visible — confirmed by API regression tests |
| Phase 3 MVP CONSTRAINS overlays | Visible — confirmed by API regression tests |
| Wave 1 TRANSFERS_LOAD_TO / DISCHARGES_TO / COORDINATES_WITH | Visible — confirmed by API regression tests |
| Wave 2 TRANSFERS_LOAD_TO / DISCHARGES_TO / COORDINATES_WITH | Visible — confirmed by API regression tests |
| Sendai Mediatheque / Toyo Ito HAS_FACET | Visible — confirmed by API regression tests |
| CROSS_DOMAIN_EQUIVALENT active edge | **Absent** — validator confirms no active admitted edge of this type |

## Dynamic Filter Reconciliation

The Explorer UI uses `reconcileFiltersForGraph` (in `App.tsx`) to dynamically absorb new edge types from the graph payload. This means:
- New Wave 3 relation types automatically appear in the edge filter panel
- No manual filter list update is required per admission wave
- Explicit `EDGE_TYPES` entries in `ExplorerRail.tsx` provide human-readable labels

## Node Inspector Display

`NodeInspector.tsx` maps edge types to colors via `EDGE_COLORS`. All new Wave 3 types have explicit color mappings, ensuring the relationship list displays correctly for selected nodes.

## Hidden Edge Types

`useSceneStore.ts` initializes `hiddenEdgeTypes` with all known types including the new Wave 3 types. This ensures toggle behavior is consistent.

## Conclusion

- [x] At least one Wave 3 edge per new relation family is visible through selected-node neighborhood
- [x] Dynamic filters include all new relation types
- [x] Node Inspector can display all new types
- [x] All regression overlays remain visible
- [x] CROSS_DOMAIN_EQUIVALENT remains absent from active admitted edges
- [x] No hidden relationship count anomalies detected
