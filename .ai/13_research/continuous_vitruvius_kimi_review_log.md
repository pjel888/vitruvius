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
