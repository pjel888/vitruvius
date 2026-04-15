# Vitruvius Cross-Language Boundary Contract

## Purpose
This document defines the boundaries, responsibilities, and allowed interactions among the major language and execution layers in Vitruvius.

Vitruvius is intentionally multi-layered. That is a strength only if the boundaries remain clean. If the boundaries blur, the system becomes harder to reason about, harder to validate, and easier for agents to corrupt accidentally.

## Core Principle
Each layer must be structurally incapable of owning the wrong kind of truth.

## Primary Layers
- LLM layer
- Python orchestration layer
- Rust compute layer
- RocksDB / rule-vault layer
- Z3 / formal adjudication layer
- optional Wasm-hosted compute deployment layer

---

## Section 1 — Layer Responsibilities

### LLM Layer
#### Role
- translate natural language into structured requests
- translate structured outputs into natural language responses
- assist with constrained extraction into schemas when explicitly permitted

#### Must Not Own
- final physics
- final legal truth
- direct numeric judgment
- hidden orchestration state
- canonical truth promotion authority

#### Rule
The LLM may speak. It may not decide truth by itself.

---

### Python Layer
#### Role
- orchestration
- routing
- stateful workflow control
- schema and contract validation
- tool dispatch
- AST compilation
- Z3 query construction
- interaction between deterministic subsystems

#### Must Not Become
- the high-performance math layer
- a substitute for Rust in hot loops
- a dumping ground for uncontrolled logic
- a vague reimplementation of law

#### Rule
Python owns coordination, not heavy deterministic physics.

---

### Rust Layer
#### Role
- deterministic computation
- geometry kernels
- spatial indexing
- ECS systems
- high-frequency or numerically sensitive routines
- Wasm-compatible compute kernels
- narrow FFI or PyO3 compute surfaces

#### Must Not Own
- orchestration
- free-form policy logic
- legal interpretation
- repo workflow control
- canonical truth governance as system law

#### Rule
Rust owns physics and compute, not business or legal meaning.

---

### RocksDB / Rule Vault Layer
#### Role
- versioned rule storage
- temporal rule history
- structured payload persistence
- provenance-carrying rule records
- append-oriented data storage for rule-like content

#### Must Not Own
- executable code
- hidden orchestration
- direct runtime decision logic
- silent mutation of truth

#### Rule
The vault stores structured rule payloads, not executable behavior.

---

### Z3 Layer
#### Role
- formal constraint adjudication
- satisfiability or violation witness generation
- arithmetic and logical constraint reasoning where modeled

#### Must Not Own
- source legal interpretation
- user-facing explanation without orchestration
- heavy geometric primitives beyond what is compiled into constraints

#### Rule
Z3 adjudicates encoded constraints. It does not define the world by itself.

---

### Wasm Compute Layer
#### Role
- deployment form of selected Rust compute kernels
- deterministic browser-safe or edge-safe computation

#### Must Not Own
- rendering logic
- uncontrolled host-language policy logic
- JSON-heavy hot-loop communication if avoidable

#### Rule
Wasm is a deployment target for compute, not a new architecture layer with different truth.

---

## Section 2 — Allowed Data Flow

### LLM → Python
Allowed:
- structured tool requests
- extraction payload candidates under schema constraints
- user intent translated into machine-readable parameters

Not allowed:
- unconstrained hidden instructions altering system truth
- direct claims of compliance without deterministic backing

### Python → LLM
Allowed:
- structured results for explanation
- limited clarification prompts
- schema definitions for constrained extraction

Not allowed:
- delegation of final numerical or legal decision

---

### Python → RocksDB
Allowed:
- validated structured writes
- versioned payload storage
- rule retrieval
- terrain, cost, and metadata persistence where designed

Not allowed:
- storing raw executable code as system logic
- bypassing schema validation on truth-bearing payloads

---

### RocksDB → Python
Allowed:
- retrieval of structured payloads
- historical versions
- temporal scans
- compact machine-readable rule records

Not allowed:
- implicit execution
- hidden behavior outside schema

---

### Python → Rust
Allowed:
- validated numeric inputs
- compact structured compute requests
- compiled constraints or relevant parameters
- local-frame geometry payloads
- narrow FFI-safe data structures

Not allowed:
- loosely validated user payloads into hot kernels
- semantically overloaded dictionaries in performance-critical loops
- hidden unit assumptions
- hidden tolerance assumptions

---

### Rust → Python
Allowed:
- deterministic compute results
- structured error states
- violation or metric data
- compact geometry or routing outputs
- benchmark or diagnostic summaries where intentionally designed

Not allowed:
- direct legal prose conclusions
- user-facing free text as primary API
- mutation of rule-vault truth

---

### Python → Z3
Allowed:
- compiled constraints
- variable bindings
- bounded formal queries
- satisfiability checks

Not allowed:
- unconstrained giant symbolic worlds without reason
- implicit semantics not reflected in the AST or compiler

---

### Z3 → Python
Allowed:
- sat / unsat / unknown
- witnesses
- unsat cores
- diagnostic constraint information

Not allowed:
- direct user-facing explanatory authority without orchestration

---

## Section 3 — Boundary Data Requirements

Any payload crossing a major boundary should, where relevant, define:
- schema
- units
- coordinate frame
- numeric types
- error behavior
- tolerance policy
- ownership / lifetime expectations
- determinism expectations

If any of these are ambiguous, the payload is unsafe.

---

## Section 4 — FFI and PyO3 Rules

### Required
- narrow interfaces
- explicit conversions
- input validation before hot kernels
- stable, well-documented payload shapes
- minimal exposure of internal abstractions

### Forbidden
- exposing fragile internal ECS details casually
- passing semantically overloaded blobs
- leaking undefined lifetimes or ownership assumptions into the boundary contract

---

## Section 5 — Wasm Boundary Rules

### Required
- deterministic compute payloads
- typed arrays or compact binary structures where possible
- strict separation from rendering concerns
- explicit memory or serialization assumptions

### Avoid
- JSON-heavy hot paths
- browser-specific hacks becoming compute truth
- divergence between native Rust and Wasm semantics without documentation

---

## Section 6 — Truth Boundary Rules

### Rule A
No candidate knowledge becomes canonical merely because one layer produced it.

### Rule B
Every truth-bearing handoff must preserve provenance and review status.

### Rule C
No layer may silently upgrade candidate output into trusted truth.

### Rule D
If a layer does not own truth, it must not pretend to own truth.

---

## Section 7 — Boundary Violation Examples

### Bad Example 1
Rust begins storing business workflow flags or legal rule interpretations internally.

### Bad Example 2
Python starts hardcoding physics logic that should belong to Rust.

### Bad Example 3
The LLM directly answers compliance questions without tool-backed data.

### Bad Example 4
RocksDB stores executable scripts as rule behavior.

### Bad Example 5
PyO3 surface leaks unstable internal structs that were never meant to be public contract.

---

## Section 8 — Boundary Review Questions

Before accepting a cross-language change, ask:
- Did any layer absorb responsibilities that belong elsewhere?
- Did any payload become more ambiguous?
- Did validation weaken at the boundary?
- Did performance-sensitive data become over-serialized?
- Did canonical truth become easier to mutate silently?
- Did the public surface become broader than necessary?

---

## Section 9 — Change Control

Any change affecting these boundaries should usually be classified as at least:
- moderate
and often:
- architecture-affecting
- Rust-critical
- truth-critical
- performance-critical

Such changes require:
- explicit plan
- validation report
- state updates
- possibly decision-log update

---

## Final Principle
Boundary discipline is what keeps a complex system understandable.  
If the boundaries blur, trust and maintainability collapse together.
