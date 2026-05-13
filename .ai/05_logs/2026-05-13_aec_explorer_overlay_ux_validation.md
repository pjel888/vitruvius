# AEC Explorer Overlay UX Validation

Date: 2026-05-13

## Scope

Improved Explorer display of completed AEC relationship-improvement and node-consolidation overlay runs while preserving the pending-only safety boundary.

## Files Reviewed

- `api/index.ts`
- `api/v2Backbone.test.ts`
- `explorer/src/components/ExplorerRail.tsx`
- `explorer/src/components/explorer-rail/BackbonePreviewPanel.tsx`
- `explorer/src/components/inspector/EdgeInspector.tsx`
- `explorer/src/components/componentInteraction.test.tsx`
- `explorer/src/types/index.ts`
- `README.md`
- `docs/knowledge-graph/aec-explorer-overlay-campaigns.md`

## Validation Commands

```bash
bun test explorer/src/components/componentInteraction.test.tsx
bun test explorer/src/app.searchInspector.integration.test.tsx
bun test explorer/src/api/graphApi.test.ts
bun test api/v2Backbone.test.ts
bun run --cwd explorer build
python -m py_compile scripts/vitruvius/kg/aec_relationship_improvement.py scripts/pipeline_cli.py
$env:PYTHONPATH='scripts'; python -m pytest scripts/tests/test_kg_aec_relationship_improvement.py -q
$env:PYTHONPATH='scripts'; python -m pytest scripts/tests/test_kg_backbone_shadow_staging.py scripts/tests/test_kg_backbone_graph_quality.py -q
git diff --check
rg -n "<secret-or-reasoning-patterns>" <changed-files>
bash ./scripts/refresh_code_intelligence.sh
cmd /c npx --yes gitnexus@1.6.4-rc.32 detect-changes --repo vitruvius
Invoke-WebRequest -UseBasicParsing http://localhost:3000/health
Invoke-WebRequest -UseBasicParsing http://localhost:5173
```

## Results

- `componentInteraction.test.tsx`: 28 passed.
- `app.searchInspector.integration.test.tsx`: 10 passed.
- `graphApi.test.ts`: 8 passed.
- `api/v2Backbone.test.ts`: 80 passed.
- Explorer build: passed; Vite reported the existing large chunk warning.
- Python compile: passed.
- AEC relationship improvement tests: 138 passed.
- Shadow staging/graph quality tests: 18 passed.
- `git diff --check`: passed; Git emitted line-ending warnings only.
- Secret/reasoning scan on changed files: no matches.
- Code intelligence refresh: completed with existing ChunkHound generated-artifact embedding warnings and missing `tree-sitter-yaml` warnings from code-review-graph.
- GitNexus detect-changes reported critical risk because the working tree includes pre-existing Python pipeline changes and large campaign artifacts beyond this Explorer UX scope.
- Local API restarted on port 3000 so the running Explorer can read enriched overlay metadata.
- Local API health: `{"status":"ok","neo4j":"not checked","aecMepfs":"ready"}`.
- Local Explorer: HTTP 200 on port 5173.
- Live overlay spot-check returned a `PENDING_RELATIONSHIP_STEWARD_APPROVED` edge from run `aec_backbone_all_nodes_bounded_004` with `effectiveJudgeProvider=deepseek` and `effectiveJudgeModel=deepseek-v4-flash`.

## Safety Confirmation

- Active graph files were not modified by this Explorer UX pass.
- No Neo4j/Postgres write path was added.
- `--apply` behavior was not changed.
- Overlay edges remain `pendingOnly: true` and `activeGraphMutation: false`.
- API payload enrichment exposes compact artifact metadata only; it does not expose API keys, prompts, raw model responses, embeddings, or model reasoning fields.
