# Cross-Domain Overlay Enrichment Research Pack

Date: 2026-04-29  
Run id: 20260429T075023Z  
Status: completed after validation

## Research purpose

Identify rights-safe, public metadata source families and practical AEC-MEPFS semantic relationship patterns for the next graph-enrichment phase: equipment anchorage/nonstructural support coordination, commissioning/testing/acceptance/handover, operational resilience/continuity, and jurisdiction/code/applicability overlays.

## Baseline inspected

- File-backed source graph: `scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json`
- Previous validated run: `20260429T065436Z`
- Previous counts: 9076 BackboneNode records, 9326 governed relationships, 41 source-rights registry rows
- Existing governed predicates available: `broader_than`, `part_of`, `requires`, `constrains`, `maps_to_external_standard`, `has_facet`, `governs`, `applicable_in_jurisdiction`, and related registry-approved predicates.

## Kimi/advisory research posture

Kimi was used/attempted for advisory taxonomy and source-family review, with Codex Spark excluded from enrichment routing. The final implementation is deterministic and steward-authored; no model output is stored as a protected payload. Existing `opencode.json` routes keep KG enrichment research on `moonshot/kimi-k2.6`; team workers were launched with non-Spark model args and performed read-only evidence checks only.

## Public metadata source families used

Only source-family names, public landing-page URLs, titles, and steward-written metadata descriptions are used. No standards clauses, tables, figures, diagrams, or protected text are stored.

- FEMA E-74 nonstructural earthquake damage reduction guidance: nonstructural anchorage/restraint and continuity context.
- SMACNA seismic restraint and duct construction manual families: HVAC duct, hanger, support, and bracing context.
- NECA National Electrical Installation Standards: electrical equipment support, installation, temporary power, and maintenance metadata context.
- ASHRAE Guideline 0 and ASHRAE/IES Standard 202 commissioning references: OPR/BOD, commissioning process, functional testing, systems manual, and handover context.
- NFPA integrated testing, ITM, and EPSS standard families: integrated systems testing, fire protection inspection/testing/maintenance, emergency power acceptance context.
- ISO 22301: business continuity management and continuity objective metadata context.
- ISO/IEC 27001 and ISA/IEC 62443: information security, OT/BAS/IACS cybersecurity, and segmentation metadata context.
- ASCE 24 and existing ASCE/FEMA source rows: flood-resistant design, nonstructural seismic coordination, and existing-building evaluation crosswalks.
- NIBS/WBDG commissioning resources: public commissioning documents, roles, OPR, BOD, systems manual, and closeout context.

## Gap analysis

1. Nonstructural equipment coordination existed as scattered discipline nodes, but the graph lacked explicit overlay nodes for seismic restraint, wind restraint, flood-resilient placement, vibration isolation, housekeeping pads, hangers/bracing, penetrations, firestopping, access clearance, maintenance clearance, and critical equipment protection.
2. Commissioning was present but shallow: OPR, BOD, commissioning plans, integrated systems testing, discipline-specific acceptance testing, COBie/digital handover, preventive maintenance setup, warranty/closeout, and O&M documentation needed typed links.
3. Resilience needed facility-operation semantics tying business continuity, backup/emergency/standby power, N+1 redundancy, RTO/RPO, wildfire smoke, extreme heat, water/sanitation continuity, emergency communications, and OT/BAS cybersecurity.
4. Applicability overlays were under-modeled for AHJ, local/model code adoption, occupancy, construction type, risk category, climate zone, seismic design category, flood hazard area, fire area, high-rise, healthcare, data center, laboratory, industrial, critical-facility, commissioning, operations, and maintenance phase applicability.

## Research conclusion

A bounded metadata-only overlay enrichment is justified. The best graph value comes from adding typed, source-backed relationships and a modest number of real overlay/source nodes rather than further broad taxonomy expansion.
