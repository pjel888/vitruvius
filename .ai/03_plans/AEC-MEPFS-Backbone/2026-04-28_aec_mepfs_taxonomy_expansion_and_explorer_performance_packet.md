# AEC-MEPFS Taxonomy Expansion And Explorer Performance Packet

```yaml
status: BOUNDARY_APPROVED_IMPLEMENTED
created: 2026-04-28
authority: project-owner-directive-actual-aec-mepfs-implementation-cutover
run_id: 20260428T021641Z
gemini_used: false
protected_content_ingest_authorized: false
neo4j_mutation_authorized: false
kg_rebuild_reload_authorized: false
```

## Purpose

Correct the Explorer AEC-MEPFS default graph from the seven-node staging stub to
the governed first-slice L1/L2 taxonomy skeleton, and reduce Explorer/API jank
introduced by repeatedly rebuilding file-backed graph state.

This packet responds to the implementation gap where Explorer was technically
cut over to AEC-MEPFS but still rendered only a small fixture:

- `scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json`
- the old shadow staging artifact under `20260426T003710Z`

The intended first-slice taxonomy is the decision-recorded AEC-MEPFS L1/L2
outline, not the seven-node smoke fixture.

## Allowed Scope

- Expand the admitted non-protected L1/L2 taxonomy fixture.
- Generate new file-backed shadow staging artifacts from that fixture.
- Make API preview/default Explorer routes resolve the latest shadow staging
  consumer report unless an explicit override path is provided.
- Cache file-backed AEC graph artifacts by file size and mtime.
- Keep `/health` and `/perspectives` cheap by avoiding unnecessary graph rebuilds
  and Neo4j checks on their default paths.
- Add Explorer large-graph rendering guardrails:
  - deterministic clustered layout for large AEC graphs,
  - disabled physics for large graphs,
  - reduced edge smoothing and shadows,
  - less camera/minimap churn while dragging,
  - visible graph-engine load errors.
- Update tests and evidence artifacts to prove the expanded graph and performance
  guardrails.

## Blocked Scope

- No protected source text, tables, figures, clauses, datasets, or local protected
  caches may be ingested or exposed.
- No Neo4j writes, resets, reloads, destructive cleanup, or primary graph
  promotion may occur.
- No KG rebuild/reload/reset may occur.
- No broad/global `LIVE_RUNTIME_AUTHORIZED` status may be granted.
- No secret, token, credential, database URL, or private connection string may be
  printed.

## Implementation Target

The AEC-MEPFS default Explorer graph must render a comprehensive first-slice
taxonomy skeleton:

- 114 admitted backbone nodes.
- 95 `broader_than` relationships.
- 19 L1 roots:
  `ARC`, `ACC`, `URB`, `CIV`, `STR`, `GEO`, `MEC`, `ELE`, `PLS`, `FLS`, `CON`,
  `MAT`, `COM`, `PER`, `SUS`, `DIG`, `OPS`, `HIS`, and `FIG`.
- `HIS` and `FIG` remain top-level auxiliary domains, not children of
  Architecture.

The Explorer should still expose legacy graph behavior through the existing
selector/escape path, but the AEC-MEPFS default should no longer look like a
seven-node placeholder.

## Verification Plan

- Validate the expanded taxonomy fixture with the existing contract tests.
- Regenerate file-backed shadow staging artifacts for run `20260428T021641Z`.
- Regenerate route inventory evidence for run `20260428T021641Z`.
- Generate an Explorer/API performance smoke report for the same run.
- Run focused Python, API, and Explorer tests.
- Run broader affected API and Explorer suites.
- Run `git diff --check`.
- Run safety greps over changed implementation and evidence.
- Attempt Kimi/Moonshot advisory review if available.

## Evidence Artifacts

- Shadow staging:
  `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260428T021641Z/`
- Route inventory:
  `006_System-Manifests/aec-mepfs-backbone/api-route-inventory/20260428T021641Z/api-route-inventory-report.json`
- Explorer performance smoke:
  `006_System-Manifests/aec-mepfs-backbone/explorer-performance/20260428T021641Z/explorer-performance-smoke-report.json`
- Validation log:
  `.ai/05_logs/2026-04-28_aec_mepfs_taxonomy_expansion_and_explorer_performance_validation.md`

## Completion Criteria

This slice is complete only when:

1. Explorer/API AEC-MEPFS graph evidence reports 114 nodes, 95 edges, and 19
   roots.
2. The fixture contract tests prove the full root set, including `HIS` and `FIG`
   as top-level nodes.
3. API tests prove preview/default routes use the new run and counts.
4. Explorer tests, lint, and build pass.
5. Performance smoke evidence confirms `/health`, `/perspectives`, and
   `/perspective/aec-mepfs/nodes` respond successfully against the expanded
   graph.
6. Safety checks prove no protected ingest, Neo4j mutation, KG rebuild/reload, or
   unauthorized live graph promotion was introduced.
7. The working tree is clean after commit and push.
