---
task: generic-aggregate-command-path
created: 2026-04-18
status: complete
---

# Research — Generic aggregate command path

## Goal
Move from a laws-specific aggregate graph command to a reusable dataset-aggregate command path.

## Current reusable pieces
- `scripts/vitruvius/aggregate_manifest.py`
- `run-dataset-source-to-graph`
- manifest-driven graph execution

## Minimum viable generalization
Add a generic command that can:
- accept a completed-lanes ledger path
- accept a manifest-index path
- accept dataset metadata and output roots
- generate an aggregate manifest
- optionally execute the resulting graph

The existing laws path can then become a thin specialization of the generic path.
