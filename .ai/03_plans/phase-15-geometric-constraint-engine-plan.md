---
plan_id: phase-15-geometric-constraint-engine
phase: "Phase 15 (Geometric Truth)"
title: "Mathematical & Geometric Constraint Engine: The Buildable Envelope"
status: planned
priority: highest
sprint: "Sprint GEOM — Mathematical Truth"
version: 1.0.0
plan_type: design_spec
created: 2026-04-15
last_updated: 2026-04-15
owner: Senior Systems Architect
dependencies:
  - .ai/13_research/mathematical and statistical relevance of architectural constraints,.md
  - .ai/03_plans/3d-spatial-intelligence-upgrade-plan.md
---

# Phase 15 Implementation Plan: Geometric Constraint Engine

> **Objective:** Bridge the gap between text-based architectural law and **computable mathematical truth**. This system translates dimensional building codes into a unified Constraint Satisfaction Problem (CSP) for deterministic compliance and spatial optimization.

## 1. Architectural Strategy: The "Constraint Solver"

1.  **Parametric Extraction:** Move from extracting "governs" to extracting **Inequalities** ($W \ge 1.2m$, $H \le 15.0m$).
2.  **Constraint Satisfaction (CSP):** Model the building code as a set of Variables, Domains, and Constraints for a solver like **Z3** or a custom CSP engine.
3.  **Boolean Geometry:** Calculate the "Buildable Envelope" by performing geometric intersections and subtractions on lot polygons.
4.  **Pareto Frontier:** Show users the mathematically optimal solutions that maximize floor area while strictly adhering to the 100% compliance boundary.

---

## 2. Execution Streams

### Stream GEOM.1: Inequality Extraction (Math-First NLP)
**Goal:** Extract numeric constraints from legal text as formal math objects.
- **Task GEOM.1.1:** Build the **Rule-to-Formula Compiler**: Map "must not exceed" to $\le$, "minimum of" to $\ge$.
- **Task GEOM.1.2:** Implement **Unit Normalization**: (meters, feet, percentage) $\rightarrow$ meters (Standard SI).
- **Task GEOM.1.3:** Extract **Conditional Dependencies**: If `Zone == R1`, then `Setback == 4.5m`.
- **Validation:** 100% success in extracting correct inequalities from 50 sample sections of PD 1096.

### Stream GEOM.2: The CSP Solver (Z3 Integration)
**Goal:** Deterministically prove compliance without LLM "guessing."
- **Task GEOM.2.1:** Integrate **Z3 SMT Solver** as the core logic backend.
- **Task GEOM.2.2:** Map the extracted inequalities to a Z3 context.
- **Task GEOM.2.3:** Implement **Clash Detection**: Automatically find "Logical Contradictions" in the code where two rules cannot both be true.
- **Validation:** "Violation Proof": The system returns `UNSAT` (Unsatisfiable) when a building design violates any numeric rule.

### Stream GEOM.3: 3D Buildable Envelope Generator
**Goal:** Generate the absolute 3D volume of legal space.
- **Task GEOM.3.1:** Implement **Polygon Offsetting**: Subtract setbacks from the base lot polygon.
- **Task GEOM.3.2:** Build the **Voxel-Based Occupation Map**: Mark every 10cm cube as "Legal" or "Illegal."
- **Task GEOM.3.3:** Export the envelope as **GLB/OBJ** for the ILXP 3D visualizer.
- **Validation:** Visualizer shows a ghosted volume that matches the exact setback/height requirements.

### Stream GEOM.4: Multimodal Compliance Auditing
**Goal:** Comparing designs against the mathematical engine.
- **Task GEOM.4.1:** Implement the **"Geometric Audit"**: Take a user's 3D design and calculate its Intersection-over-Union (IoU) with the legal envelope.
- **Task GEOM.4.2:** Build the **Pareto Optimizer**: Simulate 1,000 massing variations to find the maximum possible Floor Area Ratio (FAR).
- **Task GEOM.4.3:** Implement **Stochastic Site Feasibility**: Monte Carlo simulations for unusually shaped lots.
- **Validation:** Audit returns "98% compliant; violation at Chapter 8, Section 804 (Setback exceedance of 20cm)."

---

## 3. Tech Stack Requirements

- **Solver:** `Z3` (Python bindings), `cvxpy` for optimization.
- **Geometry:** `Shapely` (2D), `Trimesh` (3D), `Libigl` (C++ backend).
- **Format:** `glTF` for 3D export.
- **Inference:** `Pydantic` for structured numeric schemas.

---

## 4. Success Metrics

| Metric | Baseline (Textual) | Target (Geometric) |
|---|---|---|
| **Compliance Precision** | "Likely Compliant" (LLM) | Binary 100% or 0% (CSP) |
| **Logic Verification** | Manual cross-reference | Mathematical Proof (Z3) |
| **User Visualization** | Text description | Real-time 3D Envelope |
| **Optimization** | Manual design | Mathematically Optimal Pareto Frontier |
