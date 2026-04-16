# Research Pack — Laws Graph Quality Correction

## Purpose
Correct the current under-representation and misattribution problems in the bounded laws graph so future graph builds become more accurate, more meaningful, and more enterprise-grade.

## Current truth
- The bounded dataset graph is operationally valid:
  - `PD-1096`, `RA-9514`, `BP-344`, `BP-220` all report `covered`
- But the graph is still strongly imbalanced:
  - `PD-1096` dominates most nodes/edges
  - `BP-344` and `BP-220` each currently contribute only one admitted concept + one admitted relationship
- The visual graph exposed a real quality issue:
  - `BP-344` currently collapses to `accessible-ramps`
  - `BP-220` currently collapses to `socialized-housing-projects`

## Verified causes
### 1. Source provenance hardcoding
- `relationships.py` and `relationships_sections.py` still hardcode source-id derivation to PD-1096-oriented IDs
- `concept_enrichment._collect_source_texts()` currently attributes every refined markdown file to `law-national-building-code-of-the-philippines`

### 2. Concept matching is too weak
- current concept matching is substring-based
- no word-boundary safety
- no alias-aware matching
- no stable ordering of matches

### 3. Canonical source summaries are noisy
- some admitted source pages still show OCR-noisy overview/key-point output
- example: Fire Code source page starts with ISBN noise
- this reduces graph trust and operator confidence even when titles are correct

## Highest-value bounded correction lanes
1. source-id derivation fix for extraction paths
2. boundary-aware + alias-aware concept matching
3. targeted tests for false positives / ordering / non-PD source attribution
4. only then consider higher-risk enrichment-source attribution changes

## Design boundary
This slice should improve **accuracy plumbing** first.
It should not silently widen truth admission or pretend that all source-text concepts are already officially admitted graph truth.
