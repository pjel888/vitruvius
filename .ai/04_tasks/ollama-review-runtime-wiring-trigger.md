---
task: ollama-review-runtime-wiring
phase: "00"
created: 2026-04-21
author: PLANNER
supersedes: null
status: ACCEPTED
---

# Trigger — Ollama Review Runtime Wiring

## Task Statement

Bound and implement the safest runtime wiring change needed to connect the shipped `ollama_review.py` helper infrastructure to the live review loop without broadening scope beyond the current Tier-1 relationship review path.

## In Scope

- `scripts/vitruvius/ollama_review.py`
- `scripts/pipeline_cli.py`
- `scripts/vitruvius/dataset_pipeline.py`
- directly related tests under `scripts/tests/` that prove review-loop behavior
- `.ai/02_audits/` and `.ai/03_plans/` artifacts for this task
- `.ai/10_state/active_context.md`

## Out of Scope

- second-pass review redesign in `ollama_review_second_pass.py`
- new model families, cloud LLM integrations, or prompt redesign
- broad review-layer architecture cleanup outside the live Tier-1 loop
- unrelated docs/system cleanup already completed in the control-surface lane

## Identity-Locked File Check

- PASS
- No identity-locked file is currently targeted by this lane.

## Risk Class

- **L**
- Reason: touches a core review runtime module and CLI-connected behavior with high blast radius in graph analysis, but does not currently propose schema or feature-flag contract changes.

## Roles

- **PLANNER:** Hephaestus
- **AUDITOR:** pending critique phase
- **IMPLEMENTER:** Hephaestus
- **REVIEWER:** pending validation phase
- **STEWARD:** Hephaestus

## Linked Prior Artifacts

- `.ai/00_system/EXECUTION_LOOP.md`
- `.ai/00_system/pipeline-overview.md`
- `.ai/02_audits/2026-04-16_architecture-and-boundary-audit.md`
- `.ai/05_logs/2026-04-21_control-surface-consolidation-validation.md`
- `.ai/10_state/active_context.md`

## Initial Evidence

- `pipeline-overview.md` explicitly says `review_with_cache()` is shipped infrastructure but not yet the default live review loop.
- `decisions.md` records `review_with_cache()` and `select_review_model()` as flag-gated shipped hooks rather than guaranteed live-default runtime paths.
- code graph minimal context reports low graph-summary risk for planning, but impact-radius on the likely runtime files is **high**, so the implementation must stay narrow and validation-heavy.

## MCP Precheck

- `code-review-graph_get_minimal_context_tool(task="Plan bounded implementation for ollama_review runtime wiring...")`
- `code-review-graph_get_impact_radius_tool(changed_files=["scripts/vitruvius/ollama_review.py", "scripts/pipeline_cli.py", "scripts/vitruvius/dataset_pipeline.py"], max_depth=2, detail_level="minimal")`
- pending explore-agent evidence for exact live call sites and narrow validation order

## Gate Status

- No prior task artifact for `ollama-review-runtime-wiring` exists.
- This trigger is now the canonical task boundary for the next audit/plan packet.
