---
task: aec-mepfs-shadow-repo-state-helper
phase: 05
created: 2026-04-26
author: CODEX
status: PASS
supersedes: null
---

# Twenty-Ninth Shadow Slice: Shared Repo-State Helper

## Scope

Extract the duplicated shadow evidence repo-state reader into one shared
file-backed helper so route inventory, boundary audit, benchmark, and evidence
manifest reports cannot drift in how they classify source-tree dirtiness versus
generated-evidence dirtiness.

This slice is a Python helper/test refactor only. It does not promote the
shadow graph, write or query Neo4j, rebuild the KG, ingest protected content,
change feature flags, mount `/v2/resolve`, or make Explorer adopt the shadow
graph by default.

## Implementation

- Added `scripts/vitruvius/kg/backbone_repo_state.py`.
- Moved `git status --short --untracked-files=all` parsing into
  `git_status_paths`.
- Moved source/generated dirtiness classification into `read_repo_state`.
- Updated the four report generators to consume the shared helper:
  - `backbone_api_route_inventory.py`
  - `backbone_shadow_boundary_audit.py`
  - `backbone_shadow_benchmark.py`
  - `backbone_shadow_evidence_manifest.py`
- Added `scripts/tests/test_kg_backbone_repo_state.py` for parser and
  source/generated split coverage.
- Removed the route-inventory test's direct dependency on the former private
  `_git_status_paths` helper.

## Audit Findings

- GitNexus impact on the duplicated private helpers reported LOW risk and only
  local shadow evidence/report consumers.
- The generated-evidence prefix remains exactly
  `006_System-Manifests/aec-mepfs-backbone/`.
- The helper only shells out to local `git` commands and preserves the previous
  non-git-root behavior by returning clean/unknown commit metadata.
- No API, Explorer, Neo4j, KG rebuild, protected-content ingest, feature-flag,
  or live graph code was added.

## Plan Critique

- [C001] Commit the new helper with all four report consumers; omitting it
  would break imports.
- [C002] Do not broaden the generated-evidence prefix; doing so could hide
  source dirtiness.
- [C003] Do not treat this refactor as fresh clean-source evidence; regenerate
  reports only in a separate evidence-refresh slice if needed.

## Execution Checklist

- [x] Confirm GitNexus status is current before editing.
- [x] Run GitNexus impact on duplicated repo-state helpers.
- [x] Extract shared helper and replace all four report-generator copies.
- [x] Add focused helper tests.
- [x] Run focused and broad Python backbone suites.
- [x] Run Gemini/Kimi/native advisory review where available.
- [x] Record validation evidence.

## Explicit Non-Goals

- No Neo4j write, query, backup, restore, or cleanup.
- No KG rebuild/reset/load.
- No protected source content ingest.
- No feature flag cutover.
- No `/v2/resolve` or `/v2/resolve/trace` route mounting.
- No Explorer default graph adoption.
- No regenerated evidence packet in this slice.

## Next Safe Slice

Inspect remaining shadow-only opportunities after this helper extraction is
committed and pushed. Good candidates are parity fixture coverage hardening or a
fresh generated-evidence refresh from the new shared helper. Runtime integration
remains blocked.
