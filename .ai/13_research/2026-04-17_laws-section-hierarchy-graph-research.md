---
task: laws-section-hierarchy-graph
phase: 11
created: 2026-04-17
author: CODEX
status: DRAFT
---

# 2026-04-17 Laws Section-Hierarchy Graph Research

## Question
Why does BP220 appear shallow in the current knowledge graph, and what architecture change is needed so laws can contribute section / subsection / sub-subsection structure rather than only admitted concept nodes?

## Fresh evidence

### 1. BP220 currently admits only one BP220-native concept file
From `config/datasets/laws-core-bundle-m1.yaml`:
- `bp-220` admitted concept paths count: **1**
- admitted concept path:
  - `003_Canonical-Knowledge-Layer/shared/concepts/socialized-housing-projects.md`

### 2. BP220 still contributes multiple graph edges — but to shared concept nodes
From the current bounded graph snapshot:
- BP220-supported edges observed: **12**
- BP220 targets include:
  - `concept-floor-area`
  - `concept-light-and-ventilation`
  - `concept-means-of-egress`
  - `concept-setbacks`
  - `concept-socialized-housing-projects`
  - `concept-stairs`
  - `concept-yards`

### 3. BP220 clearly has rich internal structure in the refined source
From `002_Raw-Conversion-Layer/001-Laws/refined_markdown/BP-220/Revised_IRR_BP220_2008.md` and `extract_section_headers(...)`:
- extracted headers count: **60**
- examples include:
  - `RULE I GENERAL PROVISIONS`
  - `Section 1. Scope of Application`
  - `Section 2. Declaration of Policies`
  - `RULE II MINIMUM DESIGN STANDARDS AND REQUIREMENTS...`
  - `Section 3. Compliance with Standards and Guidelines`
  - `Section 5. Technical Guidelines and Standards for Subdivisions`
  - subpoints like `3. Physical Suitability`, `4. Accessibility`, `5. Setback/Yard`, etc.

### 4. The current graph contract cannot represent section hierarchy nodes
From `scripts/vitruvius/graph/contract.py`:
- allowed node types are only:
  - `source`
  - `concept`
  - `attribute`
  - `spatial_instance`
- there is no node type for:
  - section
  - subsection
  - clause
  - outline node / hierarchy node

### 5. Current snapshot node types confirm the limitation
Current bounded snapshot contains only node types:
- `source`
- `concept`

## Research conclusion
The apparent BP220 shallowness is **not** because the law has no structure.
It is because the current graph layer is a **concept graph**, not a **document structure graph**.

## Implication
To represent laws faithfully, the system likely needs a second graph layer (or an additive extension of the current one) that can model:
- law / IRR source
- rule
- section
- subsection
- clause or paragraph anchors

## Correct next step
This should be planned as a separate, additive architecture slice:
- **section-hierarchy graph model for laws**

It should not replace tranche-based laws expansion; it should complement it.

## Non-goal for the next immediate slice
- do not rewrite the current bounded graph into a full hierarchy graph in one jump
- do not block tranche-based manifest expansion on section-node modeling first
