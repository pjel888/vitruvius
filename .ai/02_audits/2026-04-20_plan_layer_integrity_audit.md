# Plan Layer Integrity Audit

**Date:** 2026-04-20
**Auditor:** automated scan + human review
**Scope:** all `.md` files in `.ai/03_plans/`
**Method:** frontmatter extraction, INDEX cross-reference, stale-claim keyword scan, status/phase reconciliation against `current-phase.md`

---

## Summary

| Metric | Value |
|---|---|
| Files scanned | 132 |
| Issues found | ~120 (after removing false positives) |
| False positives | 2 ("only two active plans" matched inside anti-stale warnings) |
| Critical | INDEX.md stale references, missing structural frontmatter |
| High | Status drift between plans and live state |
| Medium | Missing `phase` fields on ~51 files |

---

## Critical Findings

### 1. INDEX.md references 4 files that do not exist
The following files are referenced in `INDEX.md` but are absent from `.ai/03_plans/`:
- `aec-first-slice-execution-handoff-dossier-2026-04-16.md`
- `aec-g10-evidence-completion-checklist-2026-04-16.md`
- `aec-g10-execution-strategy-2026-04-16.md`
- `aec-g10-missing-evidence-inventory-2026-04-16.md`

**Impact:** INDEX.md is untruthful about the live file set. Readers may search for non-existent handoff artifacts.

### 2. INDEX.md omits ~71 files from its inventory
The index was written when the plan layer was smaller. It now fails to list:
- All tranche expansion plans (tranche-1 through tranche-15, shards, follow-ons)
- All concept-fit admission plans (PD-957, PD-1067, RA-10066, etc.)
- All AEC first-slice support plans (artifact-shapes, assumptions, benchmarks, etc.)
- All aggregate/support plans (generic-aggregate, quality-reporting, etc.)
- All explorer plans
- The rectification plans

**Impact:** The index cannot serve as a reliable lookup surface.

### 3. Missing required frontmatter on structural files
| File | Missing |
|---|---|
| `00-governing-implementation-plan.md` | `task` (has `plan_id` instead) |
| `AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md` | `task`, `created`, `phase` |
| `AEC_ENGINE_ECS_CORE_IMPLEMENTATION_PLAN.md` | `task`, `created`, `phase` |
| `AEC_ENGINE_SPATIAL_KERNEL_IMPLEMENTATION_PLAN.md` | `task`, `created`, `phase` |
| `AEC_ENGINE_KNOWLEDGE_VAULT_IMPLEMENTATION_PLAN.md` | `task`, `created`, `phase` |
| `AEC_ENGINE_Z3_VERIFICATION_IMPLEMENTATION_PLAN.md` | `task`, `created`, `phase` |
| `AEC_ENGINE_MULTI_DISCIPLINARY_COORDINATION_IMPLEMENTATION_PLAN.md` | `task`, `created`, `phase` |
| `AEC_ENGINE_OPTIMIZATION_ENGINE_IMPLEMENTATION_PLAN.md` | `task`, `created`, `phase` |
| `AEC_ENGINE_BOUNDARY_TRANSLATION_IMPLEMENTATION_PLAN.md` | `task`, `created`, `phase` |
| `AEC_ENGINE_LLM_TOOL_CALLING_IMPLEMENTATION_PLAN.md` | `task`, `created`, `phase` |
| `AEC_ENGINE_FINANCIAL_PRICING_ORACLE_IMPLEMENTATION_PLAN.md` | `task`, `created`, `phase` |
| `explorer-graph-rendering-implementation-plan.md` | `task`, `status`, `created`, `phase` |
| `explorer-graph-rendering-rewrite-plan.md` | `task`, `status`, `created`, `phase` |
| `vitruvius-explorer-phase-1-foundation.md` | `task`, `status`, `created`, `phase` |
| `vitruvius-explorer-remediation-plan.md` | `task`, `status`, `created`, `phase` |
| `2026-04-19_knowledge_graph_transition_post_implementation_rectification_plan.md` | `task`, `status`, `created`, `phase` |
| `2026-04-19_knowledge_graph_transition_post_implementation_rectification_plan_v2.md` | `task`, `status`, `created`, `phase` |

**Impact:** Automated tooling and index builders cannot classify these files correctly.

---

## High Findings

### 4. Status drift — plans marked `in_progress` that may be complete
The following plans carry `in_progress` status but the bounded work they describe was completed during the laws-wave execution burst:
- `2026-04-17_tranche-10-expansion-plan.md`
- `2026-04-17_tranche-11-expansion-plan.md`
- `2026-04-17_tranche-12-expansion-plan.md`
- `2026-04-17_tranche-6-expansion-plan.md`
- `2026-04-17_tranche-8-expansion-plan.md`
- `2026-04-17_tranche-9-expansion-plan.md`
- `2026-04-18_aggregate-quality-reporting-plan.md`
- `2026-04-18_bootstrap-artifact-promotion-plan.md`
- `2026-04-18_completed-laws-aggregate-graph-plan.md`
- `2026-04-18_dataset-wide-automation-plan.md`
- `2026-04-18_hlurb-dhsud-agency-split-plan.md`
- `2026-04-18_prc-expansion-plan.md`
- `2026-04-18_remaining-pool-final-disposition-plan.md`
- `2026-04-18_tranche-15-sharding-plan.md`

**Note:** These must be verified individually against validation logs before status is flipped. Do not bulk-update without evidence.

### 5. Phase 11 plans still in `DRAFT` or `in_progress`
Per `current-phase.md` §Next Gates, Phase 11 expansion is gated. Several Phase 11 plans exist in draft form:
- `2026-04-17_all-laws-readiness-8gb-rollout-plan.md`
- `2026-04-17_common-areas-concept-plan.md`
- `2026-04-17_laws-risk-hardening-plan.md`
- `2026-04-17_laws-section-hierarchy-graph-plan.md`
- `2026-04-17_laws-tranche-1-source-admission-plan.md`
- etc.

Some of these may have been executed (e.g., common-areas was admitted, tranche-1 source admission was executed). Their statuses should reflect actual execution state.

---

## Medium Findings

### 6. Missing `phase` field on ~51 files
Many plans created during the rapid laws-wave execution lack the `phase` frontmatter field. This is recommended but not required. Automated reporting and filtering are degraded.

### 7. `00-governing-implementation-plan.md` claims "between sprints"
Line 50 says "The repo is between sprints." While no AEC sprint is active, the laws-wave residual-hardening lane was actively executing until 2026-04-20. The claim is directionally true for product-code sprints but may mislead about governance execution.

---

## Recommendations

1. **Remove stale references from INDEX.md** — delete the 4 missing AEC handoff file references.
2. **Rebuild INDEX.md inventory** — add all 71 missing files, grouped by status/type, and remove obsolete ordering text.
3. **Add missing frontmatter** to AEC_ENGINE_*, explorer, rectification, and governing plan files.
4. **Status reconciliation** — verify each `in_progress` plan against its validation log; flip to `complete` where evidence supports it.
5. **Phase 11 gate enforcement** — ensure any executed Phase 11 plans are marked `complete` and any unexecuted ones remain `draft` or are archived if superseded.

---

## Validation

This audit was produced by:
- `scripts/audit_plan_layer.py` (automated frontmatter + INDEX scan)
- Manual review of `current-phase.md` §Next Gates and §Laws Mini Dataset→Graph Pipeline
- Cross-check against git log for recent commit evidence
