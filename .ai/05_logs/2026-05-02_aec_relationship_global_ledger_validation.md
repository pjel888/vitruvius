---
task: aec-relationship-global-ledger
phase: 09
created: 2026-05-02
author: REVIEWER
status: CLOSED
---

# AEC Relationship Campaign Ledger Validation

## Scope
Implemented and then revised the stable append-only processed-pair ledger for the pending-only AEC relationship-improvement workflow so large campaigns use isolated run-specific ledger files by default.

## Safety Confirmation
- Active graph fixture was not modified.
- No Neo4j or Postgres code path was introduced.
- Ledger writes are JSONL artifacts under `006_System-Manifests/aec-mepfs-backbone/semantic-overlays/`.
- Default ledger writes now resolve to `semantic-overlays/{run_id}-ledger.jsonl`; cross-run reuse requires an explicit `--global-ledger-path`.
- Ledger skips happen before judge prompt/model calls and do not admit or mutate graph edges.
- Ledger records are sanitized by the existing JSONL writer and include no API keys, reasoning content, or embeddings.
- Ledger reuse is gated by embedding model, node text hashes, and threshold fingerprints unless the operator explicitly passes `--force-ledger-reuse`.

## Verification
- `python -m py_compile scripts/vitruvius/kg/aec_relationship_improvement.py scripts/pipeline_cli.py` passed.
- `$env:PYTHONPATH='scripts'; python -m pytest scripts/tests/test_kg_aec_relationship_improvement.py -q` passed: 111 passed.
- `$env:PYTHONPATH='scripts'; python -m pytest scripts/tests/test_kg_backbone_shadow_staging.py scripts/tests/test_kg_backbone_graph_quality.py -q` passed: 18 passed.
- No-model smoke passed with `--run-id debug_campaign_ledger_smoke --max-nodes 0 --max-pairs 0`; the workflow created `debug_campaign_ledger_smoke-ledger.jsonl` next to the run directory. The smoke artifacts were removed after verification.
- Pre-edit and post-edit `./scripts/refresh_code_intelligence.sh` completed. code-review-graph still reports YAML parser warnings and embedding-service errors during index refresh; these were observed before this change and did not block the Python test evidence.
- `uvx --with tree-sitter-yaml code-review-graph detect-changes --repo .` reported risk score 0.00.
- `npx.cmd --yes gitnexus@1.6.4-rc.32 detect-changes --repo vitruvius` reported CRITICAL on the dirty worktree after this pass. The command included unrelated pre-existing state/research changes and broad generated-symbol noise; scoped AEC relationship workflow impact checks before edit were LOW, and `code-review-graph detect-changes` reported risk score 0.00.

## Test Coverage Added
- Automatic ledger path creation is campaign-specific: different run IDs get different `{run_id}-ledger.jsonl` files and do not contaminate each other.
- A second run with the same explicit manual ledger path skips a prior judged pair without calling the judge.
- Ledger records include `accept_threshold`, `verify_threshold`, and `candidate_top_k`.
- Threshold mismatches warn and prevent reuse by default.
- `--force-ledger-reuse` allows intentional reuse across threshold mismatches.
- `--ignore-global-ledger` allows rejudging.
- `--global-ledger-decision-filter` controls which prior statuses suppress calls.
- Different embedding model does not match the ledger.
- CLI parser accepts the campaign/global ledger flags, including `--force-ledger-reuse`.
- Checkpoint/report/summary expose `skipped_global_ledger_count`, new model call count, existing ledger pair count, threshold-match state, and saved-cost estimate.

## Known Caveats
- The generator still applies `max_pairs` before ledger skipping, so a run whose first `max_pairs` candidates are all already in the ledger will finish with skips rather than searching beyond that cap for additional fresh pairs. This preserves the current candidate-generation cap semantics.
