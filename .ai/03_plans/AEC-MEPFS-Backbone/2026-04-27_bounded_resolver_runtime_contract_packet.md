---
task: aec-mepfs-backbone
phase: bounded-resolver-runtime-contract
created: 2026-04-27
author: CODEX
status: IMPLEMENTED
---

# Bounded Resolver Runtime Contract Packet

## Implementation Record

Implemented by commit `618a659b` (`Implement bounded AEC resolver contract verification`).

Evidence:

- `.ai/05_logs/2026-04-27_aec_mepfs_bounded_resolver_contract_static_verification.md`
- `006_System-Manifests/aec-mepfs-backbone/api-route-inventory/20260427T020853Z/api-route-inventory-report.json`
- `006_System-Manifests/aec-mepfs-backbone/resolver-qa/20260427T020853Z/resolver-qa-report.json`

This implementation kept `/v2/resolve*` unmounted and completed the static/no-op contract gate. The next separate packet is `2026-04-27_default_off_resolver_runtime_packet.md`.


## Purpose

Define the first runtime-adjacent AEC-MEPFS Backbone slice after owner acceptance
of the runtime-governance row-level decisions.

This packet is deliberately bounded to resolver-runtime contract preparation,
static verification, golden fixture hardening, and no-op/read-only integration
preparation. It is not a live runtime implementation packet.

## Non-Goals

This packet does not authorize or require:

- mounting `/v2/resolve`, `/v2/resolve/trace`, or any `/v2/resolve*` route
- calling a hot resolver from the API server
- writing, resetting, reloading, backing up, restoring, or mutating Neo4j
- rebuilding or reloading the KG
- ingesting protected source text, tables, figures, datasets, or local protected
  caches
- changing Explorer default graph adoption or default perspective behavior
- adding default-on feature flags or hidden automatic cutover
- claiming measured runtime latency from file-backed shadow benchmark evidence
- editing HIGH/CRITICAL runtime roots such as `CanonicalNode`, `TaxonomyLoader`,
  or `Neo4jLoader`

## Allowed Scope

A later implementation using this packet may prepare only:

1. Resolver contract TypeScript/Python schemas or documentation that are not
   mounted as API routes.
2. Static route-surface checks proving `/v2/resolve*` remains absent.
3. Golden resolver fixtures that cover deterministic result classes without
   protected source payloads.
4. No-op/read-only seams that can be imported in tests without touching Neo4j,
   KG rebuild paths, or Explorer default state.
5. Tests that prove existing `/v2/backbone*`, `/v2/search`, and opt-in Explorer
   preview behavior remains unchanged.
6. Evidence-log and manifest requirements for the next packet.

## Explicitly Blocked Scope

The following remain blocked until a later packet explicitly changes them:

| Surface | Blocked action |
|---|---|
| Resolver API | Mount `/v2/resolve*` or call runtime resolver from Hono handlers. |
| Neo4j/live graph | Any write, reset, reload, backup, restore, cleanup, or namespace promotion. |
| KG pipeline | Any rebuild, reload, destructive reset, or primary graph replacement. |
| Protected sources | Ingest or locally cache protected text, tables, figures, datasets, or clauses. |
| Explorer | Default adoption, automatic preview fetch, graph-state replacement, or default perspective cutover. |
| Feature flags | Default-on runtime flags, hidden environment cutover, or disabled-path drift. |
| Benchmarks | Runtime latency pass/fail claims from shadow-only evidence. |
| Critical roots | Direct edits to `CanonicalNode`, `TaxonomyLoader`, or `Neo4jLoader`. |

## Contract Surfaces

The first implementation packet should define static contract surfaces before
runtime mounting exists:

- resolver request shape: query text, optional context IDs, optional jurisdiction
  or discipline filters, and deterministic trace request flag
- resolver result shape: result type, canonical backbone node references,
  confidence class, source-evidence references, fallback reason, and trace-safe
  rationale
- error shape: deterministic invalid input errors, missing fixture/artifact
  errors, blocked runtime-route errors, and no-result responses
- route-surface inventory: static evidence that `/v2/resolve` and
  `/v2/resolve/trace` are not mounted
- preview preservation contract: current `/v2/backbone*`, `/v2/search`, and
  Explorer opt-in preview routes continue to behave as file-backed previews

## Golden Fixtures

Use and extend existing non-protected fixtures only:

- `scripts/tests/fixtures/aec_mepfs_backbone/valid_readiness_s2.json`
- `scripts/tests/fixtures/aec_mepfs_backbone/valid_integration_readiness_s3.json`
- existing resolver QA cases reflected in
  `006_System-Manifests/aec-mepfs-backbone/resolver-qa/20260426T115200Z/resolver-qa-report.json`

Required fixture coverage for the next implementation packet:

- `single_value`: exact canonical node resolution from a governed alias/path
- `composed`: deterministic multi-node context response without protected text
- `conflict`: explicit conflict/fallback semantics when two candidates compete
- `none`: deterministic no-result response with safe rationale
- invalid input: empty or malformed request produces deterministic static error
- blocked route: route inventory confirms `/v2/resolve*` remains absent

## Static API Contract Tests

The next implementation may add focused static tests only. Suggested commands:

```bash
(cd api && bun test v2Backbone.test.ts)
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_resolver_qa.py
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_api_route_inventory.py
```

The test suite must prove:

- `/v2/resolve` is not mounted
- `/v2/resolve/trace` is not mounted
- required preview routes remain mounted
- invalid resolver fixture cases fail deterministically
- no API handler calls Neo4j or KG rebuild code for resolver contracts

## Fallback Semantics

Fallbacks must be deterministic and non-LLM on the hot path:

- missing exact match returns `none`, not a generated answer
- ambiguous match returns `conflict` with candidate IDs and safe rationale
- insufficient context returns a deterministic fallback reason
- unavailable artifacts fail closed with path-safe diagnostics
- no fallback may expose protected source payloads

## Preview Route Preservation Tests

The next implementation must retain current preview behavior:

- `GET /v2/backbone`
- `GET /v2/backbone/taxonomy`
- `GET /v2/backbone/node/:id`
- `GET /v2/backbone/placement-qa`
- `GET /v2/backbone/evidence`
- `GET /v2/search`
- `GET /v2/sources/:source_id`

Preview routes must remain file-backed and sanitized. Resolver contract work must
not change their response shape unless a later packet explicitly authorizes and
verifies the change.

## Explorer Opt-In Preservation Tests

Explorer must remain preview-only:

- AEC-MEPFS panel loads only by explicit user action
- placement QA and evidence subsections load only by explicit user action
- graph nodes/edges and selected perspective remain unchanged by preview fetches
- no default graph adoption or automatic preview fetch is introduced
- copyable preview text remains derived from sanitized metadata only

## Rollback / No-Op Proof

Because this packet does not authorize live runtime mutation, rollback proof is
no-op based:

- `git diff --name-only` must show only contract, fixture, test, docs, or
  evidence files in the later implementation
- route inventory must show `/v2/resolve*` absent before and after
- Neo4j write commands must not appear in changed code
- KG rebuild/reset/load commands must not appear in changed code
- feature flags must remain absent or default-off only if a later packet allows
  flag planning
- reverting the implementation commit must restore the prior shadow-preview
  surface without database action

## Verification Commands

Minimum commands for the later implementation packet:

```bash
git status --short --branch
git diff --check
rg -n "LIVE_RUNTIME_AUTHORIZED|/v2/resolve|MATCH \(n\) DETACH DELETE|Neo4j|run-kg-pipeline|--reset|protected content|protected ingest|Explorer default|default-on|runtime threshold" .ai api explorer scripts
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_resolver_qa.py
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_api_route_inventory.py
(cd api && bun test v2Backbone.test.ts)
```

Run broader API/Explorer/Python suites only if the implementation touches those
surfaces beyond static fixtures/tests.

## Evidence Artifacts

The later implementation must produce or update:

- validation log under `.ai/05_logs/`
- route inventory evidence under
  `006_System-Manifests/aec-mepfs-backbone/api-route-inventory/`
- resolver QA report under
  `006_System-Manifests/aec-mepfs-backbone/resolver-qa/` only if fixtures or QA
  runner behavior changes
- parity evidence under `006_System-Manifests/aec-mepfs-backbone/parity/` if API
  or Explorer preview contracts are touched
- GitNexus/code-impact evidence if runtime-root or API handler symbols are
  edited

## Safety Invariants

Every implementation under this packet must confirm:

- no `/v2/resolve*` route is mounted
- no Neo4j write/reset/reload/backup/restore/mutation is introduced
- no KG rebuild/reload/reset is introduced
- no protected source text/table/figure/dataset ingest is introduced
- no Explorer default graph adoption is introduced
- no default-on feature flag is introduced
- no runtime threshold claim is made from shadow-only evidence
- current file-backed preview routes remain opt-in and sanitized
- HIGH/CRITICAL runtime roots remain untouched unless a later packet explicitly
  authorizes them

## Completion Criteria

This packet is complete when:

- the governance packet records project-owner boundary approval
- this packet exists with status `BOUNDARY_APPROVED`
- evidence log records the owner decision, changed files, checks, and advisory
  review results
- roadmap/status docs point to this packet as the next safe implementation
  authority
- working tree is clean after commit
- no live runtime implementation has been performed

## Next Packet Boundary

The next packet may be an implementation packet for resolver contract/static
verification only. It must not promote this work to live runtime.

A later and separate packet is required before any of these can happen:

- `/v2/resolve*` route mounting
- hot resolver invocation from API/Explorer
- Neo4j shadow or live writes
- KG rebuild/reload
- protected content ingest
- Explorer default adoption
- default-on feature flags
- runtime threshold evaluation or claims
