# 2026-04-16 Graph Visualization CLI Validation

## Scope
Add a browser-friendly graph visualization command and document the current visualization stack for development.

## Changes
- added `visualize-graph` CLI command in `scripts/pipeline_cli.py`
- added visualization renderer in `scripts/vitruvius/graph/visualize.py`
- added CLI operator-facing documentation in `scripts/vitruvius/cli_experience.py`
- added tests in `scripts/tests/test_graph_visualize_cli.py`
- updated `README.md` with graph build/query/visualization workflow and stack direction

## Stack decision
Current development visualization stack:
- snapshot JSON from the existing graph pipeline
- HTML artifact generated locally by CLI
- Cytoscape.js in the browser for pan/zoom/selection/neighborhood inspection

Future browser-product note:
- keep the same snapshot contract
- continue with Cytoscape.js unless graph scale later justifies a move to Sigma.js or another large-graph renderer

## Verification
- `python3 -m py_compile scripts/vitruvius/graph/visualize.py scripts/pipeline_cli.py scripts/vitruvius/cli_experience.py scripts/tests/test_graph_visualize_cli.py`
  - PASS
- `PYTHONPATH=scripts pytest -q scripts/tests/test_graph_visualize_cli.py scripts/tests/test_graph_cli.py scripts/tests/test_pipeline_cli_byte_identity.py`
  - `18 passed in 1.96s`
- `git diff --check`
  - PASS

## Real-run evidence
- command:
  - `PYTHONPATH=scripts python3 scripts/pipeline_cli.py visualize-graph --snapshot 005_Operational-Intelligence-Layer/graph/datasets/laws-core-bundle-m1/20260416T095937Z_graph_snapshot.json`
- result:
  - PASS
- emitted file:
  - `004_Derived-Content-Layer/graph-visualizations/laws-core-bundle-m1/20260416T095937Z_graph_snapshot.html`
- emitted summary:
  - `node_count = 26`
  - `edge_count = 53`
- file-content checks:
  - contains Cytoscape.js loader
  - contains dataset id `laws-core-bundle-m1`
  - contains run id `20260416T095937Z`
  - contains known concept id `concept-accessible-ramps`

## Caveat
This improves the renderer and workflow, but it does not make a 26-node bounded pilot graph visually resemble a much denser public knowledge-graph demo. That visual density requires more graph content in future slices, not just a different renderer.
