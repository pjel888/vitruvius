# 2026-04-16 Dataset Source-to-Graph Hardening Validation

## Scope
Follow-on hardening for the bounded source→graph lane.

## Changes
- `scripts/vitruvius/dataset_pipeline.py`
  - normalize prefixed refined markdown paths before stage execution
  - record source-quality metrics in stage reports
  - classify source-quality severity (`low` / `medium` / `high`)
  - keep generated relationship admission bounded to graph-safe `source -> concept -> governs` records
- `scripts/tests/test_dataset_source_to_graph_pipeline.py`
  - added regression coverage for refined-path normalization
  - added coverage for source-quality reporting in dry-run and execute paths
  - added coverage for graph-admissibility filtering

## Verification
- `python3 -m py_compile scripts/vitruvius/dataset_pipeline.py scripts/vitruvius/canonicalize.py scripts/vitruvius/graph/contract.py scripts/vitruvius/graph/builder.py scripts/vitruvius/graph/visualize.py scripts/pipeline_cli.py scripts/tests/test_dataset_source_to_graph_pipeline.py scripts/tests/test_dataset_pipeline_cli.py scripts/tests/test_graph_visualize_cli.py scripts/tests/test_graph_builder.py scripts/tests/test_canonicalize_body.py`
  - PASS
- `PYTHONPATH=scripts pytest -q scripts/tests/test_dataset_source_to_graph_pipeline.py scripts/tests/test_dataset_pipeline_cli.py scripts/tests/test_graph_visualize_cli.py scripts/tests/test_graph_builder.py scripts/tests/test_canonicalize_body.py`
  - `59 passed in 1.20s`

## Fresh real evidence
- dry-run command:
  - `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-dataset-source-to-graph --dataset-manifest config/datasets/laws-core-bundle-m1.yaml --dry-run`
- result:
  - PASS
- run id:
  - `20260416T171702Z`
- report:
  - `006_System-Manifests/runs/datasets/laws-core-bundle-m1/source_to_graph/20260416T171702Z/source_to_graph_run_report.json`
- report confirms:
  - `dry_run = true`
  - `planned_stage_count = 5`
  - stage records include `normalized_refined_markdown_path`
  - stage records include `source_quality` and `source_quality_path`

## Follow-on hardening
- source-quality reporting now includes `benchmark_source_hints` for difficult sources when known official/public reference URLs exist
- latest dry-run used for validation: `20260416T175803Z`
