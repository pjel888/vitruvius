# 2026-04-18 Validation — HLURB and DHSUD agency split correction

## Verified external context
- DHSUD official profile / RA 11201 materials confirm that DHSUD was created on **February 14, 2019** by **Republic Act No. 11201** and consolidated former HLURB and HUDCC functions except adjudication.
- DHSUD official manuals/guidebooks page currently hosts both older HLURB materials and newer DHSUD publications.

## Local source evidence
The tranche-12 staged guidance files inside the combined raw folder are explicitly DHSUD publications:
- `Open Space Development Guidelines.pdf`
  - title page: `Department of Human Settlements and Urban Development`
  - copyright/publication year: `2025`
- `Resilient Urban Design and Development Guidelines.pdf`
  - title page: `Department of Human Settlements and Urban Development`
  - copyright/publication year: `2025`

## Implementation verification
- focused regression:
  - `python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py -k 'raw_folder_name_override or manifest_scoped_variants or scoped_variants_for_duplicates' -q`
  - **3 passed**
- canonical-rule suite:
  - `python3 -m pytest scripts/tests/test_canonical_rules_additional_laws.py -q`
  - **62 passed**
- tranche-12 source-prep dry-run after logical/raw-folder split:
  - `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-prep-dry-run --tranche-manifest config/datasets/laws-tranche-12.yaml`
  - `candidate_law_folder_count = 2`
  - `raw_file_count = 5`
  - `supported_direct_input_count = 5`
  - `refined_markdown_ready_count = 5`
- tranche-12 duplicate dry-run after logical/raw-folder split:
  - `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-duplicate-dry-run --tranche-manifest config/datasets/laws-tranche-12.yaml`
  - `duplicate_cluster_count = 0`
  - `duplicate_law_folders = []`

## Truthful result
- the raw storage folder remains `HLURB-DHSUD`
- the currently staged tranche-12 guidance surfaces are now represented as `DHSUD`
- older HLURB materials remain explicit but excluded until a separate HLURB-focused lane is opened
