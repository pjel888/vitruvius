# CROSS_DOMAIN Relationship Naming Report

Date: 2026-05-02

## Problem

The previous P0 loop recorded proposed Reinforced Concrete cross-domain relationships as `CROSS_DOMAIN_EQUIVALENT`. Kimi and implementation review flagged this as too strong because "equivalent" can imply identity and encourage unsafe merge/canonicalization.

## Decision

For any admitted production stewardship relationship, use `CROSS_DOMAIN_ALIGNMENT` instead of `CROSS_DOMAIN_EQUIVALENT`.

## Semantics

`CROSS_DOMAIN_ALIGNMENT` means two concepts are related across taxonomy or discipline contexts and should be navigable together, but the relation does not imply:
- identical concept identity,
- safe merge,
- canonical redirect,
- alias equivalence,
- transitive equivalence,
- source-backed external standard equivalence.

## Compatibility behavior

- Existing proposed records are not destructively rewritten in this loop.
- Admission preview and admission normalize proposed `CROSS_DOMAIN_EQUIVALENT` to `CROSS_DOMAIN_ALIGNMENT`.
- Validation blocks any active admitted relationship whose type remains `CROSS_DOMAIN_EQUIVALENT`.
- For bidirectional/cross-domain alignment, validation requires reciprocal admitted edges when explicit reciprocal edges are used.

## Kimi review summary

Accepted:
- Avoid `CROSS_DOMAIN_EQUIVALENT` for admitted production edges.
- Prefer `CROSS_DOMAIN_ALIGNMENT` with non-identity semantics.
- Treat the relation as symmetric for navigation while preventing merge/canonicalization inference.

Rejected:
- `CLOSE_MATCH`/`RELATED_MATCH` for this loop because they are either too SKOS-adjacent without a full SKOS mapping policy or too generic for discipline-context alignment.

Deferred:
- A full relation domain/range registry and external mapping policy.
- Migration/supersession of the old proposed metadata record; it remains proposed-only and is normalized at admission.
