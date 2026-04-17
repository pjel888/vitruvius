# 2026-04-17 Validation — RA-9184 procurement concept-fit

## Scope
Admit the smallest tranche-6 concept-fit slice needed to remove RA-9184's shallow-representation finding.

## Admitted concepts
- `concept-approved-budget-for-the-contract`
- `concept-bids-and-awards-committee`
- `concept-competitive-bidding`

## Admitted dataset-scoped relationships
- `law-government-procurement-reform-act governs concept-approved-budget-for-the-contract`
- `law-government-procurement-reform-act governs concept-bids-and-awards-committee`
- `law-government-procurement-reform-act governs concept-competitive-bidding`

## Fresh verification
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-to-graph-dry-run --tranche-manifest config/datasets/laws-tranche-6.yaml --review-preset m2-8gb-safe`
  - `shallow_representation_count = 0`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-to-graph --tranche-manifest config/datasets/laws-tranche-6.yaml --review-preset m2-8gb-safe`
  - `generated_relationship_count = 3`
  - `shallow_representation_count = 0`
  - graph snapshot: `7 nodes / 9 edges`

## Truthful residuals
- tranche-6 still has one spot-review signal from the updated 2016 IRR surface, but representationally it is no longer shallow
