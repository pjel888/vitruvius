# 2026-04-17 Validation — Laws tranche-10 bounded execution

## Manifest
- `config/datasets/laws-tranche-10.yaml`

## Selected tranche-10 law
- `RA-9266`

## Selection rationale
- duplicate-remediation-first singleton lane
- explicit authoritative/excluded variant handling for the byte-identical raw pair
- keeps duplicate/raw-alias visibility explicit while allowing bounded execution

## Fresh verification
- `python3 -m pytest scripts/tests/test_canonical_rules_additional_laws.py -q`
  - **33 passed**
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-duplicate-dry-run --tranche-manifest config/datasets/laws-tranche-10.yaml`
  - `duplicate_cluster_count = 1`
  - `duplicate_law_folders = [RA-9266]`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-prep --tranche-manifest config/datasets/laws-tranche-10.yaml`
  - `prepared_count = 1`
  - `failed_count = 0`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-admission --tranche-manifest config/datasets/laws-tranche-10.yaml`
  - `admitted_source_page_count = 1`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-to-graph --tranche-manifest config/datasets/laws-tranche-10.yaml --review-preset m2-8gb-safe`
  - `staged_law_folders = [RA-9266]`
  - `raw_alias_law_folders = [RA-9266]`
  - `guardrail_law_folders = [RA-9266]`
  - `generated_relationship_count = 0`
  - `shallow_representation_count = 0`
  - graph snapshot: `1 nodes / 0 edges`

## Truthful residuals
- tranche-10 is operationally clean as a duplicate-remediation lane
- tranche-10 remains graph-light because it carries only the authoritative IRR source without further concept-fit work
