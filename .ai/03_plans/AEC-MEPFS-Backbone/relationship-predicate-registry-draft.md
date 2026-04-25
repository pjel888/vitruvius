---
task: aec-mepfs-backbone
phase: readiness-predicate-registry
created: 2026-04-25
author: CODEX
status: ACCEPTED-READINESS-CONTROL
---

# Relationship Predicate Registry Readiness Spec

## Purpose

This readiness spec records the first-slice predicate vocabulary that later runtime
implementation must promote into the executable relationship registry.

This is not the runtime `relationship_registry.yaml`. It authorizes no graph
rewrite, Neo4j mutation, or relationship enrichment job.

Accepted-readiness scope: the predicate families, anti-vague-edge rule, and
record-field requirements are accepted as planning controls. Runtime promotion
still requires executable registry files, owners for each predicate, examples,
non-examples, validation rules, and migration behavior.

S6 materialized the first candidate predicate registry at
`.ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/predicate-registry.json`.
That file is validator-ready but not steward-admitted or runtime-consumed.

## Governance Rule

Only registered, typed, directional predicates may be used for canonical or
cross-domain edges. Vague relationships such as `RELATED_TO`, `CONNECTED_TO`,
`SIMILAR_TO`, and unqualified `affects` are rejected for governed edges.

`related_to` may exist only as temporary review-state vocabulary inside staging
workbooks. It must be resolved into a typed predicate or rejected before
canonical admission.

## First-Slice Predicate Families

| Predicate | Direction | Category | First-slice use | Promotion gate |
|---|---|---|---|---|
| `broader_than` | parent -> child | hierarchy | taxonomy/tree projection | steward-approved hierarchy |
| `narrower_than` | child -> parent | hierarchy | taxonomy/tree projection | generated inverse or validated pair |
| `part_of` | part -> whole | composition | system, assembly, document, and process composition | source evidence or steward rule |
| `governs` | authority/rule -> concept/context | applicability | legal, standard, or policy control | source-rights and jurisdiction review |
| `requires` | requirement -> required item/action | applicability | obligations, required submissions, required systems | evidence span and operator semantics |
| `constrains` | constraint -> constrained concept | applicability | limits, prohibitions, dimensional controls, zoning controls | evidence span and operator semantics |
| `applicable_in_jurisdiction` | overlay/rule -> jurisdiction | applicability | jurisdiction scope attachment | PSGC or official jurisdiction source |
| `maps_to_external_standard` | Vitruvius node -> external reference | mapping | standards/classification crosswalk | source-rights review |
| `conflicts_with` | candidate -> candidate | conflict | equal-force incompatible candidates | resolver conflict case |
| `supersedes` | newer -> older | temporal | edition, ordinance, release, or node replacement | effective-date evidence |
| `evidenced_by` | claim/node/edge -> evidence span | provenance | source traceability | evidence anchor exists |
| `has_facet` | node -> facet value | facet | lifecycle, asset, performance, project, standards context | controlled facet value |

## Predicate Record Fields

Every promoted predicate must have:

- predicate ID
- label
- inverse, if any
- source class
- domain and range classes
- direction
- allowed strength classes: explicit, inferred, steward-curated
- required evidence fields
- allowed confidence classes
- review owner
- examples
- non-examples
- validation rule
- migration behavior from legacy predicates

## Historical Failure Constraints

Prior `001-Laws` graph audits found the graph dominated by provenance edges:
`DEFINED_BY` and `SUPPORTED_BY` carried most assertions, while semantic edges
were sparse. The new registry must therefore distinguish:

- provenance edges that explain source support
- applicability edges that express obligations and constraints
- cross-domain edges that explain how concepts interact
- review-state edges that are not admitted into canonical graph truth

The registry must also preserve explicit and inferred edges separately. Inferred
edges cannot outnumber explicit evidence-backed edges without a quality report
flag and steward review.

## Pass / Fail Gate

Pass:

- every first-slice predicate has direction, domain, range, evidence, and owner
  fields before runtime promotion
- vague predicates are rejected or held in review state
- lossy predicate mappings are blocked until a steward accepts the migration
  rule

Fail:

- `RELATED_TO` or equivalent vague predicates are promoted as governed edges
- runtime code invents predicates not listed in an accepted registry
- provenance edges are counted as semantic relationship quality
