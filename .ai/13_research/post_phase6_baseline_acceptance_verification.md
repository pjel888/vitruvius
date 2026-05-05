# Post-Phase-6 Baseline Acceptance Verification

**Date:** 2026-05-06
**Verification commit:** `45b906d8e39a552f6a4d182e1450bbee90674403`
**Branch:** `main`
**Verdict:** PASS

## Git Evidence

Terminal stdout was visible and reliable.

| Check | Result |
|---|---|
| `pwd` | `C:\Users\phili\Desktop\vitruvius` |
| terminal marker | `VITRUVIUS_POST_PHASE6_TERMINAL_CHECK` visible |
| `git status --short --branch` | `## main...origin/main`; unrelated dirty worktree present |
| `git rev-parse HEAD` | `45b906d8e39a552f6a4d182e1450bbee90674403` |
| `git rev-parse origin/main` | `45b906d8e39a552f6a4d182e1450bbee90674403` |

Verified pushed Phase 6 closure commits in `git log --oneline -20`:

- `3521592b Validate resource-only promotion apply`
- `bc9b361f Plan resource-and-links promotion mode`
- `c1371f94 Implement resource-and-links promotion mode`
- `45b906d8 Close resource evidence baseline`

## Code Intelligence

`bash ./scripts/refresh_code_intelligence.sh` completed with exit code 0 before governance/report edits.

| Tool | Result |
|---|---|
| GitNexus | Re-indexed current commit; 28,422 nodes, 48,519 edges, 870 clusters, 300 flows |
| ChunkHound | Completed; known large-file timeout and embedding/context warnings persisted |
| code-review-graph | Full build completed; known `tree-sitter-yaml` parser warnings persisted |

These warnings were non-blocking for this docs/state closure task.

## Validator Evidence

| Command | Result |
|---|---|
| `bun run api/validateResourceLayer.ts -- --no-write` | PASS |
| `bun run api/validateGraphRelationships.ts -- --no-write` | PASS |
| `bun run api/validateCanonicalGraphStewardship.ts -- --no-write` | PASS |

## Test Evidence

| Command | Result |
|---|---|
| `cd api && bun test` | PASS, 398 pass / 0 fail |
| `cd explorer && bun test` | PASS, 118 pass / 0 fail; existing React key warning only |
| `cd explorer && bun run build` | PASS; existing Vite chunk-size warning only |
| `.venv\Scripts\python.exe -m pytest scripts/tests/test_kg_aec_relationship_improvement.py` | PASS, 118 pass |

## Verified Metrics

| Metric | Verified value |
|---|---:|
| Active admitted relationships | 264 |
| Base graph edges | 13,670 |
| Effective graph edges | 13,934 |
| `CROSS_DOMAIN_EQUIVALENT` | 0 |
| `CROSS_DOMAIN_ALIGNMENT` | 22 |
| Production resources | 7 |
| Production nodeResourceLinks | 9 |
| Existing resource candidates | 4 |
| Production external metadata candidates | 0 |
| Local files indexed / admitted | 25 / 0 |
| Standards missing context | 2 |
| Standards promotion blocked | 3 |

## Safety Findings

- Production Resource Layer data did not change: resources remain 7, nodeResourceLinks remain 9, external metadata candidates remain 0.
- `git diff -- 006_System-Manifests/resource-layer 006_System-Manifests/graph-canonical api explorer` returned 0 diff lines before this documentation update.
- ASCE 7 and ACI 318 remain incomplete and not learner-trusted.
- No learner exposure occurred.
- No external URL, DOI, ISBN, book API, PDF, or source verification occurred.
- No graph/canonical/P0/high-risk P1 mutation occurred.
- No Resource or nodeResourceLink was created.
- No candidate was promoted.

## Conclusion

The reported post-Phase-6 Resource/Evidence infrastructure baseline is verified from terminal evidence. Phase 6 can be accepted as closed, subject to the dirty worktree quarantine documented separately.
