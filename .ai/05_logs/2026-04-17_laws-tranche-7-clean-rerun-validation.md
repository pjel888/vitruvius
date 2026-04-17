# 2026-04-17 Validation — Laws tranche-7 clean rerun

## Scope
Re-run tranche-7 on the manifest-scoped source-prep path so `RA-1378` is staged truthfully with excluded auxiliary plumbing files left out of prep/admission.

## Fresh verification
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-to-graph-dry-run --tranche-manifest config/datasets/laws-tranche-7.yaml --review-preset m2-8gb-safe`
  - `staged_law_folders = [RA-1378, RA-9285, RA-11201]`
  - `blocked_law_folders = []`
  - `raw_alias_law_folders = [RA-1378]`
  - `shallow_representation_count = 0`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-to-graph --tranche-manifest config/datasets/laws-tranche-7.yaml --review-preset m2-8gb-safe`
  - `staged_law_folders = [RA-1378, RA-9285, RA-11201]`
  - `blocked_law_folders = []`
  - `generated_relationship_count = 0`
  - `shallow_representation_count = 0`
  - graph snapshot: `7 nodes / 6 edges`

## Outcome
`RA-1378` is now cleanly staged on the authoritative `MASTER PLUMBING LAW.pdf` path. Excluded plumbing-code / board files remain explicit as raw-alias visibility rather than blocking staged execution.
