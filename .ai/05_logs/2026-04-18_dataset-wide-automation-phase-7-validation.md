# 2026-04-18 Validation — Dataset-wide automation phase 7

## Change
- added starter-family scaffolding command:
  - `scaffold-completed-aggregate-family`
- this bootstraps the remaining manual onboarding artifacts for a brand-new dataset family:
  - starter completed-lanes ledger
  - starter manifest index
  - profile YAML
  - catalog entry

## Fresh verification
- focused scaffolding/profile/catalog regression:
  - `python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py -k 'scaffold_completed_aggregate_family_writes_starter_files or pipeline_cli_scaffold_completed_aggregate_family_writes_starter_files or register_completed_aggregate_family_writes_profile_and_catalog or pipeline_cli_register_completed_aggregate_family_writes_profile_and_catalog or resolve_completed_aggregate_profile_path_returns_registered_profile or pipeline_cli_build_completed_aggregate_manifest_writes_manifest or pipeline_cli_run_completed_aggregate_invokes_dataset_pipeline or pipeline_cli_build_completed_aggregate_from_profile_writes_manifest or pipeline_cli_run_completed_aggregate_from_profile_invokes_dataset_pipeline or pipeline_cli_run_completed_aggregate_family_invokes_dataset_pipeline or generic_completed_manifest_paths_returns_existing_manifests or build_laws_completed_aggregate_manifest or run_laws_completed_aggregate or raw_folder_name_override or manifest_scoped_variants or scoped_variants_for_duplicates' -q`
  - **16 passed**
- scaffold command sanity check:
  - `python3 scripts/pipeline_cli.py scaffold-completed-aggregate-family --family history-demo --catalog config/datasets/dataset-mvp-profile-catalog.yaml --dataset-kind history-aggregate --note 'History demo scaffold family.'`
  - surfaced:
    - `profile_path = config/datasets/history-demo-mvp-profile.yaml`
    - `completed_ledger_path = config/datasets/history-demo-completed-lanes.yaml`
    - `manifest_index_path = config/datasets/history-demo-manifest-index.yaml`
    - `dataset_id = history-demo-aggregate`
  - scaffolded file contents verified:
    - `completed_lanes: []`
    - `manifests: []`
- temporary `history-demo` scaffold artifacts were then removed so the repo truth remains focused on committed families only

## Truthful result
- onboarding a brand-new dataset family no longer requires hand-authoring any starter aggregate files
- the remaining missing proof is still not scaffolding but content readiness:
  - a true non-laws family with completed lanes admitted into its ledger/index pair
