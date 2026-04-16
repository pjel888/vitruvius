---
task: aec-t018-pricing-optimization-foundation
phase: 05
created: 2026-04-16
author: PLANNER
supersedes: null
status: accepted
implementation_blocked: true
planning_gate_ready: true
subsystem_ready: false
execution_role: downstream-not-selected-for-first-slice
paired_subsystem_plan: AEC_ENGINE_FINANCIAL_PRICING_ORACLE_IMPLEMENTATION_PLAN.md + AEC_ENGINE_OPTIMIZATION_ENGINE_IMPLEMENTATION_PLAN.md
gate_key: pricing + optimization
---

# AEC-T018 Pricing and Optimization Foundation Plan

## Planning Status
- planning gate: ready
- execution selection: downstream / not in first bounded slice
- interpretation: planning readiness is satisfied, but execution evidence is still pending and the subsystem is not selected for the current bounded sprint

## Purpose
Resolve `AEC-T018` at the planning layer by defining accepted downstream foundation packages for pricing and optimization while keeping implementation blocked.

## Pricing outputs to preserve
- quantity contract defined
- pricebook schema defined
- currency and freshness policy defined
- refusal behavior defined

## Optimization outputs to preserve
- objective vector defined
- reproducibility metadata defined
- frontier-first deterministic baseline defined
- seeded-search path remains explicitly gated

## Required future tests
- `scripts/tests/test_aec_pricing_schema.py`
- `scripts/tests/test_aec_pricing_quantities.py`
- `scripts/tests/test_aec_pricing_oracle.py`
- `scripts/tests/test_aec_pricing_refusals.py`
- `scripts/tests/test_aec_optimization_objectives.py`
- `scripts/tests/test_aec_optimization_frontier.py`
- `scripts/tests/test_aec_optimization_replay.py`
- `scripts/tests/test_aec_optimization_seeded_search.py`

## Stop conditions
- pricing evaluates unverified geometry
- optimization blesses unverified candidates
- stochastic search appears without explicit seeding and replay guarantees
