---
task: vitruvius-audit-pass-1
phase: 05
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# 2026-04-16 Master Audit Implementation Plan

## 1. Executive Summary
PASS 2 should be a bounded stabilization sprint, not a feature sprint. The repo’s core tested runtime is healthier than several docs claim, but graph/query trust, state truthfulness, and advanced-boundary claim accuracy are not yet stable enough for safe new feature work.

## 2. Audit Sources Used
- `2026-04-16_master-codebase-audit.md`
- `2026-04-16_backend-and-api-audit.md`
- `2026-04-16_routes-crud-and-admin-audit.md`
- `2026-04-16_test-validation-and-quality-audit.md`
- `2026-04-16_performance-stability-and-loading-audit.md`
- `2026-04-16_docs-vs-code-reality-audit.md`
- `2026-04-16_architecture-and-boundary-audit.md`
- PASS 1 baseline/research artifacts

## 3. System Risk Overview
- Highest risk is truth drift, not broad runtime breakage.
- Graph/query trust is currently weaker than the CLI/doc surface implies.
- Advanced architecture claims need wiring proof or downgrade.
- Rust hygiene debt is real but secondary to truth and identity safety.

## 4. Fix Priorities by Severity
1. `CRITICAL/HIGH`: reconcile runtime truth sources and graph identity/provenance defects
2. `HIGH`: align advanced-boundary docs/flags with actual runtime wiring
3. `MEDIUM`: restore green Rust static gates
4. `MEDIUM`: harden operator footguns and manifest-state hygiene
5. `LOW`: comment/default cleanup and documentation polish

## 5. Dependency Order of Fixes
1. Freeze live truth source: branch, commit, test counts, active state, path references
2. Fix canonical identity and graph integrity checks
3. Fix query provenance and confidence semantics
4. Reconcile advanced feature claims/flags with real runtime callers
5. Clean Rust static gates
6. Clean operator footguns and manifest/report hygiene
7. Re-run full validation and update state docs/logs

## 6. Bundled Fix Groups
### Group A — Truth Reconciliation
- `AGENTS.md` path references
- `current-phase.md`
- `active_context.md`
- `master-roadmap.md`
- `principles.md`
- README validation-count sections

### Group B — Graph Identity and Query Trust
- duplicate canonical source IDs
- graph integrity duplicate-node detection
- query citation construction
- query confidence semantics

### Group C — Boundary Truthfulness
- stateful registry wiring claim
- neuro-symbolic Datalog claim
- RocksDB “vault” claim
- ghost flags (`gt_engine_rs`, `n_spatial_daemon_enabled`)
- Phase 1B parallelism wording

### Group D — Validation Hygiene
- Rust fmt/clippy failures
- unsafe helper probe scripts
- operator-facing CLI mutation caveats

## 7. Validation Requirements per Fix Group
- Group A: re-run branch/commit/test baseline and verify every updated doc matches
- Group B: re-run `build-graph`, inspect snapshot, rerun `query`, `query-structured`, `query-graph`
- Group C: prove each kept claim with a runtime caller or downgrade/remove the claim
- Group D: re-run Rust fmt/clippy/tests, plus probe-script safety checks

## 8. Regression Risks
- Over-correcting docs without proving runtime behaviour will create a new drift cycle
- Fixing canonical IDs can affect graph/query outputs and downstream tests
- Query provenance changes may break snapshot/query test fixtures
- Rust hygiene cleanup can accidentally change exported signatures if not kept narrow

## 9. Stop Conditions
- Any proposed fix assumes operator intent for raw-layer drift without evidence
- Any graph identity fix changes canonical IDs without a migration decision
- Any advanced-boundary claim is kept without a demonstrated runtime caller
- Any PASS 2 patch broadens into new AEC/browser feature work

## 10. Rollback / Safety Notes
- Keep changes narrow and grouped by fix bundle
- Rebuild graph snapshot after graph/query fixes, but do not hand-edit generated files
- Preserve fallback codepaths when downgrading feature claims
- Avoid corpus edits unless a dedicated migration or curation decision is made

## 11. Step-by-Step Execution Checklist
1. Re-baseline branch, commit, and full validation counts.
2. Repair path-reference/state-doc conflicts.
3. Remove or mark stale runtime-health statements.
4. Resolve duplicate canonical source identity and add duplicate-node integrity checks.
5. Update query layer to emit real evidence provenance from relationship records.
6. Revalidate graph/query behaviour with targeted commands and tests.
7. Audit advanced flags/claims one by one; wire or downgrade each.
8. Fix Rust fmt/clippy failures without widening scope.
9. Harden helper scripts and document CLI mutation surfaces.
10. Re-run full Python, TypeScript, Rust, and CLI validation.
11. Write PASS 2 validation logs and reconcile state docs.

## 12. Plan Critique
- Overreach risk: implementing “future AEC/browser” work to make docs true would be the wrong move. PASS 2 must downgrade unsupported claims rather than building missing futures.
- Hidden dependency risk: duplicate canonical source IDs should be resolved before query provenance work, or query fixes may encode bad identity assumptions.
- Sequencing risk: Rust hygiene must not happen first. It is real, but it does not unblock truth or graph safety.
- Bundling risk: combining all doc updates with all graph/query fixes in one patch would make blame and rollback poor. Use separate fix groups.
- Evidence-strength caveat: raw-layer manifest drift may reflect intentional corpus churn, not code failure. PASS 2 should treat it as a truth/state reconciliation task, not automatically a bug.

## 13. Refinements After Critique
- PASS 2 should start with Group A and Group B only; Group C and D follow after truth and identity are stable.
- Manifest drift stays observational unless operator intent says it is incorrect.
- Browser/dashboard/frontend language should be clarified, not implemented.
- Query-layer fixes must prove provenance from relationship evidence, not just improve wording.
