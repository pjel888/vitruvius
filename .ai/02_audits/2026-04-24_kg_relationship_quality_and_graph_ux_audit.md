# KG Relationship Quality and Graph UX Audit — 2026-04-24

## Scope
Audit of the current knowledge-graph relationship pipeline, relationship assertion distribution, taxonomy use, and rule-node naming UX.

## How Relationships Are Made Today

Vitruvius currently has two overlapping relationship tracks:

1. **Legacy promotion track**
   - `scripts/vitruvius/relationships_sections.py` extracts relationship candidates from section-local text windows.
   - `scripts/vitruvius/ollama_review.py` reviews candidates through Ollama / local review.
   - `scripts/vitruvius/promotion/__init__.py` promotes approved candidates into canonical relationship markdown under `003_Canonical-Knowledge-Layer/shared/relationships/`.
   - `scripts/vitruvius/promotion_validator.py` validates promoted relationship records.

2. **KG v2 materialization track**
   - `scripts/vitruvius/kg/evidence_materializer.py` turns canonical relationship markdown into `EvidenceSpan` and `RelationshipAssertion` records.
   - `scripts/vitruvius/kg/rule_extractor.py` rewires source→concept assertions into atomic rule nodes:
     - `concept ──DEFINED_BY──► rule-*`
     - `rule-* ──SUPPORTED_BY──► source/evidence`
   - `scripts/vitruvius/kg/unified_snapshot_builder.py` builds unified KG v2 snapshots.
   - `scripts/vitruvius/kg/neo4j_loader.py` and `api/index.ts` feed the Explorer.

## Current Snapshot Evidence

Latest inspected snapshot: `005_Operational-Intelligence-Layer/graph/kg-v2/20260423T223813Z_kg_v2_unified.json`

Observed counts:
- canonical nodes: **395**
  - rules: **296**
  - concepts: **88**
  - taxonomy nodes: **11**
- relationship assertions: **596**
- fast edges: **300**
- evidence spans: **303**

Relationship distribution:
- `DEFINED_BY`: **296**
- `SUPPORTED_BY`: **296**
- `REQUIRES`: **2**
- `RELATED_TO`: **1**
- `DEPENDS_ON`: **1**

Lifecycle state:
- `review_state`: **596 pending**
- `validation_status`: **592 candidate**, **4 validated**

Taxonomy coverage:
- concepts with `taxonomy_path`: **88/88**
- rules with `taxonomy_path`: **296/296**
- taxonomy nodes with path coverage: **11/11**

## Findings

### Finding 1 — Relationship semantics are too shallow
The graph is currently dominated by structural edges created by the rule rewire (`DEFINED_BY`, `SUPPORTED_BY`). These are useful for provenance, but they do not yet express enough domain semantics between concepts/rules.

The result: the graph can show where rules come from, but not yet enough of what rules do, constrain, depend on, override, exclude, or apply to.

### Finding 2 — Predicate vocabularies drift across layers
Relevant files:
- `.ai/06_specs/relationship-schema.md`
- `scripts/vitruvius/rules/relationship_registry.yaml`
- `scripts/vitruvius/kg/enums.py`
- `scripts/vitruvius/kg/evidence_materializer.py`

Examples:
- `covers` exists in `relationship_registry.yaml` but not in the authoritative relationship schema.
- KG v2 `EdgeType` includes richer predicates (`APPLIES_TO`, `OVERRIDES`, `EXCLUDES`) than the legacy relationship schema.
- `evidence_materializer.py::_edge_type_from_string()` performs lossy mappings such as:
  - `governs → APPLIES_TO`
  - `limits → REQUIRES`
  - `affects → RELATED_TO`

This makes relationship quality hard to reason about and can hide meaning before data reaches the Explorer.

### Finding 3 — Rule labels are evidence sentences, not usable graph names
Relevant files:
- `scripts/vitruvius/kg/rule_extractor.py`
- `scripts/vitruvius/kg/schemas.py`
- `api/index.ts`
- `explorer/src/utils/labels.ts`

Current behavior:
- `_rule_label_from_evidence()` derives the rule label from the first evidence sentence and caps it around 120 characters.
- `CanonicalNode` has no persisted `display_label` field.
- The API now computes `displayLabel`, but this is a presentation fallback, not a real semantic display name.

This explains why rule nodes still feel long and awkward: the canonical rule `label` is doing two jobs at once — source-faithful evidence summary and graph-display name.

### Finding 4 — Taxonomy exists but does not guide enough behavior
Taxonomy paths exist for every concept and rule in the inspected snapshot, but taxonomy is not yet used strongly enough for:
- rule display-label generation,
- semantic relationship enrichment,
- Explorer filtering/legending by branch,
- distinguishing explicit versus taxonomy-lifted inferred edges.

### Finding 5 — Do not bulk-validate current candidates blindly
The snapshot has 592 candidate assertions and 596 pending review states. Promoting these wholesale would improve dashboard numbers while hiding the real issue: current relationship semantics are not yet precise enough.

## Recommended Bounded Improvement Order

1. **Relationship contract alignment**
   - Make schema, registry, KG enum, materializer mapping, API, and tests agree on predicate meaning.
   - Fail on unknown/lossy mappings instead of silently converting them.

2. **Persisted display labels for rule nodes**
   - Add `display_label` to `CanonicalNode`.
   - Generate concise taxonomy-aware rule display labels in `rule_extractor.py`.
   - Preserve the full evidence text in `summary` / evidence spans.

3. **Taxonomy-aware semantic enrichment**
   - Use taxonomy as a scaffold for additional candidate edges, but distinguish explicit evidence from inferred taxonomy-lifted edges.
   - Start with a small set of predicates and validate by stratified sampling.

4. **Explorer trust/provenance UX**
   - Filter by validation state, predicate, taxonomy branch, and explicit/inferred edge type.
   - Ensure every edge inspector can answer: “why does this edge exist?”

## Stop Conditions
- Unknown predicate appears in a build.
- Legacy predicate maps lossy to KG v2 without explicit rule/test coverage.
- New semantic edge precision falls below the review threshold.
- Inferred/taxonomy-lifted edges outnumber explicit edges in a branch without review.
- Evidence anchors or taxonomy paths cannot be resolved.

## Conclusion
The graph has made a major structural jump, but the next quality leap must be data-contract-first. The safest next slice is not a broad extractor rewrite; it is predicate contract alignment plus persisted taxonomy-aware rule display labels.
