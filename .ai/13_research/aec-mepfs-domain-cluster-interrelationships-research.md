---
task: aec-mepfs-domain-cluster-interrelationships
phase: 03
created: 2026-05-01
author: AUDITOR
supersedes: null
status: ACCEPTED
---

# Research Pack — AEC-MEPFS Domain Cluster Interrelationships

## 01 — Discover
Local discovery found the active AEC-MEPFS backbone in scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json; staging artifacts are generated under 06_System-Manifests/aec-mepfs-backbone/shadow-staging/<RUN_ID>/. The graph uses BackboneNode records plus governed relationship rows. Existing predicates are intentionally constrained: roader_than, has_facet, 
equires, constrains, part_of, governs, maps_to_external_standard, pplicable_in_jurisdiction, conflicts_with, and supersedes.

## Source-backed research notes
- buildingSMART IFC: IFC is an open, vendor-neutral schema for built-asset information, not the whole domain ontology. It supports exchange and validation but must be extended or mapped for specialist semantics. Source: https://www.buildingsmart.org/standards/bsi-standards/industry-foundation-classes/ (retrieved 2026-05-01).
- buildingSMART IDS: IDS provides computer-interpretable exchange requirements for IFC models, useful for asset/information requirement validation without treating BIM as the whole graph. Source: https://www.buildingsmart.org/standards/bsi-standards/information-delivery-specification-ids/ (retrieved 2026-05-01).
- W3C LBD BOT: BOT distinguishes sites, buildings, storeys, spaces, zones, and elements; this supports the Vitruvius distinction between room, zone, building element, and system asset. Source: https://w3c-lbd-cg.github.io/bot/ (retrieved 2026-05-01).
- Brick Schema: Brick explicitly models physical equipment, logical zones, telemetry points, composition, topology, and point relationships such as AHU-to-VAV and VAV-to-zone feeds. Source: https://docs.brickschema.org/brick/relationships.html (retrieved 2026-05-01).
- Project Haystack: Haystack models buildings, spaces, equipment, sensors, points, live values, writable setpoints, and IoT data semantics for operational analytics. Sources: https://project-haystack.org/doc/docHaystack/Intro and https://project-haystack.org/doc/docHaystack/Points (retrieved 2026-05-01).
- ASHRAE 62.1/62.2: ventilation and IAQ standards provide source-family grounding for occupancy-to-ventilation-to-IAQ relationships; jurisdictional adoption still varies. Source: https://www.ashrae.org/technical-resources/bookstore/standards-62-1-62-2 (retrieved 2026-05-01).
- ASHRAE commissioning resources: Guideline 0/Standard 202 and related guides ground commissioning, OPR, systems manual, O&M documentation, and smoke-control commissioning relationships. Source: https://www.ashrae.org/technical-resources/bookstore/commissioning (retrieved 2026-05-01).
- NFPA source families: NFPA 13/20/25/72/92/101/110 provide North American fire-protection, fire-alarm, smoke-control, ITM, life-safety, and emergency-power source-family grounding, but are not universal law. Official NFPA code-development URLs were used as metadata references; no standard text was copied.
- WBDG/VA plumbing manual: public WBDG guidance frames plumbing as drainage, waste, vent, water distribution, storm drainage, fuel gas, and specialty systems designed for sanitary, safe, reliable, sustainable facilities. Source: https://www.wbdg.org/va/design-manuals-pg-18-10/plumbing (retrieved 2026-05-01).
- CDC Legionella guidance: building water systems need water-management programs where risk exists; this supports public-health relationships among domestic hot water, storage/distribution, maintenance, and water-quality monitoring. Source: https://www.cdc.gov/control-legionella/about/ (retrieved 2026-05-01).

## Research-to-graph implications
1. Use existing governed predicates for compatibility, but add mechanism metadata (
elation_type, category, nature, weight, confidence, lifecycle phase, rationale, source families) to new edges.
2. Prefer cross-domain, directional, typed edges over broad node count expansion.
3. Keep source usage metadata-only and jurisdictionally scoped.
4. Add validation to prevent placeholders, missing descriptions, duplicate labels, orphan introduced nodes, weak 
elated_to, missing provenance/rationale on enriched relationships, unsupported fields, and broken endpoints.
