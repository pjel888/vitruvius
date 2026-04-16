# 2026-04-16 Graph Human Labels Validation

## Scope
Make the graph explorer more human-readable by preferring human titles over raw ids.

## What changed
- graph nodes now carry optional `title`
- builder populates titles from canonical source/concept frontmatter when available
- visualizer defaults to human-readable labels and searches by title or id

## Verification
- graph/visualizer focused suites passed
- real dataset graph snapshot now contains node titles
- real visualizer output contains human-readable labels like:
  - `PD 1096`
  - `Building Permit`

## Real evidence
- snapshot:
  - `005_Operational-Intelligence-Layer/graph/datasets/laws-core-bundle-m1/20260416T145312Z_graph_snapshot.json`
- visualizer output:
  - `004_Derived-Content-Layer/graph-visualizations/laws-core-bundle-m1/20260416T145312Z_graph_snapshot.html`
