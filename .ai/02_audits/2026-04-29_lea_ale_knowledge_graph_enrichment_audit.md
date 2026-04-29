---
task: lea-ale-knowledge-graph-enrichment
phase: 04
created: 2026-04-29
author: AUDITOR
supersedes: null
status: DRAFT
---

# Audit — LEA/ALE Knowledge Graph Enrichment

## Current-state findings
- Existing graph has shallow ALE anchors but lacks a broad LEA/ALE subject-domain ontology covering Philippine laws/codes, history/theory, practice, utilities, materials, contracts, site planning, and exam meta-context.
- Existing source-rights registry supports metadata-only source rows and should be extended rather than bypassed.
- Existing predicate registry supports governed predicates sufficient for enrichment without schema expansion.

## Risks
- Source-rights risk if protected reviewer/code/book PDF content is copied. Mitigation: metadata/topic signals only, official/public sources for provenance, no payload ingestion.
- Duplicate-node risk because architecture taxonomy already has ALE anchors. Mitigation: deduplicate against existing labels/aliases/paths before adding nodes.
- Overbroad PRC-area flattening risk. Mitigation: organize by actual subjects/domains and connect to exam meta nodes.
- Generated artifact drift. Mitigation: regenerate shadow staging and update count/API expectations only after validation.

## Audit verdict
Proceed with bounded file-backed enrichment under metadata-only rights constraints and Kimi-assisted review.
