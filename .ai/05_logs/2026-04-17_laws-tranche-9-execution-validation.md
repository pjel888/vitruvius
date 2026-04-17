# 2026-04-17 Validation — Laws tranche-9 bounded execution

## Manifest
- `config/datasets/laws-tranche-9.yaml`

## Selected tranche-9 surfaces
- `DENR` → `DENR DAO 2003-30 - EIS System Implementing Rules.pdf`
- `DOE` → `DOE Guidelines on Energy Conserving Design on Buildings v2008.pdf`
- `DPWH` → `DPWH DO037 Enforcement of BP344 along National Roads.pdf`

## Selection rationale
- zero exact duplicate clusters in the scoped cohort
- all scoped authoritative files use the direct prep path
- auxiliary guidance surfaces remain excluded where needed (`DENR` revised procedural manual, `DPWH` flood-control draft)

## Fresh verification
- `python3 -m pytest scripts/tests/test_canonical_rules_additional_laws.py -q`
  - **32 passed**
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-duplicate-dry-run --tranche-manifest config/datasets/laws-tranche-9.yaml`
  - `duplicate_cluster_count = 0`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-prep --tranche-manifest config/datasets/laws-tranche-9.yaml`
  - `prepared_count = 3`
  - `ocr_required_count = 0`
  - `failed_count = 0`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-admission --tranche-manifest config/datasets/laws-tranche-9.yaml`
  - `admitted_source_page_count = 3`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-to-graph --tranche-manifest config/datasets/laws-tranche-9.yaml --review-preset m2-8gb-safe`
  - `staged_law_folders = [DENR, DOE, DPWH]`
  - `generated_relationship_count = 0`
  - `shallow_representation_count = 0`
  - graph snapshot: `3 nodes / 0 edges`

## Truthful residuals
- tranche-9 is operationally clean but graph-light
- next likely follow-on would be bounded concept-fit work, probably starting from `DPWH DO037` because it overlaps accessible design enforcement concepts more directly than the DENR/DOE guidance surfaces
