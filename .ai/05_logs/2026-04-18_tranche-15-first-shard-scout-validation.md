# 2026-04-18 Validation — Tranche-15 first LGU shard scout

## Shard manifest
- `config/datasets/laws-tranche-15-san-mateo.yaml`

## Selected first shard
- `794216046-San-Mateo-Zoning-Ordinance.pdf`
- `844057380-Copy-of-San-Mateo-Rizal-clup.pdf`

## Fresh verification
- representative source detection:
  - `python3 scripts/pipeline_cli.py detect-one '/Users/philiplewis/vitruvius/001_Raw-Source-Layer/001-Laws/LGU/794216046-San-Mateo-Zoning-Ordinance.pdf'`
    - `RESULT: TEXT_PDF`
    - `RECOMMENDED ROUTE: OPENDATALOADER_DIRECT`
  - `python3 scripts/pipeline_cli.py detect-one '/Users/philiplewis/vitruvius/001_Raw-Source-Layer/001-Laws/LGU/844057380-Copy-of-San-Mateo-Rizal-clup.pdf'`
    - `RESULT: TEXT_PDF`
    - `RECOMMENDED ROUTE: OPENDATALOADER_DIRECT`
- shard duplicate screen:
  - `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-laws-duplicate-dry-run --tranche-manifest config/datasets/laws-tranche-15-san-mateo.yaml`
  - `duplicate_cluster_count = 2`
  - `duplicate_law_folders = [LGU]`
- shard source-prep dry-run:
  - `raw_file_count = 2`
  - `supported_direct_input_count = 2`
  - `refined_markdown_ready_count = 0`

## Truthful conclusion
- San Mateo is still the strongest first shard candidate inside `LGU`
- but the current duplicate screen remains folder-granular enough to mark the whole `LGU` shard duplicate-affected because unrelated duplicate files elsewhere in the folder are still seen
- this means the next truthful move is not normal shard execution yet
- the next move is to refine LGU sharding/remediation so duplicate readiness is scoped to the selected shard rather than the whole folder
