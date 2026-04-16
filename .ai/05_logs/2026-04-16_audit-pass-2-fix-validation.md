---
task: vitruvius-audit-pass-2
phase: 09
created: 2026-04-16
author: REVIEWER
supersedes: null
status: ACCEPTED
---

# 2026-04-16 Audit Pass 2 Fix Validation

## What was fixed
- Reconciled live truth/state docs to the active 2026-04-16 stabilization reality:
  - `.ai/10_state/active_context.md`
  - `.ai/01_roadmap/current-phase.md`
  - `.ai/01_roadmap/milestone-tracker.md`
  - `.ai/00_system/principles.md`
  - `.ai/01_roadmap/master-roadmap.md`
  - `README.md`
- Hardened graph/query trust in code:
  - duplicate graph node IDs now fail integrity via `scripts/vitruvius/graph/integrity.py`
  - relationship evidence is carried into the snapshot via `scripts/vitruvius/graph/builder.py` + `graph/contract.py` + `graph/snapshot.py`
  - query citations now use real `source_section_id` / `evidence_snippet` / reviewer confidence when present via `scripts/vitruvius/query/engine.py`
- Restored strict Rust static gates:
  - fmt clean in `engine_rs` and `datalog_rs`
  - clippy `-D warnings` clean in `engine_rs` and `datalog_rs`
  - runtime Rust tests still green
- Reconciled overstated boundary/runtime wording:
  - `ProcessPoolExecutor` claim downgraded to the shipped sequential `process_batch(..., max_workers=...)` compatibility API
  - stateful registry wording downgraded from “live default loop” to shipped infrastructure / follow-on wiring
  - Datalog / Wasm/browser wording downgraded to experimental or historical where proof was not present
- Updated the master implementation plan with PASS 2 execution status.

## What was attempted but deferred
- The underlying duplicate canonical source ID collision (`irr-implementing-rules-and-regulations-of-the-national-building-code`) was **not** mutated in PASS 2.
- Reason for deferral: changing canonical IDs or deleting one duplicate source page would be a truth-governance / migration decision, and the PASS 2 stop conditions explicitly forbid guessing through that boundary.
- PASS 2 instead made the defect loud and blocking in graph integrity.

## What was re-tested
- `PYTHONPATH=scripts pytest scripts/tests -q`
- `PYTHONPATH=scripts pytest -q scripts/tests/test_graph_integrity.py scripts/tests/test_graph_builder.py scripts/tests/test_query_engine.py scripts/tests/test_query_formatter.py scripts/tests/test_query_cli.py`
- `PYTHONPATH=scripts pytest -q scripts/tests/test_3d_upgrade_backcompat.py scripts/tests/test_wiring_backcompat.py scripts/tests/test_query_aggregate_confidence.py scripts/tests/test_query_seed_accuracy.py`
- `cd spatial-daemon && npm test`
- `cd spatial-daemon && npm run typecheck`
- `cd spatial-daemon && npm run build`
- `cd scripts/vitruvius/engine_rs && cargo fmt --all --check`
- `cd scripts/vitruvius/engine_rs && cargo clippy --workspace --all-targets -- -D warnings`
- `cd scripts/vitruvius/engine_rs && cargo test --quiet`
- `cd scripts/vitruvius/datalog_rs && cargo fmt --all --check`
- `cd scripts/vitruvius/datalog_rs && cargo clippy --workspace --all-targets -- -D warnings`
- `cd scripts/vitruvius/datalog_rs && cargo test --quiet`
- `python3 scripts/pipeline_cli.py run`
- `python3 scripts/pipeline_cli.py build-graph` (expected to fail on duplicate-node integrity)
- `python3 scripts/pipeline_cli.py query-structured --function what_governs --subject concept-means-of-egress`
- `python3 scripts/pipeline_cli.py query "What governs means of egress?"`
- `python3 scripts/pipeline_cli.py query-graph --from irr-implementing-rules-and-regulations-of-the-national-building-code --to concept-means-of-egress`

## What now works
- Python suite is green at **1569 passed, 1 skipped**.
- `spatial-daemon` test/typecheck/build are green at **21 tests passed**.
- Rust unit tests are green at **33 total passing**, and both Rust roots now pass fmt + clippy.
- `pipeline_cli.py run` is clean on the current raw corpus baseline (`350` files, `0` new, `0` changed, `0` missing).
- `query` / `query-structured` now emit real supporting evidence when the relationship file contains evidence metadata.
- `query-graph` now exposes evidence-bearing edge metadata in the returned path payload.
- `build-graph` no longer passes silently with duplicate canonical source IDs; it returns a failing integrity report with `duplicate_node_id`.
- Repo state docs now point at the live branch (`main`) and current validation reality instead of the stale feature-branch snapshot.

## What still fails
- `python3 scripts/pipeline_cli.py build-graph` still exits non-zero because the canonical source layer currently contains two source pages with the same ID `irr-implementing-rules-and-regulations-of-the-national-building-code`.
- This is now an intentional blocking integrity failure rather than a silent false-green.

## Remaining risks
- Canonical identity remediation still needs an explicit migration/curation decision.
- Some advanced capabilities remain shipped as infrastructure/scaffolding rather than audited live runtime paths; docs now reflect that more honestly, but operator expectations still need discipline.
- PASS 2 attempted an OMX `$team` run first; the team runtime misassigned all tasks to worker-1, stalled, and required manual cleanup. No worker worktree changes were preserved. This is an operational caveat of the execution method, not a product-code health claim.

## Final readiness before new feature work
- The repo is materially safer and more truthful than it was at PASS 1 handoff.
- Truth/state drift is reduced.
- Query provenance is now evidence-backed instead of placeholder-backed.
- Rust hygiene debt is cleared.
- The main blocking caveat before new feature work is the still-unresolved duplicate canonical source ID, which now surfaces as an explicit integrity error instead of hiding behind a passing report.

## Final Verdict
**STABILIZATION PASS COMPLETE WITH CAVEATS**
