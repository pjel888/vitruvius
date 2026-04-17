# 2026-04-18 Validation — Dataset-wide automation phase 5

## Change
- added a dataset-family catalog/alias operator path on top of the profile-driven generic aggregate flow:
  - `run-completed-aggregate-family`
  - `./run-dataset-mvp-graph --family <family>`
- added the first family catalog entry:
  - `laws`
- simplified the laws wrapper again:
  - `./run-laws-mvp-graph`
  - now delegates through the generic family alias path instead of hardcoding the profile path directly

## Fresh verification
- focused family-alias regression:
  - `python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py -k 'resolve_completed_aggregate_profile_path_returns_registered_profile or pipeline_cli_build_completed_aggregate_manifest_writes_manifest or pipeline_cli_run_completed_aggregate_invokes_dataset_pipeline or pipeline_cli_build_completed_aggregate_from_profile_writes_manifest or pipeline_cli_run_completed_aggregate_from_profile_invokes_dataset_pipeline or pipeline_cli_run_completed_aggregate_family_invokes_dataset_pipeline or generic_completed_manifest_paths_returns_existing_manifests or build_laws_completed_aggregate_manifest or run_laws_completed_aggregate or raw_folder_name_override or manifest_scoped_variants or scoped_variants_for_duplicates' -q`
  - **12 passed**
- wrapper/CLI family dry-run sanity checks:
  - `./run-dataset-mvp-graph --family laws --dry-run --review-preset m2-8gb-safe --skip-export-owl`
  - `./run-laws-mvp-graph --dry-run --review-preset m2-8gb-safe --skip-export-owl`
  - both surface:
    - `action = build-completed-aggregate-manifest`
    - `action = run-dataset-source-to-graph`
    - `planned_stage_count = 64`

## Truthful result
- operators now have three additive onboarding surfaces:
  - raw parameter bundle
  - profile YAML
  - family alias from a catalog
- the laws MVP is now a thin specialization of the most reusable path so far:
  - generic wrapper
  - family catalog
  - family profile
  - generic aggregate execution
