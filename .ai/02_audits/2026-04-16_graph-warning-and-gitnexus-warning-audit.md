---
task: graph-warning-and-gitnexus-warning
phase: "04"
created: 2026-04-16
author: IMPLEMENTER
supersedes: null
status: DRAFT
---

# Graph Warning and GitNexus Warning Audit — 2026-04-16

## Scope
1. Determine whether the current `build-graph` warnings should be fixed and, if so, remediate them truthfully.
2. Determine whether the GitNexus `MaxListenersExceededWarning` can be fixed locally, mitigated, or must be classified as an external-tool issue.

## Authority and state alignment
Read and aligned with:
- `AGENTS.md`
- `.ai/00_system/EXECUTION_LOOP.md`
- `.ai/00_system/principles.md`
- `.ai/00_system/pipeline-overview.md`
- `.ai/01_roadmap/current-phase.md`
- `.ai/01_roadmap/milestone-tracker.md`
- `.ai/10_state/known_issues.md`

## Current observed warnings
### 1. `build-graph`
Fresh run returns `passed: true` with 6 warnings:
- `concept-doors-and-exits`
- `concept-occupancy-load`
- `concept-open-courts`
- `concept-parking-and-loading-spaces`
- `concept-projections-over-public-ways`
- `law-pd-1096-national-building-code`

All warnings are currently `orphan_node` findings from `scripts/vitruvius/graph/integrity.py::_orphan_findings()`.

### 2. GitNexus analyze
Fresh raw `npx gitnexus analyze` completes successfully but prints repeated Node warnings:
- `MaxListenersExceededWarning: Possible EventEmitter memory leak detected. 11 drain listeners added to [WriteStream]`

## Code-grounded findings
### `build-graph` warnings are not all equal
1. The four enriched concept warnings are not random bad data. Their concept files contain `regulatory_basis` pointing at `law-national-building-code-of-the-philippines`.
2. The graph builder currently ignores that provenance metadata because it only creates edges from promoted relationship pages.
3. `concept-parking-and-loading-spaces` is different: it is still a draft placeholder concept with no `regulatory_basis` and no relationship references.
4. `law-pd-1096-national-building-code` appears to be a stale or duplicate source identity. Live concept/relationship references point instead to `law-national-building-code-of-the-philippines`.

### GitNexus warning is likely tool-side
1. The active `npx` cache uses GitNexus **1.6.1**.
2. The installed package already contains comments and partial mitigations specifically mentioning `MaxListenersExceededWarning`.
3. A remaining `ws.once('drain', ...)` path exists in the tool’s generated code (`dist/core/lbug/lbug-adapter.js`), consistent with the warning text.
4. This indicates an upstream listener-management issue in GitNexus, not a Vitruvius application bug.

## Audit conclusion
### `build-graph`
Yes, these warnings are worth fixing because most of them are artifacts of under-modeled provenance, not true semantic isolation. The correct fix is to improve graph construction, not merely suppress the warning.

### GitNexus
The GitNexus warning should be treated as an external-tool issue first. A repo-local workaround may be possible (for example, pinning a newer version or changing invocation), but the root cause is not in Vitruvius runtime code.
