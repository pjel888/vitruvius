# Boundary Translation Protocol

## Purpose
This file defines the AEC-engine-specific translation rules for data crossing the Python, Rust, Wasm, IFC, and LLM-facing boundaries. It does not restate the repository-wide cross-language contract. Instead, it narrows that contract into enforceable air-lock rules for spatial DTOs, IFC interoperability, and deterministic payload translation inside the AEC engine.

## Scope
This file governs:
- IFC import and export air-locks
- Python DTOs that cross into Rust or Wasm
- Rust and Wasm result payloads that re-enter Python
- versioning and schema discipline for translation payloads
- unit, coordinate-frame, and tolerance declarations on translated data

This file does NOT govern:
- global language-boundary law — see `.ai/06_specs/GOVERNANCE/04_CROSS_LANGUAGE_BOUNDARY_CONTRACT.md`
- vault schema — see `04_KNOWLEDGE_VAULT_AND_RULE_AST_CONTRACT.md`
- formal verification semantics — see `06_FORMAL_VERIFICATION_AND_Z3_PROTOCOL.md`
- determinism and audit retention — see `08_DETERMINISM_TEMPORALITY_AND_AUDIT_RULES.md`

## Core Principle
Every boundary crossing is an air-lock: meaning is normalized before the crossing, and ambiguity is rejected at the door.

## 1. Governing Boundary Law
- `.ai/06_specs/GOVERNANCE/04_CROSS_LANGUAGE_BOUNDARY_CONTRACT.md` is the higher-order law for all cross-language boundaries in Vitruvius.
- This file MUST NOT be used to weaken or override the GOVERNANCE boundary contract.
- Where this file is more specific, it specializes the AEC-engine payload shape only. Where there is conflict, GOVERNANCE wins.

## 2. Canonical Translation Objects
- Every Python-to-Rust or Python-to-Wasm request MUST use an explicit DTO with a versioned schema identifier.
- DTOs MUST carry:
  - schema version
  - units
  - coordinate frame
  - tolerance policy identifier
  - deterministic ordering expectations where arrays or sets are present
- DTOs MUST NOT carry free-form dictionaries, arbitrary metadata blobs, or hidden optional semantics in hot paths.
- A payload whose meaning depends on field absence rather than an explicit enum or status field is invalid.

## 3. IFC Air-Lock Rules

### 3.1 Import
- IFC files MUST enter through a Python-side import air-lock that parses, validates, and normalizes them before any compute kernel sees the data.
- IFC semantics such as type hierarchy, property sets, and vendor-specific metadata MUST remain in Python-side metadata structures unless a task artifact explicitly proves a compute need.
- Rust kernels MUST receive normalized geometry and compact identifiers, not raw IFC object graphs.
- Imported IFC geometry MUST be stamped with units, coordinate frame, origin policy, and source object identifiers before translation completes.

### 3.2 Export
- Rust kernels MUST NOT emit IFC directly.
- Python owns IFC export assembly, mapping internal results back into IFC entities only after verification and audit stamping.
- Export payloads MUST identify whether geometry is provisional, verified, or human-overridden. Unverified geometry MUST NOT be exported as if it were canonical.

## 4. Python ↔ Rust Translation Rules
- Python MUST validate every request payload before crossing into Rust.
- Rust-facing payloads MUST be numerically compact, unit-explicit, and free of legal prose, pricing data, jurisdiction labels, and vault AST fragments.
- Rust MUST return structured machine data only: arrays, scalars, compact result structs, status enums, and explicit error codes.
- Rust result arrays whose order matters MUST define that order in the schema and preserve it deterministically.
- Python MUST translate Rust errors into orchestration-layer failures or audit events; it MUST NOT silently coerce malformed results into success.

## 5. Python ↔ Wasm Translation Rules
- Wasm is a deployment form of approved compute kernels, not a separate reasoning layer.
- Wasm payload schemas MUST match the Rust core contract unless an adapter layer is formally versioned and documented.
- Browser or edge host state MUST NOT silently alter units, tolerances, or coordinate assumptions.
- If a Wasm bridge requires JSON for transport, the JSON shape MUST still obey the same schema, ordering, and determinism rules as the native bridge.

## 6. LLM Boundary Minimization
- The LLM MUST see only the structured summary Python chooses to expose.
- Raw IFC, raw vault rows, raw solver clauses, and raw ECS internals MUST NOT be sent to the LLM.
- If the LLM is asked to produce a translation payload candidate, that candidate MUST pass the same schema validation as any other boundary input before it is accepted.

## 7. Versioning and Compatibility Rules
- Every boundary schema MUST have an explicit version identifier.
- Breaking schema changes MUST be versioned; silent field repurposing is forbidden.
- Backward-compatibility shims MUST live in Python orchestration, not in Rust hot paths.
- A task that changes a boundary schema MUST update the task artifact, validation evidence, and any affected cross-references in this pack.

## 8. Stop Conditions
The Agent MUST stop and escalate if any of the following occur:
- a proposal uses this file to weaken `.ai/06_specs/GOVERNANCE/04_CROSS_LANGUAGE_BOUNDARY_CONTRACT.md`
- a Python/Rust boundary would accept a free-form map, unversioned blob, or payload with implicit units
- a Rust kernel is asked to parse raw IFC, raw vault rows, or legal prose
- a Rust or Wasm payload includes pricing, jurisdiction, or provenance logic that belongs in Python
- an IFC export path bypasses solver verification or audit status
- a boundary schema changes without versioning and validation updates
- a host environment can change payload meaning without the schema reflecting it

Escalation means stop and redesign the boundary explicitly.

## Cross-References
- Companion AEC_ENGINE files:
  - `01_COMPOUND_AI_OPERATING_CONTRACT.md` — layer ownership and cross-layer data contracts
  - `02_ECS_AND_COMPONENT_DESIGN_RULES.md` — IFC metadata stays out of hot ECS paths
  - `03_SPATIAL_COMPREHENSION_PROTOCOL.md` — spatial outputs that later cross the IFC or Wasm boundary
  - `06_FORMAL_VERIFICATION_AND_Z3_PROTOCOL.md` — verification gate before translated results become accepted facts
  - `08_DETERMINISM_TEMPORALITY_AND_AUDIT_RULES.md` — deterministic ordering, audit cursor, and replay requirements on translated payloads
- Related GOVERNANCE / RUST files:
  - `.ai/06_specs/GOVERNANCE/04_CROSS_LANGUAGE_BOUNDARY_CONTRACT.md` — controlling law for all cross-language boundaries
  - `.ai/06_specs/GOVERNANCE/01_VALIDATION_PROTOCOL.md` — contract validation requirements for boundary payloads
  - `.ai/06_specs/RUST/04_RUST_ARCHITECTURE_AND_BOUNDARY_RULES.md` — Rust-side boundary discipline
  - `.ai/06_specs/RUST/05_RUST_TESTING_BENCHMARKING_AND_VALIDATION.md` — validation requirements for translated compute surfaces

## Final Rule
If a payload crosses a boundary carrying ambiguity, the bug already happened before the kernel ran.
