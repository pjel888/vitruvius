# Ralph Context Snapshot — Architecture Taxonomy Expansion

## Task statement
Expand the AEC-MEPFS Architecture taxonomy with many more topics/subtopics/concepts/rules/definitions, grounded in Architecture licensure/professional exam subjects and regional curriculum/accreditation references, starting with the Philippines and also using Hong Kong, Singapore, Indonesia, Thailand, plus local `.ai/13_research` materials.

## Desired outcome
A verified repo change that substantially improves Architecture taxonomy depth/coverage while remaining rights-safe and file-backed. Explorer should show a richer Architecture branch without protected text ingestion, Neo4j mutation, or KG rebuild/reset.

## Known facts/evidence
- Current AEC-MEPFS taxonomy expansion is file-backed and rights-safe.
- Current state docs cite run `20260428T053531Z`: 984 nodes, 960 broader_than edges, 24 roots, 240 L2 topics, 720 L3 subtopics, max depth 3.
- User wants architecture improved first using licensure/professional/accreditation structures from PH/HK/SG/ID/TH.

## Constraints
- No protected content ingestion or payload exposure.
- No Neo4j mutation or KG rebuild/reload/reset.
- Use Windows-safe filenames.
- Prefer extending existing repo patterns over inventing new structure.
- Must verify tests/reports and commit/push if successful.

## Unknowns/open questions
- Exact source file/generator for current taxonomy population.
- Current Architecture L2/L3 topics.
- Available local research docs in `.ai/13_research`.
- Exact evidence/report generator commands.

## Likely codebase touchpoints
- scripts/tests fixtures for AEC-MEPFS backbone taxonomy.
- scripts/vitruvius/kg or AEC-MEPFS staging scripts.
- 006_System-Manifests/aec-mepfs-backbone/shadow-staging.
- .ai/03_plans/AEC-MEPFS-Backbone and .ai/05_logs.
- API/Explorer tests if graph artifact counts change.
