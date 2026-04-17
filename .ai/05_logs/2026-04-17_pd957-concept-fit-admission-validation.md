# 2026-04-17 PD-957 Concept-Fit Admission Validation

## Scope
Implement the smallest truthful PD-957 concept-fit slice after tranche source-to-graph dry-run showed a shallow-representation failure.

## Changes
- `config/datasets/laws-tranche-1.yaml`
  - admitted three shared concept paths for `PD-957`:
    - `floor-area`
    - `setbacks`
    - `yards`
  - admitted three dataset-scoped `governs` relationship paths for `PD-957`
- `006_System-Manifests/runs/datasets/laws-tranche-1/concept-slice-pd957/promotion_audit.log`
  - recorded the bounded concept-fit admission batch
- `006_System-Manifests/runs/datasets/laws-tranche-1/concept-slice-pd957/relationships/*.md`
  - added:
    - `rel-irr-revised-implementing-rules-and-regulations-for-pd-957-governs-concept-floor-area.md`
    - `rel-irr-revised-implementing-rules-and-regulations-for-pd-957-governs-concept-setbacks.md`
    - `rel-irr-revised-implementing-rules-and-regulations-for-pd-957-governs-concept-yards.md`
- `scripts/tests/test_dataset_pipeline_cli.py`
  - added coverage proving a three-concept tranche slice removes the shallow-representation finding in dry-run staging

## Verification
- `python3 -m py_compile scripts/vitruvius/laws_readiness.py scripts/tests/test_dataset_pipeline_cli.py`
- `python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py scripts/tests/test_canonical_rules_additional_laws.py -k 'tranche_source_to_graph_dry_run or source_admission or pd_957 or pd_1185' -q`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-to-graph-dry-run --tranche-manifest config/datasets/laws-tranche-1.yaml --review-preset m2-8gb-safe`

## Fresh evidence
- targeted tests:
  - `6 passed, 16 deselected`
- live tranche source-to-graph dry-run now shows:
  - `staged_law_folders = [PD-957, PD-1185]`
  - `blocked_law_folders = [PD-1216]`
  - `duplicate_law_folders = [PD-957]`
  - `shallow_representation_count = 0`
  - `source_to_graph_execute_ready = false`

## Conclusion
The bounded PD-957 concept-fit slice removed the current tranche shallow-representation failure without widening tranche execute.
`PD-1216` remains explicitly blocked pending OCR, and tranche execute remains gated.
