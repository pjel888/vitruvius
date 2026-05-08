# AEC Node Consolidation Discovery Context

Created: 2026-05-07T01:47:56Z

## Objective

Extend the pending-only AEC relationship-improvement workflow so it can also propose reviewable node-consolidation candidates for likely duplicate or near-duplicate Backbone nodes. The workflow should continue improving relationships, and optionally add node-improvement artifacts such as "these two nodes may represent the same concept" without mutating active graph data.

## Safety Boundary

- No active graph file mutation.
- No Neo4j or Postgres writes.
- No `--apply`; existing deferred safety error remains mandatory.
- No automatic canonical label mutation, alias application, redirect, tombstone, migration, or node retirement.
- No Kimi routing unless explicitly experimental; default routing remains local + DeepSeek.
- No API keys, bearer tokens, reasoning content, embeddings, or huge raw model responses in artifacts.
- All outputs are pending review artifacts under the run directory.

## Relevant Code Touchpoints

- `scripts/vitruvius/kg/aec_relationship_improvement.py`
  - `RunConfig`, `Checkpoint`, `RunSummary`
  - `BackboneNodeView`, `CandidatePair`, embedding generation, candidate generation
  - `RelationshipCouncil` provider routing and local/cloud calls
  - `run_relationship_improvement`
  - output files, report, summary text, review TSVs, watcher snapshot
  - CLI helpers `add_cli_arguments`, `config_from_args`
- `scripts/pipeline_cli.py`
  - `aec-improve-relationships` parser
  - command dispatch into `config_from_args` / `run_relationship_improvement`
- `scripts/tests/test_kg_aec_relationship_improvement.py`
  - existing fake embedder/model patterns and parser tests.

## Repository Evidence

- Current roadmap/state explicitly blocks graph mutation, merge/alias/redirect/tombstone actions, protected payload admission, and production promotion.
- `architecture_civil_structural_gate_review.py` exports duplicate merge review candidates with `auto_merge_allowed=false`, `batch_merge_blocked=true`, `requires_steward_decision=true`.
- `merge_adjudicator.py` proposes exact-match merge assertions for review only and requires evidence.

## Implementation Shape

- Add optional `--improve-nodes`; default remains relationship-only.
- Add node consolidation candidate generation using existing embeddings and top-k similarity, with stricter thresholds than relationship discovery.
- Add deterministic guards before model calls and final candidate classification.
- Add a `NodeConsolidationDecision` schema and prompt.
- Reuse `RelationshipCouncil` for provider routing, but parse node decisions with node-specific validation.
- Write node-only pending artifacts and review TSVs.
- Add checkpoint/report/summary counters for operator visibility.

## Validation Targets

- Existing relationship tests remain passing.
- New tests cover parser flags, node candidate generation, deterministic parent/child guard, pending-only output, review TSV/report fields, provider metadata, sanitizer behavior, and `--apply` rejection.
