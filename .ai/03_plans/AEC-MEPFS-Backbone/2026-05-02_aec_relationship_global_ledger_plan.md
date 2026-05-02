---
task: aec-relationship-global-ledger
phase: 05-07
created: 2026-05-02
author: PLANNER
status: ACCEPTED
---

# AEC Relationship Campaign Ledger Plan

## Research Pack
- Current state remains AEC-MEPFS file-backed runtime with production/live graph writes blocked.
- The relationship-improvement workflow already writes only run artifacts under `006_System-Manifests/aec-mepfs-backbone/semantic-overlays/<run_id>/`.
- `append_jsonl()` flushes and fsyncs records; checkpoint/report atomic writes already exist.
- GitNexus impact before edit: LOW for `run_relationship_improvement`, `RunConfig`, `config_from_args`, and `pipeline_cli.build_parser`.
- Code-intelligence refresh completed before edit; YAML parser warnings and embedding-service errors are pre-existing index-refresh issues, not blockers for this Python-only change.

## Audit
- Risk: medium, because this changes model-call suppression, CLI flags, reports, checkpoints, and tests.
- Safety boundary: ledger is an operational artifact only; it must not mutate graph data or influence admitted relationships.
- Main failure mode: cross-campaign contamination from a shared ledger. Mitigation: when no explicit ledger path is supplied, the workflow resolves to `semantic-overlays/{run_id}-ledger.jsonl`.
- Secondary failure mode: false skip when node text, embedding model, or thresholds change. Mitigation: ledger records carry per-node text hashes, embedding model, and threshold fingerprints; skip reuse requires a match unless `--force-ledger-reuse` is set.
- Test-run pollution risk: tests now use temp output roots and the auto campaign ledger path unless a shared ledger is intentionally part of the test.

## Implementation Plan
1. Add ledger configuration fields and CLI flags with default enabled behavior.
2. Add ledger helpers for loading, matching by pair/model/text hashes, and append-only fsync writes.
3. Insert a pre-judge skip check in the candidate loop and count `skipped_global_ledger`.
4. Append a ledger record after each processed pair, including validation/error statuses where appropriate.
5. Surface `skipped_global_ledger_count` in checkpoint, report, summary text, and progress events.
6. Revise default ledger path resolution to a campaign-specific `{run_id}-ledger.jsonl` path.
7. Store `accept_threshold`, `verify_threshold`, and `candidate_top_k` in ledger records; warn and suppress mismatched reuse unless forced.
8. Surface startup ledger path, existing-pair count, threshold-match state, new model calls, and estimated cost saved by ledger reuse.
9. Add focused unit tests for parser wiring, campaign isolation, manual-ledger skip, threshold mismatch, forced reuse, ignore flag, filter behavior, and embedding-model mismatch.
10. Run targeted verification and record results.

## Plan Critique
- C001: A process-wide ledger can accumulate stale records across node text changes. Addressed by recording and checking `build_node_text()` SHA-256 values.
- C002: Shared default paths can pollute unrelated campaigns. Addressed by resolving the default ledger to the active run ID and requiring explicit `--global-ledger-path` for shared reuse.
- C003: A skipped pair should not consume model tokens. Addressed by placing the skip before prompt construction and council judging.
- C004: Threshold changes can make prior accept/reject decisions incomparable. Addressed by threshold fingerprint checks and `--force-ledger-reuse` for deliberate operator override.

## Execution Checklist
- [x] Add ledger path/default constants and dataclass fields.
- [x] Add JSONL load/match/append helpers.
- [x] Wire CLI flags in module and top-level pipeline parser.
- [x] Add candidate-loop skip before judge calls.
- [x] Append ledger records after processed outcomes.
- [x] Add checkpoint/report/summary counters.
- [x] Add tests for cross-run skip and flags.
- [x] Make automatic ledger paths campaign-specific by run ID.
- [x] Add threshold fingerprint storage and mismatch checks.
- [x] Add `--force-ledger-reuse`.
- [x] Add startup ledger status lines and saved-cost/new-call summary fields.
- [x] Run targeted tests, graph-quality tests, py_compile, refresh indexes, and detect changes.
