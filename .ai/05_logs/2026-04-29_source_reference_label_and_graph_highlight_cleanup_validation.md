# Source-reference Label and Graph Highlight Cleanup Validation — 2026-04-29

## Scope

This validation covers two same-branch fixes requested after LEA/ALE enrichment:

1. Remove learner-facing graph nodes with labels like `Local raw-source filename metadata for TOA tropical architecture PDF` while preserving raw local source records in source-rights/provenance registries.
2. Fix Explorer selected-parent emphasis so nodes without a visible/direct edge to the selected parent are not highlighted as if they were direct neighbors.

No protected source payloads were ingested. No Neo4j/live graph promotion, KG rebuild/reload/reset, or destructive graph operation was performed.

## Cleanup plan followed

- Identify raw/local LEA source-reference records that were promoted into learner-facing source-reference nodes.
- Remove those raw local-custody source IDs from source-node suffix promotion, not from source-rights/provenance custody.
- Regenerate/synchronize the admitted fixture and latest shadow staging artifacts to remove the bad learner-facing records and dangling relationships.
- Keep source-rights rows metadata-only with clearer local-custody source family labels.
- Add/adjust regression tests for source-reference absence and current counts.
- For Explorer highlight behavior, change selected-neighborhood emphasis from recursive descendant traversal to direct visible-edge neighborhood traversal and update regression tests.

## Graph/source-rights evidence

- Current admitted learner-facing fixture count: 9,502 records / 11,617 relationships.
- Removed 9 raw local-custody source-reference graph nodes and 18 learner-facing relationships from the admitted graph/shadow staging artifacts.
- Raw local-custody source records remain in `.ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-rights-registry.json` as metadata-only provenance/source-rights records.
- Current fixture check: `bad_label_count: 0`, removed raw path codes absent, `missing_edge_endpoints: 0`.

## UI highlight evidence

- `graphVisualEmphasis.getSelectedNeighborhoodIds` now returns the selected node plus nodes directly connected by the provided visible edge set.
- `VisNetworkHost` now computes emphasis from visible nodes/edges only, so hidden/filtered or descendant-only edges do not keep unrelated descendants highlighted after parent selection.
- Pan mode now clears stale selected-node state and context-menu state while disabling node selection, so entering pan cannot leave a visually unselected node highlighted through store state.
- `VisNetworkHost.test.ts` and component interaction tests now lock the direct-neighborhood and pan-state behavior; the prior descendant expectation was removed.

## Validation commands and results

- `PYTHONPATH=scripts python3 -m py_compile scripts/vitruvius/kg/lea_ale_semantic_enrichment.py scripts/vitruvius/kg/lea_ale_resolver_deepening.py` — pass.
- `PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_lea_ale_semantic_enrichment.py scripts/tests/test_kg_lea_ale_resolver_deepening.py -q` — `9 passed`.
- `PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg*.py -q` — `582 passed`.
- JSON validation for admitted fixture, source-rights registry, and latest shadow staging/graph/report artifacts — `json ok 6`.
- Bad learner-facing source-reference label/path-code check — `records: 9502`, `relationships: 11617`, `bad_label_count: 0`, `bad_path_codes: []`, `missing_edge_endpoints: 0`.
- `cd explorer && bun test src/components/graph/VisNetworkHost.test.ts src/components/componentInteraction.test.tsx && bun run lint && bun run build` — `56 pass`, `242 expect() calls`, lint pass, build pass.
- `cd explorer && bun test && bun run lint && bun run build` — `82 pass`, `381 expect() calls`, lint pass, build pass. Vite retained only the existing large-chunk warning.
- `cd api && bun test v2Backbone.test.ts` — `69 pass`, `0 fail`.
- `cd api && bun test` — `103 pass`, `0 fail`.
- `git diff --check` — pass.
- `rg -n "Local raw-source filename metadata" scripts/vitruvius/kg scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json 006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260429T101500Z .ai/03_plans/AEC-MEPFS-Backbone/registry-candidates/source-rights-registry.json` — no matches.
- Safety scan over current source/fixture/staging/registry artifacts found only explicit negative/no-ingest boundary language and no true protected-payload/live-mutation/KG-reset flags.

## Tooling notes

- GitNexus MCP tools were not exposed in this Codex session. A local GitNexus binary was not present; `npx gitnexus --help` began an on-demand package install and was killed after no useful status output. Git status/diff/test evidence were used instead.
- `omx team` startup was attempted for a read-only evidence lane but refused to create worktrees because the Explorer camera-control branch already had a dirty working tree. Work continued locally without stashing or overwriting those edits.
