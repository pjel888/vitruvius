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
