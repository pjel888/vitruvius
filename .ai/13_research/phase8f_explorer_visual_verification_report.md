# Phase 8F Explorer Visual Verification Report

**Date:** 2026-05-06

## Applied Edge

`BIM Schemas` (`VTN-DOM-0000092`) now has an active admitted overlay edge:

`VTN-DOM-0000092--informs--VTN-DOM-0000646`

Target: `IFC Exchange` (`VTN-DOM-0000646`)

## API / Explorer Verification

Focused API regression added:

- `api/canonicalGraphStewardship.test.ts`
- Test: `serves Phase 8F resource-backed BIM schema relationship through selected-node neighborhoods and graph filters`

Verified behavior:

- `/node/VTN-DOM-0000092/neighborhood?depth=1&direction=both` includes `IFC Exchange`.
- The selected-node neighborhood includes the `INFORMS` edge.
- The normalized relationship record exposes `relationType: INFORMS`.
- `/perspective/aec-mepfs/nodes` includes the new edge.
- `CROSS_DOMAIN_EQUIVALENT` remains absent.

## Regression Preservation

Focused graph/Explorer API tests confirm:

- Sendai Mediatheque / Toyo Ito `HAS_FACET` remains visible.
- Foundation `CROSS_DOMAIN_ALIGNMENT` relationships remain visible and reciprocal.
- Existing ACS mechanism overlays remain visible through selected-node neighborhoods.
- Dynamic graph filter surfaces include active relation types.
- Full graph render count updated from 13,934 to 13,935 effective edges.
- Full graph API still does not expose the guarded phrase `protected content`.

## Learner Visibility

No Resource Layer learner visibility changed in Phase 8F:

- Resources remain 10.
- nodeResourceLinks remain 12.
- Accepted links remain 8.
- External metadata candidates remain 15.
- The new graph edge is a graph overlay between already admitted graph nodes; it does not create or expose a Resource, candidate, or learner-trusted evidence payload.
