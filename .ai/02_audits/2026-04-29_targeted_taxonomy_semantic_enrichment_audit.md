# Targeted Taxonomy Semantic Enrichment Audit

Date: 2026-04-29  
Run id: 20260429T065436Z  
Status: completed after validation

## Audit purpose

Determine whether the existing AEC-MEPFS file-backed backbone had a high-value, rights-safe enrichment opportunity after broad L4 scaffold cleanup.

## Current graph baseline before this slice

- File-backed source: `scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json`
- Previous latest shadow run: `20260429T015840Z`
- Counts: 8935 BackboneNode records, 8911 hierarchy edges, 24 roots, max depth 4
- Known prior achievement: global L4 scaffold labels were removed.

## Findings

1. **Standards/source-family context was shallow.** The graph had a `COM.STD` standards branch, but several public standards-family anchors that are operationally central to AEC-MEPFS were not explicit taxonomy nodes.
2. **Cross-domain semantic edges were underrepresented.** Prior large-scale enrichment was mainly hierarchical. It did not materially express that specific discipline topics map to or require standards/guidance families.
3. **Source-rights registry needed matching metadata rows.** New standards-family references needed explicit no-ingest boundaries before they could safely support taxonomy metadata.
4. **High-value existing branches were available.** Mechanical, electrical, fire/life safety, plumbing, sanitary, security, smart systems, heritage, sustainability, and operations already had target parent nodes that could receive real, non-placeholder L4 children.
5. **Schema constraints are strict but sufficient.** L1-L4 depth and three-character path segments support real enrichment if names are concise and deterministic.

## Risk assessment

| Risk | Assessment | Mitigation |
|---|---|---|
| Protected source ingestion | High if standards text is copied | Use only source-family metadata, landing-page URLs, aliases, and steward-written descriptions |
| Duplicate concepts | Medium | Use existing `path_code` lookup and idempotent merge behavior |
| Invalid path depth or segment length | Medium | Add explicit tests for targeted records and rely on backbone contract validation |
| Runtime/API drift | Medium | Regenerate shadow staging and update API count expectations only; no route logic change |
| Codex Spark use against user requirement | Medium | Use Kimi CLI for advisory synthesis; add a task-specific Kimi enrichment route in `opencode.json`; record rights-safety flag `codex_spark_used_for_research_or_synthesis=false` |
| Live graph mutation | High | Use file-backed fixture, reports, and shadow staging only; no Neo4j writes, no rebuild/reload/reset |

## Approved implementation scope

- Add real standards-family and discipline-topic nodes.
- Add governed relationship records using existing predicates.
- Add metadata-only source-rights rows.
- Add deterministic enrichment script and tests.
- Regenerate shadow staging artifacts for a new run.
- Update API tests to reflect changed file-backed counts and semantic edge types.

## Blocked scope

- No protected standard text, clauses, tables, figures, diagrams, or publication payloads.
- No production Neo4j mutation.
- No KG rebuild, reload, or reset.
- No Explorer/API behavior change beyond count/test expectation updates caused by the new file-backed graph.
- No fake Kimi integration or placeholder provider setting.

## Audit conclusion

A targeted standards-family and discipline-topic semantic enrichment is justified and bounded. The work materially improves graph breadth, provenance, cross-domain reasoning, aliases, and relationship semantics while preserving the file-backed read-only boundary.
