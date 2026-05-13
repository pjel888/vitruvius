# Validation - ChunkHound Generated Artifact Exclusions

## Change

Updated `.chunkhound.json` to exclude generated AEC operational artifact trees:

- `006_System-Manifests/aec-mepfs-backbone/semantic-overlays/**`
- `006_System-Manifests/aec-mepfs-backbone/source-grounding-inventory/**`

## Validation Commands

```bash
bash ./scripts/refresh_code_intelligence.sh
```

Result: exit code `0`.

Observed outcome:

- ChunkHound accepted the updated config.
- The previous oversized embedding errors from generated campaign/source-grounding artifact logs were no longer observed.
- Existing non-blocking warnings remained:
  - timeout skips for 95 large canonical source files
  - code-review-graph `tree-sitter-yaml` parser dependency warning
  - ChunkHound `_Task.elapsed` embedding-batch warnings

```bash
git diff --check -- .chunkhound.json .ai/03_plans/2026-05-13_chunkhound_generated_artifact_exclusions_plan.md .omx/context/chunkhound-generated-artifact-exclusions-20260513T093710Z.md
```

Result: passed. Git emitted only expected LF/CRLF working-copy warnings.

```bash
cmd /c npx --yes gitnexus@1.6.4-rc.32 detect-changes --repo vitruvius
```

Result: exit code `0`.

Note: GitNexus reported CRITICAL risk for the overall dirty worktree because many unrelated files are modified or untracked. That is a repository-state warning, not a scoped risk introduced by this `.chunkhound.json` change.

## Safety

- Active graph files were not modified.
- Resource Layer records were not modified.
- Neo4j/Postgres were not written.
- Pending overlay admission was not performed.
- No API keys or `reasoning_content` were added.
