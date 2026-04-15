# Advanced LLM Wiki Architecture: PDF to Knowledge Graph

## Overview
This document outlines the architecture for building a persistent, compounding LLM Wiki from raw PDFs. The goal is to move beyond standard retrieval-augmented generation (RAG) by incrementally compiling knowledge into a structured, interconnected graph of markdown files that sits between you and the raw sources.

## I. Essential Python Packages

### 1. Raw Sources: PDF to Markdown Extraction
To build a reliable knowledge base, your raw sources must be converted into perfectly formatted text before the agent reads them.
* **`marker-pdf`**: Exceptional for processing technical documents. Accurately preserves complex layouts, reading orders, equations, and tables.
* **`pymupdf4llm`**: A blazing-fast, lightweight alternative built on top of PyMuPDF, designed specifically to output LLM-ready markdown.

### 2. The Maintainer: Local LLM Orchestration
* **`ollama`**: The Python client serves as the bridge to pipe parsed markdown directly into local LLMs (like Gemma 4), handling offline summarization, entity extraction, and cross-referencing.
* **`instructor`** & **`pydantic`**: Enforces strict structural invariants, ensuring that the model strictly adheres to a defined schema (outputting verified JSON that converts to YAML frontmatter) rather than drifting into freeform prose over time.

### 3. The Wiki: Graph Topology & Storage
* **`networkx`**: Essential for analyzing the shape of your wiki locally, running topological "linting", finding orphan pages, identifying hub nodes, and verifying bidirectional links.
* **`llama-index-core` (PropertyGraphIndex)**: Formalizes connections between markdown files into a queryable knowledge graph scaffolding.

### 4. Operations: Search & Tooling
* **`qmd`**: A local search engine for markdown directories providing hybrid BM25 and vector search natively. Can be exposed to the LLM via an MCP (Model Context Protocol) server so the agent can dynamically search its own memory.

---

## II. Advanced Concepts for Optimization, Efficiency, and Accuracy

### 1. Enforce Structural Invariants via Strict Schemas (Accuracy)
* **The Approach:** Treat your LLM not as a text writer, but as a structured data engine. Separate the data structure from the prose.
* **Implementation:** When the LLM processes a parsed PDF, force it to output a strict JSON payload that maps directly to your frontend type interfaces. Use `instructor` to guarantee every new markdown file contains perfect YAML frontmatter, including arrays of `linked_entities`, `source_citations`, and `confidence_scores`. 

### 2. Cryptographic Source Lineage (Truth to Source)
* **The Approach:** Guarantee the AI wiki remains true to the source material by making every claim traceable back to an exact block in the original document.
* **Implementation:** Implement deterministic hashing for your raw PDFs. The LLM must include the exact hash and chunk ID in the YAML frontmatter (e.g., `source: 8f4e2a_page_12`). If the original PDF is updated or deleted, a script can instantly query the graph to find and flag downstream markdown pages as "stale."

### 3. Hybrid Relational-Vector Indexing (Efficiency)
* **The Approach:** Mirror the structural data of the markdown files into a high-performance database layer (like Postgres/Supabase) to avoid degrading the context window by reading a massive text index on every query.
* **Implementation:** Every time a markdown file is created or updated, a background job parses its YAML frontmatter and upserts it into the database. Map bidirectional links as relational rows and store document embeddings using `pgvector`. Query by using fast relational SQL to filter the graph topologically first, *then* run semantic search on that tiny subset.

### 4. Differential Linting (Optimization)
* **The Approach:** Periodically health-checking the entire wiki is computationally expensive. Only lint the "ego-graph"—the immediate neighborhood of a change.
* **Implementation:** When a new PDF is ingested and a concept page is updated, do not lint the whole wiki. Pass only the updated page and its immediate neighbors (depth of 1 or 2 links) to the local LLM to check strictly for contradictions or missing cross-references within that localized cluster.

### 5. Inject Cognitive Metadata for ILXPs (Smarter Systems)
* **The Approach:** If feeding an Interactive Learning Experience Platform (ILXP), the knowledge graph needs to understand the psychological weight of the material to aid in student retention and mental efficiency.
* **Implementation:** Program the ingestion prompt to evaluate the educational friction of the source text. Have the LLM append pedagogical metadata to the frontmatter, such as:
    * `cognitive_load`: High/Medium/Low (based on technical density)
    * `prerequisites`: Which other markdown nodes must be understood first
    * `common_misconceptions`: Identified traps in the logic
    * `tension_points`: Areas where this source contradicts another source
    
This allows the frontend testing engine to dynamically build spaced-repetition paths based on inherent difficulty rather than serving random wiki pages.
