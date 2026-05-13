# Source-Grounded Explorer Context Validation

Date: 2026-05-13

## Implemented

- Added `scripts/vitruvius/kg/source_grounding_inventory.py`.
- Added CLI command `aec-source-grounding-inventory`.
- Added `SOURCE_GROUNDED_ANSWER_CONTEXT_SCHEMA_VERSION` and `POST /v2/answer/context`.
- Added `sourceGroundedContext` to AEC `/node/:id` responses.
- Added Explorer NodeInspector Context tab.
- Updated source-grounded tracker and active-work state.

## Validation Commands

```bash
python -m py_compile scripts/vitruvius/kg/source_grounding_inventory.py scripts/pipeline_cli.py
$env:PYTHONPATH='scripts'; python -m pytest scripts/tests/test_kg_source_grounding_inventory.py -q
$env:PYTHONPATH='scripts'; python -m pytest scripts/tests/test_kg_aec_relationship_improvement.py -q
$env:PYTHONPATH='scripts'; python -m pytest scripts/tests/test_kg_backbone_shadow_staging.py scripts/tests/test_kg_backbone_graph_quality.py -q
bun test api/v2Backbone.test.ts --timeout 20000
bun test explorer/src/components/componentInteraction.test.tsx --timeout 20000
bun test explorer/src/api/graphApi.test.ts --timeout 20000
bun run --cwd explorer build
python scripts/pipeline_cli.py aec-source-grounding-inventory --run-id SOURCE_GROUNDING_SMOKE --relationship-run-id latest --max-gap-examples 5
```

## Results

- Source-grounding inventory tests: 3 passed.
- AEC relationship-improvement tests: 138 passed.
- Backbone shadow/graph quality tests: 18 passed.
- API backbone tests: 82 passed.
- Explorer component tests: 29 passed.
- Explorer API client tests: 8 passed.
- Explorer build: passed.
- CLI smoke wrote only `006_System-Manifests/aec-mepfs-backbone/source-grounding-inventory/SOURCE_GROUNDING_SMOKE/`.

## Smoke Metrics

`SOURCE_GROUNDING_SMOKE` reported:

- nodes: 10,018
- relationships: 13,670
- source-backed nodes: 8
- source-backed relationships: 4,344
- pending relationship overlays: 2,757
- pending node-consolidation overlays: 1,255

## Boundaries

- No active graph mutation.
- No Neo4j or Postgres writes.
- No Resource Layer mutation.
- Pending overlay records remain proposals only.
- No protected source text, API keys, or `reasoning_content` are included in the context packet or inventory report.

## Caveats

- `bash ./scripts/refresh_code_intelligence.sh` rebuilt the structural code-review graph but reported missing `tree-sitter-yaml` warnings and oversized embedding errors from large campaign logs.
- The first implementation is a deterministic context packet and Explorer display, not an answer composer.
