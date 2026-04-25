---
task: aec-mepfs-backbone
phase: fourth-bounded-readiness-implementation-packet
created: 2026-04-25
author: CODEX
status: IMPLEMENTED-VALIDATED
---

# Fourth Bounded Readiness Implementation Packet

## Slice ID

`AEC-BB-S4`: report-producing API/Explorer parity runner.

## Goal

Turn the S3 parity-runner plan into executable local evidence before any
runtime implementation starts.

This slice closes the local "parity runner exists and produces a report" gate.
It does not close future `/v2` runtime parity for routes that do not exist yet,
and it does not authorize KG runtime wiring.

## Scope

Allowed write scope:

- `scripts/vitruvius/kg/backbone_parity_runner.py`
- `scripts/tests/test_kg_backbone_parity_runner.py`
- `scripts/tests/test_kg_backbone_contracts.py`
- `scripts/tests/fixtures/aec_mepfs_backbone/api-explorer-parity-cases.json`
- `scripts/tests/fixtures/aec_mepfs_backbone/valid_integration_readiness_s3.json`
- `006_System-Manifests/aec-mepfs-backbone/parity/*/api-explorer-parity-report.json`
- AEC-MEPFS readiness docs and validation logs

## Explicit Non-Scope

This slice did not authorize or perform:

- API route edits
- Explorer route/client edits
- KG schema, loader, or snapshot edits
- Neo4j writes, backup, restore, cleanup, reset, or graph reload
- feature-flag changes
- production registry promotion
- canonical source admission
- protected standards or legal source-text ingest

## Implementation

The new runner:

- reads the S3 readiness fixture
- validates it with `validate_backbone_contract_file`
- extracts `integration_parity_runner_plan`
- loads the declared API/Explorer parity cases fixture
- requires all accepted parity categories before command execution
- replaces `RUN_ID` in the report path with a safe run id
- constrains report output to
  `006_System-Manifests/aec-mepfs-backbone/parity/<run_id>/api-explorer-parity-report.json`
- maps declared commands through a fixed shell-free allowlist before execution
- writes a deterministic JSON report with command status, duration, errors,
  warnings, declared assertions, parity case results, surfaces, and output tails
- exits non-zero when the fixture is invalid or any command fails

## Evidence Report

Report written:

```text
006_System-Manifests/aec-mepfs-backbone/parity/20260425T113719Z/api-explorer-parity-report.json
```

Report result:

```text
ok: true
commands_run: 3
commands_passed: 3
cases_declared: 14
cases_passed: 14
```

Commands executed by the runner:

```bash
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_contracts.py -q
(cd api && bun test perspectiveContracts.test.ts)
(cd explorer && bun test src/utils/labels.test.ts src/components/componentInteraction.test.tsx src/components/graph/VisNetworkHost.test.ts)
```

## Validation

Focused validation:

```bash
PYTHONPATH=scripts python3 -m pytest \
  scripts/tests/test_kg_backbone_contracts.py \
  scripts/tests/test_kg_backbone_parity_runner.py \
  -q
```

Result:

```text
48 passed
```

Actual runner execution:

```bash
PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_parity_runner \
  --run-id 20260425T113719Z \
  --timeout-seconds 600
```

Result: report `ok: true`.

## Remaining Blockers

S4 improves implementation readiness but does not make the full AEC-MEPFS
Backbone runtime-ready. Remaining blockers:

- legal/licensing clearance
- executed Neo4j backup/restore proof in a safe environment
- steward-admitted production registries
- canonical source admission
- separate runtime implementation packet for HIGH/CRITICAL KG roots
- future `/v2` route parity after shadow routes exist

## Rollback

Rollback is clean:

- remove the parity runner module
- remove the parity runner tests
- remove the parity cases fixture
- remove the generated S4 parity report
- revert the AEC-MEPFS readiness docs

Because this slice does not touch runtime graph paths, database state, feature
flags, raw sources, canonical sources, or production registries, rollback does
not require Neo4j cleanup or graph rebuild.
