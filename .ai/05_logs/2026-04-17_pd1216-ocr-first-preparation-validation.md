# 2026-04-17 PD-1216 OCR-First Preparation Validation

## Scope
Execute the OCR-first preparation slice for `PD-1216`, then rerun tranche admission and tranche source-to-graph dry-run.

## Changes
- `scripts/vitruvius/laws_readiness.py`
  - added optional OCR-first support to `run-laws-tranche-source-prep`
  - when `--allow-ocr` is set, scanned tranche PDFs can now:
    - write OCR PDF output
    - convert through OpenDataLoader
    - refine into tranche-ready markdown
  - added OCR-aware expected-path reporting
- `scripts/pipeline_cli.py`
  - added `--allow-ocr` to `run-laws-tranche-source-prep`
- `scripts/vitruvius/cli_experience.py`
  - documented OCR-first preparation in the tranche source-prep operator surface
- `scripts/vitruvius/rules/canonical_rules.yaml`
  - added canonical rule for `PD-1216`
- `scripts/tests/test_dataset_pipeline_cli.py`
  - added OCR-first unit coverage for tranche source preparation
- `scripts/tests/test_canonical_rules_additional_laws.py`
  - added PD-1216 rule coverage
- runtime outputs now exist for `PD-1216`:
  - OCR PDF
  - raw markdown
  - refined markdown
  - sidecar JSON
- tranche source admission rerun now admits the PD-1216 source page:
  - `003_Canonical-Knowledge-Layer/shared/sources/open-space-requirements-in-residential-subdivisions.md`

## Verification
- `python3 -m py_compile scripts/vitruvius/laws_readiness.py scripts/pipeline_cli.py scripts/vitruvius/cli_experience.py scripts/tests/test_dataset_pipeline_cli.py scripts/tests/test_canonical_rules_additional_laws.py`
- `python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py scripts/tests/test_canonical_rules_additional_laws.py -k 'prepare_raw_file_allow_ocr or tranche_source_to_graph_dry_run or pd_1216 or pd_957 or pd_1185' -q`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-prep --tranche-manifest config/datasets/laws-tranche-1.yaml --allow-ocr`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-admission-dry-run --tranche-manifest config/datasets/laws-tranche-1.yaml --source-prep-report 006_System-Manifests/runs/datasets/laws-tranche-1/20260417T065723Z/laws_tranche_source_prep_report.json`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-admission --tranche-manifest config/datasets/laws-tranche-1.yaml --source-prep-report 006_System-Manifests/runs/datasets/laws-tranche-1/20260417T065723Z/laws_tranche_source_prep_report.json`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-to-graph-dry-run --tranche-manifest config/datasets/laws-tranche-1.yaml --review-preset m2-8gb-safe`

## Fresh evidence
- OCR-first tranche prep:
  - `prepared_count = 6`
  - `ocr_required_count = 0`
  - `failed_count = 0`
- source admission dry-run after OCR:
  - ready:
    - `PD-957`
    - `PD-1216`
    - `PD-1185`
  - blocked:
    - none
- source admission execute after OCR:
  - `admitted_source_page_count = 3`
  - `canonicalize_failure_count = 0`
- tranche source-to-graph dry-run after OCR + PD-1216 admission:
  - `staged_law_folders = [PD-957, PD-1216, PD-1185]`
  - `blocked_law_folders = []`
  - `planned_stage_count = 3`
  - `shallow_representation_count = 0`
  - `source_to_graph_execute_ready = false`

## Conclusion
`PD-1216` is no longer blocked for lack of OCR outputs.
The tranche can now stage all three laws through source-to-graph dry-run truthfully.
Execute remains gated, but the tranche is materially closer to a buildable/testable knowledge-graph lane than before.
