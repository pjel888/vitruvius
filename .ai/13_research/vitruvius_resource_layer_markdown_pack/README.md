# Vitruvius Resource Intelligence Layer Markdown Pack

Prepared for Vitruvius codebase AI work using Codex + Kimi, with Ralph-loop / ralploop persistence and Ultrawork-style parallel execution.

## Purpose

This pack gives the codebase AI a detailed implementation reference for adding a source/resource sidebar to Vitruvius.

Target behavior:

> When a user clicks an eligible lower-level knowledge graph node, the right sidebar shows a small, ranked, verified set of relevant references: URLs, books, PDFs, local files, professional guidance, standards, academic papers, and internal documents.

The system should not attach random links. It should build a **Resource Registry** and **NodeResourceLink** layer that connects graph nodes to evidence-backed resources with metadata, verification, ranking, provenance, and review status.

## Eligible node scope

Treat these as eligible for source/reference sidebar support:

- `Concept`
- `Rule`
- `Definition`
- `Procedure`
- `Exception`
- `Evidence`
- `Document`

Taxonomy, Topic, and Subtopic nodes may optionally show aggregate or inherited resources later, but they are not the first implementation target.

## Files

1. `00_manifesto_and_scope.md`
2. `01_PRD_resource_layer.md`
3. `02_architecture_design.md`
4. `03_data_model_resource_registry.md`
5. `04_node_resource_linking_strategy.md`
6. `05_source_discovery_research_plan.md`
7. `06_api_adapter_specs.md`
8. `07_local_corpus_indexing.md`
9. `08_verification_ranking_and_deduplication.md`
10. `09_sidebar_ux_spec.md`
11. `10_agent_workflows_codex_kimi_ultrawork_ralploop.md`
12. `11_loopable_codex_prompt.md`
13. `12_kimi_review_prompts.md`
14. `13_validation_tests_quality_gates.md`
15. `14_seed_source_authority_registry.md`
16. `15_backfill_strategy_for_graph_nodes.md`
17. `16_definition_rule_procedure_evidence_document_nodes.md`
18. `17_implementation_roadmap_and_milestones.md`
19. `18_metrics_dashboard_reporting.md`
20. `19_risk_legal_copyright_and_jurisdiction.md`
21. `20_research_bibliography_and_official_docs.md`
22. `21_acceptance_checklists.md`
23. `22_appendix_sample_queries_and_pseudocode.md`

## Immediate implementation sequence

1. Add Resource Registry and NodeResourceLink structures.
2. Add local corpus scanner and metadata index.
3. Add source-family authority registry.
4. Add right-sidebar resource card UI using mock/seed data.
5. Add validation for resources and node links.
6. Backfill only top high-centrality Concept nodes first.
7. Add Rule/Definition/Procedure/Evidence/Document nodes only when source-backed.
8. Loop until resource coverage and verification quality gates pass.

## Operating principle

A sidebar reference is useful only when it answers:

- What is this source?
- Why is it relevant to this node?
- How authoritative is it?
- Is it local or online?
- Has it been verified?
- Is it jurisdiction-specific?
- Which page/chapter/section is relevant?

Do not show raw, unreviewed search results as final references.

External documentation links in this pack were checked/selected for planning on: **2026-05-01**.
