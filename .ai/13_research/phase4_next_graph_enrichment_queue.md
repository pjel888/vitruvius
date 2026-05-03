# Phase 4 Next Graph Enrichment Queue

Date: 2026-05-03T02:00:00Z  
Post-Overnight State — **257 active admitted relationships**

## Already Admitted (Cumulative: 257 edges across 16 relation families)

### Waves 1–4 (135 edges)
See prior closure reports for full enumeration.

### Wave 5 (35 edges)
See `phase4_wave5_graph_enrichment_admission_report.md`.

### Wave 6 (33 edges)
See `phase4_wave6_graph_enrichment_admission_report.md`.

### Wave 7 (21 edges)
See `phase4_wave7_graph_enrichment_admission_report.md`.

### Wave 8 (18 edges)
See `phase4_wave8_graph_enrichment_admission_report.md`.

### Wave 9 (15 edges)
See `phase4_wave9_graph_enrichment_admission_report.md`.

## Relation Type Distribution

| Family | Count | Notes |
|--------|-------|-------|
| COORDINATES_WITH | 122 | Dominant family; covers most disciplines |
| CROSS_DOMAIN_ALIGNMENT | 22 | Bidirectional pairs; discipline-scoped views |
| TRANSFERS_LOAD_TO | 30 | Structural load paths |
| SUPPORTS | 19 | Structural-equipment support |
| CONVEYS | 13 | HVAC air, plumbing water, electrical power |
| DISCHARGES_TO | 13 | Fixture drainage, civil discharge |
| AFFECTS | 6 | Seismic, wind, drainage, thermal |
| CONSTRAINS | 11 | Life-safety, planning |
| MITIGATES | 5 | Fire safety, water efficiency, geotechnical |
| INFORMS | 5 | Fire-safety sensor-to-system |
| RESISTS | 5 | Structural lateral forces |
| REQUIRES | 2 | MEPFS equipment dependencies |
| CONNECTS_TO | 1 | Building-to-utility interface |
| COLLECTS | 2 | Drainage collection |
| DRAINS_TO | 1 | Roof/floor drainage |

## Ready for Safe Non-Destructive Admission Review (Future Candidates)

- **Additional CONNECTS_TO:** building entrance ↔ site access, accessible route ↔ building entrance, sidewalk ↔ accessible route, exit discharge ↔ public way, service entry ↔ utility corridor
- **Additional COLLECTS:** catch basin → stormwater, roof drain → drainage, floor drain → drainage
- **Additional DRAINS_TO:** roof drain → stormwater, floor drain → sewer, sump pump → sewer
- **Additional REQUIRES:** fire alarm panel → emergency power, emergency lighting → emergency power, sprinkler → water service
- **Additional AFFECTS:** wind → roof, groundwater → excavation, thermal → insulation
- **Additional MITIGATES:** detention → surface runoff, bioretention → stormwater, sprinkler → fire hazard
- **Additional RESISTS:** braced frame → lateral loads, moment frame → lateral loads
- **Civil-structural interfaces:** retaining wall → foundation, earthworks → foundation, slope stability → grading
- **Material cross-domain alignments:** concrete ↔ reinforced concrete, steel ↔ steel structures, timber ↔ timber structures

## Needs Relation-Vocabulary Update Before Admission

None — all target relation types are in the admitted vocabulary.

## Needs Kimi/Source Review Before Admission

- **Grade Beam → Footing Foundation** (TRANSFERS_LOAD_TO) — verify no duplicate
- **Soil Bearing Capacity → Foundation System** (CONSTRAINS) — re-evaluate if new context emerges

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

## Rollback/Defer (Overnight Closure Gates)

None. All 122 overnight edges passed closure reconstruction, relation vocabulary, source/context, and visibility validation.

## Vocabulary Reservations for Future Waves

- **CONNECTS_TO:** 1 admission so far; more candidates exist if safe
- **COLLECTS:** 2 admissions so far; drainage collection candidates remain
- **DRAINS_TO:** 1 admission so far; roof/floor/sump drainage candidates remain
- **REQUIRES:** 2 admissions so far; MEPFS dependency candidates remain
- **AFFECTS:** 6 admissions so far; environmental/force candidates remain
- **MITIGATES:** 5 admissions so far; risk-mitigation candidates remain
- **RESISTS:** 5 admissions so far; lateral-force candidates remain
- **Additional COORDINATES_WITH:** still many unexplored domain pairs
- **Additional CROSS_DOMAIN_ALIGNMENT:** material and system alignments remain
