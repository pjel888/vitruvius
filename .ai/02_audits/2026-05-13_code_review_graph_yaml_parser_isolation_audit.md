# Audit - Code-Review-Graph YAML Parser Isolation

## Scope

Review the blast radius of changing `scripts/code_review_graph_update.sh` from cached/special-cased `uvx` tool execution to one direct isolated `uvx` tool execution with the same YAML parser add-on.

## Findings

1. Runtime product behavior is unaffected.
   - The wrapper is code-intelligence tooling only.
   - It does not run application code, mutate graph data, write databases, or admit pending artifacts.

2. Dependency surface is minimally broadened for tooling reliability.
   - `tree-sitter-yaml` was already requested by the wrapper.
   - The change makes the tool environment isolated and removes the PowerShell hop so the requested add-on is actually visible in the build process.
   - `requirements.txt` now also declares `tree-sitter-yaml>=0.7.0` so repo-local Python environments and hooks can satisfy the same parser dependency.

3. Performance impact is acceptable.
   - A direct isolated build completed in about 12 seconds during local validation.
   - uv still reuses package caches.

4. Safety boundaries remain intact.
   - No active graph files are changed.
   - No Resource Layer files are changed.
   - No Neo4j/Postgres writes occur.
   - No API keys or protected source text are touched.

## Risk

Low. The main risk is a small increase in wrapper startup time if uv cache is cold and one additional lightweight parser dependency for local development environments. The benefit is deterministic parser availability during mandatory code-intelligence refreshes and simpler cross-shell behavior.

## Recommendation

Proceed.
