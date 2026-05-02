# Ralph Context Snapshot - Architecture Civil Structural KG Loop

Timestamp UTC: 20260501T045108Z

## Task statement
Continue Vitruvius KG improvement with Ralph/UltraQA/Ultrawork loops, focusing Architecture, Civil Engineering, and Structural Engineering taxonomies. Implement remaining recommended gaps and add durable PRD/task-list, progress, quality, gap, source, and decision artifacts.

## Desired outcome
File-backed AEC-MEPFS Backbone gains evidence-backed Architecture/Civil/Structural nodes, typed mechanism-based relationships, source metadata, traversal tests, validation, and quality scoring >=90/100 with no critical validation failures.

## Known facts/evidence
- Existing previous pass added domain cluster enrichment, graph quality validation, edge metadata propagation, docs, and reports.
- Active repo has uncommitted KG changes from previous pass; these are Ralph-owned and must be preserved.
- Current file-backed graph fixture is scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json.
- Source registry is .ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-rights-registry.json.
- Resolver QA fixture is scripts/tests/fixtures/aec_mepfs_backbone/valid_readiness_s2.json.
- Current docs/shared/agent-tiers.md is missing.
- Kimi CLI is present at C:\Users\phili\.local\bin\kimi.exe.

## Constraints
- Follow AGENTS.md: state-first, execution loop, code intelligence refresh, no protected source ingestion, file-backed only.
- No placeholders, no vague related_to edges, no fake jurisdictional authority.
- Preserve compatibility with shadow/API tests.
- Windows-safe filenames.

## Unknowns/open questions
- Kimi CLI authentication/usage must be verified.
- Exact current Architecture/Civil/Structural coverage needs baseline metrics.
- Need determine best extension pattern from existing enrichment module.

## Likely codebase touchpoints
- scripts/vitruvius/kg/domain_cluster_enrichment.py
- scripts/vitruvius/kg/backbone_graph_quality.py
- scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json
- scripts/tests/fixtures/aec_mepfs_backbone/valid_readiness_s2.json
- .ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-rights-registry.json
- docs/knowledge-graph/*
- 006_System-Manifests/aec-mepfs-backbone/*
