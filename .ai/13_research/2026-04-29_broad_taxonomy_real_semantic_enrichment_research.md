# Broad Taxonomy Real Semantic Enrichment Research

Date: 2026-04-29  
Scope: AEC-MEPFS non-Architecture L4 scaffold replacement after the Architecture-first pass.

## Problem

The Architecture branch was corrected first, but the rest of the AEC-MEPFS backbone still contained generic L4 scaffold labels such as `Concepts`, `Concept Anchor`, `Rule Context`, and `Topics`. These labels are not useful taxonomy content for Explorer browsing or resolver grounding.

## Public source signals used for topic calibration

This pass uses rights-safe topic structures only. It does not copy protected clauses, tables, figures, datasets, paid handbook content, or source payloads.

- ABET engineering accreditation criteria: broad civil/environmental/geological/engineering competency structures and outcomes.  
  <https://www.abet.org/accreditation/accreditation-criteria/criteria-for-accrediting-engineering-programs-2026-2027/>
- ASHRAE handbook/topic signals for HVAC fundamentals, systems, equipment, applications, and operations.  
  <https://www.ashrae.org/technical-resources/ashrae-handbook>
- ASPE Plumbing Engineering Design Handbook public description for plumbing engineering design criteria and accepted-practice coverage.  
  <https://aspe.org/publications-news/aspe-plumbing-engineering-design-handbooks/>
- ISO BIM/information-management public standards overview for information requirements, delivery phase, operational phase, information exchange, and lifecycle information management.  
  <https://www.iso.org/sectors/building-construction/building-information-modelling>
- IES lighting fundamentals public course/topic signal for lighting science, visual comfort, color, health, professional practice, and lighting fundamentals.  
  <https://ies.org/event/ies-fundamentals-of-lighting-3-day-course/>
- NFPA public certification/code-family signals for means of egress, fire protection systems, sprinkler systems, alarm systems, deficiencies, inspection, and documentation.  
  <https://www.nfpa.org/-/media/Project/Storefront/Catalog/Files/Certification/CFI/CFI-Practicum-Rubric.pdf>

## Synthesis rule

The non-Architecture scaffold nodes are replaced with concrete discipline children under each existing L3 parent. Labels follow root-specific professional patterns, for example:

- Electrical: load/demand basis, circuiting/protection coordination, equipment schedules, testing/commissioning, isolation.
- Fire/life safety: hazard scenario basis, detection/notification, suppression/control, egress/tenability, inspection/testing/maintenance.
- Digital/BIM: information requirements, common data environment workflow, exchange validation, classification, asset handover.
- Law/compliance: applicability, permit trigger, responsible party obligation, compliance evidence, enforcement/remedy.
- Heritage: significance, fabric condition, intervention compatibility, archival record, maintenance monitoring.

## Safety

- Metadata labels only.
- No protected payloads.
- No source text ingestion.
- No Neo4j mutation.
- No KG rebuild/reload/reset.
- No API/Explorer runtime code change.
