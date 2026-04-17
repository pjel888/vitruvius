# 2026-04-18 Validation — PRC professional-practice resolution lane

## Tranche manifest
- `config/datasets/laws-tranche-prc.yaml`

## Selected PRC surfaces
- `PRBoAres03,s08_temporary Permits for Foreign Architects.pdf`
- `PRBoAreso1,s08_Prohibition of NonRLA's.pdf`
- `PRBoaRes,s08 Effectivity Dates of PRBOA Resolutions.pdf`
- `RES_Architecture and AR Interiors are Exclusive.pdf`
- `RES_Clarification of PD-9266 Rule II Registration.pdf`
- `RES_Illegal Practice of AR.pdf`

## Fresh verification
- canonical-rule tests:
  - `python3 -m pytest scripts/tests/test_canonical_rules_additional_laws.py -q`
  - **62 passed**
- tranche duplicate screen:
  - `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-duplicate-dry-run --tranche-manifest config/datasets/laws-tranche-prc.yaml`
  - `duplicate_cluster_count = 0`
  - `duplicate_law_folders = []`
- tranche source-prep dry-run:
  - `raw_file_count = 6`
  - `supported_direct_input_count = 6`
- tranche source-prep execute:
  - `prepared_count = 6`
  - `ocr_required_count = 0`
  - `failed_count = 0`
- tranche source-admission dry-run:
  - `admission_review_ready_law_folders = [PRC]`
  - `blocked_law_folders = []`
  - `candidate_source_page_count = 6`
- tranche source-admission execute:
  - `admitted_source_page_count = 6`
  - `canonicalize_failure_count = 0`
- initial source-to-graph dry-run surfaced:
  - `manual_review_required_count = 1`
  - `spot_review_required_count = 4`
  - `summary_auto_withheld_count = 4`
  - `shallow_representation_count = 1`
- bounded PRC concept-fit follow-on admitted:
  - `temporary-special-permit`
  - `architectural-interiors`
  - `architectural-firm-registration`
  - `illegal-practice-of-architecture`
  - existing `building-permit`
  - existing `standards-of-professional-practice`
- final source-to-graph dry-run:
  - `staged_law_folders = [PRC]`
  - `duplicate_law_folders = []`
  - `manual_review_required_count = 1`
  - `spot_review_required_count = 4`
  - `summary_auto_withheld_count = 4`
  - `shallow_representation_count = 0`
- final source-to-graph execute:
  - `staged_law_folders = [PRC]`
  - `duplicate_law_folders = []`
  - `generated_relationship_count = 2`
  - `filtered_relationship_count = 0`
  - `manual_review_required_count = 1`
  - `spot_review_required_count = 4`
  - `summary_auto_withheld_count = 4`
  - `shallow_representation_count = 0`
  - graph snapshot: `12 nodes / 10 edges`

## Truthful residuals
- the PRC lane now executes cleanly and is no longer concept-shallow
- `PRBoaRes,s08 Effectivity Dates of PRBOA Resolutions` still carries explicit manual-review risk because the source is structurally weak and summary-trust is low
- four PRC sources still keep spot-review / summary-withheld signals, which is truthful for this board-resolution bundle
