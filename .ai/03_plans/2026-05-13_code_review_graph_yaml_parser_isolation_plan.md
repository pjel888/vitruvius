# Plan - Code-Review-Graph YAML Parser Isolation

## Objective

Make code-review-graph refreshes consistently see `tree-sitter-yaml`.

## Checklist

1. Update `scripts/code_review_graph_update.sh` to use one direct `uvx --isolated --with tree-sitter-yaml` invocation.
2. Remove the special PowerShell hop that behaved inconsistently under the full refresh wrapper.
3. Add `tree-sitter-yaml>=0.7.0` to `requirements.txt` for local hook/parser environments.
4. Run `bash ./scripts/code_review_graph_update.sh` and confirm the YAML parser warnings disappear.
5. Run `bash ./scripts/refresh_code_intelligence.sh`.
6. Record validation and review artifacts.

## Out Of Scope

- Changing API, Explorer, relationship-improvement, graph, or Resource Layer behavior.
