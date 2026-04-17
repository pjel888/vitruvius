# 2026-04-17 Validation — Tranche source-admission variant selection

## Scope
- respect manifest-level authoritative/excluded variant intent during tranche source admission
- preserve configured raw-anchor intent when a law remains blocked
- fix the tranche-3 PD-1151 canonical rule mismatch

## Fresh verification
- `python3 -m py_compile scripts/vitruvius/laws_readiness.py scripts/tests/test_dataset_pipeline_cli.py`
- `python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py -k 'source_admission or source_to_graph' -q`
  - **8 passed, 13 deselected**

## Live tranche-3 evidence after fix
- `run-laws-tranche-source-admission-dry-run`
  - ready: `PD-1067`, `PD-1151`, `RA-9003`
  - blocked: none
  - `candidate_source_page_count = 4`
  - `excluded_prepared_count = 1`
- `run-laws-tranche-source-admission`
  - `admitted_source_page_count = 4`
  - `canonicalize_failure_count = 0`
- `run-laws-tranche-source-to-graph-dry-run`
  - staged: `PD-1067`, `PD-1151`, `RA-9003`
  - blocked: none
  - `raw_alias_law_folders = [PD-1067]`
  - `shallow_representation_count = 1`
- `run-laws-tranche-source-to-graph`
  - `source_to_graph_execute_completed = true`
  - `generated_relationship_count = 0`
  - `shallow_representation_count = 1`

## Truthful residuals
- tranche-3 is execute-capable, but still graph-thin
- `PD-1067` keeps explicit raw-alias visibility because the older IRR variant remains excluded rather than silently discarded
