# AEC-MEPFS Four Gated Lanes Reopen Packet

```yaml
status: BOUNDARY_APPROVED
created: 2026-04-27
authority: project-owner-directive-four-gated-lanes
scope: aec-mepfs-four-gated-lanes-only
baseline_commit: 64d341cf
prior_closure_anchor_commit: 8b05e559
prior_closure_evidence_run: 20260427T044757Z
live_runtime_authorization: false
global_live_authorization: false
```

## 1. Purpose

This packet reopens the AEC-MEPFS Backbone workstream for exactly four gated
lanes that were intentionally left blocked or unsatisfied in the final closure
packet:

1. Neo4j isolated rehearsal and scoped live graph promotion preparation.
2. Protected source admission.
3. Explorer default adoption.
4. Runtime threshold adoption.

The project-owner directive dated 2026-04-27 authorizes Codex to complete all
repo-actionable work for these four lanes without stopping at packet boundaries.
This packet does **not** authorize broad/global live runtime status, reckless
production graph mutation, protected source ingestion without valid authority,
silent Explorer default adoption, or runtime threshold pass/fail claims from
shadow-only evidence.

## 2. Safety baseline from prior closure

The prior closure packet remains the safety baseline. The following remain true
until a lane-specific packet satisfies its gate:

- No broad/global `LIVE_RUNTIME_AUTHORIZED` state is approved.
- No destructive production Neo4j reset is approved.
- No production primary graph replacement is approved.
- No KG rebuild/reload/reset affecting the primary graph is approved.
- No protected source text, table, figure, dataset, clause, or local protected
  cache ingestion is approved without valid source-rights/steward/legal records.
- No protected payload exposure in API, Explorer, fixtures, logs, reports, or
  evidence is approved.
- No hidden default-on feature flag is approved.
- No silent Explorer default graph adoption is approved.
- No runtime threshold pass/fail claim may be made from shadow-only evidence.

## 3. Reopened lane authority

### Lane 1 — Neo4j isolated rehearsal and live-promotion path

**Immediate GREEN work:** inspect Neo4j/KG scripts, document blast radius,
write a dedicated isolated-rehearsal packet, define backup/restore/rollback and
graph-count diff commands, add dry-run/no-op safety tests, prepare shadow
namespace/sandbox evidence directories, and prove primary/live graph is
untouched.

**SATISFIED_YELLOW only after packet proof:** an isolated rehearsal may run only
when the target is explicitly sandbox/stopped/shadow/isolated, rollback commands
exist before mutation, graph-count diff and failure recovery are documented, no
primary/live namespace is replaced, no protected content is ingested, and all
commands/results are logged.

**Still blocked:** destructive production reset, primary graph replacement, live
namespace promotion, or primary KG rebuild/reload/reset without a later live
promotion packet and rollback transcript.

### Lane 2 — Protected source admission

**Immediate GREEN work:** inspect rights/currentness/steward docs, update
metadata-only rows, produce currentness evidence rows, prove zero protected
content ingest/exposure, create sanitization tests and an admission checklist.

**SATISFIED_YELLOW only with valid repo authority:** protected ingestion may
happen only when repo records prove steward/legal/source-rights approval,
permitted use, permitted fields/payloads, currentness, storage, retention,
exposure, and rollback/removal policy.

**EXTERNAL if authority is absent:** do not ingest protected payloads; mark
protected ingest externally blocked and complete all metadata-only proof.

### Lane 3 — Explorer default adoption

**Immediate GREEN work:** inspect Explorer graph state/perspective/preview code,
write UX criteria, add or strengthen regression tests for current MVP behavior,
define opt-in-to-default migration, create rollback/escape path, and prove API
parity remains current.

**SATISFIED_YELLOW only after proof:** default adoption may be implemented only
with a dedicated packet, documented UX criteria, green MVP regression tests,
explicit default behavior, migration/rollback path, no protected payloads,
current API parity evidence, and tests proving old behavior can be restored or
disabled.

**Still blocked:** silent default switch, untested automatic preview fetch,
protected payload exposure, or default adoption while API parity is stale.

### Lane 4 — Runtime threshold adoption

**Immediate GREEN work:** inspect benchmark harnesses/evidence, define fixed
corpus, hardware/runtime baseline capture, warmup/repetition policy, percentile
reporting, predeclared thresholds, report schema, and tests that shadow-only
benchmark evidence cannot be reused as runtime threshold proof.

**SATISFIED_YELLOW only after runtime proof:** runtime threshold pass/fail
adoption may happen only when a reproducible runtime path exists, corpus is
fixed, hardware/runtime baseline is captured, repetitions/percentiles are
reported, thresholds are declared before final measurement, the benchmark runs
actual runtime path, and reports set `passFailClaim=true` only after all criteria
are met.

**UNSATISFIED_YELLOW if criteria are missing:** preserve thresholds as
requirements only; complete harness/schema/tests/evidence as repo-actionable.

## 4. Required work order

Use this order unless direct repo evidence proves a dependency requires
reordering:

1. Create this umbrella reopen packet and validation log.
2. Runtime threshold adoption packet and repo-actionable harness/schema/tests.
3. Explorer default-adoption packet and repo-actionable UX/regression/rollback
   proof.
4. Protected source admission packet and repo-actionable metadata/zero-ingest
   proof.
5. Neo4j isolated rehearsal packet and repo-actionable preflight/rehearsal proof.
6. Reconcile state docs and final four-lane closure packet.

## 5. Packet creation rule

Every lane packet must include:

- purpose and authority;
- baseline and prior evidence;
- allowed scope and blocked scope;
- implementation plan;
- verification plan;
- rollback/no-op proof;
- generated evidence artifacts;
- safety invariants;
- action classification as `GREEN`, `SATISFIED_YELLOW`,
  `UNSATISFIED_YELLOW`, `RED`, or `EXTERNAL`;
- completion criteria and next boundary.

If a lane item is GREEN or SATISFIED_YELLOW, implement it and verify it. If it is
UNSATISFIED_YELLOW, complete prerequisites first. If it is RED or EXTERNAL,
document the blocker and continue with other independent lane work.

## 6. Review and model rules

- Gemini is not part of this reopened workstream and must not be used.
- Kimi/Moonshot should be attempted for meaningful lane packets and diffs; its
  output is advisory only and must be verified through repo tests/checks.
- `gpt-5.3-codex-spark` may be used for bounded coding tasks where available;
  unavailable Spark is not blocking and final authority remains with this Codex
  session and repo evidence.

## 7. Evidence directories

Use existing conventions where possible and add lane-specific evidence under:

- `006_System-Manifests/aec-mepfs-backbone/runtime-thresholds/`
- `006_System-Manifests/aec-mepfs-backbone/explorer-default-adoption/`
- `006_System-Manifests/aec-mepfs-backbone/source-admission/`
- `006_System-Manifests/aec-mepfs-backbone/neo4j-rehearsal/`
- `006_System-Manifests/aec-mepfs-backbone/four-lane-closure/`

Validation logs belong under `.ai/05_logs/`.

## 8. Stop criteria

This reopened workstream may stop only after all four lane packets and all
repo-actionable GREEN/SATISFIED_YELLOW work are complete, RED and EXTERNAL work
is documented, Kimi/Spark statuses are recorded, relevant tests/checks pass or
unrelated failures are documented, evidence artifacts exist, final four-lane
closure packet exists, the working tree is clean, and the branch is pushed/synced
if repo convention requires.
