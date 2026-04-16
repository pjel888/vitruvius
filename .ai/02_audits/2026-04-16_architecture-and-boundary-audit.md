---
task: vitruvius-audit-pass-1
phase: 04
created: 2026-04-16
author: AUDITOR
supersedes: null
status: ACCEPTED
---

# 2026-04-16 Architecture and Boundary Audit

## Purpose
Verify the real Python/Rust/TypeScript/Wasm/RocksDB/Z3 boundaries and expose where docs overstate runtime wiring.

## Scope
- `scripts/vitruvius/**`
- `spatial-daemon/**`
- `config/vitruvius.yaml`
- boundary-related governance docs

## What Was Inspected
- `spatial-daemon/README.md`
- `spatial-daemon/src/cli.ts`
- `scripts/vitruvius/ollama_review.py`
- `scripts/vitruvius/review/stateful_registry.py`
- `scripts/vitruvius/graph/event_store.py`
- `scripts/vitruvius/parsers/factory.py`
- `scripts/vitruvius/parsers/orchestrator.py`
- `config/vitruvius.yaml`

## What Was Tested
- TypeScript daemon test/typecheck/build
- Rust runtime tests
- Direct code-path inspection for flag consumers and runtime callers

## What Works
- Python is the real control plane.
- TypeScript spatial daemon is cleanly isolated by file contract.
- Rust crates compile and pass unit/runtime tests.
- Z3 and spatial CLI boundaries are explicit and gated.

## What Fails
- Several advanced boundaries are partially implemented but not clearly wired into default runtime flows.
- Some feature flags are declared and documented without real runtime consumers.
- Process-pool orchestration is documented as shipped while the implementation is still sequential.

## What Is Misleading
- Docs blur “backend exists in tree” with “feature is live in the runtime path.”
- Comments in code still describe old flag defaults after default flips.

## Severity-Ranked Findings
- `HIGH` Stateful review cache boundary is present as infrastructure but not clearly wired into the live review loop. `_call_llm()` in `ollama_review.py:113-125` is still `NotImplementedError` for the cache wrapper path, while `y_stateful_registry` remains default-off.
- `HIGH` Neuro-symbolic Datalog is overstated. The Rust crate exists, but PASS 1 found no clear runtime caller for `evaluate_datalog` outside tests; current docs read like enforcement, not scaffolding.
- `MEDIUM` RocksDB “immutable vault” language overstates runtime centrality. Factories and backends exist, but PASS 1 found benchmark/migration usage more clearly than live pipeline reliance.
- `MEDIUM` `gt_engine_rs` and `n_spatial_daemon_enabled` read like ghost flags: declared and documented, but not obviously consumed in live Python runtime paths.
- `MEDIUM` Phase 1B parallelism is overstated. `process_batch()` is sequential despite milestone-tracker wording.
- `LOW` Several code comments still describe pre-flip defaults for RocksDB and Rust migration flags.

## Reproduction Steps
1. Read `spatial-daemon/README.md:8-12` and `spatial-daemon/src/cli.ts:81-91`.
2. Read `scripts/vitruvius/ollama_review.py:113-180`.
3. Read `scripts/vitruvius/review/stateful_registry.py:190-215`.
4. Read `scripts/vitruvius/parsers/factory.py:10-30`.
5. Read `scripts/vitruvius/parsers/orchestrator.py:159-192`.

## Suspected Root Causes
- Architecture documents were refreshed aggressively after sprint bursts, but runtime wiring and operator defaults were not uniformly re-audited.
- Feature flags accumulated faster than consumer-path audits.
- “Shipped” in docs sometimes meant “implemented in-tree and tested” rather than “default-path runtime active.”

## Recommended Fix Direction
- Audit every advanced boundary claim against a real runtime caller.
- Remove or relabel ghost flags.
- Align milestone and README wording with actual live wiring state.
- Close the review-cache and neuro-symbolic truth gap either by wiring them or downgrading the claim.

## Validation Needed After Fix
- For each advanced boundary claim, name the runtime caller and rerun a proving command/test.
- Re-run full validation after any flag/default or boundary-wiring changes.

## Audit Verdict
Boundary separation is conceptually sound, but runtime truthfulness around advanced boundaries is uneven and needs stabilization.

## PASS 2 Note — 2026-04-16
- The overstated `ProcessPoolExecutor` claim was downgraded to the shipped sequential `process_batch(..., max_workers=...)` compatibility API.
- Stateful-registry and neuro-symbolic Datalog docs were downgraded from “live default path” wording to infrastructure / experimental wording where audited runtime proof was absent.
