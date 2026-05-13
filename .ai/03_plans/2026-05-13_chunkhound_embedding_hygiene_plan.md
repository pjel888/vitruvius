# Plan - ChunkHound Embedding Hygiene

## Objective

Stop avoidable ChunkHound embedding/context and timeout noise while preserving the code-intelligence value of the index.

## Checklist

1. Add `003_Canonical-Knowledge-Layer/shared/sources/**` to `.chunkhound.json` excludes.
2. Add `003_Canonical-Knowledge-Layer/shared/relationships/**` to `.chunkhound.json` excludes.
3. Add `config/vitruvius.yaml` to `.chunkhound.json` excludes.
4. Add `--config-file-size-threshold-kb 10` to `scripts/chunkhound_analyze.sh`.
5. Run `bash ./scripts/chunkhound_analyze.sh`.
6. Confirm `tree-sitter-yaml` warnings are absent.
7. Confirm `config/vitruvius.yaml` no longer appears as missing `embeddings_768`.
8. Confirm the 95 canonical source timeout list is gone or materially reduced.
9. Run full code-intelligence refresh.
10. Record validation and review artifacts.

## Out Of Scope

- Deleting canonical source files.
- Rewriting source-document markdown.
- Changing embedding models.
- Disabling ChunkHound embeddings globally.
- Graph/Resource/API/Explorer behavior changes.
