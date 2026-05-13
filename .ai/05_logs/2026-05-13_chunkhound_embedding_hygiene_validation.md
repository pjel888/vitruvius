# Validation - ChunkHound Embedding Hygiene

## Changes

- `.chunkhound.json` now excludes:
  - `003_Canonical-Knowledge-Layer/shared/sources/**`
  - `003_Canonical-Knowledge-Layer/shared/relationships/**`
  - `config/vitruvius.yaml`
- `scripts/chunkhound_analyze.sh` now passes `--config-file-size-threshold-kb 10`.

## Root Cause Confirmed

DuckDB inspection showed the only missing active `embeddings_768` records were from `config/vitruvius.yaml`, specifically a large YAML `features` block with 11,361 characters. ChunkHound also repeatedly timed out on 95 huge canonical source markdown files.

## Validation Commands

```bash
bash ./scripts/chunkhound_analyze.sh
```

Result: exit code `0`.

Post-run database check:

- `missing_768`: empty
- `config/vitruvius.yaml` file rows in ChunkHound DB: `0`
- `003_Canonical-Knowledge-Layer/shared/sources/%` file rows in ChunkHound DB: `0`
- `003_Canonical-Knowledge-Layer/shared/relationships/%` file rows in ChunkHound DB: `0`

```bash
bash ./scripts/refresh_code_intelligence.sh
```

Result: exit code `0`.

Observed final refresh state:

- GitNexus: already up to date
- ChunkHound:
  - `3723 files`
  - `79695 chunks`
  - `79695 embeddings`
  - processed `0` files
  - errors `0`
  - no `tree-sitter-yaml` warnings
  - no OpenAI-compatible embedding context error
  - no timeout list
- code-review-graph:
  - full build completed
  - `768 files`
  - `9438 nodes`
  - `98269 edges`
  - `431` flows
  - no YAML parser warnings

```bash
git diff --check -- .chunkhound.json scripts/chunkhound_analyze.sh scripts/code_review_graph_update.sh requirements.txt .ai/01_roadmap/current-phase.md .ai/13_research/2026-05-13_code_review_graph_yaml_parser_isolation_research.md .ai/02_audits/2026-05-13_code_review_graph_yaml_parser_isolation_audit.md .ai/03_plans/2026-05-13_code_review_graph_yaml_parser_isolation_plan.md .ai/13_research/2026-05-13_chunkhound_embedding_hygiene_research.md .ai/02_audits/2026-05-13_chunkhound_embedding_hygiene_audit.md .ai/03_plans/2026-05-13_chunkhound_embedding_hygiene_plan.md
```

Result: passed. Git emitted only expected LF/CRLF working-copy warnings.

## Safety

- No canonical/source files were deleted or rewritten.
- No active graph files were modified.
- No Resource Layer records were modified.
- No Neo4j/Postgres writes occurred.
- No pending overlay admission occurred.
