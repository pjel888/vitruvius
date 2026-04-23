---
task: aec-runtime-roots-audit-and-lane-decision
phase: meta
created: 2026-04-23
author: Hephaestus
status: COMPLETE
---

# AEC Runtime Roots Audit and Lane Decision — 2026-04-23

## Scope

Audit the repository for real AEC runtime roots and record the bounded planning decision for what AEC should be treated as now.

## Question Answered

Does Vitruvius currently contain actual AEC runtime implementation roots, or only AEC planning and precursor capabilities?

## Repo Evidence

### 1. Runtime roots searched for directly

Searched for the following concrete runtime signals:
- `scripts/vitruvius/aec/**`
- `scripts/tests/test_aec_*`
- AEC-related CLI wiring in `scripts/pipeline_cli.py`
- explicit AEC runtime names in `scripts/`, `spatial-daemon/`, and executable source files

Observed result:
- no `scripts/vitruvius/aec/` namespace exists
- no `scripts/tests/test_aec_*` files exist
- no AEC CLI command wiring was found in `scripts/pipeline_cli.py`
- no explicit AEC runtime code roots were found in `scripts/` or `spatial-daemon/`

### 2. What does exist in code

The repo does contain precursor capabilities that a future AEC subsystem could build on:
- spatial intake and contract handling
- Z3 / inequality solving precedent
- deterministic graph and event-store patterns
- optimization precedent
- Rust compute kernels
- TypeScript spatial boundary work

These are reusable foundations, not an AEC runtime namespace.

### 3. What exists in planning/state

The AEC surface is substantial in planning artifacts:
- `.ai/03_plans/AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md`
- `.ai/03_plans/AEC_ENGINE_*_IMPLEMENTATION_PLAN.md`
- multiple AEC audits under `.ai/02_audits/`
- multiple AEC research packs under `.ai/13_research/`
- AEC tasks and baselines under `.ai/04_tasks/` and `.ai/10_state/baselines/`

The strongest planning statement is already explicit in:
- `.ai/03_plans/AEC_ENGINE_MASTER_IMPLEMENTATION_PLAN.md`

Current truth recorded there:
- “the AEC engine is not implemented in runtime code yet”

### 4. Live operating docs agree

The live control surface currently treats AEC as planned / blocked rather than implemented:
- `.ai/ACTIVE_WORK.md`
- `.ai/STRATEGIC_NEXT_MOVE.md`
- `.ai/IMPLEMENTATION_MATRIX.md`
- `.ai/10_state/active_context.md`

The implementation matrix is especially direct:
- AEC first bounded slice family → `planned`
- gap summary: runtime implementation roots not found in code search

## Audit Conclusion

Vitruvius does **not** currently have real AEC runtime roots.

The repo has:
- a large AEC planning / audit / research corpus,
- several strong non-AEC runtime precursors that would support later AEC implementation,
- but no actual AEC runtime namespace, tests, CLI entry points, or executable subsystem roots.

## Decision

AEC should remain the **next planned lane**, but **not** be treated as active runtime implementation yet.

That means:
- AEC remains the highest-leverage next implementation family in planning,
- the repo should not claim that AEC runtime has started,
- the next valid move is decision and preparation, not coding the runtime now.

## Recommended Bounded Next Move

Keep AEC as the next planned lane and use this audit as the grounding artifact for a future go / no-go decision.

Concretely:
1. preserve AEC as the next live planning family,
2. do not open runtime implementation until a bounded execution packet is accepted,
3. require the first implementation trigger to create the actual runtime roots explicitly (starting with the planned namespace rather than spreading changes opportunistically).

## Non-Decision

This audit does **not** authorize AEC runtime implementation.

It only establishes that:
- runtime roots are absent today,
- AEC should still stay next-in-line at the planning layer.
