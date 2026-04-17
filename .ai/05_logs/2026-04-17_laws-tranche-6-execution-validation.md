# 2026-04-17 Validation — Laws tranche-6 bounded execution

## Manifest
- `config/datasets/laws-tranche-6.yaml`

## Selected tranche-6 laws
- `RA-4566`
- `RA-386`
- `RA-9184`

## Selection rationale
- zero exact duplicate clusters in the selected cohort
- explicit exclusion of the current `RA-9266` duplicate-risk lane
- all selected files are direct-input PDFs in source-prep dry-run

## Fresh verification
- `python3 -m pytest scripts/tests/test_canonical_rules_additional_laws.py -q`
  - **24 passed**
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-duplicate-dry-run --tranche-manifest config/datasets/laws-tranche-6.yaml`
  - `duplicate_cluster_count = 0`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-prep --tranche-manifest config/datasets/laws-tranche-6.yaml`
  - `prepared_count = 7`
  - `ocr_required_count = 0`
  - `failed_count = 0`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-admission --tranche-manifest config/datasets/laws-tranche-6.yaml`
  - `admitted_source_page_count = 4`
  - `blocked_law_folders = []`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-to-graph --tranche-manifest config/datasets/laws-tranche-6.yaml --review-preset m2-8gb-safe`
  - `generated_relationship_count = 3`
  - `spot_review_required_count = 1`
  - `summary_auto_withheld_count = 1`
  - `shallow_representation_count = 0`
  - graph snapshot: `7 nodes / 9 edges`

## Truthful residuals
- tranche-6 is no longer representationally shallow
- tranche-6 still carries explicit raw-alias visibility for `RA-386` and `RA-9184`
- tranche-6 still carries one spot-review signal in the updated 2016 RA-9184 IRR surface
