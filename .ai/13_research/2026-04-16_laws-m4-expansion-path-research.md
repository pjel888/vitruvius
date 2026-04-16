# Research Pack — Laws M4 Expansion Path

## Purpose
Define the smallest truthful M4 expansion model after the bounded four-folder pilot succeeded and M3 orchestration became reproducible.

## Fresh starting truth
Current bounded official state:
- `PD-1096` → covered
- `RA-9514` → covered
- `BP-344` → covered
- `BP-220` → covered

Current reusable building blocks already in repo:
- manifest loader / scoped reporting:
  - `scripts/vitruvius/graph/dataset_manifest.py`
- scoped graph build:
  - `scripts/vitruvius/graph/cli.py`
- scoped query / provenance:
  - `scripts/vitruvius/query/cli.py`
- bounded orchestration:
  - `scripts/vitruvius/dataset_pipeline.py`
- section-aware extraction:
  - `scripts/vitruvius/relationships_sections.py`
- dataset-safe stage wiring:
  - extraction / review / second-pass / promotion explicit path selection

## M4 deliverables in the governing laws plan
- per-law repetition model
- per-section graph model
- merged-graph collision/provenance rules

## Current gaps
### Per-law repetition
Missing explicit repeatable law-unit schema in the manifest layer.
The current manifest works, but it is still bundle-shaped rather than law-unit-shaped.

### Per-section graphing
Current system preserves section evidence, but there is no explicit section scope contract in the manifest or graph build path.
The safest first model is evidence-scoped section filtering, not a new section-node ontology.

### Merged graph rules
Current node IDs are already canonical and mostly stable, but merged multi-slice behavior still lacks explicit written rules for:
- identical node reuse
- relationship provenance accumulation
- authoritative-variant conflicts
- merged snapshot selection/freshness semantics

## Recommended smallest truthful M4 model
### 1. Per-law repetition model
A dataset manifest should be able to describe repeated law units, each with:
- `law_id`
- `folder_name`
- `raw_anchor_paths`
- `authoritative_variant_paths`
- `excluded_variant_paths`
- `admitted_source_paths`
- `admitted_concept_paths`
- `admitted_relationship_paths`
- `verification_checks`
- `scope_notes`

This makes adding the 5th or 6th law a manifest edit plus bounded admission work, not a custom bundle rewrite.

### 2. Per-section graph model
Use section scope as **evidence filtering**, not new truth-bearing section nodes.
Recommended first contract:
- manifest field like `section_scope`
- explicit allowed `source_id` + `section_id` set
- section-scoped graph snapshots built by filtering existing admitted edges / regulatory basis entries
- section provenance echoed in snapshot metadata and query output

### 3. Merged-graph collision/provenance rules
Merged graphs should keep canonical IDs stable and add provenance, not rename truth.
Rules:
- same canonical node ID across slices = same node, never duplicated
- same relationship evidence ID across slices = same edge, dedupe by evidence ID
- conflicting variants for the same law/IRR must be resolved before merge, not during merge
- merged snapshots must carry contributing manifest hashes / run IDs / law unit list
- merged query/export must always state which merged snapshot was selected

## Design boundary
The truthful first M4 slice is mostly **contract/model work**, not broad new runtime expansion.
Runtime work should stay additive and only implement the schema/provenance features required by those models.
