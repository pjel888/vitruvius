# Vitruvius AEC Engine Governance Pack

## Purpose
This document set defines the mandatory architectural contracts, boundary rules, and enforcement protocols for the next-phase Vitruvius AEC Constraint Engine — the Compound AI System that fuses an ECS-based spatial kernel, a versioned knowledge vault of legal and physical rules, a formal verification layer, and a Python orchestration plane into a mathematically rigorous, deterministic engine for the built environment.

This pack exists to make next-phase AEC engine implementation:
- architecturally bounded
- deterministic
- auditable
- formally verifiable
- scale-agnostic (fractal)
- resistant to hallucination by the LLM
- resistant to hidden coupling between layers
- resistant to drift from the five-layer Compound AI contract
- resistant to the quiet absorption of law, policy, or business logic into the wrong layer

## Intended Audience
- Codex and other AI coding agents
- human reviewers
- future Vitruvius AEC engine engineers
- technical founders supervising AI-assisted implementation

## Scope
This pack governs the **AEC engine architecture** — the contract between the LLM, Python orchestrator, Rust kernels, RocksDB vault, and Z3 adjudicator, plus the domain rules that keep the engine deterministic, auditable, and boundary-safe.

This pack does **not** govern:
- Rust implementation discipline (see `.ai/06_specs/RUST/`)
- Project-level validation, truth promotion, and cross-language contracts (see `.ai/06_specs/GOVERNANCE/`)
- Concrete engineering kernel math — Euler-Bernoulli, Hazen-Williams, Manning, voltage drop formulas, etc. (those are per-kernel specs, written against the RUST pack task template)
- Use cases, feature roadmaps, sprint plans (see `.ai/03_plans/`)
- Open research questions and surveys (see `.ai/13_research/`)

## Document Order of Authority
1. `01_COMPOUND_AI_OPERATING_CONTRACT.md`
2. `02_ECS_AND_COMPONENT_DESIGN_RULES.md`
3. `03_SPATIAL_COMPREHENSION_PROTOCOL.md`
4. `04_KNOWLEDGE_VAULT_AND_RULE_AST_CONTRACT.md`
5. `05_MULTI_DISCIPLINARY_COORDINATION_RULES.md`
6. `06_FORMAL_VERIFICATION_AND_Z3_PROTOCOL.md`
7. `07_BOUNDARY_TRANSLATION_PROTOCOL.md`
8. `08_DETERMINISM_TEMPORALITY_AND_AUDIT_RULES.md`
9. `09_PARETO_OPTIMIZATION_AND_FINANCIAL_LAYER_RULES.md`
10. `10_AEC_ENGINE_TASK_TEMPLATE.md`

If any lower document conflicts with a higher document, the higher document wins.

## Authority Relative to Other Packs
- **`GOVERNANCE/` > `AEC_ENGINE/`** — project-level standards (validation, truth promotion, cross-language boundary contract, performance budget) override AEC engine architectural rules when they disagree.
- **`AEC_ENGINE/` > `RUST/`** — domain-level architectural rules override Rust-language rules when they disagree, because architectural correctness is prior to implementation style.
- **`AEC_ENGINE/` complements `RUST/`** — this pack tells the codebase AI *what* to build and *how* the layers must interact; the RUST pack tells it *how* to write the Rust correctly inside its assigned scope.

## Core Principle
Geometry is a derivative of physics and law.

The Vitruvius AEC engine does not draw buildings. It solves constraint systems and emits geometry as a byproduct of satisfiability. Every architectural decision in this pack flows from that inversion. The engine is structurally incapable of hallucinating physics or law because no single layer has both the authority and the capability to invent them.

## The Five-Layer Compound AI System
- **The LLM** — Mouth and Ears. Translates English to structured tool calls and structured results back to English. Never computes. Never adjudicates.
- **Python** — Logic. Orchestrates, fetches rules from the vault, compiles ASTs into Z3 constraints, dispatches to Rust kernels, runs the Pricing Oracle, handles LLM tool routing.
- **Rust** — Physics. Deterministic compiled kernels for collision detection, spatial indexing, pathfinding, voxel CSG, ECS systems, and engineering solvers. Owns no law.
- **RocksDB** — Rules. Append-only temporal vault of versioned legal ASTs, jurisdictional parameters, pricing data. Stores JSON only — never executable code.
- **Z3** — Adjudicator. Formal verification of whether a proposed configuration satisfies all active constraints. Produces witnesses on failure, unsat cores on success.

This separation is strategic, not stylistic. Every file in this pack enforces one or more boundaries between these five layers.

## Required Operating Sequence
For every non-trivial next-phase AEC engine task:
1. Read the governing documents in this pack, top-down in order of authority.
2. Identify which of the five layers the change touches.
3. Identify which companion files in this pack are load-bearing for the change.
4. Produce or update the task pack using `10_AEC_ENGINE_TASK_TEMPLATE.md`.
5. Run a boundary contract check against `01_COMPOUND_AI_OPERATING_CONTRACT.md`.
6. Produce or update the implementation plan.
7. Produce a plan critique.
8. Implement in controlled slices.
9. Validate against the relevant file's Red-Line Conditions.
10. Write a validation report and update state documentation.

## Absolute Rule
No next-phase AEC engine change is complete until it has:
- explicit layer-impact analysis (which of LLM / Python / Rust / RocksDB / Z3 is affected)
- boundary contract proof (no layer has taken responsibility it must not have)
- deterministic reproducibility (same snapshot + same inputs → same output)
- temporal audit trail (the change and its source are recorded where needed)
- test coverage against the file-specific Red-Line Conditions
- architectural review against the order-of-authority stack above

## Recommended Repo Placement
This pack lives at `.ai/06_specs/AEC_ENGINE/` as a sibling to `.ai/06_specs/RUST/` and `.ai/06_specs/GOVERNANCE/`.

## Suggested Companion Files Outside This Pack
These documents should be used alongside this pack:
- `.ai/00_system/EXECUTION_LOOP.md`
- `.ai/00_system/principles.md`
- `.ai/00_system/architecture.md`
- `.ai/01_roadmap/current-phase.md`
- `.ai/01_roadmap/master-roadmap.md`
- `.ai/01_roadmap/milestone-tracker.md`
- `.ai/10_state/decisions.md`
- `.ai/06_specs/RUST/*`
- `.ai/06_specs/GOVERNANCE/*`
- `.ai/13_research/AEC-ECS-SC_RESEARCH.md` (the consolidated research source for this pack)

## Cross-References
- `AGENTS.md` — root operating contract for all work in the repository
- `.ai/00_system/EXECUTION_LOOP.md` — mandatory execution lifecycle for non-trivial work
- `.ai/06_specs/GOVERNANCE/` — project-level law for validation, truth governance, performance policy, and cross-language boundaries
- `.ai/06_specs/RUST/` — implementation law for any Rust-side execution of this architecture
- `.ai/13_research/AEC-ECS-SC_RESEARCH.md` — canonical research source that motivated this pack
- `.ai/10_state/decisions.md` — append-only AD ledger for any boundary or capability change driven by this pack

## Final Rule
No single layer of the Compound AI System has both the authority and the capability to hallucinate physics or law.
This pack exists to keep it that way.
