---
task: aec-mepfs-backbone
phase: plan
created: 2026-04-25
author: CODEX
status: proposed
research:
  - .ai/03_plans/AEC-MEPFS-Backbone/2026-04-25_aec_mepfs_backbone_knowledge_graph_research.md
audit:
  - .ai/03_plans/AEC-MEPFS-Backbone/2026-04-25_aec_mepfs_backbone_architecture_audit.md
related:
  - .ai/03_plans/AEC-MEPFS-Backbone/2026-04-25_aec_mepfs_backbone_readiness_plan.md
  - .ai/03_plans/AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md
  - .ai/03_plans/taxonomy-governance/00_locked_decisions.md
  - .ai/03_plans/taxonomy-governance/03_implementation_plan.md
  - .ai/03_plans/2026-04-25_taxonomy_first_relationship_quality_plan.md
---

# AEC-MEPFS Backbone Architecture Overhaul Plan

## Requirements Summary

Prepare Vitruvius for a major architecture shift: build a standards-aligned,
authored AEC-MEPFS Backbone knowledge graph first, then classify source
documents, rules, chunks, and evidence onto that backbone. The backbone must
support the whole AEC domain, including architecture, civil engineering,
structural, electrical, mechanical, plumbing, fire protection, sanitary systems,
construction, project practice, codes, standards, history, people, works,
materials, systems, and cross-discipline relationships.

This plan does not start runtime implementation. It creates the architecture
direction that must pass the AEC-MEPFS Backbone readiness gates before any
implementation lane opens.

The readiness plan is the controlling gate for this architecture plan. Until it
reaches `ready for bounded implementation`, this plan authorizes no source-code
edits, Neo4j cleanup/reset, feature-flag changes, graph rebuilds, backup test
runs, or derived-artifact cleanup.

The AECMEPFS++ research reports are now integrated as planning evidence. They
strengthen the backbone-first direction, but they are not canonical corpus:
their proposed trees, standard-version claims, source lists, and implementation
schedule must pass the readiness gates before admission.

## Operator Intent Captured

The requested product shape is:

- not a graph primarily derived from the currently ingested data
- an AEC organizational backbone based on actual AEC standards and practice
- a taxonomy tree that also behaves as an interconnected knowledge graph
- document classification after the master taxonomy/graph exists
- document metadata visible under relevant nodes without making nodes bloated
- optimized, efficient storage and query paths
- enough breadth for all of AEC and enough graph richness for concepts like
  Modern Architecture, Le Corbusier, collaborators, engineers, works, and
  discipline crossings

## Decision

Adopt a backbone-first architecture for the next AEC planning lane.

The canonical AEC-MEPFS Backbone should be authored in
`003_Canonical-Knowledge-Layer/backbone/`, validated before runtime use, loaded
into a shadow graph first, and then used as the classification substrate for
documents and relationship enrichment.

## Architecture Principles

- The backbone is authored canonical knowledge, not extracted output.
- The tree is a navigation projection; the real model is a typed graph.
- External standards are mapped as crosswalks, not copied as internal canonical
  identity.
- L1-L2 backbone structure is human-locked.
- AI can classify and propose lower-level additions, but cannot mutate the
  governed backbone without review.
- Documents attach through classification/evidence assertions, not embedded node
  blobs.
- Explorer uses materialized read models for counts and summaries.
- No vague cross-domain `RELATED_TO` edges.

## Target Model

### Layer 1 - AEC-MEPFS Backbone Graph

Canonical nodes for:

- domains and disciplines
- subjects and concepts
- people
- organizations
- works/projects
- styles and movements
- systems
- components
- materials
- processes and methods
- codes, standards, and regulatory families
- roles and lifecycle phases

The backbone should include hierarchy edges such as:

- `HAS_CHILD`
- `BROADER_THAN`
- `NARROWER_THAN`
- `PART_OF`
- `HAS_FACET`

And semantic edges such as:

- `INFLUENCED_BY`
- `DESIGNED_BY`
- `ENGINEERED_BY`
- `COLLABORATED_WITH`
- `USES_MATERIAL`
- `REGULATED_BY`
- `REQUIRES`
- `CONSTRAINS`
- `APPLIES_TO`
- `PRECEDES`
- `DERIVED_FROM`

### Layer 2 - Standards Mapping

External systems are represented through versioned mappings:

- ISO 12006-2 / ISO 12006-3 as framework references
- buildingSMART bSDD for dictionary/class/property mappings
- IFC for exchange-object mappings
- CSI MasterFormat, UniFormat, and OmniClass as classification crosswalks
- Uniclass and CCI as classification crosswalks
- jurisdictional codes and standards as authority/document mappings

Mappings must include:

- `system`
- `code`
- `title`
- `version`
- `uri`
- `mapping_type`
- `confidence`
- `mapped_by`
- `source_license_note`

### Layer 3 - Document Classification

Documents, document editions, extraction versions, chunks, rules, and evidence
spans classify into the backbone through assertions:

- `CLASSIFIED_AS`
- `MENTIONS`
- `DEFINES`
- `SUPPORTED_BY`
- `DERIVED_FROM_SOURCE`
- `APPLIES_IN`

The canonical node should not own large document lists. Instead:

- canonical assertions store exact provenance
- Neo4j stores traversal edges
- PostgreSQL/JSON reports can store tabular audit views
- Explorer gets materialized counts and top-source summaries

### Layer 4 - Explorer Read Model

Explorer should show:

- tree projection for navigation
- graph projection for relationships
- facet filters
- standards mappings
- evidence counts
- source/rule counts
- top supporting documents
- edge provenance and review state

The Explorer should not force users to inspect raw document fragments just to
understand a concept. Document evidence should be available when needed, but the
primary experience should be concept-first.

## Initial Backbone Shape

Use a hybrid seed:

1. breadth-first L1-L2 skeleton across the whole AEC domain
2. deeper L3-L4 vertical slice for Architecture + Structural + Building Systems
   + Codes/Standards + Project Practice
3. standards mappings only where license and source quality are safe
4. explicit stubs where the taxonomy is intentionally incomplete

Candidate L1 domains:

- `ARC` - Architecture and Interior Design
- `URB` - Site Planning, Urban Design, and Landscape
- `CIV` - Civil and Transportation Infrastructure
- `STR` - Structural and Seismic Engineering
- `GEO` - Geotechnical and Underground Engineering
- `MEC` - Mechanical, Thermal, and Refrigeration
- `ELE` - Electrical, Lighting, and Power
- `PLS` - Plumbing, Sanitary, and Public Health
- `FLS` - Fire Protection, Fire Suppression, and Life Safety
- `SEC` - Security, Communications, and Smart Building Systems
- `CON` - Construction, Methods, and Temporary Works
- `MAT` - Materials, Products, and Fabrication
- `COM` - Law, Codes, Standards, and Compliance
- `PER` - Sustainability, Resilience, and Building Performance
- `DIG` - Digital Delivery, BIM, GIS, and Computation
- `OPS` - Operations, Maintenance, and Asset Management
- `HIS` - History, Theory, Typologies, and Precedent
- `FIG` - People, Organizations, Works, and Awards

The first sixteen domains are candidate operational domains. `HIS` and `FIG`
are candidate auxiliary knowledge-commons domains: they matter for precedent,
retrieval, learning, and relationship exploration, but they must not become the
default home for compliance truth.

The larger AECMEPFS++ tree is a candidate authoring corpus, not a canonical
import. The first-slice model spec must decide which branches become governed
L1-L2 backbone, which become lower-level candidates, and which remain deferred.

Orthogonal facets should remain reusable dimensions rather than uncontrolled
top-level trees:

- lifecycle stage
- asset type
- performance topic
- geography/jurisdiction
- knowledge type
- standards context

## Implementation Phases

### Phase 0 - Standards And Backbone Decision Packet

Deliverables:

- this plan
- standards source matrix
- updated active plan index
- operator decision on seed strategy

Exit gate:

- accepted backbone-first direction and selected seed strategy
- AEC-MEPFS Backbone readiness scorecard remains the active gate before any
  runtime implementation starts

### Phase 1 - Backbone Schema Freeze

Deliverables:

- `BackboneNode` schema
- `FacetAssignment` schema
- `StandardMapping` schema
- `DocumentClassification` schema
- relationship predicate registry update
- validation rules for IDs, parentage, cycles, steward fields, and external refs

Exit gate:

- schema tests pass
- no unregistered predicates
- no feature flag cutover
- locked taxonomy-governance decisions are preserved: Layer-3 backbone source of
  truth, `VTN-<kind>-<7 digits>` IDs, no jurisdiction forks, additive `/v2`, old
  ID redirects, and shadow-first rollout

### Phase 2 - Authored Backbone Seed

Deliverables:

- `003_Canonical-Knowledge-Layer/backbone/`
- L1-L2 AEC skeleton
- L3-L4 vertical slice
- steward notes and source notes
- standards mapping seed

Exit gate:

- backbone validator passes
- human-locked L1-L2 nodes are explicitly reviewed

### Phase 3 - Shadow Graph Loader

Deliverables:

- backbone-first snapshot builder
- shadow Neo4j labels or shadow database
- full-text/facet indexes
- quality report for node counts, orphan nodes, cycles, duplicate labels,
  external mappings, and relationship predicates

Exit gate:

- shadow graph loads cleanly
- Explorer/API v1 remains untouched

### Phase 4 - Existing Knowledge Mapping

Deliverables:

- mapping from existing shared concepts to backbone nodes
- mapping from existing 001-Laws rules/sources to backbone nodes
- redirect/migration evidence
- classification confidence and review queues

Exit gate:

- existing Explorer MVP remains available
- no old canonical IDs disappear

### Phase 5 - Vitruvian Context Resolver And Overlay Contract

Deliverables:

- deterministic resolver spec
- precedence engine rulebook
- resolver API contract
- resolver golden tests
- Philippines overlay pilot method
- no-LLM-hot-path rule

Exit gate:

- resolver behavior is specified before implementation
- equal-force conflicts return traceable `conflict_set` outputs
- jurisdiction overlays are modeled separately from canonical backbone meaning

### Phase 6 - Backbone-Aware Relationship Enrichment

Deliverables:

- candidate semantic edges using closed predicate families
- evidence-backed concept-to-concept and concept-to-document assertions
- no untyped `RELATED_TO` enrichment
- quality report separating structural, classification, semantic, and evidence
  relationships

Exit gate:

- semantic density improves without reducing provenance quality

### Phase 7 - Explorer Backbone Experience

Deliverables:

- backbone tree panel
- graph projection mode
- facet filters
- standards mapping display
- evidence/source summaries
- edge inspector provenance

Exit gate:

- users can navigate concept-first and inspect documents only when needed

### Phase 8 - Performance And Scale Hardening

Deliverables:

- precomputed ancestor/descendant closure
- adjacency indexes
- materialized source/rule counts
- benchmark report for snapshot build, Neo4j load, API search, and Explorer
  initial render

Exit gate:

- target latency budgets are met before cutover

## Acceptance Criteria

- A committed `backbone/` corpus exists before `k_taxonomy_v2` is enabled.
- The graph can be rendered as both tree and graph projections.
- Every semantic relationship is typed, directional, and evidence-backed or
  explicitly authored.
- Documents/rules/chunks attach through classification/evidence assertions.
- Node payloads remain small; document lists are materialized summaries, not
  canonical node state.
- External standards mappings store version/source metadata.
- Existing `001-Laws` MVP graph is not broken during shadow work.
- Explorer can explain why a node or edge exists.
- The deterministic Vitruvian Context resolver contract exists before runtime
  resolver implementation.
- AECMEPFS++ research tree branches are reviewed through steward/source gates
  before canonical admission.
- Philippines legal, standards, project, and hazard context are modeled as
  overlays, not as a second taxonomy.

## Verification Plan

- schema unit tests for backbone nodes, facets, standard mappings, and document
  classification assertions
- validator tests for duplicate IDs, invalid parent references, cycles, missing
  stewards, and unknown predicates
- snapshot tests for deterministic graph output
- Neo4j load tests for shadow graph
- API contract tests for v1 preservation and v2 backbone routes
- resolver contract tests for deterministic precedence, conflict sets, and trace
  output
- Explorer tests for tree projection, graph projection, facet filters, and
  evidence panels
- performance checks for snapshot build, Neo4j load, API search latency, and
  Explorer render behavior

## Risks And Mitigations

- Risk: taxonomy expands too broadly before it is governed.
  Mitigation: freeze L1-L2, use stubs below that, and require validator gates.

- Risk: third-party classification licensing limits seed data.
  Mitigation: store external references and sample mappings only until license
  review clears broader ingestion.

- Risk: tree navigation hides graph truth.
  Mitigation: define tree as a projection and keep semantic edges first-class.

- Risk: document metadata bloats nodes.
  Mitigation: store source links as assertions and materialize only counts and
  summaries for Explorer.

- Risk: AI generates taxonomy drift.
  Mitigation: AI classifications are candidate assertions; backbone mutations go
  through review.

- Risk: resolver answers become AI-generated runtime truth.
  Mitigation: no LLM in the hot-path resolver; use deterministic precedence,
  trace output, and conflict sets.

- Risk: the AECMEPFS++ tree is copied in as canonical because it is broad.
  Mitigation: keep it as a candidate authoring corpus until the L1-L2 decision,
  source-rights, and steward gates pass.

## Recommended Next Decision

Use a hybrid seed strategy: breadth-first L1-L2 across AEC, plus a deep vertical
slice around Architecture, Structural, Building Systems, Codes/Standards, and
Project Practice. This is the smallest path that proves the architecture without
pretending the whole AEC graph is already complete.
