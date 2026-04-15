---
plan_id: phase-9-query-ai-layer
phase: 9
title: Query & AI Augmentation Layer
status: gated
priority: low
sprint: "Post-Phase-8 (after graph snapshot stable with >= 200 verified relationships)"
version: 1.0.0
plan_type: design_spec
created: 2026-04-14
last_updated: 2026-04-14
owner: Senior Systems Architect
prerequisites:
  - Phase 8 Graph Contract & Indexing shipping
  - >= 200 verified relationships in the graph snapshot
  - Phase 3C concept enrichment complete (answers cite real definitions)
dependencies:
  - .ai/06_specs/relationship-schema.md
  - 005_Operational-Intelligence-Layer/graph/latest_graph_snapshot.json
related_plans:
  - phase-8-graph-contract-indexing-plan.md (upstream, hard dependency)
gate:
  condition: "Phase 8 stable; >= 200 verified relationships; >= 15 enriched concepts"
  rationale: "Query answers are only as good as their underlying graph. Do not ship query before the data is trustworthy."
unblocks:
  - Phase 12 AI-Augmented Reasoning (long-term; gated on Phase 9 accuracy)
---

# Phase 9 — Query & AI Augmentation Layer Design Plan

**Goal:** Enable high-fidelity, source-cited domain queries over the filesystem graph — `"What governs building permits?"`, `"Which sections limit lot occupancy?"`, `"Which concepts depend on occupancy classification?"` — with ≥95% citation accuracy on a seed-question suite.

**Architecture:** Three layers. **(1) Structured query interface** (`query_engine.py`) exposes typed Python functions that walk the graph snapshot and return evidence-joined results. **(2) Optional NL front-end** (`query_nl.py`) uses the local LLM to translate a natural-language question into a structured query call — it NEVER generates free text for answers. **(3) CLI + human-readable formatter** (`query_cli.py`) renders results with citations. The NL front-end is opt-in; a developer can always call the structured interface directly.

**Tech Stack:** Python stdlib; existing Ollama HTTP client for the NL translator. No new runtime dependencies.

---

## Design Principles

1. **Every answer cites a section.** A query that cannot cite at least one `source_section_id` with an evidence snippet fails the response, returning `"No supporting evidence found"` rather than speculating.
2. **Confidence-aware.** Every answer carries an aggregate confidence derived from the minimum `confidence_score` across its supporting evidence.
3. **Structured first.** The NL front-end is sugar on top of the structured interface. Developers can always drop down to the structured API to debug.
4. **No hallucination-capable answers.** The LLM never generates prose. It only selects from a finite set of query templates and binds entity parameters.
5. **Deterministic.** Two identical queries on the same snapshot produce byte-identical results.

## Scope Boundary

**In scope:**
- Structured query API: `what_governs`, `what_requires`, `what_limits`, `what_defines`, `what_depends_on`, `what_affects`, `supersession_chain`, `neighbors`, `edges_between`.
- Source traceability: every result carries `source_id`, `source_section_id`, `evidence_snippet`, `confidence`.
- Aggregate confidence: min of all supporting evidence.
- CLI: `query "<NL question>"` and `query-structured --function what_governs --subject concept-X`.
- Optional NL translator that maps questions to structured calls.
- Seed-question accuracy suite.

**Out of scope:**
- Generative answering (no free-text LLM responses).
- Multi-hop reasoning beyond depth 3 (a Phase 12 concern).
- Cross-document entity linking / disambiguation beyond what Phase 3C provides.
- Vector search / RAG / embeddings.
- UI (web, Streamlit, etc.).
- Caching query results (premature until latency is proven to be a problem).

## File Structure

| Path | Purpose |
|---|---|
| `scripts/vitruvius/query/__init__.py` | Package marker |
| `scripts/vitruvius/query/engine.py` | Structured query functions (pure functions over `GraphSnapshot`) |
| `scripts/vitruvius/query/result.py` | `QueryResult` and `QueryCitation` dataclasses |
| `scripts/vitruvius/query/nl_translator.py` | Optional LLM-backed NL → structured call translator |
| `scripts/vitruvius/query/cli_formatter.py` | Human-readable renderer with citations |
| `scripts/pipeline_cli.py` | Modify — add `query` and `query-structured` commands |
| `scripts/tests/test_query_engine.py` | Structured query tests on fixture graph |
| `scripts/tests/test_query_nl_translator.py` | NL translator tests (mocked LLM) |
| `scripts/tests/test_query_formatter.py` | Output rendering tests |
| `scripts/tests/fixtures/seed_questions.yaml` | Seed-question accuracy suite |

---

## Data Model

```python
@dataclass
class QueryCitation:
    source_id: str
    source_section_id: str
    evidence_snippet: str
    confidence: float


@dataclass
class QueryResult:
    question: str                # the original question (may be structured-call description)
    answer_entities: list[str]   # IDs of matched entities
    citations: list[QueryCitation]
    aggregate_confidence: float  # min across citations
    has_evidence: bool           # False => "No supporting evidence found"
    query_function: str          # e.g., "what_governs"
    arguments: dict              # e.g., {"subject": "concept-building-permit"}
```

Every public function in `engine.py` returns a `QueryResult` — never raw nodes or edges.

## Structured Query Interface

### `engine.what_governs(subject_id: str, snapshot: GraphSnapshot) -> QueryResult`
"Which sources govern `<subject_id>`?"
- Finds all edges where `to_id == subject_id` and `type == "governs"`.
- For each, resolves the `evidence_id` to a relationship file, pulls all `evidence[]` entries, and emits a citation per entry.
- `answer_entities` = set of `from_id` values.

### `engine.what_requires(subject_id: str, snapshot) -> QueryResult`
Same pattern, `type == "requires"`, `from_id == subject_id`.

### `engine.what_limits(subject_id: str, snapshot) -> QueryResult`
`type == "limits"`, `to_id == subject_id`.

### `engine.what_defines(subject_id: str, snapshot) -> QueryResult`
`type == "defines"`, `to_id == subject_id`.

### `engine.what_depends_on(subject_id: str, snapshot) -> QueryResult`
`type == "depends_on"`, `from_id == subject_id`.

### `engine.what_affects(subject_id: str, snapshot) -> QueryResult`
`type == "affects"`, `from_id == subject_id` OR `to_id == subject_id` (symmetric query).

### `engine.supersession_chain(subject_id: str, snapshot) -> QueryResult`
Follows `supersedes` edges transitively, up to 5 hops.

### `engine.neighbors(subject_id: str, snapshot, *, predicate: str | None = None) -> QueryResult`
Undirected neighborhood, optionally filtered by predicate.

### `engine.edges_between(a: str, b: str, snapshot) -> QueryResult`
All edges in either direction between `a` and `b`.

**Critical invariant:** every `QueryResult.has_evidence == True` case must contain ≥1 non-empty `QueryCitation` with `source_section_id != ""`.

## NL Translator (Optional)

### Prompt shape (sent to local LLM)
```json
{
  "task": "Translate a natural-language question into a structured query call",
  "question": "What governs building permits?",
  "allowed_functions": [
    "what_governs", "what_requires", "what_limits", "what_defines",
    "what_depends_on", "what_affects", "supersession_chain",
    "neighbors", "edges_between"
  ],
  "known_entities": ["concept-building-permit", "concept-occupancy-classification", ...],
  "output_schema": {
    "function": "one of allowed_functions",
    "arguments": {"subject": "one of known_entities"},
    "confidence": "0.0-1.0"
  }
}
```

### Rules
- If the LLM returns a function not in `allowed_functions`, fall back to `neighbors` with no subject (returns an error-level `QueryResult`).
- If the LLM's `confidence < 0.8`, the CLI prints the translation and asks for confirmation.
- `known_entities` is capped at the 100 most-connected entities in the graph to bound prompt size.

### Why the LLM is only a translator
- It never writes the answer.
- It never invents entities.
- The structured API runs afterwards and provides the citations.
- Worst-case output of a hallucination: a wrong query function on a wrong subject — still returns `has_evidence: false` rather than a fake citation.

## CLI Commands

| Command | Action |
|---|---|
| `query "<question>"` | NL → structured → formatted. Prints answer + citations. |
| `query-structured --function what_governs --subject concept-X` | Skip NL; call the structured API directly. |
| `query --explain` | Print the NL translator's structured interpretation alongside the answer. |

## Output Format (human-readable)

```
Question: What governs building permits?

Answer: The National Building Code of the Philippines governs `concept-building-permit`.

Confidence: 0.92

Supporting Evidence:
  [1] law-national-building-code-of-the-philippines §sec-301
      "No person, firm, or corporation... shall erect, construct, alter, repair,
       move, convert or demolish any building or structure without first
       obtaining a building permit..."
      Confidence: 0.92

Query trace:
  function: what_governs
  arguments: {"subject": "concept-building-permit"}
  snapshot: 005_Operational-Intelligence-Layer/graph/latest_graph_snapshot.json
```

## Seed Question Suite

`scripts/tests/fixtures/seed_questions.yaml`:
```yaml
questions:
  - q: "What governs building permits?"
    expected_function: what_governs
    expected_subject: concept-building-permit
    expected_citation_count: ">= 1"
    expected_source_ids: ["law-national-building-code-of-the-philippines"]

  - q: "Which concepts depend on occupancy classification?"
    expected_function: what_depends_on
    expected_subject: concept-occupancy-classification
    expected_citation_count: ">= 1"

  - q: "What defines fire-resistive construction?"
    expected_function: what_defines
    expected_subject: concept-fire-resistive-construction

  # ... at least 10 seed questions covering every public function
```

Accuracy metric: number of questions where (a) the translator picks the right function, (b) the structured call returns `has_evidence: true`, and (c) at least one expected source_id is in the citations.

**Target:** ≥95% on the seed suite to close Phase 9.

## Task Sequence (High-Level)

1. **`result.py`** — `QueryResult` and `QueryCitation` dataclasses. Tests for serialization.
2. **`engine.py`** — `what_governs` first (simplest), then the rest in the order above. One test per function using a fixture graph snapshot.
3. **`engine.py`** — evidence aggregation + `aggregate_confidence` helper.
4. **`nl_translator.py`** — prompt builder + stub call. Tests with mocked LLM responses.
5. **`cli_formatter.py`** — render `QueryResult` to the human-readable format above. Snapshot tests for deterministic output.
6. **`pipeline_cli.py`** — register `query` and `query-structured`.
7. **Seed-question accuracy run.** Measure, document results in `decisions.md` as `AD-XXX`.

Full TDD expansion is deferred until this plan's implementation starts.

## Gating Metrics

- **Seed-question accuracy:** ≥95%.
- **Citation accuracy:** every returned result's `citations[].source_section_id` resolves to a real section.
- **Latency:** <2s per query on the filesystem snapshot for graphs up to 1000 nodes.
- **Determinism:** identical input → byte-identical output (for the structured API).

## Non-Goals
- Generative answering.
- Multi-language support beyond English.
- Caching (premature optimization).
- Graph mutations via the query API (read-only).
- Streaming responses.

## Risks
| Risk | Mitigation |
|---|---|
| NL translator confidently picks the wrong function | `--explain` flag prints the translation; seed-question suite catches systematic errors. |
| Answers cite superseded sources | Graph builder drops superseded edges (Phase 8 design choice). |
| Users expect free-text answers | CLI help explicitly states "cites the canonical graph; does not generate new text". |
| LLM returns entities not in the known-entities list | Validation step in the translator rejects and falls back to `neighbors`. |

## Open Design Questions
- Whether to implement `list_nodes_by_type(type: str)` as a 10th public function. Likely yes; trivial to add once the pattern is established.
- Whether the CLI should support `--json` output for machine consumers. Likely yes in a follow-up.
- Whether `affects` queries should distinguish in/out direction. Current answer: no, `what_affects` is symmetric; use `neighbors --predicate affects` for direction.

## Self-Review Checklist
- Every public function in the structured API has a seed question and a test.
- No function is allowed to return a `QueryResult` with `has_evidence: true` AND `citations: []`.
- The NL translator never produces free text.

## Execution Handoff
Design-spec form. Before execution, expand the 7 tasks into TDD with code. Subagent-driven recommended.
