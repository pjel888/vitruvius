# Architecture project evidence paths context snapshot

## Task statement
Continue the architecture / AEC / LEA-ALE knowledge-graph work by deepening source-backed, project-specific evidence paths among people, works/projects, materials, structural systems, construction methods, movements/styles, Philippine vernacular architecture, tropical design, and resolver/API/UI behavior.

## Desired outcome
The learner-facing file-backed graph should answer why concepts are connected through defensible multi-hop paths, not vague density. Add or improve graph content, resolver/API cases, stale-data/bad-label checks, source-rights safety, reports, and validation evidence.

## Known facts/evidence
- User-provided previous verified state: 9729 nodes / 12376 relationships / 100 source-rights rows / 72 resolver cases.
- Current working tree baseline at intake is already 9761 nodes / 12495 relationships / 102 source-rights rows / 72 resolver cases due uncommitted architecture interconnectivity/UI work.
- Current architecture interconnectivity generator: scripts/vitruvius/kg/architecture_interconnectivity_enrichment.py.
- Existing graph fixture: scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json.
- Existing resolver fixture: scripts/tests/fixtures/aec_mepfs_backbone/valid_readiness_s2.json.
- Current Kimi route in opencode.json: kg-enrichment-researcher -> moonshot/kimi-k2.6; prior functional Kimi CLI model was kimi-for-coding/k2p6.
- Official Pritzker site currently lists Smiljan Radić Clarke 2026, Liu Jiakun 2025, Riken Yamamoto 2024, and earlier laureates.

## Constraints
- Use Kimi for model-assisted research/review/final audit; do not use Codex Spark for enrichment.
- No Neo4j/live graph promotion, KG rebuild/reload/reset, destructive graph operations, raw-source writes, or protected source ingestion.
- No copied protected text, reviewer material, exam questions, answer keys, code/standard tables, clauses, figures, diagrams, or long passages.
- Source/provenance metadata must stay metadata-only and not leak into learner-facing concept labels/search/UI.
- Windows-safe names for generated/stored KG docs and file structures.
- Native-hook surface is outside tmux, so durable tmux worker panes are unavailable here; proceed through local Ralph loop and record that limitation.

## Unknowns/open questions
- Which existing person/work/material nodes are still underconnected after the prior pass.
- Whether any current frontend/API/shadow artifact still references stale graph output with process-heavy source labels.
- Which additional high-confidence work/project anchors can be added without overclaiming.

## Likely codebase touchpoints
- scripts/vitruvius/kg/architecture_interconnectivity_enrichment.py
- scripts/tests/test_kg_architecture_interconnectivity_enrichment.py
- scripts/tests/test_kg_backbone_contracts.py
- scripts/tests/test_kg_backbone_resolver_qa.py
- scripts/tests/test_kg_lea_ale_resolver_deepening.py
- scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json
- scripts/tests/fixtures/aec_mepfs_backbone/valid_readiness_s2.json
- .ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-rights-registry.json
- api/v2Resolver.test.ts, api/v2Backbone.test.ts
- explorer graph/label tests and API data-source files
- 006_System-Manifests/aec-mepfs-backbone architecture/shadow/resolver outputs
