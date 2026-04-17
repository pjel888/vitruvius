# 2026-04-17 Laws Tranche Source-Preparation Implementation Validation

## Scope
Implementation follow-on after tranche source-preparation dry-run.

This slice adds a tranche-only source-preparation execute lane so tranche-1 can begin produced-data generation without widening into source→graph execution.

## Implemented
- `scripts/vitruvius/laws_readiness.py`
  - `run_laws_tranche_source_prep(...)`
  - tranche-only conversion + refine orchestration
  - per-file prepared / OCR-required / failed status reporting
- `scripts/pipeline_cli.py`
  - `run-laws-tranche-source-prep`
- `scripts/vitruvius/cli_experience.py`
  - operator docs for the execute step
- `scripts/tests/test_dataset_pipeline_cli.py`
  - command coverage for OCR-required handling
- `README.md`
  - tranche source-preparation execute usage

## Fresh verification evidence

### Tests
```bash
python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py -q
```
Result:
- **12 passed**

### Syntax
```bash
python3 -m py_compile scripts/vitruvius/laws_readiness.py
```
Result:
- **PASS**

### Real tranche source-preparation execute
```bash
PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-prep \
  --tranche-manifest config/datasets/laws-tranche-1.yaml
```
Result summary:
- `action = run-laws-tranche-source-prep`
- `phase_11_gate = gated`
- `tranche_id = laws-tranche-1`
- `candidate_law_folder_count = 3`
- `raw_file_count = 6`
- `supported_direct_input_count = 6`
- `prepared_count = 5`
- `ocr_required_count = 1`
- `failed_count = 0`
- report written under:
  - `006_System-Manifests/runs/datasets/laws-tranche-1/.../laws_tranche_source_prep_report.json`

## Meaning
Tranche-1 is now beyond pure readiness reporting.
It has a tranche-local source-preparation execute step.

But it is still not ready for tranche source→graph execution until the new
produced-data outputs are reviewed and tranche dry-run is rerun against the
updated state.
