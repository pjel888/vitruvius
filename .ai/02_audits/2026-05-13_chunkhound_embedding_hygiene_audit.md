# Audit - ChunkHound Embedding Hygiene

## Scope

Review the safety of excluding huge canonical source-document payloads from ChunkHound and skipping oversized structured config files.

## Findings

1. Source custody is preserved.
   - The canonical source files remain on disk.
   - No source document is deleted or rewritten.
   - No Resource Layer admission is performed.

2. Code-intelligence purpose is preserved.
   - Source code, tests, docs, `.ai` governance files, and most config files remain indexed.
   - `config/vitruvius.yaml` remains available to normal file reads and code-review-graph YAML parsing, but is skipped by ChunkHound because its `features` block exceeds embedding context.
   - Canonical source and relationship payloads are excluded from ChunkHound because they are knowledge/source artifacts, not code implementation surfaces.

3. The change reduces repeated refresh noise.
   - It removes the known oversized embedding candidate.
   - It prevents repeated timeout attempts on 95 large canonical source markdown files.

4. Product behavior is unaffected.
   - No API, Explorer, graph, Resource Layer, database, or relationship-improvement runtime behavior changes.

## Risk

Low to medium. The tradeoff is that ChunkHound semantic search will not cover canonical source-document/relationship payloads or the large root config file. This is acceptable because source-document discovery belongs to source-grounding/Resource workflows, and code-review-graph remains the structural YAML parser.

## Recommendation

Proceed.
