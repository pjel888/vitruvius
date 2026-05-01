# Ralph Context Snapshot — LEA/ALE Knowledge Graph Enrichment

- **Created:** 2026-04-29T08:40:24Z
- **Task slug:** lea-ale-knowledge-graph-enrichment
- **Mode:** ultrawork + ralph + team

## Task statement
Materially enrich the file-backed AEC-MEPFS knowledge graph for the Philippine Licensure Examination for Architects (LEA/ALE/BLEA) by adding real subject-domain nodes, aliases, source metadata, and governed relationships across history, theory, Philippine architecture, laws/codes, utilities, materials, construction, site planning, professional practice, ethics, contracts, permits, and exam meta-context.

## Desired outcome
The graph becomes useful for Philippine architecture examinees, educators, reviewers, and architects reasoning across actual LEA/ALE subject domains rather than only broad PRC exam-day areas.

## Known facts/evidence
- Current committed baseline after the prior verified AEC-MEPFS overlay slice is 9,167 nodes / 9,786 governed relationships in `scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json`.
- Current source-rights registry is `.ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-rights-registry.json` with 51 metadata/reference rows.
- Existing architecture enrichment script already contains high-level Philippine ALE nodes such as `Philippines ALE Subject Families`, `Philippines ALE History Theory Practice Area`, `Philippines ALE Structures Materials Utilities Area`, and `Philippines ALE Design And Site Planning Area`.
- Existing governed predicate vocabulary includes `broader_than`, `constrains`, `governs`, `has_facet`, `maps_to_external_standard`, `part_of`, `requires`, and related governance predicates.
- `opencode.json` includes Kimi routing via `moonshot/kimi-k2.6` for `kg-enrichment-researcher`; no active Codex Spark enrichment routing should be introduced.

## Constraints
- Use Kimi for model-assisted research/synthesis/taxonomy review/final audit; do not use Codex Spark for enrichment.
- No protected source payloads, exam questions, answer keys, reviewer text, tables, clauses, figures, diagrams, or protected standard payloads may be ingested.
- Raw PDFs in `001_Raw-Source-Layer` may be inventoried and classified by source-rights status; use only safe metadata/topic signals.
- No Neo4j/live graph promotion, destructive graph operations, or write under `001_Raw-Source-Layer`.
- Preserve schema conventions, deterministic path IDs, source-rights conventions, and file-backed/staging workflow.

## Unknowns/open questions to resolve by inspection
- Exact set of existing ALE/LEA nodes and where duplicates might already exist.
- Exact source-rights status of relevant raw PDFs.
- Whether additional Philippine law/code source rows already exist or must be added.
- Which generated report/API expectations must be updated after enrichment.

## Likely codebase touchpoints
- `scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json`
- `scripts/vitruvius/kg/architecture_taxonomy_enrichment.py`
- new or existing LEA/ALE semantic enrichment script under `scripts/vitruvius/kg/`
- `.ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-rights-registry.json`
- `scripts/tests/test_kg_*enrichment.py`, `scripts/tests/test_kg_backbone_contracts.py`
- `006_System-Manifests/aec-mepfs-backbone/` generated reports
- `api/v2Backbone.test.ts`
