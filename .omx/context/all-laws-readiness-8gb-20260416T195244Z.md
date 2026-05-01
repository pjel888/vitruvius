# All-Laws Readiness & 8GB-Safe Rollout Context

## Task
Create the correct next step after the successful 4-law bounded pilot:
1. a whole-dataset readiness plan
2. an 8GB-safe review model preset
3. an all-laws dry-run command path first

## Desired outcome
- truthful repo-local readiness assessment for all-laws / whole-dataset work
- accepted research/audit/plan artifacts before implementation
- safe rollout for a MacBook Pro M2 with 8GB RAM
- no machine-breaking full-dataset run
- dry-run/readiness-first expansion path before any broad execution

## Known facts
- bounded 4-law pilot is working end-to-end
- repo-root helper `./run-laws-pilot` exists
- browser HTML is self-contained and verified
- current default review model is still gemma4:31b in config/runtime defaults
- Phase 11 generic expansion remains gated; bounded pilot does not authorize broad all-laws execution
- repo-local raw laws inventory count observed: 48 top-level law folders, 183 PDFs

## Constraints
- accuracy, truth integrity, code integrity, optimization, and machine safety first
- user is sleeping; proceed without asking unless truly destructive/branching
- use durable OMX team runtime for coordinated parallel work
- do not claim whole-dataset readiness unless verified
- keep expansion staged: readiness/docs first, then 8GB-safe preset, then all-laws dry-run path

## Unknowns / open questions
- exact shape of the all-laws dry-run manifest/command surface
- whether to implement preset as config preset, CLI flag, or both
- which .ai docs should be updated beyond plan/audit/log artifacts
- what degree of generated artifact handling should be committed vs ignored for future whole-dataset dry-runs

## Likely touchpoints
- .ai/01_roadmap/current-phase.md
- .ai/01_roadmap/milestone-tracker.md
- .ai/03_plans/*laws*
- .ai/05_logs/*laws*
- config/vitruvius.yaml
- scripts/pipeline_cli.py
- scripts/vitruvius/dataset_pipeline.py
- scripts/vitruvius/ollama_review.py
- scripts/vitruvius/config.py
- config/datasets/
