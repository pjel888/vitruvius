# Active Context — Vitruvius

> **Updated:** 2026-04-16
> **Live branch:** `main`
> **Most recent completed work:** PASS 2 stabilization plus duplicate canonical source ID remediation (`.ai/09_archive/plans/2026-04-16_master-audit-implementation-plan.md`, `.ai/09_archive/plans/2026-04-16_duplicate-canonical-source-id-remediation-plan.md`)

## Live Repo Truth

- PASS 1 produced the audit pack, master implementation plan, baseline, research, and validation artifacts for the 2026-04-16 stabilization lane.
- PASS 2 is stabilization-only. It is focused on:
  1. truth/state reconciliation
  2. graph identity + query provenance trust
  3. advanced-boundary claim cleanup
  4. Rust/static validation hygiene
- The 2026-04-15 sprint-wave summary remains historical context in `decisions.md` and `master-roadmap.md`; it is **not** the live dispatcher anymore.

## Current Validation Snapshot

- Python tests: **1572 passed, 1 skipped** (`PYTHONPATH=scripts pytest scripts/tests -q`)
- TypeScript tests: **21 passed** (`spatial-daemon`: `npm test`)
- Rust unit tests: **33 passed** total (`engine_rs` + `datalog_rs`)
- Rust static gates: **green** (`cargo fmt --all --check`, `cargo clippy --workspace --all-targets -- -D warnings`)
- Raw-layer pipeline baseline: `python3 scripts/pipeline_cli.py run` is clean on current corpus state (`350` files, `0` new, `0` changed, `0` missing)
- Graph integrity: `python3 scripts/pipeline_cli.py build-graph` now passes with warnings only; the duplicate canonical IRR source page was remediated in the follow-on fix pass
- Query provenance: `query` / `query-structured` now render real `source_section_id` + `evidence_snippet` when relationship evidence exists

## Residual Graph Caveat

- `build-graph` is now green on errors, but still reports six orphan-node warnings that remain informational rather than blocking.

## Reference Map

- Governing plan: `/.ai/03_plans/00-governing-implementation-plan.md`
- PASS 2 master plan (archived): `/.ai/09_archive/plans/2026-04-16_master-audit-implementation-plan.md`
- PASS 1 validation: `/.ai/05_logs/2026-04-16_audit-pass-1-validation.md`
- PASS 2 validation: `/.ai/05_logs/2026-04-16_audit-pass-2-fix-validation.md`
- Duplicate-ID remediation plan (archived): `/.ai/09_archive/plans/2026-04-16_duplicate-canonical-source-id-remediation-plan.md`
- Active roadmap snapshot: `/.ai/01_roadmap/current-phase.md`
- Milestones: `/.ai/01_roadmap/milestone-tracker.md`
- Decisions: `/.ai/10_state/decisions.md`

## Handoff Note

If you continue from here, do **not** restart with a new repo-wide audit. Consult the **archived** 2026-04-16 stabilization/remediation plans together with the PASS 2 validation log and the duplicate-ID remediation validation log.
