# 2026-04-16 Graph Pipeline Self-Audit Validation

## Scope
- command chain audited: `build-graph` / `run-dataset-graph` / `query-structured` / `visualize-graph`
- purpose: explain current dataset/global divergence, capture a small performance baseline, and harden the visualization slice without changing graph truth

## Fresh evidence

### Measured command timings
- `python3 scripts/pipeline_cli.py run-dataset-graph --dataset-manifest config/datasets/laws-core-bundle-m1.yaml`
  - ~0.55s real
  - ~26 MB peak RSS
- `python3 scripts/pipeline_cli.py build-graph`
  - ~0.19s real
  - ~16 MB peak RSS
- `python3 scripts/pipeline_cli.py query-structured --snapshot 005_Operational-Intelligence-Layer/graph/datasets/laws-core-bundle-m1/20260416T095937Z_graph_snapshot.json --function what_governs --subject concept-building-permit`
  - ~0.11s real
  - ~16 MB peak RSS
- `python3 scripts/pipeline_cli.py visualize-graph --snapshot 005_Operational-Intelligence-Layer/graph/datasets/laws-core-bundle-m1/20260416T095937Z_graph_snapshot.json`
  - ~0.04s real
  - ~14 MB peak RSS

### Snapshot size check
- dataset snapshot `20260416T095937Z_graph_snapshot.json`
  - `node_count = 26`
  - `edge_count = 53`
  - size ≈ 101 KB
  - JSON parse ≈ 0.38 ms

### Global vs dataset divergence
- dataset snapshot and global snapshot currently contain the same 26 nodes
- dataset snapshot contains 4 additional edges not present in the global snapshot:
  - `rel-irr-implementing-rules-and-regulations-of-the-fire-code-of-the-philippines-governs-concept-certificate-of-occupancy`
  - `rel-irr-implementing-rules-and-regulations-of-the-fire-code-of-the-philippines-governs-concept-means-of-egress`
  - `rel-irr-revised-implementing-rules-and-regulations-of-batas-pambansa-blg-220-governs-concept-socialized-housing-projects`
  - `rel-irr-revised-implementing-rules-and-regulations-of-batas-pambansa-blg-344-governs-concept-accessible-ramps`
- these 4 edges are selected by the dataset manifest from dataset-local admitted relationship artifacts under `006_System-Manifests/runs/datasets/laws-core-bundle-m1/...`
- they are not present in `003_Canonical-Knowledge-Layer/shared/relationships/`, so the global build does not currently include them

### Orphan warning interpretation
- global `build-graph` still reports one orphan warning for:
  - `irr-implementing-rules-and-regulations-of-the-fire-code-of-the-philippines`
- this warning is currently explained by the same divergence above: the source node exists in the global canonical/shared source layer, but the currently admitted fire-code relationship edges live only in the dataset-local selected path
- conclusion: the warning is explainable and not evidence of dataset leakage; however, it is still a real signal that global/shared admission and dataset-local admission are not yet fully reconciled

## Hardening changes applied
- removed duplicate snapshot parsing in `scripts/vitruvius/graph/visualize.py`
  - `visualize-graph` now parses the snapshot JSON once and reuses the loaded payload for metadata + counts + HTML rendering
- expanded visualizer regression coverage for:
  - default global output path
  - explicit relative `--out` path handling
- updated README visualization guidance with:
  - current bounded-pilot size expectations
  - dataset-vs-global graph truth note

## Verification
- `PYTHONPATH=scripts pytest -q scripts/tests/test_graph_visualize_cli.py scripts/tests/test_dataset_pipeline_cli.py scripts/tests/test_graph_dataset_cli.py`
- `python3 -m py_compile scripts/vitruvius/graph/visualize.py`
- `python3 scripts/pipeline_cli.py visualize-graph --snapshot 005_Operational-Intelligence-Layer/graph/datasets/laws-core-bundle-m1/20260416T095937Z_graph_snapshot.json`
- `git diff --check`

## Result
- visualization slice is cleaner and better documented
- dataset/global graph divergence is now explicitly explained
- no graph truth semantics were widened in this self-audit pass
