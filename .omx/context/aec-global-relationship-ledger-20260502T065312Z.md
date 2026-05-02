---
task: aec-global-relationship-ledger
created: 2026-05-02
status: active
---

# AEC Global Relationship Ledger Context

## Task
Add a cross-run processed-pair ledger for the pending-only AEC relationship-improvement workflow so separate run IDs do not repeat DeepSeek/Ollama judgment calls for already processed node pairs.

## Constraints
- Pending artifacts only; no active graph mutation.
- No Neo4j/Postgres writes.
- No internet lookup or model tools.
- Cloud calls remain opt-in and must not happen for ledger-skipped pairs.
- Ledger must be append-only JSONL under `006_System-Manifests/aec-mepfs-backbone/semantic-overlays/`.
- API keys, reasoning content, full embeddings, and active graph fixture content must not be modified or exposed.

## Touchpoints
- `scripts/vitruvius/kg/aec_relationship_improvement.py`
- `scripts/pipeline_cli.py`
- `scripts/tests/test_kg_aec_relationship_improvement.py`
- validation evidence under `.ai/05_logs/`

## Acceptance
- CLI parser accepts the new ledger flags.
- First run appends one ledger row per processed pair.
- Second run with a different run ID and same pair skips before judge calls.
- `skipped_global_ledger` appears in checkpoint/report/summary.
- `--ignore-global-ledger` and decision filters work.
- Targeted AEC tests, graph quality tests, and py_compile pass.
