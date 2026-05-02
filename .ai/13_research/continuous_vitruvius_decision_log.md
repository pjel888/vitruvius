# Continuous Vitruvius Decision Log

Last updated: 2026-05-02T01:54:10Z

## Decision: P1 packet signatures are optional custody metadata, not approval

P1 decision packets now support optional HMAC-SHA256 custody signatures using `VITRUVIUS_PACKET_HMAC_KEY` or subsystem-scoped `VITRUVIUS_TRANSACTION_HMAC_KEY`. Without a key, packets are regenerated with `unsigned` signature metadata and canonical validation treats unsigned packets as warnings unless `VITRUVIUS_REQUIRE_PACKET_SIGNATURES=true`.

A valid packet signature only indicates that the stable signature payload matches the configured signing key. It does not prove source truth, ontology truth, steward approval, canonical admission, or merge safety.
