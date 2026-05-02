# Phase 4 Next Graph Enrichment Queue

Date: 2026-05-02T14:21:57Z

## Ready for safe non-destructive admission review

- Consider a bounded Wave 3 only after relation-vocabulary review. Current safe admitted vocabulary remains useful but `COORDINATES_WITH` and `TRANSFERS_LOAD_TO` are becoming dominant.

## Needs relation-vocabulary update

Read-only candidate generation identified useful future relations that are not currently admitted vocabulary: `INFORMS`, `AFFECTS`, `SUPPORTS`, `RESISTS`, `DRAINS_TO`, `COLLECTS`, `CONVEYS`, `MITIGATES`, and `CONNECTS_TO`. Do not admit these until `CanonicalStewardshipRelationType`, admitted relationship validation, Explorer filters, and tests are updated.

## Needs Kimi/source review before future admission

- Lateral Stability System `RESISTS` Structural Wind Load / Structural Seismic Load.
- Diaphragm Opening Coordination `AFFECTS` Diaphragm Action.
- Soil Infiltration Rate `INFORMS` Bioretention Cell / Permeable Pavement.
- Hydrologic Design Basis `INFORMS` Storm Sewer Pipe / Surface Runoff.
- Curb Ramp Geometry Interface `CONNECTS_TO` Accessible Public-Way Crossing Tie-In.

## High-risk blocked

- Shear Wall remains high-risk blocked after Wave 2 inspection.
- Retaining Wall remains high-risk blocked from Wave 1.
- Mat Foundation, Wall Finishes, and Load Path remain high-risk/source/edge-neighborhood gated.

## Duplicate base edge / no-op

- Soil Bearing Capacity -> Foundation System remains no-op due existing graph context.
- Redundant footing subtype edges to Soils were deferred after Kimi review.

## Rejected

- Directionally inverted stormwater flow path -> surface runoff edge.
- Near-duplicate Erosion And Sediment Control <-> Civil Erosion And Sediment Control edge.
- Overclaim-prone exterior route `REQUIRES` public-way crossing tie-in.
