# Concrete Governed Disambiguation Report

Date: 2026-05-01

## Outcome

The P0 concrete groups were not merged. This loop recorded proposed-only governed disambiguation decisions so the review UI/search can explain ambiguity while preserving all graph and Resource Layer data unchanged.

## Concrete

`VTN-DOM-0000068` and `VTN-DOM-0000267` share the normalized label `concrete`, but their taxonomy contexts differ:

- `VTN-DOM-0000068`: broad materials topic `MAT > MAT.CON`.
- `VTN-DOM-0000267`: structural-material subtopic `STR > STR.MAT > STR.MAT.CON`.

Decision record `canonical-20260501155958-e011dc288980` is `DISAMBIGUATED_KEEP_SEPARATE`, status `proposed`. It proposes a non-admitted `RELATED_SPECIALIZATION_OF` relationship from structural concrete to broad material concrete.

## Reinforced concrete

`VTN-DOM-0000271` and `VTN-DOM-0012147` share the normalized label `reinforced concrete`, but their role and relationship neighborhoods differ:

- `VTN-DOM-0000271`: structural-system subtopic `STR > STR.CON > STR.CON.RCO`.
- `VTN-DOM-0012147`: architecture/material concept `ARC > ARC.MAT > ARC.MAT.CON > ARC.MAT.CON.RCC` with a dense semantic neighborhood.

Decision record `canonical-20260501155958-f8da3711275f` is `CROSS_DOMAIN_EQUIVALENCE`, status `proposed`. It proposes bidirectional cross-domain alignment relationships but does not assert identity or merge eligibility.

## Kimi review notes

- Concrete: accepted keep-separate and structural-to-material specialization framing; rejected merge/alias.
- Reinforced concrete: accepted cross-domain alignment; rejected destructive merge and edge migration.
- Disambiguation relationships: accepted proposed-only status; warned that `CROSS_DOMAIN_EQUIVALENT` is semantically strong and should not be treated as identity.
- Final review: accepted no blocking safety issue; emphasized not to call P0 resolved.

## Human steward next step

Review the two proposed decisions in `/dev/canonical-review`. If approved, decide whether relation vocabulary should be renamed to `CROSS_DOMAIN_ALIGNMENT` or similar before any production edge admission.
