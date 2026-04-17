# 2026-04-17 Validation — Laws tranche-8 bounded execution

## Manifest
- `config/datasets/laws-tranche-8.yaml`

## Selected tranche-8 law
- `RA-11285`

## Selection rationale
- direct singleton widening lane with distinct energy-governance scope
- duplicate-free
- OCR-first preparation succeeds with the current local OCR stack
- preferred over `PD-9514` because it is net-new rather than fire-code overlap-heavy

## Fresh verification
- `python3 -m pytest scripts/tests/test_canonical_rules_additional_laws.py -q`
  - **29 passed**
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-duplicate-dry-run --tranche-manifest config/datasets/laws-tranche-8.yaml`
  - `duplicate_cluster_count = 0`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-prep --tranche-manifest config/datasets/laws-tranche-8.yaml --allow-ocr`
  - `prepared_count = 1`
  - `ocr_required_count = 0`
  - `failed_count = 0`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-admission --tranche-manifest config/datasets/laws-tranche-8.yaml`
  - `admitted_source_page_count = 1`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-to-graph --tranche-manifest config/datasets/laws-tranche-8.yaml --review-preset m2-8gb-safe`
  - `generated_relationship_count = 0`
  - `spot_review_required_count = 1`
  - `summary_auto_withheld_count = 1`
  - `shallow_representation_count = 0`
  - graph snapshot: `4 nodes / 6 edges`

## Truthful residuals
- tranche-8 is no longer representationally shallow
- tranche-8 still carries one spot-review / summary-withheld signal from the OCR-first RA-11285 surface
