---
task: aec-mepfs-backbone
phase: readiness-spec-acceptance
created: 2026-04-25
author: CODEX
status: SHADOW-EVIDENCE-HASH-CONSISTENT
---

# Readiness Spec Acceptance Record

## Purpose

Record which AEC-MEPFS Backbone specs are accepted as readiness-control specs,
which bounded first-slice work is accepted, and which gates still block primary
runtime integration.

Accepted-readiness-control means the document can govern bounded implementation
packets. The S8 owner directive accepted the first additive shadow-only
implementation packet, which is now complete. It does not mean canonical
taxonomy content, protected source ingest, live database mutation, default-on
feature flags, or primary runtime cutover are approved.

## Acceptance Matrix

| Spec | Acceptance status | Runtime implication | Open blockers |
|---|---|---|---|
| `relationship-predicate-registry-draft.md` | accepted as readiness predicate spec | runtime may not invent unregistered governed predicates | S6 candidate rows validate and are approved only for first-slice shadow staging; primary registry admission and migration runner remain open |
| `master-taxonomy-l1-l2-decision-record.md` | accepted as first-slice L1/L2 planning candidate | runtime may use this as guardrail, not canonical node admission | independent review, domain review, LD-10 reconciliation, admitted source files |
| `standards-legal-source-pack.md` | accepted as source-family and rights-control baseline | runtime may cite/source-map only inside declared allowed-use class | no-ingest posture accepted; content ingest, local caching, and legal/licensing escalation remain blocked |
| `governance-editorial-control-pack.md` | accepted as governance-control baseline | Philip Lewis is named accountable steward; AI remains non-authority | independent second reviewer, legal/licensing reviewer, discipline reviewers |
| `vitruvian-context-resolver-pack.md` | accepted as resolver planning contract | future resolver must be deterministic and no-LLM in hot path | fixture-level result-type coverage and file-backed resolver QA runner exist; non-PH disposition, benchmark harness, exact API assertions, and runtime resolver remain open |
| `shadow-graph-database-safety-protocol.md` | accepted as database safety protocol | first code slice must be shadow-only and non-destructive | S8 isolated dump/load proof exists for a throwaway database; live production restore proof and 48h monitoring design remain open before promotion |
| `api-explorer-parity-contract.md` | accepted as API/Explorer consumer contract | v1 behavior is preserved; `/v2` is additive and shadow-only | S4 report-producing runner exists; future `/v2` runtime route parity remains open until shadow routes exist |
| `verification-and-benchmark-contract.md` | accepted as verification skeleton | implementation packet must fill exact commands and report paths | S3 benchmark plan exists; file-backed benchmark runner/report execution is closed for shadow evidence only; runtime resolver/API/Explorer/Neo4j benchmark thresholds remain open |

## Promotion Decision

The prior drafts are promoted to `ACCEPTED-READINESS-CONTROL`.

The first additive shadow-only implementation packet is complete as
`FIRST-SHADOW-IMPLEMENTATION-COMPLETE`.

They are not promoted to broad `ACCEPTED-FOR-RUNTIME-INTEGRATION`.

Reason:

- fresh GitNexus evidence shows HIGH and CRITICAL impact roots in the KG core
- source/legal ownership is accepted only for no-ingest, metadata/reference use;
  independent legal/licensing review is still required before content ingest,
  local caching, or protected source reuse
- API/Explorer and resolver fixtures are locally executable as shadow evidence,
  not runtime route or resolver adoption
- backup/restore and rollback preflight has run; S8 adds isolated dump/load
  proof for a throwaway database, while live production stopped-restore proof
  remains open before primary graph promotion or replacement
- S6 candidate registry files are accepted only for first-slice shadow staging;
  no canonical backbone source content has been admitted

## Bounded Readiness Implementation Status

`AEC-BB-S1` through `AEC-BB-S8` are implemented and validated/prepared as
file-backed readiness controls. They improve readiness evidence but do not
promote any spec to `ACCEPTED-FOR-IMPLEMENTATION`.

`AEC-BB-S2` added executable fixture validation for:

- predicate registry rows
- source-rights registry rows
- authoring/migration QA cases
- resolver golden cases
- API / Explorer parity cases
- shadow rollback plan metadata

The rows in `valid_readiness_s2.json` are contract fixtures only. They are not
canonical taxonomy data, production source-rights registry rows, legal clearance
records, database migration inputs, or runtime API/Explorer fixtures.

`AEC-BB-S3` added executable fixture validation for:

- planned registry/report locations
- API/Explorer parity-runner plan
- rollback-proof plan
- benchmark plan
- integration readiness gates

The rows in `valid_integration_readiness_s3.json` are readiness fixtures only.
They are not steward-admitted production registries, runtime report artifacts,
legal clearances, backup/restore proof, or canonical source admissions.

`AEC-BB-S4` added:

- report-producing parity runner
- API/Explorer parity cases fixture with required category coverage
- focused runner tests
- passing parity report artifact with 14 case results

The S4 report is current-readiness evidence. It is not proof that future `/v2`
runtime routes are correct because those routes have not been implemented yet.

`AEC-BB-S5` added:

- rollback preflight reporter
- focused preflight tests
- read-only live graph smoke counts
- Neo4j admin-surface report

The S5 report is current-readiness evidence. It is not backup/export or restore
proof because it intentionally does not stop Neo4j or run dump/load commands.

`AEC-BB-S6` added:

- predicate registry candidate with 12 governed predicate rows
- source-rights registry candidate with 29 first-wave source-family rows
- source-admission checklist
- registry candidate validation report

The S6 candidate rows are current-readiness evidence. They are not
steward-admitted runtime registries, legal clearance records, or canonical
source admissions.

`AEC-BB-S7` added:

- source currentness evidence for the 29 S6 source-rights rows
- legal/steward admission record
- canonical source admission packet with zero admitted canonical sources
- Neo4j rollback rehearsal evidence and safe-rehearsal disposition
- separate runtime-root implementation packet for HIGH/CRITICAL KG roots
- generated source-currentness and GitNexus impact reports

The S7 documents prepare the remaining decision gates. They do not grant
human/steward approval, legal/licensing clearance, canonical source admission,
or stopped/isolated rollback proof.

`AEC-BB-S8` added:

- a single human inbox decision packet at `.ai/14_human_inbox/ANSWER_HERE.md`
- manual currentness resolution for the five S7 exception rows
- isolated offline Neo4j import/dump/load proof for a throwaway database
- live graph non-mutation smoke evidence
- implementation-review-ready status language

S8 makes the packet ready for implementation review. It does not grant protected
content-ingest clearance, live graph mutation authorization, or broad runtime
rewrite approval.

The seventeenth shadow slice adds a file-backed resolver QA runner over the S2
golden cases. It produces
`006_System-Manifests/aec-mepfs-backbone/resolver-qa/20260426T060300Z/resolver-qa-report.json`
with 4/4 pilot cases passing and explicitly checks that `/v2/resolve` routes
remain unmounted. This is fixture QA only; it does not execute or authorize a
runtime resolver.

The eighteenth shadow slice hardens the existing API shadow report and artifact
readers. It requires expected shadow filenames, emits deterministic invalid-JSON
diagnostics, and regenerates parity evidence at
`006_System-Manifests/aec-mepfs-backbone/parity/20260426T062032Z/api-explorer-parity-report.json`.
This improves shadow preview reliability only; it does not add routes or
authorize runtime promotion.

The nineteenth shadow slice adds a file-backed boundary audit runner. It
produces
`006_System-Manifests/aec-mepfs-backbone/boundary-audit/20260426T075100Z/shadow-boundary-audit-report.json`
with 10/10 checks passing across the current shadow consumer report, sibling
graph artifact, placement QA report, resolver QA report, parity report, feature
flags, and API route surface. This is consolidated readiness evidence only; it
does not authorize runtime promotion, feature-flag cutover, protected content
ingest, Neo4j writes, or Explorer default adoption.

The twentieth shadow slice adds a file-backed benchmark runner. It produces
`006_System-Manifests/aec-mepfs-backbone/benchmarks/20260426T080510Z/benchmark-report.json`
with five local evidence operations passing and p50/p95 timings recorded. The
report includes SHA-256 hashes for all input evidence and repo-state metadata.
Runtime thresholds are explicitly not evaluated, so this is shadow evidence
only and does not authorize resolver/API/Explorer runtime adoption, Neo4j FTS
benchmarking, protected content ingest, feature-flag cutover, or graph
promotion.

The twenty-first shadow slice adds a shared static API route inventory. It
produces
`006_System-Manifests/aec-mepfs-backbone/api-route-inventory/20260426T082614Z/api-route-inventory-report.json`
with 21 direct Hono route declarations inventoried, all six required `/v2`
preview routes present, and `/v2/resolve` plus `/v2/resolve/trace` unmounted.
Resolver QA, boundary audit, and benchmark runners now use the same route-status
helpers. This does not add or authorize any runtime route, API server call,
Explorer adoption, feature-flag cutover, protected content ingest, Neo4j write,
or graph promotion.

The twenty-second shadow slice adds a consolidated evidence manifest. It
produces
`006_System-Manifests/aec-mepfs-backbone/evidence-manifest/20260426T084131Z/shadow-evidence-manifest-report.json`
with 9/9 artifact results ok, SHA-256 hashes for the current shadow evidence
inputs, cross-report path checks, graph counts, route inventory counts,
benchmark status, and safety invariants. The refreshed benchmark report at
`006_System-Manifests/aec-mepfs-backbone/benchmarks/20260426T084118Z/benchmark-report.json`
now references the route-inventory-backed boundary audit. This is file-backed
readiness evidence only and does not authorize runtime route adoption,
Explorer adoption, feature-flag cutover, protected content ingest, Neo4j write,
KG rebuild, or graph promotion.

The twenty-third shadow slice adds `GET /v2/backbone/evidence` as a compact
API-only preview over the consolidated evidence manifest. It produces refreshed
parity, route-inventory, boundary-audit, benchmark, and manifest evidence under
the `20260426T090300Z` through `20260426T090420Z` run packet, with 25/25 parity
cases, 7/7 preview routes, 10/10 boundary checks, 5/5 file-backed benchmark
operations, and 9/9 evidence artifacts ok. This is sanitized evidence preview
only and does not authorize Explorer default adoption, `/v2/resolve` mounting,
Neo4j writes or queries, KG rebuild, protected content ingest, feature-flag
cutover, or graph promotion.

The twenty-fourth shadow slice hardens the same evidence packet against stale
API inputs. The evidence manifest now records `api/index.ts` as an input and
requires the route-inventory, boundary-audit, and benchmark reports to carry the
current API SHA-256 hash before the consolidated packet is accepted. The
refreshed packet spans `20260426T093920Z` through `20260426T093924Z` and keeps
the API evidence route fenced to the latest file-backed evidence-manifest run.
This is evidence consistency only and does not authorize Explorer default
adoption, `/v2/resolve` mounting, Neo4j writes or queries, KG rebuild,
protected content ingest, feature-flag cutover, or graph promotion.

`AEC-BB-S8` decisions were answered on 2026-04-25T15:39:12Z by project-owner
directive captured in `.ai/14_human_inbox/ANSWER_HERE.md` and the machine
response JSON. The accepted use is bounded to:

- readiness registry staging
- conservative no-ingest legal posture
- reference/metadata currentness use only
- isolated rollback proof for a first shadow-only slice
- zero-content metadata-only canonical source staging
- first implementation packet review under additive shadow-only constraints

## First Shadow-Only Packet Completion

`first-shadow-only-implementation-packet.md` is implemented as the first code
packet.

It implements only file-backed shadow staging for AEC-MEPFS Backbone registry
and source metadata. It does not authorize live graph writes, source content
ingest, Explorer/API cutover, primary graph promotion, or edits to
`CanonicalNode`, `TaxonomyLoader`, or `Neo4jLoader`.

## First Implementation Packet Constraint

The first implementation packet must be bounded enough to respect this record:

- no edit to `CanonicalNode`
- no Neo4j write-path mutation
- no feature-flag enablement
- no graph rebuild
- no destructive cleanup/reset
- no canonical content admission
- no protected source ingest

Any packet that violates these constraints must create a new audit, impact map,
implementation plan, critique, and validation contract before code work.
