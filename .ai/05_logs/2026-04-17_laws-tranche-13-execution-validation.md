# 2026-04-17 Validation — Laws tranche-13 bounded execution

## Manifest
- `config/datasets/laws-tranche-13.yaml`

## Selected tranche-13 scoped surfaces
### CHED
- `CHED CMO 61 Series 2017 - BS Architecture Curriculum Standards.pdf`

### CIAP
- `CIAP-Document-102-Private-Constn-Contract.pdf`

### UAP
- `UAP Document Code of Ethics.pdf`
- `UAP Document Standards of Professional Practice.pdf`
- `UAP Document 301.pdf`

## Fresh verification
- `python3 -m pytest scripts/tests/test_canonical_rules_additional_laws.py -q`
  - **44 passed**
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-prep --tranche-manifest config/datasets/laws-tranche-13.yaml --allow-ocr`
  - `prepared_count = 5`
  - `ocr_required_count = 0`
  - `failed_count = 0`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-admission --tranche-manifest config/datasets/laws-tranche-13.yaml --source-prep-report 006_System-Manifests/runs/datasets/laws-tranche-13/20260417T160029Z/laws_tranche_source_prep_report.json`
  - `admission_review_ready_law_folders = [CHED, CIAP, UAP]`
  - `blocked_law_folders = []`
  - `admitted_source_page_count = 5`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-to-graph-dry-run --tranche-manifest config/datasets/laws-tranche-13.yaml --review-preset m2-8gb-safe`
  - `staged_law_folders = [CHED, CIAP, UAP]`
  - `blocked_law_folders = []`
  - `spot_review_required_count = 2`
  - `summary_auto_withheld_count = 2`
  - `shallow_representation_count = 0`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-to-graph --tranche-manifest config/datasets/laws-tranche-13.yaml --review-preset m2-8gb-safe`
  - `staged_law_folders = [CHED, CIAP, UAP]`
  - `blocked_law_folders = []`
  - `generated_relationship_count = 0`
  - `spot_review_required_count = 2`
  - `summary_auto_withheld_count = 2`
  - `shallow_representation_count = 0`
  - graph snapshot: `8 nodes / 6 edges`

## Truthful residuals
- tranche-13 is operationally clean on the scoped professional/standards surfaces
- `UAP` still carries explicit raw-alias visibility because reviewer/study-aid variants remain excluded rather than silently collapsed
- tranche-13 remains standards-heavy rather than law-dense, so graph growth is modest even after the UAP concept-fit slice cleared the shallow-representation guardrail
