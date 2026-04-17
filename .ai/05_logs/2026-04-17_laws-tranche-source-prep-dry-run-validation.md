# 2026-04-17 Laws Tranche Source-Preparation Dry-Run Validation

## Scope
Implementation follow-on after tranche dry-run.

This slice adds a tranche-local source-preparation dry-run so widening work can verify raw-source readiness before attempting tranche source-to-graph execution.

## Implemented
- `scripts/vitruvius/laws_readiness.py`
  - `run_laws_tranche_source_prep_dry_run(...)`
  - per-file raw-input planning report
  - expected raw-markdown / sidecar / refined output path reporting
  - lightweight PDF detection usage during source-prep planning
- `scripts/pipeline_cli.py`
  - `run-laws-tranche-source-prep-dry-run`
- `scripts/vitruvius/cli_experience.py`
  - operator docs for tranche source-prep dry-run
- `scripts/tests/test_dataset_pipeline_cli.py`
  - CLI test coverage for tranche source-prep dry-run
- `README.md`
  - tranche source-prep dry-run operator docs

## Fresh verification evidence

### Tests
```bash
python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py -q
```
Result:
- **11 passed**

### Syntax
```bash
python3 -m py_compile scripts/pipeline_cli.py scripts/vitruvius/laws_readiness.py scripts/vitruvius/cli_experience.py
```
Result:
- **PASS**

### Real tranche source-prep dry-run
```bash
PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-prep-dry-run \
  --tranche-manifest config/datasets/laws-tranche-1.yaml
```
Result summary:
- `action = run-laws-tranche-source-prep-dry-run`
- `phase_11_gate = gated`
- `tranche_id = laws-tranche-1`
- `candidate_law_folder_count = 3`
- `raw_file_count = 6`
- `supported_direct_input_count = 6`
- `refined_markdown_ready_count = 0`
- report written under:
  - `006_System-Manifests/runs/datasets/laws-tranche-1/.../laws_tranche_source_prep_dry_run_report.json`

## Conclusion
The next execution boundary is now clearer than before:
- tranche-1 dry-run exists
- tranche-1 source-prep dry-run exists
- tranche-1 still needs produced-data generation before source→graph dry-run/execute
