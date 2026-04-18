---
task: ready-family-operator-alignment
created: 2026-04-18
status: complete
---

# Validation — ready-family operator alignment

## Goal
Align the full one-command ready-family source-to-graph operator path with the cleaner hardened build path by preventing run-local generated relationship files from duplicating already-admitted relationship evidence.

## Implemented change
- `scripts/vitruvius/dataset_pipeline.py`
  - generated relationship dedupe now considers relationship evidence id (`rel-*`) in addition to file path
  - derived manifest append now skips run-local relationship files when an existing manifest relationship already carries the same evidence id
- `scripts/tests/test_dataset_source_to_graph_pipeline.py`
  - added regression test for duplicate evidence-id collisions across different relationship paths

## Verification completed so far
- `python3 -m pytest scripts/tests/test_dataset_source_to_graph_pipeline.py -q`
  - 11 passed
- `python3 -m pytest scripts/tests/test_graph_builder.py -q`
  - 27 passed
- `python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py -k 'summarize_dataset_build_report_reports_warning_summary or pipeline_cli_summarize_dataset_build_report_reports_summary' -q`
  - 2 passed

## Fresh runtime evidence
- full operator rerun launched after the fix:
  - `./run-ready-families-mvp-graph --review-preset m2-8gb-safe --skip-export-owl`
- live process evidence at capture time:
  - PID `51659`
  - active run folder: `006_System-Manifests/runs/datasets/ready-family-aggregate/source_to_graph/20260418T020145Z`
  - elapsed: ~3m45s
  - run-folder file count: 69
  - run-folder size: ~592K

## Final end-to-end rerun result
- rerun output artifacts landed:
  - `006_System-Manifests/runs/datasets/ready-family-aggregate/20260418T021054Z_dataset_pipeline_run_report.json`
  - `006_System-Manifests/runs/datasets/ready-family-aggregate/20260418T021054Z_build_graph_dataset_report.json`
  - `005_Operational-Intelligence-Layer/graph/datasets/ready-family-aggregate/20260418T021054Z_graph_snapshot.json`
- final build-report summary:
  - `node_count = 136`
  - `edge_count = 270`
  - `warning_count = 4`
  - `duplicate_edge = 0`
  - `orphan_node = 4`
  - `covered_folder_count = 42`
  - `partial_folder_count = 4`

## Comparison
### Bad pre-fix operator rerun (`20260418T014600Z`)
- `edge_count = 313`
- `warning_count = 49`
- `duplicate_edge = 44`
- `orphan_node = 5`

### Hardened build-path baseline (`20260418T013024Z`)
- `edge_count = 256`
- `warning_count = 5`
- `duplicate_edge = 0`
- `orphan_node = 5`

### Post-fix full operator rerun (`20260418T021054Z`)
- `edge_count = 270`
- `warning_count = 4`
- `duplicate_edge = 0`
- `orphan_node = 4`

## Outcome
The one-command ready-family operator path no longer reintroduces the duplicate-edge regression. The full source-to-graph rerun is now aligned with the hardened build path on the critical metric (`duplicate_edge = 0`) and improved the remaining orphan count from 5 to 4.
