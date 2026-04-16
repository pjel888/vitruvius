# 2026-04-16 Graph Explorer Hardening Validation

## Scope
Follow-on hardening after the initial graph explorer + graph quality correction work.

## Changes
- `scripts/pipeline_cli.py`
  - malformed `--structured-check` values now return a clean JSON error with exit code `2`
- `scripts/vitruvius/graph/visualize.py`
  - uses local Cytoscape asset path instead of CDN
  - embeds snapshot/elements data more safely
  - adds basic explorer controls:
    - source/concept toggles
    - layout selector
    - label mode selector
- `scripts/tests/test_dataset_pipeline_cli.py`
  - added malformed structured-check regression
- `scripts/tests/test_graph_visualize_cli.py`
  - added local asset-path coverage
- `README.md`
  - clarified that official graph density is bounded by admitted truth-bearing inputs
  - clarified visualization workflow and current stack

## Verification
- `python3 -m py_compile scripts/vitruvius/graph/visualize.py scripts/pipeline_cli.py scripts/tests/test_graph_visualize_cli.py scripts/tests/test_dataset_pipeline_cli.py`
  - PASS
- `PYTHONPATH=scripts pytest -q scripts/tests/test_graph_visualize_cli.py scripts/tests/test_dataset_pipeline_cli.py scripts/tests/test_pipeline_cli_byte_identity.py scripts/tests/test_graph_dataset_cli.py scripts/tests/test_relationships_sections_split.py scripts/tests/test_integration_e2e.py scripts/tests/test_concept_matching.py scripts/tests/test_source_identity.py scripts/tests/test_concept_enrichment.py`
  - `43 passed in 34.41s`
- `git diff --check`
  - PASS

## Fresh behavior checks
### malformed structured-check
- command:
  - `python3 scripts/pipeline_cli.py run-dataset-graph --dataset-manifest config/datasets/laws-core-bundle-m1.yaml --structured-check badformat`
- result:
  - rc = `2`
  - stdout JSON:
    - `{"error": "structured checks must use FUNCTION:SUBJECT format"}`
  - stderr empty

### visualize-graph
- command:
  - `python3 scripts/pipeline_cli.py visualize-graph --snapshot 005_Operational-Intelligence-Layer/graph/datasets/laws-core-bundle-m1/20260416T105101Z_graph_snapshot.json`
- result:
  - rc = `0`
  - HTML output written
  - HTML no longer depends on `https://unpkg.com`
  - HTML contains explorer controls
