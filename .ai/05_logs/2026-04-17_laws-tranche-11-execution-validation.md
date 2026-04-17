# 2026-04-17 Validation — Laws tranche-11 bounded execution

## Manifest
- `config/datasets/laws-tranche-11.yaml`

## Selected tranche-11 law
- `PD-9514`

## Selection rationale
- overlap-closure singleton lane for the fire-code statute/IRR family
- reuses existing fire-code concepts and relationships rather than inventing a new fire-code concept family
- direct-prep and duplicate-free in this singleton lane

## Fresh verification
- `python3 -m pytest scripts/tests/test_canonical_rules_additional_laws.py -q`
  - **34 passed**
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-duplicate-dry-run --tranche-manifest config/datasets/laws-tranche-11.yaml`
  - `duplicate_cluster_count = 0`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-prep --tranche-manifest config/datasets/laws-tranche-11.yaml`
  - `prepared_count = 1`
  - `failed_count = 0`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-admission --tranche-manifest config/datasets/laws-tranche-11.yaml`
  - `admitted_source_page_count = 1`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-to-graph --tranche-manifest config/datasets/laws-tranche-11.yaml --review-preset m2-8gb-safe`
  - `generated_relationship_count = 7`
  - `filtered_relationship_count = 1`
  - `shallow_representation_count = 0`
  - graph snapshot: `10 nodes / 10 edges`

## Truthful residuals
- tranche-11 is no longer graph-light
- it is still an overlap-closure lane, not a net-new domain lane
