---
task: aec-mepfs-backbone
phase: readiness-resolver
created: 2026-04-25
author: CODEX
status: ACCEPTED-READINESS-CONTROL
---

# Vitruvian Context Resolver Pack

## Purpose

This pack specifies the deterministic resolver that will later answer which
taxonomy node, rule, standard mapping, or overlay applies in a given context.

No resolver implementation is authorized by this document.

The resolver is read-only. It never creates, mutates, or deletes canonical
nodes, overlays, mappings, or rules. It only selects, composes, or rejects over
pre-admitted data.

Accepted-readiness scope: the resolver inputs, outputs, precedence sequence,
conflict behavior, and no-LLM hot-path rule are accepted as planning controls.
Runtime implementation remains blocked until golden fixtures, non-Philippines
starter-jurisdiction disposition, API contracts, and benchmark harnesses exist.

## Non-Negotiable Rule

No LLM call is allowed in the hot-path resolver. LLMs may propose test cases,
summaries, or review findings outside the runtime path.

## Resolver Inputs

Required:

- query concept or node ID
- requested output type
- jurisdiction scope
- project or site scope, if any
- effective date
- lifecycle phase
- asset type or system context

Optional:

- discipline/domain filter
- performance topic
- external standard family
- source family
- evidence depth
- pagination cursor
- debug trace flag

Canonical wire field for temporal filtering is `effective_date`. If existing
code or tests still use `date` or `query_date`, a later implementation must
provide an adapter and deprecation warning rather than adding a third behavior.

Query selector policy:

- exactly one of `concept_id`, `path_code`, or `search_text` should be supplied
  by API clients
- if legacy internal calls provide more than one, priority is
  `concept_id > path_code > search_text` and the response must include a
  warning

## Resolver Outputs

The resolver returns exactly one of:

- `single_value`
- `composed`
- `conflict`
- `none`

Every response includes:

- canonical concept block, when applicable
- resolved value or values
- applicable source IDs
- jurisdiction and effective-date scope
- precedence trace
- evidence references
- confidence class: `deterministic`, `review_required`, or `insufficient`
- conflict set, if applicable
- deprecation or supersession notes

`resolved_at` may exist as metadata but is not part of semantic equality or
snapshot determinism checks.

## Precedence Sequence

1. Validate request shape.
2. Filter inactive, deprecated, out-of-date, and out-of-scope candidates.
3. Apply jurisdiction scope from broadest to most specific.
4. Rank legal force: constitutional/statutory, regulation/IRR, adopted code,
   local ordinance, project contractual, guidance, hazard context.
5. Apply operator semantics: minimum, maximum, exact, range, permitted,
   prohibited, conditional, reference-only.
6. Apply specificity: system, occupancy, use, asset type, location, hazard,
   project condition.
7. Apply temporal order only among comparable force and scope.
8. Compose compatible requirements.
9. Return conflict set for equal-force incompatible requirements.
10. Return trace.

The resolver must not hide conflicts by choosing the newest or most specific
candidate when equal-force legal conflict remains.

## Conflict Set

A `conflict_set` contains:

- candidate IDs
- source IDs
- force class
- scope
- effective dates
- conflicting operator/value
- why automatic composition failed
- required human/steward resolution path

## API Contract Sketch

Future route family:

- `POST /v2/resolve`
- `GET /v2/resolve/trace/:trace_id`
- `GET /v2/sources/:source_id`

Request fields:

- `query`
- `jurisdiction`
- `effective_date`
- `asset_context`
- `lifecycle_phase`
- `filters`
- `include_trace`
- `page`

Response fields:

- `status`
- `result_type`
- `results`
- `trace`
- `conflict_set`
- `errors`
- `warnings`
- `cache_key`
- `schema_version`

Stable error codes:

- `CONCEPT_NOT_FOUND`
- `INVALID_JURISDICTION`
- `INVALID_DATE`
- `NO_OVERLAY_FOUND`
- `EDITION_CONFLICT`
- `SUPERSEDED_EDITION`
- `INCOMPLETE_FACETS`
- `TIMEOUT`

Pagination is allowed for evidence, standards mappings, influences, and
`conflict_set`. The core identity block is never paginated.

## Cache And Deprecation Policy

- Cache key includes query, jurisdiction, effective date, asset context,
  lifecycle phase, filters, and resolver schema version.
- Resolver caches are invalidated by taxonomy, mapping, overlay, or resolver
  release changes.
- Deprecated nodes remain resolvable through redirects until a later accepted
  deprecation policy removes them.

## Golden Case Targets

Minimum first suite:

- accessibility requirement under BP 344 in a public building context
- fire-code requirement under RA 9514 with occupancy context
- zoning constraint under an exemplar LGU ordinance
- hazard context from HazardHunterPH that informs but does not override law
- project contractual requirement stricter than baseline law
- equal-force local/legal conflict returning `conflict`
- no applicable rule returning `none`
- composed requirements from compatible national and local overlays
- PH baseline overlay
- city/local override
- future-date warning
- invalid jurisdiction
- confidence-threshold filtering
- superseded-edition conflict

At least one non-Philippines starter jurisdiction must be added later or
explicitly deferred with rationale before implementation readiness can score
`3`.

Non-Philippines starter jurisdiction is explicitly deferred for this readiness
artifact. Rationale: the Philippines overlay is the only country pack currently
backed by local corpus context and source-family review in this packet. Adding a
second jurisdiction before the source-rights registry and steward roster exist
would create false parity. The later resolver execution packet must either name
one non-PH starter jurisdiction with official sources and golden cases, or keep
resolver readiness below score `3`.

## Future Performance Targets

These are verification thresholds for later implementation:

- exact ID lookup p95 <= 100 ms
- context resolve p95 <= 250 ms
- search p95 <= 300 ms
- overlay fan-out <= 50 candidate overlays after validity/scope filtering
- 100% trace availability for resolver decisions

Stretch targets from earlier resolver specs may be lower, but this pack keeps
the readiness-plan thresholds as the governing initial acceptance budget until
real graph-backed benchmarks exist.

## Pass / Fail Gate

Pass:

- resolver inputs/outputs are fixed before code starts
- precedence and conflict behavior are deterministic
- hot path has no LLM dependency
- golden cases cover single, composed, conflict, and none outcomes

Fail:

- resolver picks winners for equal-force conflicts
- runtime behavior depends on prompt output
- cache keys omit jurisdiction, date, or resolver schema version

## Current Drift To Resolve Before Implementation

- Existing specs and tests may use `date`, `query_date`, or `effective_date`.
  The implementation plan must converge on `effective_date`.
- Existing conflict handling may be boolean or ad hoc. Runtime readiness
  requires structured `conflict_set`.
- Current resolver examples are Philippines-heavy. A non-Philippines starter
  case must be added or explicitly deferred before score `3`.

## Historical Failure Constraints

- The resolver must not treat provenance-only relationships as semantic
  applicability.
- Lossy predicate mappings must fail validation or enter a review queue; they
  must not be silently converted into `RELATED_TO`.
- Explicit, inferred, and steward-curated edges must remain distinguishable in
  traces and quality reports.
- Unknown predicates fail closed until registered.
