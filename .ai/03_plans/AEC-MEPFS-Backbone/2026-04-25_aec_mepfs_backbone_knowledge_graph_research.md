---
task: aec-mepfs-backbone
phase: research
created: 2026-04-25
author: CODEX
status: drafted
---

# AEC-MEPFS Backbone Knowledge Graph Research

## Research Question

Should Vitruvius prepare for a major architecture shift where the first-class
knowledge graph is an authored, standards-aligned AEC taxonomy/ontology backbone,
and document-derived knowledge is classified onto that backbone afterward?

## Operator Intent

The operator's stated direction is to build a massive interconnected AEC taxonomy
tree/knowledge graph first, based on actual AEC organizational standards rather
than derived from the currently ingested documents. That backbone should cover
Architecture, civil engineering, electrical, mechanical, construction practice,
codes, history, people, works, systems, and cross-discipline relationships. After
that backbone exists, documents should be classified under it and additional
relationships should be layered on top.

The operator also raised an implementation concern: document metadata may need to
be visible under backbone nodes, but the system must remain optimized and
efficient.

## Repo Evidence

- `README.md` defines Vitruvius as a local-first, governance-first knowledge
  pipeline and identifies `003_Canonical-Knowledge-Layer/` as "The Brain."
- `README.md` describes KG v2 as a taxonomy-centered canonical graph with a
  separate evidence layer and reified assertions.
- `.ai/00_system/principles.md` requires explicit concept vocabulary, no
  schema-less growth, and pre-launch truth over legacy accommodation.
- `.ai/02_audits/2026-04-25_taxonomy_first_relationship_quality_audit.md`
  states that the current shared taxonomy is operational but not the intended
  governed backbone.
- `.ai/03_plans/2026-04-25_taxonomy_first_relationship_quality_plan.md`
  already names the taxonomy-first rebuild path as the long-term target.
- `003_Canonical-Knowledge-Layer/backbone/` is absent.
- `003_Canonical-Knowledge-Layer/shared/taxonomy/` currently has 11 root files.
- `scripts/vitruvius/kg/evidence_materializer.py::TaxonomyLoader` currently
  loads shared taxonomy roots and shared concepts, not a governed backbone.
- `scripts/vitruvius/kg/schemas.py::RelationshipAssertion` already supports
  reasoning summaries, reasoning detail, evidence spans, and review state. That
  assertion model is a good foundation for relationship governance.

## External Standards Findings

### ISO 12006-2

ISO 12006-2:2015 is a framework for developing built-environment classification
systems. It is not itself a full operational classification. It applies across
the whole construction works lifecycle and covers both building and civil
engineering works, including services and landscaping.

Implication: use ISO 12006-2 as a framework influence, not as imported content.

Source: https://www.iso.org/standard/61753.html

### ISO 12006-3

ISO 12006-3:2022 specifies a language-independent model for dictionaries for
construction works. ISO explicitly says instantiated content can serve as
ontology, taxonomy, meronomy, lexicon, and thesaurus, and can cross-reference
classification systems, information models, object models, data templates, and
process models.

Implication: the Vitruvius backbone should be a graph with typed relationship
families, not a single forced tree.

Source: https://www.iso.org/standard/74932.html

### buildingSMART bSDD

The buildingSMART Data Dictionary provides a dictionary structure with dictionary
codes, versions, globally unique URIs, classes, parent class references,
definitions, properties, units, document references, and status.

Implication: Vitruvius should model external standards mappings with versioned
external references and document references. It should not mutate internal
canonical meaning based on a third-party dictionary entry.

Sources:
- https://www.buildingsmart.org/users/services/buildingsmart-data-dictionary/
- https://standards.buildingsmart.org/DataDictionary/

### buildingSMART IFC

buildingSMART publishes official IFC schema releases and machine-readable forms.
IFC is the correct source for exchange-object semantics, not for the whole
editorial subject taxonomy of the product.

Implication: map Vitruvius backbone nodes to IFC where useful, but do not make IFC
the internal information architecture.

Source: https://technical.buildingsmart.org/standards/ifc/ifc-schema-specifications/

### CSI MasterFormat, UniFormat, and OmniClass

CSI describes MasterFormat, UniFormat, and OmniClass as a connected standards
system for construction's shared language. MasterFormat organizes project
documentation/work results; UniFormat supports building system and lifecycle
classification; OmniClass is intended for AEC electronic databases and BIM
classification.

Implication: these are strong crosswalk targets and seed references, but they are
not enough by themselves for history, theory, people, works, collaborators, and
full international AEC knowledge.

Source: https://www.csiresources.org/standards/overview

### Uniclass

NBS describes Uniclass as a unified classification system for the built
environment across all sectors and roles, with tables for activities, complexes,
elements, entities, equipment, functions, information forms, locations,
products, roles, spaces, systems, tools, and other areas.

Implication: Uniclass validates the need for multiple controlled tables/facets,
not one giant tree where every kind of thing sits at the same level.

Source: https://www.thenbs.com/knowledge/what-is-uniclass

### CCI

Construction Classification International publishes core tables for construction
entities, spaces, functional systems, technical systems, components, and
complexes, and states its core tables are based on ISO 12006-2 and IEC/ISO 81346
standards.

Implication: CCI is a useful open crosswalk candidate for systems/components,
especially if licensing or access limits make CSI tables impractical for broad
seeding.

Source: https://cci-collaboration.org/the-standard/

### ISO 19650

ISO 19650 is about information management across the lifecycle of a built asset,
not the subject backbone itself.

Implication: use ISO 19650 for document/information management metadata,
status/revision/workflow alignment, and CDE-like governance. Do not treat it as
the AEC subject taxonomy.

Source: https://www.iso19650.org/overview-to-iso-19650-series

## Research Synthesis

The operator's instinct is correct, but the durable architecture should not be
"one taxonomy tree." It should be an authored AEC-MEPFS Backbone graph with tree
projections.

The backbone needs:

- stable primary subject hierarchy for human navigation
- controlled facets for lifecycle, asset scope, system/component class,
  material, role, work result, performance topic, knowledge type, jurisdiction,
  and external standard system
- typed cross-domain edges for influence, collaboration, regulation, part-whole,
  dependency, applicability, and evidence
- explicit mappings to external standards with version and license metadata
- document/rule/chunk classification edges into the backbone
- materialized Explorer read models for counts, summaries, and fast display

Documents should not be embedded as large metadata blobs on backbone nodes. The
canonical model should store document relationships as edges/assertions. Explorer
can show node-level aggregate metadata such as `document_count`, `rule_count`,
`top_sources`, and `last_evidence_at` as a materialized read model.

## Recommendation

Create a formal AEC-MEPFS Backbone execution packet before any major code
overhaul.
The first build should be a hybrid:

1. breadth-first L1-L2 skeleton across the whole AEC domain
2. deep vertical slice for Architecture + Structural + MEP/Building Systems +
   Codes/Standards + Project Practice
3. standards mappings as crosswalks, not internal canonical IDs
4. no document-derived enrichment until the backbone validator and shadow graph
   pass
