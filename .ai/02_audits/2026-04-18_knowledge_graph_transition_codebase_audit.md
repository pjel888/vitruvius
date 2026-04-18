# Vitruvius — Knowledge Graph Transition: Codebase Audit (v2)

**Audited against:** `.ai/03_plans/vitruvius_knowledge_graph_transition_implementation_plan.md`  
**Audit date:** 2026-04-18  
**Method:** Direct file reads across `scripts/`, `config/`, `spatial-daemon/`, data layers `001_`–`006_`, state files  
**Scope:** Graph model, ingestion/evidence, AI orchestration, storage, API/UI, tests, operational surfaces  
**Status:** `CONFIRMED FINDINGS` — every structural claim is backed by a file read

---

## 1. Executive Verdict

**The codebase is structurally incompatible with the target architecture.**

Vitruvius today is a document-primary, CLI-batch, file-native pipeline that regenerates a flat JSON snapshot on every run. The target architecture requires a taxonomy-centered property graph with separate evidence and canonical layers, reified assertions, live queryable backends, and incremental updates.

**Compatibility:** ~15%. The only aligned pieces are the canonicalization discipline, the review/promotion gate, and the six-layer directory structure. Everything else — graph model, storage, evidence handling, AI orchestration, API, frontend, jobs — must be built or rebuilt.

**Risk:** Critical if attempted as a big-bang rewrite. Medium if executed as parallel, feature-flagged tracks.

---

## 2. Audit Method

1. **Read the target plan** in full (1,669 lines).
2. **Launch four parallel exploration agents** covering:
   - Graph & query layers (`scripts/vitruvius/graph/`, `query/`, `ontology/`, `wiki/`)
   - Ingestion & evidence pipeline (`pipeline_cli.py`, `parsers/`, `normalization/`, `conversion/`, `ocr/`, data layers)
   - AI orchestration (`ollama_review.py`, `promotion_validator.py`, `relationships/`, `concept_enrichment.py`, `config/vitruvius.yaml`)
   - API/UI/storage/tests/ops (`spatial-daemon/`, `004_Derived-Content-Layer/`, `config/`, `scripts/tests/`)
3. **Read critical files directly** to confirm exact line numbers and schemas.
4. **Classify every finding** as CONFIRMED (read directly) or INFERRED (deduced from code structure).

---

## 3. Current Architecture Snapshot

### 3.1 Graph Model (Document-Primary, Flat JSON)

**Primary file:** `scripts/vitruvius/graph/contract.py` (168 lines)

```python
# Lines 8–27
ALLOWED_NODE_TYPES = frozenset({"source", "concept", "attribute", "spatial_instance"})
ALLOWED_TRUST_LEVELS = frozenset({"primary", "secondary", "tertiary", "unverified", "derived"})
ALLOWED_EDGE_STATUSES = frozenset({"verified", "unverified", "spatially_verified"})
ALLOWED_ID_PREFIXES = frozenset({"law-", "irr-", "concept-", "rel-", "source-", "handout-", ...})

# Lines 35–42
@dataclass(frozen=True)
class GraphNode:
    id: str
    type: str
    slug: str
    trust_level: str
    last_updated_utc: str
    title: str | None = None

# Lines 45–59
@dataclass(frozen=True)
class GraphEdge:
    from_id: str
    to_id: str
    type: str
    evidence_id: str
    status: str
    evidence_source_id: str | None = None
    evidence_source_section_id: str | None = None
    evidence_snippet: str | None = None
    reviewer_confidence: float | None = None
    is_governing_standard: bool | None = None
```

**Key facts (CONFIRMED):**
- `builder.py` (line 248) hardcodes `trust_level="derived"` for all concept nodes, ignoring frontmatter.
- `builder.py` never creates `"attribute"` or `"spatial_instance"` nodes — these types are dead code in the build path.
- The graph is a **single JSON snapshot** (`005_Operational-Intelligence-Layer/graph/latest_graph_snapshot.json`) with a flat list of nodes and edges.
- No graph database. No Cypher. No property graph traversals at scale.

### 3.2 Pipeline (Synchronous CLI, Full Rebuild)

**Primary file:** `scripts/pipeline_cli.py` (1,887 lines)

**Active pipeline (confirmed by direct read of handler dispatch, lines 735–1880):**

```text
scan → convert → refine → canonicalize → extract-relationships → review → promote → build-graph
```

All stages run synchronously in a single Python process. No queue system. No worker pool.

**Key subcommands (CONFIRMED):**

| Subcommand | Handler | What it does |
|-----------|---------|-------------|
| `scan` | `vitruvius.scanner.run_scan` | Hashes raw files, writes CSV registries |
| `convert` | `vitruvius.conversion.run_convert` | PDF→Markdown via `opendataloader_pdf`; writes `002_Raw-Conversion-Layer/` |
| `refine` | `vitruvius.normalization.refine.run_refine` | Tier A/B normalization; writes `refined_markdown/` + `.refined.json` manifest |
| `canonicalize` | `vitruvius.canonicalize.run_canonicalize` | Creates canonical source pages in `003_Canonical-Knowledge-Layer/shared/sources/` |
| `extract-relationships-one` | `vitruvius.relationships.run_extract_relationships_one` | Regex-based extraction from full document text |
| `extract-relationships-sections-one` | `vitruvius.relationships_sections.run_extract_relationships_sections_one` | Section-aware regex extraction + dedupe |
| `review-relationships-ollama` | `vitruvius.ollama_review.run_review_relationships_ollama` | Tier-1 LLM review via Ollama `/api/generate` |
| `review-relationships-ollama-second-pass` | `vitruvius.ollama_review_second_pass.run_second_pass` | Tier-2 adjudication via `qwen3:30b` |
| `promote` | `vitruvius.promotion.run_promote` | Promotes high-confidence candidates to canonical relationship files |
| `build-graph` | `vitruvius.graph.cli.run_build_graph` | Rebuilds entire JSON snapshot from canonical directories |

**Critical gap:** `build-graph` regenerates the entire snapshot every time. There is no incremental update mechanism.

### 3.3 Evidence Handling (Snippet-Only, No Selectors)

**Current evidence schema** (from `promotion/__init__.py` and relationship frontmatter, CONFIRMED):

```yaml
evidence:
  - source_id: concept-floor-area
    source_section_id: section-irr-general
    evidence_snippet: "BUILDING BULK - The overall size..."
    review_decision: keep
    reviewer_model: gemma4:31b
    reviewer_confidence: 0.9
    reviewer_reason: "The provided example explicitly discusses..."
    extracted_at_utc: 20260414T234203Z
    reviewed_at_utc: 20260414T234203Z
```

**Missing (CONFIRMED by absence in all inspected files):**
- `document_version` with SHA-256 versioning
- `section` as a first-class persisted entity with selectors
- `chunk` — chunkers exist (`ast_chunker.py`, `embedding_chunker.py`) but are flag-gated OFF and not wired into the active pipeline
- `evidence_span` with byte offsets, line ranges, character ranges, or bounding boxes
- `selector` system of any kind (CSS, PDF bbox, markdown heading path + line/char)

**Parser interfaces are text-only** (`scripts/vitruvius/parsers/base_parser.py`, CONFIRMED):

```python
@dataclass(kw_only=True)
class ParseResult:
    markdown_text: str
    telemetry: ParserTelemetry
    sidecar_metadata: dict[str, Any] = field(default_factory=dict)
    failed_pages: list[int] = field(default_factory=list)
```

No structural annotation, no section map, no chunk map.

### 3.4 Storage (File-Native, No ORM, No Migrations)

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Graph snapshots | JSON files on disk | Main graph output (`005_Operational-Intelligence-Layer/graph/`) |
| Event store | SQLite (default) / RocksDB (opt-in) | Append-only edge lifecycle log (`PROMOTED`/`REJECTED`/`AMENDED`) |
| Wiki store | Kuzu (lazy import, OFF) | Wiki page node table only; no edges |
| Canonical content | Markdown + YAML frontmatter | `003_Canonical-Knowledge-Layer/` |
| Registries | CSV files | `006_System-Manifests/registries/` |
| Config | YAML | `config/vitruvius.yaml` |

**CONFIRMED absences:**
- No PostgreSQL
- No Neo4j
- No Qdrant or any vector database
- No ORM (SQLAlchemy, Django ORM)
- No schema migration framework (Alembic, Django migrations)
- No `.sql` files anywhere in the repo

### 3.5 AI Orchestration (100% Local Ollama, Minimal Structured Output)

**CONFIRMED findings:**

- **All LLM calls go to local Ollama** at `http://127.0.0.1:11434/api/generate` (`ollama_review.py`, `wiki/ollama_client.py`). No cloud fallback.
- **Tier-1 review:** `gemma4:31b` (default) or `qwen2.5:7b` (8GB-safe preset). Prompt built programmatically in `ollama_review.py::build_prompt()`; Ollama `format: "json"` enforced; manual parsing (no Pydantic).
- **Tier-2 review:** `qwen3:30b`. Second-pass adjudication. Fully wired into CLI.
- **Extraction:** Regex-based by default. LLM proposer (`relationships/llm_proposer.py`) gated behind `p5e_llm_extraction` (default `false`). No Pydantic validation on proposer output.
- **Concept enrichment:** Zero LLM calls. Deterministic regex pipeline (`concept_enrichment.py`).
- **Only Pydantic usage in LLM path:** `wiki/synthesis_loop.py` uses `TypeAdapter[WikiPageProposal].validate_json()`. This is the sole structured-output validation point in the entire codebase.
- **Scaffold modules exist but are OFF:** conformal calibrator, Bayesian fusion, stringency resolver, Naive Bayes pre-filter, SLM router, domain classifier, stateful registry. All gated by flags defaulting to `false`.

### 3.6 API / UI / Frontend

**CONFIRMED findings:**

- **No API server exists.** No FastAPI, Flask, Django, or ASGI/WSGI. All "API" is CLI subprocess invocation.
- **No SPA exists.** Frontend is `scripts/vitruvius/graph/visualize.py`, which generates self-contained HTML strings with embedded Cytoscape.js (inline CSS/JS, no build pipeline).
- **Inspector "panel"** is a hardcoded `<aside>` in a Python f-string — not a component.
- **No document viewer.** No PDF renderer. No markdown viewer with deep-linking.

### 3.7 Tests

**CONFIRMED:** 220+ test files in `scripts/tests/`.

**Key coverage:**
- `test_graph_builder.py` (602 lines) — snapshot building, frontmatter parsing, deduplication
- `test_graph_snapshot.py` (107 lines) — JSON roundtrip
- `test_graph_event_store.py` (111 lines) — SQLite append/projection
- `test_rocksdb_event_store.py` (172 lines) — RocksDB parity
- `test_graph_traverse.py` (175 lines) — BFS pathfinding
- `test_graph_cli.py` (133 lines) — CLI subprocess integration

**Critical gaps:**
- No API endpoint tests (no API exists)
- No frontend component tests (no frontend framework exists)
- No taxonomy/ontology tests (no taxonomy engine exists)
- No assertion-reification tests
- No evidence-span deep-linking tests
- No migration tests

### 3.8 Background Jobs / Operational Surfaces

**CONFIRMED findings:**

- **No job runner.** No Celery, RQ, dramatiq, Kafka, or `schedule` library. All batch work is synchronous CLI.
- **No structured logging.** Uses `print()` and `json.dumps(..., indent=2)`.
- **No metrics.** No Prometheus, StatsD, or custom metrics.
- **No health checks.** No `/health` or `/ready` endpoint.
- **Feature flags:** 80+ flags in `config/vitruvius.yaml`. Only 4 default to `true` (`hp_rocksdb_event_store`, `hp_rocksdb_verdict_cache`, `rust_mig_spatial_kernels`, `rust_mig_stats_kernels`).
- **Rollback:** `promote --rollback <batch_id>` reverses file moves. Event store uses logical rollback (`REJECTED` events). No database transaction rollback.

---

## 4. Current-State Findings by Layer

### 4.1 Domain / Ontology / Graph Model

| Finding | File Evidence | Certainty | Impact |
|---------|--------------|-----------|--------|
| Primary nodes are documents (`source-*`), not knowledge units | `contract.py` line 8; `builder.py` lines 186–220 | CONFIRMED | CRITICAL |
| Only 2 active node types: `source`, `concept` | `builder.py` lines 186–258 | CONFIRMED | CRITICAL |
| `attribute` and `spatial_instance` are dead code in build path | `contract.py` line 8 lists them; `builder.py` never creates them | CONFIRMED | LOW |
| Edges are dumb dataclasses, not reified assertions | `contract.py` lines 45–59 | CONFIRMED | CRITICAL |
| No taxonomy tree exists | Category folders (`001-Laws` through `009-Practice`) contain only `index.md` + `log.md` | CONFIRMED | HIGH |
| No `rule`, `definition`, `procedure`, `exception`, `constraint` node types | `ALLOWED_NODE_TYPES` in `contract.py` | CONFIRMED | CRITICAL |
| Edge types are ad-hoc strings, not a controlled vocabulary | `relationship_registry.yaml` has some predicates, but edges accept any non-empty string | CONFIRMED | HIGH |

### 4.2 Source Ingestion and Evidence Handling

| Finding | File Evidence | Certainty | Impact |
|---------|--------------|-----------|--------|
| Parser result is text-only: `markdown_text: str` | `parsers/base_parser.py` | CONFIRMED | HIGH |
| No section persistence | `relationships_sections.py::split_sections()` produces temp dicts then discards them | CONFIRMED | HIGH |
| No chunk persistence | `ast_chunker.py`, `embedding_chunker.py` exist but are flag-gated OFF | CONFIRMED | HIGH |
| No selector system | Absent from all inspected files | CONFIRMED | CRITICAL |
| No document versioning | `last_canonicalized_utc` exists but no SHA-256 version chain | CONFIRMED | HIGH |
| Evidence is `source_id` + `source_section_id` (loose string) + `evidence_snippet` (raw text) | `promotion/__init__.py`, relationship frontmatter | CONFIRMED | HIGH |
| OCR produces document-level output, no span tracking | `ocr.py` — calls `ocrmypdf.ocr()` then converts whole PDF to markdown | CONFIRMED | MEDIUM |

### 4.3 Assertion / Provenance / Explainability

| Finding | File Evidence | Certainty | Impact |
|---------|--------------|-----------|--------|
| No relationship_assertion objects | `contract.py` — only `GraphEdge` | CONFIRMED | CRITICAL |
| No node_assertion objects | Absent | CONFIRMED | CRITICAL |
| No placement_assertion objects | Absent | CONFIRMED | CRITICAL |
| No merge_assertion objects | Absent | CONFIRMED | CRITICAL |
| No reasoning_summary on edges | `GraphEdge` has `evidence_snippet` and `reviewer_reason` (in frontmatter only, not in edge dataclass) | CONFIRMED | HIGH |
| No inference_type taxonomy | Absent | CONFIRMED | MEDIUM |
| Event store tracks edge lifecycle but not assertion provenance | `event_store.py` — schema: `event_id`, `event_type`, `edge_id`, `timestamp_utc`, `payload_json` | CONFIRMED | MEDIUM |

### 4.4 Storage and Persistence

| Finding | File Evidence | Certainty | Impact |
|---------|--------------|-----------|--------|
| No Neo4j | Absent from imports, config, requirements | CONFIRMED | CRITICAL |
| No PostgreSQL | Absent | CONFIRMED | HIGH |
| No Qdrant | Absent | CONFIRMED | MEDIUM |
| No ORM | `models.py` has only a 15-line `FileEntry` dataclass | CONFIRMED | HIGH |
| No schema migrations | `migrations.py` is text-level ID regex replacement, not DB schema migration | CONFIRMED | HIGH |
| Kuzu is integrated but OFF and wiki-only | `wiki/kuzu_store.py`; `wiki_kuzu_store: false` in config | CONFIRMED | LOW |

### 4.5 Retrieval / Search / Graph Query

| Finding | File Evidence | Certainty | Impact |
|---------|--------------|-----------|--------|
| Query engine operates on in-memory JSON snapshot | `query/engine.py` — all functions take `snapshot: GraphSnapshot` | CONFIRMED | HIGH |
| No vector search | No vector DB; GraphSAGE flag OFF | CONFIRMED | HIGH |
| No hybrid retrieval | No lexical + dense + graph fusion | CONFIRMED | HIGH |
| NL translator is regex-only by default | `query/nl_translator.py` — `translate_question()` falls back to regex if no `llm_caller` injected | CONFIRMED | MEDIUM |

### 4.6 AI Orchestration

| Finding | File Evidence | Certainty | Impact |
|---------|--------------|-----------|--------|
| 100% local Ollama; no cloud fallback | `ollama_review.py`, `wiki/ollama_client.py` | CONFIRMED | MEDIUM |
| Structured output only in WIKI layer | `wiki/synthesis_loop.py` uses Pydantic; all other LLM paths use manual JSON parsing | CONFIRMED | HIGH |
| Extraction is regex-based; LLM path is gated OFF | `relationships_sections.py` (regex); `relationships/llm_proposer.py` (gated by `p5e_llm_extraction: false`) | CONFIRMED | HIGH |
| 17-rule validator exists but is not auto-invoked by promotion batch runner | `promotion_validator.py` is a library; audit did not find automatic invocation in `promotion/__init__.py` | CONFIRMED | MEDIUM |
| Scaffold modules (conformal, Bayesian fusion, stringency) are OFF | `review/conformal_calibrator.py`, `promotion/bayesian_fusion.py`, `promotion/stringency_resolver.py` exist but flags default false | CONFIRMED | LOW |

### 4.7 API Contracts and Backend Services

| Finding | File Evidence | Certainty | Impact |
|---------|--------------|-----------|--------|
| No server exists | No FastAPI/Flask/Django imports; no route definitions | CONFIRMED | CRITICAL |
| All inter-module communication is in-process Python or file handoff | `pipeline_cli.py`, `dataset_pipeline.py` | CONFIRMED | CRITICAL |

### 4.8 Frontend / Graph UI / Inspector

| Finding | File Evidence | Certainty | Impact |
|---------|--------------|-----------|--------|
| No SPA | `visualize.py` generates HTML strings with f-strings | CONFIRMED | CRITICAL |
| No document viewer | Absent | CONFIRMED | HIGH |
| No edge inspector that resolves assertion records | HTML "panel" is a static `<aside>` with snapshot metadata | CONFIRMED | HIGH |
| Cytoscape.js is vendored and inline | `graph/assets/cytoscape.min.js` | CONFIRMED | LOW |

### 4.9 Background Jobs / Queues

| Finding | File Evidence | Certainty | Impact |
|---------|--------------|-----------|--------|
| No job runner | No Celery/RQ/dramatiq imports; no cron files | CONFIRMED | HIGH |
| Dataset pipeline is synchronous single-process | `dataset_pipeline.py` (1,250 lines) — calls `webbrowser.open()` for local viewing | CONFIRMED | MEDIUM |

### 4.10 Testing

| Finding | File Evidence | Certainty | Impact |
|---------|--------------|-----------|--------|
| 220+ unit tests, 0 API/E2E tests | `scripts/tests/` inventory | CONFIRMED | MEDIUM |
| No taxonomy tests | No taxonomy engine to test | CONFIRMED | LOW |
| No assertion-reification tests | No assertion layer to test | CONFIRMED | LOW |

---

## 5. Current vs Target Gap Analysis

### 5.1 Non-Negotiable Rules Assessment

| # | Rule | Status | Evidence |
|---|------|--------|----------|
| 1 | Primary nodes are knowledge units, not files. | **VIOLATION** | `builder.py` lines 186–220 create `source` nodes as primary entities. |
| 2 | Every user-visible node must be backed by evidence. | **PARTIAL** | Relationships carry `evidence_snippet`; concept `regulatory_basis` exists. No formal `evidence_span`. |
| 3 | Every user-visible edge must be explainable. | **PARTIAL** | Edges have `evidence_snippet` and frontmatter `reviewer_reason`, but no `reasoning_summary` or `inference_type` in edge dataclass. |
| 4 | Every explanation must link to source at span/page/section level. | **MISSING** | No selectors, no page/bbox/line/char. Only `source_id` + `source_section_id` strings. |
| 5 | AI proposes; system promotes only validated structure. | **SATISFIED** | 17-rule validator, tier-1 + tier-2 review, promotion governance. |
| 6 | Canonical graph and evidence graph must be separated. | **MISSING** | Single JSON snapshot mixes source and concept nodes. No evidence layer abstraction. |
| 7 | Pragmatic property-graph now; RDF/ontology exports later. | **COMPATIBLE** | OWL/Turtle exporter exists (`ontology/owl_exporter.py`) but is optional. No property graph DB yet. |
| 8 | Incremental updates; no full regeneration per ingestion. | **VIOLATION** | `build-graph` rebuilds entire snapshot from canonical directories every run. |

### 5.2 Target Architecture Layer Assessment

| Target Layer | Current Equivalent | Gap |
|--------------|-------------------|-----|
| Source Layer | `001_Raw-Source-Layer/` | ✅ Adequate |
| Evidence Layer | None | ❌ No `document_version`, `section`, `chunk`, `evidence_span` |
| Canonical Knowledge Layer | `003_Canonical-Knowledge-Layer/shared/` | ⚠️ File-native Markdown; no taxonomy tree; no `rule`, `definition`, `procedure` types |
| Assertion/Explanation Layer | None | ❌ No reified assertions |

### 5.3 Maturity Scoring by Domain

Score: 0 = absent, 1 = prototype, 2 = functional, 3 = production-ready

| Domain | Score | Rationale |
|--------|-------|-----------|
| Canonicalization pipeline | 3 | Rules engine, frontmatter validation, ID system, promotion governance, audit logs |
| Review/promotion governance | 3 | Two-tier LLM review, 17-rule validator, rollback, idempotency |
| Graph snapshot integrity | 2 | Duplicate/orphan/dangling edge detection, SHA-256 fingerprinting |
| Source ingestion | 2 | Multi-parser architecture, OCR fallback, feature-gated modern parsers |
| Extraction | 1 | Regex-grade + optional LLM; no structured output constraints; no atomic rule/definition extraction |
| Evidence modeling | 0 | No evidence graph, no spans, no selectors |
| Assertion layer | 0 | No reified assertions |
| Taxonomy/ontology | 0 | Flat node types; no taxonomy tree; category folders empty |
| Graph database | 0 | JSON snapshots only |
| Vector/semantic retrieval | 0 | No vector DB, no chunk index |
| Deep linking / citations | 0 | No page/bbox/line/char selectors |
| Incremental updates | 0 | Full snapshot rebuild every run |
| Structured LLM outputs | 0 | Free-form extraction + review; only WIKI uses Pydantic |
| Query engine | 1 | In-memory Python over JSON; no graph DB traversal |
| UI/API | 0 | CLI-only; static HTML generator |
| API/server | 0 | None exists |

**Aggregate maturity:** ~0.7 / 3.0 for knowledge-graph transition readiness.

---

## 6. Blast Radius Analysis

### 6.1 Affected Files Inventory

#### Data Model / Schema

| File | Current Responsibility | Why Impacted | Change Type | Risk | Impact Level |
|------|----------------------|-------------|-------------|------|-------------|
| `scripts/vitruvius/graph/contract.py` | GraphNode, GraphEdge, GraphSnapshot dataclasses | Must add v2 models or Pydantic equivalents for canonical nodes, assertions, evidence spans | schema | CRITICAL | confirmed direct |
| `scripts/vitruvius/graph/builder.py` | Snapshot builder walking canonical dirs | Must support evidence-first build or coexist with new builder | service logic | HIGH | confirmed direct |
| `scripts/vitruvius/graph/snapshot.py` | JSON read/write | Must support v1/v2 dual format or migration | data migration | HIGH | confirmed direct |
| `scripts/vitruvius/graph/integrity.py` | Structural checks | Must validate assertion graph structure, evidence span integrity | test | MEDIUM | confirmed direct |
| `scripts/vitruvius/models.py` | Single `FileEntry` dataclass | Must expand to domain models or be replaced by Pydantic schemas | schema | HIGH | confirmed direct |

#### Ingestion / Parsing / Evidence

| File | Current Responsibility | Why Impacted | Change Type | Risk | Impact Level |
|------|----------------------|-------------|-------------|------|-------------|
| `scripts/vitruvius/parsers/base_parser.py` | Abstract parser interface | Must return structural annotation (sections, chunks) not just `markdown_text` | API contract | HIGH | confirmed direct |
| `scripts/vitruvius/parsers/opendataloader_parser.py` | OpenDataLoader wrapper | Must expose sidecar structural data for evidence spans | service logic | MEDIUM | probable adjacent |
| `scripts/vitruvius/parsers/docling_parser.py` | Docling wrapper | Same as above | service logic | MEDIUM | probable adjacent |
| `scripts/vitruvius/parsers/rust_pdf_parser.py` | Rust PDF parser | Same as above | service logic | MEDIUM | probable adjacent |
| `scripts/vitruvius/normalization/refine.py` | Text normalization | Must preserve or emit section/chunk boundaries | service logic | HIGH | confirmed direct |
| `scripts/vitruvius/normalization/engine.py` | Normalization rule engine | Same as above | service logic | MEDIUM | confirmed direct |
| `scripts/vitruvius/relationships_sections.py` | Section-aware regex extraction | Must persist sections as entities, not temp dicts | service logic | HIGH | confirmed direct |
| `scripts/vitruvius/canonicalize.py` | Canonical source page creation | Must emit section metadata, evidence span candidates | service logic | HIGH | confirmed direct |

#### AI Orchestration

| File | Current Responsibility | Why Impacted | Change Type | Risk | Impact Level |
|------|----------------------|-------------|-------------|------|-------------|
| `scripts/vitruvius/ollama_review.py` | Tier-1 review | Must enforce structured output schemas for all reviews | prompt/model | HIGH | confirmed direct |
| `scripts/vitruvius/relationships/llm_proposer.py` | Phase 5E LLM proposer | Must use Pydantic/JSON Schema validation on output | prompt/model | HIGH | confirmed direct |
| `scripts/vitruvius/concept_enrichment.py` | Zero-LLM enrichment | Must support structured LLM extraction for rules/definitions/exceptions | prompt/model | HIGH | confirmed direct |
| `scripts/vitruvius/pre_review_filter.py` | Deterministic triage | Must route new node/assertion types, not just relationships | service logic | MEDIUM | confirmed direct |
| `scripts/vitruvius/promotion_validator.py` | 17-rule validator | Must validate canonical nodes and assertions, not just relationships | service logic | HIGH | confirmed direct |
| `scripts/vitruvius/promotion/__init__.py` | Promotion batch runner | Must auto-invoke validator and write to Neo4j/Postgres, not just Markdown files | service logic | HIGH | confirmed direct |
| `config/vitruvius.yaml` | Feature flags | Must add `kg_transition.*` flag block | config | LOW | confirmed direct |

#### Storage / Persistence

| File | Current Responsibility | Why Impacted | Change Type | Risk | Impact Level |
|------|----------------------|-------------|-------------|------|-------------|
| `scripts/vitruvius/graph/event_store.py` | SQLite event store | Must support assertion events, not just edge events | schema | MEDIUM | confirmed direct |
| `scripts/vitruvius/graph/rocksdb_event_store.py` | RocksDB event store | Same as above | schema | MEDIUM | confirmed direct |
| `scripts/vitruvius/wiki/kuzu_store.py` | Kuzu wiki facade | May be extended or replaced by Neo4j canonical graph store | service logic | MEDIUM | probable adjacent |
| *(new)* `scripts/vitruvius/kg/neo4j_schema.cypher` | — | New file: Neo4j DDL for canonical + evidence + assertion graph | schema | HIGH | new module |
| *(new)* `scripts/vitruvius/db/schema.sql` | — | New file: PostgreSQL DDL for registry, jobs, audit, review queues | schema | HIGH | new module |

#### Query / Retrieval

| File | Current Responsibility | Why Impacted | Change Type | Risk | Impact Level |
|------|----------------------|-------------|-------------|------|-------------|
| `scripts/vitruvius/query/engine.py` | Structured queries over JSON snapshot | Must query Neo4j canonical graph first, evidence second | service logic | HIGH | confirmed direct |
| `scripts/vitruvius/query/nl_translator.py` | NL→query translation | Must resolve to canonical nodes, not just document nodes | service logic | MEDIUM | confirmed direct |
| `scripts/vitruvius/query/graphrag_router.py` | GraphRAG routing | Must route canonical-first | service logic | MEDIUM | confirmed direct |

#### UI / Visualization

| File | Current Responsibility | Why Impacted | Change Type | Risk | Impact Level |
|------|----------------------|-------------|-------------|------|-------------|
| `scripts/vitruvius/graph/visualize.py` | Static HTML generator | Must show canonical nodes by default, evidence in inspector | UI | HIGH | confirmed direct |
| `004_Derived-Content-Layer/graph-visualizations/` | Static HTML outputs | Will be replaced by live queryable UI or API-driven rendering | UI | MEDIUM | indirect |

#### CLI / Pipeline Orchestration

| File | Current Responsibility | Why Impacted | Change Type | Risk | Impact Level |
|------|----------------------|-------------|-------------|------|-------------|
| `scripts/pipeline_cli.py` | Main CLI entrypoint (~70 subcommands) | Must add `kg-*` subcommands for evidence ingestion, extraction, canonicalization, assertion materialization | API contract | HIGH | confirmed direct |
| `scripts/vitruvius/dataset_pipeline.py` | End-to-end dataset orchestrator | Must support KG transition stages in pipeline manifest | service logic | HIGH | confirmed direct |

#### Tests

| File | Current Responsibility | Why Impacted | Change Type | Risk | Impact Level |
|------|----------------------|-------------|-------------|------|-------------|
| `scripts/tests/test_graph_builder.py` | Snapshot builder tests | Must pass with v1 compatibility; new tests needed for v2 | test | MEDIUM | confirmed direct |
| `scripts/tests/test_graph_contract.py` | Contract validation tests | Must test new v2 schemas | test | MEDIUM | confirmed direct |
| *(new)* `scripts/tests/test_kg_*.py` | — | New test files for every KG module | test | HIGH | new module |

---

## 7. High-Risk Assumptions and Unknowns

### Unknowns (Must Verify Before Execution)

1. **Neo4j operational constraints** — The team has Kuzu integration skill (`wiki/kuzu_store.py`) but no Neo4j experience in the repo. Can the team operate Neo4j at scale? **UNKNOWN / must verify** via a spike.

2. **PostgreSQL schema migration strategy** — No Alembic or migration framework exists. Will the team adopt Alembic, or use raw SQL + version tracking? **UNKNOWN / must decide**.

3. **Structured output reliability from local models** — The only Pydantic-validated LLM path is WIKI synthesis. Can `gemma4:31b` reliably produce schema-valid extraction outputs at 90%+ first-pass rate? **UNKNOWN / must benchmark**.

4. **Cloud model integration** — The target plan recommends cloud models for ambiguity resolution. The repo has zero cloud LLM integration. Is there budget/API access for OpenAI/Anthropic? **UNKNOWN / must verify**.

5. **Frontend strategy** — The target plan implies a live graph UI with edge inspectors. The repo has no frontend framework. Will the team build a SPA, embed in an existing app, or keep CLI-first? **UNKNOWN / must decide**.

6. **Incremental update feasibility** — The existing pipeline is designed for full rebuilds. Can evidence spans survive document reprocessing without ID drift? **UNKNOWN / must design**.

### High-Risk Assumptions

1. **AD-001 (Filesystem-as-database) will not block the transition** — If the maintainers treat Neo4j/PostgreSQL as violations of Principle P1, the transition stalls. **RISK: HIGH**.

2. **Existing concept pages can seed the canonical graph** — Most concepts are stubs (Definition + Regulatory Basis only). Assuming they are "seedable" may lead to a low-quality canonical layer. **RISK: HIGH**.

3. **Feature flags prevent regression** — The codebase has 80+ flags, almost all false. Adding more flags may increase configuration complexity without guaranteeing safety. **RISK: MEDIUM**.

4. **Parser adapters can be extended to return structural data** — `BaseParser.parse()` currently returns `markdown_text: str`. Extending this to return section maps and chunk maps is a breaking API change for all parser implementations. **RISK: MEDIUM**.

---

## 8. Priority Findings

**Fix first (blocks everything else):**
1. Resolve AD-001 conflict — operational DBs must be permitted as Layer 5 indexes.
2. Bump graph contract to v2.0.0-alpha with backward-compat shim.
3. Implement Pydantic v2 schemas for canonical node, assertion, evidence span, selector, document version.

**Fix second (blocks evidence graph):**
4. Extend `BaseParser.parse()` to return structural annotation (sections, chunks).
5. Implement selector resolution (PDF bbox, markdown heading path + line/char).
6. Add document version tracking with SHA-256.

**Fix third (blocks assertion layer):**
7. Implement structured LLM output validation across all extraction paths.
8. Build assertion validator and materializer.
9. Introduce Neo4j behind feature flag.

**Do not fix yet (low priority):**
- Spatial daemon schema extension (low coupling)
- Graph physics modules (PageRank, Boltzmann) — these operate on graph topology and can be adapted later
- OWL/Turtle exporter — can be updated after canonical graph stabilizes

---

## 9. Recommended Architectural Stance

**Do not attempt a big-bang rewrite.** The existing pipeline produces validated, audited outputs. Breaking it risks losing the only working path from raw documents to promoted relationships.

**Recommended path:**
1. **Parallel track:** Build the new KG pipeline alongside the existing one. Use `kg_transition.enabled: false` to keep the legacy path untouched.
2. **Evidence-first:** Start by building the evidence graph (document → version → section → chunk → span). This does not require changing the canonical layer yet.
3. **Small seed set:** Use 10–20 well-enriched concepts to test canonicalization and placement. Do not migrate all ~72 concepts at once.
4. **CLI-first API:** Add `kg-*` subcommands to `pipeline_cli.py` before building any HTTP server. The CLI is the only proven interaction surface.
5. **Freeze taxonomy roots by hand.** Do not let AI propose top-level branches until Phase 3+.
6. **Validate before promote:** No canonical node or assertion reaches `validated` status without passing deterministic rules and having ≥1 evidence span.

---

*End of Audit*
