# 2026-04-18 Validation — Laws MVP graph command

## Operator command
- `./run-laws-mvp-graph --review-preset m2-8gb-safe`

## Supporting automation commands
- `python3 scripts/pipeline_cli.py build-laws-completed-aggregate-manifest`
- `python3 scripts/pipeline_cli.py run-laws-completed-aggregate --dry-run --review-preset m2-8gb-safe`
- `python3 scripts/pipeline_cli.py run-laws-completed-aggregate --review-preset m2-8gb-safe`

## Fresh verification
- aggregate automation tests:
  - `python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py -k 'build_laws_completed_aggregate_manifest or run_laws_completed_aggregate or raw_folder_name_override or manifest_scoped_variants or scoped_variants_for_duplicates' -q`
  - **5 passed**
- canonical-rule tests:
  - `python3 -m pytest scripts/tests/test_canonical_rules_additional_laws.py -q`
  - **62 passed**
- aggregate manifest generation:
  - `law_unit_count = 48`
  - `source_count = 65`
  - `concept_count = 92`
  - `relationship_count = 127`
  - `raw_slice_anchor_count = 41`
- aggregate dry-run:
  - `planned_stage_count = 64`
  - `manual_review_required_count = 7`
  - `spot_review_required_count = 24`
  - `summary_auto_withheld_count = 24`
  - `shallow_representation_count = 3`
  - `benchmark_hint_count = 5`
- aggregate execute:
  - `generated_relationship_count = 75`
  - `filtered_relationship_count = 3`
  - `manual_review_required_count = 7`
  - `spot_review_required_count = 24`
  - `summary_auto_withheld_count = 24`
  - `shallow_representation_count = 3`
  - graph snapshot: `126 nodes / 260 edges`

## Truthful result
- a one-command aggregate graph path now exists for the completed authoritative laws wave
- this is the current MVP for seeing interconnectedness across the completed laws dataset
- deferred residual folders are still intentionally excluded for integrity
