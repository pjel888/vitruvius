# Phase 4 Next Graph Enrichment Queue

Date: 2026-05-02T11:25:29Z

## Ready for safe non-destructive admission review

- p4w1-039: `VTN-DOM-0012792` Anchor Bolt Group `COORDINATES_WITH` `VTN-DOM-0012782` Footing Foundation. Kimi accepted; deferred only to keep Wave 1 bounded. Requires normal duplicate check, dry-run, scoped approval, rollback preview, and visibility validation.
- p4w1-040: `VTN-DOM-0012782` Footing Foundation `COORDINATES_WITH` `VTN-DOM-0012792` Anchor Bolt Group. Kimi accepted reciprocal; deferred only to keep Wave 1 bounded.

## Needs Kimi review

- Additional low-risk coordination edges around structural connection detailing and site access can be generated from existing nodes only.

## Needs relation-vocabulary update

- Diaphragm openings and seismic load effects may need `AFFECTS` or `INFORMS`; do not force with `CONSTRAINS`.
- Soil infiltration to bioretention may need `AFFECTS`/`INFORMS`; do not force with `CONSTRAINS`.

## Needs source/context review

- Groundwater -> Excavation Support.
- Facade Anchor Interface -> Facade Assembly.
- Shaft Planning <-> Structural Core.
- Flood/FFE and topography/FFE candidates.

## High-risk blocked

- Retaining Wall: remains high-risk blocked; CHED curriculum metadata scope requires source/scope clarification.
- Shear Wall, Mat Foundation, Wall Finishes, Load Path: remain high-risk/source/edge-neighborhood gated.

## Duplicate base edge / no-op

- Soil Bearing Capacity -> Foundation System remains no-op due existing base relationship.

## Rejected

- Abstract/generic coordination candidates p4w1-026, p4w1-027, p4w1-036.
- Regulatory/context-sensitive flood/FFE candidates p4w1-030/031 for this wave.
