# AEC-MEPFS Backbone Plan Packet

## Purpose

This folder contains the planning packet for the proposed AEC-MEPFS Backbone
knowledge graph architecture shift.

`AEC-MEPFS` names the broader AEC scope while keeping mechanical, electrical,
plumbing, fire protection, and sanitary systems explicit as first-class domains.

The direction captured here is planning-only: build an authored,
standards-aligned AEC-MEPFS Backbone graph first, then classify documents, rules,
chunks, and evidence onto that backbone.

## Files

| File | Role |
|---|---|
| `2026-04-25_aec_mepfs_backbone_knowledge_graph_research.md` | Standards and repo-context research |
| `2026-04-25_aec_mepfs_research_integration_addendum.md` | Integration of the AECMEPFS++ research reports into readiness gates |
| `2026-04-25_aec_mepfs_backbone_architecture_audit.md` | Current-state audit and blast-radius assessment |
| `2026-04-25_aec_mepfs_backbone_readiness_plan.md` | Go/no-go readiness gates before implementation |
| `2026-04-25_aec_mepfs_backbone_architecture_overhaul_plan.md` | Proposed architecture overhaul plan |
| `2026-04-25_aec_mepfs_backbone_cleanup_and_blast_radius_plan.md` | Cleanup, database migration, and blast-radius plan |
| `2026-04-25_aec_mepfs_backbone_plan_validation.md` | Planning-artifact validation note |
| `standards-legal-source-pack.md` | Source families, rights classes, and official-source verification controls |
| `master-taxonomy-l1-l2-decision-record.md` | First-slice L1/L2 taxonomy decision and canonical rules |
| `governance-editorial-control-pack.md` | Stewardship, review, change-control, AI-use, and release controls |
| `vitruvian-context-resolver-pack.md` | Deterministic resolver contract and no-LLM hot-path rules |
| `taxonomy-authoring-migration-qa-pack.md` | Authoring, staging, review queues, confidence policy, and golden dataset design |
| `philippines-overlay-pilot-pack.md` | Philippines jurisdiction overlay pilot and source/fallback rules |
| `relationship-predicate-registry-draft.md` | Readiness-stage predicate vocabulary and vague-edge rejection gate |
| `readiness-artifact-history-and-blast-radius-audit.md` | Historical KG failure evidence and blast-radius implications for the readiness packet |
| `code-intelligence-impact-map.md` | Fresh GitNexus CLI impact map and HIGH/CRITICAL risk evidence |
| `sel-mcp-precheck.md` | Tool-availability, MCP transport, and CLI parity precheck |
| `shadow-graph-database-safety-protocol.md` | Shadow graph topology, backup/restore prerequisites, and destructive-operation block |
| `api-explorer-parity-contract.md` | V1 preservation, `/v2` shadow route, and Explorer parity contract |
| `verification-and-benchmark-contract.md` | Later verification commands, thresholds, and output report requirements |
| `readiness-spec-acceptance-record.md` | Promotion record for accepted readiness-control specs and remaining implementation blockers |
| `first-bounded-implementation-packet.md` | Separate non-executed packet for the first safe code slice |
| `second-bounded-readiness-implementation-packet.md` | Implemented fixture-level readiness validator extension for S2 |
| `third-bounded-readiness-implementation-packet.md` | Implemented S3 readiness-gate validator extension for registry locations, parity, rollback, benchmark, and runtime-blocking gates |
| `fourth-bounded-readiness-implementation-packet.md` | Implemented S4 report-producing API/Explorer parity runner |
| `fifth-bounded-readiness-implementation-packet.md` | Implemented S5 rollback preflight reporter |
| `sixth-bounded-readiness-implementation-packet.md` | Implemented S6 registry/source-admission candidate preparation |
| `registry-candidates/` | Candidate predicate, source-rights, and source-admission review artifacts; not runtime registries |
| `readiness-closure-scorecard.md` | Current go/no-go scorecard after S1/S2/S3/S4/S5/S6 |

## Current Status

Status: accepted readiness-control packet in iteration.

Current implementation status: not ready for runtime architecture work; bounded
readiness slices `AEC-BB-S1` through `AEC-BB-S6` are implemented and
validated.

No runtime implementation has started from this packet. It authorizes no code
edits, Neo4j cleanup/reset, feature-flag changes, graph rebuilds, backup test
runs, or derived-artifact cleanup.

Readiness-control artifacts for source rights, L1/L2, governance, resolver,
shadow graph safety, API/Explorer parity, predicate registry, and verification
are now accepted as readiness controls. Taxonomy authoring/migration QA and the
Philippines overlay pilot remain draft controls. These artifacts improve
readiness evidence but do not by themselves authorize implementation.

The current scorecard remains conservative because the packet still lacks
independent second review, legal/licensing clearance, rollback proof, executable
benchmark fixtures, accepted runtime registries, and canonical source admission.
Fresh GitNexus evidence also shows HIGH/CRITICAL KG impact roots that must be
avoided or separately planned.

`AEC-BB-S1` added a file-backed validator only. It does not wire Backbone data
into the KG, Neo4j, API, Explorer, feature flags, or graph rebuilds.

`AEC-BB-S2` extends that same runtime-disconnected validator to executable
readiness fixtures for predicate rows, source-rights rows, authoring/migration
QA cases, resolver golden cases, API/Explorer parity cases, and a planned shadow
rollback protocol. The S2 fixture rows are contract examples only, not admitted
canonical taxonomy/source data.

`AEC-BB-S3` extends the validator again for integration readiness controls:
planned registry locations, API/Explorer parity-runner plan, rollback-proof
plan, benchmark plan, and runtime-blocking gate status. The S3 fixture is still
planning/readiness evidence only. It is not a production registry, not a Neo4j
backup/restore proof, and not runtime API/Explorer parity execution.

The current go/no-go answer is recorded in
`readiness-closure-scorecard.md`: local readiness controls improved, but runtime
integration remains blocked by legal/licensing clearance, executed rollback
proof, steward-admitted registries, canonical source admission, and separate
impact packets for HIGH/CRITICAL KG roots.

`AEC-BB-S4` adds the report-producing parity runner and a passing report at
`006_System-Manifests/aec-mepfs-backbone/parity/20260425T113719Z/api-explorer-parity-report.json`.
It also adds
`scripts/tests/fixtures/aec_mepfs_backbone/api-explorer-parity-cases.json`
with 14 required parity categories. This closes the local runner/case-evidence
gate, but not future `/v2` runtime route parity after shadow routes exist.

`AEC-BB-S5` adds the rollback preflight runner and a read-only report at
`006_System-Manifests/aec-mepfs-backbone/rollback/20260425T130816Z/rollback-preflight-report.json`.
It confirms the local Neo4j admin surface is available and the live graph is
reachable, but also confirms runtime remains blocked because dump/load require a
stopped or isolated database and no online backup subcommand is available.

`AEC-BB-S6` adds candidate registry files under `registry-candidates/` and a
validation report at
`006_System-Manifests/aec-mepfs-backbone/registry-candidates/20260425T133000Z/registry-candidate-validation-report.json`.
It validates 12 governed predicate rows and 29 first-wave source-rights rows,
but does not make those rows steward-admitted or legally cleared.

Final locked-decision review returned `ITERATE` until L1/L2 home-domain policy,
L3/L4 auto-accept policy, and L1/L2 review thresholds are fully reconciled with
`.ai/03_plans/taxonomy-governance/00_locked_decisions.md`.
