# 2026-04-17 Laws Tranche-2 Candidate Scout (Worker 1) Validation

## Scope
Gather fresh readiness evidence for tranche-2 candidate selection and duplicate/quality deferral risk.

## Commands run
1. `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-all-dry-run --review-preset m2-8gb-safe`
2. `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-duplicate-dry-run`
3. `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-duplicate-dry-run --tranche-manifest /tmp/laws-tranche-2-candidate.yaml`
4. `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-prep-dry-run --tranche-manifest /tmp/laws-tranche-2-candidate.yaml`
5. `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-dry-run --tranche-manifest /tmp/laws-tranche-2-candidate.yaml --review-preset m2-8gb-safe`

## Key outputs
- whole-laws readiness:
  - `run_id = 20260417T082529Z`
  - `inventory_only_law_count = 43`
  - `duplicate_cluster_count = 9`
- whole-laws duplicate dry-run:
  - `duplicate_law_folders = [EO, HLURB-DHSUD, LGU, PD-1096, PD-957, RA-7160, RA-9266]`
- scout duplicate dry-run:
  - `duplicate_cluster_count = 0`
- scout source-prep dry-run:
  - `raw_file_count = 3`
  - `supported_direct_input_count = 3`
  - all three files detected as `TEXT_PDF`
  - all three files recommended route `OPENDATALOADER_DIRECT`
- scout tranche dry-run:
  - `candidate_law_folders = [RA-7279, RA-4726, RA-7899]`
  - `structure_guardrail_law_folders = []`
  - `duplicate_law_folders = []`

## Conclusion
The cleanest next bounded scout set is `RA-7279`, `RA-4726`, and `RA-7899`. Duplicate-heavy or heterogeneous folders should stay excluded/deferred from tranche-2 until cleaned up.
