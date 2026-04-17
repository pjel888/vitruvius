# 2026-04-18 Validation — Dataset-wide automation phase 9

## Change
- added family readiness-check command:
  - `check-completed-aggregate-family`
- this surfaces structured blockers for scaffolded or partially onboarded families before a run attempt

## Fresh verification
- focused readiness/admission/scaffolding regression:
  - `python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py -k 'check_completed_aggregate_family_readiness_reports_blockers or check_completed_aggregate_family_readiness_reports_ready_family or pipeline_cli_check_completed_aggregate_family_reports_blockers or admit_completed_manifest_to_family_updates_ledger_and_index or pipeline_cli_admit_completed_aggregate_manifest_updates_family_ledgers or scaffold_completed_aggregate_family_writes_starter_files or pipeline_cli_scaffold_completed_aggregate_family_writes_starter_files or register_completed_aggregate_family_writes_profile_and_catalog or pipeline_cli_register_completed_aggregate_family_writes_profile_and_catalog or resolve_completed_aggregate_profile_path_returns_registered_profile or pipeline_cli_build_completed_aggregate_manifest_writes_manifest or pipeline_cli_run_completed_aggregate_invokes_dataset_pipeline or pipeline_cli_build_completed_aggregate_from_profile_writes_manifest or pipeline_cli_run_completed_aggregate_from_profile_invokes_dataset_pipeline or pipeline_cli_run_completed_aggregate_family_invokes_dataset_pipeline or generic_completed_manifest_paths_returns_existing_manifests or build_laws_completed_aggregate_manifest or run_laws_completed_aggregate or raw_folder_name_override or manifest_scoped_variants or scoped_variants_for_duplicates' -q`
  - **21 passed**
- temporary scaffold + readiness demo:
  - scaffolded `history-demo`
  - checked with:
    - `python3 scripts/pipeline_cli.py check-completed-aggregate-family --family history-demo --catalog config/datasets/dataset-mvp-profile-catalog.yaml`
  - surfaced:
    - `ready_to_run = false`
    - blocker: `no completed lanes admitted`
    - blocker: `no completed manifests resolved from ledger/index`
- temporary `history-demo` artifacts were removed after validation so repo truth remains focused on committed families only

## Truthful result
- a new family can now be scaffolded, registered, admitted, and checked for readiness without hand-reading internal manifest errors
- the remaining missing proof is still content, not orchestration:
  - first true non-laws trusted family with admitted completed manifests
