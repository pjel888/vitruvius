# 2026-04-17 Validation — RA-11285 energy-governance concept-fit

## Scope
Admit the smallest tranche-8 concept-fit slice needed to remove RA-11285's shallow-representation finding.

## Admitted concepts
- `concept-energy-audit`
- `concept-designated-establishment`
- `concept-minimum-energy-performance`

## Admitted dataset-scoped relationships
- `law-energy-efficiency-and-conservation-act governs concept-energy-audit`
- `law-energy-efficiency-and-conservation-act governs concept-designated-establishment`
- `law-energy-efficiency-and-conservation-act governs concept-minimum-energy-performance`

## Fresh verification
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-to-graph-dry-run --tranche-manifest config/datasets/laws-tranche-8.yaml --review-preset m2-8gb-safe`
  - `shallow_representation_count = 0`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-to-graph --tranche-manifest config/datasets/laws-tranche-8.yaml --review-preset m2-8gb-safe`
  - `shallow_representation_count = 0`
  - graph snapshot: `4 nodes / 6 edges`

## Truthful residuals
- representationally, tranche-8 is no longer shallow
- the OCR-first law surface still carries spot-review and summary-withheld signals
