# .ai Audit Report (Repository Operations & Planning Reconciliation)

**Date:** 2026-04-21  
**Scope:** Entire `.ai/` tree, cross-checked against repository implementation artifacts  
**Method:** Structural inventory + evidence checks against code, config, tests, manifests, and generated run artifacts

## Executive Summary

The `.ai/` layer is rich but overgrown: it contains strong historical evidence, but active planning surfaces are partially stale and internally contradictory. The repository implementation is ahead of several roadmap narratives. The highest-value fix is to make roadmap/state docs short, current, and evidence-linked rather than historical ledgers.

Overall health: **mixed (operational but drifted)**.

- **Strong:** deep audit trail in `.ai/05_logs/`, broad implementation evidence in `scripts/`, `config/datasets/`, and canonical graph artifacts.
- **Weak:** active roadmap/planning docs contain stale claims, duplicate status narratives, and references to missing artifacts.
- **Risk:** operators can choose wrong work because active docs disagree with code reality.

## Major Inconsistencies Found During Initial Reconciliation

1. **Roadmap path mismatch:** expected `.ai/roadmap/` does not exist; live roadmap is `.ai/01_roadmap/`.
2. **Master roadmap contradiction:** `/.ai/01_roadmap/master-roadmap.md` still says Promotion Layer is unimplemented, while `run_promote` and canonical relationship artifacts exist.
   - Evidence: `scripts/pipeline_cli.py`, `scripts/vitruvius/promotion_validator.py`, `003_Canonical-Knowledge-Layer/shared/relationships/*.md`.
3. **Current-phase contradiction (same file):** nested AGENTS was marked complete in one section and still treated as incomplete elsewhere.
   - Evidence: `/.ai/01_roadmap/current-phase.md`.
4. **Milestone stale residual note:** still reports RA-386 as unresolved and older aggregate metrics.
   - Evidence mismatch with `/.ai/05_logs/2026-04-20_ra-386-residual-hardening-validation.md` and dataset build report.
5. **Missing referenced artifact index:** `docs/LAWS_WAVE_ARTIFACT_INDEX.md` was referenced even though `docs/` is absent.
   - Evidence: `README.md`, `config/datasets/laws-artifact-catalog.yaml`, missing `/docs` path.
6. **Missing referenced viewer artifact:** multiple active docs pointed to `004_Derived-Content-Layer/graph-visualizations/ready-family-aggregate.html`, but the file is absent.
7. **Duplicate KG post-implementation docs left active:** v1 + v2 audit/rectification docs coexist without clear authoritative marker.

## What Was Updated In This Pass

### New control-surface files

- `/.ai/AUDIT_REPORT.md` (this file)
- `/.ai/IMPLEMENTATION_MATRIX.md`
- `/.ai/ACTIVE_WORK.md`
- `/.ai/STRATEGIC_NEXT_MOVE.md`
- `/.ai/README.md` (main navigation / where-to-start)
- `/.ai/archive/ARCHIVE_INDEX.md`

### Reconciliations / cleanup annotations

- Added audit warning banners to:
  - `/.ai/01_roadmap/master-roadmap.md`
  - `/.ai/01_roadmap/current-phase.md`
  - `/.ai/01_roadmap/milestone-tracker.md`
  - `/.ai/03_plans/INDEX.md`
- Marked superseded KG duplicates in place:
  - `/.ai/02_audits/2026-04-19_knowledge_graph_transition_post_implementation_audit.md`
  - `/.ai/03_plans/2026-04-19_knowledge_graph_transition_post_implementation_rectification_plan.md`
- Replaced stale laws-wave `/docs` references with repo-valid `.ai/03_plans/laws-wave/` paths in the active reference stack and dataset catalog.
- Narrowed the active AEC surface to the master plan plus the minimal session packet.
- Corrected `README.md` testing commands to the repo-proven `PYTHONPATH=scripts python3 -m pytest ...` form.

## What Was Archived

No destructive deletion was performed.

This pass used **soft archive in place** for two superseded files (v1 kept for history; v2 is authoritative), recorded in `/.ai/archive/ARCHIVE_INDEX.md`.

## Major Risks

1. **Execution misrouting risk:** operators may follow stale roadmap statuses instead of repo reality.
2. **Authority dilution risk:** multiple active docs compete as “truth,” especially around laws-wave and KG transition closure.
3. **Artifact reference decay:** historical/reference docs still contain some stale paths, so future edits must keep the live surface isolated from old narrative documents.
4. **Planning clutter risk:** AEC and laws-wave planning corpus remains very large; active vs historical boundary is still noisy.

## Strategic Conclusions

1. The codebase has substantial implemented capability (KG commands, tranche pipeline commands, explorer implementation, canonical relationships).
2. The critical problem is **planning-system coherence**, not feature absence.
3. The highest-leverage move is a focused rewrite of active roadmap/state docs into a short, evidence-backed “live operations layer,” while retaining long-form history in archive/reference lanes.

## Confidence Notes

- **High confidence:** structural inventory, command/code existence checks, and artifact presence/absence checks.
- **Medium confidence:** exact operational “completeness” of every historical plan (due to volume; matrix is evidence-based but grouped by meaningful initiative clusters).
