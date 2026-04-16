# `.ai/03_plans/` — Active Plan Index

> **Authoritative dispatcher:** `00-governing-implementation-plan.md`
> **Authoritative state snapshot:** `/.ai/01_roadmap/current-phase.md`
> **Updated:** 2026-04-16

## Purpose
This index answers two questions:
1. what active plans currently exist in `.ai/03_plans/`
2. which plan a reader should open next

It is an inventory and lookup surface.
It is not the execution-order authority. The governing plan owns execution order.

## Current Active Plan Set

| File | Plan Type | Status | Scope | Open Next When |
|---|---|---|---|---|
| `00-governing-implementation-plan.md` | orchestration | active | dispatches the live plan layer | you are entering `.ai/03_plans/` fresh |
| `2026-04-15-nested-agents-governance-plan.md` | governance maintenance | accepted / pending execution | nested `AGENTS.md` hierarchy | you are working on AGENTS coverage and hierarchy |
| `2026-04-16-whole-codebase-plans-upgrade-plan.md` | governance maintenance | active | current rewrite task for the plan layer | you are continuing the plan-layer rewrite task |
| `2026-04-16_graph-warning-and-gitnexus-warning-plan.md` | maintenance draft | draft / unexecuted | graph-warning reduction and GitNexus warning investigation | you are explicitly taking up the warning-reduction draft |
| `2026-04-16_laws-mini-dataset-graph-pipeline-plan.md` | implementation plan | accepted / bounded pilot success achieved | scoped core-laws-bundle graph proof and scale path | you are auditing the bounded pilot lane or tracing how the laws dataset work shipped |
| `2026-04-16_laws-m2-admission-plan.md` | implementation plan | complete | per-law truth admission + dataset-safe M2 path for blocked laws | you are tracing how the blocked non-PD laws were admitted inside the bounded lane |
| `2026-04-16_laws-m4-expansion-path-plan.md` | implementation plan | complete | minimal post-pilot scaling contract + additive law-unit runtime support | you are tracing the accepted M4 slice or planning a future section/merge follow-on |
| `AEC_ENGINE_BOUNDARY_TRANSLATION_IMPLEMENTATION_PLAN.md` | subsystem plan | proposed | IFC/CAD/DTO boundary translation | AEC import/export work is selected |
| `AEC_ENGINE_ECS_CORE_IMPLEMENTATION_PLAN.md` | subsystem plan | proposed | canonical ECS world state | AEC ECS work is selected |
| `AEC_ENGINE_FINANCIAL_PRICING_ORACLE_IMPLEMENTATION_PLAN.md` | subsystem plan | proposed | pricing and quantity scoring | AEC pricing work is selected |
| `AEC_ENGINE_KNOWLEDGE_VAULT_IMPLEMENTATION_PLAN.md` | subsystem plan | proposed | temporal rule vault and AST storage | AEC vault work is selected |
| `AEC_ENGINE_LLM_TOOL_CALLING_IMPLEMENTATION_PLAN.md` | subsystem plan | proposed | bounded tool-calling and explanation | AEC tool layer work is selected |
| `AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md` | architecture implementation plan | proposed | governs AEC sequencing and integration boundaries | you are doing any AEC planning or future implementation |
| `AEC_ENGINE_MULTI_DISCIPLINARY_COORDINATION_IMPLEMENTATION_PLAN.md` | subsystem plan | proposed | cross-discipline issue coordination | AEC coordination work is selected |
| `AEC_ENGINE_OPTIMIZATION_ENGINE_IMPLEMENTATION_PLAN.md` | subsystem plan | proposed | scoring, Pareto frontier, bounded search | AEC optimization work is selected |
| `AEC_ENGINE_SPATIAL_KERNEL_IMPLEMENTATION_PLAN.md` | subsystem plan | proposed | deterministic spatial compute | AEC spatial work is selected |
| `AEC_ENGINE_Z3_VERIFICATION_IMPLEMENTATION_PLAN.md` | subsystem plan | proposed | formal verification compiler and replay | AEC Z3 work is selected |

## Reader Entry Order

### For General Plan Consumption
1. `00-governing-implementation-plan.md`
2. this file
3. the specific active plan for the task

### For AGENTS Hierarchy Work
1. `00-governing-implementation-plan.md`
2. this file
3. `2026-04-15-nested-agents-governance-plan.md`

### For AEC Work
1. `00-governing-implementation-plan.md`
2. this file
3. `AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md`
4. only the subsystem plans relevant to the selected slice

## Plan Families

### Governance / Maintenance
- `00-governing-implementation-plan.md`
- `2026-04-15-nested-agents-governance-plan.md`
- `2026-04-16-whole-codebase-plans-upgrade-plan.md`
- `2026-04-16_graph-warning-and-gitnexus-warning-plan.md` (draft / unexecuted)

### Dataset→Graph Planning
- `2026-04-16_laws-mini-dataset-graph-pipeline-plan.md`
- `2026-04-16_laws-m2-admission-plan.md`
- `2026-04-16_laws-m4-expansion-path-plan.md`

### AEC Engine
- `2026-04-16-aec-first-bounded-slice-pre-implementation-plan.md`
- `AEC_ENGINE_BOUNDARY_TRANSLATION_IMPLEMENTATION_PLAN.md`
- `AEC_ENGINE_ECS_CORE_IMPLEMENTATION_PLAN.md`
- `AEC_ENGINE_FINANCIAL_PRICING_ORACLE_IMPLEMENTATION_PLAN.md`
- `AEC_ENGINE_KNOWLEDGE_VAULT_IMPLEMENTATION_PLAN.md`
- `AEC_ENGINE_LLM_TOOL_CALLING_IMPLEMENTATION_PLAN.md`
- `AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md`
- `AEC_ENGINE_MULTI_DISCIPLINARY_COORDINATION_IMPLEMENTATION_PLAN.md`
- `AEC_ENGINE_OPTIMIZATION_ENGINE_IMPLEMENTATION_PLAN.md`
- `AEC_ENGINE_SPATIAL_KERNEL_IMPLEMENTATION_PLAN.md`
- `AEC_ENGINE_Z3_VERIFICATION_IMPLEMENTATION_PLAN.md`

### Recently Archived (2026-04-16)
- `2026-04-16-app-integrity-reliability-plan.md`
- `2026-04-16_cli-human-readable-output-plan.md`
- `2026-04-16_readme-investor-mermaid-diagram-plan.md`
- `2026-04-16_master-audit-implementation-plan.md`
- `2026-04-16_duplicate-canonical-source-id-remediation-plan.md`

## Relationship to Archived Plans
- Archived plans live in `/.ai/09_archive/plans/`.
- They are historical inputs, not active dispatch targets.
- If a new task wants to reuse archived work, it must cite the archived file explicitly from a new live plan or audit.

## Plan Writing Standards For This Directory
- live plans must use truthful status values
- live plans must name real repo anchors where relevant
- active inventory here must match the actual directory listing
- execution order belongs in the governing plan, not in duplicated diagrams here
- historical sprint narration belongs in archive or decisions, not in the active inventory

## Notes
- The AEC family remains planning-only. No runtime code roots have been created yet.
- The nested-AGENTS plan remains a live governance candidate because the repo still lacks several of the target nested `AGENTS.md` files.
- The five completed 2026-04-16 non-AEC plans were archived to `/.ai/09_archive/plans/` during the plan-layer cleanup pass.
