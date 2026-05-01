# Architecture Taxonomy Real Enrichment Context

## Task statement
Populate the AEC-MEPFS Architecture (`ARC`) branch first with real, comprehensive architecture concepts/rules/definitions/procedures, not placeholder scaffold nodes.

## Desired outcome
Replace/augment Architecture L4 scaffold nodes such as `[Subtopic] Concepts`, `Concept Anchor`, and `Rule Context` with meaningful Architecture domain nodes. Preserve rights-safe metadata only. Generate current fixture/artifacts, tests, evidence, and commit/push.

## Known facts/evidence
- Current fixture: `scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json`.
- Current graph artifact: `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260428T174344Z/shadow-backbone-graph.json`.
- Previous scaffold count: 1984 generic scaffold nodes across all taxonomies; many Architecture L4 labels are generic.
- User explicitly rejected scaffold/placeholder content.

## Constraints
- No protected payload ingestion.
- No Neo4j/KG mutation or rebuild/reload/reset.
- No API/Explorer runtime behavior change unless needed for tests.
- Use Kimi if available for advisory review.
- Use team/parallel lanes for research only; keep shared-file edits local.
- Windows-safe filenames.

## Acceptance criteria
- Architecture branch has real L4 semantic nodes, not generic scaffold placeholders.
- Architecture scaffold ratio is materially reduced and specifically validated.
- At least major architecture domains are covered: history/theory, design process, building technology, structures coordination, environmental systems, professional practice, laws/code compliance, accessibility, site/planning, sustainability, materials, documentation/specifications, construction admin, heritage, interiors, digital/BIM, urban context.
- Focused tests/staging pass.
- Evidence report and validation log exist.

## Likely touchpoints
- `scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json`
- `scripts/vitruvius/kg/backbone_shadow_staging.py`
- `scripts/tests/test_kg_backbone_contracts.py`
- `scripts/tests/test_kg_backbone_resolver_qa.py`
- `.ai/13_research/`
- `.ai/03_plans/AEC-MEPFS-Backbone/`
- `.ai/05_logs/`
- `006_System-Manifests/aec-mepfs-backbone/taxonomy-expansion/`
