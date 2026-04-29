# Targeted Taxonomy Semantic Enrichment Research

Date: 2026-04-29  
Run id: 20260429T065436Z  
Mode: Kimi-assisted advisory synthesis plus human steward integration  
Scope: rights-safe metadata-only AEC-MEPFS taxonomy enrichment

## Research question

After broad scaffold replacement, the AEC-MEPFS backbone still had weak semantic connections between discipline topics and standards/source-family context. The target was not to ingest standards text. The target was to add durable taxonomy nodes, aliases, source-family provenance, and typed relationships that improve findability and cross-domain reasoning.

## Repository baseline inspected

- Source-of-truth file-backed backbone fixture: `scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json`
- Previous run: `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260429T015840Z/`
- Previous graph counts: 8935 BackboneNode records, 8911 `broader_than` edges, 24 roots, max depth 4
- Existing source rights registry: `.ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-rights-registry.json`
- Existing constraints: L1-L4 path depth, three-character path segments, admitted nodes require `path_code`, `parent_path_code`, owner/steward, and deterministic identifiers.

## Kimi-assisted advisory synthesis

Kimi CLI was used for model-assisted taxonomy target selection and source-family/edge-pattern synthesis. Codex Spark was not used for research or taxonomy synthesis.

Kimi advisory conclusions:

1. Highest-impact expansion targets should be domains that already exist in the graph and benefit from authoritative public standards-family anchors: HVAC/mechanical, electrical/ICT, fire/life safety, plumbing/sanitary, security/smart systems, heritage, sustainability, and operations.
2. Source-family nodes should be metadata crosswalks, not content-ingest records.
3. Relationship predicates should stay within the existing governed predicate registry where possible: `broader_than`, `part_of`, `has_facet`, `constrains`, `maps_to_external_standard`, and `requires`.
4. Added nodes should be concrete engineering, operations, conservation, or standards-reference concepts, not scaffolds or generic placeholders.

## Public source-family references used as metadata anchors

The enrichment uses source-family labels and official landing-page URLs only. No standards clauses, tables, figures, diagrams, or publication text were ingested.

- ASHRAE Standard 90.1 and related ASHRAE standards/guidelines pages: https://www.ashrae.org/technical-resources/bookstore/standard-90-1, https://www.ashrae.org/technical-resources/bookstore/standards-62-1-62-2, https://www.ashrae.org/news/esociety/updated-commissioning-guideline
- NFPA codes and standards landing page: https://www.nfpa.org/for-professionals/codes-and-standards
- ICC 2024 I-Codes landing page: https://www.iccsafe.org/products-and-services/i-codes/2024-i-codes/
- TIA and BICSI standards landing pages: https://tiaonline.org/what-we-do/standards/, https://www.bicsi.org/standards
- NIST Cybersecurity Framework and IoT program pages: https://www.nist.gov/cyberframework, https://www.nist.gov/itl/applied-cybersecurity/nist-cybersecurity-iot-program
- WHO sanitation safety planning page: https://www.who.int/teams/environment-climate-change-and-health/water-sanitation-and-health/sanitation-safety/sanitation-safety-planning
- ICOMOS charters and doctrinal texts page: https://www.icomos.org/en/resources/charters-and-texts
- ISO public landing pages for ISO 14040, ISO 14044, ISO 41001, and ISO 55001: https://www.iso.org/standard/37456.html, https://www.iso.org/standard/38498.html, https://www.iso.org/standard/68021.html, https://www.iso.org/standard/55089.html
- IES standards and lighting library pages: https://ies.org/standards/, https://ies.org/standards/lighting-library/
- ASCE and FEMA public reference pages for seismic/resilience families: https://www.asce.org/publications-and-news/asce-7, https://www.asce.org/publications-and-news/asce-41, https://www.fema.gov/emergency-managers/risk-management/building-science/earthquake/publications

## Enrichment targets selected

### Standards-family spine

Added standards/guidance family nodes under `COM.STD` for:

- ASHRAE
- NFPA
- TIA/BICSI
- ICC I-Codes
- WHO WASH
- NIST cybersecurity
- ICOMOS conservation doctrine
- IES lighting

Also enriched the existing `COM.STD.ISO` branch with ISO LCA, facility-management, asset-management, environmental-management, and energy-management reference nodes.

### Discipline topic branches

Added discipline topics under existing L3 parents where a standards-family crosswalk materially improves retrieval and reasoning:

- Mechanical: chilled-water optimization, outdoor air/IAQ, energy-recovery ventilation, thermal comfort
- Electrical: transformer coordination, grounding/bonding, emergency power, structured cabling
- Fire/life safety: smoke control, fire alarm cause/effect, sprinklers, standpipes
- Plumbing and sanitary: backflow prevention, water quality, sanitary drainage, public-health risk controls
- Security and smart systems: video analytics, IoT device identity, certificates, asset inventory
- Heritage: reversible fixings, like-for-like repair, intervention logs, conservation mockups
- Sustainability: LCA goal/scope, life-cycle inventory, impact categories, critical review
- Operations: asset naming, warranty capture, COBie mapping, asset criticality

## Disambiguation and quality rules

- Keep all new `path_code` segments to three characters to satisfy the admitted BackboneNode schema.
- Keep depth at L4 or shallower.
- Use metadata-only `source_family_ids` and `provenance_note` fields.
- Preserve aliases/acronyms such as NEC, LSC, NFPA 72, ANSI/TIA-568, NIST CSF, LCA, LCI, COBie, LPR, ANPR, RPZ, DCV, DOAS, ERV, and WASH.
- Avoid broad generic buckets like `Miscellaneous`, `Advanced Topic 1`, `TBD`, `Concepts`, `Concept Anchor`, `Rule Context`, and `Topics`.

## Research result

The research supports a targeted metadata graph enrichment rather than a code-only refactor. The resulting fixture added 141 real BackboneNode records, 415 governed relationships, 749 aliases on new/improved nodes, and 12 source-rights registry references while preserving read-only/file-backed boundaries.
