# Continuous Vitruvius Quality Report

Date: 2026-05-03T02:45:00+08:00
Baseline admitted relationships: 264
Final admitted relationships: 264
New admitted relationships: 0
Baseline effective edges: 13,934
Final effective edges: 13,934
Base graph edges: 13,670 unchanged
Nodes: 10,018 unchanged
Approvals: 16
Transaction manifests: 84
Latest afterHash mismatches: 0
Aliases/redirects/tombstones: 0/0/0
Resources/nodeResourceLinks: 7/9 unchanged

## Quality Gates

- Existing nodes only: passed.
- Existing admitted relation vocabulary only: passed.
- Duplicate base/overlay edge check: passed for all 264 admitted edges.
- Source/context gate: passed for all admitted edges.
- Kimi review: completed; no new admissions in this loop.
- Graph visibility: passed for all edges.
- No Resource Layer mutation: confirmed.
- No merge/alias/redirect/tombstone: confirmed.
- P1 packet hash integrity: 0 mismatches, 0 stale reviews.
- Manifest chain: valid.
- Reasoning-path tests: 18/18 pass.
- Relation-family count: 15 active (corrected from erroneous 16).
- COORDINATES_WITH dominance: 46.6% (within threshold).
- CROSS_DOMAIN_EQUIVALENT active edges: 0 (blocked).
- related_to active edges: 0 (blocked).
- Duplicate-base-edge test normalization: fixed.
- Fire/egress rationale review: completed; queued for future metadata repair.
- COORDINATES_WITH NEEDS_REVIEW follow-up: 2 edges reclassified as PASS_WITH_MINOR_CAVEAT.
- High-risk P1 gating: confirmed blocked.
- Traceability gaps: documented; no action required at current scale.

## Phase 5 Audit Remediation Artifacts

- State verification: `.ai/13_research/phase5_audit_remediation_state_verification.md`
- Worktree remediation: `.ai/13_research/phase5_worktree_remediation_report.md`
- Report reconciliation: `.ai/13_research/phase5_report_snapshot_reconciliation.md`
- Duplicate base edge test fix: `.ai/13_research/phase5_duplicate_base_edge_test_fix_report.md`
- Reasoning path test hardening: `.ai/13_research/phase5_reasoning_path_test_hardening_report.md`
- Fire/egress rationale review: `.ai/13_research/phase5_fire_egress_rationale_review.md`
- COORDINATES_WITH follow-up: `.ai/13_research/phase5_coordinates_with_needs_review_followup.md`
- Traceability gap review: `.ai/13_research/phase5_traceability_gap_review.md`
- High-risk gating confirmation: `.ai/13_research/phase5_high_risk_packet_gating_confirmation.md`
