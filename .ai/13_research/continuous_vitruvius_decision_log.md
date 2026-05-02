# Continuous Vitruvius Decision Log

Last updated: 2026-05-02T01:54:10Z

## Decision: P1 packet signatures are optional custody metadata, not approval

P1 decision packets now support optional HMAC-SHA256 custody signatures using `VITRUVIUS_PACKET_HMAC_KEY` or subsystem-scoped `VITRUVIUS_TRANSACTION_HMAC_KEY`. Without a key, packets are regenerated with `unsigned` signature metadata and canonical validation treats unsigned packets as warnings unless `VITRUVIUS_REQUIRE_PACKET_SIGNATURES=true`.

A valid packet signature only indicates that the stable signature payload matches the configured signing key. It does not prove source truth, ontology truth, steward approval, canonical admission, or merge safety.

---

## Decision: latest manifest afterHash checks are custody drift signals, not truth signals

Last updated: 2026-05-02T02:20:03Z

Canonical validation now compares each manifest-governed file to the latest transaction manifest that touched it. Older superseded manifests remain validated for hash-chain/HMAC integrity but are not expected to match current file bytes. Non-strict mode warns on drift. VITRUVIUS_REQUIRE_LATEST_MANIFEST_AFTERHASH=true turns drift on custody-critical manifest-governed files into blockers.

The check indicates byte-level drift since the latest manifest only. It does not prove steward approval, source truth, ontology truth, canonical admission, or merge safety.

---

## 2026-05-02 Resource Layer standards-context decision

Decision: Add a structured, preview-first, dev/admin-gated standards-context cleanup workflow for standard/code-like Resource Layer records. Needs-review/rejected ASCE 7 and ACI 318 records remain warnings/review items; accepted/promoted records missing edition/version, citation/scope, or jurisdiction/geographic scope are blockers. Placeholder context values are rejected. Complete/not-required context decisions require reviewer, rationale, and sourceOfContext.

Rationale: The previous warnings were honest but not actionable. The new workflow lets a real reviewer supply context later without inventing standard editions or silently promoting broad landing-page links.

Consequences: `/dev/resource-review` now exposes standards-context form and diff preview; APIs support detail/preview/apply; production registry data is unchanged until a real gated context decision is applied.

---

## Decision: P1 ontology review metadata is separate advisory custody, not approval

Date: 2026-05-02T04:12:51Z

P1 per-packet ontology reviews are stored in `p1-packet-reviews.json` and referenced to packet hashes. They are advisory only and cannot approve graph mutation. Apply routes write review metadata and a transaction manifest only.


---

## Top P1 packet review decision

Last updated: 2026-05-02T04:58:59Z

Decision: record Kimi packet reviews as advisory review_metadata_only records and use first_graph_admission_queue.md for future steward packet planning; do not create approvals or production graph mutation from P1 review status.
