# Phase 4 Wave 1 Graph Enrichment Candidates

Date: 2026-05-02T11:25:29Z
Baseline active admitted relationships: 26
Final active admitted relationships: 51
New admitted relationships: 25
Baseline effective edges: 13,696
Final effective edges: 13,721
Base graph edges: 13,670 unchanged
Nodes: 10,018 unchanged
Approvals: 7
Transaction manifests: 60
Latest afterHash mismatches: 0
Aliases/redirects/tombstones: 0/0/0
Resources/nodeResourceLinks: 7/9 unchanged
Decision: canonical-20260502112100-b7a51ec7b419
Approval: canonical-approval-20260502112100-5cd241c0a1d3
Admission manifest: canonical-tx-20260502112100-243af2f4fb8d
P1 rebase manifest: canonical-tx-20260502112148-d6defc99a5f5

All candidates used existing nodes and existing admissible relation types only. Source/context basis was general non-numerical ACS domain synthesis plus existing graph taxonomy context; no source URL, standard edition, AHJ/jurisdiction, numerical design criterion, protected payload, merge, alias, redirect, tombstone, or Resource Layer mutation was asserted.

| Candidate | Source | Relation | Target | Outcome |
|---|---|---|---|---|
| p4w1-001 | `VTN-DOM-0012266` Slab | TRANSFERS_LOAD_TO | `VTN-DOM-0012263` Beam | admitted |
| p4w1-002 | `VTN-DOM-0012265` Joist | TRANSFERS_LOAD_TO | `VTN-DOM-0012264` Girder | admitted |
| p4w1-003 | `VTN-DOM-0012264` Girder | TRANSFERS_LOAD_TO | `VTN-DOM-0012269` Column | admitted |
| p4w1-004 | `VTN-DOM-0012780` Structural Beam | TRANSFERS_LOAD_TO | `VTN-DOM-0012781` Structural Column | admitted |
| p4w1-005 | `VTN-DOM-0012781` Structural Column | TRANSFERS_LOAD_TO | `VTN-DOM-0012782` Footing Foundation | admitted |
| p4w1-006 | `VTN-DOM-0012779` Suspended Slab System | TRANSFERS_LOAD_TO | `VTN-DOM-0012780` Structural Beam | admitted |
| p4w1-007 | `VTN-DOM-0012785` Grade Beam | TRANSFERS_LOAD_TO | `VTN-DOM-0012782` Footing Foundation | admitted |
| p4w1-008 | `VTN-DOM-0012791` Base Plate Connection | TRANSFERS_LOAD_TO | `VTN-DOM-0012782` Footing Foundation | deferred_wrong_abstraction |
| p4w1-009 | `VTN-DOM-0012792` Anchor Bolt Group | COORDINATES_WITH | `VTN-DOM-0012791` Base Plate Connection | admitted |
| p4w1-010 | `VTN-DOM-0012791` Base Plate Connection | COORDINATES_WITH | `VTN-DOM-0012792` Anchor Bolt Group | admitted |
| p4w1-011 | `VTN-DOM-0012793` Force Transfer Connection | COORDINATES_WITH | `VTN-DOM-0012791` Base Plate Connection | admitted |
| p4w1-012 | `VTN-DOM-0012791` Base Plate Connection | COORDINATES_WITH | `VTN-DOM-0012793` Force Transfer Connection | admitted |
| p4w1-013 | `VTN-DOM-0012788` Collector Drag Strut | TRANSFERS_LOAD_TO | `VTN-DOM-0012793` Force Transfer Connection | admitted |
| p4w1-014 | `VTN-DOM-0012789` Diaphragm Opening Coordination | CONSTRAINS | `VTN-DOM-0012787` Diaphragm Action | deferred_relation_type_overstrong |
| p4w1-015 | `VTN-DOM-0012778` Structural Seismic Load | CONSTRAINS | `VTN-DOM-0012787` Diaphragm Action | deferred_relation_type_overstrong |
| p4w1-016 | `VTN-DOM-0012794` Structural Movement Joint | COORDINATES_WITH | `VTN-DOM-0012745` Architectural Movement Joint Cover | admitted |
| p4w1-017 | `VTN-DOM-0012745` Architectural Movement Joint Cover | COORDINATES_WITH | `VTN-DOM-0012794` Structural Movement Joint | admitted |
| p4w1-018 | `VTN-DOM-0012059` Site Drainage Planning | COORDINATES_WITH | `VTN-DOM-0000232` Site Grading | admitted |
| p4w1-019 | `VTN-DOM-0000232` Site Grading | COORDINATES_WITH | `VTN-DOM-0012059` Site Drainage Planning | admitted |
| p4w1-020 | `VTN-DOM-0012059` Site Drainage Planning | COORDINATES_WITH | `VTN-DOM-0012758` Surface Runoff | deferred_activity_phenomenon_mismatch |
| p4w1-021 | `VTN-DOM-0012758` Surface Runoff | DISCHARGES_TO | `VTN-DOM-0012759` Catch Basin | admitted |
| p4w1-022 | `VTN-DOM-0012759` Catch Basin | DISCHARGES_TO | `VTN-DOM-0012760` Storm Sewer Pipe | admitted |
| p4w1-023 | `VTN-DOM-0012760` Storm Sewer Pipe | DISCHARGES_TO | `VTN-DOM-0000224` Detention And Retention | deferred_context_specific |
| p4w1-024 | `VTN-DOM-0012763` Overland Stormwater Overflow Path | DISCHARGES_TO | `VTN-DOM-0012814` Culvert Drainage Interface | deferred_context_specific |
| p4w1-025 | `VTN-DOM-0012765` Perimeter Drain | DISCHARGES_TO | `VTN-DOM-0012760` Storm Sewer Pipe | admitted |
| p4w1-026 | `VTN-DOM-0012767` Permeable Pavement | COORDINATES_WITH | `VTN-DOM-0012815` Pavement Subgrade Interface | rejected_too_generic |
| p4w1-027 | `VTN-DOM-0012815` Pavement Subgrade Interface | COORDINATES_WITH | `VTN-DOM-0012767` Permeable Pavement | rejected_too_generic |
| p4w1-028 | `VTN-DOM-0012770` Soil Infiltration Rate | CONSTRAINS | `VTN-DOM-0012766` Bioretention Cell | deferred_wrong_relation_type |
| p4w1-029 | `VTN-DOM-0012750` Topography Survey Surface | CONSTRAINS | `VTN-DOM-0012749` Site Finished Floor Elevation Interface | rejected_wrong_relation_type |
| p4w1-030 | `VTN-DOM-0012749` Site Finished Floor Elevation Interface | COORDINATES_WITH | `VTN-DOM-0012804` Design Flood Elevation Interface | rejected_regulatory_context_risk |
| p4w1-031 | `VTN-DOM-0012804` Design Flood Elevation Interface | COORDINATES_WITH | `VTN-DOM-0012749` Site Finished Floor Elevation Interface | rejected_regulatory_context_risk |
| p4w1-032 | `VTN-DOM-0012739` Egress Discharge Site Interface | COORDINATES_WITH | `VTN-DOM-0012813` Accessible Public-Way Crossing Tie-In | admitted |
| p4w1-033 | `VTN-DOM-0012813` Accessible Public-Way Crossing Tie-In | COORDINATES_WITH | `VTN-DOM-0012739` Egress Discharge Site Interface | admitted |
| p4w1-034 | `VTN-DOM-0012058` Fire Access Site Planning | COORDINATES_WITH | `VTN-DOM-0012754` Emergency Vehicle Access Route | admitted |
| p4w1-035 | `VTN-DOM-0012754` Emergency Vehicle Access Route | COORDINATES_WITH | `VTN-DOM-0012058` Fire Access Site Planning | admitted |
| p4w1-036 | `VTN-DOM-0012810` Emergency Access Geometry Basis | COORDINATES_WITH | `VTN-DOM-0012808` Pavement Structure Interface | rejected_abstract_endpoint_mismatch |
| p4w1-037 | `VTN-DOM-0012791` Base Plate Connection | COORDINATES_WITH | `VTN-DOM-0012782` Footing Foundation | admitted |
| p4w1-038 | `VTN-DOM-0012782` Footing Foundation | COORDINATES_WITH | `VTN-DOM-0012791` Base Plate Connection | admitted |
| p4w1-039 | `VTN-DOM-0012792` Anchor Bolt Group | COORDINATES_WITH | `VTN-DOM-0012782` Footing Foundation | ready_future_queue |
| p4w1-040 | `VTN-DOM-0012782` Footing Foundation | COORDINATES_WITH | `VTN-DOM-0012792` Anchor Bolt Group | ready_future_queue |
