# 2026-04-18 Validation — Dataset-wide automation phase 3

## Change
- added the first generic aggregate execute CLI command surface:
  - `run-completed-aggregate`
- preserved the laws-specific MVP as a thin specialization above the reusable aggregate helper and the new generic execute path

## Fresh verification
- focused aggregate automation regression:
  - `python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py -k 'generic_completed_manifest_paths_returns_existing_manifests or pipeline_cli_build_completed_aggregate_manifest_writes_manifest or pipeline_cli_run_completed_aggregate_invokes_dataset_pipeline or build_laws_completed_aggregate_manifest or run_laws_completed_aggregate or raw_folder_name_override or manifest_scoped_variants or scoped_variants_for_duplicates' -q`
  - **8 passed**
- canonical law-rule regression:
  - `python3 -m pytest scripts/tests/test_canonical_rules_additional_laws.py -q`
  - **62 passed**
- generic execute dry-run sanity check:
  - `python3 scripts/pipeline_cli.py run-completed-aggregate --completed-ledger config/datasets/laws-completed-lanes.yaml --manifest-index config/datasets/laws-manifest-index.yaml --dataset-id laws-generic-run-check --dataset-kind laws-aggregate --out config/datasets/laws-generic-run-check.yaml --graph-output-root 005_Operational-Intelligence-Layer/graph/datasets/laws-generic-run-check --run-output-root 006_System-Manifests/runs/datasets/laws-generic-run-check --query-snapshot-template 005_Operational-Intelligence-Layer/graph/datasets/laws-generic-run-check/{run_id}_graph_snapshot.json --dry-run --review-preset m2-8gb-safe --skip-export-owl`
  - result:
    - `law_unit_count = 48`
    - `source_count = 65`
    - `concept_count = 92`
    - `relationship_count = 127`
    - `raw_slice_anchor_count = 41`
    - `planned_stage_count = 64`
    - `manual_review_required_count = 7`
    - `spot_review_required_count = 24`
    - `summary_auto_withheld_count = 24`
    - `shallow_representation_count = 3`
    - `benchmark_hint_count = 5`

## Truthful result
- the aggregate command surface is no longer limited to:
  - generic build only
- it now supports:
  - generic build
  - generic dry-run/execute
- the laws MVP remains intact while the dataset-wide command pattern becomes reusable beyond laws-specific orchestration
