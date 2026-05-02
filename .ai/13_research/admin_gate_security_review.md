# Admin Gate Security Review

Date: 2026-05-01 23:08:42 +08:00

## Implemented mutation gate

Mutation routes now require one of:

- non-production local/dev/test mode,
- VITRUVIUS_ENABLE_DEV_ADMIN=true with local request hostname,
- valid VITRUVIUS_ADMIN_TOKEN supplied through x-vitruvius-admin-token or Authorization: Bearer.

Production without a valid token blocks mutation routes with 403. Read-only canonical and resource review routes remain available.

## Improvements in this loop

- Token comparison uses 	imingSafeEqual on equal-length buffers.
- Canonical and Resource Layer manifests use subsystem-scoped HMAC derivation when VITRUVIUS_TRANSACTION_HMAC_KEY is configured.
- HMAC signs the stable manifest payload rather than only signing the manifest hash.
- Canonical validation checks manifest hash-chain and HMAC mismatch when a key is configured.

## Kimi review accepted

- Constant-time token comparison.
- Subsystem-scoped HMAC keys.
- HMAC over stable payload.

## Kimi review deferred

- Binding local gate to server socket origin instead of request URL hostname.
- Rate limiting/backoff/audit log for failed admin attempts.
- Strong cross-process advisory lock implementation.

## Residual security boundary

This is not a full production auth system. It is a safer mutation gate for local/dev and token-gated deployments. Public production deployment should still add real auth, CSRF protection, rate limiting, and auditable identity.
