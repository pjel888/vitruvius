# 2026-04-17 Laws Tranche-2 Execution Validation

## Scope
Create the next bounded manifest-backed tranche after tranche-1, then execute it through the same bounded workflow.

## Tranche-2 manifest
- `config/datasets/laws-tranche-2.yaml`
- candidate laws:
  - `RA-7279`
  - `RA-4726`
  - `RA-7899`

## Changes
- `scripts/vitruvius/rules/canonical_rules.yaml`
  - added canonical rules for:
    - `RA-7279`
    - `RA-4726`
    - `RA-7899`
- `scripts/tests/test_canonical_rules_additional_laws.py`
  - added rule coverage for those three laws
- `config/datasets/laws-tranche-2.yaml`
  - new bounded tranche manifest

## Verification
- `python3 -m pytest scripts/tests/test_canonical_rules_additional_laws.py -q`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-dry-run --tranche-manifest config/datasets/laws-tranche-2.yaml --review-preset m2-8gb-safe`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-prep-dry-run --tranche-manifest config/datasets/laws-tranche-2.yaml`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-prep --tranche-manifest config/datasets/laws-tranche-2.yaml`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-admission-dry-run --tranche-manifest config/datasets/laws-tranche-2.yaml --source-prep-report 006_System-Manifests/runs/datasets/laws-tranche-2/20260417T092005Z/laws_tranche_source_prep_report.json`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-admission --tranche-manifest config/datasets/laws-tranche-2.yaml --source-prep-report 006_System-Manifests/runs/datasets/laws-tranche-2/20260417T092005Z/laws_tranche_source_prep_report.json`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-to-graph-dry-run --tranche-manifest config/datasets/laws-tranche-2.yaml --review-preset m2-8gb-safe`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-to-graph --tranche-manifest config/datasets/laws-tranche-2.yaml --review-preset m2-8gb-safe`

## Fresh evidence
- tranche-2 dry-run:
  - `candidate_law_folder_count = 3`
  - `duplicate_cluster_count = 0`
  - `structure_guardrail_law_folders = []`
- tranche-2 source prep execute:
  - `prepared_count = 3`
  - `ocr_required_count = 0`
  - `failed_count = 0`
- tranche-2 source admission:
  - ready/admitted:
    - `RA-7279`
    - `RA-4726`
    - `RA-7899`
  - `admitted_source_page_count = 3`
- tranche-2 source-to-graph dry-run:
  - `staged_law_folders = [RA-7279, RA-4726, RA-7899]`
  - `blocked_law_folders = []`
  - `duplicate_law_folders = []`
  - `shallow_representation_count = 0`
- tranche-2 source-to-graph execute:
  - `staged_law_folders = [RA-7279, RA-4726, RA-7899]`
  - `generated_relationship_count = 0`
  - `filtered_relationship_count = 0`
  - `source_to_graph_execute_completed = true`
  - graph snapshot:
    - `005_Operational-Intelligence-Layer/graph/datasets/laws-tranche-2-source-to-graph-execute/20260417T092038Z_graph_snapshot.json`

## Interpretation
Tranche-2 now executes through the same bounded pipeline as tranche-1.
It is a clean, low-duplicate, housing/condominium-adjacent tranche, but it currently yields a sparse graph (`0` generated relationships), so it should be treated as a successful bounded execute lane, not as evidence of broad graph richness yet.
