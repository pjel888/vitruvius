---
task: duplicate-canonical-source-id-remediation
phase: 09
created: 2026-04-16
author: REVIEWER
supersedes: null
status: ACCEPTED
---

# 2026-04-16 Duplicate Canonical Source ID Remediation Validation

## What was fixed
- Removed the duplicate live canonical IRR source page `003_Canonical-Knowledge-Layer/shared/sources/pd-1096-irr.md`.
- Retained the pipeline-backed live page `003_Canonical-Knowledge-Layer/shared/sources/implementing-rules-and-regulations-of-the-national-building-code.md` with the same canonical ID `irr-implementing-rules-and-regulations-of-the-national-building-code`.
- Folded the richer lineage/content from the removed duplicate page into the retained page so no source-lineage scope was lost.
- Refreshed the live/generated artifacts that still mentioned `pd-1096-irr.md`:
  - `006_System-Manifests/runs/latest_migrate_ids_plan.*`
  - `006_System-Manifests/runs/latest_migrate_ids_apply.*`
  - `005_Operational-Intelligence-Layer/graph/latest_graph_snapshot.ttl`

## What was re-tested
- `python3 scripts/pipeline_cli.py build-graph`
- `PYTHONPATH=scripts pytest scripts/tests -q`
- `PYTHONPATH=scripts pytest -q scripts/tests/test_graph_integrity.py scripts/tests/test_graph_builder.py scripts/tests/test_query_engine.py scripts/tests/test_query_cli.py scripts/tests/test_query_seed_accuracy.py`
- `cd spatial-daemon && npm test`
- `cd spatial-daemon && npm run typecheck`
- `cd spatial-daemon && npm run build`
- `cd scripts/vitruvius/engine_rs && cargo fmt --all --check`
- `cd scripts/vitruvius/engine_rs && cargo clippy --workspace --all-targets -- -D warnings`
- `cd scripts/vitruvius/engine_rs && cargo test --quiet`
- `cd scripts/vitruvius/datalog_rs && cargo fmt --all --check`
- `cd scripts/vitruvius/datalog_rs && cargo clippy --workspace --all-targets -- -D warnings`
- `cd scripts/vitruvius/datalog_rs && cargo test --quiet`
- `python3 scripts/pipeline_cli.py query-structured --function what_governs --subject concept-means-of-egress`
- `python3 scripts/pipeline_cli.py query "What governs means of egress?"`
- repo-wide search for remaining live/generated references: `rg -n "pd-1096-irr\\.md|pd-1096-irr" .`

## What now works
- `build-graph` no longer fails on `duplicate_node_id` for the IRR source.
- Query outputs remain stable because the canonical ID was preserved.
- The retained IRR page now carries the richer multi-artifact lineage that had only existed on the removed duplicate page.

## What still warns
- `build-graph` still reports six orphan-node warnings, but `error_count` is now `0` and `passed` is `true`.

## Validation Results
- `python3 scripts/pipeline_cli.py build-graph` → PASS (`passed: true`, `error_count: 0`, `warning_count: 6`)
- `PYTHONPATH=scripts pytest scripts/tests -q` → PASS (`1572 passed, 1 skipped`)
- Targeted graph/query pytest selection → PASS (`50 passed`)
- `spatial-daemon` test/typecheck/build → PASS (`21 passed`, `tsc --noEmit`, `tsc`)
- Rust fmt/clippy/tests in both roots → PASS
- `query-structured` / `query` for `concept-means-of-egress` → PASS with real evidence provenance and unchanged canonical answer ID
- Architect verification → PASS (`APPROVED`: smallest safe truth-preserving fix, no hidden migration blocker found)
- Deslop/noise check on session-owned files → PASS (`git diff --check` clean after removing trailing whitespace in `.ai/10_state/active_context.md`)
- live/generated reference cleanup → PASS (`rg -n "pd-1096-irr\\.md|pd-1096-irr" .` returned no residual live/generated refs after artifact refresh)

## Result
The underlying duplicate canonical source ID issue is resolved.
