---
task: lea-ale-knowledge-graph-enrichment
phase: 00
created: 2026-04-29
author: PLANNER
supersedes: null
status: ACCEPTED
---

# Trigger — LEA/ALE Knowledge Graph Enrichment

## Task statement
Enrich the AEC-MEPFS file-backed backbone with real Philippine Architecture Licensure Examination subject-domain nodes, aliases, source metadata, and governed relationships.

## In scope
- `scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json`
- `scripts/vitruvius/kg/*lea*` or a new bounded enrichment script under `scripts/vitruvius/kg/`
- `.ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-rights-registry.json`
- focused/broad/backbone/API tests affected by file-backed graph counts
- generated shadow/report artifacts under `006_System-Manifests/aec-mepfs-backbone/`

## Out of scope
- raw source writes under `001_Raw-Source-Layer/`
- protected source payload ingestion
- Neo4j/live graph promotion
- destructive graph operations
- schedule tracking as ontology core

## Risk class
M — multi-file file-backed KG enrichment, tests, source-rights metadata, and generated artifacts. No schema/predicate expansion planned.

## Identity-locked file check
PASS. No identity-locked system files or raw source writes are planned.

## MCP/GitNexus precheck
- `omx explore` located graph/source/test/Kimi-routing touchpoints; Codex Spark attempt failed and fallback used non-Spark model.
- `gitnexus query` located architecture taxonomy enrichment and tests.
- Before editing any existing symbol, run `gitnexus impact` on the symbol/module entry point.
