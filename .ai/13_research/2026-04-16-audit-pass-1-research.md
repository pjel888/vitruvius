---
task: vitruvius-audit-pass-1
phase: 03
created: 2026-04-16
author: PLANNER
supersedes: null
status: ACCEPTED
---

# 01 — Discover

## Governance Files Read
- `AGENTS.md`
- `.ai/00_system/EXECUTION_LOOP.md`
- `.ai/00_system/principles.md`
- `.ai/00_system/architecture.md`
- `.ai/00_system/pipeline-overview.md`
- `.ai/01_roadmap/master-roadmap.md`
- `.ai/01_roadmap/current-phase.md`
- `.ai/01_roadmap/milestone-tracker.md`
- `.ai/03_plans/00-governing-implementation-plan.md`
- `.ai/03_plans/INDEX.md`
- `.ai/10_state/active_context.md`
- `.ai/10_state/decisions.md`
- `.ai/10_state/known_issues.md`
- `.ai/06_specs/source-schema.md`
- `.ai/06_specs/concept-schema.md`
- `.ai/06_specs/relationship-schema.md`
- `.ai/06_specs/spatial-schema.md`

## Existing Audits / Plans Consulted
- `.ai/02_audits/APP_INTEGRITY_RELIABILITY_AUDIT_2026-04-16.md`
- `.ai/02_audits/WHOLE_CODEBASE_PLAN_LAYER_AUDIT_2026-04-16.md`
- `.ai/02_audits/extraction-audit.md`
- `.ai/02_audits/ingestion-audit.md`
- `.ai/02_audits/normalization-audit.md`
- `.ai/02_audits/review-layer-audit.md`
- `.ai/03_plans/2026-04-16-app-integrity-reliability-plan.md`
- `.ai/03_plans/2026-04-16-whole-codebase-plans-upgrade-plan.md`

## Structure-Aware Exploration Notes
- `code-review-graph` MCP tools were unavailable in-session.
- GitNexus CLI was available:
  - `npx gitnexus status` initially reported a stale index.
  - `npx gitnexus analyze` refreshed the repo index successfully.
  - Analyzer emitted repeated `MaxListenersExceededWarning` warnings during indexing.

## Repo Shape Observed
- Python-first CLI/pipeline under `scripts/` and `scripts/vitruvius/`
- TypeScript sibling CLI under `spatial-daemon/`
- Rust under `scripts/vitruvius/engine_rs/` and `scripts/vitruvius/datalog_rs/`
- No web frontend, HTTP server, admin panel, or dashboard code root present

## Critical Early Contradictions
1. User prompt referenced `.ai/10_state/current-phase.md` and `.ai/10_state/milestone-tracker.md`; repo authority uses `.ai/01_roadmap/*`.
2. `current-phase.md` says `main` / between sprints; `active_context.md` still claims `feat/sprint-r-per-layer-embeddings`.
3. Runtime validation counts in `principles.md`, `master-roadmap.md`, `active_context.md`, and README do not agree with fresh test execution.

## Targeted Verification Surfaces Chosen
- Full Python suite: `pytest scripts/tests -q`
- Spatial daemon: `npm test`, `npm run typecheck`, `npm run build`
- Rust runtime: `cargo test --quiet`
- Rust hygiene: `cargo fmt --all --check`, `cargo clippy --workspace --all-targets -- -D warnings`
- CLI/operator paths:
  - `pipeline_cli.py run`
  - `pipeline_cli.py build-graph`
  - `pipeline_cli.py query-structured`
  - `pipeline_cli.py query`
  - `pipeline_cli.py export-graph-owl`

## High-Signal Findings Before Audit Synthesis
- Core tested codepaths are healthier than some state docs claim.
- Graph/query surfaces are live but evidence fidelity is weak.
- Canonical source identity is duplicated in the graph snapshot and not caught by integrity checks.
- Several advanced architecture claims are partially implemented or test-only rather than clearly wired into default runtime paths.
