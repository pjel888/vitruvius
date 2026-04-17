# 2026-04-17 Laws Duplicate Readiness Validation

## Scope
Add an exact-duplicate raw-PDF readiness surface for whole-laws and tranche-scoped widening, then expose those duplicate clusters inside the existing readiness reports.

## Changes
- `scripts/vitruvius/laws_readiness.py`
  - added exact duplicate cluster reporting for laws raw PDFs
  - reuses `latest_raw_file_registry.csv` SHA-256 data when available, with direct hashing fallback
  - added `run_laws_duplicate_dry_run(...)`
  - injected duplicate-cluster summaries into:
    - `run-laws-all-dry-run`
    - `run-laws-tranche-dry-run`
- `scripts/pipeline_cli.py`
  - wired `run-laws-duplicate-dry-run`
- `scripts/vitruvius/cli_experience.py`
  - documented the duplicate-readiness checkpoint
- `scripts/tests/test_dataset_pipeline_cli.py`
  - added coverage for:
    - exact duplicate report command
    - duplicate cluster exposure in all-laws readiness
    - duplicate cluster exposure in tranche readiness

## Verification
- `python3 -m py_compile scripts/vitruvius/laws_readiness.py scripts/pipeline_cli.py scripts/vitruvius/cli_experience.py scripts/tests/test_dataset_pipeline_cli.py`
- `python3 -m pytest scripts/tests/test_dataset_pipeline_cli.py -k 'run_laws_all_dry_run or run_laws_tranche_dry_run or run_laws_duplicate_dry_run' -q`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-duplicate-dry-run --tranche-manifest config/datasets/laws-tranche-1.yaml`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-all-dry-run --review-preset m2-8gb-safe`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-dry-run --tranche-manifest config/datasets/laws-tranche-1.yaml --review-preset m2-8gb-safe`

## Fresh evidence
- targeted tests:
  - `4 passed, 11 deselected`
- tranche duplicate dry-run:
  - `duplicate_cluster_count = 1`
  - `duplicate_law_folders = [PD-957]`
- whole-laws readiness now surfaces corpus-wide duplicate risk:
  - `duplicate_cluster_count = 9`
  - `duplicate_law_folders = [EO, HLURB-DHSUD, LGU, PD-1096, PD-957, RA-7160, RA-9266]`
- tranche readiness now surfaces duplicate risk directly:
  - `duplicate_cluster_count = 1`
  - `duplicate_law_folders = [PD-957]`

## Conclusion
The repo now has an explicit duplicate-readiness checkpoint before broader laws widening.
Exact duplicate raw PDFs are visible at:
- whole-laws scope
- tranche scope

This reduces the risk of scaling duplicate raw evidence into wider tranche or all-laws execution while keeping the raw layer immutable.
