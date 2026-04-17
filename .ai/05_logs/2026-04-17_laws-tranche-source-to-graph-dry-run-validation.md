# 2026-04-17 Laws Tranche Source-to-Graph Dry-Run Validation

## Scope
Add a tranche-local source→graph dry-run checkpoint after tranche source admission and duplicate hardening.

## Changes
- `scripts/vitruvius/laws_readiness.py`
  - added derived manifest generation from executed tranche source-admission state
  - added `run_laws_tranche_source_to_graph_dry_run(...)`
  - stages only admitted tranche members and keeps blocked members explicit
- `scripts/pipeline_cli.py`
  - wired `run-laws-tranche-source-to-graph-dry-run`
- `scripts/vitruvius/cli_experience.py`
  - documented the new tranche-local source→graph dry-run checkpoint
- `scripts/tests/test_dataset_pipeline_cli.py`
  - added CLI coverage proving only admitted tranche members stage
- `README.md`
  - documented the new command

## Verification
- `python3 -m py_compile scripts/vitruvius/laws_readiness.py scripts/pipeline_cli.py scripts/vitruvius/cli_experience.py scripts/tests/test_dataset_pipeline_cli.py`
- `python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py scripts/tests/test_canonical_rules_additional_laws.py -k 'source_admission or source_to_graph_dry_run or run_laws_all_dry_run or run_laws_tranche_dry_run or run_laws_duplicate_dry_run or pd_957 or pd_1185' -q`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-to-graph-dry-run --tranche-manifest config/datasets/laws-tranche-1.yaml --review-preset m2-8gb-safe`

## Fresh evidence
- targeted tests:
  - `9 passed, 12 deselected`
- live tranche source-to-graph dry-run:
  - `staged_law_folders = [PD-957, PD-1185]`
  - `blocked_law_folders = [PD-1216]`
  - `duplicate_cluster_count = 1`
  - `duplicate_law_folders = [PD-957]`
  - `planned_stage_count = 2`
  - `shallow_representation_count = 1`
  - `source_to_graph_execute_ready = false`

## Conclusion
The repo now has a truthful tranche-local source→graph dry-run checkpoint.
It stages only admitted tranche members, keeps blocked members explicit, preserves duplicate visibility, and still keeps execute gated.
