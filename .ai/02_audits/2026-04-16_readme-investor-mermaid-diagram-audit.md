---
task: readme-investor-mermaid-diagram
phase: "04"
created: 2026-04-16
author: IMPLEMENTER
supersedes: null
status: DRAFT
---

# README Investor Mermaid Diagram Audit — 2026-04-16

## Scope
Add an investor-readable Mermaid diagram to `README.md` that explains what Vitruvius does from source documents through current value creation and planned product direction.

## Authority and state alignment
Read and aligned with:
- `AGENTS.md`
- `.ai/00_system/EXECUTION_LOOP.md`
- `.ai/00_system/principles.md`
- `.ai/00_system/pipeline-overview.md`
- `.ai/01_roadmap/master-roadmap.md`
- `.ai/01_roadmap/current-phase.md`
- `.ai/01_roadmap/milestone-tracker.md`
- `.ai/03_plans/00-governing-implementation-plan.md`
- `.ai/03_plans/INDEX.md`
- `README.md`

## Current README reality
The README already contains:
- a high-level AEC/compound-system framing at the top
- a plain-English section
- an architecture-at-a-glance ASCII diagram
- a current-status section with phase/sprint truth

## Gap identified
The README does **not** currently contain a single concise diagram that answers an investor-style question:

> What does this product do from start to finish, and what does that become over time?

Current problems:
1. The top of the README emphasizes the future AEC engine thesis more than the currently shipped document-to-knowledge pipeline.
2. The ASCII architecture diagram is useful for engineers but not ideal for investors or non-technical readers.
3. The existing story is split across multiple sections (`plain English`, `architecture`, `current status`, `next phase`) rather than one narrative flow.
4. The README needs clearer separation between **live today** capability and **planned next** capability so it does not overclaim.

## Repo truth that the diagram must reflect
### What Vitruvius clearly does today
- takes raw technical/regulatory documents as input
- converts them into machine-readable text and structured sidecars
- refines and normalizes that text deterministically
- turns that material into canonical sources, concepts, and relationships
- runs deterministic filtering plus targeted local LLM review where ambiguity remains
- promotes reviewed records into an auditable knowledge/graph layer
- supports traceable query/answer workflows on top of that foundation

### What Vitruvius is clearly building toward
- jurisdiction-aware compliance workflows
- higher-level AEC reasoning / constraint-solving product surfaces
- broader decision-support and scenario-analysis layers over the verified knowledge substrate

### Claims the diagram should avoid
- claiming the future AEC runtime/constraint-solver product is already fully shipped
- implying free-form LLM reasoning is the main engine
- implying the current system starts and ends with a chatbot
- implying investor-visible workflow surfaces are already complete product UX layers in this repo

## Recommended README change
Add a new section immediately after `## Vitruvius in plain English`:
- section title should be investor-readable
- diagram should show a left-to-right or top-to-bottom flow
- diagram should label current pipeline stages in plain English
- diagram should include one clearly marked planned/future node
- supporting bullets should explain how to interpret the diagram

## Audit conclusion
The correct change is not a README rewrite. It is a focused README upgrade:
1. add one Mermaid section for end-to-end investor comprehension
2. explicitly separate live capability from roadmap direction
3. keep the rest of the README as the deeper technical layer
