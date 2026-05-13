# Context Snapshot — ChunkHound Generated Artifact Exclusions

## Task

Reduce repeated code-intelligence refresh failures caused by very large generated AEC relationship campaign logs and source-grounding inventory outputs being sent to the embedding provider.

## Desired Outcome

Exclude generated campaign/inventory artifact trees from ChunkHound indexing while preserving source code, docs, plans, and active governance files in the index.

## Evidence

Recent `refresh_code_intelligence.sh` runs completed with exit code `0` but repeatedly logged oversized OpenAI embedding failures for campaign logs under:

- `006_System-Manifests/aec-mepfs-backbone/semantic-overlays/...`

Those directories are generated operational artifacts, not source code.

## Constraints

- Do not hide source code.
- Do not delete artifacts.
- Do not mutate active graph files.
- Do not change relationship workflow behavior.
