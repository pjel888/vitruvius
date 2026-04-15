"""Sprint WIKI — Autonomous Knowledge Synthesis narrow-slice package.

Ships three modules:
  * :mod:`docling_parser` — thin wrapper around ``docling.document_converter``
    that converts PDFs to Markdown with table + heading fidelity
    (WIKI.1 Structural Ingestion).
  * :mod:`kuzu_store` — hybrid Kuzu-backed store: upserts wiki-page
    YAML frontmatter into a graph database and exposes multi-hop
    queries (WIKI.3 Hybrid Storage).
  * :mod:`delta_tracker` — SHA-256 delta tracking for wiki files,
    layering on top of the HP.1 Merkle primitive (WIKI.4.1
    Differential Health).

The LLM-driven pieces (WIKI.2 Synthesis Loop + WIKI.4.2 Ego-Graph
Linter) are deferred because they need live Ollama round-trips
that are out of scope for in-session TDD.
"""
