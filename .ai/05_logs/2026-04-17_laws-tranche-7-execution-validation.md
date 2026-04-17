# 2026-04-17 Validation — Laws tranche-7 bounded execution

## Manifest
- `config/datasets/laws-tranche-7.yaml`

## Selected tranche-7 laws
- `RA-1378`
- `RA-9285`
- `RA-11201`

## Fresh verification
- `python3 -m pytest scripts/tests/test_canonical_rules_additional_laws.py -q`
  - **28 passed**
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-duplicate-dry-run --tranche-manifest config/datasets/laws-tranche-7.yaml`
  - `duplicate_cluster_count = 0`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-to-graph --tranche-manifest config/datasets/laws-tranche-7.yaml --review-preset m2-8gb-safe`
  - `staged_law_folders = [RA-9285, RA-11201]`
  - `blocked_law_folders = [RA-1378]`
  - `generated_relationship_count = 0`
  - `shallow_representation_count = 0`
  - graph snapshot: `6 nodes / 6 edges`

## Truthful residuals
- tranche-7 is representationally sound for the currently staged laws
- `RA-1378` remains outside staged execution because the tranche still needs a clean source-prep execute report that reflects manifest-scoped exclusion of auxiliary plumbing files
- tranche-7 still carries `spot_review_required_count = 2` and `summary_auto_withheld_count = 2`
