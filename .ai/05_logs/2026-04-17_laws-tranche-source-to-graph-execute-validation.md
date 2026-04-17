# 2026-04-17 Laws Tranche Source-to-Graph Execute Validation

## Scope
Implement and run the bounded tranche-local source-to-graph execute wrapper after tranche dry-run readiness, PD-957 concept-fit admission, and PD-1216 OCR-first preparation.

## Changes
- `scripts/vitruvius/laws_readiness.py`
  - added `run_laws_tranche_source_to_graph(...)`
  - added execute-specific derived-manifest/report roots
  - preserved admitted-only staging while keeping duplicate visibility explicit
- `scripts/pipeline_cli.py`
  - wired `run-laws-tranche-source-to-graph`
- `scripts/vitruvius/cli_experience.py`
  - documented the tranche execute wrapper
- `scripts/tests/test_dataset_pipeline_cli.py`
  - added execute-wrapper coverage
- `README.md`
  - documented the execute command

## Verification
- `python3 -m py_compile scripts/vitruvius/laws_readiness.py scripts/pipeline_cli.py scripts/vitruvius/cli_experience.py scripts/tests/test_dataset_pipeline_cli.py scripts/tests/test_canonical_rules_additional_laws.py`
- `python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py scripts/tests/test_canonical_rules_additional_laws.py -k 'tranche_source_to_graph_dry_run or tranche_source_to_graph_execute or prepare_raw_file_allow_ocr or pd_1216 or pd_957 or pd_1185' -q`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-to-graph --tranche-manifest config/datasets/laws-tranche-1.yaml --review-preset m2-8gb-safe`

## Fresh evidence
- targeted tests:
  - `7 passed, 18 deselected`
- live execute summary:
  - `staged_law_folders = [PD-957, PD-1216, PD-1185]`
  - `blocked_law_folders = []`
  - `duplicate_law_folders = [PD-957]`
  - `generated_relationship_count = 2`
  - `filtered_relationship_count = 0`
  - `manual_review_required_count = 0`
  - `shallow_representation_count = 0`
  - `source_to_graph_execute_completed = true`
- live execute output paths:
  - graph snapshot:
    - `005_Operational-Intelligence-Layer/graph/datasets/laws-tranche-1-source-to-graph-execute/20260417T071754Z_graph_snapshot.json`
  - graph build report:
    - `006_System-Manifests/runs/datasets/laws-tranche-1-source-to-graph-execute/20260417T071754Z_build_graph_dataset_report.json`
  - pipeline report:
    - `006_System-Manifests/runs/datasets/laws-tranche-1-source-to-graph-execute/source_to_graph/20260417T071754Z/source_to_graph_run_report.json`
  - wrapper report:
    - `006_System-Manifests/runs/datasets/laws-tranche-1/source_to_graph_execute/20260417T071754Z/laws_tranche_source_to_graph_execute_report.json`

## Conclusion
The tranche source-to-graph execute slice now runs successfully as a bounded wrapper.
All three tranche laws are staged, duplicate visibility is preserved, and the tranche can now build and test a real knowledge-graph execution lane without widening into generic all-laws execution.
