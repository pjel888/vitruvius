---
task: aec-execution-dependency-manifest
phase: 00
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# AEC Execution Dependency Manifest

## Purpose
This artifact lists the minimum dependency/tooling expectations for bounded first-slice execution on the clean baseline worktree.

## Python lane
Required:
- `python3`
- `pytest`
- repo Python dependencies sufficient to run `scripts/tests/test_aec_*` plus adjacent `test_spatial_*`, `test_graph_*`, and `test_geometric_*` smoke lanes when needed

## TypeScript adjacent lane
Required when boundary-adjacent TS files are touched:
- Node runtime
- `spatial-daemon/package.json` dependencies installed
- `vitest` available through local project tooling
- typecheck command available

## Repo-local expectations
- clean baseline worktree exists at `/Users/philiplewis/vitruvius-aec-clean-baseline`
- bounded `test_aec_*` files exist before attempting G10 closure
- bounded first-slice fixtures exist before attempting G10 closure

## Interpretation rule
A missing dependency is an environment/preflight problem.
A missing `test_aec_*` file or fixture is still part of G10 execution evidence.
Do not conflate the two.

## Final rule
Use this manifest together with the clean-baseline preflight and remediation guide before starting execution.
