---
task: aec-t019-tooling-foundation
phase: 05
created: 2026-04-16
author: PLANNER
supersedes: null
status: accepted
implementation_blocked: true
planning_gate_ready: true
subsystem_ready: false
execution_role: downstream-not-selected-for-first-slice
paired_subsystem_plan: AEC_ENGINE_LLM_TOOL_CALLING_IMPLEMENTATION_PLAN.md
gate_key: llm_tools
---

# AEC-T019 Tooling Foundation Plan

## Planning Status
- planning gate: ready
- execution selection: downstream / not in first bounded slice
- interpretation: planning readiness is satisfied, but execution evidence is still pending and the subsystem is not selected for the current bounded sprint

## Purpose
Resolve `AEC-T019` at the planning layer by defining the accepted tooling foundation package while keeping implementation blocked.

## Required outputs
- tool catalog design frozen
- authority fence frozen
- refusal taxonomy frozen
- explanation payload contract bound to stored artifacts/snapshots

## Required future tests
- `scripts/tests/test_aec_tools_catalog.py`
- `scripts/tests/test_aec_tools_router.py`
- `scripts/tests/test_aec_tools_refusals.py`
- `scripts/tests/test_aec_tools_explainer.py`

## Stop conditions
- tool routing makes compliance decisions
- explanations are not artifact-grounded
- hidden multi-action workflows appear
