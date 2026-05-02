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
