# Laws KG Hardening Context

## Task
Continue hardening the bounded laws source→graph pipeline and supporting graph surfaces.

## Desired outcome
- cleaner canonical source summaries for difficult laws/IRRs
- stronger source-difficulty / extraction-trust reporting
- continued execute-path truthfulness for the bounded source→graph lane
- human-readable graph/query output
- no shortcutting governance or raw→graph direct paths

## Known facts
- bounded source→graph execute lane exists and works
- dry-run planning lane exists and reports source quality summary
- latest bounded graph around 26 nodes / 94 edges
- high-severity refined sources include PD-1096 IRR and RA-9514 RIRR
- user allows internet-assisted benchmarking but not truth shortcuts

## Constraints
- accuracy, truth, and code integrity first
- no fake completeness
- no bypass of review/promotion
- dataset-local outputs for bounded dataset mode

## Likely touchpoints
- scripts/vitruvius/canonicalize.py
- scripts/vitruvius/dataset_pipeline.py
- scripts/vitruvius/query/*
- scripts/vitruvius/graph/*
- README.md
