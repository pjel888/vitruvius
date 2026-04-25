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

## Current Status

Status: accepted readiness-control packet in iteration.

Current implementation status: not ready for runtime architecture work; bounded
validator slice `AEC-BB-S1` is implemented and validated.

No runtime implementation has started from this packet. It authorizes no code
edits, Neo4j cleanup/reset, feature-flag changes, graph rebuilds, backup test
runs, or derived-artifact cleanup.

Readiness-control artifacts for source rights, L1/L2, governance, resolver,
shadow graph safety, API/Explorer parity, predicate registry, and verification
are now accepted as readiness controls. Taxonomy authoring/migration QA and the
Philippines overlay pilot remain draft controls. These artifacts improve
readiness evidence but do not by themselves authorize implementation.

The current scorecard remains conservative because the packet still lacks
independent second review, legal/licensing clearance, parity fixtures, rollback
proof, executable benchmark fixtures, and accepted runtime registries. Fresh
GitNexus evidence also shows HIGH/CRITICAL KG impact roots that must be avoided
or separately planned.

`AEC-BB-S1` added a file-backed validator only. It does not wire Backbone data
into the KG, Neo4j, API, Explorer, feature flags, or graph rebuilds.

Final locked-decision review returned `ITERATE` until L1/L2 home-domain policy,
L3/L4 auto-accept policy, and L1/L2 review thresholds are fully reconciled with
`.ai/03_plans/taxonomy-governance/00_locked_decisions.md`.
