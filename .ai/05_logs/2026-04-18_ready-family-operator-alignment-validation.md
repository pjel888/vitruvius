---
task: ready-family-operator-alignment
created: 2026-04-18
status: in_progress
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

## Pending
- wait for the full operator rerun to complete
- compare resulting warning counts with the hardened build-path baseline (`warning_count = 5`, `duplicate_edge = 0`)
