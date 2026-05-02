# Vitruvius Resource Layer

Date: 2026-05-01

## Overview
The Resource Layer is a file-backed reference intelligence layer for selected knowledge graph nodes. It stores resources and node-resource links separately from graph nodes so the graph is not polluted by arbitrary URLs.

## Runtime paths
- Resource manifests: `006_System-Manifests/resource-layer/`
- API services: `api/resourceLayer/`
- Node detail integration: `GET /node/:id`
- Explicit resources route: `GET /node/:id/resources`
- Metrics: `GET /resources/metrics`
- Sidebar UI: `explorer/src/components/inspector/NodeInspector.tsx`

## Registry files
- `resources.json`: resource metadata, verification status, source rights, and admission provenance.
- `node-resource-links.json`: node-to-resource relationship, scores, rationale, references, and review status.
- `source-families.json`: authority-scoring families and jurisdiction/scope notes.
- `resource-checks.json`: URL/canonical/deduplication checks.
- `resource-candidates.json`: candidate/needs_review/rejected discovery records.
- `local-file-index.json`: output of the safe local corpus scanner; not automatically linked to graph nodes.

## Review behavior
Accepted and human-reviewed links are displayed by default. Candidate, needs_review, and rejected links are hidden unless an API caller uses `includeCandidates=true`.

## Validation
Run:

```bash
bun run api/validateResourceLayer.ts
```

Validation checks required metadata, identifier formats, duplicate DOI/ISBN/canonical URL/local hash groups, accepted external timestamps, accepted local hashes, node/resource references, score ranges, and regulatory/standards context warnings.

## Local corpus indexing
Run:

```bash
bun run api/indexLocalResources.ts --dir=.ai/13_research/vitruvius_resource_layer_markdown_pack --maxFiles=50
```

The scanner hashes real local files and writes metadata-only Resource records to `local-file-index.json`. It does not copy full document text and does not admit node links automatically.

## Online adapters
The first adapter is Open Library. It is candidate-only, needs no API key, and is test-covered with mocked responses. Future adapters should implement the same interface and fail gracefully when credentials or network access are unavailable.

## Seed status
Accepted seed links are intentionally small:
- U.S. Access Board ADA Chapter 4 to Accessible Route Continuity.
- WBDG Wind Safety to Load Path and Structural Wind Load as contextual guidance.
- WBDG Seismic Design Principles to Structural Seismic Load as contextual guidance.
- ICE Structural Load Paths to Load Path.

Held or rejected records:
- ASCE 7 landing page for wind/seismic remains `needs_review` pending edition/section/adoption context.
- FHWA retaining-wall page remains `needs_review` because scope is U.S. federal transportation/geotechnical.
- ACI 318 portal to Structural Column is `rejected` as too broad without section-specific support.

## Reviewer workflow (loop 2)
Loop 2 adds a local/dev reviewer workflow for inspecting pending resource intelligence before promotion. It remains file-backed and does not introduce auth, a database, Neo4j writes, graph rebuilds, broad backfill, paid APIs, or automatic local-file linking.

### Review routes
- `GET /resources/review/queue` returns grouped `needsReviewLinks`, `rejectedLinks`, `acceptedLinks`, `candidateLinks`, `candidates`, `localFiles`, `standardsMissingContext`, validation warnings/errors/blockers, decision history, and metrics.
- `GET /resources/review/candidates` returns candidate records with dedupe/suggested linkage context.
- `GET /resources/review/local-files` returns local-file-index records with admitted/not-admitted status and linked-node count.
- `GET /resources/review/standards` returns standard/code-like resources or links missing edition, section, publication-year, or jurisdiction/context signals.
- `GET /resources/review/report` returns review metrics for accepted, needs_review, rejected, candidates, local files, standards context, duplicates, broken link checks, source families, and authority tiers.
- `POST /resources/review/link/:linkId/decision` applies reviewer decisions for existing node-resource links.
- `POST /resources/review/candidate/:candidateId/decision` applies reviewer decisions for candidate records.
- `POST /resources/review/local-file/:fileId/decision` applies reviewer decisions for indexed local files.

### Review decisions and history
Review decisions require a reviewer and rationale. Successful write decisions append to `006_System-Manifests/resource-layer/review-decisions.json` and preserve prior history. Mutations are deterministic JSON writes under `006_System-Manifests/resource-layer/` and run Resource Layer validation before writing. The current production decision log is intentionally empty until a human reviewer takes an action.

### Promotion gates
- Accepted standard/code-like links are blocked unless edition/version plus page/chapter/section context exists, or an explicit reviewer standard-context justification is recorded.
- ASCE and ACI links cannot be accepted without section/adoption context.
- FHWA links require explicit U.S. transportation/geotechnical scope review before promotion.
- WBDG/NIBS remains contextual guidance and cannot become a primary/governing authority without explicit review.
- Candidate promotion requires source family, stable URL/local identifier, source-rights boundary, admission provenance, and reviewer rationale.
- Standard/code candidate promotion additionally requires edition/version and jurisdiction/geographic scope.
- Local indexed files are never auto-linked. Local admission requires explicit reviewer action and the indexed file path must still exist.

### Explorer admin UI
The Explorer now includes a clearly labeled local/dev admin route:

```text
/dev/resource-review
```

It shows metrics and tabs for Needs Review, Candidates, Local Files, Rejected, Standards Missing Context, and Accepted. Review actions confirm before POSTing to the API and refresh the queue afterward. This is not an authentication system; deployers must not expose mutation routes on a shared/public server without a separate auth/role gate.

### Validation and tests
Run:

```bash
bun run api/validateResourceLayer.ts
cd api && bun test
cd ../explorer && bun test
cd ../explorer && bun run build
```

Loop 2 extends validation output with `accepted_count`, `needs_review_count`, `rejected_count`, `candidate_count`, `local_files_indexed`, `local_files_admitted`, `standards_missing_context`, `warnings`, `blockers`, and `errors`.

### Backfill status
Broad backfill remains blocked until the reviewer workflow is exercised on small batches. The loop 1 status decisions remain unchanged: ASCE/FHWA are still `needs_review`, ACI-to-Structural-Column is still `rejected`, and WBDG remains contextual guidance.

## Reviewer hardening and canonical stewardship integration (loop 3)
Loop 3 keeps the Resource Layer file-backed but adds safer review operations:

- Mutation routes are now local/dev gated server-side. A mutation is allowed only in a non-production runtime, from localhost/loopback, or when `VITRUVIUS_ENABLE_DEV_ADMIN=true` is explicitly set. This is not production authentication.
- `/dev/resource-review` uses structured reviewer forms rather than browser prompt/confirm dialogs. Reviewer and rationale are required before mutation.
- Decision POST bodies are schema-checked for allowed decisions, reviewer/rationale types, reference arrays, score ranges, and object-shaped provenance/source-rights fields.
- Resource Layer registry writes use a lightweight `.resource-layer-review.lock`, stale-lock cleanup, validation-before-write, deterministic JSON output, and transaction manifests under `006_System-Manifests/resource-layer/transaction-manifests/`.
- Metrics now distinguish `resourcesTotal`, `resourcesNonRejected`, `resourcesWithAcceptedLinks`, and `acceptedNodeResourceLinks`; `acceptedResources` remains for backward compatibility.
- Canonical graph stewardship is separate from Resource Layer review. If a future canonical redirect is applied, Resource Layer node links are preserved and validation reports links that rely on redirects rather than silently deleting or rewriting them.

Canonical duplicate review lives at `/dev/canonical-review` and via `GET /graph/canonical/*` routes. It does not broad-merge duplicates and did not promote the known Concrete/Reinforced Concrete duplicate groups in this loop.

## Canonical operations hardening - 2026-05-01

Resource Layer review mutations now share the same operational safety posture as canonical stewardship mutations:

- local/dev or token-gated mutation access; read-only review routes remain inspectable,
- transaction manifests include before/after file hashes, previous manifest hash, manifest hash, and optional subsystem-scoped HMAC signature through `VITRUVIUS_TRANSACTION_HMAC_KEY`,
- Resource Layer links are treated as preservation targets in canonical dry-run previews and rollback reports,
- canonical batch review does not auto-promote Resource Layer links or local files.

Relevant commands:

```bash
bun run api/validateResourceLayer.ts
bun run api/validateCanonicalGraphStewardship.ts
```

Production deployments should still add real authentication, failed-attempt auditing, rate limiting, and CSRF protection before exposing mutation routes beyond local/dev or token-gated operator use.
