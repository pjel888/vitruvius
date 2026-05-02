# Phase 3 Next Graph Enrichment Queue

Date: 2026-05-02T10:24:13Z

## Ready for future safe non-destructive review

1. Additional foundation/geotechnical constraints where duplicate-free and Kimi/source-safe.
2. Additional site/drainage interface `COORDINATES_WITH` pairs that avoid numeric hydrology/capacity claims.
3. Additional structural load-path edges using `TRANSFERS_LOAD_TO` where endpoint semantics are direct and existing-node based.

## Needs Kimi/source-context review

- Groundwater -> Excavation Support (`CONSTRAINS`) after Kimi requested source/reference context.
- Facade Anchor Interface -> Facade Assembly (`COORDINATES_WITH`) after Kimi requested assembly/source context.
- Shaft Planning <-> Structural Core (`COORDINATES_WITH`) after Kimi requested source/directionality context.

## Duplicate base edge / no-op

- Soil Bearing Capacity -> Foundation System (`CONSTRAINS`) already exists in the base graph.

## High-risk blocked

- Shear Wall remains high-risk blocked.
- Retaining Wall remains high-risk blocked.
- Mat Foundation, Wall Finishes, and Load Path remain source/edge-neighborhood gated.
