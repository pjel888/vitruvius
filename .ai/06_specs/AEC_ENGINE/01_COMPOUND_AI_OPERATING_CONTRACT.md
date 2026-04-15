# Compound AI Operating Contract

## Purpose
This file defines the non-negotiable behavioral contract that any AI coding agent (Claude Code, Codex, etc.) and any human engineer MUST follow whenever working on the Vitruvius AEC Engine. It is the most authoritative file in the AEC_ENGINE pack because every other file in the pack builds on the five-layer separation declared here. If a downstream file or an ad-hoc decision conflicts with a rule in this file, this file wins. Where this document says "the Agent", it means whichever AI agent is currently editing the engine.

## Scope
This file governs:
- layer ownership across LLM, Python, Rust, RocksDB, and Z3
- tool-call and schema discipline
- cross-layer responsibility boundaries
- escalation rules when a change cannot fit inside the declared architecture

This file does NOT govern:
- the details of ECS design inside the Rust layer — see `02_ECS_AND_COMPONENT_DESIGN_RULES.md`
- vault payload schema specifics — see `04_KNOWLEDGE_VAULT_AND_RULE_AST_CONTRACT.md`
- solver workflow specifics — see `06_FORMAL_VERIFICATION_AND_Z3_PROTOCOL.md`
- translation DTO specifics — see `07_BOUNDARY_TRANSLATION_PROTOCOL.md`
- project-wide cross-language law — see `.ai/06_specs/GOVERNANCE/04_CROSS_LANGUAGE_BOUNDARY_CONTRACT.md`

## Core Principle
Each layer must be structurally incapable of owning the wrong kind of truth.

## Identity of the Compound AI System
The Vitruvius AEC engine is a **Compound AI System** composed of five strictly separated layers. Each layer has a single role. No layer is permitted to absorb the role of another.

- **LLM** — *Mouth and Ears*. Translates English into structured JSON tool calls and translates structured JSON results back into English.
- **Python** — *Logic / Orchestrator*. Routes requests, fetches rule ASTs from the vault, compiles ASTs into Z3 constraints, dispatches to Rust kernels, runs the Pricing Oracle, owns tool dispatch and schema validation.
- **Rust** — *Physics Kernel*. Deterministic compiled kernels for spatial indexing, collision, pathfinding, voxel CSG, ECS systems, and engineering solvers. Owns no law.
- **RocksDB** — *Rule Vault*. Append-only temporal store of versioned legal ASTs, jurisdictional parameters, and pricing data. Stores strict JSON only.
- **Z3** — *Adjudicator*. Formal verification of whether a proposed configuration satisfies all active constraints. Produces sat witnesses or unsat cores.

These five layers are the only layers the Agent may reason about. Introducing a sixth layer, merging two layers, or moving a responsibility across a boundary is forbidden unless an AD explicitly authorizes it.

## Codex Must Assume
1. The five-layer separation is not a coding style; it is a correctness property. Violating it is a correctness bug, not a taste issue.
2. A compiling change that crosses a layer boundary may still be architecturally wrong, even if every test passes.
3. A passing test suite does not prove boundary compliance. Boundary compliance is proved by explicit layer-impact analysis and by the schemas that guard every cross-layer call.
4. The LLM is not trusted to compute, adjudicate, or interpret law. It is a translator. Anything else it appears to do is a leak, even when the answer happens to be correct.
5. The Rust layer has no knowledge of legal rules, pricing, or jurisdictions. If a Rust change requires such knowledge, the change is wrong — the rule MUST stay in the vault and Python MUST compile it down to numerics before crossing into Rust.
6. The RocksDB vault holds only JSON. Any proposal to store executable code (Python, Rust, JavaScript, grammars that are executed, lambdas, pickles, shell commands, `eval`-able strings) in the vault is an immediate escalation.
7. Determinism is the default below the Python layer. Any non-determinism below Python is a defect unless an AD explicitly authorizes it and documents its containment.
8. Every cross-layer call is a contract. Undocumented contracts are latent defects waiting to be triggered by the next change.

## Codex Must Read First
Before touching any layer of the AEC engine, the Agent MUST read these files in this order:
1. `.ai/06_specs/AEC_ENGINE/00_README_AEC_ENGINE_DOC_SET.md` (scope, authority order, pack identity)
2. `.ai/06_specs/AEC_ENGINE/01_COMPOUND_AI_OPERATING_CONTRACT.md` (this file)
3. The other AEC_ENGINE files whose scope the change touches (see the Cross-References section below)
4. `.ai/06_specs/RUST/01_RUST_OPERATING_CONTRACT_FOR_CODEX.md` (if the change touches Rust)
5. `.ai/06_specs/RUST/04_RUST_ARCHITECTURE_AND_BOUNDARY_RULES.md` (if the change crosses the Python/Rust boundary)
6. `.ai/06_specs/GOVERNANCE/04_CROSS_LANGUAGE_BOUNDARY_CONTRACT.md`
7. `.ai/13_research/AEC-ECS-SC_RESEARCH.md` sections §1.2, §1.3, §4.4, §5 (the canonical research source for this pack)
8. `.ai/10_state/decisions.md` (the AD ledger — at minimum any AD that touches the layer being modified)
9. `.ai/00_system/EXECUTION_LOOP.md` and `.ai/00_system/principles.md`

## Absolute Separation Rules
These rules are the core of the contract. They are written MUST / MUST NOT because they are enforceable, not aspirational.

### 1. LLM — Mouth and Ears
- The LLM MUST only emit structured tool calls conforming to a Python-side JSON schema.
- The LLM MUST only receive structured JSON results from Python and convert them into natural language.
- The LLM MUST NOT compute clearances, distances, areas, volumes, loads, flows, costs, or any other numeric quantity.
- The LLM MUST NOT answer a spatial, legal, cost, or compliance question directly. It MUST route the question through a tool call.
- The LLM MUST NOT invent a tool that is not in the Python-side tool catalog.
- The LLM MUST NOT receive raw geometry, raw ECS state, or raw vault rows. It only receives the structured result Python chose to expose.
- Local LLMs (Gemma, Llama, Qwen, Mistral, Phi) MUST be wrapped in constrained generation (Outlines, llama.cpp GBNF grammars, or equivalent) so schema adherence is enforced at decode time, not prayed for.
- **Canonical rule: the LLM cannot hallucinate a clearance because it is never asked to compute one.**

### 2. Python — The Orchestrator
- Python MUST own all tool dispatch. Every LLM tool call is validated against its JSON schema before Python acts on it.
- Python MUST be the only layer that reads RocksDB rule ASTs and the only layer that compiles them into Z3 constraints.
- Python MUST be the only layer that calls into Rust kernels. No other layer may hold a PyO3 handle or a kernel entry point.
- Python MUST convert rule ASTs into pure numerics before any call into Rust. Rust MUST NOT see an AST.
- Python MUST own the Pricing Oracle, the temporal clock, the jurisdictional binding, and the tool-call router.
- Python MUST NOT compute collision, pathfinding, voxel CSG, FEA, fluid dynamics, or any hot geometric/numeric kernel that falls below the AD-036 Rust Line. Those belong in Rust.
- Python MUST NOT embed hard-coded legal constants. Legal constants live in the vault and arrive via AST, never as Python literals.
- Python MUST NOT pass raw LLM output to any downstream layer without schema validation.

### 3. Rust — The Physics Kernel
- Rust MUST be deterministic. Given the same inputs, the same kernel build MUST produce bit-identical outputs.
- Rust MUST only accept validated numeric inputs from Python across the PyO3 shim.
- Rust MUST return structured numeric results (arrays, scalars, indices, flags) — never prose, never LLM-facing strings, never rule interpretations.
- Rust MUST NOT read RocksDB directly. Rules do not live in Rust.
- Rust MUST NOT embed legal parameters, jurisdictional values, or pricing constants in source. Those arrive as function arguments compiled by Python.
- Rust MUST NOT call into the LLM, the Pricing Oracle, or any orchestration layer.
- Rust MUST NOT introduce non-determinism (hash-map iteration order, threading races, uninitialized memory, system clock reads) in any code path whose output crosses the boundary.
- **Canonical rule: Rust cannot bend a rule because rules are not in Rust.**

### 4. RocksDB — The Rule Vault
- The vault MUST store only strict JSON payloads conforming to the AST schema defined in `04_KNOWLEDGE_VAULT_AND_RULE_AST_CONTRACT.md`.
- The vault MUST be append-only and temporally versioned. Historical snapshots MUST remain queryable.
- The vault MUST NOT contain executable code of any kind — no Python scripts, no Rust functions, no JavaScript, no lambdas, no pickles, no shell commands, no grammars that are executed, no `eval`-able strings.
- The vault MUST NOT be written to directly by the LLM. The LLM ingestion pipeline emits JSON; Python validates the JSON against the schema; only validated JSON reaches the vault.
- The vault MUST NOT be read by Rust. Rust sees compiled numerics, not vault rows.
- Every vault write MUST carry provenance (source document, jurisdiction, effective date, confidence, ingest timestamp) per the AST contract in `04`.
- **Canonical rule: never store raw executable code inside the RocksDB vault. Rules live in the vault as strict JSON, never as code.**

### 5. Z3 — The Adjudicator
- Z3 MUST be reached only through the Z3 Inequality Compiler in Python (see `06_FORMAL_VERIFICATION_AND_Z3_PROTOCOL.md`).
- Z3 MUST receive only compiled constraint expressions. It MUST NOT parse raw legal text, raw ASTs, or raw LLM output.
- Z3 MUST return machine-readable results — a sat witness (variable assignment) or an unsat core (the minimal conflicting constraint set) — never a natural-language explanation.
- Z3 MUST be called on bounded, decomposed sub-queries. Whole-building queries MUST be decomposed by Python into per-floor, per-zone, or per-discipline sub-problems before reaching Z3.
- Z3 MUST NOT be used as a general-purpose search engine or optimizer. Optimization lives above the verification layer; Z3 verifies, it does not search.
- **Canonical rule: Z3 answers small questions, not whole-building questions.**

## Tool Call Discipline
1. Every LLM tool call MUST be validated against a Python-owned JSON schema before Python acts on it. Unvalidated tool calls MUST be rejected, not "best-effort parsed".
2. The tool surface MUST be small, well-typed, well-documented, and composable. Each tool MUST do exactly one thing; composition happens by the LLM chaining tool calls, not by omnibus tools that fan out internally.
3. Tool catalog additions MUST go through the same review bar as layer boundary changes. New tools are new boundary contracts and MUST be registered in the file in this pack that governs the responsibility they touch.
4. Local / untrusted LLMs MUST use constrained generation (Outlines, llama.cpp GBNF grammars, Guidance, or equivalent). Free-form JSON prompting is forbidden for vault ingestion and for any tool call that mutates state.
5. The LLM MUST NOT be given a "free text" escape hatch that bypasses the tool schema. Any natural-language answer the LLM produces is downstream of a structured tool result, not a substitute for one.
6. Tool results returned to the LLM MUST be the same structured JSON Python handed to the tool consumer. The LLM MUST NOT be fed raw kernel outputs, raw vault rows, or raw Z3 models.
7. Tool-call retries on validation failure MUST be bounded and MUST feed the schema error back as a corrective message; unbounded retry loops are forbidden.
8. Every tool call and every tool result MUST be loggable in plain JSON for audit reproducibility (see `08_DETERMINISM_TEMPORALITY_AND_AUDIT_RULES.md`).

## Cross-Layer Data Contracts
1. Every cross-layer call MUST be guarded by a schema. No boundary may be crossed without one.
2. **LLM → Python:** JSON tool call validated against the tool's JSON schema. No free text, no positional args, no implicit coercions.
3. **Python → RocksDB:** structured AST payload validated against the AST JSON schema in `04_KNOWLEDGE_VAULT_AND_RULE_AST_CONTRACT.md`. Writes MUST carry provenance.
4. **RocksDB → Python:** AST JSON read-through a deserializer that fails loudly on schema drift. No partial / best-effort parses.
5. **Python → Rust:** validated numerics only — fixed-width types, explicit units, documented coordinate frame, explicit tolerance policy. The AST MUST have been compiled to numerics by Python before the call.
6. **Rust → Python:** structured numeric results (arrays, scalars, indices, flags, status enums). No prose. No rule interpretations. No hidden state.
7. **Python → Z3:** compiled Z3 expressions from the Inequality Compiler. No raw strings, no eval-derived expressions.
8. **Z3 → Python:** sat witness or unsat core only. Python maps these back into tool results.
9. Every boundary MUST document its inputs, outputs, units, coordinate frame, tolerance policy, and invalid-state behavior. Undocumented boundaries are defects.
10. Nothing crosses a boundary without a schema. "Just this once" is not permitted.

## Codex Must Not
- blur layer responsibilities, even in prototype or demo code
- let the LLM compute, adjudicate, or invent numeric quantities
- let the LLM pick which rule applies — jurisdictional binding is a Python responsibility, not an LLM one
- absorb legal parameters into Python source, Rust source, or hard-coded constants
- store executable code (Python, Rust, JavaScript, grammars, lambdas, pickles, shell commands) inside the RocksDB vault under any circumstances
- allow Rust to read from RocksDB directly
- allow Rust to call into the LLM, the Pricing Oracle, or any orchestration layer
- pass raw LLM output to a downstream layer without schema validation
- hand Z3 whole-building queries instead of decomposed sub-queries
- use Z3 as a search engine or optimizer (optimization lives above verification)
- introduce non-determinism below the Python layer (hash-map iteration order, thread races, system-clock reads in hot paths)
- add a new tool, boundary, or schema without an AD and without the file in this pack that governs it
- rely on an LLM's schema adherence without constrained generation for untrusted / local models
- bypass the tool schema by routing LLM text directly into a mutation path
- treat "just this once" as a valid justification for crossing a boundary without a schema
- collapse two layers into one because a prototype "only needs one of them"
- claim boundary compliance without explicit layer-impact analysis

## Escalation Conditions
The Agent MUST stop and escalate if any of the following occur:
- a proposed change requires the LLM to compute or adjudicate a quantity
- a proposed change requires Rust to know a legal rule, a jurisdictional constant, or a price
- a proposed change requires storing executable code inside the RocksDB vault
- a proposed change requires Rust to read RocksDB directly
- a proposed change requires bypassing the JSON schema on any boundary
- a proposed change requires handing Z3 a whole-building query
- a proposed change requires non-determinism below the Python layer
- the tool catalog must grow to accommodate a single change and no AD authorizes the growth
- two files in this pack disagree about layer responsibility
- the change cannot be expressed without blurring a layer boundary

Escalation means stop, write the conflict down, and request an AD. It does not mean "work around it".

## Completion Standard
Work that touches this contract is not complete until ALL of the following hold:
1. Explicit layer-impact analysis exists: every affected layer is named and the responsibility of each is shown to be inside its contract.
2. Every new or modified boundary has a JSON schema checked into the repository and referenced from the call site.
3. Every new or modified cross-layer call is documented with inputs, outputs, units, coordinate frame, tolerance policy, and invalid-state behavior.
4. Every new tool added to the LLM tool catalog has a schema, a validator, a test, and a docstring.
5. Constrained generation is in place for any local / untrusted model reachable through the change.
6. Determinism below the Python layer is preserved. Any new non-determinism carries an AD.
7. No executable code has been added to RocksDB. The vault diff, if any, is JSON only.
8. The Rust layer, if touched, still owns no law.
9. The change is traceable in the audit log (see `08_DETERMINISM_TEMPORALITY_AND_AUDIT_RULES.md`).
10. An AD is appended to `.ai/10_state/decisions.md` when the change modifies a boundary, a tool schema, or the layer responsibility map.

## Cross-References
- **Research paper** (`/.ai/13_research/AEC-ECS-SC_RESEARCH.md`):
  - §1.2 The Compound AI System Pattern
  - §1.3 Determinism as the Default
  - §4.4 The Absolute Rule — No Code in the Database
  - §5 The Compound AI System (full section — roles, tool calling, Z3 compiler, local LLM considerations)
- **Companion AEC_ENGINE files:**
  - `02_ECS_AND_COMPONENT_DESIGN_RULES.md` — ECS archetypes and component traps inside the Rust Physics layer
  - `03_SPATIAL_COMPREHENSION_PROTOCOL.md` — voxel CSG, heightmap, and the 3-layer spatial stack
  - `04_KNOWLEDGE_VAULT_AND_RULE_AST_CONTRACT.md` — RocksDB schema, 4-block JSON, LLM ingestion discipline
  - `05_MULTI_DISCIPLINARY_COORDINATION_RULES.md` — hierarchy of precedence, negotiation protocol, feedback loop
  - `06_FORMAL_VERIFICATION_AND_Z3_PROTOCOL.md` — Z3 Inequality Compiler, decomposition rules
  - `07_BOUNDARY_TRANSLATION_PROTOCOL.md` — IFC air-lock, Wasm, PyO3 boundary discipline
  - `08_DETERMINISM_TEMPORALITY_AND_AUDIT_RULES.md` — reproducibility, retroactive audits, temporal clock
  - `09_PARETO_OPTIMIZATION_AND_FINANCIAL_LAYER_RULES.md` — Pricing Oracle, Pareto frontier, optimization above the verification layer
  - `10_AEC_ENGINE_TASK_TEMPLATE.md` — cross-layer task template
- **Related RUST / GOVERNANCE pack files:**
  - `.ai/06_specs/RUST/01_RUST_OPERATING_CONTRACT_FOR_CODEX.md` — Rust-layer behavioral contract
  - `.ai/06_specs/RUST/04_RUST_ARCHITECTURE_AND_BOUNDARY_RULES.md` — Rust-side boundary rules
  - `.ai/06_specs/GOVERNANCE/04_CROSS_LANGUAGE_BOUNDARY_CONTRACT.md` — project-level cross-language boundary discipline

## Final Rule
Each layer is structurally incapable of the failure modes that plague monolithic systems. Keep it that way.
