# Formal Verification and Z3 Protocol

## Purpose
This file defines the mandatory rules for turning AEC rule ASTs and spatial state into formal verification queries. It governs how Python compiles admissible constraints into Z3, how those queries must be decomposed, and what counts as a valid solver result. It exists to keep formal verification authoritative without letting the solver absorb interpretation, optimization, or orchestration work that belongs elsewhere.

## Scope
This file governs:
- the Python-side Z3 Inequality Compiler
- the admissible constraint shapes that may reach Z3
- decomposition of whole-project questions into bounded sub-problems
- sat / unsat result handling
- proof artifacts, witness artifacts, and unsat-core handling
- solver determinism and replay requirements

This file does NOT govern:
- rule authoring or vault storage shape — see `04_KNOWLEDGE_VAULT_AND_RULE_AST_CONTRACT.md`
- cross-language transport mechanics — see `07_BOUNDARY_TRANSLATION_PROTOCOL.md` and `.ai/06_specs/GOVERNANCE/04_CROSS_LANGUAGE_BOUNDARY_CONTRACT.md`
- audit-log retention and temporal replay policy — see `08_DETERMINISM_TEMPORALITY_AND_AUDIT_RULES.md`
- cost ranking or Pareto search — see `09_PARETO_OPTIMIZATION_AND_FINANCIAL_LAYER_RULES.md`
- low-level numeric kernels — see `.ai/06_specs/RUST/`

## Core Principle
Z3 adjudicates compiled constraints. It does not interpret law, search design space, or decide tradeoffs.

## 1. Solver Ownership Rules
- Python MUST be the only layer that constructs Z3 variables, assertions, solver scopes, and model queries.
- The LLM MUST NOT emit raw solver syntax, SMT-LIB fragments, or unconstrained symbolic expressions. It may request a tool call only.
- Rust MUST NOT construct or mutate Z3 formulas. Rust supplies deterministic numerics only.
- The vault MUST NOT store solver clauses, executable predicates, or pre-baked SMT fragments. It stores structured rule payloads that Python compiles.
- Z3 MUST receive only compiled constraints whose provenance can be traced back to a vault row, a project brief field, or a derived spatial fact already validated upstream.

## 2. Constraint Compilation Rules

### 2.1 Compiler Input Contract
- The compiler MUST accept only schema-valid AST nodes from the vault plus schema-valid project state from Python orchestration.
- Every compiled quantity MUST carry explicit units, coordinate frame, and tolerance semantics before it becomes a solver term.
- Ambiguous quantities MUST be rejected before compilation. The compiler MUST NOT guess whether a number is millimeters, meters, degrees, percent, or currency.
- A constraint derived from geometry MUST reference a deterministic geometric fact already computed outside the solver. Z3 proves compliance over facts; it does not replace collision kernels.

### 2.2 Compiler Output Contract
- Every compiled constraint MUST carry a stable identifier, source provenance, effective-date binding, and jurisdiction binding.
- Every compiled constraint MUST declare whether it is hard, soft, or advisory. Soft constraints MAY influence ranking, but they MUST NOT be merged into the hard-feasibility set silently.
- The compiler MUST emit machine-readable clause metadata so unsat cores can be mapped back to source rules and project entities.
- A compile step that drops provenance, units, or enforcement level is invalid and MUST fail closed.

### 2.3 Admissible Constraint Forms
- Hard-feasibility queries MUST be reduced to bounded arithmetic and logical predicates that the team can explain and replay.
- Non-linear or combinatorial encodings MAY be used only when the task artifact explicitly names the reason, the cost, and the termination bound.
- Quantifiers, recursion, and unconstrained symbolic growth MUST NOT be introduced casually. Their use requires an AD or a task-local escalation note that explains why a bounded decomposition was impossible.

## 3. Decomposition Rules
- Whole-building or whole-site questions MUST be decomposed by Python into bounded sub-problems before reaching Z3.
- Canonical decomposition axes are: jurisdiction, building, resolution level, floor, zone, discipline, and time slice.
- The solver MUST NOT receive an undifferentiated "entire project" query when a smaller bounded query can be formed.
- Decomposition boundaries MUST be recorded in the proof artifact so a replay can reconstruct the exact query partition.
- A later stage MAY aggregate sub-query results, but the aggregation step MUST remain outside Z3 unless it is itself modeled as a separate bounded query.

## 4. Result Semantics

### 4.1 SAT
- A satisfiable result MUST return a machine-readable witness that identifies the variable assignments or bounded facts that satisfied the query.
- The witness MUST be stored alongside the query identifier, solver version, and audit cursor.
- Python MAY translate the witness into user-facing prose, but the witness itself remains the source of truth.

### 4.2 UNSAT
- An unsatisfiable result MUST produce an unsat core or equivalent minimal conflict set whenever the solver mode supports it.
- The unsat core MUST be traceable back to source constraint identifiers, not merely anonymous clauses.
- A compliance failure reported to the user MUST cite the relevant constraint identifiers and provenance references. Python may summarize; it may not invent reasons absent from the core.

### 4.3 UNKNOWN / TIMEOUT
- `unknown`, timeout, resource exhaustion, or non-termination MUST be treated as non-verification, not as success.
- A solver run that does not produce SAT or UNSAT within the configured bound MUST be escalated or retried under a documented fallback policy.
- Python MUST surface the bound hit explicitly in the audit record and user-facing status.

## 5. Determinism and Replay Rules
- Solver configuration MUST be pinned per task artifact: solver version, tactic selection, timeout, seed, and decomposition strategy.
- If randomness is used anywhere in solver orchestration, the seed MUST be explicit, logged, and replayable.
- The same snapshot, same compiled constraints, and same solver configuration MUST yield the same verdict artifact.
- Proof artifacts MUST be written in a stable, machine-readable form suitable for replay and diffing.
- A solver run that cannot be replayed from recorded artifacts is incomplete.

## 6. Boundary Rules
- Verification sits after rule selection and before optimization. A design option that is not solver-feasible MUST NOT enter Pareto ranking.
- Pricing, ROI, or schedule objectives MUST NOT alter the hard-feasibility verdict. They rank feasible options only.
- The LLM may request verification and explain results, but it MUST NOT post-process a failed verdict into an approval.
- Rust MAY provide geometry-derived facts to Python, but Python MUST decide which facts become constraints and how they are labeled in the solver.

## 7. Stop Conditions
The Agent MUST stop and escalate if any of the following occur:
- a proposed change asks Z3 to parse raw legal text, raw LLM output, or raw vault JSON directly
- a proposed change uses Z3 as a search engine or optimizer instead of a verifier
- a proposed query cannot state its units, coordinate frame, tolerance policy, or provenance
- a proposed whole-project query cannot be decomposed into bounded sub-problems
- a proposed result path treats `unknown` or timeout as equivalent to `sat`
- a proposed unsat result cannot be mapped back to source constraint identifiers
- a proposed solver configuration is non-replayable or depends on ambient machine state
- a proposed optimization objective modifies the hard-feasibility set

Escalation means stop, document the unresolved point, and request an AD or task-local redesign.

## Cross-References
- Companion AEC_ENGINE files:
  - `01_COMPOUND_AI_OPERATING_CONTRACT.md` — five-layer contract and Z3 ownership boundary
  - `04_KNOWLEDGE_VAULT_AND_RULE_AST_CONTRACT.md` — AST and provenance inputs to the compiler
  - `05_MULTI_DISCIPLINARY_COORDINATION_RULES.md` — concession verification and infeasibility handling
  - `07_BOUNDARY_TRANSLATION_PROTOCOL.md` — boundary DTO rules for inputs and outputs crossing Python/Rust/Wasm
  - `08_DETERMINISM_TEMPORALITY_AND_AUDIT_RULES.md` — proof-artifact retention, replay, and temporal audit clock
  - `09_PARETO_OPTIMIZATION_AND_FINANCIAL_LAYER_RULES.md` — optimization happens only after hard-feasibility is proven
- Related GOVERNANCE / RUST files:
  - `.ai/06_specs/GOVERNANCE/04_CROSS_LANGUAGE_BOUNDARY_CONTRACT.md` — global cross-language law
  - `.ai/06_specs/GOVERNANCE/05_TRUTH_GOVERNANCE_AND_PROMOTION_CONTRACT.md` — truth-admission discipline for solver-backed claims
  - `.ai/06_specs/RUST/04_RUST_ARCHITECTURE_AND_BOUNDARY_RULES.md` — Rust MUST stay out of formal-law interpretation
  - `.ai/06_specs/RUST/05_RUST_TESTING_BENCHMARKING_AND_VALIDATION.md` — validation discipline for kernel facts that feed the solver

## Final Rule
The solver may prove or disprove a bounded claim. It may not decide what the claim means.
