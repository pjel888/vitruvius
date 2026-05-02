# Steward Approval Records Report

Date: 2026-05-02T06:03:16Z

This report records scoped action-specific approval records created from the project-owner steward authorization. It is not a blanket approval for fake data, destructive merges, protected payloads, AHJ/numerical claims, or source fabrication.

## dup-5c6457d515c1

- Approval ID: `canonical-approval-20260502055659-b9a6f6b671e2`
- Decision ID: `canonical-20260502055659-9bcef6559923`
- Approved by: `project_owner_steward`
- Reviewer role: `project_owner_steward`
- Approval source: `user_supplied_standing_steward_approval`
- Mutation scope: `non_destructive_edge_admission`
- Status: `admitted`
- Transaction manifest: `canonical-tx-20260502055659-1db3a592dcbf`
- Rationale: Project owner supplied standing steward authorization for high-quality, validated, non-destructive graph improvement. This scoped approval applies only to reciprocal CROSS_DOMAIN_ALIGNMENT between VTN-DOM-0000262 and VTN-DOM-0003013 for Deep Foundations, with no merge, alias, redirect, tombstone, Resource Layer mutation, fake source claim, or protected payload.
- Rollback plan: Rollback by decisionId marks both Deep Foundations admitted relationship records and the scoped approval rolled_back, then reruns canonical, graph relationship, Resource Layer, and latest manifest afterHash validation. No graph nodes or Resource Layer records are deleted or rewritten.

## dup-6400e3e0c204

- Approval ID: `canonical-approval-20260502055700-0109b1ea4688`
- Decision ID: `canonical-20260502055659-59a7c7db99fe`
- Approved by: `project_owner_steward`
- Reviewer role: `project_owner_steward`
- Approval source: `user_supplied_standing_steward_approval`
- Mutation scope: `non_destructive_edge_admission`
- Status: `admitted`
- Transaction manifest: `canonical-tx-20260502055700-16e059859bd5`
- Rationale: Project owner supplied standing steward authorization for high-quality, validated, non-destructive graph improvement. This scoped approval applies only to reciprocal CROSS_DOMAIN_ALIGNMENT between VTN-DOM-0000261 and VTN-DOM-0003010 for Shallow Foundations, with no merge, alias, redirect, tombstone, Resource Layer mutation, fake source claim, or protected payload.
- Rollback plan: Rollback by decisionId marks both Shallow Foundations admitted relationship records and the scoped approval rolled_back, then reruns canonical, graph relationship, Resource Layer, and latest manifest afterHash validation. No graph nodes or Resource Layer records are deleted or rewritten.

## dup-ca1078594013

- Approval ID: `canonical-approval-20260502055700-65171a76c4e6`
- Decision ID: `canonical-20260502055700-8e92ff2fc366`
- Approved by: `project_owner_steward`
- Reviewer role: `project_owner_steward`
- Approval source: `user_supplied_standing_steward_approval`
- Mutation scope: `metadata_only`
- Status: `steward_approved`
- Transaction manifest: `canonical-tx-20260502055700-03aee1feeafc`
- Rationale: Project owner supplied standing steward authorization for high-quality, validated graph stewardship. This scoped approval applies only to metadata-only DISAMBIGUATED_KEEP_SEPARATE for Buildings nodes VTN-DOM-0000716 and VTN-DOM-0000757; it does not admit a production edge or authorize merge, alias, redirect, tombstone, Resource Layer mutation, fake source claim, or protected payload.
- Rollback plan: Rollback by decisionId marks the Buildings metadata-only approval rolled_back and reverts the decision status through the canonical rollback workflow, then reruns canonical, graph relationship, Resource Layer, and latest manifest afterHash validation. No graph nodes, graph edges, or Resource Layer records are deleted or rewritten.

## Post-Kimi implementation-safety repair (2026-05-02T06:20:00Z)

Kimi's final implementation-safety review was accepted. Before commit, the run repaired two custody issues:

- Approval records for Deep Foundations, Shallow Foundations, and Buildings now contain revalidated embedded snapshots with `ok: true` and no embedded false blocker snapshots.
- Buildings remains a metadata-only `DISAMBIGUATED_KEEP_SEPARATE` / governed-disambiguation decision; latent `CROSS_DOMAIN_ALIGNMENT` relationship proposals were cleared and no Buildings graph edge was admitted.
- A new `canonical_approval_metadata_revalidation` transaction manifest (`canonical-tx-20260502061917-f0d21c4f7013`) records the approval/decision metadata repair.
- Current canonical validation: blockers 0; approvals 3; admitted relationships 4; transaction manifests 30; latest afterHash mismatches 0.

Accepted Kimi suggestions: repair failed embedded validation snapshots; remove latent Buildings edge proposals; isolate commit scope. Rejected: none. Deferred: P1 packet custody snapshot refresh after admitted canonical state.
