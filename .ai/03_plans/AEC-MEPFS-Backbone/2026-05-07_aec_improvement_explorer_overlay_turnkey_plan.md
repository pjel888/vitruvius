# AEC Improvement Explorer Overlay Turnkey Plan

## Task

Make the pending-only AEC relationship/node improvement workflow usable as a turn-key discovery loop:

- run local/DeepSeek relationship improvement;
- run node-consolidation candidate discovery;
- keep every output pending-only;
- surface the resulting relationship and node-consolidation candidates in the Explorer graph without mutating the admitted graph.

## Safety Boundary

- No active backbone file mutation.
- No Neo4j/Postgres writes.
- No `--apply` enablement.
- No Kimi default routing.
- Explorer display is a read-only pending overlay, not graph admission.
- Overlay records must remain visually and metadata-distinct from steward-admitted edges.

## Audit

The AEC Explorer graph is built in `api/index.ts` from file-backed shadow artifacts by `buildAecMepfsExplorerGraph()`, then served through `/perspective/aec-mepfs/nodes`. The frontend loads that perspective through `explorer/src/api/graphApi.ts` and `ExplorerRail` already has an AEC-MEPFS preview panel. This makes the smallest safe integration a read-only API overlay over the existing Explorer graph.

The relationship workflow already writes:

- `accepted-relationships.jsonl`
- `candidate-relationships.jsonl`
- `accepted-node-consolidations.jsonl`
- `node-consolidation-candidates.jsonl`
- report/checkpoint/summary metadata

Those artifacts are enough to project pending relationship candidate edges and pending node-consolidation edges in Explorer.

## Blast Radius

Expected changed surfaces:

- `api/index.ts`: read semantic-overlay run artifacts and inject pending overlay edges into AEC Explorer graph.
- `explorer/src/types/index.ts`: add overlay preview response type.
- `explorer/src/api/graphApi.ts`: add overlay preview fetcher.
- `explorer/src/components/ExplorerRail.tsx`: load overlay preview in the AEC preview panel.
- `explorer/src/components/explorer-rail/BackbonePreviewPanel.tsx`: display pending-only overlay counts and latest run.
- Python workflow/tests may need minor artifact assertions only.

Risk is medium because `api/index.ts` is central to Explorer AEC graph loading. Mitigation:

- default to no overlay when no run exists;
- cache key includes overlay file mtimes;
- overlay edges use distinct `PENDING_*` edge types;
- active graph rows remain untouched;
- tests cover graph injection and frontend preview behavior.

## Design

### API Overlay

Add a semantic overlay reader under:

`006_System-Manifests/aec-mepfs-backbone/semantic-overlays/<run_id>/`

Default behavior:

- overlay enabled when artifacts exist;
- latest run folder is selected unless `VITRUVIUS_AEC_RELATIONSHIP_IMPROVEMENT_RUN_ID` is set;
- `VITRUVIUS_AEC_RELATIONSHIP_IMPROVEMENT_OVERLAY=0|false|off|disabled|no` disables display.

Pending relationship records become graph edges with:

- `type: "PENDING_RELATIONSHIP_CANDIDATE"`
- `reviewStatus: "candidate"`
- `semanticOverlayCategory: "relationship_improvement_candidate"`
- `pendingOnly: true`
- source/target from final accepted edge or candidate judge direction.

Node consolidation records become graph edges with:

- `type: "PENDING_NODE_CONSOLIDATION"`
- `reviewStatus: "candidate"`
- `semanticOverlayCategory: "node_consolidation_candidate"`
- `pendingOnly: true`
- source/target = candidate node pair.

### Explorer UX

Add a small AEC preview section showing:

- overlay enabled/disabled;
- latest improvement run;
- pending relationship edge count;
- pending node-consolidation edge count;
- skipped duplicate/invalid overlay count;
- explicit pending-only reminder.

The graph itself shows pending overlay edges as distinct edge types.

## Acceptance Criteria

- Existing relationship/node improvement tests pass.
- API AEC Explorer tests cover overlay injection.
- Explorer tests/build pass for the preview panel changes.
- Graph-quality and shadow-staging Python regressions pass.
- Compile succeeds for Python and Explorer TypeScript.
- A no-model run can create artifacts, and Explorer overlay code tolerates empty/missing artifacts.
- No active graph mutation path is introduced.

## Validation Log

- 2026-05-07: Implemented pending-only Explorer overlay for relationship and node-consolidation artifacts.
- 2026-05-07: Added explicit scale-run CLI controls: `--all-nodes`, `--all-pairs` / `--all-relationship-candidates`, and `--all-node-consolidation-candidates`.
- 2026-05-07: Replaced full per-row similarity sorting with bounded `argpartition` top-k selection for large node sets.
- 2026-05-07: Added append-only processed-pair ledgers and resume reconstruction from result artifacts to reduce checkpoint growth and crash-window duplicate risk.
- 2026-05-07: Added campaign-specific node-consolidation ledger reuse with threshold/text-hash matching.
- 2026-05-07: Validation passed:
  - `PYTHONPATH=scripts python -m pytest scripts/tests/test_kg_aec_relationship_improvement.py -q` -> 128 passed.
  - `PYTHONPATH=scripts python -m pytest scripts/tests/test_kg_backbone_shadow_staging.py scripts/tests/test_kg_backbone_graph_quality.py -q` -> 18 passed.
  - `bun test api/v2Backbone.test.ts` -> 76 passed.
  - `cd explorer && bun test src/api/graphApi.test.ts src/app.searchInspector.integration.test.tsx` -> 18 passed.
  - `cd explorer && bun run build` -> passed with existing Vite chunk-size warning.
  - `python -m py_compile scripts/vitruvius/kg/aec_relationship_improvement.py scripts/pipeline_cli.py` -> passed.
  - No-model CLI smoke `turnkey_scale_no_model_smoke_20260507T024621Z` -> completed, wrote report/checkpoint/summary/processed ledgers, and watcher attached successfully.
