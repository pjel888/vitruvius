# 2026-04-18 Validation — Dataset-wide automation phase 12

## Change
- added starter lane source-preparation command:
  - `prepare-completed-aggregate-lane-sources`
- this brings scaffolded starter lanes one step closer to truthful canonical admission by generating source-prep reports from the lane manifest itself

## Fresh verification
- focused starter-lane source-prep/regression suite:
  - `python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py -k 'prepare_completed_aggregate_lane_sources_dry_run_reports_inventory or prepare_completed_aggregate_lane_sources_execute_uses_prepare_helper or pipeline_cli_prepare_completed_aggregate_lane_sources_dry_run_reports_inventory or inspect_completed_aggregate_lane_sources_reports_inventory or pipeline_cli_inspect_completed_aggregate_lane_sources_reports_inventory or scaffold_completed_aggregate_lane_manifest_writes_starter_manifest or pipeline_cli_scaffold_completed_aggregate_lane_manifest_writes_manifest or check_completed_aggregate_family_readiness_reports_blockers or check_completed_aggregate_family_readiness_reports_ready_family or pipeline_cli_check_completed_aggregate_family_reports_blockers or admit_completed_manifest_to_family_updates_ledger_and_index or pipeline_cli_admit_completed_aggregate_manifest_updates_family_ledgers or scaffold_completed_aggregate_family_writes_starter_files or pipeline_cli_scaffold_completed_aggregate_family_writes_starter_files or register_completed_aggregate_family_writes_profile_and_catalog or pipeline_cli_register_completed_aggregate_family_writes_profile_and_catalog or resolve_completed_aggregate_profile_path_returns_registered_profile or pipeline_cli_build_completed_aggregate_manifest_writes_manifest or pipeline_cli_run_completed_aggregate_invokes_dataset_pipeline or pipeline_cli_build_completed_aggregate_from_profile_writes_manifest or pipeline_cli_run_completed_aggregate_from_profile_invokes_dataset_pipeline or pipeline_cli_run_completed_aggregate_family_invokes_dataset_pipeline or generic_completed_manifest_paths_returns_existing_manifests or build_laws_completed_aggregate_manifest or run_laws_completed_aggregate or raw_folder_name_override or manifest_scoped_variants or scoped_variants_for_duplicates' -q`
  - **28 passed**
- temporary non-laws starter-lane source-prep demo:
  - scaffolded family: `history-demo`
  - scaffolded starter lane: `history-lane-starter`
  - dry-run prepared with:
    - `python3 scripts/pipeline_cli.py prepare-completed-aggregate-lane-sources --manifest config/datasets/history-lane-starter.yaml --dry-run`
  - surfaced:
    - `action = prepare-completed-aggregate-lane-sources-dry-run`
    - `raw_file_count = 1`
    - `supported_direct_input_count = 1`
    - source-prep `report_path` under the lane run root
- temporary `history-demo` artifacts were removed after validation so repo truth remains focused on committed families only

## Truthful result
- a brand-new non-laws family can now reach all the way through:
  - family scaffold
  - registration
  - starter lane scaffold
  - starter lane inspection
  - starter lane source-prep dry-run/execute
- the next remaining manual/truthful step is canonical source/relationship admission, not raw-file preparation plumbing
