# Vitruvius — Knowledge Graph Transition: Readiness Plan (v2)

**Prepared:** 2026-04-18  
**Status:** `PROPOSED`  
**Derived from:** `.ai/03_plans/vitruvius_knowledge_graph_transition_implementation_plan.md`  
**Informed by:** `.ai/02_audits/2026-04-18_knowledge_graph_transition_codebase_audit.md` (v2)
**Audience:** Engineering, data pipeline, graph layer, AI orchestration, product  
**Purpose:** Define the concrete pre-conditions, decision gates, and exit criteria that must be satisfied before the first implementation sprint of the knowledge graph transition begins.

---

## 1. Readiness Verdict

**NOT READY.**

The codebase audit (v2) confirms that nearly every structural primitive required by the target architecture is missing:
- No evidence graph (document_version, section, chunk, evidence_span)
- No reified assertions
- No live graph database
- No taxonomy tree
- No structured LLM output enforcement (except WIKI synthesis)
- No API server, no SPA frontend
- No ORM, no schema migrations

**Before Sprint 1 can begin, the team must close 6 readiness gates.** These gates are non-negotiable.

---

## 2. Readiness Dimensions

| Dimension | Current State | Target State | Blocker Level |
|-----------|--------------|-------------|---------------|
| **Architecture** | AD-001 prohibits hidden DBs; filesystem graph contract frozen | Operational DBs permitted as Layer 5 indexes; contract bumped to v2.0.0-alpha | **BLOCKING** |
| **Schema / Data Model** | `@dataclass(frozen=True)` GraphNode/GraphEdge; no Pydantic | Pydantic v2 models for CanonicalNode, Assertion, EvidenceSpan, Selector, DocumentVersion | **BLOCKING** |
| **Infrastructure** | SQLite/RocksDB (events), JSON (snapshots), Kuzu (wiki, OFF) | Neo4j + PostgreSQL provisioned and reachable | **BLOCKING** |
| **Ingestion / Evidence** | Text-only parser output; no selectors; no chunks | Parser returns structural annotation; selector system designed; chunk boundaries defined | **BLOCKING** |
| **AI Orchestration** | 100% local Ollama; manual JSON parsing; regex extraction | Structured output validation on ALL LLM paths; local/cloud split operational | **HIGH** |
| **Storage / Migrations** | No ORM, no migrations, no schema files | PostgreSQL DDL + migration strategy; Neo4j Cypher schema | **BLOCKING** |
| **Retrieval / Indexing** | In-memory Python over JSON; no vector search | Neo4j indexes + optional Qdrant decision record | **MEDIUM** |
| **API / UI** | None exist | No server/SPA required for Sprint 1, but must be planned | **LOW** |
| **Tests** | 220+ unit tests, 0 API/E2E, no assertion tests | Golden dataset + structured output validity tests must exist | **HIGH** |
| **Operational Safety** | 80+ feature flags, print-based logging, no metrics | `kg_transition.*` flags added; rollback plan documented | **MEDIUM** |

---

## 3. Prerequisites and Blockers

### 3.1 Blocker 1: AD-001 Conflict (Architecture)

**Problem:** AD-001 (Filesystem-as-Database) states "Core lineage uses structured directories (`001_`–`006_`) and CSV/JSON registries. No hidden SQLite/Postgres for core lineage (Principle P1)."

**Why it blocks:** The target plan requires Neo4j and PostgreSQL. If AD-001 is interpreted literally, the transition cannot proceed.

**Resolution required:**
1. Draft **AD-043: Operational Databases as Layer 5 Indexes**.
   - Layers 1–4 remain file-native and git-tracked (Principle P1 preserved).
   - Layer 5 (Operational Intelligence) may use live databases as **materialized indexes** of file-native truth.
   - Neo4j = canonical graph index. PostgreSQL = job/audit/registry index. Qdrant = retrieval index (optional).
   - File-native lineage remains **source of truth**; databases are **queryable replicas** rebuilt from manifests.
2. Merge AD-043 into `.ai/10_state/decisions.md`.
3. Bump graph contract version to `"2.0.0-alpha"` in `scripts/vitruvius/graph/contract.py` (line 64).
4. Preserve `"1.0.0"` backward compatibility behind `kg_transition.legacy_snapshot_mode: true`.

**Gate:** AD-043 merged; `GraphSnapshot.schema_version` accepts `"2.0.0-alpha"`; v1 snapshot build still passes.

### 3.2 Blocker 2: Infrastructure Not Provisioned

**Problem:** No Neo4j or PostgreSQL instances exist or are configured.

**Why it blocks:** Phase 1 (Evidence Graph) cannot be validated without a graph database and relational registry.

**Resolution required:**

#### Neo4j (Mandatory)
- [ ] Install Neo4j Community or Enterprise (local dev) or provision cloud instance.
- [ ] Add `neo4j` Python driver to `requirements.txt`.
- [ ] Validate connectivity from `scripts/pipeline_cli.py` process.
- [ ] Create idempotent schema script: `scripts/vitruvius/kg/neo4j_schema.cypher`.
- [ ] Constraints: `CanonicalNode.id`, `Assertion.id`, `EvidenceSpan.id` are UNIQUE.
- [ ] Indexes: `CanonicalNode(type)`, `CanonicalNode(status)`, `Assertion(edge_type)`, `Assertion(validation_status)`.

#### PostgreSQL (Mandatory)
- [ ] Install PostgreSQL 15+ or provision cloud instance.
- [ ] Add `psycopg` (v3) to `requirements.txt`.
- [ ] Create initial DDL: `scripts/vitruvius/db/schema.sql`.
- [ ] Minimum tables:
  - `file_registry` (id, path, sha256, mime_type, created_at)
  - `document_version` (id, document_id, title, source_uri, sha256, created_at, supersedes)
  - `ingestion_run` (id, started_at, completed_at, status, manifest_hash)
  - `extraction_run` (id, ingestion_run_id, model, pipeline_stage, config)
  - `review_queue` (id, item_type, item_id, confidence, status, assigned_to, created_at, updated_at)
  - `canonical_merge_log` (id, from_node_id, to_node_id, merged_at, merge_reason)
  - `audit_event` (id, event_type, actor, details, timestamp)
- [ ] Validate connectivity via pytest.

**Gate:** `pytest` passes for `test_neo4j_backend.py` and `test_postgres_registry.py` (create, read, traverse, CRUD).

### 3.3 Blocker 3: Schema Not Frozen

**Problem:** No Pydantic models exist for the target architecture. The codebase uses `@dataclass(frozen=True)` extensively.

**Why it blocks:** All extraction, validation, and storage code depends on stable schemas.

**Resolution required:**

**New file:** `scripts/vitruvius/kg/schemas.py`

Implement Pydantic v2 models:
- `Selector` (kind, page, bbox, heading_path, line_start, line_end, char_start, char_end)
- `EvidenceSpan` (id, document_id, document_version_id, selector, quote, normalized_text, deep_link, parser, parser_version, checksum)
- `DocumentVersion` (id, document_id, title, source_uri, mime_type, sha256, created_at, supersedes)
- `CanonicalNode` (id, type, label, summary, taxonomy_path, aliases, status, confidence, version)
- `RelationshipAssertion` (id, edge_type, from_node_id, to_node_id, reasoning_summary, reasoning_detail, inference_type, confidence, validation_status, evidence_ids, document_version_ids, created_by, review_state, created_at, updated_at, version)
- `PlacementAssertion` (id, node_id, parent_node_id, reasoning_summary, confidence, validation_status, evidence_ids)
- `MergeAssertion` (id, from_node_id, to_node_id, reasoning_summary, confidence, validation_status)

**New file:** `scripts/vitruvius/kg/enums.py`

```python
from enum import StrEnum

class NodeType(StrEnum):
    TAXONOMY = "taxonomy"
    TOPIC = "topic"
    SUBTOPIC = "subtopic"
    CONCEPT = "concept"
    TERM = "term"
    DEFINITION = "definition"
    RULE = "rule"
    PROCEDURE = "procedure"
    EXCEPTION = "exception"
    CONSTRAINT = "constraint"
    EXAMPLE = "example"

class EdgeType(StrEnum):
    HAS_CHILD = "HAS_CHILD"
    BELONGS_TO = "BELONGS_TO"
    RELATED_TO = "RELATED_TO"
    DEFINED_BY = "DEFINED_BY"
    DEPENDS_ON = "DEPENDS_ON"
    APPLIES_TO = "APPLIES_TO"
    OVERRIDES = "OVERRIDES"
    CONTRADICTS = "CONTRADICTS"
    SAME_AS = "SAME_AS"
    PART_OF = "PART_OF"
    REQUIRES = "REQUIRES"
    EXCLUDES = "EXCLUDES"

class InferenceType(StrEnum):
    DIRECT_CITATION = "direct_citation"
    TAXONOMY_PLACEMENT = "taxonomy_placement"
    RULE_BASED_DERIVATION = "rule_based_derivation"
    SEMANTIC_SIMILARITY = "semantic_similarity"
    MULTI_HOP_INFERENCE = "multi_hop_inference"
    HUMAN_AUTHORED = "human_authored"

class ValidationState(StrEnum):
    CANDIDATE = "candidate"
    VALIDATED = "validated"
    REVIEW_REQUIRED = "review_required"
    REJECTED = "rejected"
    DEPRECATED = "deprecated"
    SUPERSEDED = "superseded"
```

**Gate:** All models pass `pytest` validation tests (valid creation, invalid rejection, roundtrip JSON, JSON Schema export).

### 3.4 Blocker 4: Evidence Capture Not Designed

**Problem:** The current pipeline produces `markdown_text: str` with no structural annotation. No selectors, no chunks, no evidence spans.

**Why it blocks:** The evidence graph is the foundation of the canonical graph. Without it, canonical nodes have no provable backing.

**Resolution required:**

1. **Extend parser interface** (`scripts/vitruvius/parsers/base_parser.py`):
   ```python
   @dataclass(kw_only=True)
   class ParseResult:
       markdown_text: str
       section_map: list[SectionBlock] | None = None   # NEW
       chunk_map: list[ChunkBlock] | None = None       # NEW
       telemetry: ParserTelemetry
       sidecar_metadata: dict[str, Any]
       failed_pages: list[int]
   ```
   **Note:** This is a breaking change. All parser implementations must be updated.

2. **Define selector schema** (in `schemas.py`):
   - `PdfBboxSelector`: page, bbox[x1,y1,x2,y2], quote
   - `MarkdownRangeSelector`: heading_path, line_start, line_end, char_start, char_end, quote
   - `TextRangeSelector`: char_start, char_end, quote

3. **Create evidence span resolution test**:
   - Select 3–5 representative documents (clean PDF, scanned PDF, Markdown).
   - Manually create ≥10 `evidence_span` records with valid selectors.
   - Validate that selectors resolve to correct text/quotes.

**Gate:** `BaseParser.parse()` compiles with new signature; at least one parser implementation returns non-null `section_map`; selector resolution passes on 100% of seed spans.

### 3.5 Blocker 5: Structured LLM Pipeline Not Ready

**Problem:** Only the WIKI layer uses Pydantic for LLM output validation. All extraction and review paths use manual JSON parsing.

**Why it blocks:** The target plan mandates structured outputs for every extraction step. Without this, the graph becomes "semantic sludge."

**Resolution required:**

1. **New file:** `scripts/vitruvius/llm/structured_client.py`
   ```python
   class StructuredLLMClient:
       def extract(self, prompt: str, model: type[BaseModel], *, max_retries: int = 3) -> BaseModel | None:
           ...
   ```
   - Input: prompt + Pydantic model class
   - Output: validated model instance or `None`
   - Retry: 3 retries with exponential backoff
   - Failure logging: write invalid raw output to `006_System-Manifests/runs/llm_parse_failures/`

2. **Benchmark seed test:**
   - Run 50 extraction calls against a test document.
   - Target: ≥90% first-pass schema validity.
   - If local models cannot meet this, cloud model fallback must be available.

3. **Cloud model decision:**
   - Decide whether OpenAI/Anthropic API keys are available.
   - If no cloud access, local models must be sufficient for Sprint 1 scope (small seed set).

**Gate:** `StructuredLLMClient` passes unit tests; seed benchmark shows ≥90% validity; fallback strategy documented.

### 3.6 Blocker 6: No Taxonomy Backbone

**Problem:** The 9 category folders in `003_Canonical-Knowledge-Layer/` are empty except for `index.md` + `log.md`. No taxonomy tree exists.

**Why it blocks:** The canonical graph requires a seeded top-level taxonomy. AI must not invent roots freely.

**Resolution required:**

1. Hand-curate 8–12 top-level taxonomy domains:
   - `taxonomy-architecture`
   - `taxonomy-building-code`
   - `taxonomy-fire-and-life-safety`
   - `taxonomy-accessibility`
   - `taxonomy-structural`
   - `taxonomy-mep`
   - `taxonomy-site-planning`
   - `taxonomy-definitions`
   - `taxonomy-procedures`
   - `taxonomy-compliance-checks`

2. Create canonical Markdown files in `003_Canonical-Knowledge-Layer/shared/taxonomy/`:
   ```yaml
   ---
   id: taxonomy-building-code
   title: Building Code
   page_type: taxonomy
   canonical_status: validated
   trust_level: primary
   ---
   ```

3. Validate via existing frontmatter lint.

**Gate:** ≥8 taxonomy root files exist and pass lint; IDs are stable and follow the canonical ID standard.

---

## 4. Capabilities Already Present (Reusable)

These reduce readiness work. They do not eliminate the blockers above.

1. **Canonicalization pipeline** — `canonicalize.py`, `canonicalize-concept-one` produce structured Markdown with YAML frontmatter. The pipeline structure is correct.
2. **Feature-flag framework** — `config/vitruvius.yaml` with 80+ flags. New `kg_transition.*` block can be added safely.
3. **Dataset manifest system** — `dataset_manifest.py` provides scoped, versioned, fingerprinted execution. Can be extended with KG-specific manifests.
4. **Event-sourced graph store** — `event_store.py` / `rocksdb_event_store.py` provide append-only provenance. Can be extended with assertion event types.
5. **Graph integrity checker** — `integrity.py` tests duplicates, orphans, dangling edges. Can be extended for assertion graph integrity.
6. **Two-tier LLM review** — `ollama_review.py` + `ollama_review_second_pass.py` are operational. Can be extended to review assertions, not just relationships.
7. **Promotion validator** — `promotion_validator.py` has 17 rigorous rules. Can be extended to validate canonical nodes and assertions.
8. **Kuzu integration** — `wiki/kuzu_store.py` proves the team can integrate graph DBs. Neo4j is a different API but similar concept.
9. **Deterministic ID system** — `<prefix>-<slug>` pattern is stable. New prefixes (`rule-`, `definition-`, `taxonomy-`) can be added.

---

## 5. Missing Capabilities That Must Exist Before Execution

| Capability | Why Required | Sprint 0 Deliverable |
|-----------|-------------|---------------------|
| Neo4j instance + Python driver | Canonical + evidence graph storage | `scripts/vitruvius/kg/neo4j_client.py` + schema script |
| PostgreSQL instance + Python driver | Registry, jobs, audit, review queues | `scripts/vitruvius/db/postgres_client.py` + DDL |
| Pydantic v2 schemas | Type-safe extraction, validation, serialization | `scripts/vitruvius/kg/schemas.py` + `enums.py` |
| Structured LLM client | Reliable extraction output | `scripts/vitruvius/llm/structured_client.py` |
| Taxonomy root seed files | Curated top-level ontology | `003_Canonical-Knowledge-Layer/shared/taxonomy/*.md` |
| Parser structural output | Section/chunk maps for evidence spans | Updated `BaseParser.parse()` + one implemented parser |
| Selector resolution | Verify evidence spans point to real text | `scripts/vitruvius/kg/selector_resolver.py` + seed tests |
| Document version backfill | Every source needs a v1 record | One-time script: `scripts/vitruvius/kg/backfill_document_versions.py` |
| Feature flags | Safe parallel development | `kg_transition.*` block in `config/vitruvius.yaml` |

---

## 6. Dependency Ordering / Readiness Gates

```text
Gate 0: Architecture Resolution
├── AD-043 drafted and merged
├── Graph contract bumped to 2.0.0-alpha
└── Backward compatibility preserved (legacy_snapshot_mode)

Gate 1: Infrastructure
├── Neo4j installed and reachable
├── PostgreSQL installed and reachable
└── Python drivers in requirements.txt

Gate 2: Schema Freeze
├── Pydantic models created and tested
├── Neo4j Cypher schema idempotent
└── PostgreSQL DDL created and tested

Gate 3: Data Seed
├── Taxonomy roots created (≥8)
├── Document versions backfilled (100% of sources)
└── Evidence span seed set created (≥10 spans, 100% resolvable)

Gate 4: Tooling
├── Feature flags added to config
├── Structured LLM client implemented and benchmarked (≥90% validity)
└── Promotion rules extended for new node/assertion types

Gate 5: Process
├── Component owners assigned
├── Walkthrough completed
└── Rollback plan documented
```

**Sequencing rule:** Gate N cannot begin until Gate N-1 is green. Gates 0–2 are strictly sequential. Gates 3–5 can partially overlap once Gate 2 is green.

---

## 7. Migration Safety Requirements

### 7.1 Dual-Write / Dual-Read

- **Legacy path:** `build-graph` continues producing v1 JSON snapshots.
- **New path:** `kg-ingest-evidence` writes to Neo4j + PostgreSQL.
- **Rule:** The new path must not write to `003_Canonical-Knowledge-Layer/shared/` until Phase 4 (canonicalization). This preserves the legacy pipeline's input directories.

### 7.2 Backfill Safety

- Document version backfill (`backfill_document_versions.py`) is **read-only** on `001_Raw-Source-Layer/` and `003_Canonical-Knowledge-Layer/shared/sources/`.
- It writes only to PostgreSQL `document_version` table.
- If backfill fails, drop the table and rerun. No file-native data is modified.

### 7.3 Idempotency

- All new KG CLI commands must be idempotent:
  - `kg-ingest-evidence <path>` — check SHA-256 in `document_version`; skip if unchanged.
  - `kg-materialize-edges` — check `assertion_id` on existing edges; upsert, not duplicate.

### 7.4 Rollback Points

| Phase | Rollback Action | Safety |
|-------|----------------|--------|
| Phase 0 (Readiness) | Revert commits; drop Neo4j/Postgres tables | Safe — no file-native data touched |
| Phase 1 (Evidence Graph) | Delete Neo4j evidence nodes; drop Postgres evidence rows | Safe — file-native data untouched |
| Phase 2 (Extraction) | Delete candidate nodes/assertions from Neo4j; reset review queue | Safe |
| Phase 3 (Canonicalization) | Demote canonical nodes to `candidate`; restore review queue | Safe |
| Phase 4 (Assertions) | Dematerialize fast edges; revert assertions to `candidate` | Safe |
| Phase 5 (Query Switch) | Set `kg_transition.legacy_snapshot_mode: true`; rebuild v1 snapshot | Safe |
| Phase 6 (Deprecation) | Cannot rollback after legacy code is deleted | **IRREVERSIBLE** — only after parity proven |

### 7.5 Feature Flags

Add to `config/vitruvius.yaml`:

```yaml
kg_transition:
  enabled: false                    # Master kill-switch
  legacy_snapshot_mode: true        # Keep building v1 JSON snapshots
  neo4j_backend: false              # Enable Neo4j writes
  postgres_registry: false          # Enable PostgreSQL registry
  evidence_graph: false             # Enable document→version→section→chunk→span pipeline
  assertion_layer: false            # Enable reified assertions
  taxonomy_seeding: false           # Allow AI to propose taxonomy placements
  structured_extraction: false      # Require JSON-schema-constrained LLM output
  incremental_updates: false        # Enable subgraph delta updates
  qdrant_retrieval: false           # Enable Qdrant hybrid search (Sprint 3+)
```

**Rule:** No flag may be removed until the feature is production-ready and parity is confirmed.

### 7.6 Observability (Minimum)

Before Sprint 1, add at minimum:
- Structured logging for all `kg-*` CLI commands (Python `logging` module, not `print()`).
- Audit events in PostgreSQL `audit_event` table for every ingestion run, extraction run, and promotion action.

---

## 8. Testing Readiness

### 8.1 Required Test Scaffolding

Before the main execution begins, these test files must exist and pass:

- `scripts/tests/test_kg_schemas.py` — Pydantic model validation, JSON Schema export, roundtrip serialization
- `scripts/tests/test_neo4j_backend.py` — Connection, schema creation, CRUD, traversal
- `scripts/tests/test_postgres_registry.py` — CRUD on all minimum tables
- `scripts/tests/test_structured_llm_client.py` — Mocked LLM responses, retry logic, validation failure handling
- `scripts/tests/test_selector_resolver.py` — Resolution accuracy, quote-matching validation
- `scripts/tests/test_kg_feature_flags.py` — Toggling flags does not break existing pipeline

### 8.2 Golden Dataset

Create a seed golden dataset (≥20 documents) covering:
- Clean PDF
- Scanned PDF
- Markdown
- Tables
- Sections with exceptions
- Cross-references
- Definition-heavy sections
- Rule-heavy sections

**Location:** `scripts/vitruvius/kg/gold_dataset.py` or `006_System-Manifests/gold/`

### 8.3 Benchmark Targets

- Structured output validity: ≥90% first-pass on seed set
- Selector resolution: 100% of seed spans resolve to correct text
- Taxonomy root stability: 0% AI-invented top-level branches

---

## 9. Exit Criteria to Begin Implementation

All of the following must be true before Sprint 1 starts:

1. [ ] AD-043 merged; graph contract bumped to `2.0.0-alpha`; legacy compatibility preserved.
2. [ ] Neo4j installed and reachable; `pytest scripts/tests/test_neo4j_backend.py` passes.
3. [ ] PostgreSQL installed and reachable; `pytest scripts/tests/test_postgres_registry.py` passes.
4. [ ] Pydantic models frozen in `scripts/vitruvius/kg/schemas.py`; all enum types defined; JSON Schema exported.
5. [ ] `kg_transition` feature flags added to `config/vitruvius.yaml`; toggling `enabled: false` does not break `python scripts/pipeline_cli.py build-graph`.
6. [ ] ≥8 taxonomy root files created in `003_Canonical-Knowledge-Layer/shared/taxonomy/` and pass frontmatter lint.
7. [ ] 100% of source pages have v1 `document_version` records with valid SHA-256 in PostgreSQL.
8. [ ] ≥10 evidence spans created with resolvable selectors; 100% pass quote-matching.
9. [ ] `StructuredLLMClient` implemented and benchmarked at ≥90% validity on seed set.
10. [ ] Component owners assigned and briefed; walkthrough completed.
11. [ ] Rollback plan documented; all rollback points defined through Phase 5.

---

## 10. Exit Criteria to Move Between Major Phases

### Phase 0 → Phase 1 (Evidence Graph)
- [ ] All 11 readiness exit criteria are green.
- [ ] A single document can be ingested into the evidence graph (document → version → section → chunk → span) end-to-end via CLI.
- [ ] Neo4j query `MATCH (d:DocumentVersion)-[:HAS_SECTION]->(s)-[:HAS_CHUNK]->(c)-[:HAS_SPAN]->(e) RETURN count(e)` returns expected count.

### Phase 1 → Phase 2 (Atomic Extraction)
- [ ] Evidence graph covers ≥5 representative documents.
- [ ] `kg-extract-candidates` produces valid Pydantic models for concept, rule, definition candidates.
- [ ] Every candidate has ≥1 supporting span ID.

### Phase 2 → Phase 3 (Canonicalization)
- [ ] Extraction run produces ≥50 candidate nodes and ≥30 candidate assertions.
- [ ] Dedupe precision ≥95% on gold dataset.
- [ ] Placement engine places ≥80% of candidates without human review (seed taxonomy only).

### Phase 3 → Phase 4 (Assertions)
- [ ] ≥20 canonical nodes promoted to `validated` status.
- [ ] Taxonomy tree has ≥3 levels deep (roots + branches + leaves).
- [ ] Review queue is operational; candidates can be approved/rejected via CLI.

### Phase 4 → Phase 5 (Query Switch)
- [ ] 100% of visible edges in Neo4j carry an `assertion_id`.
- [ ] Edge inspector resolves full assertion detail + evidence + deep links.
- [ ] Parity checker shows ≥95% coverage of legacy nodes/edges.

### Phase 5 → Phase 6 (Legacy Deprecation)
- [ ] Product queries use canonical graph for ≥30 days without critical regression.
- [ ] All stakeholders confirm legacy snapshot is no longer needed.
- [ ] Documentation updated to reflect new architecture.

---

## 11. Timeline Estimate

| Phase | Duration | Depends On |
|-------|----------|------------|
| Gate 0: Architecture resolution | 1–2 days | Human decision on AD-043 |
| Gate 1: Infrastructure provisioning | 1–2 days | DevOps / local setup |
| Gate 2: Schema design & implementation | 2–3 days | Pydantic v2 familiarity |
| Gate 3: Data seeding | 2–3 days | Domain expert for taxonomy roots |
| Gate 4: Tooling | 2–3 days | LLM benchmarking |
| Gate 5: Process & ownership | 1 day | Team scheduling |
| **Total readiness phase** | **~10–14 days** | All gates green |

---

*End of Readiness Plan*
