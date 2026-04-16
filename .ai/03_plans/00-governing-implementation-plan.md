---
plan_id: governing-implementation
phase: "Meta — Active Plan Dispatch"
title: "Governing Implementation Plan — Active Plan Dispatcher and Execution Gates"
status: active
priority: highest
sprint: "Meta"
version: 4.0.0
plan_type: orchestration
created: 2026-04-15
last_updated: 2026-04-16
owner: Senior Systems Architect
takes_precedence_over:
  - "Any execution-order claim in any other active plan"
  - "Any stale inventory claim in `.ai/03_plans/INDEX.md` or roadmap/state summaries"
dependencies:
  - AGENTS.md
  - .ai/00_system/EXECUTION_LOOP.md
  - .ai/00_system/principles.md
  - .ai/01_roadmap/master-roadmap.md
  - .ai/01_roadmap/current-phase.md
  - .ai/01_roadmap/milestone-tracker.md
  - .ai/02_audits/WHOLE_CODEBASE_PLAN_LAYER_AUDIT_2026-04-16.md
  - .ai/03_plans/INDEX.md
  - .ai/10_state/active_context.md
  - .ai/10_state/known_issues.md
---

# Governing Implementation Plan

## 1. Purpose
This file is the live dispatcher for the active plan layer.

It exists to answer three questions safely:
1. which plans are actually active right now
2. which plan a worker must read next for a given class of work
3. what must be true before implementation can start

This file is not a sprint-history dump.
Archived sprint history lives in `.ai/09_archive/plans/` and in the decision/state ledgers.

## 2. Current Repo Ground Truth

### 2.1 Runtime Reality
- Vitruvius is a Python-first system with lazy CLI dispatch in `scripts/pipeline_cli.py`.
- Rust is a hardened compute boundary under `scripts/vitruvius/engine_rs/` and `scripts/vitruvius/datalog_rs/`.
- TypeScript is isolated to `spatial-daemon/` and communicates by file contract, not by live service coupling.

### 2.2 Execution Reality
- The repo is between sprints.
- The historical sprint burst described in archived plans and state ledgers is largely closed.
- No AEC runtime implementation is active yet.
- The active work in `.ai/03_plans/` is governance/planning work, not product-code execution.

### 2.3 Planning Reality
- The plan layer now contains multiple active or live-reference documents again.
- Any document claiming only two active plans is stale and must be ignored.
- Archived plans remain reference-only and cannot be implicitly reactivated.

## 3. Active Plan Inventory

### 3.1 Active / Live-Reference Plans

| Order | File | Role | Status | How to use it |
|---|---|---|---|---|
| 1 | `00-governing-implementation-plan.md` | top-level dispatcher | active | read first for any work that starts in `.ai/03_plans/` |
| 2 | `INDEX.md` | inventory and lookup table | active reference | use to locate the right active plan and archived lineage |
| 3 | `2026-04-16-whole-codebase-plans-upgrade-plan.md` | current task meta-plan | active until validation closes | governs the current plan-layer rewrite task |
| 4 | `2026-04-15-nested-agents-governance-plan.md` | governance maintenance plan | accepted / pending execution | use only for AGENTS hierarchy work |
| 5 | `2026-04-16_graph-warning-and-gitnexus-warning-plan.md` | maintenance draft | draft / unexecuted | use only when explicitly taking up the warning-reduction draft |
| 6 | `2026-04-16_laws-mini-dataset-graph-pipeline-plan.md` | dataset→graph implementation plan | accepted / partially executed | governs the M1→M4 laws mini dataset graph lane |
| 7 | `2026-04-16_laws-m2-admission-plan.md` | dataset→graph follow-on implementation plan | accepted / in progress | governs the per-law M2 admission path after the M1 partial result |
| 8 | `AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md` | AEC execution-order authority | proposed | read before any AEC subsystem plan |
| 9 | `AEC_ENGINE_ECS_CORE_IMPLEMENTATION_PLAN.md` | AEC subsystem plan | proposed | use only with AEC master plan |
| 10 | `AEC_ENGINE_SPATIAL_KERNEL_IMPLEMENTATION_PLAN.md` | AEC subsystem plan | proposed | use only with AEC master plan |
| 11 | `AEC_ENGINE_KNOWLEDGE_VAULT_IMPLEMENTATION_PLAN.md` | AEC subsystem plan | proposed | use only with AEC master plan |
| 12 | `AEC_ENGINE_Z3_VERIFICATION_IMPLEMENTATION_PLAN.md` | AEC subsystem plan | proposed | use only with AEC master plan |
| 13 | `AEC_ENGINE_MULTI_DISCIPLINARY_COORDINATION_IMPLEMENTATION_PLAN.md` | AEC subsystem plan | proposed | use only with AEC master plan |
| 14 | `AEC_ENGINE_OPTIMIZATION_ENGINE_IMPLEMENTATION_PLAN.md` | AEC subsystem plan | proposed | use only with AEC master plan |
| 15 | `AEC_ENGINE_BOUNDARY_TRANSLATION_IMPLEMENTATION_PLAN.md` | AEC subsystem plan | proposed | use only with AEC master plan |
| 16 | `AEC_ENGINE_LLM_TOOL_CALLING_IMPLEMENTATION_PLAN.md` | AEC subsystem plan | proposed | use only with AEC master plan |
| 17 | `AEC_ENGINE_FINANCIAL_PRICING_ORACLE_IMPLEMENTATION_PLAN.md` | AEC subsystem plan | proposed | use only with AEC master plan |

### 3.2 Archived Plans
- Archived sprint plans live in `.ai/09_archive/plans/`.
- They remain useful as implementation evidence and historical constraints.
- They are not dispatchable by default.
- If future work wants to reuse archived logic, it must create a new live plan that cites the archived plan explicitly.

## 4. Consumption Order

### 4.1 For Any Plan-Layer Task
1. read this file
2. read `INDEX.md`
3. read `current-phase.md`
4. read the specific live plan for the work
5. check whether the plan is active, accepted, or merely proposed

### 4.2 For AGENTS Hierarchy Work
1. read this file
2. read `2026-04-15-nested-agents-governance-plan.md`
3. read the AGENTS audit / validation artifacts
4. do not consult archived sprint plans for AGENTS scope decisions

### 4.3 For AEC Work
1. read this file
2. read `AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md`
3. read only the relevant AEC subsystem plans
4. read the AEC/GOVERNANCE/RUST packs named in those plans
5. do not start implementation until the AEC namespace decision and code-root allocation are accepted

## 5. Governing Execution Order

### 5.1 Plan-Layer Maintenance Lane
This lane is active now.

Sequence:
1. whole-codebase plan-layer audit and rewrite
2. validation of rewritten plan layer
3. optional execution of the nested-AGENTS governance plan if still required after the rewrite

Entry gate:
- live plan layer contains stale or contradictory guidance

Exit gate:
- all active plans are truthful, codebase-aware, and internally consistent

### 5.2 AEC Planning Lane
This lane is active as planning only.

Sequence:
1. master AEC plan
2. subsystem plan refinement and critique
3. namespace and code-root decision
4. implementation kick-off only after a new execution trigger exists

Entry gate:
- AEC implementation request exists
- master plan and relevant subsystem plans are accepted
- planned namespace is frozen

Exit gate:
- implementation-ready artifact set exists with validation and stop conditions

### 5.3 Archived Sprint Lane
Closed by default.

Any attempt to reopen archived sprint work must:
- create a new trigger
- cite the archived plan explicitly
- explain why the archived plan is insufficient as-is

## 6. AEC Implementation Gate Matrix

| Gate | Must be true before AEC coding starts |
|---|---|
| Namespace gate | planned Python namespace and Rust extension points are explicitly frozen |
| Boundary gate | Python / Rust / TypeScript ownership is explicit in the relevant subsystem plans |
| Validation gate | each subsystem plan names the existing test and benchmark surfaces it will extend |
| Truth gate | Knowledge vault and promotion rules are aligned with GOVERNANCE truth contracts |
| Determinism gate | replay and audit artifact requirements are frozen before optimization or tool-calling work starts |

If any gate is open, AEC work remains planning-only.

## 7. Cross-Plan Rules

### 7.1 Governing Plan vs Index
- This file defines execution order.
- `INDEX.md` defines inventory and lookup.
- If they diverge, this file wins and `INDEX.md` must be repaired immediately.

### 7.2 Governing Plan vs Current Phase
- `current-phase.md` is the live execution snapshot.
- This file is the plan-layer dispatcher.
- If `current-phase.md` points to stale plan versions or stale plan identities, correct it as state drift.

### 7.3 Master AEC Plan vs Subsystem Plans
- the master plan defines sequencing and cross-subsystem boundaries
- subsystem plans define local implementation steps
- if a subsystem plan implies a different phase order than the master plan, the master plan wins until the full AEC set is revised together

## 8. Known Plan-Layer Risks
- stale inventory claims can misroute future agents
- AEC implementation can fragment across existing packages if the namespace decision is not frozen
- subsystem plans can drift into spec duplication if they restate whole governance packs instead of naming repo-local consequences
- state files can keep pointing to obsolete versions if plan rewrites do not reconcile them

## 9. Validation Requirements For Any Active Plan Edit
- frontmatter status is truthful
- execution state is truthful
- plan references match real files
- no active plan claims archived work is still dispatchable
- AEC plans name actual repo anchors, tests, flags, and boundaries
- `INDEX.md` inventory matches the actual directory listing

## 10. Stop Conditions
- a live plan contradicts this dispatcher and the contradiction is not explicitly resolved
- a proposed plan is treated as implementation-ready without acceptance criteria being met
- archived work is being revived by implication instead of by a new live plan
- AEC code is requested before namespace, validation, and boundary gates are frozen

## 11. Immediate Next Actions
1. finish the whole-codebase plan-layer rewrite and validation
2. keep the nested-AGENTS plan available as the next governance maintenance lane if AGENTS coverage remains incomplete
3. treat the AEC family as planning-ready but implementation-blocked until namespace and trigger artifacts are approved

## 12. Handoff Rule
Any future worker entering `.ai/03_plans/` must start here.

If they do not, they are operating out of order.
