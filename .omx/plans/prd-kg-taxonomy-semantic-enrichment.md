# PRD - KG Taxonomy Semantic Enrichment

## Goal
Improve the real AEC-MEPFS knowledge graph content by adding curated, researched L4 domain nodes and meaningful governed relationships while preserving the file-backed, rights-safe shadow boundary.

## Scope
- Add substantial real graph content to the admitted backbone fixture.
- Add or update source/provenance registry entries for public taxonomy/standard families used as references.
- Regenerate shadow staging and graph artifacts under a new run ID.
- Update affected validation tests and record validation evidence.
- Configure active model-assisted enrichment workflow toward Kimi and away from Codex Spark where project config supports it.

## Non-goals
- No protected source payload ingestion.
- No raw-source edits.
- No production Neo4j writes or graph reset/reload.
- No API or Explorer runtime behavior changes.
- No new relationship predicate vocabulary unless existing allowed predicates are insufficient.

## Acceptance criteria
- At least 75 real, non-placeholder BackboneNode records are added.
- At least 150 governed relationships are added or improved, including hierarchy and semantic cross-domain edges.
- At least 25 aliases/synonyms/acronyms are added through node aliases.
- At least 10 source/provenance references are added or materially used in registry/research/validation artifacts.
- Added nodes are connected, use deterministic IDs/path codes, and pass existing contract validation.
- New shadow staging artifacts are generated and reports are green.
- Relevant Python tests pass.
- Kimi CLI is used for research/review; Codex Spark is not used for taxonomy research/synthesis/content generation.
