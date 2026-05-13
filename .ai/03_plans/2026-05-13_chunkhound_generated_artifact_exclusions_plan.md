# Plan — ChunkHound Generated Artifact Exclusions

## Objective

Add generated AEC campaign/inventory artifact directories to `.chunkhound.json` excludes.

## Implementation Checklist

1. Add `006_System-Manifests/aec-mepfs-backbone/semantic-overlays/**` to ChunkHound excludes.
2. Add `006_System-Manifests/aec-mepfs-backbone/source-grounding-inventory/**` to ChunkHound excludes.
3. Keep source code, docs, `.ai`, and test files indexed.
4. Run ChunkHound or full code-intelligence refresh after the config change.
5. Record remaining known warnings separately.
