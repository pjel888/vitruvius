# Architecture Civil Structural Knowledge Graph PRD

Date: 2026-05-01

## Goal
Improve Architecture, Civil Engineering, and Structural Engineering taxonomies so the file-backed Vitruvius graph supports mechanism-based cross-taxonomy reasoning, not just BIM-style object lists.

## Durable work packages

| ID | Status | Outcome |
|---|---|---|
| `kg-arch-audit` | completed | 79 ACS nodes added/refined with Architecture space, access, public-way accessibility interfaces, roof, facade, opening, movement-joint, fire/acoustic/daylight, flood datum, and utility/service-entry interfaces. |
| `kg-civil-audit` | completed | Civil/site coverage expanded for grading, runoff, stormwater conveyance, accessibility grade control, emergency access, utilities, SUE conflict review, flood elevation, LID, and hydrology. |
| `kg-structural-audit` | completed | Structural coverage expanded for load path, load actions, slab/beam/column/foundation, diaphragm, collector, core, connections, movement, retaining, slope stability, temporary works, shoring, and rebar. |
| `kg-cross-taxonomy-edges` | completed | 143 ACS typed non-hierarchy relationships plus 79 hierarchy relationships support traversal across Architecture, Civil Engineering, and Structural Engineering. |
| `kg-provenance` | completed | 123 source-rights rows remain in the registry; introduced ACS edge source-family coverage is 143/143 with metadata-only source-family IDs. |
| `kg-validation` | completed | `backbone_graph_quality` validates source references, relation categories, placeholder strings, global self-loops, same-parent duplicates, duplicate-label samples, introduced non-hierarchy orphans, cycles, and generic predicate/edge_type relationships; gated-review validation now also covers steward duplicate packets, hash-only protected-payload manifests, live-promotion plans, packet path escapes, and generated external-gate readiness skeletons. |
| `kg-traversal-tests` | completed | Tests and reports validate accessible route, roof drainage, foundation/geotech, gravity/lateral load, floor opening, retaining wall, movement-joint, utility conflict, flood elevation, and slope-stability traversals. |
| `kg-quality-score` | completed | ACS quality score report run `20260501T082300Z_ACS_EXTERNAL_GATED_GAP_QUALITY` scores 100/100; graph-quality run `20260501T082200Z_ACS_EXTERNAL_GATED_GAP_GRAPH_QUALITY` passes with 0 self-loops; gated-review runs `20260501T090200Z_ACS_EXTERNAL_GATE_APPLY_PATHS_DRY_RUN` and `20260501T094300Z_ACS_EXTERNAL_GATE_READINESS_BUNDLE` validate the dry-run external-apply/readiness surface with 0 report errors. |

## Boundaries
- File-backed Backbone fixture, source-rights metadata, resolver fixture, tests, docs, and shadow reports only.
- No protected source text, formulas, standard clauses, tables, figures, or images were ingested.
- No production Neo4j/live KG writes, KG rebuild/reset, feature-flag cutover, or canonical source admission.

## External-gated follow-up update

The durable work packages remain complete after the external-gated follow-up. Current file-backed status:

- `kg-arch-audit`: completed with 79 ACS nodes added/refined, including architecture-to-public-way accessibility interfaces.
- `kg-civil-audit`: completed with added public-way crossing, culvert, pavement subgrade, flood/scour, runoff, and stormwater-maintenance reasoning.
- `kg-structural-audit`: completed with an explicit non-numeric Structural Criteria Basis Gate connecting AHJ, risk, seismic applicability, and load concepts.
- `kg-cross-taxonomy-edges`: completed with 143 typed ACS non-hierarchy relationships and 79 ACS hierarchy relationships.
- `kg-provenance`: completed with 143/143 introduced ACS edges carrying source-family IDs; no protected payloads or numeric criteria admitted.
- `kg-validation`: completed with graph-quality, ACS quality, resolver QA, shadow staging, and gated-review checks, including dry-run steward duplicate apply plans, hash-only protected payload manifests, live-promotion plan preflight, external packet path validation, and generated draft readiness skeletons.
- `kg-traversal-tests`: completed with additional public-way, culvert, structural-criteria, and operations-maintenance traversal gates.
- `kg-quality-score`: completed with run `20260501T082300Z_ACS_EXTERNAL_GATED_GAP_QUALITY` at 100/100 and external-gate dry-run/readiness reports through `20260501T094300Z_ACS_EXTERNAL_GATE_READINESS_BUNDLE` at 0 errors.
