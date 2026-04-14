---
plan_id: phase-14-autonomous-knowledge-synthesis
phase: "Phase 14 (AI Wiki & Persistent Synthesis)"
title: "Autonomous Knowledge Synthesis: The Persistent LLM Wiki"
status: planned
priority: high
sprint: "Sprint WIKI — The Compounding Asset"
version: 1.0.0
plan_type: design_spec
created: 2026-04-15
last_updated: 2026-04-15
owner: Senior Systems Architect
dependencies:
  - .ai/13_research/Building Advanced PDF-to-Graph AI Wiki.md
  - .ai/13_research/llm_wiki_architecture_guide.md
  - .ai/03_plans/phase-1b-multi-parser-integration-plan.md
---

# Phase 14 Implementation Plan: Autonomous Knowledge Synthesis

> **Objective:** Transition from episodic RAG to a **Persistent AI Wiki**. This system treats the LLM as a "maintainer" that compiles raw sources into a structured, interlinked markdown codebase, ensuring knowledge compounds over time.

## 1. Architectural Strategy: The "Compile-First" Wiki

1.  **High-Fidelity Ingestion:** Use **Docling** with the **Heron** layout engine to reconstruct PDFs into structurally accurate Markdown.
2.  **Structural Invariants:** Use **Pydantic/Instructor** to force LLMs to output strictly valid YAML frontmatter for every wiki page.
3.  **Differential Maintenance:** Only re-process "ego-graphs" (local neighborhoods) when a source changes, using SHA-256 manifest files for delta tracking.
4.  **Isomorphic Interface:** The Wiki is the source of truth, stored as Markdown files that are both human-readable (Obsidian) and machine-queryable (Kuzu/NetworkX).

---

## 2. Execution Streams

### Stream WIKI.1: Structural Ingestion (Fidelity)
**Goal:** Perfect PDF-to-Markdown conversion that preserves tables and hierarchies.
- **Task WIKI.1.1:** Integrate `docling` project with `Heron` layout model as the primary parser.
- **Task WIKI.1.2:** Implement **Multimodal Captioning**: Use Qwen2-VL to describe charts/diagrams and inject as text.
- **Task WIKI.1.3:** Implement **TableFormer** post-processing for nested regulatory tables.
- **Validation:** 95%+ accuracy on complex PD 1096 occupancy tables.

### Stream WIKI.2: The Maintainer (Orchestration)
**Goal:** LLM-driven synthesis and interlinking.
- **Task WIKI.2.1:** Implement the **"Synthesis Loop"**: LLM reads new Markdown, identifies entities, and creates/updates wiki pages.
- **Task WIKI.2.2:** Define **Structural Schemas**: Use `pydantic` to enforce `linked_entities`, `source_citations`, and `cognitive_load` fields.
- **Task WIKI.2.3:** Build the **Bidirectional Linker**: Automatic `[[link]]` generation using cosine similarity (>0.70 threshold).
- **Validation:** Zero "orphaned" pages in the ego-graph after ingesting a new chapter.

### Stream WIKI.3: Hybrid Storage (Kuzu + Markdown)
**Goal:** Fast relational queries over text files.
- **Task WIKI.3.1:** Deploy **Kuzu DB** as the embeddable graph backend.
- **Task WIKI.3.2:** Implement the **Manifest Sync**: Background job that upserts Markdown YAML frontmatter into Kuzu relational rows.
- **Task WIKI.3.3:** Integrate **pgvector** or Kuzu-native vector search for hybrid retrieval.
- **Validation:** Multi-hop query ("Laws cited by rules affecting Fire Walls") returns results in <50ms.

### Stream WIKI.4: Governance & Linting (Differential Health)
**Goal:** Maintaining graph integrity without full-rebuild costs.
- **Task WIKI.4.1:** Implement **SHA-256 Delta Tracking**: Only process files with changed hashes.
- **Task WIKI.4.2:** Build the **Ego-Graph Linter**: Pass an updated page and its depth-2 neighbors to the LLM to check for contradictions.
- **Task WIKI.4.3:** Implement **Stale Reports**: Identify wiki nodes whose source citations have been deleted or modified.
- **Validation:** Re-linting a single node takes <2s, regardless of total wiki size.

---

## 3. Tech Stack Requirements

- **Ingestion:** `docling`, `pymupdf4llm`.
- **Inference:** `vLLM` or `Ollama` with `Gemma 4 26B MoE`.
- **Graph:** `Kuzu` (Primary), `NetworkX` (Analysis).
- **Validation:** `instructor`, `pydantic`.

---

## 4. Success Metrics

| Metric | Baseline (RAG) | Target (AI Wiki) |
|---|---|---|
| **Knowledge Persistence** | Episodic (lost) | Persistent (Markdown files) |
| **Retrieval Accuracy** | Semantic-only | Hybrid (Relational + Semantic) |
| **Maintainer Overhead** | Full rebuilds | Differential updates (Delta-only) |
| **Fidelity** | Text-only | Structural (Tables + Vision Captions) |
