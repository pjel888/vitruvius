# 2026-04-18 Validation — Tranche-15 Pasay LGU shard

## Shard manifest
- `config/datasets/laws-tranche-15-pasay.yaml`

## Selected shard
- `579259927-ZONING-ORDINANCE-PASAY.pdf`

## Fresh verification
- canonical-rule tests:
  - `python3 -m pytest scripts/tests/test_canonical_rules_additional_laws.py -q`
  - **55 passed**
- shard duplicate screen:
  - `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-duplicate-dry-run --tranche-manifest config/datasets/laws-tranche-15-pasay.yaml`
  - `duplicate_cluster_count = 0`
  - `duplicate_law_folders = []`
- shard source-prep dry-run:
  - `raw_file_count = 1`
  - `supported_direct_input_count = 1`
- shard source-prep execute with OCR:
  - `prepared_count = 1`
  - `ocr_required_count = 0`
  - `failed_count = 0`
  - OCR warnings remained visible during prep (`lots of diacritics - possibly poor OCR`)
- shard source-admission dry-run:
  - `admission_review_ready_law_folders = [LGU]`
  - `blocked_law_folders = []`
  - `candidate_source_page_count = 1`
- shard source-admission execute:
  - `admitted_source_page_count = 1`
  - `canonicalize_failure_count = 0`
- initial shard source-to-graph execute failed graph integrity because a generated promoted relationship referenced unadmitted `concept-floor-area`
- bounded Pasay concept-fit / concept-admission follow-on added:
  - existing `zoning-ordinance`
  - existing `comprehensive-land-use-plan`
  - existing `floor-area-ratio`
  - existing `central-business-district`
  - existing `floor-area`
- final shard source-to-graph dry-run:
  - `staged_law_folders = [LGU]`
  - `duplicate_law_folders = []`
  - `manual_review_required_count = 0`
  - `spot_review_required_count = 1`
  - `summary_auto_withheld_count = 1`
  - `shallow_representation_count = 0`
- final shard source-to-graph execute:
  - `staged_law_folders = [LGU]`
  - `duplicate_law_folders = []`
  - `generated_relationship_count = 1`
  - `filtered_relationship_count = 0`
  - `manual_review_required_count = 0`
  - `spot_review_required_count = 1`
  - `summary_auto_withheld_count = 1`
  - `shallow_representation_count = 0`
  - graph snapshot: `6 nodes / 5 edges`

## Truthful residuals
- the eighth LGU shard now executes cleanly and is not duplicate-blocked
- Pasay remains explicitly review-sensitive because the shard required OCR-first prep and still carries a spot-review/suppressed-summary signal
- the wider `LGU` lane remains open because multiple city/family shards still remain beyond San Mateo, Dagupan, Malolos, Meycauayan, Davao, Tarlac, QC-CBD, and Pasay
