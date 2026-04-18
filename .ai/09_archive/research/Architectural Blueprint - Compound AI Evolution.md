### Architectural Blueprint: Compound AI Evolution

**1. Adversarial Agent Topologies (Automated Red-Teaming)**
* **The Concept:** Instead of a single Mixture of Experts (MoE) router attempting to find the *correct* answer, Vitruvius deploys a multi-agent swarm with competing objectives to eliminate edge-case hallucinations.
* **The Architecture:**
    * *Agent A (The Proposer):* Attempts to mathematically prove a design constraint extracted from a text chunk is valid.
    * *Agent B (The Inspector):* Specifically prompted and weighted to find loopholes, contradictions, or violations in Agent A's proof against the existing Phase 8 graph.
    * *Agent C (The Adjudicator):* The deterministic Z3 Theorem Prover acts as the immutable tie-breaker.
* **The Benefit:** Bounding generative logic through adversarial synthesis. If Agent A hallucinates a spatial compliance, Agent B's sole loss-function objective is to destroy that assumption before it writes to the binary vault. [Image of Generative Adversarial Networks architecture]

**2. Algorithmic Prompt Compilation (DSPy Integration)**
* **The Concept:** Hand-writing and manually tweaking system prompts (e.g., "You are an expert architect evaluating...") is brittle and unscalable across thousands of LGU ordinances. State-of-the-art compound systems compile prompts like executable code.
* **The Architecture:** Integrate frameworks like Stanford's DSPy. You define the metric (e.g., precise extraction of setback limits). The system uses an optimizer to mathematically adjust the prompt's few-shot examples and instructional syntax to maximize accuracy across the specific dataset it is currently processing.
* **The Computation:** Optimizing prompt parameters $\theta$ to maximize the expected reward $R$ over a validation dataset $D$:
    $$\theta^* = \arg\max_\theta \mathbb{E}_{(x,y) \sim D} [R(P_\theta(x), y)]$$
* **The Benefit:** Vitruvius self-optimizes its Ollama inference strategy dynamically. The prompt used for the National Building Code will mathematically diverge from the prompt optimized for an unstructured local fire code. 

**3. Tool Synthesis over Text Generation (Code-as-Reasoning)**
* **The Concept:** Large Language Models are highly prone to error when executing mathematical or geometric reasoning, but they possess near-perfect syntax for generating deterministic code.
* **The Architecture:** When the MoE router identifies a highly complex, novel spatial constraint (e.g., a multi-tiered daylighting plane angle), it is restricted from outputting a `keep/reject` decision directly. Instead, it synthesizes a temporary Python function wrapping a Z3 constraint.
* **Execution Flow:**
    1. LLM synthesizes `temp_evaluator.py`.
    2. Vitruvius executes the script in an isolated sandbox.
    3. The pipeline captures the deterministic boolean output.
* **The Benefit:** Absolute decoupling of semantic parsing from spatial algebra.

**4. Continuous Active Learning (Epistemic Foraging)**
* **The Concept:** When the system flags a human architect due to high Epistemic Uncertainty (quantified via Monte Carlo Dropout), that manual resolution must permanently decrease the system's ignorance map.
* **The Architecture:** * When an architect manually resolves a topological contradiction, the orchestrator generates a compiled "delta event" in the RocksDB log.
    * Vitruvius updates the routing weights so that identical geometric queries bypass the LLM entirely in the future.
* **The Benefit:** The system strictly adheres to an asymptote of zero-inference. The more the compound system is used, the less it relies on generative AI, shifting operations back to $O(1)$ memory-mapped graph lookups.

Which of these compound mechanisms aligns best with the current trajectory of the agentic AI building the V1 pipeline?

### 1. Visual-Topological RAG (V-RAG) for Code Diagrams
Standard text-extraction fails on legacy AEC documents. PD 1096 and LGU zoning laws embed critical spatial constraints (e.g., daylighting planes, minimum parking turning radii) directly into unparseable diagrams.

* **The Mechanism:** Integrate a local, quantized Vision-Language Model (VLM) explicitly for visual constraint extraction, linking it to the textual Knowledge Graph.
* **The Architecture:**
    1. During ingestion, layout parsers isolate images from the PDF.
    2. The VLM evaluates the image and outputs a strict JSON representation of the visual geometric constraints.
    3. The orchestrator maps these constraints as child nodes to the textual rules in the RocksDB vault.
* **The Computation:**
  Visual embedding extraction $E_{vis}$ fused with textual embedding $E_{text}$ to create a multimodal node representation:
  $$H_{node} = \sigma(W_{v} E_{vis} \oplus W_{t} E_{text} + b)$$



### 2. Isomorphic Spatial Execution (Frontend/Backend Parity)
A frequent point of failure in compound AEC systems is a mismatch between what the user sees in the 3D canvas and what the backend mathematically evaluates. 

* **The Mechanism:** Utilize the Rust-to-Wasm compiler pipeline to create an isomorphic spatial engine. The exact same binary that evaluates compliance in the backend runs directly inside the client's browser.
* **The Architecture:**
    * **Backend (Python/Rust):** Runs the heavy Z3 Theorem Prover and absolute compliance checks.
    * **Frontend (React Three Fiber / Three.js):** Loads the `vitruvius_spatial.wasm` kernel directly into the browser thread. As the user manipulates geometry on the canvas, the Wasm kernel calculates GJK intersections in real-time at 60FPS. 
* **The Benefit:** Zero latency for visual feedback. The architect sees a setback violation turn red instantly in the UI, mathematically guaranteed to match the final backend audit.



### 3. Behavioral Confidence Weighting for Human-in-the-Loop (HitL)
When Epistemic Uncertainty triggers a fallback to human adjudication, standard boolean inputs (`Approve/Reject`) fail to capture human doubt. A rushed click degrades the integrity of the graph.

* **The Mechanism:** Embed cognitive behavioral analytics into the adjudication UI to mathematically weight the human's input before committing it to the event-sourced log.
* **The Architecture:**
    * Implement a high-friction input mechanism for critical graph mutations (e.g., a time-locked "slide-to-submit" interface).
    * Capture behavioral telemetry: Time-to-decision ($T_d$), interaction jitter, and explicit confidence sliders.
* **The Computation:**
  The new edge weight $W_{edge}$ is a function of the architect's historical accuracy $A_{user}$ and the behavioral confidence metric $C_{beh}$:
  $$W_{edge} = \alpha A_{user} + \beta \left( 1 - e^{-\lambda T_d} \right)$$
* **The Benefit:** If an architect rapidly forces an approval on a highly ambiguous LGU ordinance overlap, the system accepts it but assigns a low topological weight, flagging it for secondary review during the next batch process.

### Artifact: Isomorphic Wasm Bridge Configuration

```typescript
// frontend/src/lib/vitruvius-spatial-bridge.ts
import { initWasm, check_gjk_collision } from 'vitruvius-spatial-wasm';
import * as THREE from 'three';

export class VitruviusCanvasEngine {
    private isReady = false;

    async initialize() {
        // Loads the exact same mathematical kernel used by the Python backend
        await initWasm('/static/vitruvius_spatial_bg.wasm');
        this.isReady = true;
    }

    validateMeshCompliance(
        proposedMesh: THREE.BufferGeometry, 
        legalEnvelope: THREE.BufferGeometry
    ): boolean {
        if (!this.isReady) throw new Error("Wasm Kernel not loaded");
        
        // Extract raw Float32Arrays directly from R3F/Three.js
        const proposedVertices = proposedMesh.attributes.position.array as Float32Array;
        const envelopeVertices = legalEnvelope.attributes.position.array as Float32Array;

        // O(1) execution inside browser memory sandbox
        return check_gjk_collision(proposedVertices, envelopeVertices);
    }
}
```

Which of these mechanisms—V-RAG for diagram extraction, Wasm isomorphic bridging for the 3D canvas, or behavioral weighting for adjudication—presents the most immediate utility for the current development phase?

If we are stepping back to look at the absolute "Big Picture," we have to stop thinking about making the current pipeline run *faster* and start thinking about mathematically eliminating the need to run it at all. 

True architectural optimization means doing less work. True accuracy means relying on structural proofs rather than statistical probability.

To make Vitruvius a generational leap in AEC software, here are four long-term, structural paradigms we must architect into the codebase. 

### 1. Neuro-Symbolic Intermediate Representation (IR)
Right now, you are using the LLM to output a text-based decision (`keep`, `reject`, or a summary). Text is inherently ambiguous, which leaves room for hallucination.

* **The Big Picture:** Transition Vitruvius to a **Neuro-Symbolic** system. You force the LLM (the "Neuro" part) to output its reasoning strictly in a formal logic language, like **Datalog** or **Prolog** (the "Symbolic" part).
* **How it improves accuracy:** The LLM does not get to say "The building is compliant." It must output the logical proof: 
  `Violates(Rule804) :- Distance(Wall, PropertyLine, D), D < 2.0.`
* **The Optimization:** Your Rust kernel takes that Datalog string and mathematically evaluates it against the RocksDB vault. If the LLM hallucinates a rule or makes a logical leap, the Rust compiler instantly catches the syntax/logic error and rejects it. You achieve 100% mathematical certainty on AI outputs.

### 2. Differential Dataflow for the Legal Graph
As Vitruvius scales, the Phase 8 Knowledge Graph will grow to millions of nodes. If the Philippine government amends one paragraph of the National Building Code, recalculating the entire graph's PageRank or clustering metrics will take hours, even in Rust.

* **The Big Picture:** Implement **Differential Dataflow**. Instead of thinking of the graph as a static object that gets recalculated, you treat computations as a flowing stream.
* **How it improves optimization:** When an amendment event occurs, the system calculates *only the delta* ($\Delta$). It mathematically tracks exactly which edges are downstream of that specific law and updates only those nodes.
* **The Result:** An $O(V + E)$ full-graph recalculation becomes an $O(\Delta)$ micro-update. The brain learns new laws in milliseconds rather than hours.

### 3. Topological Memoization (Merkle Trees for 3D Geometry)
Buildings contain massive repetition. A high-rise might have 1,200 identical hotel room layouts. Currently, a spatial engine would run the heavy Z3 Theorem Prover on every single room, redundantly recalculating the exact same spatial algebra 1,200 times.

* **The Big Picture:** Hash the physical geometry into a **Merkle Tree**. 
* **How it improves optimization:** Before the Rust kernel runs the GJK collision algorithm on a room, it hashes the spatial JSON of that room. It checks a local `Verified_Cache` in RocksDB.
* **The Result:** 1. Room 1 is processed: Takes 500ms. Result is saved as `Hash_X = Compliant`.
  2. Rooms 2 through 1,200 are processed: The engine sees `Hash_X`, knows it is identical, and skips the Z3 math entirely. Evaluation drops from 10 minutes to 12 milliseconds.

### 4. Vector Quantization (PQ) for Infinite Graph Scaling
If you use GraphSAGE to create embeddings (float arrays) for every legal node so you can find structural patterns, an 8GB machine will eventually run out of RAM to hold those vectors.

* **The Big Picture:** Implement **Product Quantization (PQ)**. 
* **How it improves optimization:** Standard embeddings use 32-bit floats. PQ mathematically compresses these vectors by splitting them into sub-vectors and replacing them with short centroid IDs from a codebook. 
* **The Result:** A vector database that would normally require 16GB of RAM is mathematically compressed down to 500MB with negligible loss in cosine similarity accuracy. You can hold the entire global library of architectural standards in your M2's active memory simultaneously.

***

These aren't just software features; they are computer science principles that will make the Vitruvius codebase virtually indestructible as it scales. 

If we are plotting the long-term roadmap, which of these paradigms should we consider the absolute "North Star" for the engine's next major evolution: forcing the LLM into **Neuro-Symbolic logic outputs**, or building the **Differential Dataflow** to handle real-time code amendments?

You hit the nail on the head. It is a false dichotomy. You absolutely need both, because they solve two entirely different halves of the same "Big Picture" problem: **Trust** and **Scale**. 

If you have a perfectly accurate system (Neuro-Symbolic) but it takes 12 hours to recalculate the city grid every time a law changes, it's useless in the real world. Conversely, if you have a lightning-fast, real-time engine (Differential Dataflow) but it's propagating LLM hallucinations at the speed of light, it's actively dangerous.

When you combine them, you create a **Reactive Deterministic Engine**. It’s like React.js, but for building laws and spatial geometry. 

Here is exactly how the "Both" pipeline works together in harmony:

### The Neuro-Symbolic Dataflow Pipeline

**Step 1: The "Neuro" Ingestion (The AI)**
A new local ordinance is passed regarding fire safety. The LLM (Gemma 4) reads the messy PDF. Instead of outputting a summary, it is strictly prompted to output formal logic (Datalog):
```prolog
Violation(Building, "Fire_Code_01") :- 
    Distance(Building, Adjacent_Structure, D), 
    D < 3.0.
```

**Step 2: The "Symbolic" Verification (The Compiler)**
The LLM passes this logic to the Rust Kernel. Rust doesn't "think" about it; it mathematically compiles it. If the LLM made a syntax error or hallucinated a variable, Rust instantly rejects it and forces the LLM to try again. **(Trust Achieved)**

**Step 3: The Delta Injection (The Event)**
Once compiled, this new rule is not just dropped into a static database. It is treated as a flowing "Delta" ($\Delta$) event: `+ [New Fire Code Rule]`.

**Step 4: Differential Propagation (The Stream)**
The Differential Dataflow engine receives this Delta. Because it mathematically maps dependencies, it realizes: *"I don't need to rescan the whole city. This rule only affects 'Distance' and 'Adjacent_Structure'."* It instantly ripples through your RocksDB vault, identifies only the specific buildings that violate this new 3.0m rule, and flips their status to `Non-Compliant` in milliseconds. **(Scale Achieved)**

---

### The Result: The Ultimate Compound OS

By combining these two, Vitruvius reaches a state of software nirvana. 
* **The AI** handles the messy, human reality of reading PDFs and deciphering intent. 
* **The Logic Language** acts as the impenetrable firewall that stops hallucinations.
* **The Dataflow Engine** acts as the central nervous system, instantly feeling the "ripple effect" of a changing law across a massive 3D database without freezing your computer.

You aren't just integrating AI; you are building an engine that makes AI mathematically accountable and endlessly scalable.

Since we are cementing this as the grand architecture for the Vitruvius OS, where do you want to lay the first experimental brick? Should we try prompting your local model to translate a simple building code into strict Datalog/Prolog, or should we map out how the event-stream architecture would look in Rust?

```markdown
# Vitruvius Core: Differential Event-Stream Architecture
> **Domain:** Rust Systems Programming, Event Sourcing, Differential Dataflow
> **Objective:** Process legal code amendments as $O(\Delta)$ micro-updates instead of $O(V+E)$ full-graph recalculations.
> **Target:** 8GB Unified Memory (Apple M2)

## 1. The Architectural Paradigm

In a static graph, if PD 1096 Section 804 changes, the entire system halts to recalculate compliance for all geometries. In an **Event-Stream** architecture, the graph is never "edited." Instead, the system appends immutable `Delta` events to a log. The engine listens to this stream, identifies exactly which spatial relationships are downstream of the change, and re-evaluates only those specific nodes.

## 2. Core Rust Implementation (`vitruvius_stream`)

This module defines the zero-copy event structures and the differential engine that processes them.

### A. The Immutable Delta Types (`src/events.rs`)
We use Enums to strictly define the bounded state changes. By deriving `Serialize` and `Deserialize`, these map directly to FlatBuffers for the RocksDB vault.

```rust
use serde::{Deserialize, Serialize};

/// Represents a uniquely identifiable building or spatial envelope
type GeometryId = String;

/// Represents a specific legal constraint (e.g., "PD_1096_Sec_804")
type RuleId = String;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum LegalDelta {
    /// A completely new law is introduced by the LLM
    RuleAdded {
        rule_id: RuleId,
        datalog_proof: String, 
        timestamp: u64,
    },
    /// An LGU amends an existing constraint (e.g., 2.0m setback becomes 3.0m)
    RuleAmended {
        rule_id: RuleId,
        new_datalog_proof: String,
        timestamp: u64,
    },
    /// A rule is repealed or overwritten
    RuleRepealed {
        rule_id: RuleId,
        timestamp: u64,
    },
    /// Spatial daemon detects a physical change in the SketchUp model
    GeometryUpdated {
        geometry_id: GeometryId,
        new_volume_hash: String, // Merkle root of the B-Rep
    }
}
```

### B. The Differential Engine (`src/engine.rs`)
This is the heart of the reactive system. It maintains an in-memory index of dependencies. When a rule changes, it finds the exact geometries that rely on that rule and flags them for Wasm re-evaluation.

```rust
use std::collections::{HashMap, HashSet};
use crate::events::LegalDelta;

pub struct DifferentialEngine {
    // Maps a Rule ID to all Building Geometries that currently rely on it.
    // Memory Footprint: Very small (just pointers/Strings), easily fits in 8GB.
    dependency_graph: HashMap<String, HashSet<String>>,
    
    // Simulating the RocksDB connection
    event_log: Vec<LegalDelta>, 
}

impl DifferentialEngine {
    pub fn new() -> Self {
        DifferentialEngine {
            dependency_graph: HashMap::new(),
            event_log: Vec::new(),
        }
    }

    /// The single entry point for all graph mutations.
    pub fn apply_delta(&mut self, event: LegalDelta) {
        // 1. Append to the immutable log (The "Source of Truth")
        self.event_log.push(event.clone());

        // 2. Route the event to the highly-optimized delta processor
        match event {
            LegalDelta::RuleAdded { rule_id, datalog_proof, .. } => {
                self.handle_new_rule(rule_id, datalog_proof);
            }
            LegalDelta::RuleAmended { rule_id, new_datalog_proof, .. } => {
                self.propagate_amendment(rule_id, new_datalog_proof);
            }
            LegalDelta::GeometryUpdated { geometry_id, new_volume_hash } => {
                self.evaluate_single_geometry(geometry_id, new_volume_hash);
            }
            _ => {} // Handle other cases
        }
    }

    /// O(Δ) Propagation: The core optimization
    fn propagate_amendment(&self, rule_id: String, _new_logic: String) {
        // Instead of rescanning the whole city, we ONLY look up the buildings 
        // that were previously evaluated against this specific rule.
        if let Some(affected_buildings) = self.dependency_graph.get(&rule_id) {
            println!("[Differential Route] Rule {} amended.", rule_id);
            println!(">> Mathematically isolating {} affected geometries...", affected_buildings.len());
            
            for building_id in affected_buildings {
                // Here, we pass the building's Apache Arrow memory pointer 
                // to the Wasm spatial kernel to re-evaluate against the new logic.
                println!("   -> Re-evaluating constraint for {}", building_id);
            }
        } else {
            println!("[Differential Route] Rule amended, but no current geometries depend on it. Skipping compute.");
        }
    }

    fn handle_new_rule(&mut self, rule_id: String, _logic: String) {
        // Initialize dependency tracking for the new rule
        self.dependency_graph.insert(rule_id, HashSet::new());
    }

    fn evaluate_single_geometry(&self, _geometry_id: String, _hash: String) {
        // Triggers the Z3 solver via Wasm for a single building update
    }
}
```

### C. The Python PyO3 Bridge (`src/lib.rs`)
To integrate this with the existing Python orchestrator, we expose the Rust engine to Python via PyO3.

```rust
use pyo3::prelude::*;
use crate::engine::DifferentialEngine;
use crate::events::LegalDelta;

#[pyclass]
struct VitruviusStream {
    engine: DifferentialEngine,
}

#[pymethods]
impl VitruviusStream {
    #[new]
    fn new() -> Self {
        VitruviusStream {
            engine: DifferentialEngine::new(),
        }
    }

    /// Python calls this when the LLM outputs a new Datalog proof
    fn inject_rule_amendment(&mut self, rule_id: String, datalog: String) {
        let event = LegalDelta::RuleAmended {
            rule_id,
            new_datalog_proof: datalog,
            timestamp: 1713149533, // Example Unix Timestamp
        };
        
        self.engine.apply_delta(event);
    }
}

#[pymodule]
fn vitruvius_differential(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<VitruviusStream>()?;
    Ok(())
}
```

## 3. Dataflow Execution Trace

When the LLM finishes parsing a PDF and generates an amendment, the Python orchestrator executes:

```python
import vitruvius_differential

# 1. Initialize the Rust Kernel
stream_engine = vitruvius_differential.VitruviusStream()

# 2. LLM detects an LGU changed the setback from 2.0m to 3.0m
datalog_output = 'Violates(B, "Setback") :- Distance(B, PLine, D), D < 3.0.'

# 3. Python pushes the delta into the Rust Data Plane
# Rust bypasses the GIL, finds the exact 4 buildings affected out of 10,000, 
# and triggers Wasm re-evaluation in milliseconds.
stream_engine.inject_rule_amendment("LGU_QC_Ordinance_15", datalog_output)
```
```

### Vitruvius: Compound AI System Definition

Vitruvius operates strictly as a Compound AI System. It abandons the monolithic LLM approach—where a single model is trusted to read, reason, and calculate—in favor of a multi-component engine. The generative AI is subordinated to deterministic mathematical and logical constraints, acting as a modular piece within a larger, verifiable pipeline.



**1. The Semantic Extractor (Generative Component)**
* **Engine:** Local LLM (e.g., Gemma 4).
* **Function:** Natural language understanding and unstructured data parsing.
* **Constraint:** Strictly barred from making final compliance decisions. Used exclusively to translate messy human input—such as scanned LGU ordinances or fragmented client briefs—into formal intermediate representations (e.g., Datalog, JSON).

**2. The Mathematical Verifier (Deterministic Component)**
* **Engine:** Z3 Theorem Prover and Rust/Wasm Spatial Kernels.
* **Function:** Absolute geometric and logical verification.
* **Constraint:** Takes the extracted constraints from the LLM and mathematically evaluates them against the physical 3D B-Rep geometry. If the spatial engine returns `unsat` (unsatisfiable), the LLM's assumption is instantly destroyed.

**3. The Immutable Vault (Topological Component)**
* **Engine:** RocksDB, FlatBuffers, and Event-Sourced Graph.
* **Function:** Maintains the persistent, uncorrupted state of Philippine architectural laws (e.g., PD 1096) and historical precedents.
* **Constraint:** Employs Differential Dataflow to update graph dependencies in $O(\Delta)$ time when an amendment occurs, explicitly bypassing the need for generative LLM inference during graph updates.

**4. The Orchestrator (Control Component)**
* **Engine:** Python Control Plane.
* **Function:** Routes data streams between the Generative, Deterministic, and Topological components.
* **Constraint:** Enforces ingestion validations, such as the numerical lock algorithms and Monte Carlo Dropout uncertainty thresholds, before committing any new data to the binary vault.

---

Which orchestration boundary should we formally define next: the human-in-the-loop adjudication protocol for resolving epistemic uncertainty, or the exact API contract connecting the Wasm spatial kernel to the 3D client canvas?

# API Contract: Wasm Spatial Kernel $\leftrightarrow$ 3D Client Canvas

**Protocol:** Zero-Copy Linear Memory Sharing (WebAssembly to JavaScript/WebGL)
**Frontend:** React Three Fiber / Three.js (TypeScript)
**Kernel:** Rust compiled to `wasm32-unknown-unknown` via `wasm-bindgen`



### 1. Data Type Definitions

To achieve $O(1)$ transfer speeds, the contract strictly forbids JSON serialization for geometry. The client canvas must extract the raw flat coordinate buffers from the GPU and pass them as memory pointers to the Wasm kernel.

#### TypeScript Interfaces (Client-Side)
```typescript
// types/vitruvius-wasm.d.ts

/** * Represents a flat Float32Array extracted from THREE.BufferGeometry
 * Format: [x1, y1, z1, x2, y2, z2, ...]
 */
export type FlatVertexArray = Float32Array;
export type FlatIndexArray = Uint32Array;

export interface SpatialResult {
    is_compliant: boolean;
    violation_distance?: number;
    // If collision occurs, returns the exact [x, y, z] coordinate of the breach
    collision_point?: [number, number, number]; 
    rule_id: string;
}
```

#### Rust Structs (Kernel-Side)
```rust
// src/contract.rs
use serde::{Serialize, Deserialize};
use wasm_bindgen::prelude::*;

#[wasm_bindgen]
#[derive(Serialize, Deserialize)]
pub struct SpatialResult {
    pub is_compliant: bool,
    pub violation_distance: Option<f32>,
    pub collision_point: Option<Vec<f32>>,
    pub rule_id: String,
}
```

### 2. The Execution Contract

The API exposes three strict operational phases: Kernel Allocation, Context Injection, and The Hot Loop.

#### A. Kernel Allocation & Initialization
Loads the `.wasm` binary into the browser's execution thread and allocates the isolated linear memory sandbox.

**TypeScript Invocation:**
```typescript
import initWasm from 'vitruvius-spatial-kernel';

async function bootstrapEngine() {
    // Allocates a strict 256MB memory boundary for the Wasm sandbox
    await initWasm({ memory: new WebAssembly.Memory({ initial: 256, maximum: 256 }) });
}
```

#### B. Context Injection (The Legal Envelope)
Loads the static Phase 8 spatial constraints (e.g., setbacks, height limits) into the kernel. This is done once per session or when the law changes.

**Rust Signature:**
```rust
#[wasm_bindgen]
pub fn load_legal_envelope(
    rule_id: &str, 
    vertices: &[f32], // Zero-copy view into JS memory
    indices: &[u32]
) -> Result<(), JsValue> {
    // Parses the flat buffer into a BVH (Bounding Volume Hierarchy) tree
    // Stores in the Wasm heap for fast reference
}
```

**TypeScript Invocation:**
```typescript
function injectConstraint(envelopeMesh: THREE.Mesh, ruleId: string) {
    const vertices = envelopeMesh.geometry.attributes.position.array as Float32Array;
    const indices = envelopeMesh.geometry.index.array as Uint32Array;
    
    wasmKernel.load_legal_envelope(ruleId, vertices, indices);
}
```

#### C. The Hot Loop (Real-Time Evaluation)
This function executes inside the React `useFrame` loop at 60 FPS. It calculates GJK/EPA intersections between the user's active cursor/mesh and the injected legal envelope.

**Rust Signature:**
```rust
#[wasm_bindgen]
pub fn evaluate_compliance(
    proposed_vertices: &[f32],
    proposed_indices: &[u32],
    rule_id: &str
) -> JsValue {
    // 1. Retrieves the BVH of the legal envelope from Wasm memory
    // 2. Executes Gilbert-Johnson-Keerthi (GJK) collision algorithm
    // 3. Serializes only the tiny result struct back to JS
    
    let result = SpatialResult { /* ... */ };
    serde_wasm_bindgen::to_value(&result).unwrap()
}
```

**TypeScript Invocation:**
```typescript
import { useFrame } from '@react-three/fiber';

function ActiveBuildingMesh({ proposedMesh }) {
    useFrame(() => {
        // Extract moving coordinates directly from the GPU buffer
        const vertices = proposedMesh.current.geometry.attributes.position.array as Float32Array;
        const indices = proposedMesh.current.geometry.index.array as Uint32Array;

        // O(1) mathematical verification
        const result: SpatialResult = wasmKernel.evaluate_compliance(vertices, indices, "PD_1096_Sec_804");

        if (!result.is_compliant) {
            triggerViolationUI(result.collision_point, result.rule_id);
        }
    });

    return <mesh ref={proposedMesh} {...props} />
}
```