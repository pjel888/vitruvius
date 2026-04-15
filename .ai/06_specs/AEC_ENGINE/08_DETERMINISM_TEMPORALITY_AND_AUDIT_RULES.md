# Determinism, Temporality, and Audit Rules

## Purpose
This file defines the mandatory reproducibility, temporal-clock, and audit-trail rules for the AEC engine. It exists to ensure that a design verdict, clash resolution, solver proof, or optimization result can be replayed later from recorded evidence rather than trusted by memory.

## Scope
This file governs:
- deterministic execution expectations across the five-layer system
- temporal binding of rules, prices, and project-state snapshots
- audit artifacts for tool calls, boundary crossings, solver runs, and committed geometry
- replay and retroactive-audit requirements

This file does NOT govern:
- project-wide validation law — see `.ai/06_specs/GOVERNANCE/01_VALIDATION_PROTOCOL.md`
- vault schema — see `04_KNOWLEDGE_VAULT_AND_RULE_AST_CONTRACT.md`
- formal verification semantics — see `06_FORMAL_VERIFICATION_AND_Z3_PROTOCOL.md`
- optimization objectives — see `09_PARETO_OPTIMIZATION_AND_FINANCIAL_LAYER_RULES.md`

## Core Principle
If the engine cannot replay a result from recorded artifacts, the result is not trustworthy enough to commit.

## 1. Determinism Rules
- The same snapshot, same temporal clock, same input payloads, same solver configuration, and same feature-flag state MUST produce the same machine-readable result.
- Determinism applies below the Python layer by default. Any exception requires an AD and explicit containment.
- Any ordering that escapes a layer boundary MUST be stable and explicit. Hash-order-dependent output is forbidden.
- Randomness, if used at all, MUST use an explicit seed recorded in the audit trail.
- Parallel execution is allowed only when it is proven not to change observable output.

## 2. Temporal Clock Rules
- Time relevant to verification, pricing, and rule selection MUST come from an explicit Python-owned temporal clock, never an ambient system clock in Rust, Wasm, or solver hot paths.
- Every run MUST declare whether it is evaluating:
  - current-time compliance
  - historical compliance
  - future scenario analysis
- Rule selection, pricing selection, and jurisdictional binding MUST all key off the same declared temporal clock for a given run unless the task artifact explicitly models multiple clocks.
- A run whose clock is implicit, inferred, or absent is invalid.

## 3. Snapshot Identity Rules
- Every committed run MUST have a stable snapshot identifier that can re-bind:
  - input project state
  - selected vault records and their versions
  - feature-flag state
  - solver configuration
  - kernel versions relevant to the run
- A snapshot identifier MUST be written before irreversible state changes or canonical export.
- Partial runs MAY emit provisional artifacts, but those artifacts MUST be marked provisional and MUST NOT be confused with committed outputs.

## 4. Audit Artifact Rules
- Every tool call, boundary crossing, solver invocation, concession step, and final commitment MUST be loggable in plain machine-readable form.
- Minimum audit fields are:
  - audit cursor or event id
  - timestamp in the declared audit-clock format
  - actor or subsystem
  - input artifact reference
  - output artifact reference
  - status
  - snapshot id
- Audit logs MUST distinguish between:
  - proposed
  - verified
  - rejected
  - human-overridden
  - rolled-back
- A human override without explicit provenance and justification is invalid.

## 5. Replay Rules
- A replay must be able to reconstruct the verdict using recorded artifacts alone.
- Replay artifacts MUST include enough information to re-run the same bounded solver queries and the same kernel computations under the same assumptions.
- A replay mismatch MUST be treated as a correctness incident until explained.
- Retroactive audits MUST be able to bind historical rule versions and price versions using the recorded temporal clock.

## 6. Mutation and Rollback Rules
- No committed geometry, rule selection, or optimization decision MAY become irreversible without an audit record that identifies the prior state and the new state.
- Rollback MUST be possible at the orchestration layer for any committed step that affects canonical state or accepted geometry.
- If a system cannot identify the exact state to roll back to, it is not ready to commit.

## 7. Stop Conditions
The Agent MUST stop and escalate if any of the following occur:
- a proposed result cannot be reproduced from explicit snapshot artifacts
- a proposed temporal decision depends on an ambient wall clock outside Python control
- a proposed output order depends on hash iteration or scheduler timing
- a proposed audit log omits actor, status, snapshot id, or artifact references
- a proposed human override lacks provenance or justification
- a proposed rollback path cannot identify the pre-commit state
- a proposed parallel path changes byte-level observable output

Escalation means stop, record the missing reproducibility or audit guarantee, and redesign.

## Cross-References
- Companion AEC_ENGINE files:
  - `01_COMPOUND_AI_OPERATING_CONTRACT.md` — overall determinism and audit obligations across layers
  - `04_KNOWLEDGE_VAULT_AND_RULE_AST_CONTRACT.md` — temporal fields and provenance at the vault layer
  - `05_MULTI_DISCIPLINARY_COORDINATION_RULES.md` — cascade logging, oscillation, and manual-override handling
  - `06_FORMAL_VERIFICATION_AND_Z3_PROTOCOL.md` — replayable proof artifacts and solver configuration
  - `07_BOUNDARY_TRANSLATION_PROTOCOL.md` — stable payload ordering and versioned schemas across boundaries
  - `09_PARETO_OPTIMIZATION_AND_FINANCIAL_LAYER_RULES.md` — temporal pricing inputs and ranking replay
- Related GOVERNANCE / RUST files:
  - `.ai/06_specs/GOVERNANCE/01_VALIDATION_PROTOCOL.md` — repo-wide validation layers
  - `.ai/06_specs/GOVERNANCE/05_TRUTH_GOVERNANCE_AND_PROMOTION_CONTRACT.md` — provenance and promotion discipline
  - `.ai/06_specs/RUST/03_RUST_SAFEGUARDS_AND_FAILURE_CONTAINMENT.md` — failure containment for deterministic kernels
  - `.ai/06_specs/RUST/05_RUST_TESTING_BENCHMARKING_AND_VALIDATION.md` — deterministic and differential validation expectations

## Final Rule
No replay, no trust. No audit trail, no commit.
