---
plan_id: phase-12-compound-ai-evolution
phase: "Phase 12 (Advanced Compound AI)"
title: "Compound AI Evolution: The Reactive Neuro-Symbolic OS"
status: planned
priority: highest
sprint: "Sprint Z — The Compound Evolution"
version: 1.0.0
plan_type: design_spec
created: 2026-04-15
last_updated: 2026-04-15
owner: Senior Systems Architect
dependencies:
  - .ai/13_research/Architectural Blueprint: Compound AI Evolution.md
  - .ai/03_plans/statistical-architectural-upgrade-plan.md
  - .ai/03_plans/3d-spatial-intelligence-upgrade-plan.md
  - .ai/10_state/active_context.md
  - .ai/00_system/architecture.md
takes_precedence_over:
  - "Future-state items in phase-9-query-ai-layer-plan.md"
---

# Phase 12 Implementation Plan: Compound AI Evolution

> **Objective:** Transition Vitruvius from a statistical pipeline to a **Reactive Neuro-Symbolic OS**. This plan operationalizes the "Big Picture" blueprint by mathematically bounding LLM outputs through formal logic, implementing $O(\Delta)$ reactive updates, and deploying adversarial agent topologies.

## 1. Architectural Strategy: The "OS" vs. The "Pipeline"

The current pipeline is linear (Ingest → Convert → Canonicalize → Review). The **Compound AI Evolution** shifts this to a **Reactive Loop**:
1.  **Neuro-Symbolic IR:** The LLM does not output natural language; it outputs **Datalog/Prolog** logical proofs.
2.  **Symbolic Firewall:** A Rust-based Datalog engine (the "Symbolic" part) verifies the logic. Hallucinations result in immediate syntax/logic rejections before any write occurs.
3.  **Differential Propagation:** Updates are processed as **Deltas ($\Delta$)** in a differential dataflow, updating only downstream dependencies in the graph.
4.  **Adversarial Synthesis:** Decisions are reached via a **Proposer/Inspector/Adjudicator** swarm rather than a single inference call.

---

## 2. Execution Streams

### Stream S1: Neuro-Symbolic Logic Bridge (The Firewall)
**Goal:** Force LLM (Gemma 4) to output compliance reasoning as strict Datalog triples.
- **Task S1.1:** Define the **Vitruvius Logic Schema** (Predicates for `Violates`, `Distance`, `Zone`, `Height`).
- **Task S1.2:** Implement a **Rust Datalog Evaluator** (using `crepe` or a custom Datalog engine) as a Python extension.
- **Task S1.3:** Prompt Engineering: Update Review Tier-1 prompts to require a `<logic>` block containing the formal proof.
- **Validation:** 100% rejection of LLM outputs that fail logical consistency checks against the Phase 8 graph.

### Stream S2: Adversarial Swarm Topology (Red-Teaming)
**Goal:** Deploy a multi-agent swarm to eliminate edge-case hallucinations.
- **Task S2.1:** Implement **Agent A (The Proposer)**: Optimistic extraction and proof generation.
- **Task S2.2:** Implement **Agent B (The Inspector)**: Prompt-weighted to find contradictions in Agent A's proof.
- **Task S2.3:** Implement **Agent C (The Adjudicator)**: The deterministic Z3 SMT solver that breaks ties between A and B based on numeric constraints.
- **Validation:** Measure "Hallucination Capture Rate" — Agent B should flag ≥30% of Agent A's initial novel claims for secondary review.

### Stream S3: Differential Dataflow Engine (The Central Nervous System)
**Goal:** $O(\Delta)$ updates for the million-node legal graph.
- **Task S3.1:** Implement **Event Sourcing** for the RocksDB log (Every change is an immutable `Delta` event).
- **Task S3.2:** Build the **Dependency Tracker**: A map of which buildings/rules depend on specific legal clauses.
- **Task S3.3:** Integrate **Differential Dataflow** (using Rust's `timely-dataflow` or a simplified Python dependency-graph walker) to propagate changes.
- **Validation:** PD 1096 amendment simulation — change one setback rule and verify that *only* affected buildings are re-audited in <100ms.

### Stream S4: Isomorphic Spatial Wasm Kernel (Frontend Parity)
**Goal:** Absolute mathematical parity between backend audit and frontend 3D UI.
- **Task S4.1:** Refactor `scripts/vitruvius/spatial/` geometry math into a **pure Rust crate**.
- **Task S4.2:** Compile to **WebAssembly (Wasm)** for the browser.
- **Task S4.3:** Implement the **Bridge Layer** for React Three Fiber to call the Wasm kernel for real-time GJK collision checks.
- **Validation:** "Zero-Latency Compliance": UI turns red at 60FPS in the browser using the exact same logic that runs in the Python backend.

### Stream S5: Algorithmic Prompt Compilation (DSPy)
**Goal:** Self-optimizing prompts that diverge by dataset/jurisdiction.
- **Task S5.1:** Integrate **DSPy framework** for local Ollama models.
- **Task S5.2:** Define **Metrics for Extraction**: Precise regex-match density vs. semantic similarity.
- **Task S5.3:** Run **Compilation Cycles**: DSPy optimizes the prompt for "National Building Code" vs. "Local Fire Code" automatically.
- **Validation:** Accuracy lift of ≥15% on "Unstructured LGU Ordinances" compared to the static master prompt.

---

## 3. Tech Stack Requirements (Additive)

- **Logic:** `crepe` (Datalog in Rust) or `asprin` (Answer Set Programming).
- **Reactive:** `timely-dataflow` (Rust) for Stream S3.
- **Optimizer:** `dspy-ai` (Python) for Stream S5.
- **Frontend:** `wasm-pack` for the Rust-to-Wasm bridge.
- **Memory:** PQ (Product Quantization) via `scikit-learn` or `faiss` for scaling embeddings on 8GB.

---

## 4. Non-Breaking Guarantee

1.  **Feature-Flag Isolation:** All Phase 12 features ship behind `features.s1_*` through `features.s5_*` flags.
2.  **Legacy Fallback:** If the Neuro-Symbolic IR fails to compile, the system falls back to the existing Statistical Review (Phase 6) and flags the node for human review.
3.  **8GB Hardening:** Differential dataflow ensures we never load the full graph into memory; we only process the active Delta ($\Delta$).

---

## 5. Success Metrics

| Metric | Baseline (Phase 7-9) | Target (Phase 12) |
|---|---|---|
| **Hallucination Rate** | ~5% (Statistical) | <0.1% (Neuro-Symbolic Verified) |
| **Update Latency** | Minutes (Full Graph Rebuild) | <100ms (Differential Delta) |
| **Inference Cost** | Constant per query | $O(1)$ for cached/memoized geometry |
| **UI Parity** | Visual Guess (UI) vs. Math (Backend) | 100% Binary Identical (Wasm) |

---

## 6. Implementation Sequence

1.  **Sprint Z.1:** Stream S1 (Neuro-Symbolic Bridge) + Stream S4 (Wasm Bridge).
2.  **Sprint Z.2:** Stream S2 (Adversarial Swarm) + Stream S5 (DSPy Compilation).
3.  **Sprint Z.3:** Stream S3 (Differential Dataflow) — The Final OS Integration.
