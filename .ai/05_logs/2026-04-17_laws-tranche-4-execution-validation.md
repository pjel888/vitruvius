# 2026-04-17 Validation — Laws tranche-4 bounded execution

## Manifest
- `config/datasets/laws-tranche-4.yaml`

## Selected tranche-4 laws
- `PD-1517`
- `RA-6969`
- `RA-10066`

## Selection rationale
- zero exact duplicate clusters in the candidate set
- all three files classify as direct text-PDF / `OPENDATALOADER_DIRECT`
- avoids immediate OCR-first debt while widening by another bounded manifest

## Fresh verification
- `python3 -m py_compile scripts/tests/test_canonical_rules_additional_laws.py`
- `python3 -m pytest scripts/tests/test_canonical_rules_additional_laws.py -q`
  - **16 passed**
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-duplicate-dry-run --tranche-manifest config/datasets/laws-tranche-4.yaml`
  - `duplicate_cluster_count = 0`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-prep --tranche-manifest config/datasets/laws-tranche-4.yaml`
  - `prepared_count = 3`
  - `ocr_required_count = 0`
  - `failed_count = 0`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-admission --tranche-manifest config/datasets/laws-tranche-4.yaml`
  - `admitted_source_page_count = 3`
  - `blocked_law_folders = []`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-to-graph --tranche-manifest config/datasets/laws-tranche-4.yaml --review-preset m2-8gb-safe`
  - staged: `PD-1517`, `RA-6969`, `RA-10066`
  - `generated_relationship_count = 0`
  - `spot_review_required_count = 1`
  - `summary_auto_withheld_count = 1`
  - `shallow_representation_count = 1`
  - `source_to_graph_execute_completed = true`

## Truthful residuals
- tranche-4 is execute-capable but graph-thin
- `RA-10066` is the current richest next follow-on target because it is both:
  - `accepted_with_spot_review`
  - `shallow_representation`

## Updated tranche-4 richness follow-on
- bounded `RA-10066` cultural-heritage concept-fit slice admitted three new shared concepts and three dataset-scoped relationships
- refreshed execute evidence:
  - `staged_law_folders = [PD-1517, RA-6969, RA-10066]`
  - `generated_relationship_count = 1`
  - `spot_review_required_count = 1`
  - `shallow_representation_count = 0`
  - graph snapshot: `6 nodes / 7 edges`
- see `/.ai/05_logs/2026-04-17_ra10066-cultural-heritage-concept-fit-validation.md`
