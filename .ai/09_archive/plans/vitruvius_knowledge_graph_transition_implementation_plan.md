# Vitruvius — Knowledge Graph Transition & Implementation Plan

**Prepared:** 2026-04-18  
**Status:** Proposed implementation directive  
**Audience:** Vitruvius codebase AI, engineering, data pipeline, retrieval, and graph layers  
**Purpose:** Transition Vitruvius from a document-centric graph into a citable, explainable, taxonomy-centered knowledge system without breaking the existing ingestion roadmap.

---

## 0. Executive decision

Vitruvius should **stop treating documents as the primary graph spine**. Documents are evidence, not the ontology.  
The new architecture should be built around a **taxonomy-centered canonical knowledge graph**, backed by a separate **evidence graph** that stores documents, sections, chunks, and exact evidence spans.

### Non-negotiable rules

1. **Primary nodes are knowledge units**, not files.
2. **Every user-visible node must be backed by evidence.**
3. **Every user-visible edge must be explainable.**
4. **Every explanation must link to the source document at span/page/section level.**
5. **AI proposes structure; the system promotes only validated structure.**
6. **Canonical graph and evidence graph must be separated.**
7. **Do not chase ontology purity.** Use a pragmatic property-graph implementation now; add RDF/ontology exports later if needed.
8. **Do not regenerate the whole graph on every ingestion.** Use incremental updates and localized recomputation.

---

## 1. Why this transition is necessary

The current graph direction is upside down if its primary nodes are documents.  
That produces a file cabinet with semantic decorations, not a knowledge base.

### What is wrong with a document-primary graph

- Documents are containers, not concepts.
- Documents mix multiple ideas, levels, exceptions, and contexts.
- Documents are bad primary units for quiz generation, rule lookup, semantic traversal, and concept reuse.
- Documents make the graph brittle: every new file distorts structure instead of strengthening it.
- Documents do not explain **why** two concepts are related. They only co-locate them.

### What the graph should represent instead

Vitruvius should represent:

- taxonomies
- topics
- subtopics
- concepts
- rules
- definitions
- procedures
- exceptions
- constraints
- terms / aliases
- evidence supporting all of the above

### Strategic framing

This refactor does **not** replace the earlier roadmap around:

- multi-parser integration
- centralized normalization
- review / validation layers

It depends on them.

The earlier pipeline still stands:

```text
Raw docs
-> parsing / OCR
-> normalization
-> extraction
-> canonicalization
-> graph placement
-> validation
-> retrieval
```

The change is that the graph target is now **knowledge-first and evidence-backed**, not **document-first**.

---

## 2. Target state architecture

Vitruvius should operate as four connected layers:

```text
[1] Source Layer
    Raw PDF / Markdown / HTML / scans / code / standards / books

[2] Evidence Layer
    Document -> version -> section -> chunk -> evidence span

[3] Canonical Knowledge Layer
    Taxonomy -> topic -> subtopic -> concept -> rule/definition/procedure/exception

[4] Assertion / Explanation Layer
    Addressable relationship assertions with reasoning summary + provenance
```

### High-level graph model

```text
(DocumentVersion)-[:HAS_SECTION]->(Section)-[:HAS_CHUNK]->(Chunk)-[:HAS_SPAN]->(EvidenceSpan)

(CanonicalNode)<-[:FROM]-(Assertion)-[:TO]->(CanonicalNode)
(Assertion)-[:SUPPORTED_BY]->(EvidenceSpan)
(Assertion)-[:GENERATED_BY]->(ExtractionRun)
(Assertion)-[:REVIEWED_BY]->(Review)
```

### What users should see

By default, the visible graph in the product should be the **canonical graph**, not the evidence graph.

- graph canvas: canonical nodes + semantic edges
- node click: definition, placement, related nodes, supporting evidence
- edge click: explanation, confidence, inference type, supporting sources, direct links to documents

Evidence nodes should live in the side panel / inspector / detail views, not clutter the main graph.

---

## 3. Design principles

### 3.1 Canonical before evidentiary display
The user should explore knowledge first, documents second.

### 3.2 Evidence is first-class data, not metadata
Evidence must be modeled explicitly and queryably.

### 3.3 Reified assertions, not dumb edges
A relationship must be an addressable object if you want it to be explainable and citable.

### 3.4 AI is an extractor and organizer, not the source of truth
AI may propose nodes, edges, placements, summaries, merges, and labels.  
It must not directly define canonical truth without evidence and validation.

### 3.5 Deterministic backbone, AI-assisted interpretation
Structure must be schema-bound, type-safe, and confidence-scored.  
Interpretation can be AI-assisted.

### 3.6 Version everything that matters
Documents, evidence spans, assertions, and canonical merges must be revision-aware.

### 3.7 Separate online from offline work
Heavy clustering, graph analytics, and taxonomy refinement belong in background jobs, not the request path.

### 3.8 Keep the top of the taxonomy tighter than the leaves
Top-level taxonomy should be seeded and curated.  
AI should be allowed more freedom deeper in the tree, not at the root.

---

## 4. Canonical graph vs evidence graph

This is the most important structural decision.

## 4.1 Canonical Knowledge Graph (clean graph)

This is the graph that powers:

- graph browsing
- semantic navigation
- quiz / drill generation
- rule lookup
- concept retrieval
- graph-based answer composition
- dependency reasoning

### Canonical node classes

Use these as the starting set:

- `taxonomy`
- `topic`
- `subtopic`
- `concept`
- `term`
- `definition`
- `rule`
- `procedure`
- `exception`
- `constraint`
- `example`

### Canonical edge classes

Use these as the starting set:

- `HAS_CHILD`
- `BELONGS_TO`
- `RELATED_TO`
- `DEFINED_BY`
- `DEPENDS_ON`
- `APPLIES_TO`
- `OVERRIDES`
- `CONTRADICTS`
- `SAME_AS`
- `PART_OF`
- `REQUIRES`
- `EXCLUDES`

You can add more later, but do not start with 50 edge types.

## 4.2 Evidence Graph (messy graph)

This graph captures source structure and provenance.

### Evidence node classes

- `document`
- `document_version`
- `section`
- `chunk`
- `evidence_span`
- `citation`
- `parser_run`
- `ocr_run`
- `normalization_run`
- `extraction_run`
- `review`

### Evidence graph purpose

- preserve source traceability
- preserve parser provenance
- allow exact citation / highlighting
- support reprocessing without corrupting canonical structure
- let the system explain where every claim came from

## 4.3 Assertion Layer

A relationship is not just an edge. It is a claim.

### Assertion classes

At minimum:

- `node_assertion`  
  (“this canonical node exists and is defined this way”)

- `relationship_assertion`  
  (“node A depends on / defines / relates to node B”)

- `placement_assertion`  
  (“this node belongs under this parent in the taxonomy”)

- `merge_assertion`  
  (“these two candidates represent the same canonical unit”)

### Why assertions matter

Without assertions, you cannot answer:

- why are these two nodes linked?
- is this edge direct or inferred?
- what source supports it?
- which model or rule generated it?
- was it reviewed?
- when did it change?

---

## 5. Recommended storage architecture

Use a pragmatic stack.

## 5.1 Recommended baseline

### A. Object storage / file storage
Store raw PDFs, Markdown, images, and rendered derivatives.

### B. PostgreSQL
Use as the authoritative registry for:

- file registry
- versions
- job state
- evaluation results
- audit events
- feature flags
- review queues
- migration mappings
- canonical merge tables
- user feedback / correction data

### C. Neo4j
Use as the main graph database for:

- canonical nodes
- assertions
- evidence graph relationships
- semantic traversals
- materialized fast edges
- node / assertion embeddings if you want a simpler single-system first version

### D. Optional retrieval accelerator: Qdrant
Add only if you need stronger retrieval pipelines than Neo4j alone can comfortably provide:

- chunk retrieval at scale
- hybrid lexical + dense retrieval
- RRF fusion
- reranking pipelines
- multivector / late-interaction search experiments

### Recommendation
Start with **Postgres + Neo4j + file storage**.  
Add **Qdrant** when retrieval quality / latency / experimentation requirements justify the extra operational complexity.

## 5.2 Why not one giant “everything” store

Because the access patterns are different:

- files: immutable blobs
- metadata/jobs/audit: relational
- semantic traversal: graph
- large-scale retrieval/reranking: vector / hybrid search engine

Trying to make one store do all of this usually leads to awkward compromises.

---

## 6. Data model specification

## 6.1 Canonical node schema

```json
{
  "id": "concept-means-of-egress",
  "type": "concept",
  "label": "Means of Egress",
  "slug": "means-of-egress",
  "summary": "A continuous and unobstructed path of travel from any occupied portion of a building to a public way.",
  "taxonomy_path": [
    "Architecture",
    "Code Compliance",
    "Fire and Life Safety",
    "Means of Egress"
  ],
  "aliases": ["egress", "exit path"],
  "status": "validated",
  "confidence": 0.97,
  "created_at": "2026-04-18T00:00:00Z",
  "updated_at": "2026-04-18T00:00:00Z",
  "version": 3
}
```

### Required fields

- `id`
- `type`
- `label`
- `status`
- `confidence`
- `version`

### Strongly recommended fields

- `summary`
- `taxonomy_path`
- `aliases`
- `embedding_ref`
- `primary_assertion_id`

## 6.2 Relationship assertion schema

This is the core object for clickable edges.

```json
{
  "id": "assert-rule-depends-on-occupant-load-0001",
  "assertion_type": "relationship_assertion",
  "edge_type": "DEPENDS_ON",
  "from_node_id": "rule-minimum-corridor-width",
  "to_node_id": "concept-occupant-load",
  "reasoning_summary": "Minimum corridor width requirements vary according to occupant load thresholds defined in the source code provisions.",
  "reasoning_detail": [
    "Source text defines minimum width requirements for egress components.",
    "The same provision qualifies those requirements by occupant load conditions.",
    "Therefore corridor width depends on occupant load."
  ],
  "inference_type": "direct_citation",
  "confidence": 0.94,
  "validation_status": "validated",
  "created_by": {
    "mode": "hybrid",
    "model": "local-llm",
    "pipeline_stage": "edge_extraction"
  },
  "review_state": "approved",
  "evidence_ids": [
    "span-pd1096-irr-v1-p087-b03",
    "span-pd1096-irr-v1-p087-b04"
  ],
  "document_version_ids": [
    "docv-pd1096-irr-v1"
  ],
  "created_at": "2026-04-18T00:00:00Z",
  "updated_at": "2026-04-18T00:00:00Z",
  "version": 2
}
```

### Required fields

- `id`
- `edge_type`
- `from_node_id`
- `to_node_id`
- `reasoning_summary`
- `inference_type`
- `confidence`
- `validation_status`
- `evidence_ids`

## 6.3 Evidence span schema

```json
{
  "id": "span-pd1096-irr-v1-p087-b03",
  "document_id": "doc-pd1096-irr",
  "document_version_id": "docv-pd1096-irr-v1",
  "mime_type": "application/pdf",
  "selector": {
    "kind": "pdf_bbox",
    "page": 87,
    "bbox": [72.1, 144.0, 381.4, 175.8]
  },
  "quote": "Stairways, ramps, horizontal exits and passageways shall form part of the required means of egress...",
  "normalized_text": "Stairways, ramps, horizontal exits and passageways shall form part of the required means of egress...",
  "deep_link": "/viewer/doc-pd1096-irr/docv-pd1096-irr-v1?page=87&bbox=72.1,144.0,381.4,175.8",
  "parser": "pymupdf",
  "parser_version": "1.27.x",
  "ingestion_run_id": "ingest-2026-04-18-0001",
  "checksum": "sha256:...",
  "created_at": "2026-04-18T00:00:00Z"
}
```

### Markdown evidence selector example

```json
{
  "kind": "markdown_range",
  "heading_path": ["Rule VII", "Means of Egress"],
  "line_start": 120,
  "line_end": 128,
  "char_start": 3421,
  "char_end": 3678
}
```

## 6.4 Document version schema

Never cite a floating file without version context.

```json
{
  "id": "docv-pd1096-irr-v1",
  "document_id": "doc-pd1096-irr",
  "title": "PD 1096 IRR Volume 1",
  "source_uri": "/docs/pd1096-irr-v1.pdf",
  "mime_type": "application/pdf",
  "sha256": "sha256:...",
  "created_at": "2026-04-18T00:00:00Z",
  "supersedes": null
}
```

### Rule
Evidence spans attach to `document_version`, not just `document`.

That is how citations survive future document updates.

---

## 7. Provenance and citation model

Vitruvius needs a provenance model, but it does **not** need to become a full semantic-web triple-store on day one.

### Recommendation

Use a **property graph implementation inspired by**:

- PROV-O concepts (`Entity`, `Activity`, `Agent`, qualified provenance)
- W3C Web Annotation selectors for targeting content segments
- PDF fragment conventions and text fragment conventions for deep links

### Pragmatic mapping

| Concept | Vitruvius implementation |
|---|---|
| PROV Entity | document version, chunk, evidence span, canonical node, assertion |
| PROV Activity | parser run, OCR run, extraction run, merge run, review action |
| PROV Agent | local model, cloud model, human reviewer, system job |
| Qualified provenance | assertion object with attached evidence and method metadata |
| Annotation selector | selector JSON for page / bbox / line / char / heading path |

### Important implementation decision

**Do not store model chain-of-thought.**  
Store a concise **reasoning summary** and optional structured reasoning steps.  
That is enough for explainability and avoids over-coupling to hidden model internals.

### Minimum provenance fields for every assertion

- creation method
- model or rule name
- model version / pipeline version
- evidence ids
- confidence
- review state
- timestamp
- source document versions

---

## 8. Citability requirements

Citability must exist for both nodes and edges.

## 8.1 Node click requirements

When a user clicks a node, the system must be able to show:

- canonical label
- node type
- summary / definition
- taxonomy placement
- aliases / synonyms
- supporting sources
- exact evidence spans
- confidence
- last validation state

## 8.2 Edge click requirements

When a user clicks a visible connection, the system must be able to show:

- relationship label
- why the connection exists
- whether the connection is direct or inferred
- which evidence supports it
- which source documents support it
- confidence score
- extraction / validation method
- deep links to the evidence locations

### Minimum edge click payload

```json
{
  "assertion_id": "assert-rule-depends-on-occupant-load-0001",
  "edge_type": "DEPENDS_ON",
  "from_node": {
    "id": "rule-minimum-corridor-width",
    "label": "Minimum Corridor Width"
  },
  "to_node": {
    "id": "concept-occupant-load",
    "label": "Occupant Load"
  },
  "reasoning_summary": "Minimum corridor width requirements vary according to occupant load thresholds defined in the source code provisions.",
  "inference_type": "direct_citation",
  "confidence": 0.94,
  "evidence": [
    {
      "document_title": "PD 1096 IRR Volume 1",
      "document_version_id": "docv-pd1096-irr-v1",
      "page": 87,
      "quote": "....",
      "deep_link": "/viewer/doc-pd1096-irr/docv-pd1096-irr-v1?page=87&bbox=..."
    }
  ]
}
```

## 8.3 Direct vs inferred edges

Do not flatten all edges into the same trust level.

### Allowed inference types

- `direct_citation`
- `taxonomy_placement`
- `rule_based_derivation`
- `semantic_similarity`
- `multi_hop_inference`
- `human_authored`

### Policy

- `direct_citation` can be promoted with strong evidence.
- `taxonomy_placement` can be promoted if parent confidence is high and top-level drift is controlled.
- `semantic_similarity` alone should **not** create user-visible truth without confirmation.
- `multi_hop_inference` must expose the chain of supporting assertions.

---

## 9. Deep-linking to PDFs and Markdown

The graph is not citable if it only points to filenames.

## 9.1 PDF linking

For PDFs, store:

- document version id
- page number
- bbox when available
- quoted text
- optional viewer link

### Notes
If you expose raw PDF URLs, standard PDF open parameters can target pages, named destinations, zoom, view rectangles, and highlights.  
Inside Vitruvius, it is better to interpret your own selector JSON and drive the PDF viewer precisely.

### Recommended internal format

```text
/viewer/:document_id/:document_version_id?page=87&bbox=72.1,144.0,381.4,175.8
```

## 9.2 Markdown linking

For Markdown, store:

- heading path
- line range
- character range
- quote
- rendered anchor id if available

### Recommended internal format

```text
/viewer/:document_id/:document_version_id#heading=rule-vii/means-of-egress&line=120-128
```

## 9.3 Selector priority

When resolving a span, prefer:

1. exact page + bbox + quote
2. page + quote
3. heading path + line range + quote
4. char range + checksum fallback
5. document-only fallback

The quote is important because it helps survive layout drift.

---

## 10. Migration strategy from the existing graph

Do not destroy the current graph first.  
Migrate in parallel.

## Phase 0 — Freeze the schema direction
**Goal:** Stop adding new conceptual debt.

### Actions

- stop creating new document-primary canonical nodes
- preserve old graph for compatibility only
- define the new schemas and ids
- add a legacy mapping table:
  - `legacy_node_id -> new_entity_id(s)`
  - `legacy_edge_id -> new_assertion_id`

## Phase 1 — Build the evidence graph first
**Goal:** Move current document-derived nodes into the correct layer.

### Actions

- ingest documents into:
  - `document`
  - `document_version`
  - `section`
  - `chunk`
  - `evidence_span`
- preserve parser / OCR metadata
- generate stable deep links
- attach raw text, normalized text, and selectors

### Output
A reliable evidence graph with no taxonomy assumptions yet.

## Phase 2 — Extract atomic knowledge units
**Goal:** Stop extracting paragraph-sized blobs.

### Actions

Extract structured candidates from chunks:

- concepts
- definitions
- rules
- procedures
- exceptions
- constraints
- aliases / terms
- edge candidates
- rationale summaries
- supporting span ids

All extraction outputs must be valid structured JSON.

## Phase 3 — Canonicalize and place
**Goal:** Turn noisy candidates into reusable knowledge objects.

### Actions

- normalize casing and naming
- dedupe exact / near duplicates
- resolve aliases
- create canonical ids
- place nodes into seeded taxonomy
- create placement assertions
- send ambiguous items to review queue

### Policy
Seed the top 1–2 levels of the taxonomy manually.  
Allow AI to propose deeper placements.

## Phase 4 — Build assertions and materialized edges
**Goal:** Make edges explainable and fast.

### Actions

- create `relationship_assertion` objects for all candidate edges
- attach reasoning summary + evidence ids
- validate
- materialize a fast traversal edge only for validated assertions

### Materialized edge pattern

Keep both:

1. **source of truth**: assertion node / record
2. **fast graph edge**: direct relationship with `assertion_id`

Example:

```text
(rule-minimum-corridor-width)-[:DEPENDS_ON {assertion_id: "..."}]->(concept-occupant-load)
```

This lets the UI click the edge and resolve full explanation from the assertion record.

## Phase 5 — Switch product queries
**Goal:** Make the app use the new graph.

### Actions

- search concepts and rules first, documents second
- graph UI uses canonical nodes
- edge inspector resolves assertion data
- answer generation uses canonical nodes + evidence spans
- quizzes use canonical rules / concepts, not chunks

## Phase 6 — Deprecate legacy document-primary graph
**Goal:** Remove the old spine without losing traceability.

### Actions

- keep legacy mapping for compatibility
- stop writing to old structures
- archive old visualizations if needed
- remove old query paths after parity is confirmed

---

## 11. Extraction and normalization pipeline

This plan preserves earlier roadmap priorities.

## 11.1 Parsing and OCR

Use a multi-parser strategy.

### Recommended parsing mix

- PyMuPDF for fast extraction, block / word coordinates, and layout-aware text structures
- Unstructured for semantically typed elements and higher-resolution partitioning on difficult documents
- OCR fallback for scanned/image-heavy files
- optional external/cloud enrichment only where local extraction fails or confidence is low

### Why this matters

- PDFs often have broken reading order
- scans need OCR
- layout matters for citation precision
- tables and lists need structure-aware parsing

## 11.2 Normalization

Normalization remains the backbone.

### Normalize to a canonical element schema

Every parsed output should be normalized into a shared internal representation, e.g.:

```json
{
  "document_version_id": "docv-...",
  "page": 87,
  "section_path": ["Rule VII", "Means of Egress"],
  "element_type": "NarrativeText",
  "text": "...",
  "bbox": [72.1, 144.0, 381.4, 175.8],
  "line_range": [120, 128],
  "parser": "unstructured-hi-res"
}
```

### Rule
No downstream extractor should consume raw parser output directly.

Everything should consume normalized elements only.

## 11.3 Chunking

Chunking must respect structure.

### Chunk boundaries should be based on

- section boundaries
- lists
- tables
- paragraphs
- semantic breaks
- page continuity where needed

### Do not chunk blindly by tokens
You will destroy evidence traceability and legal meaning.

---

## 12. AI orchestration plan

This is where the local/cloud hybrid becomes useful.

## 12.1 What local models should do

Use local models (Gemma-family / Llama-family or equivalent) for:

- first-pass entity extraction
- type classification
- alias extraction
- relation candidate generation
- taxonomy candidate generation
- cluster labeling
- nightly graph maintenance
- low-cost reruns over large corpora

## 12.2 What cloud models should do

Use cloud models for:

- ambiguous canonical merges
- hard parent-placement decisions
- cross-document legal reasoning
- difficult contradiction / override detection
- high-value explanation cleanup
- evaluation / adjudication jobs

## 12.3 Deterministic code must still do this

- schema validation
- id generation
- duplicate blocking
- confidence thresholding
- promotion rules
- review routing
- merge tracking
- provenance logging

### Principle
**AI proposes. Deterministic logic decides what is promotable.**

---

## 13. Structured output requirements

This is mandatory.

Every extraction, classification, placement, merge, and assertion-generation task must use **schema-constrained structured outputs**.

### Why

Free-form model output is where graph quality dies.

### Required pattern

- one task per model call
- one schema per task
- no “do everything in one prompt” jobs
- every output validated before persistence
- invalid outputs retried or rejected

## 13.1 Recommended local structured output options

### Option A — vLLM
Strong option if you are serving local models at higher throughput.

### Option B — llama.cpp grammar / JSON schema
Strong option if you are running GGUF models locally and want hard constraints.

### Option C — Outlines
Good provider-agnostic layer across OpenAI, llama.cpp, vLLM, MLX, etc.

## 13.2 Recommended cloud structured output

Use JSON-schema-based structured outputs for all cloud extraction tasks.

## 13.3 Important implementation note

If using llama.cpp JSON schemas, keep schemas practical:

- prefer simple nested objects
- avoid exotic schema features
- avoid deep `$ref` nesting
- avoid unsupported patterns / advanced conditionals
- explicitly describe expected structure in the prompt, because grammar constraint alone does not teach the model the semantics

---

## 14. Taxonomy self-organization strategy

You said you no longer want to be a purist because AI is available.  
That is correct — but it still needs guardrails.

## 14.1 Seed top-level taxonomies manually

Do **not** let AI invent the top of the ontology freely.

For architecture/legal initial scope, hand-seed top-level domains such as:

- Architecture
- Building Code
- Fire and Life Safety
- Accessibility
- Structural
- MEP
- Site Planning
- Definitions
- Procedures
- Compliance Checks

These are examples, not fixed truth.

## 14.2 Let AI organize below the root

AI can propose:

- subtopics
- concept clusters
- rule placements
- alias groups
- cross-links
- merge candidates

### Promotion rules for new branches

- new top-level branch: human or strong review required
- new second-level branch: high threshold + multi-evidence support
- deeper leaf branches: can be auto-promoted if confidence and evidence are strong

## 14.3 Recommended self-organization algorithm

### Stage A — Candidate generation
From chunks, extract atomic candidates.

### Stage B — Candidate normalization
Normalize labels and classify candidate type.

### Stage C — Candidate deduplication
Use:
- exact string rules
- normalized label match
- alias dictionary
- embedding similarity
- pairwise merge adjudication

### Stage D — Parent assignment
Try in order:

1. deterministic taxonomy rules
2. nearest-neighbor among existing nodes
3. cluster-based parent suggestion
4. AI adjudication
5. review queue if still ambiguous

### Stage E — Cross-linking
Generate related / depends-on / applies-to / same-as / overrides / contradicts candidates.

### Stage F — Evidence-backed promotion
No promotion without evidence.

## 14.4 Use graph algorithms offline, not inline

Use graph analytics for maintenance jobs, not for the request path.

### Good offline uses

- community detection for orphan concept clustering
- node embeddings for graph similarity
- topological link prediction for edge suggestions
- inconsistency detection / orphan detection

### Bad inline use
Running expensive graph analytics every time a user clicks a node.

---

## 15. Retrieval architecture

Vitruvius should retrieve **knowledge-first, evidence-second**.

## 15.1 Search strategy

### For user query
1. search canonical nodes and assertion summaries
2. expand relevant graph neighborhood
3. retrieve supporting evidence spans / chunks
4. build answer with citations

### Result ranking
Prioritize:

1. validated canonical nodes
2. validated assertions
3. high-confidence evidence spans
4. source documents

Documents should appear as supporting evidence unless the user specifically asks for documents.

## 15.2 Hybrid retrieval recommendation

Use a hybrid mix:

- lexical retrieval
- dense retrieval
- graph neighborhood expansion
- reranking

### Do not rely on embeddings alone
Embeddings are retrieval aids, not knowledge structure.

## 15.3 Recommended retrieval target objects

Index these:

- chunk text
- canonical node summaries
- assertion reasoning summaries
- definitions
- rule texts

### Do not over-index raw file blobs
Index normalized, structured units.

---

## 16. Performance strategy

Performance matters at both ingest time and query time.

## 16.1 Ingest-time performance

### Rules

- parse once, persist normalized evidence
- do not re-parse on every query
- cache embeddings
- batch local extraction jobs
- separate hot and cold documents
- version immutably
- recompute only affected subgraphs

## 16.2 Query-time performance

### Rules

- query canonical graph first
- materialize validated fast edges
- keep heavy evidence nodes out of default graph canvases
- load evidence lazily when inspector opens
- cache common node neighborhoods
- precompute taxonomy paths
- precompute canonical summaries
- precompute “best evidence span” per node and per assertion

## 16.3 Background jobs

Run offline jobs for:

- reclustering
- merge suggestions
- stale assertion review
- orphan detection
- contradiction surfacing
- broken deep-link repair
- embedding refresh
- taxonomy relabel suggestions

---

## 17. Confidence, validation, and promotion policy

Without a promotion system, the graph becomes semantic sludge.

## 17.1 Status model

Use explicit statuses for both nodes and assertions:

- `candidate`
- `validated`
- `review_required`
- `rejected`
- `deprecated`
- `superseded`

## 17.2 Promotion rules for canonical nodes

A node can become `validated` only if:

- type is valid
- id is stable
- evidence count >= 1
- summary exists
- taxonomy placement exists
- no unresolved hard-duplicate conflict exists

## 17.3 Promotion rules for assertions

An assertion can become `validated` only if:

- source and target types are allowed
- reasoning summary exists
- evidence count >= 1
- inference type is declared
- confidence threshold met
- no contradiction blocker exists

## 17.4 Hard rejection rules

Reject automatically when:

- no evidence exists
- selector cannot resolve
- source quote is empty
- output schema invalid
- node type impossible for context
- edge type invalid for source/target types
- duplicate collision unresolved
- inferred edge presented as direct citation

---

## 18. UI / API contract implications

This refactor should directly improve the product.

## 18.1 Graph UI

Default view:
- canonical nodes only
- simplified semantic edges only

Inspector:
- node details
- assertion details
- evidence cards
- document deep links

## 18.2 Drill / quiz system

Quiz generation should operate over:

- canonical concept nodes
- validated rule nodes
- supported definitions
- supported exceptions

Not over arbitrary chunks.

## 18.3 Admin / review tools

You need admin tooling for:

- pending candidates
- merge suggestions
- low-confidence placements
- broken citations
- unresolved contradictions
- orphan concepts
- document reprocessing diffs

---

## 19. Concrete implementation directives for the codebase AI

The following directives should be treated as implementation rules.

### Directive 1
Do not create new primary graph nodes from raw documents.

### Directive 2
Introduce separate entity types for:
- `document`
- `document_version`
- `section`
- `chunk`
- `evidence_span`
- `canonical_node`
- `assertion`

### Directive 3
Treat the assertion as the source of truth for edges.

### Directive 4
Materialize direct fast edges only from validated assertions.

### Directive 5
Every visible edge must carry an `assertion_id`.

### Directive 6
Every assertion must store:
- reasoning summary
- inference type
- evidence ids
- confidence
- creation method
- validation state

### Directive 7
All LLM extraction jobs must use structured outputs.

### Directive 8
All evidence spans must point to a document version and a selector.

### Directive 9
All source documents must be versioned immutably.

### Directive 10
The UI must resolve edge clicks through assertion records, not through raw relationship labels alone.

---

## 20. Suggested API endpoints

These are implementation-oriented suggestions, not rigid doctrine.

### Ingestion

- `POST /ingest/document`
- `POST /ingest/document/:documentVersionId/parse`
- `POST /ingest/document/:documentVersionId/extract`
- `POST /ingest/document/:documentVersionId/canonicalize`

### Graph

- `GET /graph/node/:id`
- `GET /graph/node/:id/neighborhood`
- `GET /graph/assertion/:id`
- `GET /graph/assertion/:id/evidence`
- `GET /graph/taxonomy/:id/tree`

### Evidence

- `GET /evidence/span/:id`
- `GET /evidence/document/:documentVersionId`
- `GET /evidence/document/:documentVersionId/sections`

### Review

- `GET /review/candidates`
- `POST /review/assertion/:id/approve`
- `POST /review/assertion/:id/reject`
- `POST /review/node/:id/merge`
- `POST /review/node/:id/reclassify`

---

## 21. Example Pydantic / TypeScript style contracts

## 21.1 Python example

```python
from typing import Literal, List, Optional
from pydantic import BaseModel, Field

NodeType = Literal[
    "taxonomy", "topic", "subtopic", "concept", "term",
    "definition", "rule", "procedure", "exception",
    "constraint", "example"
]

InferenceType = Literal[
    "direct_citation", "taxonomy_placement", "rule_based_derivation",
    "semantic_similarity", "multi_hop_inference", "human_authored"
]

ValidationState = Literal[
    "candidate", "validated", "review_required", "rejected",
    "deprecated", "superseded"
]

class Selector(BaseModel):
    kind: Literal["pdf_bbox", "pdf_page", "markdown_range", "text_range"]
    page: Optional[int] = None
    bbox: Optional[List[float]] = None
    heading_path: Optional[List[str]] = None
    line_start: Optional[int] = None
    line_end: Optional[int] = None
    char_start: Optional[int] = None
    char_end: Optional[int] = None

class EvidenceSpan(BaseModel):
    id: str
    document_id: str
    document_version_id: str
    selector: Selector
    quote: str
    normalized_text: str
    deep_link: str
    parser: str
    parser_version: Optional[str] = None
    checksum: str

class CanonicalNode(BaseModel):
    id: str
    type: NodeType
    label: str
    summary: str
    taxonomy_path: List[str] = Field(default_factory=list)
    aliases: List[str] = Field(default_factory=list)
    status: ValidationState
    confidence: float

class RelationshipAssertion(BaseModel):
    id: str
    edge_type: str
    from_node_id: str
    to_node_id: str
    reasoning_summary: str
    inference_type: InferenceType
    confidence: float
    validation_status: ValidationState
    evidence_ids: List[str]
```

## 21.2 Materialization pseudocode

```python
def promote_relationship_assertion(assertion):
    if assertion.validation_status != "validated":
        return

    if not assertion.evidence_ids:
        raise ValueError("validated assertion requires evidence")

    materialize_fast_edge(
        from_node_id=assertion.from_node_id,
        to_node_id=assertion.to_node_id,
        edge_type=assertion.edge_type,
        assertion_id=assertion.id,
        confidence=assertion.confidence,
    )
```

---

## 22. Evaluation plan

If this transition is not measured, it will drift.

## 22.1 Build a gold dataset

Use a representative seed set of documents from your current architectural/legal corpus.

The gold set should include:

- clean PDFs
- scanned PDFs
- Markdown
- tables
- sections with exceptions
- cross-references
- definition-heavy sections
- rule-heavy sections

## 22.2 Evaluate these separately

### A. Parsing quality
- text recovery
- section detection
- page/span fidelity

### B. Extraction quality
- correct node type
- correct label
- correct rule / definition boundary

### C. Canonicalization quality
- merge precision
- merge recall
- alias correctness

### D. Taxonomy placement quality
- parent correctness
- top-level drift rate

### E. Edge quality
- precision of relation type
- correctness of explanation
- evidence support correctness

### F. Citation quality
- link resolves
- highlight resolves
- quote matches source

## 22.3 Minimum acceptance criteria

The new graph is not production-ready until:

- 100% of visible nodes have evidence
- 100% of visible edges resolve to an assertion record
- 100% of visible assertions have a reasoning summary
- 100% of evidence links resolve to a source location
- taxonomy roots are stable
- legacy graph parity is acceptable for key product flows

---

## 23. Anti-patterns to avoid

These are failure modes.

### 23.1 Letting documents stay primary
This keeps the graph semantically wrong.

### 23.2 Storing only embeddings
Embeddings do not replace ontology, provenance, or explainability.

### 23.3 Letting AI freely invent the graph
That creates graph-shaped hallucinations.

### 23.4 Mixing canonical and evidence nodes in the main UX graph
That makes the graph unreadable.

### 23.5 Using free-form model output
That destroys reliability and slows everything down with retries and hand-cleaning.

### 23.6 Recomputing the full graph on every file update
That is wasteful and destabilizes ids.

### 23.7 Treating similarity as proof
Similarity suggests candidates. It does not prove truth.

### 23.8 Using BM42 as a production default without proof
Do not do that. If you use Qdrant, favor measured hybrid pipelines and treat BM42 as experimental unless your own evals prove it.

### 23.9 Depending on experimental libraries as core truth infrastructure
Use experimental packages carefully. Do not hardwire the entire platform around unstable experimental builders.

---

## 24. First implementation sprint recommendation

If starting now, the first sprint should not try to solve everything.

## Sprint 1 objectives

### A. Freeze the new schema
Implement:
- canonical node type enum
- assertion type enum
- evidence span schema
- document version schema

### B. Build the evidence graph
For PDF + Markdown first:
- ingest
- version
- section/chunk/span storage
- deep links

### C. Build one structured extraction pipeline
For a small subset:
- concept extraction
- rule extraction
- definition extraction
- relationship assertion extraction

### D. Build one inspector view
Make edge click show:
- assertion summary
- evidence quote
- source doc link

### E. Add promotion states
Nothing user-visible unless validated.

## Deliverable of Sprint 1
A minimal end-to-end flow where:

1. a document is ingested
2. evidence spans are stored
3. one concept-to-rule edge is created as an assertion
4. clicking the edge shows explanation + citation

If that works, the architecture is real.

---

## 25. Research-informed recommendations

This section captures external implementation-relevant findings that should influence the build.

### 25.1 Provenance should be modeled explicitly
W3C PROV-O provides a stable conceptual basis for expressing provenance across systems and supports specialization for domain-specific provenance.  
Use it as conceptual guidance, not as a reason to overcomplicate the implementation.

### 25.2 Evidence selectors should target sub-resources, not just files
The Web Annotation Data Model is useful because it treats annotations as targetable to specific data points or segments of content.  
This maps well to Vitruvius evidence spans.

### 25.3 PDF links can target more than just a file
The PDF media type supports fragment parameters such as `page`, `nameddest`, `zoom`, `viewrect`, and `highlight`.  
This supports deep-link thinking even if the app ultimately uses its own viewer routing.

### 25.4 Plain text / Markdown linking should use positions and ranges
Text fragment identifiers for plain text support character and line positions/ranges.  
Even if you do not expose the RFC syntax directly, the selector design should follow the same logic.

### 25.5 PDF extraction should preserve coordinates
PyMuPDF exposes blocks, words, and coordinates. It also warns that extracted text may not appear in natural reading order unless reordered.  
This is important for both citation fidelity and normalization.

### 25.6 Partitioning strategy must be quality-aware
Unstructured separates fast rule-based partitioning from higher-resolution model-based partitioning.  
This aligns with the Vitruvius need for a multi-parser quality/cost strategy.

### 25.7 Neo4j is a strong graph core, but some helper builders are experimental
Neo4j’s GraphRAG package is first-party and maintained, but the knowledge graph builder docs explicitly mark the builder as experimental.  
Do not couple the whole platform to an experimental builder.

### 25.8 Native vector support is useful, but hybrid retrieval still needs evaluation
Neo4j supports vector indexes and HNSW-based vector search, which may be enough initially.  
If retrieval quality becomes a bottleneck, a dedicated hybrid retrieval engine can be added.

### 25.9 Qdrant is strong for hybrid retrieval pipelines
Qdrant’s Query API supports server-side fusion and multi-stage retrieval pipelines.  
That is useful if Vitruvius later wants stronger chunk retrieval and reranking.

### 25.10 Treat BM42 cautiously
Qdrant’s own BM42 article notes BM42 should be considered experimental and requiring further research before production use.  
Do not make it the default unless internal evals prove it helps your corpus.

### 25.11 Use structured outputs everywhere
Cloud models now support strict schema-constrained outputs, and local serving stacks such as vLLM, llama.cpp, and Outlines support structured generation / grammar-constrained decoding.  
This is the correct foundation for extraction reliability.

---

## 26. Final recommendation

The correct transition is:

1. **invert the graph**
2. **separate canonical knowledge from evidence**
3. **reify relationships as assertions**
4. **attach every visible truth to evidence spans**
5. **use structured AI outputs for every extraction step**
6. **promote only validated nodes and assertions**
7. **materialize fast edges for traversal, but resolve explanations through assertion records**
8. **keep taxonomy roots curated and allow AI to organize deeper layers**

### Blunt conclusion

If Vitruvius keeps documents as primary nodes, it will remain a document browser with graph styling.  
If Vitruvius moves to a taxonomy-centered, evidence-backed assertion graph, it becomes a real knowledge system.

That is the transition.

---

## 27. Research references

### Standards / provenance / citation
- **R1 — PROV-O: The PROV Ontology**  
  https://www.w3.org/TR/prov-o/

- **R2 — Web Annotation Data Model**  
  https://www.w3.org/TR/annotation-model/

- **R3 — RFC 3778: The application/pdf Media Type**  
  https://www.rfc-editor.org/rfc/rfc3778.html

- **R4 — RFC 5147: URI Fragment Identifiers for the text/plain Media Type**  
  https://datatracker.ietf.org/doc/html/rfc5147

### Parsing / normalization
- **R5 — PyMuPDF: Details on Text Extraction**  
  https://pymupdf.readthedocs.io/en/latest/app1.html

- **R6 — PyMuPDF: Text extraction recipes**  
  https://pymupdf.readthedocs.io/en/latest/recipes-text.html

- **R7 — Unstructured: Partitioning**  
  https://docs.unstructured.io/open-source/core-functionality/partitioning

- **R8 — Unstructured: Partitioning strategies**  
  https://docs.unstructured.io/open-source/concepts/partitioning-strategies

### Graph / retrieval
- **R9 — Neo4j GraphRAG for Python**  
  https://neo4j.com/docs/neo4j-graphrag-python/current/

- **R10 — Neo4j Knowledge Graph Builder guide**  
  https://neo4j.com/docs/neo4j-graphrag-python/current/user_guide_kg_builder.html

- **R11 — Neo4j vector indexes**  
  https://neo4j.com/docs/cypher-manual/current/indexes/semantic-indexes/vector-indexes/

- **R12 — Neo4j vector search overview**  
  https://neo4j.com/developer/genai-ecosystem/vector-search/

- **R13 — Neo4j community detection algorithms**  
  https://neo4j.com/docs/graph-data-science/current/algorithms/community/

- **R14 — Neo4j Louvain**  
  https://neo4j.com/docs/graph-data-science/current/algorithms/louvain/

- **R15 — Neo4j topological link prediction**  
  https://neo4j.com/docs/graph-data-science/current/algorithms/linkprediction/

- **R16 — Neo4j node embeddings**  
  https://neo4j.com/docs/graph-data-science/current/machine-learning/node-embeddings/

- **R17 — Qdrant hybrid search / Query API**  
  https://qdrant.tech/articles/hybrid-search/

- **R18 — Qdrant BM42 article**  
  https://qdrant.tech/articles/bm42/

### Structured outputs / local + cloud AI
- **R19 — OpenAI Structured Outputs**  
  https://developers.openai.com/api/docs/guides/structured-outputs

- **R20 — vLLM structured outputs**  
  https://docs.vllm.ai/en/latest/features/structured_outputs/

- **R21 — llama.cpp grammars / JSON Schema support**  
  https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md

- **R22 — Outlines structured generation**  
  https://dottxt-ai.github.io/outlines/latest/

### Local model context
- **R23 — Gemma 4 model overview**  
  https://ai.google.dev/gemma/docs/core