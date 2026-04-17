# 2026-04-18 Validation — Dataset-wide automation phase 6

## Change
- added a one-command family registration/scaffolding surface:
  - `register-completed-aggregate-family`
- proved reusable onboarding with a registered demo family:
  - `laws-demo`
- the new command writes:
  - a profile YAML
  - a catalog entry
- the registered family then runs through:
  - `./run-dataset-mvp-graph --family laws-demo`

## Fresh verification
- focused registration/profile/catalog regression:
  - `python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py -k 'register_completed_aggregate_family_writes_profile_and_catalog or pipeline_cli_register_completed_aggregate_family_writes_profile_and_catalog or resolve_completed_aggregate_profile_path_returns_registered_profile or pipeline_cli_build_completed_aggregate_manifest_writes_manifest or pipeline_cli_run_completed_aggregate_invokes_dataset_pipeline or pipeline_cli_build_completed_aggregate_from_profile_writes_manifest or pipeline_cli_run_completed_aggregate_from_profile_invokes_dataset_pipeline or pipeline_cli_run_completed_aggregate_family_invokes_dataset_pipeline or generic_completed_manifest_paths_returns_existing_manifests or build_laws_completed_aggregate_manifest or run_laws_completed_aggregate or raw_folder_name_override or manifest_scoped_variants or scoped_variants_for_duplicates' -q`
  - **14 passed**
- demo family registration:
  - `python3 scripts/pipeline_cli.py register-completed-aggregate-family --family laws-demo ...`
  - result:
    - `profile_path = config/datasets/laws-demo-profile.yaml`
    - `catalog_path = config/datasets/dataset-mvp-profile-catalog.yaml`
    - `dataset_id = laws-demo-aggregate`
- demo family run dry-run:
  - `./run-dataset-mvp-graph --family laws-demo --dry-run --review-preset m2-8gb-safe --skip-export-owl`
  - surfaced:
    - `action = build-completed-aggregate-manifest`
    - `action = run-dataset-source-to-graph`
    - `dataset_id = laws-demo-aggregate`
    - `planned_stage_count = 64`

## Truthful result
- onboarding a new dataset family no longer requires hand-editing both a profile and a catalog entry
- a reusable demo family is now registered and runnable through the same generic family path
- the remaining missing proof is still:
  - a first true non-laws trusted dataset family with its own completed-ledger and manifest-index pair
