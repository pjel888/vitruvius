# 2026-04-17 Laws Tranche-1 Source Admission Implementation Validation

## Scope
Implementation follow-on after tranche-1 source-admission planning.

## Changes
- `scripts/vitruvius/laws_readiness.py`
  - added `run_laws_tranche_source_admission_dry_run(...)`
  - reports admission-ready vs blocked/incomplete tranche members
  - derives candidate canonical source paths for ready refined markdown inputs
  - keeps tranche source→graph execute explicitly gated
- `scripts/pipeline_cli.py`
  - wired `run-laws-tranche-source-admission-dry-run`
- `scripts/vitruvius/cli_experience.py`
  - documented the new tranche source-admission checkpoint
- `scripts/tests/test_dataset_pipeline_cli.py`
  - added CLI coverage for ready-vs-blocked tranche admission state
- `README.md`
  - documented the tranche-1 source-admission checkpoint

## Expected truthful tranche split
- `PD-957` — ready for source admission review
- `PD-1185` — ready for source admission review
- `PD-1216` — blocked pending OCR-first processing

## Verification
- `python3 -m py_compile scripts/pipeline_cli.py scripts/vitruvius/laws_readiness.py scripts/vitruvius/cli_experience.py`
- `python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py -q`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-admission-dry-run --tranche-manifest config/datasets/laws-tranche-1.yaml`

## Fresh evidence
Result summary:
- `admission_review_ready_law_folders = [PD-957, PD-1185]`
- `blocked_law_folders = [PD-1216]`
- `candidate_source_page_count = 5`
- `source_to_graph_execute_ready = false`

## Conclusion
The repo now has an explicit tranche-1 source-admission dry-run/report surface.
It preserves the ready-vs-blocked split and avoids implying tranche
source→graph execute readiness while PD-1216 remains OCR-blocked.
