# Phase 8G Explorer Visual Verification Report

**Date:** 2026-05-06

## Verified Surfaces

The Phase 8G edge was checked through the API surfaces used by Explorer and NodeInspector.

| Check | Result |
|---|---|
| `GET /node/VTN-DOM-0012777/neighborhood?depth=1&direction=both` | PASS |
| Neighborhood includes `Load Path` node | PASS |
| Neighborhood includes `VTN-DOM-0012777--informs--VTN-DOM-0012160` as `INFORMS` | PASS |
| Relationship details include the Phase 8G edge | PASS |
| `GET /perspective/aec-mepfs/nodes?profile=render` | PASS |
| Render graph edge count | `13936` |
| Render graph includes Phase 8G edge | PASS |
| Render graph preserves Phase 8F BIM edge | PASS |
| Render graph includes `CROSS_DOMAIN_EQUIVALENT` | PASS - absent |

## Regression Coverage

Added API regression test:

- `serves Phase 8G resource-backed wind-load/load-path relationship through selected-node neighborhoods and graph filters`

Preserved:

- Sendai Mediatheque / Toyo Ito `HAS_FACET`
- Phase 8F `BIM Schemas INFORMS IFC Exchange`
- Dynamic edge filters based on real graph edge types
- `CROSS_DOMAIN_EQUIVALENT` absence

## Learner Visibility

Phase 8G did not change Resource Layer visibility:

- Resources remain 10.
- nodeResourceLinks remain 12.
- Accepted Resource Layer links remain 8.
- External metadata candidates remain 15.
- No candidate exposure or reviewer-only Resource exposure changed.
