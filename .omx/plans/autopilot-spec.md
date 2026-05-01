# Autopilot Spec: AEC-MEPFS Backbone Readiness Closure

## Objective

Make the AEC-MEPFS Backbone ready for a later bounded runtime implementation
packet by closing all automatable readiness gates. Do not start runtime
integration.

## Immediate Slice

`AEC-BB-S4`: implement a file-backed, report-producing API/Explorer parity
runner.

## Requirements

- Read the S3 readiness fixture and validate it before runner execution.
- Execute the declared parity commands and capture exit code, duration, and
  bounded output snippets.
- Produce a deterministic JSON report at the plan's `report_path`, replacing
  `RUN_ID` with a concrete safe run id.
- Fail if the S3 plan is missing, malformed, not v1/v2 complete, or does not
  block runtime without a report.
- Keep the runner runtime-disconnected: no API route edits, Explorer route
  edits, Neo4j writes, graph rebuild, feature flags, or canonical source
  admission.
- Add focused tests using injected command runners so unit tests do not execute
  the full API/Explorer suites.
- Update readiness docs and validation logs with honest status.

## Out Of Scope

- Full AEC-MEPFS runtime implementation.
- Legal/licensing approval.
- Executed Neo4j backup/restore proof.
- Production registry promotion.
- Canonical source admission.

## Completion Criteria

- Focused runner tests pass.
- Existing S3 validator tests pass.
- API and Explorer tests pass.
- Runner creates an actual parity report from the current fixture.
- GitNexus impact/scope evidence is captured.
- Architect/security/quality validation is approved.
- Commit is pushed; OMX state is cleared.
