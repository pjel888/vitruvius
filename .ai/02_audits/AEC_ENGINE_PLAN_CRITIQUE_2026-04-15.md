---
title: AEC Engine Plan Critique
type: critique
status: accepted
date: 2026-04-15
derived_from:
  - .ai/03_plans/AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md
  - .ai/03_plans/AEC_ENGINE_*_IMPLEMENTATION_PLAN.md
governing_inputs:
  - AGENTS.md
  - .ai/00_system/EXECUTION_LOOP.md
  - .ai/06_specs/GOVERNANCE/07_RESEARCH_TO_PLAN_CONVERSION_STANDARD.md
  - .ai/06_specs/AEC_ENGINE/10_AEC_ENGINE_TASK_TEMPLATE.md
---

# AEC Engine Plan Critique

## 1. Master Plan Critique

### Over-Ambition Risk
- The research wants everything at once: ECS, spatial kernels, Z3, optimization, IFC, pricing, Wasm, and advanced engineering solvers. The master plan correctly stages them, but implementation pressure will try to collapse Phases 4 through 7. That must be resisted.

### Hidden Dependency Risk
- The master plan assumes the Phase 1 contract freeze is taken seriously. If teams start building DTOs and schemas in parallel before that freeze, every downstream subsystem will drift.
- The plan assumes rule AST structure is known early enough for both the vault and Z3 compiler. If the AST stays soft, both subsystems will stall or fork.

### Boundary Risk
- The easiest failure mode is to let boundary translation dictate the internal model because IFC already exists. That would poison the ECS and spatial kernel with external schema baggage.
- Another likely failure mode is to let optimization become the public face before verification is complete, which would create attractive but untrustworthy outputs.

### Sequencing Risk
- Financial oracle and optimization are intentionally later. Engineers will be tempted to pull them earlier because they are user-visible. That would produce demos faster and architecture failure even faster.

## 2. Subsystem Critique

### ECS Core
- Persistence is still not solved. The plan correctly refuses to solve it implicitly, but that means future execution must not smuggle persistence requirements into baseline ECS work.

### Spatial Kernel
- Research pressure toward FEA, fluids, and pathfinding breadth is still dangerous. The current plan is safe only if the kernel stays narrow at first.

### Knowledge Vault
- The vault is the easiest place to hide schema debt. If provenance or temporal fields are optional even once, later truth governance becomes fiction.

### Z3 Verification
- The plan can fail if teams treat unsupported rule families as “mostly covered.” Unsupported classes must remain explicit rejects, not soft claims.

### Multi-Disciplinary Coordination
- “Coordination” is vague by nature. Without hard conflict taxonomies and escalation rules, this subsystem will become a dumping ground.

### Optimization Engine
- This is the subsystem most likely to cause architecture drift. It is attractive, stochastic, and easy to oversell. It must stay gated behind verification.

### Boundary Translation
- Over-documenting external schemas would be a trap. The translation plan should remain about contract boundaries, not full BIM encyclopedias.

### LLM Tool Calling
- This subsystem will fail if refusal behavior is weak. Unsupported requests must hard-fail cleanly.

### Financial / Pricing Oracle
- Freshness and uncertainty are the main unresolved risk. Cost without provenance is theater.

## 3. Where the Plan May Still Under-Document
- explicit event / replay model for ECS snapshots
- unsupported rule-family taxonomy for early Z3 scope
- exact audit artifact naming conventions for future implementation runs
- benchmark thresholds for spatial hot paths and solver latency

## 4. Where the Plan Might Drift Over Time
- external schema support matrix
- pricing-source freshness policy
- stochastic algorithm roster
- accepted rule-family coverage inside the Z3 compiler

## 5. Direct Warnings for Codex
- Do not infer missing contracts from research prose.
- Do not implement FEA because the research mentions it.
- Do not embed legal semantics in Rust because it feels “cleaner.”
- Do not expose an LLM-facing tool until the deterministic artifact it cites already exists.

## 6. Critique Verdict
The plan set is viable because it says “not yet” in the right places. If those deferrals are ignored, the plan becomes another research document pretending to be executable.
