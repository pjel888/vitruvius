# 2026-04-18 Validation — Laws tranche-14 bounded execution

## Manifest
- `config/datasets/laws-tranche-14.yaml`

## Selected tranche-14 scoped surfaces
### DOH
- `DOH Guidelines for Health Facilities 20004.pdf`

### DEPED
- `DepEd DRRR Manual Philippines.pdf`

## Fresh verification
- `python3 -m pytest scripts/tests/test_canonical_rules_additional_laws.py -q`
  - **46 passed**
- `python3 scripts/pipeline_cli.py detect-one '/Users/philiplewis/vitruvius/001_Raw-Source-Layer/001-Laws/DOH/DOH Guidelines for Health Facilities 20004.pdf'`
  - `RESULT: TEXT_PDF`
  - `RECOMMENDED ROUTE: OPENDATALOADER_DIRECT`
- `python3 scripts/pipeline_cli.py detect-one '/Users/philiplewis/vitruvius/001_Raw-Source-Layer/001-Laws/DEPED/DepEd DRRR Manual Philippines.pdf'`
  - `RESULT: TEXT_PDF`
  - `RECOMMENDED ROUTE: OPENDATALOADER_DIRECT`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-duplicate-dry-run --tranche-manifest config/datasets/laws-tranche-14.yaml`
  - `duplicate_cluster_count = 0`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-prep --tranche-manifest config/datasets/laws-tranche-14.yaml`
  - `prepared_count = 2`
  - `ocr_required_count = 0`
  - `failed_count = 0`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-admission --tranche-manifest config/datasets/laws-tranche-14.yaml --source-prep-report 006_System-Manifests/runs/datasets/laws-tranche-14/20260417T160848Z/laws_tranche_source_prep_report.json`
  - `admission_review_ready_law_folders = [DOH, DEPED]`
  - `blocked_law_folders = []`
  - `admitted_source_page_count = 2`
- initial tranche-14 source-to-graph dry-run surfaced:
  - `manual_review_required_count = 1`
  - `spot_review_required_count = 2`
  - `summary_auto_withheld_count = 2`
  - `shallow_representation_count = 1`
- bounded guidance concept-fit follow-on admitted:
  - `disaster-risk-reduction`
  - `continuity-of-instruction`
  - `school-safety`
  - `patient-movement`
  - `waste-disposal`
  - `health-facility-zoning`
- post-follow-on tranche-14 source-to-graph dry-run:
  - `staged_law_folders = [DOH, DEPED]`
  - `blocked_law_folders = []`
  - `manual_review_required_count = 1`
  - `spot_review_required_count = 2`
  - `summary_auto_withheld_count = 2`
  - `shallow_representation_count = 0`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-to-graph --tranche-manifest config/datasets/laws-tranche-14.yaml --review-preset m2-8gb-safe`
  - `staged_law_folders = [DOH, DEPED]`
  - `generated_relationship_count = 0`
  - `manual_review_required_count = 1`
  - `spot_review_required_count = 2`
  - `summary_auto_withheld_count = 2`
  - `shallow_representation_count = 0`
  - graph snapshot: `8 nodes / 12 edges`

## Truthful residuals
- tranche-14 is operationally clean on the scoped guidance surfaces
- `DOH` still carries explicit raw-alias/manual-review risk because the selected source is table-heavy and low-structure
- tranche-14 is now representationally sound, but it remains guidance-heavy and summary-conservative rather than relationship-generative
