# 2026-04-18 Validation — Dataset-wide automation phase 8

## Change
- added completed-manifest admission command for scaffolded/registered dataset families:
  - `admit-completed-aggregate-manifest`
- this updates a family's:
  - completed-lanes ledger
  - manifest index
- this removes the next remaining manual onboarding step between scaffold/registration and aggregate run

## Fresh verification
- focused admission/profile/catalog regression:
  - `python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py -k 'admit_completed_manifest_to_family_updates_ledger_and_index or pipeline_cli_admit_completed_aggregate_manifest_updates_family_ledgers or scaffold_completed_aggregate_family_writes_starter_files or pipeline_cli_scaffold_completed_aggregate_family_writes_starter_files or register_completed_aggregate_family_writes_profile_and_catalog or pipeline_cli_register_completed_aggregate_family_writes_profile_and_catalog or resolve_completed_aggregate_profile_path_returns_registered_profile or pipeline_cli_build_completed_aggregate_manifest_writes_manifest or pipeline_cli_run_completed_aggregate_invokes_dataset_pipeline or pipeline_cli_build_completed_aggregate_from_profile_writes_manifest or pipeline_cli_run_completed_aggregate_from_profile_invokes_dataset_pipeline or pipeline_cli_run_completed_aggregate_family_invokes_dataset_pipeline or generic_completed_manifest_paths_returns_existing_manifests or build_laws_completed_aggregate_manifest or run_laws_completed_aggregate or raw_folder_name_override or manifest_scoped_variants or scoped_variants_for_duplicates' -q`
  - **18 passed**
- temporary scaffold + admission demo:
  - scaffolded `history-demo`
  - created temporary manifest `config/datasets/history-lane-1.yaml`
  - admitted it with:
    - `python3 scripts/pipeline_cli.py admit-completed-aggregate-manifest --family history-demo --catalog config/datasets/dataset-mvp-profile-catalog.yaml --lane-id history-lane-1 --manifest config/datasets/history-lane-1.yaml`
  - verified ledger/index update semantics in tests and command output
- temporary `history-demo` artifacts were then removed so repo truth remains focused on committed families only

## Truthful result
- a new dataset family can now progress through:
  - scaffold starter artifacts
  - register catalog/profile entry
  - admit completed manifests
  - run by family alias
- the remaining missing proof is no longer wiring, but actual content readiness:
  - first true non-laws family with trusted completed manifests admitted into its ledgers
