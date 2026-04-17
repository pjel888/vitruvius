# 2026-04-17 Validation — Laws tranche-7 bounded execution

## Manifest
- `config/datasets/laws-tranche-7.yaml`

## Selected tranche-7 laws
- `RA-1378`
- `RA-9285`
- `RA-11201`

## Fresh verification
- `python3 -m pytest scripts/tests/test_canonical_rules_additional_laws.py -q`
  - **28 passed**
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-duplicate-dry-run --tranche-manifest config/datasets/laws-tranche-7.yaml`
  - `duplicate_cluster_count = 0`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-to-graph --tranche-manifest config/datasets/laws-tranche-7.yaml --review-preset m2-8gb-safe`
  - `staged_law_folders = [RA-9285, RA-11201]`
  - `blocked_law_folders = [RA-1378]`
  - `generated_relationship_count = 0`
  - `shallow_representation_count = 0`
  - graph snapshot: `6 nodes / 6 edges`

## Truthful residuals
- tranche-7 is representationally sound for the currently staged laws
- `RA-1378` is now best described as **mixed readiness**, not a pure prep rerun TODO:
  - the authoritative `MASTER PLUMBING LAW.pdf` variant was prepared and admitted
  - excluded plumbing-code / board files stayed explicit
  - the law family still remains outside staged source-to-graph because the excluded `Board of Master Plumber.doc` prep failure leaves `source_admission_state = admitted_subset_failed`
- tranche-7 still carries `spot_review_required_count = 2` and `summary_auto_withheld_count = 2`

## Updated tranche-7 clean rerun
- manifest-scoped prep rerun now stages all three tranche-7 laws cleanly
- refreshed execute evidence:
  - `staged_law_folders = [RA-1378, RA-9285, RA-11201]`
  - `blocked_law_folders = []`
  - `generated_relationship_count = 0`
  - `shallow_representation_count = 0`
  - graph snapshot: `7 nodes / 6 edges`
- see `/.ai/05_logs/2026-04-17_laws-tranche-7-clean-rerun-validation.md`
