# 2026-04-18 Validation — Dataset-wide automation phase 4

## Change
- added a profile-driven generic aggregate operator path:
  - `build-completed-aggregate-from-profile`
  - `run-completed-aggregate-from-profile`
  - `./run-dataset-mvp-graph`
- converted the laws MVP wrapper into a thin specialization over the generic profile-driven operator path:
  - `./run-laws-mvp-graph`
  - now delegates to `./run-dataset-mvp-graph --profile config/datasets/laws-mvp-profile.yaml`

## Fresh verification
- focused profile-path regression:
  - `python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py -k 'generic_completed_manifest_paths_returns_existing_manifests or pipeline_cli_build_completed_aggregate_manifest_writes_manifest or pipeline_cli_run_completed_aggregate_invokes_dataset_pipeline or pipeline_cli_build_completed_aggregate_from_profile_writes_manifest or pipeline_cli_run_completed_aggregate_from_profile_invokes_dataset_pipeline or build_laws_completed_aggregate_manifest or run_laws_completed_aggregate or raw_folder_name_override or manifest_scoped_variants or scoped_variants_for_duplicates' -q`
  - **10 passed**
- canonical law-rule regression:
  - `python3 -m pytest scripts/tests/test_canonical_rules_additional_laws.py -q`
  - **62 passed**
- profile build sanity check:
  - `python3 scripts/pipeline_cli.py build-completed-aggregate-from-profile --profile config/datasets/laws-mvp-profile.yaml`
  - result:
    - `law_unit_count = 48`
    - `source_count = 65`
    - `concept_count = 92`
    - `relationship_count = 127`
    - `raw_slice_anchor_count = 41`
- profile run dry-run sanity check:
  - `python3 scripts/pipeline_cli.py run-completed-aggregate-from-profile --profile config/datasets/laws-mvp-profile.yaml --dry-run --review-preset m2-8gb-safe --skip-export-owl`
  - result:
    - `planned_stage_count = 64`
    - `manual_review_required_count = 7`
    - `spot_review_required_count = 24`
    - `summary_auto_withheld_count = 24`
    - `shallow_representation_count = 3`
    - `benchmark_hint_count = 5`

## Truthful result
- the dataset-wide operator surface no longer requires repeating a long set of aggregate parameters at runtime
- the reusable onboarding unit is now a profile YAML plus the generic wrapper
- the laws MVP remains intact while becoming a thin specialization of the generic profile-driven path
