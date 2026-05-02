# Medium-Risk P1 Steward Packet Kimi Review

Date: 2026-05-02T05:24:16Z

Kimi was asked to review a proposed medium-risk P1 steward admission packet for Buildings, Shallow Foundations, and Deep Foundations. The prompt explicitly stated that the packet does not approve, merge, alias, redirect, tombstone, admit relationships, or mutate the graph.

## Kimi verdict

Advisory-only Kimi review. This is not approval for graph mutation/admission.

Packet is acceptable as a future-review candidate, with safeguards. Relation choices are mostly correct and intentionally non-destructive.

## Candidate findings

### Buildings - dup-ca1078594013

- Recommended future decision: `DISAMBIGUATED_KEEP_SEPARATE` / governed disambiguation.
- Relation: Prefer metadata-only disambiguation. If visible graph relation is later admitted, use two explicit `DISAMBIGUATED_FROM` proposals, not one implied symmetric edge.
- Risk: medium.
- Concern: visible `DISAMBIGUATED_FROM` between broad taxonomy containers may add learner-facing noise. HIS precedent Buildings and FIG works/projects Buildings are clearly separate organizational buckets.
- Too strong: any alias or merge.

### Shallow Foundations - dup-6400e3e0c204

- Recommended future decision: cross-domain alignment candidate.
- Relation: reciprocal `CROSS_DOMAIN_ALIGNMENT` is appropriate; do not use `CROSS_DOMAIN_EQUIVALENT`.
- Risk: medium.
- Rationale: STR node represents structural foundation behavior/design; GEO node represents geotechnical foundation-engineering controls. Same object family, different discipline scopes.
- Too strong: equivalence or merge; alignment is acceptable if phrased as non-identity.

### Deep Foundations - dup-5c6457d515c1

- Recommended future decision: cross-domain alignment candidate.
- Relation: reciprocal `CROSS_DOMAIN_ALIGNMENT` is appropriate.
- Risk: medium.
- Rationale: STR deep foundation node covers structural load/member/cap behavior; GEO node covers investigation/design assumptions/monitoring/construction risk.
- Too strong: merge/equivalence.

## Directionality and symmetry

- `CROSS_DOMAIN_ALIGNMENT` should be reciprocal. Repo validation expects reciprocal pairs for cross-domain alignment.
- `DISAMBIGUATED_FROM` is not inherently symmetric in the same way; if visible relation is wanted, use explicit A-to-B and B-to-A proposals.
- Do not infer parent/child specialization for the foundation pairs; cross-domain peer alignment is safer.

## Human steward approval checklist from Kimi

1. Confirm packet hashes/snapshot are current; unsigned status acknowledged.
2. Confirm both nodes still exist and no production edge already exists.
3. Require real human steward approval; no Kimi/test-fixture approval.
4. Confirm mutation scope is only `non_destructive_edge_admission` or metadata-only.
5. For `CROSS_DOMAIN_ALIGNMENT`, require reciprocal edge preview.
6. For Buildings, prefer metadata-only unless visible disambiguation improves UX.
7. Run dry-run preview, validation snapshot, transaction manifest, rollback plan.
8. Verify Resource Layer unaffected.
9. Verify Explorer graph visibility does not imply equivalence/merge.

## Accepted by Codex

- Use `CROSS_DOMAIN_ALIGNMENT` rather than `CROSS_DOMAIN_EQUIVALENT` for future foundation alignment proposals.
- Require reciprocal foundation alignment proposals.
- Keep Buildings as governed disambiguation/keep-separate and prefer metadata-only unless visible relation improves UX.
- Preserve all no-mutation/no-approval/no-merge guardrails.

## Rejected by Codex

- No Kimi suggestion was rejected as unsafe in this pass.

## Deferred

- Actual steward approval and admission.
- Whether Buildings should receive visible reciprocal `DISAMBIGUATED_FROM` edges or remain metadata-only.
- Learner-facing wording review after graph visibility preview.
