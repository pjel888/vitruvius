---
title: AEC Engine Research-to-Plan Audit
type: audit
status: accepted
date: 2026-04-15
derived_from:
  - .ai/13_research/AEC-ECS-SC_RESEARCH.md
governing_inputs:
  - AGENTS.md
  - .ai/00_system/EXECUTION_LOOP.md
  - .ai/00_system/principles.md
  - .ai/01_roadmap/master-roadmap.md
  - .ai/01_roadmap/current-phase.md
  - .ai/01_roadmap/milestone-tracker.md
  - .ai/06_specs/GOVERNANCE/07_RESEARCH_TO_PLAN_CONVERSION_STANDARD.md
  - .ai/06_specs/AEC_ENGINE/10_AEC_ENGINE_TASK_TEMPLATE.md
---

# AEC Engine Research-to-Plan Audit

## 0. Task Identity and State Alignment
- Task class: architecture / planning / governance
- Current phase alignment: between sprints; no active sprint owns this work
- Milestone alignment: this creates planning artifacts only; it does not mark implementation complete
- Related output plans: `AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md` plus subsystem plans under `.ai/03_plans/`
- State reconciliation: no roadmap/state file updates required because no implementation reality changed

## Research Source
- File: `.ai/13_research/AEC-ECS-SC_RESEARCH.md`
- Date: 2026-04-15
- Status in source: `RESEARCH`

## 1. Purpose
This audit converts the consolidated AEC research document into plan-grade facts by separating:
- architectural truths
- promising but unproven directions
- future-phase ideas
- blocked or deferred areas

The research is useful. It is not executable law.

## 2. Extraction Summary

### Proposed Subsystems
1. ECS core system
2. Spatial kernel
3. Knowledge vault
4. Z3 compiler and verification layer
5. Multi-disciplinary coordination engine
6. Optimization engine
7. Boundary translation system
8. LLM tool-calling layer
9. Financial / pricing oracle

### Architectural Truths Confirmed by Research and Specs
- Vitruvius must remain a compound AI system with hard layer separation.
- Geometry is derivative, not source truth.
- Determinism is mandatory below the optimization layer.
- Python orchestrates; Rust computes; RocksDB stores structured rules; Z3 adjudicates; the LLM translates.
- Boundary translation is an I/O responsibility, not internal kernel truth.
- Optimization must remain above verification.

### Open Questions Preserved From Research
- ECS persistence strategy
- undo / redo strategy
- multi-user concurrency model
- component version migration
- FEA scope and maturity
- WFC applicability limits
- numeric precision policy details for hybrid `f64`/`f32` usage

### Claimed Benefits
- mathematically bounded compliance engine
- reusable kernels across scale
- formal auditable verification
- stronger resistance to LLM hallucination
- portable compute via Rust and Wasm

### Risks Named by Research
- floating-point precision loss
- ECS “god component” anti-pattern
- spatial index thrashing
- vault corruption or schema drift
- Z3 misuse as source truth
- performance collapse from hot-loop metadata leakage
- constructability blind spots

## 3. Audit Against Current Repo Reality

### What Already Exists in Repo State
- Strong repo-wide governance stack
- Existing Rust and graph-oriented infrastructure per roadmap and current phase
- Completed or advanced work on promotion, graph/indexing, query, and multiple deterministic subsystems outside the AEC engine
- New AEC governance pack defining architectural law for the future engine

### What Does Not Exist Yet
- No master AEC engine implementation blueprint in `.ai/03_plans/`
- No subsystem-by-subsystem implementation plans for the AEC engine
- No declared execution order tying vault, ECS, Z3, spatial, optimization, and translation into one bounded rollout

### What In Research Is Not Yet Plan-Ready
- Broad references to FEA, fluids, WFC, MCTS, SA, and advanced optimization as if they are equally mature
- Implied concurrency ambitions without a deterministic single-node baseline
- Persistence discussion without a committed event model
- Wasm discussion without a concrete host boundary plan

### What Must Be Deferred
- Full FEA integration
- Multi-user collaborative editing
- production-scale stochastic search
- jurisdictional expansion beyond the first rule packs
- any optimization or generation loop that runs before the deterministic verification baseline is proven

## 4. Repo-Grounded Planning Constraints
- Planning must follow `AGENTS.md`, `EXECUTION_LOOP.md`, `principles.md`, roadmap, state docs, GOVERNANCE, RUST, and AEC_ENGINE packs.
- Research cannot authorize code or dependency adoption.
- Rust is a hardened compute zone and must not absorb legal interpretation, orchestration, or financial semantics.
- Boundary translation must not redefine internal canonical structures around IFC or other external schemas.
- The next AEC phase must use existing repo maturity where possible rather than pretending the whole system starts from zero.

## 5. Subsystem Readiness Assessment

| Subsystem | Maturity | Audit Judgment |
|---|---|---|
| ECS Core | Promising | Phase-ready if contracts stay narrow and persistence is deferred |
| Spatial Kernel | Promising | Phase-ready for collision / voxel / routing baseline; defer FEA breadth |
| Knowledge Vault | Phase-ready | Critical foundation; schema and temporality first |
| Z3 Verification | Phase-ready | Critical foundation; must consume compiled contracts, not raw law text |
| Coordination Engine | Promising | Build after ECS + Z3 + vault exist |
| Optimization Engine | Blocked by prerequisites | Defer stochastic breadth until deterministic baseline exists |
| Boundary Translation | Phase-ready | Build early as contract surface, not late-stage patch |
| LLM Tool Calling | Blocked by prerequisites | Build only after deterministic services exist |
| Financial / Pricing Oracle | Promising | Build as data-oracle and scoring layer above verification |

## 6. Core Planning Conclusions
1. The AEC engine must be planned as a staged architecture program, not a feature sprint.
2. The vault, DTO contracts, determinism rules, and verification path are prerequisites, not polish.
3. Optimization is downstream of verification. If planned too early, the architecture will rot.
4. FEA, concurrency, and broad Wasm delivery are explicit future-phase concerns, not baseline scope.
5. The subsystem plans must name stop conditions whenever the research remains unresolved.

## 7. Output Required by This Audit
- One master governing implementation plan
- Nine subsystem implementation plans
- A plan critique artifact
- A validation report

## 8. Final Audit Judgment
The research is strong enough to produce plans. It is not strong enough to justify direct implementation without first constraining scope, dependencies, and stop conditions.
