# Context Snapshot — LEA/ALE Resolver and Semantic Deepening

## Task statement
Continue verified LEA/ALE Philippine Architecture Licensure Examination graph enrichment by improving real graph usability, resolver/API golden paths, utilities/structural-concept detail, cross-subject reasoning paths, and source-rights safety.

## Desired outcome
A file-backed AEC-MEPFS backbone with additional source-safe LEA/ALE nodes/relationships and validated resolver/API golden cases proving practical licensure-study query paths.

## Known facts/evidence
Previous phase completed 9,403 nodes / 10,979 relationships, 236 LEA/ALE nodes, 1,193 LEA/ALE relationships, 79 source-rights rows, Kimi audit PASS, no protected payloads or live graph promotion.

## Constraints
Use Kimi for model-assisted research/review; do not use Codex Spark. No protected source payloads, exam questions, answer keys, tables, clauses, figures, diagrams, reviewer text, Neo4j/live graph promotion, KG rebuild/reload/reset, destructive operations, or raw-source writes.

## Unknowns/open questions
Exact resolver/golden-case file format and API test patterns need inspection. Current valid predicate set must be reused. Source-rights row enum constraints must be preserved.

## Likely touchpoints
scripts/vitruvius/kg/lea_ale_semantic_enrichment.py; scripts/vitruvius/kg/backbone_resolver_qa.py; scripts/tests/test_kg_lea_ale_semantic_enrichment.py; scripts/tests/test_kg_backbone_resolver_qa.py; api/v2Backbone.test.ts; source-rights registry; admitted backbone fixture; shadow staging reports; .ai plan/log docs.

## Acceptance criteria
- Baseline counts captured before edits.
- Actual graph content improved with utilities/structural/cross-subject LEA/ALE content.
- 40+ resolver/API/golden assertions added.
- New relationships are governed and schema-valid.
- Raw-source handling remains metadata-only and tested.
- Fresh validations and Kimi final audit pass.
