# Canonical Graph Stewardship Loop Progress

Date: 2026-05-01

## Baseline diagnosis
- Current graph artifact: `006_System-Manifests/aec-mepfs-backbone/shadow-staging/20260501T082100Z/shadow-backbone-graph.json`.
- Existing relationship visibility loop remains active: `GET /node/:id/neighborhood` uses normalized relationship hydration and still exposes the Sendai Mediatheque/Toyo Ito semantic `HAS_FACET` edge.
- Existing duplicate report found 544 duplicate normalized-label groups, 251 safer review candidates, 293 manual/unsafe candidates, and 2 concrete-related groups.
- Graph edges use stable file-backed node IDs in Explorer graph payloads; Resource Layer `nodeResourceLinks` also point to graph node IDs.
- No production canonical merge/alias decisions existed before this loop (`006_System-Manifests/graph-canonical/` was absent).

## Concrete duplicate investigation
- `concrete`: `VTN-DOM-0000068` and `VTN-DOM-0000267`.
  - `VTN-DOM-0000068`: label `Concrete`, type `topic`, taxonomy `MAT > MAT.CON`, aliases include `cementitious materials`, `cast concrete`, 1 incoming / 3 outgoing edges, 0 resource links.
  - `VTN-DOM-0000267`: label `Concrete`, type `subtopic`, taxonomy `STR > STR.MAT > STR.MAT.CON`, aliases include `structural materials concrete`, 1 incoming / 5 outgoing edges, 0 resource links.
  - Risk: high because node type and taxonomy contexts differ. Status: unresolved, `NEEDS_HUMAN_REVIEW`; no merge applied.
- `reinforced concrete`: `VTN-DOM-0000271` and `VTN-DOM-0012147`.
  - `VTN-DOM-0000271`: label `Reinforced Concrete`, type `subtopic`, taxonomy `STR > STR.CON > STR.CON.RCO`, 1 incoming / 6 outgoing edges, 0 resource links.
  - `VTN-DOM-0012147`: label `Reinforced Concrete`, type `concept`, taxonomy `ARC > ARC.MAT > ARC.MAT.CON > ARC.MAT.CON.RCC`, aliases include `RC`, 23 incoming / 10 outgoing edges, 0 resource links.
  - Risk: high because node type/taxonomy differ and combined edge count is high. Status: unresolved, `NEEDS_HUMAN_REVIEW`; no merge applied.

## Implemented in this loop
- Added a file-backed canonical stewardship service with duplicate candidate groups, risk scoring, dry-run merge/alias/keep-separate previews, proposed/applied decision recording, alias records, redirect records, validation, locks, and transaction manifests.
- Added canonical API routes for duplicate queues, group detail, previews, decisions, decision history, node status, canonical-preferred search, and validation.
- Added `/dev/canonical-review` Explorer UI with local/dev gate messaging, duplicate group list/detail, concrete quick filter, structured decision form, dry-run diff preview, and safe apply/proposed decision controls.
- Integrated canonical alias preference into the AEC-MEPFS `/search` route only when approved aliases/redirects exist, preserving existing search behavior otherwise.
- Hardened Resource Layer reviewer workflow with local/dev mutation gate, structured reviewer form, request-body validation, transaction manifests/lock, stale lock cleanup, dry-run preview form, and clearer metrics.
- No broad duplicate cleanup, no production concrete merge, no source/resource backfill, no fake resources, and no local-file auto-linking were performed.

## Kimi review log
1. Strategy review: Kimi warned about homonym blindness, taxonomic flattening, alias pollution, lack of partial-overlap/deprecation/reopen states, dry-run fidelity, and search split-brain.
   - Accepted: no auto-merge, high-risk concrete groups remain `NEEDS_HUMAN_REVIEW`; alias is non-destructive; canonical search is applied only from approved alias/redirect records.
   - Deferred: partial-overlap/external-equivalence/versioned equivalence states and richer priority queue.
2. Merge/alias dry-run review: Kimi warned about rollback, lossy normalization, undefined property merge, edge provenance loss, redirect chains, alias/redirect cycles, and target-node validity.
   - Accepted: alias decisions do not tombstone source nodes; merge redirects are blocked for non-low-risk groups; validation now checks aliases pointing to redirected canonical nodes and canonical targets that already redirect.
   - Deferred: rollback/unmerge, node property unioning, predicate domain/range validation, and signed manifests.
3. Resource hardening review: Kimi warned about localhost/proxy risk, stale lockfiles, self-asserted reviewer identity, CSRF/rate limiting, manifest tampering, and weak visual diffs.
   - Accepted: local/dev gate is explicit, mutation routes also gate server-side, and stale lock cleanup was added to Resource Layer and canonical transaction helpers.
   - Deferred: production auth, CSRF/rate limiting, signed manifests, and richer metric-delta diff UI.

## Current status
- Canonical validation passes with 544 unresolved duplicate groups and 0 blockers.
- Resource Layer validation passes with the pre-existing 2 warnings for standards missing edition/version context.
- API and Explorer tests pass; Explorer build passes.

## Kimi final review addendum
Final Kimi verdict: safe and conservative. Kimi identified residual risk as operational stagnation rather than accidental corruption, because 544 groups remain unresolved. Accepted next-loop recommendation: use the new workflow to triage the two concrete duplicate groups and then define objective auto-merge criteria behind review gates. Deferred: batch review UI, rollback query surfaces, queue-age metrics.
