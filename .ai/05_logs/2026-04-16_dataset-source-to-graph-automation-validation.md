# 2026-04-16 Dataset Source-to-Graph Automation Validation

## Scope
Add a bounded source→graph orchestration command for the laws dataset without bypassing truth-governance.

## What was added
- `run-dataset-source-to-graph` CLI surface
- dataset pipeline support for:
  - bounded stage planning via `--dry-run`
  - dataset-local canonicalize / extract / review / promote orchestration
  - derived manifest emission before final graph build

## Verification
- `python3 scripts/pipeline_cli.py run-dataset-source-to-graph --help`
  - PASS
- `PYTHONPATH=scripts pytest -q scripts/tests/test_dataset_source_to_graph_pipeline.py scripts/tests/test_dataset_pipeline_cli.py scripts/tests/test_graph_visualize_cli.py scripts/tests/test_pipeline_cli_byte_identity.py`
  - PASS

## Real dry-run evidence
- command:
  - `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-dataset-source-to-graph --dataset-manifest config/datasets/laws-core-bundle-m1.yaml --dry-run`
- result:
  - PASS
- report:
  - `006_System-Manifests/runs/datasets/laws-core-bundle-m1/source_to_graph/20260416T144518Z/source_to_graph_run_report.json`
- summary:
  - `dry_run = true`
  - `planned_stage_count = 5`
  - dataset-local stage outputs are planned per law unit

## Truth boundary
This command is intended to automate the bounded produced-data lane.
It is not a raw-PDF→graph shortcut and is not a license to skip review/promotion governance.
