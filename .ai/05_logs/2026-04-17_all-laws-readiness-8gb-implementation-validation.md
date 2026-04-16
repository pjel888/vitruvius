# 2026-04-17 All-Laws Readiness & 8GB Rollout Implementation Validation

## Scope
Post-pilot follow-on slice only:
1. whole-dataset readiness planning artifacts
2. 8GB-safe review preset support
3. all-laws dry-run command path

This does **not** open generic Phase 11 all-laws execution.

## Implemented
- `scripts/vitruvius/config.py`
  - review preset resolution helpers
  - M2 8GB-safe preset alias support
- `config/vitruvius.yaml`
  - review preset definitions including `m2-8gb-safe`
- `scripts/vitruvius/laws_readiness.py`
  - readiness-only all-laws dry-run implementation
- `scripts/pipeline_cli.py`
  - `run-laws-all-dry-run` CLI command wiring
  - review preset wiring for bounded pilot and readiness commands
- `scripts/vitruvius/dataset_pipeline.py`
  - bounded source→graph review-setting resolution cleanup
  - `review_runtime` / preset reporting for bounded dry-run output
- tests updated/added for:
  - config preset resolution
  - laws pilot preset application
  - all-laws readiness dry-run CLI behavior

## Fresh verification evidence

### Python syntax
```bash
python3 -m py_compile \
  scripts/pipeline_cli.py \
  scripts/vitruvius/config.py \
  scripts/vitruvius/dataset_pipeline.py \
  scripts/vitruvius/laws_readiness.py \
  scripts/vitruvius/cli_experience.py
```
Result:
- PASS

### Test slice
```bash
python3 -m pytest \
  scripts/tests/test_config.py \
  scripts/tests/test_dataset_pipeline_cli.py \
  scripts/tests/test_dataset_source_to_graph_pipeline.py \
  scripts/tests/test_graph_visualize_cli.py \
  scripts/tests/test_canonicalize_body.py \
  scripts/tests/test_canonicalize_integration.py \
  scripts/tests/test_query_formatter.py -q
```
Result:
- **65 passed**

### Real all-laws readiness dry-run
```bash
PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-all-dry-run --review-preset m2-8gb-safe
```
Result summary:
- `action = run-laws-all-dry-run`
- `phase_11_gate = gated`
- `review_model = qwen2.5:7b`
- `review_model_preset = m2-8gb-safe`
- `raw_law_folder_count = 47`
- `raw_pdf_count = 183`
- `bounded_manifest_law_unit_count = 4`
- `pilot_covered_law_count = 4`
- `inventory_only_law_count = 43`
- report path written under:
  - `006_System-Manifests/runs/datasets/laws-all-readiness/.../all_laws_dry_run_report.json`

### Real bounded pilot dry-run with 8GB-safe preset
```bash
PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-pilot --dry-run --review-preset m2-8gb-safe
```
Result summary:
- `review_model = qwen2.5:7b`
- `review_settings.timeout_seconds = 900`
- `review_settings.parallelism = 1`
- `review_settings.num_ctx_cap = 4096`
- bounded pilot still plans successfully (`planned_stage_count = 5`)

## Conclusion
This slice is successful:
- planning artifacts exist
- an 8GB-safe preset path exists
- an all-laws dry-run command path exists
- bounded pilot dry-run can now use the 8GB-safe preset
- generic all-laws execute remains intentionally gated
