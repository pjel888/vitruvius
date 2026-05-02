# Phase 4 Next Graph Enrichment Queue

Date: 2026-05-03T01:57:00Z  
Post-Wave-4 State

## Already Admitted (Cumulative: 135 edges across 14 relation families)

### Waves 1–3 (102 edges)
See prior closure reports for full enumeration.

### Wave 4 (33 edges)

**COORDINATES_WITH (8):**
- Air Handling Units → Roof Systems
- Air Handling Units → Wall And Facade Systems
- Passenger Lifts → Construction Systems
- Exits → Means Of Egress Planning
- Fire Barriers → Compartmentation And Fire Resistance
- Water Service And Meters → Water Distribution Networks
- Wastewater Infrastructure → Sewerage Networks
- Grounding Electrode Systems → Foundations Interface

**CONVEYS (6):**
- Duct Design → Diffusers And Terminal Devices
- Chilled Water Loops → Chilled Water
- Hot Water Loops → Hydronic Heating
- Water Service And Meters → Lavatories
- Water Service And Meters → Showers
- Water Service And Meters → Water Closets

**INFORMS (2):**
- Smoke Detection → Detection
- Heat Detection → Detection

**CONSTRAINS (2):**
- Occupant Load → Exits
- Travel Distance → Exits

**SUPPORTS (4):**
- Frame Systems → Slabs Beams And Columns
- Frame Systems → Air Handling Units
- Frame Systems → Cooling Towers
- Frame Systems → Generators

**TRANSFERS_LOAD_TO (2):**
- Slabs Beams And Columns → Foundations Interface
- Wall Systems → Foundations Interface

**DISCHARGES_TO (3):**
- Water Distribution Networks → Water Infrastructure
- Sewerage Networks → Wastewater Infrastructure
- Stormwater Networks → Drainage

**CROSS_DOMAIN_ALIGNMENT (6 — 3 bidirectional pairs):**
- Chilled Water ↔ Chilled Water Loops
- Hydronic Heating ↔ Hot Water Loops
- Water Heating ↔ Water Heaters

## Ready for Safe Non-Destructive Admission Review (Future Wave 5 Candidates)

- **Lateral Stability System → Lateral Loads** (RESISTS) — complements existing Braced Frame / Moment Frame RESISTS edges
- **Lateral Stability System → Structural Wind Load / Structural Seismic Load** (RESISTS) — same family as Wave 3 RESISTS
- **Diaphragm Opening Coordination → Diaphragm Action** (AFFECTS) — coordination-mechanism family
- **Soil Infiltration Rate → Bioretention Cell / Permeable Pavement** (INFORMS) — same family as Wave 3 INFORMS
- **Hydrologic Design Basis → Storm Sewer Pipe / Surface Runoff** (INFORMS) — hydrology-to-design family
- **CONNECTS_TO candidates** — piping, ducting, cabling physical connections (first safe admission for this vocabulary entry)
- **FLS-ELE coordination** — fire alarm ↔ electrical power, emergency lighting ↔ egress
- **PLS-ELE coordination** — plumbing fixtures ↔ electrical services
- **Additional structural-civil interfaces** — retaining wall, earthworks, slope stability

## Needs Relation-Vocabulary Update Before Admission

None — all target relation types are already in the admitted vocabulary.

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

## Rollback/Defer (Wave 4 Closure Gates)

None. All 33 Wave 4 edges passed closure reconstruction, relation vocabulary, source/context, and visibility validation.

## Vocabulary Reservations for Future Waves

- **CONNECTS_TO**: in vocabulary, awaiting first safe admission candidate (target: Wave 5)
- **Additional COORDINATES_WITH pairs**: site/civil and MEPFS coordination still has unexplored candidates
- **Additional TRANSFERS_LOAD_TO paths**: lateral system load paths may be candidates
- **REQUIRES / COLLECTS / MITIGATES / RESISTS / AFFECTS**: expand to new domain pairs where safe
