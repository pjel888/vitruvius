# Context Snapshot — laws-folder-mini-graph-pipeline

- created_utc: 20260416T002818Z
- task_statement: Study the Vitruvius codebase and create a consensus-backed implementation plan for a mini dataset->graph pipeline starting with the laws folder in the raw source layer.
- desired_outcome: New SEL-compliant planning artifacts (research, audit, plan with critique) that explain whether and how Vitruvius can output a knowledge graph for one folder/section now, then scale to per-section and interconnected graphs later.

## Known Facts / Evidence
- User wants planning only, not feature implementation yet.
- Existing repo already has graph-related commands (`build-graph`, `query-graph`, `export-graph-owl`) and a canonical-layer -> graph path.
- AEC Engine plans remain planning-only and unrelated to this immediate mini graph pipeline request.
- Active plan layer is under cleanup/maintenance; completed stabilization plans are archived.

## Constraints
- Must follow AGENTS/SEL: no plan without research and audit basis.
- Need repo-grounded, truthful plan — not speculative architecture fiction.
- Need to study current pipeline and graph surfaces first.
- Output the plan into `.ai/03_plans/`.

## Unknowns / Open Questions
- How close the existing code already is to a one-folder laws->graph pipeline.
- Whether the main gap is operator workflow/scoping or missing runtime stages.
- What folder-scoping and graph-output semantics already exist.
- What the smallest viable pilot scope should be (one laws folder, one subsection, one law family).

## Likely Touchpoints
- `scripts/pipeline_cli.py`
- `scripts/vitruvius/graph/*`
- `scripts/vitruvius/query/*`
- canonicalization / relationships / promotion modules
- `README.md` and roadmap/state docs for current graph status
- `.ai/09_archive/plans/phase-8-graph-contract-indexing-plan.md` and related archived planning docs
