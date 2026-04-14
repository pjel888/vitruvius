---
plan_id: phase-8b-geo-topological-graph
phase: "Phase 8B / 10B (System-Level Performance + Spatial Graph)"
title: "Geo-Topological Knowledge Graph: Binary Vault & Octree Engine"
status: planned
priority: high
sprint: "Sprint GT — System Hardening"
version: 1.0.0
plan_type: design_spec
created: 2026-04-15
last_updated: 2026-04-15
owner: Senior Systems Architect
dependencies:
  - .ai/13_research/Geo-Topological Knowledge Graph.md
  - .ai/03_plans/statistical-architectural-upgrade-plan.md
  - .ai/03_plans/3d-spatial-intelligence-upgrade-plan.md
  - .ai/03_plans/phase-8-graph-contract-indexing-plan.md
takes_precedence_over:
  - "Decoupled Spatial Daemon (Stream N) in 3d-spatial-intelligence-upgrade-plan.md (Upgrades TS to Rust)"
---

# Phase 8B Implementation Plan: Geo-Topological Knowledge Graph

> **Objective:** Operationalize the **Spatial Memory** system by building a high-performance Rust Data Plane. This replaces the linear search with $O(\log n)$ Octree traversals and connects physical proximity to topological relationships via **Spatial GraphRAG**.

## 1. Architectural Strategy: The Binary Vault

To survive on an 8GB M2, Vitruvius must stop treating the filesystem as a collection of text files and start treating it as a **Memory-Mapped Binary Vault**.

1.  **Zero-Copy Exchange:** Use **Apache Arrow** to share data between Python and Rust without serialization overhead.
2.  **Pre-Aligned Access:** Use **FlatBuffers** for $O(1)$ access to spatial octants.
3.  **LSM-Tree Storage:** Use **RocksDB** as the high-speed backend for the Temporal Knowledge Graph.

---

## 2. Execution Streams

### Stream GT.1: The Binary Data Plane (Rust/Python Bridge)
**Goal:** Establish the high-speed link between the Control Plane and the Engine.
- **Task GT.1.1:** Setup `pyo3` bridge in `scripts/vitruvius/engine_rs/`.
- **Task GT.1.2:** Implement **FlatBuffer Schemas** for `SpatialNode` and `LegalEdge`.
- **Task GT.1.3:** Configure **Apache Arrow** buffers for zero-copy geometry streaming.
- **Validation:** Benchmark 10,000 node reads; target <5ms (Python-to-Rust roundtrip).

### Stream GT.2: Sparse Linear Octree Engine (The "Where")
**Goal:** Implement the $O(\log n)$ spatial indexing system in Rust.
- **Task GT.2.1:** Implement the **Linear Octree** (Flat `Vec` storage for cache locality).
- **Task GT.2.2:** Build the **SIMD-Optimized Bounds Checker** (Pruning 8 octants per cycle).
- **Task GT.2.3:** Implement **Recursive Search** (Point, Sphere, and Frustum queries).
- **Validation:** Traverse a building model with 100k nodes; target <1ms search time.

### Stream GT.3: Temporal Knowledge Graph (The "When")
**Goal:** Upgrade Phase 8 nodes to time-bound quadruples $(s, p, o, t)$.
- **Task GT.3.1:** Extend RocksDB schema to support **Temporal Edges** (`valid_from`, `valid_until`).
- **Task GT.3.2:** Implement **Versioned Retrieval** (Query the graph as it existed at any Unix timestamp).
- **Task GT.3.3:** Build the **Parquet Archiver** for historical code snapshots (Cold Storage).
- **Validation:** Successfully retrieve "PD 1096 Section 804" as it was written in 1977 vs. 2004.

### Stream GT.4: Geo-Topological Bridging (Spatial GraphRAG)
**Goal:** Seed GraphRAG with physical proximity results.
- **Task GT.4.1:** The **"Proximity Jump"**: Seed the Graph search with IDs retrieved from the Octree Leaf.
- **Task GT.4.2:** Implement **Geometric Weighting** ($W = W_{sem} \cdot e^{-\lambda d}$) to decay relevance over distance.
- **Task GT.4.3:** Build the **Spatial Edge Generator**: Automatically create `physically_adjacent_to` edges for intersecting bounding boxes.
- **Validation:** Query: "Laws affecting this Column" → Returns IDs based on both text-links AND 3D proximity.

### Stream GT.5: Hardware Hardening (8GB M2 Guardrails)
**Goal:** Mathematically eliminate memory pressure.
- **Task GT.5.1:** Implement **mmap (Memory Mapping)**: Only load active Octree pages into RAM.
- **Task GT.5.2:** Deploy **Bloom Filters**: Drop redundant ingestion data before it hits the engine.
- **Task GT.5.3:** **Monte Carlo Dropout** integration: Quantify Epistemic Uncertainty for every compliance decision.
- **Validation:** Run full-city scan; verify Python process stays <400MB RSS.

---

## 3. Tech Stack Requirements

- **Engine:** Rust (`pyo3`, `arrow`, `flatbuffers`, `rocksdb`, `memmap2`).
- **Math:** `glam` or `nalgebra` for SIMD-accelerated 3D primitives.
- **Python:** `polars` (Arrow-native) for high-speed data frame manipulation.

---

## 4. Implementation Workflow

1.  **Foundation:** Setup the Rust crate and FlatBuffer schemas.
2.  **Spatial:** Build the Octree and Search algorithms.
3.  **Topological:** Link Octree Leaf data to RocksDB Graph IDs.
4.  **Inference:** Wire the Spatial-Topological results into the Gemma 4 prompt context.

---

## 5. Success Metrics

| Metric | Baseline (Traditional) | Target (Geo-Topological) |
|---|---|---|
| **Search Speed** | $O(N)$ (Scan all rules) | $O(\log N)$ (Octree Pruning) |
| **Data Access** | JSON Parsing (Slow) | Zero-Copy Arrow (Instant) |
| **Memory Footprint** | Loads full dataset | Loads active pages (mmap) |
| **Reasoning Quality** | Semantic-only | Semantic + Physical Proximity |
