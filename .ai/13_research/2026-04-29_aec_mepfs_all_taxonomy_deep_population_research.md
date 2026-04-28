---
task: aec-mepfs-all-taxonomy-deep-population-research
phase: AEC-MEPFS taxonomy expansion
status: completed
created: 2026-04-29
---

# AEC-MEPFS All-Taxonomy Deep Population Research

## Purpose

Expand the AEC-MEPFS Backbone from a useful but still sparse taxonomy into a richer prelaunch knowledge-graph backbone across all root taxonomies. This research is used only for metadata-level topic and subtopic labels. It does not admit protected source payloads, standards clauses, tables, figures, datasets, exam questions, or local raw-source text.

## Repo evidence used

- `scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json` was the authoritative authored fixture.
- Latest pre-expansion committed evidence was run `20260428T144427Z` with 2697 nodes, 2673 edges, 24 roots, and max depth 4.
- Local raw-source filenames under `001_Raw-Source-Layer/` were used only as source-family signals. No raw document text was copied.
- OMX read-only research workers supplied domain recommendations for architecture/planning/history/laws, civil/structural/geotech/transport/urban/infrastructure, MEPFS/security/smart systems, and evidence/metadata labels.

## Official and public research signals

| Area | Source | Taxonomy signal used |
|---|---|---|
| Architecture | PRC Architecture syllabi | History/theory/planning/practice, structures/materials/construction/utilities, design/site planning, world architectural eras, tropical design, professional practice, codes, and utilities. |
| Civil / structural / transport | PRC Civil Engineering page and 2026 CELE adjustment | Civil practice includes streets, bridges, highways, railroads, airports, ports, canals, flood protection, drainage, water supply, sewerage, tunnels, and related infrastructure; exam grouping reinforces hydraulics, geotechnical, structural analysis/design, surveying, transportation/highway, and construction management. |
| Urban planning | PRC Environmental Planning page and 2024 TOS | Planning information management, mandated plans, CLUP/CDP distinction, development planning, sectoral plans, mapping tools, DRR/CCA, land-use controls, and site planning. |
| Sanitary engineering | PRC Sanitary Engineering 2022 enhanced syllabi/TOS | Civil engineering, public health engineering, environmental engineering, sanitary science for buildings, wastewater/urban drainage, and water supply engineering. |
| Electrical / mechanical | PRC Electrical and Mechanical Engineering pages | Professional regulatory scope and source-family anchors for electrical, low-voltage, power, mechanical, HVAC, plant, and equipment systems. |
| Engineering breadth | ABET engineering criteria | Breadth/depth across engineering topics, design experience, environmental media, geoscience/geological engineering, engineering management, and systems-oriented engineering topics. |
| HVAC | ASHRAE Handbook systems/equipment page | HVAC systems and equipment, steam, district heating/cooling, germicidal UV, controls, systems selection, operations, and applications. |
| Plumbing | ICC 2024 International Plumbing Code table of contents | Fixtures, traps/interceptors/separators, storm drainage, special piping, nonpotable water, graywater, referenced standards, roof drains, subsoil drains, and pumping systems. |

## Local source-family signals

The raw-source filename inventory supports keeping explicit branches for Philippine laws and professional domains, including PD 1096, BP 344, RA 9514, RA 9266, RA 1378, PD 856, water/wastewater laws, heritage law, CLUP/zoning materials, utilities, plumbing, electrical, mechanical, fire, construction, materials, history, theory, and conservation references. These are filename-level source signals only.

## Domain expansion decisions

1. **All roots should receive more detail, not just Architecture.** Architecture was already improved, but Civil, Structural, Geotechnical, Urban Planning, Mechanical, Electrical, Plumbing, Fire, Sanitary, Security, Smart Systems, Heritage, Laws, Metadata/Governance, Materials, Construction, Performance, Sustainability, Digital, Operations, and Figures all needed more L2/L3/L4 depth.
2. **World architecture history belongs under History as a full global branch.** `HIS` now gets era/region branches for prehistoric, ancient, classical, Asian, African, American, medieval, Renaissance, Baroque/Rococo, Industrial, Modernist, Postmodern, and contemporary topics.
3. **Philippine building-law families belong under Laws as metadata rule families.** `LAW` now gets building-code, fire-code, accessibility, professional-practice, plumbing, electrical, water, clean-water, sanitation, environmental, energy, heritage, zoning/CLUP, housing/subdivision, procurement/contracts, and liability families.
4. **Services must be cyber-physical and cross-disciplinary.** Mechanical, electrical, fire, security, and smart systems remain separate canonical roots but are ready for future typed cross-links such as `INTERLOCKED_WITH`, `CONTROLLED_BY`, `MONITORED_BY`, and `HAS_PRIVACY_OVERLAY`.
5. **Metadata governance is first-class.** Source authority, currentness, evidence, artifact, validation, benchmark, and route-inventory labels should exist in the backbone so future document and runtime evidence can be classified without overloading design disciplines.

## Safety boundary

This research supports a metadata-only taxonomy population. It does not authorize protected ingest, live Neo4j mutation, KG rebuild/reload/reset, production graph promotion, runtime route changes, or Explorer behavior changes.
