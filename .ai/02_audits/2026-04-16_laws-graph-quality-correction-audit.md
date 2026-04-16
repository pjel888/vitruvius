# Audit — Laws Graph Quality Correction

## Verdict
Proceed with a bounded correction slice focused on **source attribution** and **concept matching precision**.

## Why this is the right next move
- The graph is currently operational but not semantically balanced across the four admitted laws.
- The user-visible symptom is real: the graph under-represents `BP-344` and `BP-220`.
- The safest first fixes are plumbing-level, not mass truth-admission changes.

## In-scope corrections
- remove PD-1096-only source-id hardcoding in extraction paths
- replace substring-only concept matching with boundary-aware, alias-aware matching helpers
- add regression tests for concept matching and source-id attribution

## Out of scope for this correction step
- bulk automatic admission of new concepts/relationships into the official graph
- full rewrite of concept enrichment provenance collection
- pretending the official graph is already complete for every concept mentioned in raw/refined sources

## Risk notes
- changing extraction source ids is low-risk and bounded
- changing concept enrichment source collection is higher-risk and should follow after tests, not before
