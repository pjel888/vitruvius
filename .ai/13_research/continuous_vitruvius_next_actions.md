# Continuous Vitruvius Next Actions

Last updated: 2026-05-02T07:20:07Z

## Immediate next action

Continue remaining P1 reviews: select 3 to 5 unreviewed P1 packets, obtain Kimi ontology review, record advisory review metadata, and queue only low/medium-risk non-destructive candidates for future scoped steward-approved admission.

## Priority queue

1. Continue P1 reviews for unreviewed packets without shallow-reviewing all remaining packets.
2. Prepare/admit next low/medium-risk non-destructive P1 candidates only after Kimi review, dry-run, validation, rollback preview, and visibility checks.
3. Keep high-risk/source-sensitive packets gated for source and edge-neighborhood review.
4. Consider P0 Concrete/Reinforced Concrete only as non-destructive disambiguation/alignment first; no blind merge.
5. Begin broader AEC relationship-enrichment batch only when existing nodes, relation vocabulary, and source/reasoning evidence are explicit.

## Persistent blockers / caveats

- No real HMAC key is configured; P1 packets remain unsigned.
- ASCE 7 and ACI 318 context values must not be invented.
- Unrelated AEC files/artifacts remain dirty and should stay out of the P1 snapshot rebase commit.


## 2026-05-02T07:58:28Z - Next actions

1. Finish broad validation for the current review-only changes.
2. Review relation vocabulary options for the accepted ACS candidates, especially candidates that can safely reuse existing `constrains` or `requires`.
3. Continue P1 reviews for the seven remaining unreviewed packets if no ACS candidate can pass vocabulary/source-context gates.
4. Keep Shear Wall, Retaining Wall, Mat Foundation, Wall Finishes, and Load Path gated until source/edge-neighborhood review clears specific blockers.
