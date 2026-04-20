<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-20 -->

# 005_Operational-Intelligence-Layer

## Purpose
Machine infrastructure: chunks, embeddings, graphs, and derived operational artifacts. This layer contains generated downstream content and must not silently redefine truth.

## Subdirectories
| Directory | Purpose |
|-----------|---------|
| `graph/` | Graph snapshots, build reports, and dataset graph outputs |
| `embeddings/` | Vector embeddings and chunk indexes |
| `chunks/` | Text chunks and chunk metadata |

## For AI Agents

### Working In This Directory
- **This layer is generated.** Do not hand-edit generated artifacts.
- **Graph snapshots** are the source of truth for graph state. Build them via `scripts/pipeline_cli.py build-graph`.
- **Do not commit large generated files.** This directory is gitignored for a reason.
- **Preserve artifact provenance.** Generated files must be traceable to the manifest and canonical inputs that produced them.

### Testing Requirements
- Verify graph build reports after any canonical layer change.
- Check that `build-graph` produces zero warnings before claiming graph health.

### Common Patterns
- Graph snapshots are timestamped: `YYYYMMDDTHHMMSSZ_graph_snapshot.json`.
- Build reports accompany snapshots: `YYYYMMDDTHHMMSSZ_build_graph_dataset_report.json`.
- Visualizations go to `004_Derived-Content-Layer/graph-visualizations/`.
