# 2026-04-18 Validation — Tranche-15 San Mateo LGU shard

## Shard manifest
- `config/datasets/laws-tranche-15-san-mateo.yaml`

## Selected shard
- `794216046-San-Mateo-Zoning-Ordinance.pdf`
- `844057380-Copy-of-San-Mateo-Rizal-clup.pdf`

## Fresh verification
- duplicate-scope regression tests:
  - `python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py -k 'manifest_scoped_variants or scoped_variants_for_duplicates' -q`
  - **2 passed**
- canonical-rule tests:
  - `python3 -m pytest scripts/tests/test_canonical_rules_additional_laws.py -q`
  - **48 passed**
- shard duplicate screen after duplicate-scope fix:
  - `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-duplicate-dry-run --tranche-manifest config/datasets/laws-tranche-15-san-mateo.yaml`
  - `duplicate_cluster_count = 0`
  - `duplicate_law_folders = []`
- shard source prep:
  - `prepared_count = 2`
  - `ocr_required_count = 0`
  - `failed_count = 0`
- shard source admission dry-run:
  - `admission_review_ready_law_folders = [LGU]`
  - `blocked_law_folders = []`
  - `candidate_source_page_count = 2`
- shard source admission execute:
  - `admitted_source_page_count = 2`
  - `canonicalize_failure_count = 0`
- initial shard source-to-graph execute failed graph integrity because generated promoted relationships referenced unadmitted `concept-floor-area` and `concept-waste-disposal`
- bounded San Mateo concept-fit / concept-admission follow-on added:
  - `zoning-ordinance`
  - `floor-area-ratio`
  - existing `comprehensive-land-use-plan`
  - existing `floor-area`
  - existing `waste-disposal`
- final shard source-to-graph dry-run:
  - `staged_law_folders = [LGU]`
  - `duplicate_law_folders = []`
  - `manual_review_required_count = 2`
  - `spot_review_required_count = 2`
  - `summary_auto_withheld_count = 2`
  - `shallow_representation_count = 0`
- final shard source-to-graph execute:
  - `staged_law_folders = [LGU]`
  - `duplicate_law_folders = []`
  - `generated_relationship_count = 2`
  - `filtered_relationship_count = 0`
  - `manual_review_required_count = 2`
  - `spot_review_required_count = 2`
  - `summary_auto_withheld_count = 2`
  - `shallow_representation_count = 0`
  - graph snapshot: `7 nodes / 7 edges`

## Truthful residuals
- the first LGU shard now executes cleanly and is no longer duplicate-blocked
- the shard still keeps explicit manual-review / summary-withheld signals because both selected LGU sources are image-heavy / TOC-heavy planning documents
- the wider `LGU` lane remains open because this is only the first shard, not the whole folder
