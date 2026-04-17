---
task: dataset-wide-automation-mvp
created: 2026-04-18
status: complete
---

# Research — Dataset-wide automation MVP

## Goal
Generalize the laws-wave automation pattern so dataset-to-knowledge-graph execution is not special-cased to laws only.

## Current reusable pieces
Already reusable:
- `run-dataset-source-to-graph`
- manifest-driven graph execution
- machine-readable completed/disposition/provenance ledgers
- artifact indices and reload protocol pattern

Currently laws-specific:
- completed-lanes ledger schema and aggregate-manifest synthesis logic
- residual defer/disposition policy rules
- law-centric source-quality expectations and benchmark hints

## MVP direction
Build a generic automation layer that can:
1. define a dataset scope via machine-readable ledgers
2. synthesize an aggregate manifest from completed lane manifests
3. exclude deferred/non-authoritative items automatically
4. run one command to produce a graph for the trusted subset

## Why this is the right next step
The laws wave proved the pattern. The next leverage point is not more manual curation, but lifting the pattern into a generic dataset automation framework.
