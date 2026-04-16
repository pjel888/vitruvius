# Laws Dataset M4 Expansion Model

## 1. Per-Law Repetition Model
A successful bounded pilot must scale by repeating one law-unit pattern.

### Required law-unit fields
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

### Repetition rule
Adding a new law should require:
1. manifest edit
2. bounded admission work
3. bounded verification

It must not require new bundle-specific code paths.

## 2. Per-Section Graph Model
### First safe model
Section graphs are evidence-scoped snapshots built from already admitted truth-bearing nodes/edges.

### Rules
- section scope filters existing edges by `evidence_source_id` + `evidence_source_section_id`
- concept-basis edges may enter when `regulatory_basis.section_id` matches scope
- no new section nodes are created in the first M4 model
- section scope must be explicit in snapshot metadata

## 3. Merged-Graph Collision / Provenance Rules
### Node collision
- identical canonical node ID across slices = same node
- no per-slice node renaming

### Edge collision
- identical `evidence_id` across slices = same edge
- merged views dedupe by evidence ID

### Variant conflicts
- same-law competing variants must be resolved before merge admission
- merge layer does not decide authority

### Provenance
Merged snapshot metadata must include:
- contributing manifest hashes
- contributing run IDs
- contributing law IDs / law units
- generated_at_utc

### Query rule
Merged query/export must always report which merged snapshot was selected.
