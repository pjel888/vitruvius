# 2026-04-18 Validation — RA-9279 remediation-first lane

## Remediation manifest
- `config/datasets/laws-tranche-ra-9279-remediation.yaml`

## Selected source
- `IRR RA 7279 Sec 18.pdf`

## Fresh verification
- canonical-rule tests:
  - `python3 -m pytest scripts/tests/test_canonical_rules_additional_laws.py -q`
  - **56 passed**
- remediation duplicate screen:
  - `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-duplicate-dry-run --tranche-manifest config/datasets/laws-tranche-ra-9279-remediation.yaml`
  - `duplicate_cluster_count = 0`
  - `duplicate_law_folders = []`
- remediation source-prep dry-run:
  - `raw_file_count = 1`
  - `supported_direct_input_count = 1`
- remediation source-prep execute:
  - `prepared_count = 1`
  - `ocr_required_count = 0`
  - `failed_count = 0`
- remediation source-admission dry-run:
  - `admission_review_ready_law_folders = [RA-9279]`
  - `blocked_law_folders = []`
  - `candidate_source_page_count = 1`
- remediation source-admission execute:
  - `admitted_source_page_count = 1`
  - `canonicalize_failure_count = 0`
- bounded concept/remediation follow-on admitted:
  - `balanced-housing-development`
  - `project-area`
  - existing `socialized-housing-projects`
- final source-to-graph dry-run:
  - `staged_law_folders = [RA-9279]`
  - `duplicate_law_folders = []`
  - `manual_review_required_count = 0`
  - `spot_review_required_count = 0`
  - `summary_auto_withheld_count = 0`
  - `shallow_representation_count = 0`
- final source-to-graph execute:
  - `staged_law_folders = [RA-9279]`
  - `duplicate_law_folders = []`
  - `generated_relationship_count = 0`
  - `filtered_relationship_count = 0`
  - `manual_review_required_count = 0`
  - `spot_review_required_count = 0`
  - `summary_auto_withheld_count = 0`
  - `shallow_representation_count = 0`
  - graph snapshot: `4 nodes / 4 edges`

## Truthful remediation result
- the `RA-9279` folder is now handled truthfully as a remediation-first lane
- the actual admitted source identity is:
  - `Implementing Rules and Regulations to Govern Section 18 of Republic Act No. 7279`
- this resolves the filename/folder mismatch without pretending the folder really contains RA 9279 statute text
