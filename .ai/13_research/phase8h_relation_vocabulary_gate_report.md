# Phase 8H Relation Vocabulary Gate Report

**Date:** 2026-05-06

## Gate Result

`NO_NEW_RELATION_PASSES`

No Phase 8H candidate relation advances to dry-run/admission.

## Vocabulary Checks

| Check | Result |
|---|---|
| Source and target nodes exist for inspected accepted links | PASS |
| `CROSS_DOMAIN_EQUIVALENT` proposed | PASS - no |
| generic `related_to` proposed | PASS - no |
| Duplicate exact admitted edge avoided | PASS |
| Duplicate exact base edge avoided | PASS |
| Self-loop avoided | PASS |
| Broad endpoint pair avoided | PASS |
| Directionality justified for proposed graph edges | BLOCKED - no new relation has enough non-duplicative support |
| P0 endpoint mutation avoided | PASS |

## Duplicate / Existing Semantics

| Candidate Tuple | Status | Reason |
|---|---|---|
| `VTN-DOM-0000092` / BIM Schemas `INFORMS` `VTN-DOM-0000646` / IFC Exchange | already admitted | Phase 8F active admitted edge exists. |
| `VTN-DOM-0012777` / Structural Wind Load `INFORMS` `VTN-DOM-0012160` / Load Path | already admitted | Phase 8G active admitted edge exists. |
| Fire Protection to Egress semantics | already covered | Active overlays include `Fire Protection CONSTRAINS Egress` and `Egress REQUIRES Fire Protection`. |
| Classification Systems to Uniclass semantics | already covered by hierarchy | Base graph includes `Classification Systems broader_than Uniclass Mapping`. |
| Structural Seismic Load to Diaphragm Action | already covered by base graph | Base graph includes `Structural Seismic Load requires Diaphragm Action`. |

## Relation Families Rejected for Phase 8H

| Relation Family | Reason |
|---|---|
| `CONSTRAINS` | Would overclaim code/design constraint from public metadata-only evidence. |
| `REQUIRES` | Would imply mandatory relationship without source-context support. |
| `MAPS_TO_EXTERNAL_STANDARD` | Not supported for these Phase 8H evidence items without standards/context/adoption review. |
| `CROSS_DOMAIN_ALIGNMENT` | Not needed; candidates are not non-identity discipline-scoped duplicate alignments. |
| `SUPPORTS`, `CONNECTS_TO`, `COORDINATES_WITH`, `HAS_FACET` | No precise non-duplicative endpoint pair passed source/context and directionality checks. |

## Dry-Run Status

No graph admission dry-run was executed because no new relation passed the source/context and vocabulary gates. This avoids creating a transaction manifest for a known-empty graph mutation.
