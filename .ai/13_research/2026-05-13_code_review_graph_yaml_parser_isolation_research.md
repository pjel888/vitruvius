# Research Pack - Code-Review-Graph YAML Parser Isolation

## Question

Why does code-review-graph still warn about missing `tree-sitter-yaml` during refresh when the wrapper already passes `uvx --with tree-sitter-yaml`?

## Evidence

- Current wrapper: `scripts/code_review_graph_update.sh`.
- The wrapper invokes code-review-graph through `uvx --with tree-sitter-yaml`.
- Direct import checks passed:
  - `uv run --with tree-sitter-yaml python -c "import tree_sitter_yaml; print(tree_sitter_yaml.__name__)"`
  - `uvx --with tree-sitter-yaml --from code-review-graph python -c "import tree_sitter_yaml; print(tree_sitter_yaml.__name__)"`
- The repository `.venv` does not currently have `tree_sitter_yaml` installed, so the parser must come from the `uvx` tool environment.
- A direct isolated code-review-graph run from bash passed without YAML parser warnings:
  - `uvx --isolated --with tree-sitter-yaml code-review-graph build --repo .`
- The full refresh remained inconsistent while the wrapper kept a special `powershell.exe` hop. Removing that hop gives the wrapper one deterministic execution path, matching the clean direct bash validation.
- The remaining warnings appeared before ChunkHound's own output in a captured full refresh, indicating a separate local parser path or hook could still be using the repository Python environment rather than the isolated wrapper.
- The emitted remedy is explicit: `pip install tree-sitter-yaml`.

## Inference

The stale or cached `uvx` tool environment can run code-review-graph without making the `--with tree-sitter-yaml` package visible to the parser path used during the build. `--isolated` forces a clean tool environment for the invocation while still using uv caches, which preserves a short runtime in local testing.

## Recommendation

Update `scripts/code_review_graph_update.sh` to run `uvx --isolated --with tree-sitter-yaml` directly from bash, without the special PowerShell branch, and declare `tree-sitter-yaml` in `requirements.txt` so local repo Python environments also satisfy the parser dependency.
