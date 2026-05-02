# ACS Second Batch Admission Report

Date: 2026-05-02T09:55:00Z

## Baseline

- Baseline nodes: 10,018
- Baseline base edges: 13,670
- Baseline effective edges before second batch: 13,677
- Baseline admitted relationship overlays before second batch: 7

## Admission result

- Second-batch ACS edges admitted: 7
- Effective edges after second batch: 13,684
- Base graph edges after second batch: 13,670
- Approval count after second batch: 5
- Admitted relationship overlays after second batch: 14
- Scoped decision: `canonical-20260502094003-61c2eec9c83a`
- Scoped approval: `canonical-approval-20260502094003-2fd59939b532`
- Approval/admission manifest: `canonical-tx-20260502094003-9f1441ef1e5b`
- P1 custody rebase manifest after graph/canonical state change: `canonical-tx-20260502094802-f4fdf2cf8f1f`

## Admitted edges

- `VTN-DOM-0012263--transfers_load_to--VTN-DOM-0012269` - `TRANSFERS_LOAD_TO` - `VTN-DOM-0012263` -> `VTN-DOM-0012269` - approval `canonical-approval-20260502094003-2fd59939b532`
- `VTN-DOM-0012269--transfers_load_to--VTN-DOM-0012273` - `TRANSFERS_LOAD_TO` - `VTN-DOM-0012269` -> `VTN-DOM-0012273` - approval `canonical-approval-20260502094003-2fd59939b532`
- `VTN-DOM-0012764--discharges_to--VTN-DOM-0002899` - `DISCHARGES_TO` - `VTN-DOM-0012764` -> `VTN-DOM-0002899` - approval `canonical-approval-20260502094003-2fd59939b532`
- `VTN-DOM-0012741--coordinates_with--VTN-DOM-0012266` - `COORDINATES_WITH` - `VTN-DOM-0012741` -> `VTN-DOM-0012266` - approval `canonical-approval-20260502094003-2fd59939b532`
- `VTN-DOM-0012266--coordinates_with--VTN-DOM-0012741` - `COORDINATES_WITH` - `VTN-DOM-0012266` -> `VTN-DOM-0012741` - approval `canonical-approval-20260502094003-2fd59939b532`
- `VTN-DOM-0012165--coordinates_with--VTN-DOM-0012261` - `COORDINATES_WITH` - `VTN-DOM-0012165` -> `VTN-DOM-0012261` - approval `canonical-approval-20260502094003-2fd59939b532`
- `VTN-DOM-0012261--coordinates_with--VTN-DOM-0012165` - `COORDINATES_WITH` - `VTN-DOM-0012261` -> `VTN-DOM-0012165` - approval `canonical-approval-20260502094003-2fd59939b532`

## Rationale

The admitted edges improve learner-facing ACS reasoning paths for structural load transfer, roof drainage discharge, and architecture/structure coordination. They are non-destructive overlay admissions over existing nodes. They do not assert numerical criteria, code compliance, AHJ adoption, or source-specific standard truth.

## Deferred/rejected

- `INFORMS` candidate deferred pending narrower relation vocabulary/source-context review.
- ambiguous Site Grading/Accessible Routes candidate deferred.
- high-risk Retaining Wall and Shear Wall candidates remain blocked.

## Safety confirmations

- No base graph mutation.
- No node addition/deletion/rename.
- No merge, alias, redirect, or tombstone.
- No Resource Layer mutation.
- No fake source URL, standard edition, AHJ claim, numerical criterion, or protected payload.
- Selected-node visibility is covered by API regression tests and direct validation.
