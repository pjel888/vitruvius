# 2026-04-17 Validation — Laws tranche-3 bounded execution

## Manifest
- `config/datasets/laws-tranche-3.yaml`

## Selected tranche-3 laws
- `PD-1067`
- `PD-1151`
- `RA-9003`

## Selection rationale
- zero exact duplicate clusters in the tranche candidate set
- direct text-PDF readiness for all selected files
- bounded utilities/environmental-law adjacency rather than generic whole-laws widening

## Fresh verification
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-duplicate-dry-run --tranche-manifest config/datasets/laws-tranche-3.yaml`
  - `duplicate_cluster_count = 0`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-prep --tranche-manifest config/datasets/laws-tranche-3.yaml`
  - `prepared_count = 5`
  - `ocr_required_count = 0`
  - `failed_count = 0`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-admission --tranche-manifest config/datasets/laws-tranche-3.yaml --source-prep-report 006_System-Manifests/runs/datasets/laws-tranche-3/20260417T103824Z/laws_tranche_source_prep_report.json`
  - `admitted_source_page_count = 4`
  - `blocked_law_folders = []`
- `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-tranche-source-to-graph --tranche-manifest config/datasets/laws-tranche-3.yaml --review-preset m2-8gb-safe`
  - staged: `PD-1067`, `PD-1151`, `RA-9003`
  - `generated_relationship_count = 0`
  - `raw_alias_law_folders = [PD-1067]`
  - `shallow_representation_count = 1`
  - `source_to_graph_execute_completed = true`

## Output artifacts
- `005_Operational-Intelligence-Layer/graph/datasets/laws-tranche-3-source-to-graph-execute/20260417T104201Z_graph_snapshot.json`
- `006_System-Manifests/runs/datasets/laws-tranche-3-source-to-graph-execute/20260417T104201Z_build_graph_dataset_report.json`
- `006_System-Manifests/runs/datasets/laws-tranche-3/source_to_graph_execute/20260417T104201Z/laws_tranche_source_to_graph_execute_report.json`

## Truthful residuals
- tranche-3 is now a successful bounded execute lane
- tranche-3 still needs graph-richness follow-on work before it should be considered mature
