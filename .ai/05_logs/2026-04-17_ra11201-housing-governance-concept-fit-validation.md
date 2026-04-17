# 2026-04-17 Validation — RA-11201 housing-governance concept-fit

## Scope
Admit the smallest tranche-7 concept-fit slice needed to remove RA-11201's shallow-representation finding.

## Admitted concepts
- `concept-human-settlements`
- `concept-urban-development-planning`
- `concept-local-shelter-plan`

## Admitted dataset-scoped relationships
- `law-department-of-human-settlements-and-urban-development-act governs concept-human-settlements`
- `law-department-of-human-settlements-and-urban-development-act governs concept-urban-development-planning`
- `irr-implementing-rules-and-regulations-of-the-department-of-human-settlements-and-urban-development-act governs concept-local-shelter-plan`

## Fresh verification
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-to-graph-dry-run --tranche-manifest config/datasets/laws-tranche-7.yaml --review-preset m2-8gb-safe`
  - `shallow_representation_count = 0`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-to-graph --tranche-manifest config/datasets/laws-tranche-7.yaml --review-preset m2-8gb-safe`
  - `shallow_representation_count = 0`
  - graph snapshot: `6 nodes / 6 edges`

## Truthful residuals
- representationally, the staged tranche-7 laws are no longer shallow
- tranche-7 still needs a manifest-scoped source-prep rerun to bring `RA-1378` into staged execution cleanly
