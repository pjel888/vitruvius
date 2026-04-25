---
task: taxonomy-first-relationship-quality
phase: 04
created: 2026-04-25
author: PLANNER
status: AMENDED
---

# Taxonomy-First Relationship Quality Audit

## Scope

Audit whether the current laws-only KG relationship quality should be improved against the current shared taxonomy or against the intended taxonomy-governance backbone.

## Evidence

- Latest laws-only KG snapshot: `005_Operational-Intelligence-Layer/graph/kg-v2/20260424T195515Z_kg_v2_unified.json`.
- Snapshot shape:
  - 313 canonical nodes
  - 88 concepts
  - 214 rules
  - 432 relationship assertions
  - 734 fast edges
- Relationship assertions:
  - `DEFINED_BY`: 214
  - `SUPPORTED_BY`: 214
  - `REQUIRES`: 3
  - `RELATED_TO`: 1
- Semantic relationship assertions: 4 total.
- Concept taxonomy coverage: 88/88 concepts have `taxonomy_path`.
- Rule taxonomy coverage: 214/214 rules have `taxonomy_path`.
- Current operational taxonomy corpus:
  - `003_Canonical-Knowledge-Layer/shared/taxonomy/`: 11 root files
  - `003_Canonical-Knowledge-Layer/shared/topics/`: 23 topic files
  - `003_Canonical-Knowledge-Layer/shared/subtopics/`: 54 subtopic files
  - `003_Canonical-Knowledge-Layer/shared/concepts/`: 88 concept files
- `scripts/vitruvius/kg/evidence_materializer.py::TaxonomyLoader` loads `shared/taxonomy/*.md` and `shared/concepts/*.md`.
- `scripts/vitruvius/kg/neo4j_loader.py` virtualizes `Topic` and `Subtopic` nodes from `taxonomy_path` arrays.
- `config/vitruvius.yaml` currently has:
  - `k_taxonomy_v2: false`
  - `k_vitruvian_context: false`
  - `k_backbone_validation: false`
- `003_Canonical-Knowledge-Layer/backbone/` is absent.
- Taxonomy-governance planning states the governed backbone is the intended architecture, but the backbone gate is not ready.

## Findings

### Finding 1 - Relationships Are Structurally Valid But Semantically Thin

The current graph is dominated by provenance/structure edges (`DEFINED_BY`, `SUPPORTED_BY`). This is useful for auditability but weak for Explorer reasoning because it does not explain how regulatory concepts constrain, require, affect, or depend on each other.

### Finding 2 - Current Taxonomy Is Operational, Not Final Architecture

The current shared taxonomy is live and useful as migration evidence, but it is not the latest intended taxonomy-governance backbone. The intended backbone lives in the taxonomy-governance design, is feature-flagged off, and has no committed `backbone/` corpus yet.

### Finding 3 - Turning On Taxonomy V2 Is Not A Flag Flip

The latest taxonomy cannot be safely "turned on" by changing `k_taxonomy_v2` alone because the required backbone files and validation/runtime path are not present. A flag flip would imply a runtime architecture that the repository has not admitted.

### Finding 4 - Pre-Launch Means Replace Legacy, Not Preserve It

Because Vitruvius is pre-launch, the current shared taxonomy should not be accommodated as a backward-compatibility product contract. It should either be:

- migrated into the intended governed backbone, or
- treated as temporary source material until the governed backbone is admitted.

### Finding 5 - Relationship Enrichment Should Wait For Or Target The Governed Taxonomy

Improving semantic relationships against the current taxonomy as a long-term surface risks rework. The better path is taxonomy-first:

1. admit or build the intended backbone taxonomy,
2. map existing concepts/rules to it,
3. then generate and review richer relationship candidates using that backbone.

### Finding 6 - Explorer MVP Needs A Temporary Concept-Centric Overlay

Operator feedback after this audit made the short-term priority explicit: do not
rebuild `001-Laws`, but improve the already-loaded Explorer graph so it behaves
per concept rather than per document fragment. The implemented MVP overlay is
therefore acceptable only under these constraints:

- it uses existing derived artifacts, not a raw/canonical rebuild
- it marks new deterministic relationships as review-required candidates
- it keeps document provenance in evidence/support edges
- it does not enable `k_taxonomy_v2` or claim the governed backbone is ready

The immediate fragmentation cause was confirmed: source pages such as
`spp-doc-205.md` declared `concept-standards-of-professional-practice`, but that
source-reference signal was not materialized into the KG. The Explorer therefore
showed document/evidence fragments without enough concept-level assembly.

## Stop Conditions

- Do not bulk-validate the current shallow relationship set.
- Do not mark `k_taxonomy_v2` active without committed backbone files and validation evidence.
- Do not maintain two taxonomy systems as equal runtime surfaces.
- Do not use vague `RELATED_TO` as the primary enrichment predicate.
