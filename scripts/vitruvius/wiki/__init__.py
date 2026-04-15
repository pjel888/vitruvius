"""Sprint WIKI — Autonomous Knowledge Synthesis package.

Ships the full phase-14 slice:
  * :mod:`docling_parser` — thin wrapper around ``docling.document_converter``
    that converts PDFs to Markdown with table + heading fidelity
    (WIKI.1 Structural Ingestion).
  * :mod:`kuzu_store` — hybrid Kuzu-backed store: upserts wiki-page
    YAML frontmatter into a graph database and exposes multi-hop
    queries (WIKI.3 Hybrid Storage).
  * :mod:`delta_tracker` — SHA-256 delta tracking for wiki files,
    layering on top of the HP.1 Merkle primitive (WIKI.4.1
    Differential Health).
  * :mod:`llm_client` — shared :class:`LLMClient` Protocol so the
    LLM-driven streams are injectable and testable with mocks.
  * :mod:`synthesis_loop` — WIKI.2 Synthesis Loop: reads raw Markdown
    and proposes a strictly-validated :class:`WikiPageProposal` via
    ``pydantic.TypeAdapter.validate_json``.
  * :mod:`ego_linter` — WIKI.4.2 Ego-Graph Linter: feeds a focal
    page and its depth-2 neighbors to the LLM to detect
    contradictions and returns a :class:`ContradictionReport`.

  * :mod:`ollama_client` — production :class:`LLMClient` adapter
    backed by a local Ollama ``/api/generate`` endpoint with
    ``format="json"`` enforced. Operators inject
    :class:`OllamaLLMClient` into the synthesis loop and ego linter;
    unit tests keep using tiny in-memory mocks.
"""
