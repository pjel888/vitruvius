---
task: aec-relationship-improvement
created_at_utc: 2026-05-01T14:14:45Z
status: active
---

# Ralph Context Snapshot

## Task Statement
Implement the first safe, pending-only Python CLI workflow for local Ollama-assisted AEC-MEPFS Backbone relationship improvement.

## Desired Outcome
Add a resumable, sequential, slow CLI command that reads existing Backbone nodes and relationships, builds/reuses embeddings, generates similarity candidate pairs, asks local Ollama judge/verifier models for conservative relationship decisions, and writes only review artifacts under `006_System-Manifests/aec-mepfs-backbone/semantic-overlays/<run_id>/`.

## Known Facts / Evidence
- Primary input: `scripts/tests/fixtures/aec_mepfs_backbone/admitted_backbone_nodes_l1_l2.json`.
- Input collections: `records` for nodes and `relationships` for existing edges.
- Duplicate edge key: `from_id--predicate--to_id`.
- Output must be pending-only, never `steward_admitted`.
- Default models: `qwen3-embedding:0.6b`, `qwen3.5:9b`, `deepseek-r1:8b-0528-qwen3-q4_K_M`.
- Existing AEC state remains file-backed; production Neo4j/live graph promotion is blocked.

## Constraints
- Do not mutate active graph files or the AEC fixture.
- Do not write to Neo4j or Postgres.
- Do not use internet access in v1.
- Do not run Ollama calls in parallel.
- Do not materialize all node pairs in memory.
- Do not emit blocked predicates: `affects`, `connected_to`, `related_to`, `similar_to`.
- `--apply` must reject with a clear safety error.

## Unknowns / Open Questions
- Whether `qwen3-embedding:0.6b` is installed and compatible with Ollama `/api/embed` on the user's machine.
- Whether a later steward workflow should promote candidates; v1 intentionally avoids promotion.

## Likely Codebase Touchpoints
- `scripts/vitruvius/kg/aec_relationship_improvement.py`
- `scripts/pipeline_cli.py`
- `scripts/tests/test_kg_aec_relationship_improvement.py`
- Existing validation references: `scripts/vitruvius/kg/backbone_graph_quality.py`, `scripts/vitruvius/kg/backbone_shadow_staging.py`
