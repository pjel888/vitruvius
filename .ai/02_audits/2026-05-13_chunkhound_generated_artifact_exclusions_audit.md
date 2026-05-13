# Audit - ChunkHound Generated Artifact Exclusions

## Scope

Audit the proposed ChunkHound exclusion change for blast radius and safety.

## Findings

1. The change is tooling-only.
   - File touched: `.chunkhound.json`
   - Runtime behavior touched: none
   - API behavior touched: none
   - Explorer behavior touched: none

2. Excluded paths are generated operational artifact trees.
   - `006_System-Manifests/aec-mepfs-backbone/semantic-overlays/**`
   - `006_System-Manifests/aec-mepfs-backbone/source-grounding-inventory/**`

3. Source materials remain available on disk.
   - No files are deleted.
   - No graph files are mutated.
   - No Resource Layer records are admitted.
   - No protected source text is exposed.

4. Remaining code-intelligence warnings are separate issues.
   - ChunkHound still reports timeout skips for some large canonical source files.
   - code-review-graph still reports missing `tree-sitter-yaml`.
   - ChunkHound still reports `_Task.elapsed` embedding-batch warnings in some runs.

## Risk

Low. The risk is that future semantic searches will not return generated campaign/inventory artifacts. That is intentional because those trees are operational outputs, not code or design source.

## Recommendation

Proceed with the exclude change and record the remaining warnings as follow-up tooling hygiene, not blockers for Explorer/source-gap work.
