# 2026-04-18 Validation — Dataset-wide automation phase 2

## Change
- added a generic aggregate-manifest CLI command surface:
  - `build-completed-aggregate-manifest`
- the existing laws-specific command remains as a thin specialization above the extracted helper

## Fresh verification
- `python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py -k 'generic_completed_manifest_paths_returns_existing_manifests or build_laws_completed_aggregate_manifest or run_laws_completed_aggregate' -q`
  - **3 passed**
- generic command sanity check:
  - `python3 scripts/pipeline_cli.py build-completed-aggregate-manifest --completed-ledger config/datasets/laws-completed-lanes.yaml --manifest-index config/datasets/laws-manifest-index.yaml --dataset-id laws-generic-check --dataset-kind laws-aggregate --out config/datasets/laws-generic-check.yaml --graph-output-root 005_Operational-Intelligence-Layer/graph/datasets/laws-generic-check --run-output-root 006_System-Manifests/runs/datasets/laws-generic-check --query-snapshot-template 005_Operational-Intelligence-Layer/graph/datasets/laws-generic-check/{run_id}_graph_snapshot.json`
  - result:
    - `law_unit_count = 48`
    - `source_count = 65`
    - `concept_count = 92`
    - `relationship_count = 127`
    - `raw_slice_anchor_count = 41`

## Truthful result
- the aggregate-manifest build path is no longer laws-only at the command-surface level
- the laws-specific MVP remains intact while the generic command layer begins to emerge
