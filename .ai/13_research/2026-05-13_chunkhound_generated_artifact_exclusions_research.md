# Research Pack - ChunkHound Generated Artifact Exclusions

## Question

Why is the code-intelligence refresh repeatedly warning during ChunkHound analysis, and what is the smallest safe change?

## Evidence

- `./scripts/refresh_code_intelligence.sh` completed with exit code `0`, but ChunkHound repeatedly attempted to embed generated AEC relationship campaign and source-grounding operational artifacts.
- The noisy generated trees are under:
  - `006_System-Manifests/aec-mepfs-backbone/semantic-overlays/`
  - `006_System-Manifests/aec-mepfs-backbone/source-grounding-inventory/`
- These directories contain run artifacts, reports, JSONL logs, and inventory output. They are operational evidence, not source code.
- `.chunkhound.json` already had targeted exclude support for large non-source markdown artifacts.

## Boundary

This research does not authorize deletion, rewriting, or admission of generated artifacts. It only supports excluding generated output trees from semantic code indexing.

## Conclusion

The smallest safe fix is to add the two generated AEC artifact trees to `.chunkhound.json` excludes. This preserves source code, tests, documentation, plans, and active governance files in the index while avoiding repeated oversized embedding attempts against generated operational output.
