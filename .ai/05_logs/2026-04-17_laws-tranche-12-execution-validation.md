# 2026-04-17 Validation — Laws tranche-12 bounded execution

## Manifest
- `config/datasets/laws-tranche-12.yaml`

## Selected tranche-12 scoped surfaces
### EO
- `EO 72 Comprehensive Land use.pdf`
- `EO 90 NGO for Shelter Program.pdf`
- `EO 648 Chapter of the Human Settlements Regulatory Commissio.pdf`

### DHSUD
- `Open Space Development Guidelines.pdf`
- `Resilient Urban Design and Development Guidelines.pdf`

## Fresh verification
- `python3 -m pytest scripts/tests/test_canonical_rules_additional_laws.py -q`
  - **39 passed**
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-duplicate-dry-run --tranche-manifest config/datasets/laws-tranche-12.yaml`
  - `duplicate_cluster_count = 1`
  - `duplicate_law_folders = [EO]`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-prep --tranche-manifest config/datasets/laws-tranche-12.yaml`
  - `prepared_count = 5`
  - `failed_count = 0`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-admission --tranche-manifest config/datasets/laws-tranche-12.yaml`
  - `admitted_source_page_count = 5`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-to-graph --tranche-manifest config/datasets/laws-tranche-12.yaml --review-preset m2-8gb-safe`
  - `staged_law_folders = [EO, DHSUD]`
  - `duplicate_law_folders = [EO]`
  - `raw_alias_law_folders = [EO, DHSUD]`
  - `generated_relationship_count = 3`
  - `shallow_representation_count = 0`
  - graph snapshot: `7 nodes / 6 edges`

## Truthful residuals
- tranche-12 is operationally clean on the scoped guidance surfaces
- `EO` still carries explicit duplicate/raw-alias visibility
- `DHSUD` remains only partially connected in graph terms; it is staged but still more guidance-heavy than statute-heavy
- the raw storage folder remains `HLURB-DHSUD`, but the staged 2025 guidance documents are explicitly DHSUD publications
