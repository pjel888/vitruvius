---
task: aec-mepfs-backbone
phase: s4-parity-runner-validation
created: 2026-04-25
author: CODEX
status: VALIDATED-WITH-BLOCKERS
---

# AEC-BB-S4 Parity Runner Validation

## Scope

Validated the S4 readiness-control slice:

- file-backed API/Explorer parity runner
- focused unit tests with injected command executors
- declared API/Explorer parity cases fixture
- actual runner execution against the S3 readiness fixture
- generated parity report under `006_System-Manifests/aec-mepfs-backbone/`

No API route, Explorer route, KG schema, Neo4j, feature flag, raw/canonical
source, production registry, backup/restore, cleanup, reset, or graph reload
was changed.

## Commands And Evidence

Focused tests:

```bash
PYTHONPATH=scripts python3 -m pytest \
  scripts/tests/test_kg_backbone_contracts.py \
  scripts/tests/test_kg_backbone_parity_runner.py \
  -q
```

Result:

```text
48 passed in 0.20s
```

Actual parity runner:

```bash
PYTHONPATH=scripts python3 -m vitruvius.kg.backbone_parity_runner \
  --run-id 20260425T113719Z \
  --timeout-seconds 600
```

Generated report:

```text
006_System-Manifests/aec-mepfs-backbone/parity/20260425T113719Z/api-explorer-parity-report.json
```

Report summary:

```text
ok: true
commands_run: 3
commands_passed: 3
cases_declared: 14
cases_passed: 14
errors: []
warnings: ["integration_rollback_proof_plan: rollback proof is planned, not executed"]
```

Runner-executed commands:

```text
PYTHONPATH=scripts python3 -m pytest scripts/tests/test_kg_backbone_contracts.py -q
  -> 35 passed
(cd api && bun test perspectiveContracts.test.ts)
  -> 15 pass, 0 fail
(cd explorer && bun test src/utils/labels.test.ts src/components/componentInteraction.test.tsx src/components/graph/VisNetworkHost.test.ts)
  -> 18 pass, 0 fail
```

Backup/restore feasibility check:

```bash
neo4j-admin database backup --help
neo4j-admin server backup --help
```

Observed: this installed `neo4j-admin` surface exposes `database dump/load` and
server start/stop/report commands, but no online backup command in the available
help surface. The existing `database dump` help still says it cannot dump a
mounted database. Rollback proof therefore remains a separate runtime packet
that must safely stop or isolate Neo4j before dump/restore evidence.

Read-only Neo4j no-mutation smoke:

```text
connectivity: true
nodes: 2429
BackboneShadow nodes: 0
CanonicalNode nodes: 313
```

## Validation Result

S4 is validated as a local readiness-control slice.

Security posture:

- default command execution is shell-free
- declared fixture commands are mapped through an allowlist
- unknown commands produce a failed report entry instead of shell execution
- timeout and executor exceptions produce failed command entries while still
  writing the audit report
- invalid cases-fixture JSON produces a failed report instead of aborting before
  artifact write
- report output is constrained to
  `006_System-Manifests/aec-mepfs-backbone/parity/<run_id>/api-explorer-parity-report.json`
  for the active run id

Parity posture:

- `scripts/tests/fixtures/aec_mepfs_backbone/api-explorer-parity-cases.json`
  declares 14 required parity categories from the accepted API/Explorer
  contract.
- The report maps every declared case to an allowlisted dedicated command and
  records 14 passing case results.
- Future `/v2` runtime route parity still requires a later shadow-route packet;
  S4 proves the file-backed case runner and current contract/unit surfaces.

The full AEC-MEPFS Backbone integration remains blocked by:

- legal/licensing clearance
- executed backup/export and restore proof
- steward-admitted production registries
- canonical source admission
- separate runtime impact packet for HIGH/CRITICAL KG roots
- future `/v2` runtime route parity after shadow routes exist
