# 2026-04-17 Laws Risk Hardening Execution Validation

## Scope
Bounded risk-reduction pass after the tranche source-to-graph execute slice.

## Risk lanes addressed
1. `PD-957` duplicate/raw-alias visibility
2. `PD-1216` OCR quality confidence / acceptance reporting
3. bounded graph-richness next-slice identification

## Changes
- `scripts/vitruvius/laws_readiness.py`
  - tranche dry-run and execute summaries now preserve:
    - duplicate visibility
    - raw-alias visibility
    - guardrail law-folder visibility
    - OCR spot-review counts
- `scripts/vitruvius/dataset_pipeline.py`
  - source-quality summary now rolls up:
    - `source_acceptance_counts`
    - `spot_review_required_paths`
    - `spot_review_required_count`
- `scripts/tests/test_dataset_source_to_graph_pipeline.py`
  - added OCR-like spot-review regression coverage

## Verification
- `python3 -m py_compile scripts/vitruvius/dataset_pipeline.py scripts/vitruvius/laws_readiness.py scripts/tests/test_dataset_source_to_graph_pipeline.py`
- `python3 -m pytest scripts/tests/test_dataset_source_to_graph_pipeline.py scripts/tests/test_dataset_pipeline_cli.py -k 'source_to_graph or duplicate' -q`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-to-graph-dry-run --tranche-manifest config/datasets/laws-tranche-1.yaml --review-preset m2-8gb-safe`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-to-graph --tranche-manifest config/datasets/laws-tranche-1.yaml --review-preset m2-8gb-safe`

## Fresh evidence
- targeted tests:
  - `16 passed, 13 deselected`
- fresh tranche dry-run:
  - `duplicate_law_folders = [PD-957]`
  - `raw_alias_law_folders = [PD-957]`
  - `guardrail_law_folders = [PD-957]`
  - `spot_review_required_count = 1`
  - `summary_auto_withheld_count = 1`
  - `shallow_representation_count = 0`
- fresh tranche execute:
  - `duplicate_law_folders = [PD-957]`
  - `raw_alias_law_folders = [PD-957]`
  - `guardrail_law_folders = [PD-957]`
  - `spot_review_required_count = 1`
  - `summary_auto_withheld_count = 1`
  - `generated_relationship_count = 2`
  - `source_to_graph_execute_completed = true`

## Conclusions
- duplicate/raw-alias risk is still present for `PD-957`, but it is now more explicit in tranche reports
- `PD-1216` OCR is no longer a blind accept path; it now rolls up as `accepted_with_spot_review` with withheld automated summary prose
- broader widening should still remain gated
