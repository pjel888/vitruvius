---
task: aggregate-hardening-referenced-concepts
created: 2026-04-18
status: complete
---

# Validation — Aggregate hardening via referenced-concept edges

## Goal
Use the new aggregate warning summary surface to reduce duplicate edges, orphan nodes, and partial-family coverage in the combined ready-family graph without inventing stronger relationship claims.

## Implementation
- Added conservative source→concept `covers` edges in `build_snapshot()` for sources that currently have zero incident edges.
- Derived those edges only from the canonical source page body section:
  - `## Referenced Concepts`
- Marked inferred edges as `unverified`.
- Limited the inference to currently orphan sources so already-connected sources do not gain redundant inferred edges.

## Verification commands
- `python3 -m pytest scripts/tests/test_graph_builder.py -q`
- `python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py -k 'summarize_dataset_build_report_reports_warning_summary or pipeline_cli_summarize_dataset_build_report_reports_summary' -q`
- `python3 -m pytest scripts/tests/test_registry_load.py -q`
- `python3 scripts/pipeline_cli.py build-graph --dataset-manifest config/datasets/ready-family-aggregate.yaml`
- `python3 scripts/pipeline_cli.py summarize-dataset-build-report --build-report 006_System-Manifests/runs/datasets/ready-family-aggregate/20260418T013024Z_build_graph_dataset_report.json --top-n 20`

## Results
### Tests
- `test_graph_builder.py`: 27 passed
- dataset-pipeline summary tests: 2 passed
- registry tests: 3 passed

### Combined ready-family graph before this pass
- node_count: 136
- edge_count: 265
- warning_count: 62
- warning_codes:
  - `duplicate_edge = 44`
  - `orphan_node = 18`
- covered_folder_count: 31
- partial_folder_count: 15

### Combined ready-family graph after this pass
- node_count: 136
- edge_count: 256
- warning_count: 5
- warning_codes:
  - `orphan_node = 5`
- covered_folder_count: 42
- partial_folder_count: 4

## Remaining orphan nodes
- `handout-resolution-on-effectivity-dates-of-prboa-resolutions`
- `law-alternative-dispute-resolution-act-of-2004`
- `law-civil-code-of-the-philippines`
- `law-plumbing-law`
- `law-toxic-substances-and-hazardous-and-nuclear-wastes-control-act-of-1990`

## Remaining partial folders
- `RA-6969`
- `RA-386`
- `RA-1378`
- `RA-9285`

## Interpretation
The warning-summary surface successfully identified that the largest recoverable hardening opportunity was graph connectivity, not new relationship mining. Reusing already-admitted `Referenced Concepts` sections removed all duplicate-edge warnings, cut orphan-node warnings from 18 to 5, and reduced partial-folder coverage from 15 to 4 while preserving conservative truth boundaries.
