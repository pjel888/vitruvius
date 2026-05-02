# Phase 3 MVP Graph Enrichment Candidates

Date: 2026-05-02T10:24:13Z

This candidate queue was generated from existing nodes only. Candidate records are not source truth and do not imply admission until scoped approval, dry-run, transaction manifest, rollback, and visibility validation pass.

| Candidate | Source | Proposed relation | Target | Gate result |
|---|---|---|---|---|
| phase3-acs-001 | `VTN-DOM-0012267` One Way Slab | `TRANSFERS_LOAD_TO` | `VTN-DOM-0012263` Beam | admitted |
| phase3-acs-002 | `VTN-DOM-0012268` Two Way Slab | `TRANSFERS_LOAD_TO` | `VTN-DOM-0012263` Beam | admitted |
| phase3-acs-003 | `VTN-DOM-0012268` Two Way Slab | `TRANSFERS_LOAD_TO` | `VTN-DOM-0012269` Column | admitted |
| phase3-acs-004 | `VTN-DOM-0012785` Grade Beam | `TRANSFERS_LOAD_TO` | `VTN-DOM-0012273` Foundation System | admitted |
| phase3-acs-005 | `VTN-DOM-0012293` Soil Bearing Capacity | `CONSTRAINS` | `VTN-DOM-0012786` Slab-On-Grade | admitted |
| phase3-acs-006 | `VTN-DOM-0002906` Site Grading | `COORDINATES_WITH` | `VTN-DOM-0005262` Stormwater Flow Path | admitted |
| phase3-acs-007 | `VTN-DOM-0005262` Stormwater Flow Path | `COORDINATES_WITH` | `VTN-DOM-0002906` Site Grading | admitted |
| phase3-acs-008 | `VTN-DOM-0012742` Roof Drainage Interface | `COORDINATES_WITH` | `VTN-DOM-0012764` Roof Drainage Discharge Interface | admitted |
| phase3-acs-009 | `VTN-DOM-0012764` Roof Drainage Discharge Interface | `COORDINATES_WITH` | `VTN-DOM-0012742` Roof Drainage Interface | admitted |
| phase3-acs-010 | `VTN-DOM-0012280` Foundation Settlement | `CONSTRAINS` | `VTN-DOM-0012273` Foundation System | admitted |
| phase3-acs-011 | `VTN-DOM-0012749` Site Finished Floor Elevation Interface | `COORDINATES_WITH` | `VTN-DOM-0012740` Architectural Finished Floor Datum | admitted |
| phase3-acs-012 | `VTN-DOM-0012740` Architectural Finished Floor Datum | `COORDINATES_WITH` | `VTN-DOM-0012749` Site Finished Floor Elevation Interface | admitted |
| phase3-acs-defer-001 | VTN-DOM-0000317 Groundwater | `CONSTRAINS` | VTN-DOM-0000313 Excavation Support | deferred/rejected: Deferred because Kimi requested source/reference support despite general plausibility. |
| phase3-acs-defer-002 | VTN-DOM-0012743 Facade Anchor Interface | `COORDINATES_WITH` | VTN-DOM-0012313 Facade Assembly | deferred/rejected: Deferred because Kimi requested source/assembly context. |
| phase3-acs-defer-003 | VTN-DOM-0012210 Shaft Planning <-> VTN-DOM-0012790 Structural Core | `COORDINATES_WITH` | VTN-DOM-0012210 Shaft Planning <-> VTN-DOM-0012790 Structural Core | deferred/rejected: Deferred because Kimi requested source/directionality context. |
| phase3-acs-reject-001 | VTN-DOM-0012293 Soil Bearing Capacity | `CONSTRAINS` | VTN-DOM-0012273 Foundation System | deferred/rejected: Rejected/no-op because the base graph already contains this edge. |
