# Post Laws KG Rebuild Relationship Graph Audit - 2026-04-24

## Scope

Post-audit of the clean `001-Laws` raw-source to KG rebuild, Neo4j reload, Explorer-facing rule-title quality, source-title quality, and relationship distribution.

## Verdict

The current Explorer graph is a `001-Laws`-only rebuild. The graph is suitable for laws-only Explorer inspection, with two caveats:

- `001-Laws/refined_markdown/test/...` is inside the selected subject and contributed 2 source pages.
- Relationship semantics are still mostly provenance/structure edges. Cross-subject and richer semantic edges need a later aggregate enrichment pass.

## Evidence

Snapshot: `005_Operational-Intelligence-Layer/graph/kg-v2/20260424T195515Z_kg_v2_unified.json`

Entity counts:
- document_versions: 181
- sections: 905
- chunks: 724
- evidence_spans: 220
- canonical_nodes: 313
- relationship_assertions: 432
- placement_assertions: 302
- fast_edges: 734

Source-scope audit:
- canonical source pages: 181
- non-`001-Laws` source paths: 0
- generic/invalid source titles: 0
- conversion-layer files: 753, all under `002_Raw-Conversion-Layer/001-Laws/`
- subject caveat: 2 source pages originate from `001-Laws/refined_markdown/test/...`

Rule-title audit:
- rule nodes: 214
- missing display labels: 0
- duplicate display labels: 0
- generic display labels: 0
- display-title truncation markers: 0
- source-faithful label duplicates: 36, accepted because Explorer display titles use `display_label` while full source wording remains available for inspection.

Relationship distribution:
- `DEFINED_BY`: 214
- `SUPPORTED_BY`: 214
- `REQUIRES`: 3
- `RELATED_TO`: 1
- fast-edge `BELONGS_TO`: 302

Neo4j evidence:
- connectivity: true
- before reload: 2429 nodes
- after clear: 0 nodes
- load: 5911/5911 Cypher statements executed, 0 errors
- after load: 2429 nodes
- labels: 905 `Section`, 724 `Chunk`, 313 `CanonicalNode`, 220 `EvidenceSpan`, 181 `DocumentVersion`, 52 `Subtopic`, 23 `Topic`, 11 `Taxonomy`

## Fixes Applied

- Tightened source-title validation so navigation/front-matter headings such as `CONTENTS`, `ACKNOWLEDGEMENT`, `FOREWORD`, `PREFACE`, `CLUP`, `BERDE`, and law-number-only headings do not become canonical source titles.
- Repaired the generated `001-Laws` canonical source frontmatter and H1 titles without changing canonical IDs.
- Preserved source-faithful rule labels while keeping Explorer-facing `display_label` as the audited rule-title surface.
- Removed generated `...` truncation from rule extraction reasoning details and normalized HTML tag artifacts in generated rule summaries/labels.
- Rebuilt the unified snapshot and reloaded Neo4j from that rebuilt snapshot only.

## Residual Risks

- The graph remains laws-only by design. It will not discover Laws to Utilities or other cross-subject relationships until a combined enrichment pass runs.
- Relationship assertions remain dominated by structural provenance edges. This is truthful for the current build but not enough for mature semantic reasoning.
- Legacy relationship snippets still originate from the 300-character `relationships_sections.py` `source_text` cap. This is an optimization/quality target, not a blocker for rule display-title quality.
- `HLURB_Supplemental_Guidelines.pdf` still fails conversion through the current OpenDataLoader/Docling path during the full rebuild, while the pipeline continues and processes the rest of the subject.
