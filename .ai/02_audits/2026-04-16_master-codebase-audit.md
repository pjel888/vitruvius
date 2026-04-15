---
task: vitruvius-audit-pass-1
phase: 04
created: 2026-04-16
author: AUDITOR
supersedes: null
status: ACCEPTED
---

# 2026-04-16 Master Codebase Audit

## Purpose
Establish the true current operating state of the Vitruvius repo and decide whether it is stable enough for new feature work.

## Scope
- Governance/state truthfulness
- CLI/runtime health
- Graph/query path integrity
- Cross-language boundaries
- Test and validation infrastructure

## What Was Inspected
- Root governance stack under `.ai/`
- `README.md`
- `scripts/pipeline_cli.py`
- `scripts/vitruvius/**`
- `scripts/tests/**`
- `spatial-daemon/**`
- Canonical source / relationship files under `003_Canonical-Knowledge-Layer/shared/`

## What Was Tested
- `npx gitnexus status`
- `npx gitnexus analyze`
- `pytest scripts/tests -q`
- `npm test`
- `npm run typecheck`
- `npm run build`
- `cargo test --quiet` in both Rust roots
- `cargo fmt --all --check` and `cargo clippy --workspace --all-targets -- -D warnings` in both Rust roots
- `python3 scripts/pipeline_cli.py run`
- `python3 scripts/pipeline_cli.py build-graph`
- `python3 scripts/pipeline_cli.py query-structured --function neighbors --subject concept-occupancy-classification`
- `python3 scripts/pipeline_cli.py query "What governs occupancy classification?"`
- `python3 scripts/pipeline_cli.py export-graph-owl`

## What Works
- Python test suite is green: `1566 passed, 1 skipped`.
- `spatial-daemon/` test, typecheck, and build paths are green.
- Rust runtime/unit tests pass in both Rust roots.
- Core CLI surfaces load and run.
- Graph build and OWL export execute successfully.

## What Fails
- Rust strict static gates fail (`fmt --check`, `clippy -D warnings`).
- Graph integrity does not detect duplicate canonical source IDs.
- Query CLI emits placeholder citations with no evidence snippets or section IDs.
- Live state docs contradict each other on branch, counts, and current truth.

## What Is Misleading
- Repo-level docs overstate some advanced paths as live runtime behaviour when they are infrastructure, scaffold, or test-only.
- “Frontend/routes/admin” language does not match the actual headless CLI shape.
- Older audit/state files still describe runtime instability that is no longer true on the current checkout.

## Severity-Ranked Findings
- `HIGH` Fresh runtime truth is not centralized. `current-phase.md`, `active_context.md`, `master-roadmap.md`, `principles.md`, and README disagree on branch and validation counts.
- `HIGH` Graph/query trust is weaker than the CLI suggests. The graph snapshot includes duplicate source-node IDs and the integrity checker still passes.
- `HIGH` Query citations are synthetic, not evidence-backed. `scripts/vitruvius/query/engine.py` builds citations from edge metadata only, with empty `source_section_id` and empty `evidence_snippet`.
- `MEDIUM` Advanced architecture claims (stateful registry, neuro-symbolic Datalog, RocksDB “vault”, Wasm loader, ProcessPool orchestration) are unevenly wired and oversold in docs.
- `MEDIUM` Strict Rust hygiene is red even though runtime tests are green.
- `LOW` Operator-facing helper scripts are unsafe for read-only probing; `scripts/test_odl_one.py --help` executes a real conversion.

## Reproduction Steps
1. Run `pytest scripts/tests -q`.
2. Run `python3 scripts/pipeline_cli.py build-graph`.
3. Inspect `005_Operational-Intelligence-Layer/graph/latest_graph_snapshot.json` for duplicate node IDs.
4. Run `python3 scripts/pipeline_cli.py query-structured --function neighbors --subject concept-occupancy-classification`.
5. Run `cargo clippy --workspace --all-targets -- -D warnings` under both Rust roots.
6. Compare `.ai/01_roadmap/current-phase.md` with `.ai/10_state/active_context.md`.

## Suspected Root Causes
- Rapid governance/doc churn without a single refreshed runtime-health source.
- Graph integrity rules focus on edges and dangling references, not duplicate node IDs.
- Query layer is reading graph topology, not provenance-bearing relationship evidence.
- Feature-flag and architecture documentation were updated faster than end-to-end runtime wiring.

## Recommended Fix Direction
- Reconcile and freeze one live runtime truth source first.
- Fix canonical identity/integrity in the graph path before adding new graph/query features.
- Downgrade or wire advanced architecture claims so docs match runtime reality.
- Restore green Rust hygiene gates.

## Validation Needed After Fix
- Re-run full Python, TypeScript, and Rust test matrices.
- Rebuild the graph and verify duplicate-node detection.
- Re-run query commands and confirm real evidence snippets/section IDs appear.
- Reconcile state docs and confirm all validation counts match the live repo.

## Audit Verdict
Vitruvius is not broadly broken. It is operationally usable on its tested CLI surfaces. It is not truthful enough or graph-safe enough to call “stable for new feature work” without a focused stabilization pass first.
