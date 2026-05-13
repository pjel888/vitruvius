# Context Snapshot - ChunkHound Embedding Hygiene

## Task

Remove the remaining avoidable ChunkHound refresh noise after generated artifacts and YAML parser support were fixed.

## Desired Outcome

`scripts/chunkhound_analyze.sh` should not repeatedly:

- try to embed an oversized `config/vitruvius.yaml` YAML block
- spend time timing out on huge canonical source-document markdown payloads

## Evidence

- The active embedding model is `nomic-embed-text:latest` through the local OpenAI-compatible Ollama endpoint.
- ChunkHound reported an OpenAI-compatible embedding error: input length exceeds context length.
- Database inspection showed the only missing `embeddings_768` records were 100 chunks from `config/vitruvius.yaml`.
- The largest missing chunk was the `features` YAML block, 11,361 characters.
- ChunkHound also reports 95 timeout-skipped files under `003_Canonical-Knowledge-Layer/shared/sources/`.

## Constraints

- Do not delete source artifacts.
- Do not mutate graph files.
- Do not hide source code, tests, docs, or active `.ai` governance files.
- Keep ChunkHound useful for code and operator docs.
- Leave source-document custody/search to the repository's source-grounding and Resource Layer workflows, not the code-intelligence index.
