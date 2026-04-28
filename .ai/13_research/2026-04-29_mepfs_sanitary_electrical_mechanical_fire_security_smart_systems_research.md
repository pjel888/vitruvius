---
task: read-only-research-worker-3-mepfs-systems
phase: AEC-MEPFS read-only research
status: completed
created: 2026-04-29
worker: worker-3
---

# MEPFS / Sanitary / Electrical / Mechanical / Fire / Security / Smart Systems Research

## Purpose

Map the current Vitruvius AEC-MEPFS knowledge/backbone coverage for building-service disciplines and identify rights-safe, current-source gaps for the next source-admission or taxonomy-hardening pass. This is a read-only research synthesis: no protected source payloads, no standards clauses, no Neo4j mutation, and no runtime behavior changes.

## Executive findings

1. **The file-backed AEC-MEPFS backbone already has first-class branches for the assigned systems.** The latest staged graph evidence at `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260428T144427Z/shadow-backbone-graph.json` reports **2,697 nodes**, **2,673 edges**, **24 roots**, and **max depth 4**. The relevant roots are `MEC`, `ELE`, `PLS`, `SAN`, `FLS`, `SEC`, and `SMS`.
2. **Each assigned branch has a uniform 101-node subtree** in `scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json`: 1 L1 root, 10 L2 topics, 30 L3 subtopics, and 60 L4 concept/rule-context anchors.
3. **Canonical concept/source coverage is much thinner than the backbone.** The shared canonical layer has strong fire-law, water, wastewater, and limited plumbing/sanitary anchors, but very sparse direct concept files for mechanical, electrical, security, CCTV/access-control, BAS/BMS, and smart systems.
4. **The source-rights registry recognizes Philippine MEP-adjacent legal families but should be split and currentness-hardened.** Current registry rows include `SRC-PH-BFP-RA9514-RIRR`, `SRC-PH-PD856`, `SRC-PH-DPWH-PGBC`, and a combined `SRC-PH-PLUMBING-ELECTRICAL-PROFESSIONAL-CODES`. Mechanical, sanitary-engineering, CCTV/privacy, smart/building automation, and cyber-physical security should become explicit source-family records.
5. **A currentness correction is needed for CCTV/security overlays.** Repo-local research and current web checks show NPC Advisory 2020-04 is superseded/repealed by **NPC Circular No. 2024-02 - Closed-Circuit Television (CCTV) Systems**, effective in 2024; the next security source pack should prefer the 2024 circular, not the 2020 advisory.

## Repo-local evidence

### Latest backbone and branch counts

Inspected:

- `scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json`
- `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260428T144427Z/shadow-backbone-graph.json`
- `006_System-Manifests/aec-mepfs-backbone/taxonomy-expansion/20260428T144427Z/architecture-taxonomy-expansion-report.json`
- `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-28_aec_mepfs_taxonomy_domain_expansion_and_spacing_packet.md`
- `.ai/03_plans/AEC-MEPFS-Backbone/2026-04-28_aec_mepfs_l4_concept_rule_expansion_packet.md`

Fixture totals from `admitted_backbone_nodes_l1_l2.json`:

| Metric | Count |
|---|---:|
| Backbone records | 2,697 |
| `broader_than` relationships | 2,673 |
| L1 roots | 24 |
| L2 nodes | 261 |
| L3 nodes | 804 |
| L4 concept/rule-context anchors | 1,608 |

Assigned-branch subtrees:

| Root | Label | L2 | L3 | L4 | Subtree total |
|---|---|---:|---:|---:|---:|
| `MEC` | Mechanical Systems | 10 | 30 | 60 | 101 |
| `ELE` | Electrical And Low-Voltage Systems | 10 | 30 | 60 | 101 |
| `PLS` | Plumbing And Sanitary Systems | 10 | 30 | 60 | 101 |
| `SAN` | Sanitary Engineering | 10 | 30 | 60 | 101 |
| `FLS` | Fire And Life Safety | 10 | 30 | 60 | 101 |
| `SEC` | Security Systems | 10 | 30 | 60 | 101 |
| `SMS` | Smart Systems And Automation | 10 | 30 | 60 | 101 |

### Current branch shape

- `MEC`: air-conditioning, cooling, controls, elevators/escalators, heating, hydronics, plant, refrigeration, smoke-control interface, ventilation.
- `ELE`: communications, controls, emergency power, grounding/bonding, lighting, low-voltage systems, metering/monitoring, power distribution, renewable power, electronic security.
- `PLS`: fixtures, fuel gas, hot water, irrigation interfaces, pumps/pressure, sanitary drainage, storm drainage, water treatment, water supply, wastewater.
- `SAN`: public health engineering, wastewater collection, treatment systems, solid waste, drainage/flood sanitation, industrial wastewater, water-supply sanitation, septic/on-site systems, sanitary facility planning, environmental sanitation compliance.
- `FLS`: detection/alarm, compartmentation, hazard detection, egress, fire department access, fire protection, special hazards, risk/fire strategy, smoke management, suppression.
- `SEC`: video surveillance, access control, intrusion detection, perimeter security, electric fences, security lighting, security operations centers, identity/credential management, emergency communication, cyber-physical interfaces.
- `SMS`: IoT devices, home automation, building automation, sensors/actuators, edge gateways, smart networks, data platforms, occupant apps/voice, interoperability protocols, smart energy controls.

### Canonical concept/source coverage

Relevant shared canonical files already present:

- Fire/life-safety: `003_Canonical-Knowledge-Layer/shared/sources/fire-code-of-the-philippines.md`, `003_Canonical-Knowledge-Layer/shared/sources/implementing-rules-and-regulations-of-the-fire-code-of-the-philippines.md`, `003_Canonical-Knowledge-Layer/shared/taxonomy/taxonomy-fire-life-safety.md`, `003_Canonical-Knowledge-Layer/shared/topics/topic-fire-protection.md`, and fire-related concept/relationship files.
- Sanitary/water/waste: `003_Canonical-Knowledge-Layer/shared/sources/revised-national-plumbing-code-of-the-philippines.md`, `003_Canonical-Knowledge-Layer/shared/sources/philippine-clean-water-act-of-2004.md`, `003_Canonical-Knowledge-Layer/shared/sources/the-water-code-of-the-philippines.md`, plus concepts such as `waste-disposal`, `wastewater-charge-system`, `discharge-permit`, `water-permit`, `water-quality-management-area`, and `groundwater-drilling`.
- Mechanical/electrical: mostly indirect through PD 1096/NBCP excerpts and high-level taxonomy; direct canonical concept/source coverage is sparse.
- Security/smart systems: strong taxonomy coverage in the backbone fixture, but little direct canonical source evidence beyond data/privacy and general standards references in research packs.

## External currentness checks used

Only official or primary-ish sources were used for currentness and source-family recommendations; no protected code/standards text was copied.

- DPWH Philippine Green Building Code page: https://dpwh.gov.ph/DPWH/references/laws_codes_orders/pgbc
- BFP 2019 Revised IRR of RA 9514 PDF: https://bfp.gov.ph/wp-content/uploads/2019/10/RA9514-RIRR-rev-2019.pdf
- Lawphil PD 856 Code on Sanitation: https://lawphil.net/statutes/presdecs/pd1975/pd_856_1975.html
- PRC Mechanical Engineering page / RA 8495 practice scope: https://www.prc.gov.ph/index.php/mechanical-engineering
- PSME Philippine Mechanical Engineering Code 2012 listing: https://www.psme.org/product-page/philippine-mechanical-engineering-code-2012-hard-bound
- PRC Electrical Engineering page / RA 7920 context: https://www.prc.gov.ph/Pages/PRBv4/ElectricalEngineering.htm
- PRC Board of Electrical Engineering syllabus mentioning Philippine Electrical Code Parts 1 and 2: https://www.prc.gov.ph/uploaded/documents/Board%20of%20Electrical%20Engineering-SB.pdf
- PRC Sanitary Engineering page: https://www.prc.gov.ph/Pages/PRBv4/SanitaryEngineering.htm
- PRC RA 1364 Sanitary Engineering Law PDF: https://www.prc.gov.ph/sites/default/files/Sanitary%20Engineering%20Law_0.PDF
- PRC Sanitary Engineering Resolution No. 06 s. 2023 snippet/adoption of Uniform Plumbing Code of the Philippines as a referral code: https://www.prc.gov.ph/sites/default/files/2023-06%20published%20Sanitary.pdf
- NPC Circular No. 2024-02 CCTV Systems: https://privacy.gov.ph/wp-content/uploads/2024/08/NPC-Circular-No.-2024-02-CCTV-Systems.pdf
- NPC advisory/circular index confirming 2020-04 was repealed by 2024-02: https://privacy.gov.ph/pips-and-pics/advisories-circulars/
- ASHRAE Handbook page for current HVAC reference-family context: https://www.ashrae.org/technical-resources/ashrae-handbook
- ASHRAE building controls/BACnet source-family context: https://www.ashrae.org/technical-resources/bookstore/building-controls
- CEDIA smart-home domain framing: https://cedia.org/smart-home-professionals/

## Recommended next source-family splits

### P0: split combined Philippine professional-code registry row

Current registry row `SRC-PH-PLUMBING-ELECTRICAL-PROFESSIONAL-CODES` is too broad for source admission. Split into distinct metadata-first source families:

1. `SRC-PH-PEC` — Philippine Electrical Code / RA 7920 professional context / PRC Board of Electrical Engineering.
2. `SRC-PH-PME-CODE` — Philippine Mechanical Engineering Code / RA 8495 / PSME and PRC Board of Mechanical Engineering context.
3. `SRC-PH-PLUMBING-CODE` — plumbing code family / master-plumber law / NAMPAP where official access permits.
4. `SRC-PH-SANITARY-RA1364` — Sanitary Engineering Law and Board of Sanitary Engineering issuances.
5. `SRC-PH-UNIFORM-PLUMBING-REFERRAL-2023` — PRC Sanitary Board Resolution No. 06 s. 2023 as a referral-code metadata anchor, without copying code content.

### P0: add CCTV/privacy security source family

Add `SRC-PH-NPC-CCTV-2024` for NPC Circular No. 2024-02. Model it as security/privacy overlay metadata for `SEC.VSS`, `SEC.SOC`, `SEC.CPI`, and relevant smart-system data platform nodes. Do not rely on NPC Advisory 2020-04 as current authority except as superseded history.

### P1: add smart/building automation standards families

Add reference-only/metadata-crosswalk source families for:

- ASHRAE BACnet / building controls / BAS guidance family.
- CEDIA smart-home professional topic family for residential smart-system vocabulary calibration.
- Cybersecurity/critical-infrastructure guidance for OT, IoT, device lifecycle, and network segmentation, preferably official government/standards-body sources.

## Recommended graph-model hardening

1. **Use one canonical home and cross-domain edges.** Keep `SEC` separate from `ELE.SEC` and `SMS` but connect them with typed relations. Example: `ELE.SEC.VSU` can `SERVED_BY` / `INTEGRATES_WITH` `SEC.VSS`, while `SMS.BAS` can `MONITORS_OR_CONTROLS` `MEC.CTL` and `ELE.CTL`.
2. **Promote service-system edges beyond hierarchy.** Add relationship predicates for `SERVED_BY`, `PROTECTED_BY`, `MONITORED_BY`, `CONTROLLED_BY`, `INTERLOCKED_WITH`, `REQUIRES_CLEARANCE_FROM`, and `HAS_PRIVACY_OVERLAY` after steward approval.
3. **Treat fire/security/smart as cyber-physical systems.** Fire alarms, access control, CCTV, BAS/BMS, energy controls, and IoT should have both physical device topology and data/privacy/cybersecurity overlays.
4. **Represent Philippine rule families as overlays.** PD 856, RA 1364, RA 9514 RIRR, PEC, PME Code, plumbing-code families, and NPC CCTV rules should constrain canonical concepts through jurisdiction/effective-date metadata rather than duplicating concept nodes.
5. **Keep protected standards out of fixtures.** Use labels, public metadata, official URLs, edition identifiers, source-family records, and crosswalk IDs only until license/legal review authorizes more.

## Priority gap list by assigned domain

| Domain | Backbone status | Canonical/source gap | Recommended next action |
|---|---|---|---|
| Mechanical | Strong L1-L4 taxonomy | No explicit PME Code source family; limited direct mechanical concepts | Add PME/RA8495/PSME metadata source family; map HVAC/controls/refrigeration source families |
| Electrical | Strong L1-L4 taxonomy | Combined professional-code row; no explicit PEC source pack | Split `SRC-PH-PEC`; add currentness record and edition metadata |
| Plumbing/Sanitary | Strong `PLS` and `SAN` branches | Canonical water/waste stronger than code-family structure; RA1364 not explicit in registry | Add RA1364, PRC Sanitary Board, and Uniform Plumbing referral records |
| Fire | Strong taxonomy and strongest canonical legal coverage | Needs current BFP/RIRR edition metadata and fire-system device crosslinks | Harden RA9514 RIRR source-family currentness and map to `FLS` + `MEC.SMK` + `ELE.EPW` |
| Security | Strong `SEC` taxonomy | CCTV/access/privacy official current source missing; 2020 NPC advisory superseded | Add NPC Circular 2024-02; add DILG/local CCTV mandates only as jurisdiction overlays |
| Smart systems | Strong `SMS` taxonomy | Needs official BAS/BACnet/smart-home/cyber source-family records | Add ASHRAE/CEDIA/reference-only families and OT cybersecurity overlays |

## Validation evidence

- `python3` fixture inspection confirmed 2,697 records, 2,673 relationships, and uniform 101-node subtrees for `MEC`, `ELE`, `PLS`, `SAN`, `FLS`, `SEC`, and `SMS`.
- `rg` repo scans confirmed relevant canonical source/concept files are concentrated in fire, water/wastewater, and plumbing/sanitation; mechanical/electrical/security/smart are mostly taxonomy-first today.
- Web currentness checks found official/primary sources for DPWH PGBC, BFP RA9514 RIRR, Lawphil PD856, PRC mechanical/electrical/sanitary pages, PSME PME Code listing, PRC sanitary 2023 referral resolution, NPC CCTV 2024 circular, ASHRAE controls/HVAC, and CEDIA smart-home framing.
