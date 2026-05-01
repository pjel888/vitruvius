# 2026-05-01 Code Intelligence and Valyu Governance Validation

## Scope

Added a repeatable code-intelligence refresh gate for future AI editing sessions and documented Valyu as an environment-backed external research tool.

## Changes

- Added `scripts/refresh_code_intelligence.sh` to run GitNexus, ChunkHound, and code-review-graph refreshes together.
- Added `scripts/chunkhound_analyze.sh` for repo-local ChunkHound indexing using `.chunkhound.json` and `.chunkhound/db`.
- Added `scripts/code_review_graph_update.sh` for repo-local full code-review-graph builds.
- Updated `AGENTS.md` and `.ai/00_system/EXECUTION_LOOP.md` so agents must refresh these indices before and after code/schema/runtime/active-governance edits.
- Documented Valyu usage through `VALYU_API_KEY` only and added `.env.example` with an empty placeholder; no API key is stored in the repository.

## Validation

- `bash -n scripts/gitnexus_analyze.sh scripts/chunkhound_analyze.sh scripts/code_review_graph_update.sh scripts/refresh_code_intelligence.sh`
- `cmd /c npx.cmd --yes gitnexus@1.6.4-rc.32 status`
- `chunkhound --version`
- `uvx code-review-graph status --repo .`
- `uvx --with tree-sitter-yaml code-review-graph build --repo .`
- `./scripts/refresh_code_intelligence.sh`
- `chunkhound search --regex --page-size 10 "VALYU_API_KEY|refresh_code_intelligence" .`
- `git diff --check`

## Notes

- The Valyu key must remain operator-local. If a key was exposed in chat or logs, rotate it before production use.
- The first code-review-graph refresh exposed missing YAML parser support. The wrapper now supplies `tree-sitter-yaml` through `uvx --with tree-sitter-yaml`.
- Incremental update left only a tiny diff graph in this workspace, so the wrapper uses full `code-review-graph build` to preserve reliable blast-radius context.
