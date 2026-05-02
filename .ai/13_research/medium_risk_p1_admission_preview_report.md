# Medium-Risk P1 Admission Preview Report

Date: 2026-05-02T05:24:16Z

This report previews possible future non-destructive admission actions for three medium-risk P1 candidates. It performs no mutation and creates no approval.

## Summary matrix

| Candidate | What would be added if approved later | Edge IDs proposed | Symmetric | Reciprocal required | Resource Layer affected | Current blocker |
|---|---|---|---|---|---|---|
| Buildings | metadata-only disambiguation preferred; optional reciprocal visible disambiguation edges | `VTN-DOM-0000716--disambiguated_from--VTN-DOM-0000757`, `VTN-DOM-0000757--disambiguated_from--VTN-DOM-0000716` | not inherent; explicit two-way proposals if visible | only if steward wants visible two-way disambiguation | no | missing real steward approval |
| Shallow Foundations | two reciprocal non-identity alignment edges | `VTN-DOM-0000261--cross_domain_alignment--VTN-DOM-0003010`, `VTN-DOM-0003010--cross_domain_alignment--VTN-DOM-0000261` | yes | yes, validation expects it | no | missing real steward approval |
| Deep Foundations | two reciprocal non-identity alignment edges | `VTN-DOM-0000262--cross_domain_alignment--VTN-DOM-0003013`, `VTN-DOM-0003013--cross_domain_alignment--VTN-DOM-0000262` | yes | yes, validation expects it | no | missing real steward approval |

## Detailed previews

### Buildings

- Packet ID: `p1-decision-packet-fee6fbd9a0fc`
- Group ID: `dup-ca1078594013`
- Source nodes: `VTN-DOM-0000716`, `VTN-DOM-0000757`
- Current review status: `kimi_reviewed`; review risk `medium`; recommended future action `governed_disambiguation_candidate`.
- Packet content hash: `8f16388aa4601c8e6a07c582f53a6982996efc4c1a803fe6aa3e6faecadd3120`; source snapshot hash: `92885969a8cc72d61331742a7f1c995e9b542b881b52487e28decdd94a519f93`; candidate edge neighborhood hash: `7d1a0065bddc6c98d52f13c49205b07d2bc50a9c124220aa135578e42975fd31`.
- Proposed future relation type: `DISAMBIGUATED_FROM`.
- Proposed relation direction/symmetry: Prefer metadata-only disambiguation. If visible relation admission is approved later, propose explicit reciprocal DISAMBIGUATED_FROM edges so the UI can show bidirectional disambiguation without implying identity.
- Rationale to attach if approved later: The HIS precedent-study bucket and FIG works/projects bucket share a surface label but represent distinct taxonomy-context containers with very different child neighborhoods.
- Proposed edge IDs if approved later: `VTN-DOM-0000716--disambiguated_from--VTN-DOM-0000757`, `VTN-DOM-0000757--disambiguated_from--VTN-DOM-0000716`
- Existing matching production graph edge IDs now: `0`.
- Would this be metadata-only or production graph edge admission? This packet is metadata/report-only. A future approved loop may choose metadata-only for Buildings, and production graph edge admission for the foundation alignment pairs.
- Validation rules for future admission: existing node IDs, admissible relation type, no self-loop, no duplicate existing tuple, reciprocal pair for `CROSS_DOMAIN_ALIGNMENT`, real approval, transaction manifest, rollback preview, canonical validation, graph relationship validation, Resource Layer validation.
- Transaction manifest files future admission would likely touch: `006_System-Manifests/graph-canonical/approvals.json`, `006_System-Manifests/graph-canonical/admitted-relationships.json`, `006_System-Manifests/graph-canonical/stewardship-decisions.json` if decision status changes, and a new `006_System-Manifests/graph-canonical/transaction-manifests/*.json` manifest. This run touches none of those registry files.
- Rollback preview: remove or mark rolled-back admitted relationship records for the transaction, rerun canonical validation, confirm node/resource counts unchanged, and verify latest afterHash custody for touched files.
- Resource Layer preservation preview: no candidate node has nodeResourceLinks now; future admission must still assert resources, nodeResourceLinks, review decisions, candidates, local files, and standards context are unchanged.
- Graph visibility preview: after future admission, selected-node neighborhood should include the visible stewardship edge and Explorer dynamic filters should not hide the relation type.
- What could go wrong: stale packet hash, missing approval, accidental equivalence wording, missing reciprocal alignment, duplicate existing edge tuple, learner-facing confusion, or unintended Resource Layer rewrite.
- What should block admission: no real approval, any request to merge/alias/redirect/tombstone, proposed `CROSS_DOMAIN_EQUIVALENT`, one-way foundation alignment, self-loop/missing node, graph validation failure, Resource Layer validation failure, or transaction manifest/rollback failure.

### Shallow Foundations

- Packet ID: `p1-decision-packet-d5a20759fdfd`
- Group ID: `dup-6400e3e0c204`
- Source nodes: `VTN-DOM-0000261`, `VTN-DOM-0003010`
- Current review status: `kimi_reviewed`; review risk `medium`; recommended future action `cross_domain_alignment_candidate`.
- Packet content hash: `d723c0b32a052cc8bbfd6387f6e03bc30becfc70a6542a1ffc775ca32395cc46`; source snapshot hash: `92885969a8cc72d61331742a7f1c995e9b542b881b52487e28decdd94a519f93`; candidate edge neighborhood hash: `4bcd860c191fbca419662a911c9e95014c1312c5bf8a24e90f3d5a1ca0a607db`.
- Proposed future relation type: `CROSS_DOMAIN_ALIGNMENT`.
- Proposed relation direction/symmetry: Symmetric cross-domain peer alignment. Current validation expects reciprocal edge proposals for CROSS_DOMAIN_ALIGNMENT.
- Rationale to attach if approved later: The STR node captures structural shallow-foundation behavior/design topics; the GEO node captures geotechnical foundation-engineering controls for the same object family.
- Proposed edge IDs if approved later: `VTN-DOM-0000261--cross_domain_alignment--VTN-DOM-0003010`, `VTN-DOM-0003010--cross_domain_alignment--VTN-DOM-0000261`
- Existing matching production graph edge IDs now: `0`.
- Would this be metadata-only or production graph edge admission? This packet is metadata/report-only. A future approved loop may choose metadata-only for Buildings, and production graph edge admission for the foundation alignment pairs.
- Validation rules for future admission: existing node IDs, admissible relation type, no self-loop, no duplicate existing tuple, reciprocal pair for `CROSS_DOMAIN_ALIGNMENT`, real approval, transaction manifest, rollback preview, canonical validation, graph relationship validation, Resource Layer validation.
- Transaction manifest files future admission would likely touch: `006_System-Manifests/graph-canonical/approvals.json`, `006_System-Manifests/graph-canonical/admitted-relationships.json`, `006_System-Manifests/graph-canonical/stewardship-decisions.json` if decision status changes, and a new `006_System-Manifests/graph-canonical/transaction-manifests/*.json` manifest. This run touches none of those registry files.
- Rollback preview: remove or mark rolled-back admitted relationship records for the transaction, rerun canonical validation, confirm node/resource counts unchanged, and verify latest afterHash custody for touched files.
- Resource Layer preservation preview: no candidate node has nodeResourceLinks now; future admission must still assert resources, nodeResourceLinks, review decisions, candidates, local files, and standards context are unchanged.
- Graph visibility preview: after future admission, selected-node neighborhood should include the visible stewardship edge and Explorer dynamic filters should not hide the relation type.
- What could go wrong: stale packet hash, missing approval, accidental equivalence wording, missing reciprocal alignment, duplicate existing edge tuple, learner-facing confusion, or unintended Resource Layer rewrite.
- What should block admission: no real approval, any request to merge/alias/redirect/tombstone, proposed `CROSS_DOMAIN_EQUIVALENT`, one-way foundation alignment, self-loop/missing node, graph validation failure, Resource Layer validation failure, or transaction manifest/rollback failure.

### Deep Foundations

- Packet ID: `p1-decision-packet-8a66e785d02a`
- Group ID: `dup-5c6457d515c1`
- Source nodes: `VTN-DOM-0000262`, `VTN-DOM-0003013`
- Current review status: `kimi_reviewed`; review risk `medium`; recommended future action `cross_domain_alignment_candidate`.
- Packet content hash: `5469654cd4d3c42d4d4717a05bedd316678b846de62fb7e331b8b6832d3cbea7`; source snapshot hash: `92885969a8cc72d61331742a7f1c995e9b542b881b52487e28decdd94a519f93`; candidate edge neighborhood hash: `dde9ff4db95effe4049582168f74b7135d8184ecb391bbeef00bde22b145d885`.
- Proposed future relation type: `CROSS_DOMAIN_ALIGNMENT`.
- Proposed relation direction/symmetry: Symmetric cross-domain peer alignment. Current validation expects reciprocal edge proposals for CROSS_DOMAIN_ALIGNMENT.
- Rationale to attach if approved later: The STR node covers structural load/member/cap behavior; the GEO node covers investigation, assumptions, monitoring, construction risk, and long-term performance for the same foundation class.
- Proposed edge IDs if approved later: `VTN-DOM-0000262--cross_domain_alignment--VTN-DOM-0003013`, `VTN-DOM-0003013--cross_domain_alignment--VTN-DOM-0000262`
- Existing matching production graph edge IDs now: `0`.
- Would this be metadata-only or production graph edge admission? This packet is metadata/report-only. A future approved loop may choose metadata-only for Buildings, and production graph edge admission for the foundation alignment pairs.
- Validation rules for future admission: existing node IDs, admissible relation type, no self-loop, no duplicate existing tuple, reciprocal pair for `CROSS_DOMAIN_ALIGNMENT`, real approval, transaction manifest, rollback preview, canonical validation, graph relationship validation, Resource Layer validation.
- Transaction manifest files future admission would likely touch: `006_System-Manifests/graph-canonical/approvals.json`, `006_System-Manifests/graph-canonical/admitted-relationships.json`, `006_System-Manifests/graph-canonical/stewardship-decisions.json` if decision status changes, and a new `006_System-Manifests/graph-canonical/transaction-manifests/*.json` manifest. This run touches none of those registry files.
- Rollback preview: remove or mark rolled-back admitted relationship records for the transaction, rerun canonical validation, confirm node/resource counts unchanged, and verify latest afterHash custody for touched files.
- Resource Layer preservation preview: no candidate node has nodeResourceLinks now; future admission must still assert resources, nodeResourceLinks, review decisions, candidates, local files, and standards context are unchanged.
- Graph visibility preview: after future admission, selected-node neighborhood should include the visible stewardship edge and Explorer dynamic filters should not hide the relation type.
- What could go wrong: stale packet hash, missing approval, accidental equivalence wording, missing reciprocal alignment, duplicate existing edge tuple, learner-facing confusion, or unintended Resource Layer rewrite.
- What should block admission: no real approval, any request to merge/alias/redirect/tombstone, proposed `CROSS_DOMAIN_EQUIVALENT`, one-way foundation alignment, self-loop/missing node, graph validation failure, Resource Layer validation failure, or transaction manifest/rollback failure.

## Non-mutation checks

- Production graph edge count expected to remain `13,670`.
- Approvals expected to remain `0`.
- Admitted relationships expected to remain `0`.
- Aliases, redirects, tombstones expected to remain `0 / 0 / 0`.
- Resources and nodeResourceLinks expected to remain `7 / 9`.