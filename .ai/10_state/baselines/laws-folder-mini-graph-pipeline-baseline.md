---
task: laws-folder-mini-graph-pipeline
phase: 02
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# Baseline — Laws-Folder Mini Graph Pipeline

## Current Capability Snapshot
- Vitruvius already has a real canonical-layer → graph path:
  - `build-graph`
  - `query-graph`
  - `export-graph-owl`
  - `query`
  - `query-structured`
- The graph builder currently reads from the whole canonical shared root:
  - `003_Canonical-Knowledge-Layer/shared/sources`
  - `003_Canonical-Knowledge-Layer/shared/concepts`
  - `003_Canonical-Knowledge-Layer/shared/relationships`
- Existing upstream stages already cover source→canonical→relationship promotion:
  - `scan`
  - `convert` / `convert-one`
  - `refine` / `refine-one`
  - `canonicalize` / `canonicalize-one`
  - `extract-relationships-one` / `extract-relationships-sections-one`
  - `review-relationships-ollama`
  - `review-relationships-ollama-second-pass`
  - `promote`

## Current Gaps Relative to User Goal
- no folder-scoped orchestration command from raw folder → graph
- no dataset manifest or workspace concept for isolated pilot graphs
- review/promotion flows rely on latest global run artifacts rather than dataset-scoped artifacts
- `build-graph` is whole-canonical-layer only, not one-folder or one-section scoped
- the future performance-sensitive pieces are not yet isolated from orchestration, so any Rust discussion is premature until the full path and blast radius are mapped

## Sample Pilot Candidate
- raw folder root: `001_Raw-Source-Layer/001-Laws/`
- user-preferred first pilot bundle:
  - `001_Raw-Source-Layer/001-Laws/PD-1096/`
  - `001_Raw-Source-Layer/001-Laws/RA-9514/`
  - `001_Raw-Source-Layer/001-Laws/BP-344/`
  - `001_Raw-Source-Layer/001-Laws/BP-220/`
- matching conversion subtree already exists under `002_Raw-Conversion-Layer/001-Laws/...`
