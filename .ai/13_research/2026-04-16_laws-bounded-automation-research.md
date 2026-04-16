# Research Pack — Bounded Laws Source→Graph Automation

## Purpose
Define the smallest truthful automation slice that can run a bounded laws dataset from produced pipeline data through to a dataset graph without bypassing governance.

## Current verified truth
- `run-dataset-graph` already automates:
  - scoped graph build
  - optional Turtle export
  - optional structured checks
- It does **not** automate the full bounded upstream lane:
  - refine
  - canonicalize
  - extract
  - review
  - promote
  - then graph

## Why the current command is insufficient
The current command starts from **already admitted** canonical/promoted inputs.
That is correct for graph truth, but it is not the full bounded source→graph pipeline the user now requires.

## Truth boundary
The automation command must not:
- read raw files directly into the graph
- bypass review/promotion
- silently mutate global `latest_*` artifacts
- silently mutate unrelated shared truth outside the selected bounded slice

## Smallest acceptable automation model
Introduce a bounded automation lane that uses **produced pipeline data** and explicit manifest-driven paths.

### Proposed phases
1. verify/select refined markdown inputs per law unit
2. canonicalize selected refined sources
3. extract section-aware relationship candidates dataset-locally
4. review dataset-locally
5. promote dataset-locally
6. build/query/export graph from the resulting bounded dataset inputs

### Required data additions
The manifest needs enough structure to automate this safely, likely:
- `refined_markdown_paths`
- `canonical_source_paths`
- `relationship_staging_root` or derived run root
- optional `concept_allowlist_paths`

## Design principle
The automation lane should be **bounded and replayable**:
- dry-run first
- execute only when explicit
- every stage writes dataset-local artifacts
- graph outputs stay dataset-local

## What “step 1” should mean here
For this bounded automation lane, “step 1” should mean:
- start from selected source/refined/canonical pipeline assets we already produce
- not raw-PDF-to-graph shortcutting

That preserves both correctness and auditability.
