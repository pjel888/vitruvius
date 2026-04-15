"""Sprint LSH-1 — relationship MinHash + LSH fuzzy near-duplicate layer.

Package houses the fuzzy near-duplicate dedup layer that sits on top of
the existing O(n log n) dict-grouped exact-endpoint dedup in
:func:`vitruvius.relationships_sections.dedupe_by_endpoints`. See
``.ai/10_state/decisions.md`` AD-037 for the premise correction and the
language/runtime choice (Python, NOT Rust — cold path, once per ingestion
batch).
"""
