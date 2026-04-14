---
plan_id: phase-13-high-performance-optimizations
phase: "Phase 13 (System Performance & Reliability)"
title: "High-Performance Architectural Optimizations: The 8GB M2 Hardening"
status: planned
priority: high
sprint: "Sprint HP — Performance & Scale"
version: 1.0.0
plan_type: design_spec
created: 2026-04-15
last_updated: 2026-04-15
owner: Senior Systems Architect
dependencies:
  - .ai/13_research/advanced architectural and code-level optimizations.md
  - .ai/13_research/Codebase-Langiage-Improvements.md
  - .ai/13_research/3D-Thinking-improvement.md
  - .ai/03_plans/live-wiring-and-8gb-hardening-plan.md
---

# Phase 13 Implementation Plan: High-Performance Architectural Optimizations

> **Objective:** Operationalize advanced data engineering and machine learning optimizations to ensure Vitruvius scales to city-sized datasets while remaining strictly within the 8GB M2 RAM envelope. This plan fills the gaps between research docs and execution.

## 1. Architectural Strategy: The "Lean & True" Engine

Vitruvius must evolve from a sequential pipeline to a high-performance engine using:
1.  **Structural Determinism:** Replace $O(N)$ filesystem scans with $O(1)$ Merkle Tree hashes.
2.  **Immutability:** Move to an **Event-Sourcing** model for the Knowledge Graph to enable auditing and rollbacks.
3.  **Low-Level Compute:** Offload spatial math to **Wasm/Rust** kernels to bypass Python overhead.
4.  **Semantic Precision:** Implement **AST-based chunking** to preserve legal context.

---

## 2. Execution Streams

### Stream HP.1: Merkle Tree Filesystem (Zero-RAM Status)
**Goal:** Eliminate the linear scan of the `001_Raw-Source-Layer`.
- **Task HP.1.1:** Implement `calculate_directory_hash(dir_path)` using SHA-256.
- **Task HP.1.2:** Update `scanner.py` to store root hashes in the System Manifests.
- **Task HP.1.3:** Modify `run_status` to skip directories where the hash matches the previous run.
- **Validation:** Benchmark status checks on 10,000 files; target <100ms vs. current seconds/minutes.

### Stream HP.2: AST-Based Semantic Chunking (Legal Precision)
**Goal:** Prevent LLM hallucinations caused by splitting legal clauses mid-sentence.
- **Task HP.2.1:** Build a **PD 1096 AST Parser** that identifies Title/Chapter/Section/Paragraph markers.
- **Task HP.2.2:** Group chunks by logical Section boundaries rather than hard token limits.
- **Task HP.2.3:** Append parent metadata (Section Title) to every chunk payload.
- **Validation:** 0% rate of "lost context" errors where the LLM forgets which section a rule belongs to.

### Stream HP.3: Event-Sourced Graph Engine (Auditability)
**Goal:** Transition the graph from a mutable JSON blob to an immutable event log.
- **Task HP.3.1:** Implement the **Event Store** (append-only log of `PROMOTED`, `REJECTED`, `AMENDED` events).
- **Task HP.3.2:** Build the **Graph Reducer**: A function that projects the event log into the current RocksDB state.
- **Task HP.3.3:** Expose the **Time-Travel API**: `get_graph_at(timestamp)`.
- **Validation:** Successfully reconstruct the 1977 vs. 2004 versions of PD 1096 from the same event log.

### Stream HP.4: Wasm-Compiled Spatial Kernels (Math Speed)
**Goal:** Execute collision math (GJK) at near-native speed with zero Python GC overhead.
- **Task HP.4.1:** Port `scripts/vitruvius/spatial/` math to **Rust**.
- **Task HP.4.2:** Compile to **WebAssembly** for use in the Python Control Plane (via `wasmtime`) and React Frontend.
- **Task HP.4.3:** Implement **SIMD optimizations** for the M2 chip inside the Rust crate.
- **Validation:** 5x-10x speedup in geometric compliance checks compared to the pure Python implementation.

### Stream HP.5: Knowledge Graph Representation Learning (GraphSAGE)
**Goal:** Find structural loopholes using topological embeddings rather than text search.
- **Task HP.5.1:** Implement **GraphSAGE** aggregators to generate structural embeddings for nodes.
- **Task HP.5.2:** Store embeddings in a **Product-Quantized (PQ)** vector store to save memory.
- **Task HP.5.3:** Build the **Loopholes Detector**: Find nodes with high topological distance but high semantic similarity.
- **Validation:** Identify ≥3 contradictory local ordinances by structure alone, without LLM inference.

---

## 3. Tech Stack Requirements

- **Hashing:** `hashlib` (stdlib).
- **Event Store:** `RocksDB` (via `python-rocksdb`).
- **Low-Level:** `Rust` + `wasm-pack`.
- **Representation Learning:** `DeepGraphLibrary (DGL)` or `PyTorch Geometric` (Low-RAM configuration).

---

## 4. Non-Breaking Guarantee

1.  **Flag Gating:** Features ship behind `features.hp_*` flags.
2.  **Standard IO:** The Event Sourced engine still outputs standard Phase 8 JSON snapshots for backward compatibility with older tools.
3.  **Graceful Degradation:** If the Wasm kernel fails to load, the system falls back to the original Python spatial scripts.

---

## 5. Success Metrics

| Metric | Current Baseline | Phase 13 Target |
|---|---|---|
| **Status Check Latency** | Seconds/Minutes | <100ms |
| **Extraction Accuracy** | ~85% (Statistical) | >95% (AST-Augmented) |
| **Audit Fidelity** | Manual snapshots | 100% Event-Sourced Trail |
| **Spatial Math Speed** | Python interpretation | Near-Native Wasm |
