# Multi-Disciplinary Coordination Rules

## Purpose
This file defines the mandatory rules that govern how Architecture, Structural, Mechanical / HVAC, Plumbing, and Electrical / Fire disciplines share a single 3D computational arena inside the Vitruvius AEC engine. It is the file that turns the combinatorial explosion of "all disciplines simultaneously" into a bounded, ordered, deterministic, auditable sequence of kernel calls. Every rule in this file exists to prevent the two canonical failure modes of multi-discipline coordination: silent clash acceptance and unbounded renegotiation cascades. Where this file conflicts with a lower file in the AEC_ENGINE pack, this file wins. Where it conflicts with `01_COMPOUND_AI_OPERATING_CONTRACT.md`, `01` wins.

## Scope
This pack file governs:
- the Hierarchy of Precedence between disciplines
- the automated Negotiation Protocol for clash resolution
- Hierarchical Lazy Evaluation across Resolution 1 / 2 / 3
- the Bi-Directional Feedback Loop that propagates pressure upward
- fractal scale-agnosticism at the Rust kernel level
- convergence and oscillation detection
- human escalation when the protocol cannot resolve

This file does NOT govern:
- ECS archetype or component design — see `02_ECS_AND_COMPONENT_DESIGN_RULES.md`
- spatial index internals, voxel CSG, heightmaps — see `03_SPATIAL_COMPREHENSION_PROTOCOL.md`
- vault AST format or rule authoring — see `04_KNOWLEDGE_VAULT_AND_RULE_AST_CONTRACT.md`
- Z3 compilation and witness / unsat core semantics — see `06_FORMAL_VERIFICATION_AND_Z3_PROTOCOL.md`
- audit trail, temporal clock, reproducibility — see `08_DETERMINISM_TEMPORALITY_AND_AUDIT_RULES.md`
- Pricing Oracle and Pareto optimization — see `09_PARETO_OPTIMIZATION_AND_FINANCIAL_LAYER_RULES.md`

## Core Principle
Disciplines are solved in strict order of physical inflexibility. The discipline that costs the most to relocate yields last. The Hierarchy of Precedence is the cost-of-relocation ranking made mechanical, and every rule in this file is a consequence of that ranking.

## The Shared Arena
- All disciplines MUST register their occupied volumes in a single Global BVH.
- The Global BVH is the only data structure through which disciplines communicate about space.
- The protocol of communication is the Hierarchy of Precedence and the Negotiation Protocol defined below.
- No discipline MAY maintain a private spatial index for its OWN volumes. The arena is shared, and private indices fork the truth.
- A discipline MAY maintain a discipline-local cache keyed to the Global BVH generation counter, but it MUST be invalidated whenever the counter advances.
- Every registration MUST carry the owning discipline, the occupancy class (`OCCUPIED_RIGID`, `OCCUPIED_SOFT`, `RESERVED`), and the resolution level at which it was registered.
- The BVH generation counter is the coordination clock. Stale reads across generations are a correctness defect, not a performance hiccup.

## The Hierarchy of Precedence

### Canonical Order
The canonical ranking from most inflexible to most flexible:

1. **Architecture — Bounds.** Legal envelope, vertical shafts, minimum clear ceiling heights, egress widths, fire compartmentation.
2. **Structural — Skeleton.** Column grid, beam spans, load paths, lateral bracing, shear walls.
3. **Mechanical / HVAC — Lungs.** Main duct runs, turning radii, large plenum volumes, air handling clearances.
4. **Plumbing — Veins.** Waste stacks with gravity slope constraints, vent stacks, supply risers.
5. **Electrical / Fire — Nerves.** Cable trays, conduits, sprinklers, low-voltage, data, fire detection.

### Order Rules
- The order reflects the cost of relocation. It is NOT arbitrary and MUST NOT be re-ranked to suit a specific project without a decision-log entry and an explicit AD.
- Architecture MUST lock the envelope before Structural begins.
- Structural MUST drop the grid before any MEP kernel routes.
- MEP disciplines MUST route into space remaining after the two higher-precedence disciplines have settled.
- The Rust kernel MUST NOT know this order. The Python orchestrator enforces it. The kernel only sees the volumes handed to it.
- Registrations MUST be emitted in order of precedence within a single Resolution step; out-of-order registration is a defect.
- The order MAY be paused at any point for a negotiation cascade, but MUST resume from the paused precedence level, never from the top, unless the cascade invalidated a higher level.
- A discipline MUST NOT pre-emptively reserve space it does not yet need. Precedence is spent, not hoarded.

## The Negotiation Protocol

### When to Trigger
- Any kernel that fails to find a feasible solution at its current precedence level MUST emit a `Constraint_Violation` signal to the Python orchestrator.
- The orchestrator MUST handle the violation; silent failure, best-effort placement, or ignoring the violation are all red-line conditions.
- Trigger conditions include: pathfinding with no legal path, clash with an `OCCUPIED_RIGID` volume, slope / clearance / radius budget exceeded, kernel returned `INFEASIBLE`.

### Escalation Sequence
- **Step 1.** The orchestrator asks the adjacent higher-precedence discipline for the smallest concession that would resolve the conflict. "Smallest" is measured by the discipline's local relaxation metric (e.g. duct aspect ratio delta, drop-ceiling delta, bay-width delta).
- **Step 2.** The concession is applied **transiently**, re-registered in the Global BVH under a pending generation, and re-verified against the knowledge vault through Z3. The concession is NOT committed until it passes verification.
- **Step 3.** If the concession fails vault verification or fails to resolve the downstream conflict, the orchestrator escalates to the next-higher discipline and repeats Step 1.
- **Step 4.** If no concession at any level resolves the conflict, the orchestrator MUST escalate upward to the Bi-Directional Feedback Loop defined below.
- **Step 5.** If the Bi-Directional Feedback Loop cannot resolve the conflict, the orchestrator MUST escalate to the human per the Human Escalation Rules below.

### Termination Conditions
- **Success.** The conflict is resolved within a bounded number of concession steps, the concession is committed to the Global BVH, and the audit trail records each step.
- **Infeasibility.** No valid configuration exists at any precedence level. The orchestrator MUST mark the sub-problem infeasible and escalate to the human.
- **Oscillation.** A state is revisited within a bounded window. The orchestrator MUST treat oscillation as infeasibility and escalate to the human.
- **Depth exceeded.** The cascade depth exceeds its configured bound. The orchestrator MUST terminate, mark the sub-problem unresolved, and escalate.

### Forbidden
- Silent clash acceptance.
- Concessions applied permanently before vault re-verification.
- Concessions that bypass the Z3 adjudicator.
- Concessions compiled from LLM output without schema validation.
- Concessions that modify a higher-precedence discipline without an explicit escalation event in the audit trail.
- Concessions that lose the pre-concession snapshot, preventing rollback.
- Pathfinding retries that relax clearance budgets below the vault-enforced minima.

## Hierarchical Lazy Evaluation

### Resolution 1 — Macro Envelope
- Scope: subdivision / site level.
- Buildings are represented as solid empty blocks.
- The optimizer optimizes for lot yield, road placement, legal setbacks, and ROI.
- Internal building structure MUST NOT be instantiated at Resolution 1.

### Resolution 2 — Core and Shell
- Scope: a single building block.
- Structural grid is placed. Vertical MEP shafts are placed. Core walls and elevator cores are placed.
- Buildings are represented as bounding boxes with internal shafts and a coarse structural grid.
- Floor-level routing MUST NOT be instantiated at Resolution 2.

### Resolution 3 — Micro Routing
- Scope: a single floor of a single building.
- Full ECS scene with every component of every discipline.
- A* pathfinding routes pipes, cables, ducts, and conduits through the available plenum.
- Full clash detection runs against the Global BVH at this resolution.

### Resolution Rules
- Each resolution MUST operate on its own abstraction level.
- Memory and compute MUST be spent only at the resolution currently under inspection. Holding full Resolution 3 scenes for every building in a Resolution 1 site is forbidden.
- The orchestrator MUST expose an explicit resolution promotion / demotion API. Implicit promotion (e.g. "fetch the floor plan to answer a subdivision question") is a defect.
- Promoting from a coarser resolution to a finer one MUST seed the finer resolution from the coarser one's committed state — never from raw LLM output and never from stale caches.
- Demoting from a finer resolution to a coarser one MUST distill the finer resolution into summary constraints (footprint, shaft envelope, pressure deltas) before the finer state is released.
- The resolution of every committed fact MUST be stamped in the audit trail so retroactive audits can reconstruct the coarse-to-fine cascade.

## The Bi-Directional Feedback Loop

### Pressure Signal Protocol
- When a kernel at Resolution N fails and no concession at Resolution N resolves the conflict, the orchestrator MUST emit a pressure signal upward to Resolution N-1.
- The pressure signal MUST carry: the failing kernel, the failed constraint, the quantitative delta required (e.g. "+15% shaft area", "+150 mm plenum depth"), and the current audit cursor.
- Resolution N-1 MUST receive the signal, re-optimize against the new delta, and re-emit a refreshed context to Resolution N.
- Resolution N MUST then re-attempt its computation against the refreshed context.
- If Resolution N-1 cannot accommodate the delta, it MUST in turn emit a pressure signal upward to Resolution N-2.

### Cascade Rules
- Every cascade MUST be bounded by a configured maximum depth. Unbounded cascades are a red-line condition.
- Every cascade step MUST be logged to the audit trail with source resolution, target resolution, failing kernel, delta, decision, and timestamp (see `08_DETERMINISM_TEMPORALITY_AND_AUDIT_RULES.md`).
- Every cascade step that alters a committed volume MUST be replayed against the Pricing Oracle and the financial layer (see `09_PARETO_OPTIMIZATION_AND_FINANCIAL_LAYER_RULES.md`). A millimeter change in a pipe is allowed to ripple upward into the ROI of the entire project — that is the feature, not a bug.
- Cascades MUST be fixed-point iterated. If a fixed point is not reached within the depth bound, the orchestrator MUST treat the cascade as non-convergent and escalate.
- Pressure signals MUST NOT be merged, averaged, or reordered. The order of signals is part of the audit record.

## Fractal Scale-Agnosticism Rule
- A plumbing pipe and a subdivision road are the same type at the Rust kernel level: a line with a radius.
- The Rust kernel MUST NOT contain a `Pipe` type, a `Road` type, a `Duct` type, a `Cable` type, or any other discipline-named geometry type. The geometry type is `LineWithRadius` (or the equivalent named in `02_ECS_AND_COMPONENT_DESIGN_RULES.md`).
- The same `aabb_intersects`, the same A*, the same capsule clash check, the same BVH query MUST apply at every scale, from a 0.05 m sprinkler line to a 5.0 m roadway centerline.
- Discipline labels MUST live in the `DomainDiscipline` component defined in file `02`, never in the geometry type.
- Any Rust type whose name implies a discipline is a defect and MUST be renamed or removed.
- The Rust kernel MUST NOT receive discipline names as function arguments or match on discipline strings. Discipline is a Python concern.
- Scale-agnosticism MUST be proved by differential test: the same kernel call applied at subdivision scale and at plumbing scale MUST produce structurally identical answers (modulo numeric scale), and the kernel MUST NOT branch on scale.

## Convergence and Oscillation Detection
- The Negotiation Protocol MUST detect oscillation by hashing the committed state at each step and checking for revisits within a configured window.
- The committed-state hash MUST include the generation counter, the set of registered volumes, and the set of active constraints at the current resolution.
- Monotone relaxation is the default strategy: each concession step MUST monotonically loosen the local constraint envelope relative to its starting point. Non-monotone steps are permitted only at resolution boundaries.
- Termination proofs MUST rely on the literature on iterative constraint relaxation with finite tile sets, under which convergence to a fixed point or to provable infeasibility is guaranteed.
- Any cascade that is not guaranteed to terminate under that literature MUST NOT be used.
- Unbounded cascade depth is a red-line condition. The depth bound MUST be configured, documented, and enforced by the orchestrator.
- Oscillation detection MUST NOT be disabled in production runs. A "temporarily disable oscillation detection" flag is forbidden.

## Human Escalation Rules
When the Negotiation Protocol and the Bi-Directional Feedback Loop cannot resolve:
- The full cascade history MUST be presented to the human: every pressure signal, every concession attempt, every rejection, every Z3 verdict, in chronological order.
- The failure mode MUST be classified as one of: `INFEASIBLE` (no valid configuration exists), `OSCILLATION` (state revisited within the window), `DEPTH_EXCEEDED` (cascade depth bound hit), `VAULT_REJECTED` (every concession was rejected by Z3 against the vault), `PRICING_REJECTED` (financial layer refused the concession).
- The human decision space MUST be: relax a constraint in the vault (with an AD), revise the brief, reject the project, or accept a manual override (which itself MUST be recorded in the audit trail with provenance and justification).
- Silent failure is forbidden. A run that cannot resolve MUST either reach a human or raise a loud orchestrator error. It MUST NOT return a plausible-looking but unverified configuration.
- Manual overrides MUST carry the same audit provenance as any other committed fact, and they MUST be flagged in the audit trail as `HUMAN_OVERRIDE`.

## Parallelism
- Disciplines MAY be computed in parallel up to the point of negotiation. A clash or a `Constraint_Violation` MUST force serialization at the precedence boundary.
- Parallel computation MUST NOT introduce non-determinism across runs. If parallelism changes the output bit-for-bit, it is a defect per `08_DETERMINISM_TEMPORALITY_AND_AUDIT_RULES.md`.
- Scheduler design for explicit parallel disciplines is non-trivial and is deferred to Phase 2. Phase 1 MUST serialize disciplines in precedence order unless an AD authorizes otherwise.
- Parallel kernels MUST write into the Global BVH through a single-writer serialization point. Multi-writer races on the BVH are forbidden.

## Red-Line Conditions
Any of the following is a hard failure of this pack file and MUST stop the work:
- reordering the Hierarchy of Precedence without an AD and an entry in `.ai/10_state/decisions.md`
- silent clash acceptance at any resolution
- a concession committed to the Global BVH without vault re-verification
- a concession compiled from LLM output without schema validation
- unbounded cascade depth in the Bi-Directional Feedback Loop
- oscillation undetected at runtime
- a Rust type named after a discipline (`Pipe`, `Duct`, `Cable`, `Road`, `Wall`, etc.)
- a Rust kernel that branches on a discipline string
- a discipline maintaining its own private spatial index for its own volumes
- a Resolution 3 scene instantiated while a Resolution 1 pass is still active
- implicit resolution promotion without the explicit API
- a manual override committed without `HUMAN_OVERRIDE` provenance in the audit trail
- a cascade step that alters a committed volume without replaying the Pricing Oracle
- a discipline reserving space it does not yet need
- a Global BVH write from more than one writer at the same generation

## Cross-References
- **Research paper** (`.ai/13_research/AEC-ECS-SC_RESEARCH.md`):
  - §6 Multi-Disciplinary Coordination (full section, all of 6.1 through 6.8)
- **Companion AEC_ENGINE files:**
  - `00_README_AEC_ENGINE_DOC_SET.md` — pack order of authority
  - `01_COMPOUND_AI_OPERATING_CONTRACT.md` — five-layer separation, LLM / Python / Rust / RocksDB / Z3 roles
  - `02_ECS_AND_COMPONENT_DESIGN_RULES.md` — `DomainDiscipline`, geometry components, archetype rules
  - `03_SPATIAL_COMPREHENSION_PROTOCOL.md` — BVH internals, voxel CSG, spatial stack
  - `04_KNOWLEDGE_VAULT_AND_RULE_AST_CONTRACT.md` — vault AST, rule fetch, jurisdictional binding
  - `06_FORMAL_VERIFICATION_AND_Z3_PROTOCOL.md` — Z3 decomposition, concession verification semantics
  - `08_DETERMINISM_TEMPORALITY_AND_AUDIT_RULES.md` — cascade audit trail, replay, temporal clock
  - `09_PARETO_OPTIMIZATION_AND_FINANCIAL_LAYER_RULES.md` — Pricing Oracle replay on cascade steps
- **Related RUST / GOVERNANCE pack files:**
  - `.ai/06_specs/RUST/02_RUST_KERNEL_DEVELOPMENT_PROTOCOL.md` — kernel data contract, determinism, differential tests
  - `.ai/06_specs/RUST/04_RUST_ARCHITECTURE_AND_BOUNDARY_RULES.md` — Rust boundary rules, no discipline strings across PyO3

## Final Rule
Disciplines yield in the order they cost to relocate. The engine never asks a column to move for a cable.
