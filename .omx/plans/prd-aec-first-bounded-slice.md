# PRD — AEC First Bounded Slice

## Goal
Implement the first bounded AEC slice as a Python-first contract spine from strict boundary payload to ECS world, bounded spatial facts, and verifier whitelist artifacts.

## Scope
- strict boundary import lane
- bounded DTO family
- Python reference ECS world
- bounded spatial fact lane
- verifier whitelist/refusal/artifact lane

## Out of scope
- pricing
- optimization
- coordination
- LLM tool routing
- Rust-first execution
- TypeScript orchestration

## User stories
### US-001 Strict boundary import
As a pipeline operator, I want one strict AEC import lane so only footer-valid, unit-explicit payloads enter the bounded slice.

### US-002 Deterministic ECS world
As a downstream subsystem, I want one deterministic ECS world and snapshot contract so replay and schedule order are stable.

### US-003 Bounded spatial facts
As the verifier, I want bounded spatial facts produced outside the solver so rule checks remain explicit and replayable.

### US-004 Explicit verification artifacts
As an auditor, I want sat/unsat/refusal artifacts so the first slice remains traceable and bounded.
