# Architecture Project Evidence Paths Validation — 2026-04-30

## Scope

Ralph/Ultrawork phase for project-specific architecture evidence paths across people, works, materials, structural systems, movements, Philippine vernacular/tropical design, and resolver/API/UI bad-label safety.

## Baseline before this phase

- File-backed graph fixture: 9,761 nodes / 12,495 relationships.
- Source-rights registry: 102 rows.
- Resolver golden cases: 72.
- Duplicate IDs/path codes: 0.
- Missing edge endpoints: 0.
- Missing parent paths: 0.

## Output after this phase

- File-backed graph fixture: 9,834 nodes / 12,970 relationships.
- Source-rights registry: 105 rows.
- Resolver golden cases: 97.
- Nodes added: 73.
- Existing nodes improved: 24.
- Governed relationships added: 475.
- Person-work relationships added/improved: 60.
- Work-material/system/movement relationships added/improved: 200.
- Material-property/method/assembly relationships added/improved: 102.
- Engineer/architect-engineer structural paths added/improved: 72.
- Pritzker/person/work/material paths added/improved: 36.
- LEA/ALE cross-subject relationships added/improved: 301.
- Aliases preserved/added on new/improved nodes: 338.

## Generated artifacts

- Enrichment report: `006_System-Manifests/aec-mepfs-backbone/architecture-project-evidence-paths/20260430T075722Z/architecture-project-evidence-paths-report.json`.
- Shadow staging: `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260430T080147Z/`.
- Resolver QA: `006_System-Manifests/aec-mepfs-backbone/resolver-qa/20260430T080147Z_RESOLVER_QA/`.
- Kimi advisory: `.ai/13_research/2026-04-30_architecture-evidence-paths-advisory.md`.
- Kimi final audit logs:
  - `.omx/logs/architecture-project-evidence-kimi-final-audit.txt`.
  - `.omx/logs/architecture-project-evidence-kimi-final-audit-followup.txt`.

## Validation commands and results

- `PYTHONPATH=scripts python3 -m py_compile scripts/vitruvius/kg/architecture_interconnectivity_enrichment.py` — passed.
- `PYTHONPATH=scripts python3 -m py_compile scripts/vitruvius/kg/broad_taxonomy_semantic_enrichment.py scripts/vitruvius/kg/architecture_interconnectivity_enrichment.py` — passed.
- `PYTHONPATH=scripts python3 scripts/vitruvius/kg/architecture_interconnectivity_enrichment.py --write --report 006_System-Manifests/aec-mepfs-backbone/architecture-project-evidence-paths/20260430T075722Z/architecture-project-evidence-paths-report.json` — passed; wrote graph/source/resolver updates.
- `PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_shadow_staging --run-id 20260430T080147Z --backbone-nodes scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json` — passed.
- `PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_shadow_report_reader --run-id 20260430T080147Z` — passed.
- `PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_resolver_qa --run-id 20260430T080147Z_RESOLVER_QA` — passed; 97/97 resolver cases.
- `PYTHONPATH=scripts pytest -q scripts/tests/test_kg_architecture_interconnectivity_enrichment.py` — 6 passed.
- `PYTHONPATH=scripts pytest -q scripts/tests/test_kg_broad_taxonomy_semantic_enrichment.py scripts/tests/test_kg_architecture_taxonomy_enrichment.py` — 4 passed.
- `PYTHONPATH=scripts pytest -q scripts/tests/test_kg_backbone_contracts.py scripts/tests/test_kg_backbone_resolver_qa.py scripts/tests/test_kg_lea_ale_resolver_deepening.py` — 75 passed.
- `PYTHONPATH=scripts pytest -q scripts/tests/test_kg*.py` — 588 passed.
- `bun test api/v2Resolver.test.ts` — 15 passed / 514 expects.
- `bun test api/v2Backbone.test.ts` — 72 passed / 281 expects.
- `bun test api` — 109 passed / 880 expects.
- `bun test explorer/src/components/componentInteraction.test.tsx explorer/src/components/graph/VisNetworkHost.test.ts` — 60 passed / 253 expects after clearance-label fix.
- `bun test explorer/src` — 86 passed / 392 expects.
- JSON validation with `python3 -m json.tool` equivalent on modified graph, resolver, source-rights, report, shadow staging, and resolver QA artifacts — passed.
- Duplicate/integrity script — 0 duplicate IDs, 0 duplicate path codes, 0 missing edge endpoints, 0 missing parent paths.
- Bad learner-facing label scan on current fixture and `20260430T080147Z` shadow staging — 0 hits.
- Current graph search for `SRC-RAW-*` nodes in `shadow-backbone-graph.json` — 0 hits.
- Source-rights registry validation — 105 rows, 0 duplicate source IDs, 0 fields over 80 words in source-rights registry values checked.
- Relationship quality scan — 0 direct person-to-material edges; 0 phase `related_to` edges; 0 learner-facing process-label hits; phase material nodes all have parents.
- Safety diff scan for added Neo4j writes, destructive graph operations, KG rebuild/reload/reset, protected payload markers, exam questions, answer keys, reviewer text, protected tables/clauses/figures/diagrams — no added unsafe operations or payloads found.
- `git diff --check` — passed.
- `npx -p gitnexus@1.6.2-rc.10 gitnexus status` — indexed commit equals current commit; up-to-date.
- Kimi final read-only audit — APPROVED; follow-up audit after source-clearance display fix — APPROVED.

## UI/API data-source and stale-label findings

- API resolver fixture source: `scripts/tests/fixtures/aec_mepfs_backbone/valid_readiness_s2.json`.
- API/Explorer graph source: latest safe file-backed shadow staging artifact `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260430T080147Z/shadow-backbone-staging.json` plus shadow graph artifact.
- Current learner-facing graph output does not expose `Local raw-source filename metadata for TOA tropical architecture PDF`.
- Current default `/v2/search`, `/search`, and Explorer graph tests assert clean `Tropical Architecture And Climate Response` and absence of raw-source metadata labels.
- Source-rights/provenance rows preserve local PDF filename/path metadata in source-rights registry only.
- Opt-in source clearance preview now displays human-readable labels such as `Planning Reference Only` instead of raw `planning_reference_only` text in the component DOM.

## Safety confirmation

No protected source payloads, reviewer text, exam questions, answer keys, protected tables, clauses, figures, diagrams, Neo4j/live graph promotion, KG rebuild/reload/reset, or destructive graph operations were performed.

## OMX state

Ralph and Ultrawork were active during execution. Team mode could not be controlled from this native/non-attached tmux surface; no fake worker output was produced.
