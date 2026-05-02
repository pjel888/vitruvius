---
task: aec-mepfs-domain-cluster-interrelationships
phase: 00
created: 2026-05-01
author: PLANNER
supersedes: null
status: ACCEPTED
---

# Trigger — AEC-MEPFS Domain Cluster Interrelationships

## Task statement
Improve the file-backed AEC-MEPFS knowledge graph with source-backed, deeply interconnected domain clusters and validation while preserving protected-content and production/live graph blockers.

## In scope
- scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json
- scripts/tests/fixtures/aec_mepfs_backbone/valid_readiness_s2.json
- .ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-rights-registry.json
- New KG enrichment/quality modules and focused Python tests under scripts/vitruvius/kg/ and scripts/tests/
- New generated evidence reports under 06_System-Manifests/aec-mepfs-backbone/
- Planning, research, audit, validation, and docs/state updates

## Out of scope
- Production Neo4j mutation or live graph promotion
- Protected source text/table/figure/clause ingestion
- Raw source file reads beyond filename-level custody metadata
- KG rebuild/reload/reset of any primary graph
- Default Explorer/API behavior changes beyond file-backed artifact metadata

## Identity lock and risk
- Identity-locked file check: PASS; no raw source or production graph identity files are edited.
- Risk class: L, because this adds graph records, relationship metadata, validation, tests, and state artifacts.
