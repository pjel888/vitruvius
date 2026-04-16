# 2026-04-16 Laws Graph Quality Correction Implementation Validation

## Scope implemented
- added reusable concept-matching helper:
  - `scripts/vitruvius/concept_matching.py`
- corrected source-id derivation helper:
  - `scripts/vitruvius/source_identity.py`
- routed:
  - `scripts/vitruvius/canonicalize.py`
  - `scripts/vitruvius/relationships.py`
  - `scripts/vitruvius/relationships_sections.py`
  through the improved matching / source-id helpers
- corrected refined-markdown source attribution in:
  - `scripts/vitruvius/concept_enrichment.py`
- added regression tests:
  - `scripts/tests/test_concept_matching.py`
  - `scripts/tests/test_source_identity.py`
  - updated `scripts/tests/test_concept_enrichment.py`

## Why this slice matters
The bounded official graph under-represented `BP-344` and `BP-220`.
The visual graph made the issue obvious, but the root cause was data-quality plumbing:
- substring concept matching
- PD-1096-centric source-id attribution

## Verification
- `python3 -m py_compile scripts/vitruvius/concept_matching.py scripts/vitruvius/source_identity.py scripts/vitruvius/canonicalize.py scripts/vitruvius/relationships.py scripts/vitruvius/relationships_sections.py scripts/vitruvius/concept_enrichment.py`
  - PASS
- `PYTHONPATH=scripts pytest -q scripts/tests/test_concept_enrichment.py scripts/tests/test_concept_matching.py scripts/tests/test_source_identity.py scripts/tests/test_canonicalize_body.py scripts/tests/test_relationships_sections_split.py scripts/tests/test_integration_e2e.py`
  - `24 passed in 0.26s`

## Fresh evidence: concept-hit breadth after correction
Using the corrected concept matcher against the refined markdown:

### BP-344
- matched concepts: `3`
- concepts:
  - `concept-accessible-ramps`
  - `concept-stairs`
  - `concept-means-of-egress`

### BP-220
- matched concepts: `7`
- concepts:
  - `concept-socialized-housing-projects`
  - `concept-yards`
  - `concept-setbacks`
  - `concept-floor-area`
  - `concept-light-and-ventilation`
  - `concept-stairs`
  - `concept-means-of-egress`

### RA-9514
- matched concepts: `13`

## Fresh evidence: extraction source ids after correction
Section-aware extraction now correctly derives non-PD source ids:
- BP-344 → `irr-revised-implementing-rules-and-regulations-of-batas-pambansa-blg-344`
- BP-220 → `irr-revised-implementing-rules-and-regulations-of-batas-pambansa-blg-220`

## Fresh evidence: section-window extraction improved concept coverage
After the correction pass, section-aware extraction on the refined markdown now yields:

### BP-344
- total relationships: `4`
- includes law-scoped governs edges for:
  - `concept-accessible-ramps`
  - `concept-stairs`
  - `concept-means-of-egress`

### BP-220
- total relationships: `8`
- includes law-scoped governs edges for:
  - `concept-socialized-housing-projects`
  - `concept-yards`
  - `concept-floor-area`
  - `concept-light-and-ventilation`
  - `concept-stairs`
  - `concept-setbacks`
  - `concept-means-of-egress`

## Remaining issue
Some concept→concept candidates are still noisy/spurious.
So the next correction step remains relation-extraction precision, not just concept-hit breadth.

## Fresh evidence: bounded official graph after manual quality-correction admission
Rebuilt bounded dataset graph:
- command:
  - `PYTHONPATH=scripts python3 scripts/pipeline_cli.py run-dataset-graph --dataset-manifest config/datasets/laws-core-bundle-m1.yaml --skip-export-owl`
- run id:
  - `20260416T105101Z`

### Resulting official bounded graph
- node_count: `26`
- edge_count: `60` (up from `53`)

### Coverage after correction admission
- `PD-1096`
  - `21` nodes
  - `56` edges
- `RA-9514`
  - `1` node
  - `2` edges
- `BP-344`
  - `2` nodes
  - `3` edges
- `BP-220`
  - `2` nodes
  - `8` edges

### Fresh query evidence
- `what_governs concept-stairs`
  - now returns:
    - `irr-implementing-rules-and-regulations-of-the-national-building-code`
    - `irr-revised-implementing-rules-and-regulations-of-batas-pambansa-blg-220`
    - `irr-revised-implementing-rules-and-regulations-of-batas-pambansa-blg-344`
- `what_governs concept-floor-area`
  - now returns:
    - `irr-implementing-rules-and-regulations-of-the-national-building-code`
    - `irr-revised-implementing-rules-and-regulations-of-batas-pambansa-blg-220`

## Explicit non-claim
This correction improves extraction and matching quality.
It does **not** by itself widen the official admitted manifest.
So the official bounded graph may still remain under-admitted until the newly supported concepts/relationships are reviewed and admitted into the bounded dataset lane.
