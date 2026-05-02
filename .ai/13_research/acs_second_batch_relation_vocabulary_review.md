# ACS Second Batch Relation Vocabulary Review

Date: 2026-05-02T09:55:00Z

## Result

Completed. The second batch used existing or explicitly governed non-equivalence relation types only.

## Accepted/admitted relation types

- `TRANSFERS_LOAD_TO` - admitted for load path mechanism edges; directional; non-numerical and non-code-specific.
- `DISCHARGES_TO` - admitted for roof drainage discharge interface to stormwater networks; directional; non-numerical.
- `COORDINATES_WITH` - admitted as reciprocal visible coordination pairs where the relation is symmetric in practice and the current overlay schema represents symmetry as two directed edges.

## Deferred relation types

- `INFORMS` - deferred. Kimi flagged it as too broad for Geotechnical Investigation Interface -> Foundation System without tighter semantics or source context.
- `CONSTRAINS` for Site Grading -> Accessible Routes - deferred due ambiguous physical-vs-regulatory semantics.
- `CROSS_DOMAIN_EQUIVALENT` - remains blocked for active admitted production edges.
- generic `related_to` - not used.

## Admitted edges

- `VTN-DOM-0012263--transfers_load_to--VTN-DOM-0012269` - `TRANSFERS_LOAD_TO` - `VTN-DOM-0012263` -> `VTN-DOM-0012269` - approval `canonical-approval-20260502094003-2fd59939b532`
- `VTN-DOM-0012269--transfers_load_to--VTN-DOM-0012273` - `TRANSFERS_LOAD_TO` - `VTN-DOM-0012269` -> `VTN-DOM-0012273` - approval `canonical-approval-20260502094003-2fd59939b532`
- `VTN-DOM-0012764--discharges_to--VTN-DOM-0002899` - `DISCHARGES_TO` - `VTN-DOM-0012764` -> `VTN-DOM-0002899` - approval `canonical-approval-20260502094003-2fd59939b532`
- `VTN-DOM-0012741--coordinates_with--VTN-DOM-0012266` - `COORDINATES_WITH` - `VTN-DOM-0012741` -> `VTN-DOM-0012266` - approval `canonical-approval-20260502094003-2fd59939b532`
- `VTN-DOM-0012266--coordinates_with--VTN-DOM-0012741` - `COORDINATES_WITH` - `VTN-DOM-0012266` -> `VTN-DOM-0012741` - approval `canonical-approval-20260502094003-2fd59939b532`
- `VTN-DOM-0012165--coordinates_with--VTN-DOM-0012261` - `COORDINATES_WITH` - `VTN-DOM-0012165` -> `VTN-DOM-0012261` - approval `canonical-approval-20260502094003-2fd59939b532`
- `VTN-DOM-0012261--coordinates_with--VTN-DOM-0012165` - `COORDINATES_WITH` - `VTN-DOM-0012261` -> `VTN-DOM-0012165` - approval `canonical-approval-20260502094003-2fd59939b532`

## Non-admitted candidates

- Existing-edge no-ops remained deferred/no-op when the base graph or admitted overlay already contained the relation.
- Retaining Wall and Shear Wall candidates remained high-risk gated.
