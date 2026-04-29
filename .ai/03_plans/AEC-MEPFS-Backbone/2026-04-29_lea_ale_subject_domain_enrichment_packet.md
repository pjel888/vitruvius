---
task: lea-ale-knowledge-graph-enrichment
phase: 05
created: 2026-04-29
author: PLANNER
supersedes: null
status: VALIDATED
---

# Plan — LEA/ALE Subject-Domain Knowledge Graph Enrichment

## Objective
Improve the AEC-MEPFS file-backed backbone so it can answer practical Philippine architecture licensure questions across real subjects/domains, legal/code domains, practice domains, and architectural knowledge topics.

## Strategy
1. Inspect current graph, source-rights registry, predicate registry, enrichment scripts, tests, generated reports, opencode Kimi routing, and raw-source filename inventory.
2. Use official/public metadata and Kimi advisory synthesis to build a source-safe LEA/ALE subject-domain map.
3. Add a deterministic enrichment script that adds missing real nodes, improves weak existing nodes, appends metadata-only source refs, and adds governed relationships without new predicates.
4. Regenerate the file-backed fixture and shadow artifacts.
5. Add focused tests and update affected contract/API expectations.
6. Run validation, safety greps, Kimi final review, and state/doc reconciliation.

## Relationship predicate mapping
- `governed_by`, `regulates`, `applies_to` → source node uses `governs` or `constrains` toward topic.
- `exemplifies`, `influences`, `used_in` → use `has_facet`, `part_of`, `requires`, or `constrains` depending on direction and semantic fit.
- Avoid `related_to` and other vague predicates unless already governed; current plan uses stricter governed predicates.

## Plan Critique
[C001] Count targets must not override semantic quality. Relationships must be category-reported and spot-checkable.
[C002] Raw-source inspection can become unsafe if body text is extracted from protected reviewers or standards. Limit to filenames/metadata unless official public law text is clearly safe and still summarize originally.
[C003] Broad taxonomy and existing architecture enrichment may reprocess new level-3 semantic nodes. Exclude new semantic node kinds from broad auto-enrichment if needed.
[C004] Generated report and API count expectations must be updated only after actual fixture generation.

## Execution Checklist
- [x] [G001] Verify Kimi routing and no active Codex Spark enrichment routing.
- [x] [G002] Inventory raw PDFs/XLSX and classify source rights.
- [x] [G003] Run Kimi advisory taxonomy/source-family review.
- [x] [G004] Run GitNexus impact for modified enrichment symbols.
- [x] [G005] Implement source-safe LEA/ALE enrichment script and update source-rights rows.
- [x] [G006] Generate fixture/report artifacts and tests.
- [x] [G007] Run validations and safety greps; fix failures.
- [x] [G008] Run Kimi final review and write validation log/state updates.


## Implementation Result
- Enrichment script: `scripts/vitruvius/kg/lea_ale_semantic_enrichment.py`.
- File-backed fixture updated: `scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json`.
- Enrichment report: `006_System-Manifests/aec-mepfs-backbone/lea-ale-enrichment/20260429T091500Z/lea-ale-enrichment-report.json`.
- Shadow staging and consumer reports: `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260429T092800Z/`.
- Counts: 236 new LEA/ALE/source nodes, 65 improved existing nodes, 1,193 new governed relationships, 799 cross-domain relationships, 572 Philippine law/code relationships, and 1,135 aliases added or preserved on new/improved nodes.
- Source-rights registry: 28 metadata-only rows added, 79 total rows after enrichment.
- Raw-source custody classifications: three LEA/ALE-relevant files were treated as metadata/topic-signal only because they appear to be private/third-party reviewer or exam-prep materials.

## Validation Evidence
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts python3 -m pytest -q scripts/tests/test_kg_lea_ale_semantic_enrichment.py` → 4 passed.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts python3 -m pytest -q scripts/tests/test_kg_lea_ale_semantic_enrichment.py scripts/tests/test_kg_backbone_contracts.py` → 52 passed.
- Relevant KG suite (`test_kg_lea_ale_semantic_enrichment.py`, `test_kg_backbone_contracts.py`, `test_kg_architecture_taxonomy_enrichment.py`, `test_kg_broad_taxonomy_semantic_enrichment.py`, `test_kg_cross_domain_overlay_enrichment.py`, `test_kg_targeted_taxonomy_semantic_enrichment.py`, `test_kg_backbone_shadow_staging.py`, `test_kg_backbone_shadow_report_reader.py`) → 96 passed.
- Shadow staging `20260429T092800Z` and shadow consumer report validation → ok=true.
- `cd api && bun test v2Backbone.test.ts` → 69 passed / 0 failed.
- JSON validation for modified fixture, source-rights registry, enrichment report, and shadow reports → OK.
- Duplicate/orphan check → duplicate IDs 0, duplicate paths 0, missing edge endpoints 0, missing parent paths 0.
- `git diff --check` → OK.
- GitNexus status → repository index up-to-date at commit `742ac6c`.

## Safety Result
- Kimi was used for advisory synthesis and final read-only audit; Codex Spark was not used for enrichment research/synthesis.
- No protected source payloads, reviewer text, exam questions/answer keys, protected code tables/clauses/figures/diagrams, or raw PDF body text were ingested.
- No Neo4j/live graph promotion, destructive graph operation, KG rebuild/reload/reset, API behavior change, or Explorer behavior change was performed.
