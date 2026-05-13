# Context Snapshot - Code-Review-Graph YAML Parser Isolation

## Task

Fix the remaining code-intelligence refresh warning where code-review-graph cannot load the YAML parser even though the wrapper already requests `tree-sitter-yaml`.

## Desired Outcome

`./scripts/refresh_code_intelligence.sh` should run code-review-graph without repeated `Missing: tree-sitter-yaml` warnings.

## Evidence

- `scripts/code_review_graph_update.sh` currently runs `uvx --with tree-sitter-yaml code-review-graph build --repo .`.
- `./scripts/refresh_code_intelligence.sh` still reports YAML parser warnings from code-review-graph.
- `uv run --with tree-sitter-yaml python -c "import tree_sitter_yaml"` succeeds.
- `uvx --with tree-sitter-yaml --from code-review-graph python -c "import tree_sitter_yaml"` succeeds.
- `uvx --isolated --with tree-sitter-yaml code-review-graph build --repo .` completed without the `tree-sitter-yaml` warnings.

## Constraints

- Do not mutate graph data.
- Do not change runtime/API/Explorer behavior.
- Do not add heavyweight dependency management churn.
- Keep the wrapper portable across Git Bash and direct shell usage.
