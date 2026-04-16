---
task: graph-warning-and-gitnexus-warning
phase: "05"
created: 2026-04-16
author: IMPLEMENTER
supersedes: null
status: DRAFT
---

# Graph Warning and GitNexus Warning Plan — 2026-04-16

## Objective
First remove or materially reduce the current `build-graph` warnings using truthful graph semantics. Then investigate and, if feasible, fix or mitigate the GitNexus `MaxListenersExceededWarning`.

## In scope
- `scripts/vitruvius/graph/builder.py`
- `scripts/tests/test_graph_builder.py`
- `scripts/tests/test_graph_integrity.py`
- selected canonical source/concept files if a stale duplicate source node must be removed or reconciled
- validation/audit artifacts for both warning surfaces

## Out of scope
- broad graph schema redesign
- changing query product behavior beyond what is needed to support truthful graph edges
- patching GitNexus cached files in-place unless explicitly needed as a last-resort local workaround

## Execution sequence
### Part 1 — `build-graph` warnings
1. Add graph edges for provenance that already exists in canonical metadata:
   - source frontmatter relationships (for example `implements`)
   - concept `regulatory_basis` links to sources
2. Ensure placeholder concept nodes without grounding do not enter the operational graph when they are both:
   - ungrounded (no `regulatory_basis`)
   - unreferenced by any relationship edge
3. Resolve the stale unused law source page if it is confirmed to be a duplicate/obsolete identity.
4. Add targeted regression tests for the new graph-building behavior.
5. Re-run `build-graph` and the graph/query test slice.

### Part 2 — GitNexus warning
1. Verify whether the warning persists with a newer published GitNexus version.
2. If a newer version fixes it, prefer a local invocation/installation upgrade path over repo code changes.
3. If it persists, record it as an upstream bug and capture the best available local mitigation.

## Plan Critique
### C001 — warning suppression risk
Simply muting orphan warnings would preserve an under-modeled graph.
- **Mitigation:** add truthful provenance edges rather than changing integrity severity first.

### C002 — placeholder concept overreach risk
Blindly dropping all draft concepts from the graph could create dangling edges or hide live placeholders that are already referenced.
- **Mitigation:** only exclude concepts that are both ungrounded and unreferenced.

### C003 — stale source identity risk
Deleting a source page without confirming live references could break graph/query provenance.
- **Mitigation:** grep live references first and prefer the actively referenced canonical source identity.

### C004 — GitNexus scope drift risk
Patching external cached package files inside the repo task could create non-reproducible local fixes.
- **Mitigation:** prefer version upgrade or documented workaround; patch upstream only if clearly necessary.

## Execution Checklist
- [ ] G001 — implement provenance-aware graph edges
- [ ] G002 — exclude only truly ungrounded/unreferenced placeholder concept nodes
- [ ] G003 — resolve stale unused law source identity if confirmed safe
- [ ] G004 — add/adjust tests for new graph semantics
- [ ] G005 — verify `build-graph` and targeted graph/query tests
- [ ] G006 — test a newer GitNexus version or equivalent mitigation path
- [ ] G007 — write validation log with final recommendation for the GitNexus warning
