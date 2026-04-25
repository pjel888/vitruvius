---
task: aec-mepfs-backbone
phase: audit
created: 2026-04-25
author: CODEX
status: drafted
research:
  - .ai/03_plans/AEC-MEPFS-Backbone/2026-04-25_aec_mepfs_backbone_knowledge_graph_research.md
---

# AEC-MEPFS Backbone Architecture Audit

## Scope

Audit whether the current KG/taxonomy architecture can support the operator's
requested standards-backed AEC master taxonomy/knowledge graph, and identify the
blast radius of preparing for that overhaul.

## Current Repo Reality

- The current KG v2 is taxonomy-centered, but it is not yet backed by a governed
  `003_Canonical-Knowledge-Layer/backbone/` corpus.
- The current shared taxonomy corpus is operational:
  - `003_Canonical-Knowledge-Layer/shared/taxonomy/`
  - `003_Canonical-Knowledge-Layer/shared/topics/`
  - `003_Canonical-Knowledge-Layer/shared/subtopics/`
  - `003_Canonical-Knowledge-Layer/shared/concepts/`
- `003_Canonical-Knowledge-Layer/backbone/` is absent.
- `config/vitruvius.yaml` still has `k_taxonomy_v2: false` and
  `k_backbone_validation: false`.
- `TaxonomyLoader` loads roots and concepts from `shared/`, then unified snapshot
  building layers sources, rules, and generated relationships around that data.
- `CanonicalNode.taxonomy_path` is useful as a migration field but too weak for a
  full AEC-MEPFS Backbone because it is a list of labels, not governed typed
  placement.
- `RelationshipAssertion` is strong enough to remain part of the future design
  because it already separates assertions, reasoning, evidence, and review state.

## Findings

### Finding 1 - The Operator's Proposed Direction Matches The Existing Target

The 2026-04-25 relationship-quality audit already concluded that relationship
quality should target the governed taxonomy/backbone rather than permanently
enriching the current shared taxonomy. The new operator note broadens that target
from laws-only graph quality into the core AEC product architecture.

### Finding 2 - The Current Runtime Is Document-Influenced, Not Backbone-First

The current unified snapshot builder materializes taxonomy/concepts, then source
evidence, rules, and relationships. That is acceptable for the MVP overlay, but
it is backwards for the intended architecture. The future graph should start with
the authored AEC-MEPFS Backbone, then classify documents/rules/chunks into it.

### Finding 3 - A Single Tree Will Fail At AEC Scale

AEC concepts are multi-axis. Le Corbusier is a person, an architect, a modernist
figure, a writer, and a collaborator on works involving engineers and contractors.
Modern architecture is a movement/style/history topic and also relates to
materials, structures, urbanism, regulatory changes, and construction methods.

The product needs a graph with tree projections. The tree is for navigation; the
graph is the truth model.

### Finding 4 - External Standards Should Be Crosswalks, Not The Internal Schema

ISO 12006 is a framework, IFC is an exchange schema, bSDD is a dictionary service,
and CSI/Uniclass/CCI are classification systems. None of them alone is the whole
Vitruvius product ontology.

Vitruvius should own stable canonical IDs and map to external standard systems
with versioned `StandardMapping` records.

### Finding 5 - Document Metadata Should Be A Read Model, Not Canonical Node State

Putting all documents "under" a node as embedded node metadata will bloat nodes,
make updates expensive, and blur provenance. The durable model should store:

- canonical backbone node
- document/rule/chunk classification assertion
- evidence/support edge
- materialized counts and summaries for Explorer display

Explorer can show document counts and top sources without making source documents
part of the canonical node definition.

### Finding 6 - The Current Assertion Layer Is A Strength

The future architecture should keep the assertion/evidence/review separation. The
problem is not that assertions exist; the problem is that the backbone they are
asserting against is not yet admitted.

## Blast Radius

Likely impacted surfaces if this plan proceeds to implementation:

- `003_Canonical-Knowledge-Layer/backbone/`: new canonical source of truth
- `003_Canonical-Knowledge-Layer/shared/*`: migration input, not peer runtime
- `scripts/vitruvius/kg/schemas.py`: `BackboneNode`, facets, mappings,
  document classification records
- `scripts/vitruvius/kg/evidence_materializer.py`: replace/shared taxonomy loader
  path with backbone-first loader
- `scripts/vitruvius/kg/unified_snapshot_builder.py`: build from backbone before
  evidence/rules
- `scripts/vitruvius/kg/neo4j_loader.py`: labels, constraints, indexes, shadow
  graph support
- `api/index.ts`: v2 taxonomy/search/node routes and backbone projections
- `explorer/src/*`: tree projection, graph projection, facet filters, evidence
  panels, standard mapping display
- `config/vitruvius.yaml`: feature flags remain false until shadow validation
  passes
- tests under `scripts/tests/`, `api/*.test.ts`, and `explorer/src/**/*.test.tsx`

## Risks

- Copying a third-party standard too directly can create licensing and
  maintainability problems.
- A tree-only model will fragment people, works, movements, systems, materials,
  and engineering topics.
- AI-generated top-level taxonomy changes would destabilize the product.
- Premature cutover would break the current Explorer MVP.
- Large node payloads would hurt Neo4j and API performance.
- Vague predicates such as `RELATED_TO` would produce another shallow graph.

## Stop Conditions

- Do not enable `k_taxonomy_v2` without committed backbone files and validators.
- Do not treat the current shared taxonomy as the final architecture.
- Do not import copyrighted classification tables wholesale without license
  review.
- Do not place jurisdiction-specific meanings in global backbone node
  definitions.
- Do not start runtime implementation until a bounded backbone execution packet
  is accepted.

## Audit Verdict

Proceed with a backbone-first architecture plan. Do not rebuild or re-enrich the
current laws graph as the next architecture step. The next safe move is to admit a
standards-aligned AEC-MEPFS Backbone plan, then implement a validator and shadow graph
before any feature flag cutover.
