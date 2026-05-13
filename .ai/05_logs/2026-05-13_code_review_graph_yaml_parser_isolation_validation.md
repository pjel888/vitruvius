# Validation - Code-Review-Graph YAML Parser Isolation

## Changes

- `scripts/code_review_graph_update.sh` now uses one direct `uvx --isolated --with tree-sitter-yaml code-review-graph build --repo .` path.
- `requirements.txt` now declares `tree-sitter-yaml>=0.7.0`.
- The local ChunkHound uv tool environment was reinstalled at `chunkhound==4.0.1` with `tree-sitter-yaml`.

## Commands

```bash
uv run --with tree-sitter-yaml python -c "import tree_sitter_yaml; print(tree_sitter_yaml.__name__)"
```

Result: passed.

```bash
uvx --with tree-sitter-yaml --from code-review-graph python -c "import tree_sitter_yaml; print(tree_sitter_yaml.__name__)"
```

Result: passed.

```bash
bash ./scripts/code_review_graph_update.sh
```

Result: exit code `0`; no `tree-sitter-yaml` parser warnings observed.

```bash
python -m pip install "tree-sitter-yaml>=0.7.0"
```

Result: installed `tree-sitter-yaml==0.7.2` in the active Python environment.

```bash
uv tool install chunkhound==4.0.1 --with tree-sitter-yaml --reinstall
```

Result: installed ChunkHound `4.0.1` with `tree-sitter-yaml==0.7.2` in the uv tool environment.

```bash
bash ./scripts/chunkhound_analyze.sh
```

Result: exit code `0`; no `tree-sitter-yaml` parser warnings observed.

## Remaining Warnings

- ChunkHound still reports 95 timeout-skipped large canonical source files.
- ChunkHound still reports one oversized embedding batch for 100 existing chunks:
  - OpenAI `input length exceeds the context length`
  - follow-on `_Task.elapsed` logging errors from ChunkHound's async batch handler

These are separate from the YAML parser dependency fix and should be handled as the next tooling hygiene item.

## Safety

- No active graph files were modified.
- No Resource Layer records were modified.
- No Neo4j/Postgres writes were performed.
- No pending overlay admission was performed.
