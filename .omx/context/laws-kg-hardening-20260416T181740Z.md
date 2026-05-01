# Laws KG Hardening Context

## Task
Continue hardening the bounded laws source→graph pipeline and supporting graph/query surfaces using durable OMX team mode.

## Desired outcome
- stronger source-difficulty / extraction-trust reporting
- cleaner canonical source summaries for difficult law/IRR sources
- continued execute-path truthfulness for the bounded source→graph lane
- no shortcutting governance or raw→graph direct paths
- preserve human-readable graph/query output

## Known facts
- latest committed head: 40c15bb
- bounded source→graph execute lane exists and works
- latest bounded execute run: 20260416T173622Z
- latest bounded graph build: 20260416T173918Z
- latest bounded graph: 26 nodes / 94 edges
- source quality severity counts: low=1 medium=2 high=2
- high-severity refined sources: PD-1096 IRR, RA-9514 RIRR
- dry-run trust summary now aggregates benchmark source hints and manual review requirements
- user allows internet-assisted benchmarking but forbids truth shortcuts

## Constraints
- accuracy, truth, and code integrity first
- no fake completeness
- no bypass of review/promotion
- dataset-local outputs for bounded dataset mode
- internet sources are benchmark/reference aids, not silent substitutions

## Likely touchpoints
- scripts/vitruvius/canonicalize.py
- scripts/vitruvius/dataset_pipeline.py
- scripts/vitruvius/query/*
- scripts/vitruvius/graph/*
- README.md
