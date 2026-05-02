# Phase 4 Next Graph Enrichment Queue

Date: 2026-05-03T01:00:00Z
Post-Wave-3 State

## Already Admitted (Wave 3 — 22 edges)

| Edge ID | Type | Source → Target |
|---------|------|-----------------|
| VTN-DOM-0012759--collects--VTN-DOM-0012758 | COLLECTS | Catch basin → Surface runoff |
| VTN-DOM-0012759--drains_to--VTN-DOM-0012760 | DRAINS_TO | Catch basin → Storm sewer pipe |
| VTN-DOM-0012760--conveys--VTN-DOM-0005262 | CONVEYS | Storm sewer pipe → Stormwater flow path |
| VTN-DOM-0012762--collects--VTN-DOM-0012758 | COLLECTS | Inlet capacity → Surface runoff |
| VTN-DOM-0000224--mitigates--VTN-DOM-0012758 | MITIGATES | Detention/retention → Surface runoff |
| VTN-DOM-0012769--informs--VTN-DOM-0012273 | INFORMS | Geotechnical investigation → Foundation system |
| VTN-DOM-0012770--informs--VTN-DOM-0012767 | INFORMS | Soil infiltration rate → Permeable pavement |
| VTN-DOM-0012280--affects--VTN-DOM-0012273 | AFFECTS | Foundation settlement → Foundation system |
| VTN-DOM-0000317--affects--VTN-DOM-0000313 | AFFECTS | Groundwater → Excavation support |
| VTN-DOM-0003029--constrains--VTN-DOM-0002906 | CONSTRAINS | Slope stability → Site grading |
| VTN-DOM-0012773--affects--VTN-DOM-0012273 | AFFECTS | Differential settlement → Foundation system |
| VTN-DOM-0012273--supports--VTN-DOM-0012269 | SUPPORTS | Foundation system → Column |
| VTN-DOM-0012273--supports--VTN-DOM-0012261 | SUPPORTS | Foundation system → Column grid |
| VTN-DOM-0012269--supports--VTN-DOM-0012263 | SUPPORTS | Column → Beam |
| VTN-DOM-0012282--resists--VTN-DOM-0000259 | RESISTS | Braced frame → Lateral loads |
| VTN-DOM-0012283--resists--VTN-DOM-0000259 | RESISTS | Moment frame → Lateral loads |
| VTN-DOM-0000233--coordinates_with--VTN-DOM-0012749 | COORDINATES_WITH | Site access → Site finished floor elevation |
| VTN-DOM-0000012--coordinates_with--VTN-DOM-0000233 | COORDINATES_WITH | Accessible routes → Site access |
| VTN-DOM-0012809--coordinates_with--VTN-DOM-0000012 | COORDINATES_WITH | Curb ramp geometry → Accessible routes |
| VTN-DOM-0012289--coordinates_with--VTN-DOM-0012794 | COORDINATES_WITH | Expansion joint → Structural movement joint |
| VTN-DOM-0012313--coordinates_with--VTN-DOM-0012743 | COORDINATES_WITH | Facade assembly → Facade anchor interface |
| VTN-DOM-0012311--transfers_load_to--VTN-DOM-0012263 | TRANSFERS_LOAD_TO | Roof assembly → Beam |

## Ready for Safe Non-Destructive Admission Review (Future Wave 4 Candidates)

These candidates were deferred from prior waves and may be reconsidered:

- **Lateral Stability System → Lateral Loads** (RESISTS) — complements existing Braced Frame / Moment Frame RESISTS edges
- **Lateral Stability System → Structural Wind Load / Structural Seismic Load** (RESISTS) — same family as Wave 3 RESISTS
- **Diaphragm Opening Coordination → Diaphragm Action** (AFFECTS) — coordination-mechanism family
- **Soil Infiltration Rate → Bioretention Cell / Permeable Pavement** (INFORMS) — same family as Wave 3 INFORMS
- **Hydrologic Design Basis → Storm Sewer Pipe / Surface Runoff** (INFORMS) — hydrology-to-design family

## Needs Relation-Vocabulary Update Before Admission

- **Curb Ramp Geometry Interface → Accessible Public-Way Crossing Tie-In** (CONNECTS_TO) — CONNECTS_TO is in vocabulary but not yet used; candidate needs edge-neighborhood review

## Needs Kimi/Source Review Before Admission

- **Grade Beam → Footing Foundation** (TRANSFERS_LOAD_TO) — already admitted in prior waves; verify no duplicate
- **Soil Bearing Capacity → Foundation System** (CONSTRAINS) — deferred as no-op due to existing graph context; re-evaluate if new context emerges

## High-Risk Blocked (Explicitly Gated)

| Packet | Label | Blocker | Next Action |
|--------|-------|---------|-------------|
| p1-decision-packet-fa4918982178 | Mat Foundation | 3-way cross-domain, mixed taxonomy depths, no resources | Future wave: consider pairwise STR-GEO CROSS_DOMAIN_ALIGNMENT only |
| p1-decision-packet-3946860e327a | Load Path | Different taxonomy contexts, high risk | Remains blocked pending domain review |
| p1-decision-packet-0cfa6a7f88a1 | Wall Finishes | 3 nodes, different types, high risk | Remains blocked pending domain review |
| p1-decision-packet-9d2ac282265b | Shear Wall | Different node roles (STR vs ARC) | Remains blocked; reviewed Wave 2 |
| p1-decision-packet-12e81a4fbcde | Retaining Wall | Different taxonomy contexts | Remains blocked pending domain review |

## Duplicate Base Edge / No-Op

- Soil Bearing Capacity → Foundation System: existing graph context provides equivalent semantics; no admission needed.
- Redundant footing subtype edges to Soils: deferred after Kimi review as no-op.

## Rejected (Do Not Revisit Without New Evidence)

- Directionally inverted stormwater flow path → surface runoff edge
- Near-duplicate Erosion And Sediment Control <-> Civil Erosion And Sediment Control edge
- Overclaim-prone exterior route REQUIRES public-way crossing tie-in

## Rollback/Defer (Wave 3 Closure Gates)

None. All 22 Wave 3 edges passed closure reconstruction, relation vocabulary, source/context, and visibility validation.

## Vocabulary Reservations for Future Waves

- CONNECTS_TO: in vocabulary, awaiting first safe admission candidate
- Additional COORDINATES_WITH pairs: site/civil coordination still has unexplored candidates
- Additional TRANSFERS_LOAD_TO paths: lateral system load paths may be candidates
