# Continuous Vitruvius Kimi Review Log

Last updated: 2026-05-02T01:54:10Z

## Review: P1 packet HMAC/signature evidence locks

Kimi verdict: accept optional HMAC-SHA256 custody signatures with payload/wording hardening. Kimi stressed that signatures must be framed only as tamper-evident custody/authenticity aids, not steward approval, ontology truth, source quality, or merge safety.

### Accepted suggestions

- Added explicit signature payload version and purpose.
- Included packet run/source batch context, source snapshot schema/hash/stale policy, recommended decision type, merge safety, and non-mutation flags in the signature payload.
- Kept signature fields excluded from packet content hash and signature payload.
- Avoided writing the raw HMAC key or key-derived secret material to packets, logs, API, or UI.
- Used a non-secret key identifier based on the environment variable name and subsystem scope.
- Used timing-safe comparison for HMAC verification.
- Added strict-mode semantics: unsigned/missing-key packets block only when signatures are required; invalid signatures block.
- Kept UI wording clear that signatures are custody metadata only.

### Rejected suggestions

- None rejected outright.

### Deferred suggestions

- Key rotation ledger.
- Multiple signer support.
- Public-key signatures instead of shared-secret HMAC.
- Hardware/OS secret-store integration.
- Joint signing of transaction manifests and packet files.
- Source freshness recrawl signatures.

---

## Review: latest transaction-manifest afterHash enforcement

Last updated: 2026-05-02T02:20:03Z

Kimi verdict: accept latest-manifest-per-file enforcement as a custody-integrity improvement, framed only as “current file still matches the latest transaction manifest afterHash.”

### Accepted suggestions

- Validate the latest manifest per touched file, not every historical afterHash.
- Keep older manifests in hash-chain/HMAC validation even when superseded for current-file comparison.
- Normalize file paths for matching/display and show repo-relative paths in UI.
- Use deterministic ordering by completedAt, startedAt, transactionId, and filename.
- Use non-strict warnings for drift and strict blockers for custody-critical files when VITRUVIUS_REQUIRE_LATEST_MANIFEST_AFTERHASH=true.
- Use UI wording such as “matched latest manifest” and “drift since latest manifest,” not “verified truth,” “approved,” or “safe to merge.”
- Exclude generated reports, .ai logs, caches, lock files, and transaction manifest files themselves from latest afterHash custody checks.

### Rejected suggestions

- None rejected outright.

### Deferred suggestions

- Stable JSON semantic-hash mode in addition to raw byte hash.
- Bootstrap transaction to cover every custody-critical file.
- Cross-subsystem consolidated manifest dashboard.
- Manifest key rotation/signing policy.
- Enforcement for Resource Layer files not yet governed by resource transaction manifests.

---

## Review: Resource Layer standards-context cleanup workflow

Last updated: 2026-05-02T02:58:00Z

Kimi verdict: accept the workflow and keep ASCE 7 / ACI 318 pending until human/source-supported context is supplied.

### Accepted suggestions

- Keep ASCE/ACI missing context as warnings while records remain needs_review or rejected.
- Block accepted/promoted standard/code links missing complete edition/version, citation/scope, and jurisdiction/geographic scope context.
- Reject placeholder values including `latest`, `current`, `unknown`, `TBD`, `varies`, `sample`, empty/whitespace, and unjustified `n/a`.
- Require reviewer, rationale, and sourceOfContext for complete/not-required context decisions.
- Avoid UI wording that implies current edition, governing applicability, approval, or source truth.
- Prefer structured standards context over magic review-note phrases.

### Rejected suggestions

- Using a legacy magic review-note phrase alone as sufficient context for accepted/promoted standard links.

### Deferred suggestions

- External authoritative lookup/recrawl.
- AHJ/adoption effective-date tracking.
- Multi-jurisdiction applicability modeling.
- Full standards evidence-span admission.
- Automatic edition inference from title/URL.

### Final review attempt

A final concise Kimi implementation-review prompt was sent after validation. It did not return before checkpoint/commit timing. The earlier Kimi standards-context review was incorporated, and this timeout is recorded as a deferred final-review artifact rather than hidden.

---

## Review: P1 packet ontology review workflow

Last updated: 2026-05-02T04:12:51Z

Kimi verdict: accept the workflow only if review metadata remains separate, advisory, transaction-manifest-backed, and non-mutating. Kimi warned that `human_reviewed` and `kimi_reviewed` must never be presented as steward approval or graph admission.

### Accepted suggestions

- Store mutable review metadata in a separate manifest-governed registry keyed by packet identifiers and hashes.
- Keep P1 packet custody hashes separate from review metadata.
- Use transaction-manifest-backed writes for review apply.
- Preserve review history and derive current status from the latest valid review record.
- Use UI wording such as ?advisory ontology review,? ?no graph mutation,? and ?needs separate human steward approval.?
- Block review records that claim graph mutation approval or attempt mutation-like state.

### Rejected suggestions

- None rejected outright.

### Deferred suggestions

- Explicit reviewer role/model-run metadata.
- Review file latest-afterHash drift enforcement beyond the existing transaction-manifest path.
- Real steward approval integration.
- Ontology evidence-span review.
- Multi-reviewer quorum.
- Any production graph mutation path.


---

## Review: Top P1 packet ontology review session

Last updated: 2026-05-02T04:58:59Z

Kimi reviewed eight top-priority P1 packets and returned packet-specific classifications. The review was recorded as advisory metadata only through the P1 packet review workflow.

### Accepted suggestions

- Keep all reviewed nodes separate pending future steward action.
- Treat Buildings as governed disambiguation, not alias-only.
- Treat Shallow Foundations, Deep Foundations, and Retaining Wall as possible non-identity cross-domain alignment candidates.
- Treat Shear Wall as possible related-specialization candidate with directionality review.
- Route Load Path, Wall Finishes, Mat Foundation, Shear Wall, and Retaining Wall to human/edge-neighborhood/source review due high risk.

### Rejected suggestions

- No graph mutation, merge, alias, redirect, tombstone, admitted relationship, or steward approval was accepted from Kimi output.
- Alias-only shortcuts were rejected for the reviewed packet set.

### Deferred suggestions

- Any future non-destructive relation proposal, admission review, or steward approval remains deferred to a separate approval-gated loop.
- Source/resource review for Load Path and standard-mapped packets remains deferred.

### Packet-level outcomes

- `p1-decision-packet-fee6fbd9a0fc` / building: `governed_disambiguation_candidate`, risk `medium`. Kimi classifies this as governed disambiguation: the HIS precedent-study bucket and FIG works/projects bucket share a surface label but have different taxonomy roles and edge neighborhoods.
- `p1-decision-packet-fa4918982178` / mat foundation: `needs_edge_neighborhood_review`, risk `high`. Kimi classifies this as cross-domain alignment with high directionality risk: mat or raft foundation spans STR, GEO, and ARC contexts, but the three-node alignment, type mismatch, and standard edge require careful review.
- `p1-decision-packet-d5a20759fdfd` / shallow foundation: `cross_domain_alignment_candidate`, risk `medium`. Kimi classifies this as cross-domain alignment candidate: STR and GEO shallow-foundation nodes likely represent the same engineering object from separate disciplinary views, with different taxonomy contexts and no resource links.
- `p1-decision-packet-9d2ac282265b` / shear wall: `related_specialization_candidate`, risk `high`. Kimi classifies this as related specialization candidate: STR seismic Shear Walls may be a design-topic specialization of ARC Shear Wall as building element, but directionality is risky because STR context is seismic-specific.
- `p1-decision-packet-8a66e785d02a` / deep foundation: `cross_domain_alignment_candidate`, risk `medium`. Kimi classifies this as cross-domain alignment candidate: STR and GEO Deep Foundations nodes likely describe the same class through discipline-specific taxonomies, with low mutation pressure and no resource links.
- `p1-decision-packet-12e81a4fbcde` / retaining wall: `cross_domain_alignment_candidate`, risk `high`. Kimi classifies this as cross-domain alignment candidate: GEO retaining-wall system and ARC building-structural concept are semantically close but discipline-scoped, and the external-standard edge creates directionality and source risk.
- `p1-decision-packet-0cfa6a7f88a1` / wall finishe: `needs_edge_neighborhood_review`, risk `high`. Kimi classifies this as high-risk edge-neighborhood review needed: three Wall Finishes nodes span material finish/product and ARC concept contexts, and duplicate status is unclear from type and taxonomy differences.
- `p1-decision-packet-3946860e327a` / load path: `needs_human_review`, risk `high`. Kimi classifies this as high-risk human review needed: STR subtopic and ARC concept overlap semantically, but node type, taxonomy context, REQUIRES edges, external-standard mappings, and two resource links make mutation unsafe.


## 2026-05-02T05:31:17Z - Medium-risk P1 steward packet critique

Kimi reviewed the proposed Buildings, Shallow Foundations, and Deep Foundations steward packet.

Accepted:
- Reciprocal `CROSS_DOMAIN_ALIGNMENT` for future Shallow/Deep Foundations admission review.
- No `CROSS_DOMAIN_EQUIVALENT`, merge, alias, redirect, tombstone, or graph mutation.
- Buildings should prefer metadata-only governed disambiguation; visible reciprocal `DISAMBIGUATED_FROM` edges are optional future proposals only if a human steward confirms they improve UX.

Rejected:
- None of Kimi's safety suggestions were rejected.

Deferred:
- Actual admission decision.
- Human/steward approval.
- Learner-facing wording/visibility review after future preview.

Full critique: `.ai/13_research/medium_risk_p1_steward_packet_kimi_review.md`.


## 2026-05-02T06:03:16Z - Kimi review for first steward-approved graph admissions

Accepted:
- Deep Foundations reciprocal `CROSS_DOMAIN_ALIGNMENT` has no ontology blocker when scoped to exact edge tuples, with non-identity wording, rollback, and validation.
- Shallow Foundations reciprocal `CROSS_DOMAIN_ALIGNMENT` has no ontology blocker under the same conditions.
- Buildings metadata-only keep-separate is safer than visible `DISAMBIGUATED_FROM` edge admission because both nodes are broad taxonomy containers.

Rejected:
- `CROSS_DOMAIN_EQUIVALENT`, merge, alias, redirect, tombstone, canonical substitution, and source overclaims.
- Any UI/search wording such as equivalent, same-as, duplicate resolved, merged, canonical Buildings, or deprecated.

Deferred:
- Broader STR/GEO foundation alignment batch.
- Visible Buildings disambiguation edge; not admitted in this run.
- Source-backed AEC enrichment and P1 packet snapshot refresh.

## Post-Kimi implementation-safety repair (2026-05-02T06:20:00Z)

Kimi's final implementation-safety review was accepted. Before commit, the run repaired two custody issues:

- Approval records for Deep Foundations, Shallow Foundations, and Buildings now contain revalidated embedded snapshots with `ok: true` and no embedded false blocker snapshots.
- Buildings remains a metadata-only `DISAMBIGUATED_KEEP_SEPARATE` / governed-disambiguation decision; latent `CROSS_DOMAIN_ALIGNMENT` relationship proposals were cleared and no Buildings graph edge was admitted.
- A new `canonical_approval_metadata_revalidation` transaction manifest (`canonical-tx-20260502061917-f0d21c4f7013`) records the approval/decision metadata repair.
- Current canonical validation: blockers 0; approvals 3; admitted relationships 4; transaction manifests 30; latest afterHash mismatches 0.

Accepted Kimi suggestions: repair failed embedded validation snapshots; remove latent Buildings edge proposals; isolate commit scope. Rejected: none. Deferred: P1 packet custody snapshot refresh after admitted canonical state.


## 2026-05-02T07:20:07Z - Kimi review for P1 packet custody snapshot rebase

Accepted:
- Preserve old review hashes as historical evidence while refreshing current packet custody hashes.
- Add explicit carried-forward review lineage and caveats.
- Link consumed packets to scoped approval/admission records.
- Re-sign only with a real HMAC key and avoid exposing/copying secrets.
- Use non-overclaiming UI language: carried forward, consumed by admission, snapshot refreshed.

Rejected:
- Fake re-review, broad approval, old-signature carry-forward, merge/alias/tombstone/source-truth wording, and reopening consumed packets as unresolved active duplicates.

Deferred:
- Fresh Kimi review of changed packets, HMAC-signed regeneration until a real key is configured, and broader P1 review/admission work after this rebase.
