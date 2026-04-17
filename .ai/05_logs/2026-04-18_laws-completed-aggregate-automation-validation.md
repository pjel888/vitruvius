# 2026-04-18 Validation — Completed-laws aggregate automation

## New automation surfaces
- `python3 scripts/pipeline_cli.py build-laws-completed-aggregate-manifest`
- `python3 scripts/pipeline_cli.py run-laws-completed-aggregate --dry-run --review-preset m2-8gb-safe`
- `python3 scripts/pipeline_cli.py run-laws-completed-aggregate --review-preset m2-8gb-safe`

## Aggregate manifest generation
- output:
  - `config/datasets/laws-completed-aggregate.yaml`
- current generated summary:
  - `law_unit_count = 48`
  - `source_count = 65`
  - `concept_count = 92`
  - `relationship_count = 127`
  - `raw_slice_anchor_count = 41`

## Focused regression
- `python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py -k 'build_laws_completed_aggregate_manifest or run_laws_completed_aggregate or raw_folder_name_override or manifest_scoped_variants or scoped_variants_for_duplicates' -q`
  - **5 passed**
- `python3 -m pytest scripts/tests/test_canonical_rules_additional_laws.py -q`
  - **62 passed**

## Aggregate dry-run
- `python3 scripts/pipeline_cli.py run-laws-completed-aggregate --dry-run --review-preset m2-8gb-safe`
- current dry-run evidence:
  - `planned_stage_count = 64`
  - `manual_review_required_count = 7`
  - `spot_review_required_count = 24`
  - `summary_auto_withheld_count = 24`
  - `shallow_representation_count = 3`
  - `benchmark_hint_count = 5`

## Aggregate execute
- `python3 scripts/pipeline_cli.py run-laws-completed-aggregate --review-preset m2-8gb-safe`
- current execute evidence:
  - `generated_relationship_count = 75`
  - `filtered_relationship_count = 3`
  - `manual_review_required_count = 7`
  - `spot_review_required_count = 24`
  - `summary_auto_withheld_count = 24`
  - `shallow_representation_count = 3`
  - graph snapshot: `126 nodes / 260 edges`

## Truthful result
- there is now a one-command path to build a graph over the completed authoritative laws-wave dataset
- the aggregate command does not silently include deferred residual folders
- the aggregate graph is now large enough to inspect interconnectivity and shared concepts across completed laws-wave lanes
