---
task: aec-mepfs-backbone
phase: runtime-governance-admission
created: 2026-04-27
author: CODEX
status: BOUNDARY_APPROVED
---

# Runtime Governance Admission Packet

## Purpose

This packet defines the decision boundary required after the AEC-MEPFS Backbone
shadow/read-only lane closed. It is an admission and governance packet, not a
runtime implementation packet.

It answers what may be considered next for resolver runtime, Neo4j/live graph,
protected source admission, Explorer default adoption, feature flags, runtime
thresholds, and verification. It does not authorize any live runtime change by
itself.

## Non-Goals

This packet does not:

- mount `/v2/resolve` or `/v2/resolve/trace`
- write, reset, reload, back up, restore, or mutate Neo4j
- rebuild or reload the KG
- ingest protected source text, tables, figures, or datasets
- cut over feature flags or default-on behavior
- make Explorer adopt the AEC-MEPFS graph as the default graph
- evaluate runtime latency thresholds
- edit runtime code

## Baseline State

The safe shadow-only/read-only scope is complete. Current evidence is anchored
by:

- `forty-first-shadow-safe-scope-closure-packet.md`
- `readiness-closure-scorecard.md`
- `readiness-spec-acceptance-record.md`
- `runtime-root-implementation-packet.md`
- `verification-and-benchmark-contract.md`
- `006_System-Manifests/aec-mepfs-backbone/evidence-manifest/20260426T132003Z/shadow-evidence-manifest-report.json`

The project owner accepted the row-level decisions on 2026-04-27 for the
first bounded resolver-runtime contract/static-verification packet only. The
active state remains live-runtime-blocked: this boundary approval does not
authorize mounted resolver routes, Neo4j mutation, KG rebuild/reload, protected
ingest, Explorer default adoption, default-on feature flags, or runtime
threshold claims.

## Status Semantics

Packet-level statuses:

| Status | Meaning |
|---|---|
| `DRAFT` | Packet incomplete. |
| `REVIEW_READY_RUNTIME_BLOCKED` | Evidence and decisions are mapped, but live runtime remains blocked. |
| `BOUNDARY_APPROVED` | A specific bounded runtime boundary is approved, but only for the named surface and commands. |
| `LIVE_RUNTIME_AUTHORIZED` | Every listed gate is explicitly approved with commands, evidence, rollback, and verification. Not current. |
| `REJECTED` | Runtime movement is disallowed under current evidence. |

Row-level decisions:

| Decision | Meaning |
|---|---|
| `approve_bounded` | Approved only within the row's exact boundary. |
| `defer` | Postponed until named evidence or authority exists. |
| `reject` | Not allowed under current evidence. |
| `blocked` | Cannot proceed without a new packet or explicit scope change. |



## Owner Acceptance / Boundary Approval

Project-owner acceptance was provided in the current 2026-04-27 task directive:

> I accept the runtime-governance-admission packet row-level decisions. I approve
> only BOUNDARY_APPROVED status for the first bounded resolver-runtime contract
> packet. This is not LIVE_RUNTIME_AUTHORIZED.

Boundary approval is limited to creating and later implementing the first
bounded resolver-runtime contract/static-verification packet:

```text
.ai/03_plans/AEC-MEPFS-Backbone/2026-04-27_bounded_resolver_runtime_contract_packet.md
```

This status change means:

- row-level decisions in the matrix are accepted as the current governance
  boundary
- the first follow-up packet may define resolver-runtime contracts, static
  fixtures, no-op/read-only preparation seams, and verification requirements
- implementation remains blocked until that follow-up packet is used as the
  explicit execution authority
- this is **not** `LIVE_RUNTIME_AUTHORIZED`

This packet still does not authorize:

- `/v2/resolve*` mounting
- Neo4j writes, reset, reload, backup, restore, cleanup, live namespace
  promotion, or primary graph replacement
- KG rebuild or reload
- protected source text, table, figure, dataset, or local protected-cache ingest
- Explorer default graph adoption
- default-on feature flags or hidden runtime cutover
- runtime threshold claims from shadow-only benchmark evidence

## Admission Decision Matrix

| Gate | Current decision | Allowed now | Still blocked | Evidence required before promotion |
|---|---|---|---|---|
| Resolver runtime | `defer` | Write a separate resolver-runtime execution packet and static contract tests. | Mounting `/v2/resolve*`, calling a hot runtime resolver from API, or changing current preview behavior. | Exact resolver contract, golden fixtures, API parity cases, fallback semantics, latency harness, rollback plan, and tests proving preview routes stay stable. |
| Neo4j / live graph | `blocked` | Read existing shadow evidence and plan a stopped or isolated rehearsal. | Any Neo4j write, reset, backup, restore, cleanup, live namespace promotion, or primary graph replacement. | Stopped/isolated dump-load proof, shadow namespace plan, rollback command transcript, graph-count diff, and failure recovery plan. |
| Protected source admission | `approve_bounded` for metadata/reference rows only | Maintain source-rights metadata and currentness evidence. | Protected content ingest, local protected-content cache, or canonical source admission beyond approved metadata/reference boundary. | Steward/legal owner approval, source-rights row with intended use, currentness evidence, and zero-content-ingest proof. |
| Explorer default adoption | `blocked` | Keep AEC-MEPFS preview opt-in and non-default. | Replacing primary Explorer graph state, automatic preview fetch, default perspective adoption, or default graph switch. | UX acceptance criteria, parity tests, opt-in-to-default migration plan, escape/rollback UI, and current MVP graph regression tests. |
| Feature flags | `defer` | Plan flag names and defaults only. | Default-on flags, hidden automatic cutover, or environment defaults that change runtime behavior. | Flag registry, default-off proof, tests for disabled/enabled behavior, and rollback procedure. |
| Runtime thresholds | `defer` | Preserve threshold targets as requirements. | Claiming measured runtime latency from file-backed benchmark evidence. | Fixed corpus, hardware/runtime baseline, warmup/repetition policy, percentile reporting, pass/fail thresholds, and reproducible reports. |
| Verification | `approve_bounded` for gatekeeping | Require targeted tests and evidence before every later packet. | Fresh green claims without fresh commands and logs. | Validation log with exact commands, outputs, affected files, safety invariants, and GitNexus/code-impact status. |

## First Eligible Follow-Up Packet

Because this packet is boundary-approved, the first follow-up remains conservative:

1. Use `2026-04-27_bounded_resolver_runtime_contract_packet.md` as the bounded resolver-runtime contract packet.
2. Keep `/v2/resolve*` unmounted; the bounded packet names tests for route absence and no-op rollback proof only.
3. Add no Neo4j writes and no protected ingest.
4. Prove current `/v2/backbone*` preview routes and Explorer opt-in previews remain unchanged.

Neo4j/live graph, Explorer default adoption, and default-on feature flags remain
later gates, not the first runtime step.

## Authority Map

| Area | AI role | Required authority |
|---|---|---|
| Runtime/API packet preparation | Draft and verify packet. | Project owner acceptance before implementation. |
| Neo4j/live graph mutation | Prepare evidence and rollback plan only. | Project owner acceptance plus rollback proof. |
| Protected source admission | Prepare rights/currentness rows only. | Steward/legal owner acceptance. |
| Explorer default adoption | Prepare UX/test packet only. | Project owner acceptance after preview regression evidence. |
| Feature flags | Draft flag registry only. | Project owner acceptance before any default change. |
| Runtime thresholds | Draft benchmark plan only. | Project owner acceptance after reproducible measurement evidence. |

## Safety Invariants

Every follow-up packet must explicitly prove:

- no Neo4j writes unless the packet is specifically a Neo4j-authorized packet
- no KG rebuild/reset/load unless explicitly authorized
- no protected content ingest without source-rights approval
- no `/v2/resolve*` mounting before resolver-runtime authorization
- no Explorer default graph adoption before UX/default-cutover authorization
- no default-on feature flags before flag authorization
- no runtime threshold claims from shadow-only benchmark evidence
- no AI self-authorization of steward/legal decisions

## Acceptance Checklist

This packet can be marked `BOUNDARY_APPROVED` only when all are true:

- [x] Project owner explicitly accepts the row-level decisions.
- [x] The first follow-up implementation packet is named.
- [x] Exact commands, tests, and artifacts are listed for that follow-up.
- [x] Rollback or no-op safety proof is listed for that follow-up.
- [x] State docs are updated without implying broad runtime authorization.

Even with this checklist closed, the approval is boundary-only and not `LIVE_RUNTIME_AUTHORIZED`.
