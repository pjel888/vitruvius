# 2026-04-18 Validation — Tranche-15 Davao LGU shard

## Shard manifest
- `config/datasets/laws-tranche-15-davao.yaml`

## Selected shard
- `253090760-Zoning-Davao-City.pdf`

## Fresh verification
- canonical-rule tests:
  - `python3 -m pytest scripts/tests/test_canonical_rules_additional_laws.py -q`
  - **52 passed**
- shard duplicate screen:
  - `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-duplicate-dry-run --tranche-manifest config/datasets/laws-tranche-15-davao.yaml`
  - `duplicate_cluster_count = 0`
  - `duplicate_law_folders = []`
- shard source-prep dry-run:
  - `raw_file_count = 1`
  - `supported_direct_input_count = 1`
- shard source-prep execute:
  - `prepared_count = 1`
  - `ocr_required_count = 0`
  - `failed_count = 0`
- shard source-admission dry-run:
  - `admission_review_ready_law_folders = [LGU]`
  - `blocked_law_folders = []`
  - `candidate_source_page_count = 1`
- shard source-admission execute:
  - `admitted_source_page_count = 1`
  - `canonicalize_failure_count = 0`
- bounded Davao concept-fit / concept-admission follow-on added:
  - existing `comprehensive-land-use-plan`
  - existing `disaster-risk-reduction`
- final shard source-to-graph dry-run:
  - `staged_law_folders = [LGU]`
  - `duplicate_law_folders = []`
  - `manual_review_required_count = 1`
  - `spot_review_required_count = 1`
  - `summary_auto_withheld_count = 1`
  - `shallow_representation_count = 0`
- final shard source-to-graph execute:
  - `staged_law_folders = [LGU]`
  - `duplicate_law_folders = []`
  - `generated_relationship_count = 0`
  - `filtered_relationship_count = 0`
  - `manual_review_required_count = 1`
  - `spot_review_required_count = 1`
  - `summary_auto_withheld_count = 1`
  - `shallow_representation_count = 0`
  - graph snapshot: `3 nodes / 2 edges`

## Truthful residuals
- the fifth LGU shard now executes cleanly and is not duplicate-blocked
- this Davao shard remains slide-deck / image-heavy, so review signals remain explicit and graph growth is modest
- the wider `LGU` lane remains open because more city/family shards still remain beyond San Mateo, Dagupan, Malolos, Meycauayan, and Davao
