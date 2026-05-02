# AEC Relationship Improvement Final UX Corrections Validation

Date: 2026-05-02

## Scope

Validated final corrections for the pending-only AEC relationship-improvement workflow:

- `scripts/vitruvius/kg/aec_relationship_improvement.py`
- `scripts/pipeline_cli.py`
- `scripts/tests/test_kg_aec_relationship_improvement.py`

The workflow remains Stage 1 Discovery only. It writes review artifacts under semantic-overlay run directories and does not mutate the admitted AEC Backbone graph, Neo4j, or Postgres.

## Verification

- `PYTHONPATH=scripts python -m pytest scripts/tests/test_kg_aec_relationship_improvement.py -q`
  - Result: `93 passed`
- `PYTHONPATH=scripts python -m pytest scripts/tests/test_kg_backbone_shadow_staging.py scripts/tests/test_kg_backbone_graph_quality.py -q`
  - Result: `18 passed`
- `python -m py_compile scripts/vitruvius/kg/aec_relationship_improvement.py scripts/pipeline_cli.py`
  - Result: passed
- `PYTHONPATH=scripts python scripts/pipeline_cli.py aec-improve-relationships --dry-run --council-mode deepseek_local --allow-cloud-ai --no-cloud-preflight --max-nodes 0 --max-pairs 0 --progress-mode plain`
  - Result: completed without model calls
- `PYTHONPATH=scripts python scripts/pipeline_cli.py aec-improve-relationships --apply --progress-mode off`
  - Result: rejected with the deferred apply-mode safety error

## Safety Confirmation

- Active graph fixture mutation remains outside this workflow.
- `--apply` still fails before execution.
- Kimi remains disabled unless explicitly selected with `--enable-kimi-experimental`.
- Cloud calls still require `--allow-cloud-ai`.
- Validation diagnostics, reports, events, and TSVs are sanitized for API keys, bearer tokens, `sk-*` strings, embeddings, and `reasoning_content`.

## Code Intelligence

`./scripts/refresh_code_intelligence.sh` completed after implementation. Existing repository warnings remain:

- YAML parser warnings for missing `tree-sitter-yaml`.
- code-review-graph embedding errors for long OpenAI embedding inputs and `_Task.elapsed`.

`npx.cmd --yes gitnexus@1.6.4-rc.32 detect-changes --repo vitruvius` reported critical repository-wide risk because the worktree contains many unrelated pre-existing changes. The scoped relationship-improvement tests and graph-quality tests pass.
