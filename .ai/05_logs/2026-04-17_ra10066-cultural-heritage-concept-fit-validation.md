# 2026-04-17 Validation — RA-10066 cultural-heritage concept-fit

## Scope
Admit the smallest tranche-4 concept-fit slice needed to remove RA-10066's shallow-representation finding.

## Admitted concepts
- `concept-adaptive-reuse`
- `concept-built-heritage`
- `concept-heritage-zone`

## Admitted dataset-scoped relationships
- `law-national-cultural-heritage-act-of-2009 governs concept-adaptive-reuse`
- `law-national-cultural-heritage-act-of-2009 governs concept-built-heritage`
- `law-national-cultural-heritage-act-of-2009 governs concept-heritage-zone`

## Fresh verification
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-to-graph-dry-run --tranche-manifest config/datasets/laws-tranche-4.yaml --review-preset m2-8gb-safe`
  - `shallow_representation_count = 0`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-to-graph --tranche-manifest config/datasets/laws-tranche-4.yaml --review-preset m2-8gb-safe`
  - `generated_relationship_count = 1`
  - `shallow_representation_count = 0`
  - graph snapshot: `6 nodes / 7 edges`

## Truthful residuals
- tranche-4 still carries `spot_review_required_count = 1` and `summary_auto_withheld_count = 1` because RA-10066 remains accepted-with-spot-review for OCR-sensitive heading/title lines
- representationally, tranche-4 is no longer shallow
